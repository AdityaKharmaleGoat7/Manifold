# mathplt

Mathematical animation toolkit for visualizing complex functions, 2D/3D graphs, and Riemann Hypothesis structures — built for Jupyter notebooks with matplotlib.

## Features

- **2D animated graphs** — input any `f(x, t)` equation, watch it evolve over time
- **3D surface animations** — rotating `f(x, y)` surfaces
- **Complex plane** — domain coloring of `f(z)` with hue=arg, brightness=|z|
- **Riemann Hypothesis** — zeta function on the critical strip, zeros on the critical line, argument principle / winding numbers, analytic continuation

## Setup

```bash
pip install -e ".[notebook]"
jupyter lab
```

## Usage in Jupyter

```python
from mathplt.jupyter.widgets import EquationWidget, AnimationWidget
from mathplt.animations.graph2d import Graph2DAnimator
from mathplt.core.animator import AnimationConfig

# Type your equation interactively
eq = EquationWidget(variable='x')
eq.display()
# → enter: sin(x + t) * exp(-0.1 * x**2)

config = AnimationConfig(fps=30, duration_seconds=12.0)
animator = Graph2DAnimator(config, equation=eq.equation)
AnimationWidget(animator).display()
```

## Animations

| Name | Description |
|------|-------------|
| `graph2d` | Animated 2D curve `f(x, t)` |
| `graph3d` | Rotating 3D surface `f(x, y)` |
| `complex` | Domain coloring of `f(z)` |
| `riemann.zeros` | Zeros of ζ(s) on the critical line |
| `riemann.critical_strip` | Magnitude + phase heatmap of ζ(s) |
| `riemann.zeta_surface` | Domain coloring of ζ(s) on the complex plane |
| `riemann.winding` | Argument principle — winding number as contour expands |
| `riemann.continuation` | Analytic continuation of ζ(s) beyond Re(s) > 1 |

## Project Structure

```
mathplt/
├── core/           # BaseAnimator, AnimationRegistry, EquationParser
├── math/           # zeta.py, complex_ops.py, numerics.py (no matplotlib)
├── animations/     # All animator implementations
│   └── riemann/    # Riemann-specific animations
└── jupyter/        # EquationWidget, AnimationWidget
notebooks/          # Ready-to-run Jupyter notebooks
tests/              # pytest suite
```

## Extending

Adding a new animation is one file:

```python
# mathplt/animations/my_animation.py
from mathplt.core.animator import BaseAnimator, AnimationConfig
from mathplt.core.registry import AnimationRegistry

@AnimationRegistry.register
class MyAnimator(BaseAnimator):
    NAME = "my_animation"
    DESCRIPTION = "What it does"

    def setup(self) -> None:
        self.fig, ax = ...

    def update(self, frame: int) -> list:
        # update artists, return list of changed ones
        return [self._line]
```

It will be auto-discovered and available immediately.
