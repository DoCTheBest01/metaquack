import numpy as np
from ...pipeline import Operator

class OnePointCrossover(Operator):
    def __init__(self, probability=0.7):
        self.probability = probability

    def apply(self, state):
        for i in range(0, len(state.population), 2):
            if np.random.rand() < self.probability:
                parent1 = state.population[i]
                parent2 = state.population[i+1]
                crossover_point = np.random.randint(1, len(parent1) - 1)  # Ensure crossover point is not at the beginning or end

                child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
                child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))

                state.population[i] = child1
                state.population[i+1] = child2
        return state

class TwoPointCrossover(Operator):
    def __init__(self, probability=0.7):
        self.probability = probability

    def apply(self, state):
        for i in range(0, len(state.population), 2):
            if np.random.rand() < self.probability:
                parent1 = state.population[i]
                parent2 = state.population[i+1]
                crossover_point1 = np.random.randint(1, len(parent1) - 1)
                crossover_point2 = np.random.randint(crossover_point1 + 1, len(parent1))

                child1 = np.concatenate((parent1[:crossover_point1], parent2[crossover_point1:crossover_point2], parent1[crossover_point2:]))
                child2 = np.concatenate((parent2[:crossover_point1], parent1[crossover_point1:crossover_point2], parent2[crossover_point2:]))

                state.population[i] = child1
                state.population[i+1] = child2
        return state

class UniformCrossover(Operator):
    def __init__(self, probability=0.5):
        self.probability = probability

    def apply(self, state):
        for i in range(0, len(state.population), 2):
            if np.random.rand() < self.probability:
                parent1 = state.population[i]
                parent2 = state.population[i+1]
                child1 = np.copy(parent1)  # Create copies to avoid modifying parents directly
                child2 = np.copy(parent2)

                for j in range(len(parent1)):
                    if np.random.rand() < self.probability:
                        child1[j] = parent2[j]
                        child2[j] = parent1[j]

                state.population[i] = child1
                state.population[i+1] = child2
        return state

class ArithmeticCrossover(Operator):
    def __init__(self, alpha=0.5):
        self.alpha = alpha

    def apply(self, state):
        for i in range(0, len(state.population), 2):
            parent1 = state.population[i]
            parent2 = state.population[i+1]
            child1 = (self.alpha * parent1) + ((1 - self.alpha) * parent2)
            child2 = (self.alpha * parent2) + ((1 - self.alpha) * parent1)

            state.population[i] = child1
            state.population[i+1] = child2
        return state

class NPointCrossover(Operator):
    def __init__(self, num_points, probability=0.7):
        self.num_points = num_points
        self.probability = probability

    def apply(self, state):
        for i in range(0, len(state.population), 2):
            if np.random.rand() < self.probability:
                parent1 = state.population[i]
                parent2 = state.population[i+1]

                crossover_points = np.sort(np.random.choice(range(1, len(parent1) - 1), size=self.num_points, replace=False))

                child1 = list(parent1)
                child2 = list(parent2)

                start = 0
                for point in crossover_points:
                    child1[start:point] = parent2[start:point]
                    child2[start:point] = parent1[start:point]
                    start = point

                child1[start:] = parent2[start:]
                child2[start:] = parent1[start:]

                state.population[i] = np.array(child1)
                state.population[i+1] = np.array(child2)
        return state