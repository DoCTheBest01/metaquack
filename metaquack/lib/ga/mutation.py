import numpy as np
from ...pipeline import Operator

class GaussianMutation(Operator):
    def __init__(self, sigma=0.1):
        self.sigma = sigma

    def apply(self, state):
        noise = np.random.normal(0, self.sigma, state.population.shape)
        state.population += noise
        return state

class BitFlipMutation(Operator):
    def __init__(self, probability=0.01):
        self.probability = probability

    def apply(self, state):
        for i in range(len(state.population)):
            for j in range(len(state.population[i])):
                if np.random.rand() < self.probability:
                    state.population[i][j] = 1 - state.population[i][j]  # Flip the bit
        return state

class SwapMutation(Operator):
    def __init__(self, probability=0.1):
        self.probability = probability

    def apply(self, state):
        for i in range(len(state.population)):
            for j in range(len(state.population[i]) - 1):
                if np.random.rand() < self.probability:
                    state.population[i][j], state.population[i][j+1] = state.population[i][j+1], state.population[i][j]
        return state

class InversionMutation(Operator):
    def __init__(self, probability=0.05):
        self.probability = probability

    def apply(self, state):
        for i in range(len(state.population)):
            if np.random.rand() < self.probability:
                start = np.random.randint(0, len(state.population[i]) - 1)
                end = np.random.randint(start + 1, len(state.population[i]))
                state.population[i][start:end] = state.population[i][start:end][::-1]  # Reverse the segment
        return state

class ScrambleMutation(Operator):
    def __init__(self, segment_length, probability=0.1):
        self.segment_length = segment_length
        self.probability = probability

    def apply(self, state):
        for i in range(len(state.population)):
            if np.random.rand() < self.probability:
                start = np.random.randint(0, len(state.population[i]) - self.segment_length)
                segment = state.population[i][start:start + self.segment_length]
                np.random.shuffle(segment)
                state.population[i][start:start + self.segment_length] = segment
        return state