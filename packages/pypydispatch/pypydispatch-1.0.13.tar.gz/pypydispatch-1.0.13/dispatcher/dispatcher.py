import sys
import threading
import weakref
import inspect
from celery.execute import send_task   # pylint: disable=import-error,no-name-in-module

from .weakref_backports import WeakMethod
from . import const


def func_accepts_kwargs(func):
    return any(
        p for p in inspect.signature(func).parameters.values()
        if p.kind == p.VAR_KEYWORD
    )


def _make_id(target):
    if not inspect.isfunction(target):
        raise Exception("receiver must be function")
    custom_name = getattr(target, 'dispatch_uid', '')
    if custom_name:
        return custom_name
    return ':'.join([target.__module__, target.__name__])


def _make_lookup_key(receiver, target):
    return [_make_id(receiver), target]


NONE_ID = None

# A marker for caching
NO_RECEIVERS = object()

DEBUG = False


class Signal(object):
    """
    Base class for all signals

    Internal attributes:

        receivers
            { receiverkey (id) : weakref(receiver) }
    """
    ALL_SIGNALS = dict()

    def __init__(self, name, providing_args=None, use_caching=False):
        """
        Create a new signal.

        providing_args
            A list of the arguments this signal can pass along in a send() call.
        """
        self.name = name
        _signal = self.get_by_name(name)
        if _signal:
            raise Exception('already registered signal "%s"' % name)

        self.ALL_SIGNALS[name] = self

        self.receivers = []
        if providing_args is None:
            providing_args = []
        self.providing_args = set(providing_args)
        self.lock = threading.Lock()
        self.use_caching = use_caching
        # For convenience we create empty caches even if they are not used.
        # A note about caching: if use_caching is defined, then for each
        # distinct sender we cache the receivers that sender has in
        # 'sender_receivers_cache'. The cache is cleaned when .connect() or
        # .disconnect() is called and populated on send().
        self.sender_receivers_cache = weakref.WeakKeyDictionary() if use_caching else {}
        self._dead_receivers = False

    @classmethod
    def get_by_name(cls, name):
        return cls.ALL_SIGNALS.get(name)

    def connect(self, receiver, sender=None, weak=True):
        """
        Connect receiver to sender for signal.

        Arguments:

            receiver
                A function or an instance method which is to receive signals.
                Receivers must be hashable objects.

                If weak is True, then receiver must be weak referenceable.

                Receivers must be able to accept keyword arguments.

            sender
                The sender to which the receiver should respond. Must either be
                a Python object, or None to receive events from any sender.

            weak
                Whether to use weak references to the receiver. By default, the
                module will attempt to use weak references to the receiver
                objects. If this parameter is false, then strong references will
                be used.
        """
        # If DEBUG is on, check that we got a good receiver
        if DEBUG:
            assert callable(receiver), "Signal receivers must be callable."

            # Check for **kwargs
            if not func_accepts_kwargs(receiver):
                raise ValueError("Signal receivers must accept keyword arguments (**kwargs).")

        lookup_key = _make_lookup_key(receiver, sender)

        if weak:
            ref = weakref.ref
            # Check for bound methods
            if hasattr(receiver, '__self__') and hasattr(receiver, '__func__'):
                ref = WeakMethod
            receiver = ref(receiver, self._remove_receiver)

        with self.lock:
            self._clear_dead_receivers()
            for r_key, _ in self.receivers:
                if r_key == lookup_key:
                    raise Exception("Already exisit receiver {}".format(r_key))
            else:
                self.receivers.append((lookup_key, receiver))
            self.sender_receivers_cache.clear()

    def disconnect(self, receiver, sender=None, weak=None):
        """
        Disconnect receiver from sender for signal.

        If weak references are used, disconnect need not be called. The receiver
        will be remove from dispatch automatically.

        Arguments:

            receiver
                The registered receiver to disconnect.

            sender
                The registered sender to disconnect
        """
        lookup_key = _make_lookup_key(receiver, sender)

        disconnected = False
        with self.lock:
            self._clear_dead_receivers()
            for index in range(len(self.receivers)):
                (r_key, _) = self.receivers[index]
                if r_key == lookup_key:
                    disconnected = True
                    del self.receivers[index]
                    break
            self.sender_receivers_cache.clear()
        return disconnected

    def has_listeners(self, sender=None):
        return bool(self._live_receivers(sender))

    def send_async(self, sender, options=None, **named):
        options = options or {}
        send_task(const.TASK_NAME, args=(self.name, sender), kwargs=named, **options)

    def send(self, sender, **named):
        """
        Send signal from sender to all connected receivers.

        If any receiver raises an error, the error propagates back through send,
        terminating the dispatch loop. So it's possible that all receivers
        won't be called if an error is raised.

        Arguments:

            sender
                The sender of the signal. Either a specific object or None.

            named
                Named arguments which will be passed to receivers.

        Returns a list of tuple pairs [(receiver, response), ... ].
        """
        if not self.receivers or self.sender_receivers_cache.get(sender) is NO_RECEIVERS:
            return []

        return [
            (_make_lookup_key(receiver, sender), receiver(signal=self, sender=sender, **named))
            for receiver in self._live_receivers(sender)
        ]

    def send_to_target_receiver(self, sender, receiver_key, **named):
        """
        Send signal from sender to target receiver catching error.
        return (receiver_key, response)
        """
        for receiver in self._live_receivers(sender):
            lookup_key = _make_lookup_key(receiver, sender)
            if lookup_key == receiver_key:
                try:
                    response = receiver(signal=self, sender=sender, **named)
                except Exception as err:
                    if not hasattr(err, '__traceback__'):
                        err.__traceback__ = sys.exc_info()[2]
                    return (lookup_key, err)
                else:
                    return (lookup_key, response)
                break
        return None


    def send_robust(self, sender, finished_receivers=None, **named):
        """
        Send signal from sender to all connected receivers catching errors.

        Arguments:

            sender
                The sender of the signal. Can be any python object (normally one
                registered with a connect if you actually want something to
                occur).

            named
                Named arguments which will be passed to receivers. These
                arguments must be a subset of the argument names defined in
                providing_args.

        Return a list of tuple pairs [(receiver, response), ... ]. May raise
        DispatcherKeyError.

        If any receiver raises an error (specifically any subclass of
        Exception), the error instance is returned as the result for that
        receiver. The traceback is always attached to the error at
        ``__traceback__``.
        """
        if not self.receivers or self.sender_receivers_cache.get(sender) is NO_RECEIVERS:
            return []

        # Call each receiver with whatever arguments it can accept.
        # Return a list of tuple pairs [(receiver, response), ... ].
        responses = []
        for receiver in self._live_receivers(sender):
            lookup_key = _make_lookup_key(receiver, sender)
            # skip finished receivers
            if finished_receivers and lookup_key in finished_receivers:
                continue

            try:
                response = receiver(signal=self, sender=sender, **named)
            except Exception as err:
                if not hasattr(err, '__traceback__'):
                    err.__traceback__ = sys.exc_info()[2]
                responses.append((lookup_key, err))
            else:
                responses.append((lookup_key, response))
        return responses

    def _clear_dead_receivers(self):
        # Note: caller is assumed to hold self.lock.
        if self._dead_receivers:
            self._dead_receivers = False
            new_receivers = []
            for r in self.receivers:
                if isinstance(r[1], weakref.ReferenceType) and r[1]() is None:
                    continue
                new_receivers.append(r)
            self.receivers = new_receivers

    def live_receiver_keys(self, sender):
        keys = []
        for receiver in self._live_receivers(sender):
            lookup_key = _make_lookup_key(receiver, sender)
            keys.append(lookup_key)
        return keys

    def _live_receivers(self, sender):
        """
        Filter sequence of receivers to get resolved, live receivers.

        This checks for weak references and resolves them, then returning only
        live receivers.
        """
        receivers = None
        if self.use_caching and not self._dead_receivers:
            receivers = self.sender_receivers_cache.get(sender)
            # We could end up here with NO_RECEIVERS even if we do check this case in
            # .send() prior to calling _live_receivers() due to concurrent .send() call.
            if receivers is NO_RECEIVERS:
                return []
        if receivers is None:
            with self.lock:
                self._clear_dead_receivers()
                senderkey = sender
                receivers = []
                for (_, r_senderkey), receiver in self.receivers:
                    if r_senderkey == NONE_ID or r_senderkey == senderkey:
                        receivers.append(receiver)
                if self.use_caching:
                    if not receivers:
                        self.sender_receivers_cache[sender] = NO_RECEIVERS
                    else:
                        # Note, we must cache the weakref versions.
                        self.sender_receivers_cache[sender] = receivers
        non_weak_receivers = []
        for receiver in receivers:
            if isinstance(receiver, weakref.ReferenceType):
                # Dereference the weak reference.
                receiver = receiver()
                if receiver is not None:
                    non_weak_receivers.append(receiver)
            else:
                non_weak_receivers.append(receiver)
        return non_weak_receivers

    def _remove_receiver(self, receiver=None):
        # Mark that the self.receivers list has dead weakrefs. If so, we will
        # clean those up in connect, disconnect and _live_receivers while
        # holding self.lock. Note that doing the cleanup here isn't a good
        # idea, _remove_receiver() will be called as side effect of garbage
        # collection, and so the call can happen while we are already holding
        # self.lock.
        self._dead_receivers = True


def receiver(signal, **kwargs):
    """
    A decorator for connecting receivers to signals. Used by passing in the
    signal (or list of signals) and keyword arguments to connect::

        @receiver(post_save, sender=MyModel)
        def signal_receiver(sender, **kwargs):
            ...

        @receiver([post_save, post_delete], sender=MyModel)
        def signals_receiver(sender, **kwargs):
            ...
    """
    def _decorator(func):
        if 'dispatch_uid' in kwargs:
            func.dispatch_uid = kwargs.pop('dispatch_uid')

        if isinstance(signal, (list, tuple)):
            for s in signal:
                s.connect(func, **kwargs)
        else:
            signal.connect(func, **kwargs)
        return func
    return _decorator
