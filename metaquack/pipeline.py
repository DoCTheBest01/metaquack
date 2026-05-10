import sys, time
import numpy as np
from colorama import Fore, Style

class State:
    def __init__(self, population, objective=None):
        self.population = population  # shape: (N, D)
        self.objective = objective        # shape: (N,)

    def copy(self):
        return State(
            population=self.population.copy(),
            objective=None if self.objective is None else self.objective.copy()
        )

class ProgressBar:
    def __init__(self, total, length=30):
        self.total = total
        self.length = length

    def update(self, current):
        percent = current / self.total * 100
        bar_len = int(self.length * current / self.total)
        bar = Fore.GREEN+Style.DIM+'—' * bar_len + '>' + Fore.RESET+Style.RESET_ALL
        space = ' ' * (self.length - bar_len)
        print(f"|{bar}{space}| {percent:5.1f}%", end='\r', flush=True)

    def finish(self):
        print()

class Pipeline:
    def __init__(self, operators=None):
        self.operators = operators or []
        self._repeat = 1

    def __rshift__(self, other):
        if isinstance(other, Pipeline):
            return Pipeline(self.operators + other.operators)
        return Pipeline(self.operators + [other])

    def repeat(self, n):
        self._repeat = n
        return self

    def run(self, state=None, verbose=True):
        for i in range(self._repeat):
            if verbose:
                pb = ProgressBar(total=len(self.operators))
                print(f"\nIteration {i+1}/{self._repeat}:")
            for j, op in enumerate(self.operators):
                state = op.apply(state)
                if verbose:
                    pb.update(j + 1)
            if verbose:
                pb.finish()
                if state.objective is not None:
                    print(f"  Best fitness: {state.objective.min()}")
        return state

class Operator:
    def apply(self, state):
        raise NotImplementedError("Operator subclasses must implement an `apply` method")

    def __rshift__(self, other):
        return Pipeline([self]) >> other

class Initialize(Operator):
    def __init__(self, fields, count):
        self.fields = fields
        self.count = count

    def apply(self, state=None):
        D = len(self.fields)
        population = np.zeros((self.count, D))

        for d, field in enumerate(self.fields):
            population[:, d] = field.generate(self.count)

        return State(population)

class Evaluate(Operator):
    def __init__(self, objective_function):
        self.objective_function = objective_function

    def apply(self, state):
        try:
            # try batch
            state.objective = self.objective_function(state.population)
        except:
            # fallback
            state.objective = np.array([
                self.objective_function(ind)
                for ind in state.population
            ])
        return state