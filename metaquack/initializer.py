import numpy as np

class Initializer:
    def generate(self, size):
        raise NotImplementedError

class Bound(Initializer):
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def generate(self, size):
        return np.random.uniform(self.low, self.high, size)

class Int(Initializer):
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def generate(self, size):
        return np.random.randint(self.low, self.high, size)

class Binary(Initializer):
    def generate(self, size):
        return np.random.choice([0, 1], size)

class Choice(Initializer):
    def __init__(self, items):
        self.items = items

    def generate(self, size):
        return np.random.choice(self.items, size)