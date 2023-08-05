"""Base class for Callbacks.
"""

from typing import Callable

from argus.utils import inheritors
from argus.engine import Events, EventEnum


class Callback:
    """Base callback class.

    Raises:
        TypeError: Attribute is not callable.

    """

    def attach(self, engine, handler_kwargs_dict=None):
        if handler_kwargs_dict is None:
            handler_kwargs_dict = dict()

        for event_enum in inheritors(EventEnum):
            for key, event in event_enum.__members__.items():
                if hasattr(self, event.value):
                    handler = getattr(self, event.value)
                    if isinstance(handler, Callable):
                        handler_kwargs = handler_kwargs_dict.get(event, dict())
                        engine.add_event_handler(event, handler, **handler_kwargs)
                    else:
                        raise TypeError(f"Attribute {event.value} is not callable.")


class FunctionCallback(Callback):
    def __init__(self, event: EventEnum, handler):
        self.event = event
        self.handler = handler

    def attach(self, engine, *args, **kwargs):
        engine.add_event_handler(self.event, self.handler, *args, **kwargs)


def on_event(event):
    def wrap(func):
        return FunctionCallback(event, func)
    return wrap


def on_start(func):
    return FunctionCallback(Events.START, func)


def on_complete(func):
    return FunctionCallback(Events.COMPLETE, func)


def on_epoch_start(func):
    return FunctionCallback(Events.EPOCH_START, func)


def on_epoch_complete(func):
    return FunctionCallback(Events.EPOCH_COMPLETE, func)


def on_iteration_start(func):
    return FunctionCallback(Events.ITERATION_START, func)


def on_iteration_complete(func):
    return FunctionCallback(Events.ITERATION_COMPLETE, func)


def on_catch_exception(func):
    return FunctionCallback(Events.CATCH_EXCEPTION, func)
