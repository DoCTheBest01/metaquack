# MetaQuack

A **Domain-Specific Language (DSL)** framework for building **evolutionary algorithm pipelines**. Currently supports Genetic Algorithm (GA) utilities with extensible operators. Chain operators using the intuitive `>>` syntax to create complex optimization pipelines.

## ✨ Features

- **Fluent Pipeline DSL**: Build algorithms with `>>` operator chaining
- **Progress Visualization**: Real-time colored progress bars with best fitness tracking
- **Modular Operators**: Extensible operator system for custom algorithms
- **NumPy-powered**: Efficient vectorized operations
- **State Management**: Immutable state copying for safe pipeline execution
- **Repeatable Iterations**: Easily repeat full pipeline cycles

## 📦 Installation

```bash
git clone this repo
pip install numpy colorama
cd metaquack && pip install .
```

## 🚀 Quick Start

```python
import numpy as np
from metaquack import initializer as ini
from metaquack.pipeline import Initialize, Evaluate
from metaquack.lib.ga import SelectBest, GaussianMutation

# Define objective function (minimize sphere function)
def sphere(x):
    return np.sum(x**2, axis=1)

# Define search space fields
fields = [
    ini.Bound(-5, 5),  # Continuous [-5, 5]
    ini.Bound(-5, 5),
    ini.Bound(-5, 5),
]

# Build pipeline using DSL
algo = (
    Initialize(fields, count=50)      # Initialize population
    >> Evaluate(sphere)               # Evaluate fitness
    >> SelectBest(25)                 # Keep top 25 individuals
    >> GaussianMutation(0.5)          # Mutate survivors
).repeat(50)  # Repeat full cycle 50 times

# Run pipeline
final_state = algo.run(verbose=True)

print(f"Best solution: {final_state.population[0]}")
print(f"Best fitness: {final_state.fitness.min()}")
```

**Sample Output:**
```
Iteration 1/50:
|——————————————————————————————>| 100.0%
  Best fitness: 2.806442046806472
...
Iteration 50/50:
|——————————————————————————————>| 100.0%
  Best fitness: 0.10880373897580911
```

## 🏗️ Core Components

### 1. **State**
Holds population and fitness values:
```python
State(population=(N, D), fitness=(N,))
```

### 2. **Pipeline**
Chains operators with `>>` and supports repetition:
```python
pipeline = op1 >> op2 >> op3
algo = pipeline.repeat(100)
```

### 3. **Operators**
Base class for all pipeline operations:
```python
class Operator:
    def apply(self, state): ...
```

### 4. **Initializers** (Population Generation)
| Initializer | Use Case | Example |
|-------------|----------|---------|
| `Bound(low, high)` | Continuous values | `Bound(-5.0, 5.0)` |
| `Int(low, high)` | Integer values | `Int(0, 100)` |
| `Binary()` | Binary strings | `Binary()` |

## 🧬 Available GA Operators

### Selection
```python
SelectBest(k=25, goal='min')  # Keep top k individuals
```

### Mutation
```python
GaussianMutation(sigma=0.1)  # Add Gaussian noise
```

### Evaluation
```python
Evaluate(objective_function)  # Vectorized or individual evaluation
```

## 🔧 Extending with Custom Operators

```python
class MyCustomOperator(Operator):
    def apply(self, state):
        # Modify state.population or state.fitness
        state.population *= 1.1  # Example: amplify
        return state

# Use in pipeline
algo = Initialize(fields, 50) >> MyCustomOperator() >> Evaluate(sphere)
```

## 🐛 Known Issues & Fixes

**IndexError in TwoPointCrossover**: Ensure population size supports pairing:
```python
# After SelectBest(25), use even population sizes or adjust selection
SelectBest(24) >> TwoPointCrossover()
```

## 🎯 Roadmap

- [x] GA Operators (Selection, Mutation)
- [ ] Push to PYPI and make it installable throught the package manager
- [ ] Crossover operators (fix population size issues)
- [ ] DE (Differential Evolution) operators
- [ ] PSO (Particle Swarm) operators
- [ ] Logging & statistics
- [ ] Multi-objective optimization
- [ ] Parallel evaluation

## 🤝 Contributing

1. Fork the repo
2. Create new `Operator` subclasses in `lib/`
3. Add to `__init__.py` exports
4. Update this README
5. Submit PR!

## 📄 License
MIT License - see `LICENSE` file for details.
