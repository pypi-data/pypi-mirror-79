import math
import torch
import warnings

from argus.callbacks import Callback
from argus.engine import State


METRIC_REGISTRY = {}


def init_better(better: str, monitor: str) -> tuple:
    if better not in ['min', 'max', 'auto']:
        raise ValueError(f"Unknown better option '{better}'")

    if better == 'auto':
        if monitor.startswith('val_'):
            metric_name = monitor[len('val_'):]
        else:
            metric_name = monitor[len('train_'):]
        if metric_name not in METRIC_REGISTRY:
            raise ImportError(f"Metric '{metric_name}' not found in scope")
        better = METRIC_REGISTRY[metric_name].better

    if better == 'min':
        better_comp = lambda a, b: a < b
        best_value = math.inf
    else:  # better == 'max':
        better_comp = lambda a, b: a > b
        best_value = -math.inf

    return better, better_comp, best_value


class MetricMeta(type):
    def __new__(mcs, name, bases, attrs, *args, **kwargs):
        new_class = super().__new__(mcs, name, bases, attrs)
        metric_name = attrs['name']
        if metric_name:
            if metric_name in METRIC_REGISTRY:
                current_class = f"<class '{attrs['__module__']}.{attrs['__qualname__']}'>"
                warnings.warn(f"{current_class} redefined '{metric_name}' "
                              f"that was already registered by {METRIC_REGISTRY[metric_name]}")
            METRIC_REGISTRY[metric_name] = new_class
        return new_class


class Metric(Callback, metaclass=MetricMeta):
    name: str = ''
    better: str = 'min'

    def reset(self):
        pass

    def update(self, step_output: dict):
        pass

    def compute(self):
        pass

    def epoch_start(self, state: State):
        self.reset()

    def iteration_complete(self, state: State):
        self.update(state.step_output)

    def epoch_complete(self, state: State):
        with torch.no_grad():
            score = self.compute()
        name_prefix = f"{state.phase}_" if state.phase else ''
        state.metrics[name_prefix + self.name] = score
