import numpy as np
from ...pipeline import Operator

class RouletteWheelSelection(Operator):
    def __init__(self, goal='min'):
        self.goal = goal

    def apply(self, state):
        fitness = state.objective
        if self.goal == 'min':
            fitness = -fitness  # Invert for minimization problems

        total_fitness = np.sum(fitness)
        probabilities = fitness / total_fitness

        # Select individuals based on probabilities
        selected_indices = np.random.choice(len(state.population), size=len(state.population), replace=True, p=probabilities)
        state.population = state.population[selected_indices]
        state.objective = state.objective[selected_indices]
        return state

class RankSelection(Operator):
    def __init__(self, goal='min'):
        self.goal = goal

    def apply(self, state):
        ranked_indices = np.argsort(state.objective)
        if self.goal == 'min':
            ranked_indices = ranked_indices[::-1]

        # Assign probabilities based on rank
        rank_probabilities = np.arange(1, len(state.population) + 1) / (len(state.population))
        rank_probabilities = rank_probabilities[ranked_indices]

        # Select individuals based on rank probabilities
        selected_indices = np.random.choice(len(state.population), size=len(state.population), replace=True, p=rank_probabilities)
        state.population = state.population[selected_indices]
        state.objective = state.objective[selected_indices]
        return state

class TournamentSelection(Operator):
    def __init__(self, tournament_size, goal='min'):
        self.tournament_size = tournament_size
        self.goal = goal

    def apply(self, state):
        selected_indices = []
        for _ in range(len(state.population)):
            tournament_indices = np.random.choice(len(state.population), size=self.tournament_size, replace=False)
            tournament_fitness = state.objective[tournament_indices]

            if self.goal == 'min':
                winner_index = tournament_indices[np.argmin(tournament_fitness)]
            else:
                winner_index = tournament_indices[np.argmax(tournament_fitness)]

            selected_indices.append(winner_index)

        state.population = state.population[selected_indices]
        state.objective = state.objective[selected_indices]
        return state

class StochasticUniversalSampling(Operator):
    def __init__(self, goal='min'):
        self.goal = goal

    def apply(self, state):
        fitness = state.objective
        if self.goal == 'min':
            fitness = -fitness

        total_fitness = np.sum(fitness)
        probabilities = fitness / total_fitness

        # Calculate pick points
        pick_points = np.cumsum(probabilities)
        pick_points = np.linspace(0, 1, len(state.population))

        # Select individuals
        selected_indices = []
        for i in range(len(state.population)):
            for j in range(len(state.population)):
                if pick_points[i] <= probabilities[j]:
                    selected_indices.append(j)
                    break

        state.population = state.population[selected_indices]
        state.objective = state.objective[selected_indices]
        return state

class BoltzmannSelection(Operator):
    def __init__(self, temperature, goal='min'):
        self.temperature = temperature
        self.goal = goal

    def apply(self, state):
        fitness = state.objective
        if self.goal == 'min':
            fitness = -fitness

        # Boltzmann probabilities
        probabilities = np.exp(fitness / self.temperature)
        probabilities /= np.sum(probabilities)

        # Select individuals
        selected_indices = np.random.choice(len(state.population), size=len(state.population), replace=True, p=probabilities)
        state.population = state.population[selected_indices]
        state.objective = state.objective[selected_indices]
        return state

class SigmaSelection(Operator):
    def __init__(self, sigma, goal='min'):
        self.sigma = sigma
        self.goal = goal

    def apply(self, state):
        fitness = state.objective
        if self.goal == 'min':
            fitness = -fitness

        # Scale fitness values
        scaled_fitness = fitness + self.sigma

        # Normalize probabilities
        probabilities = scaled_fitness / np.sum(scaled_fitness)

        # Select individuals
        selected_indices = np.random.choice(len(state.population), size=len(state.population), replace=True, p=probabilities)
        state.population = state.population[selected_indices]
        state.objective = state.objective[selected_indices]
        return state

class SelectBest(Operator):
    def __init__(self, k, goal='min'):
        self.k = k
        self.goal = goal

    def apply(self, state):
        idx = np.argsort(state.objective)
        if self.goal == 'max':
            idx = idx[::-1]

        idx = idx[:self.k]

        state.population = state.population[idx]
        state.objective = state.objective[idx]
        return state