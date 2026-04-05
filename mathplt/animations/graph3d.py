"""3D surface animation: rotating f(x, y) surface."""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — registers 3d projection

from mathplt.core.animator import AnimationConfig, BaseAnimator
from mathplt.core.equation_parser import EquationParser
from mathplt.core.registry import AnimationRegistry
from mathplt.config import SURFACE_CMAP


@AnimationRegistry.register
class Graph3DAnimator(BaseAnimator):
    """
    Animated 3D surface for f(x, y).

    The surface rotates by incrementing the azimuth angle each frame.
    Example equations:
        sin(sqrt(x**2 + y**2))
        exp(-0.1*(x**2 + y**2)) * cos(x + y)
        sin(x) * cos(y)
        x * exp(-x**2 - y**2)
    """

    NAME = "graph3d"
    DESCRIPTION = "Rotating 3D surface f(x, y)"

    def __init__(
        self,
        config: AnimationConfig,
        equation: str = "sin(sqrt(x**2 + y**2))",
        x_range: tuple[float, float] = (-5.0, 5.0),
        y_range: tuple[float, float] = (-5.0, 5.0),
        resolution: int = 60,
        cmap: str = SURFACE_CMAP,
        azim_start: float = -60.0,
        azim_per_frame: float = 1.0,
        elev: float = 30.0,
    ) -> None:
        super().__init__(config)
        self.equation = equation
        self.x_range = x_range
        self.y_range = y_range
        self.resolution = resolution
        self.cmap = cmap
        self.azim_start = azim_start
        self.azim_per_frame = azim_per_frame
        self.elev = elev

        parser = EquationParser()
        self._f = parser.parse_xy(equation)

        x = np.linspace(x_range[0], x_range[1], resolution)
        y = np.linspace(y_range[0], y_range[1], resolution)
        self.X, self.Y = np.meshgrid(x, y)
        self.Z = self._f(self.X, self.Y)

    def setup(self) -> None:
        self.fig = plt.figure(figsize=self.config.figsize, dpi=self.config.dpi)
        ax = self.fig.add_subplot(111, projection="3d")
        self.axes = [ax]

        ax.set_title(f"f(x,y) = {self.equation}", color="white", pad=10)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("f(x,y)")
        ax.view_init(elev=self.elev, azim=self.azim_start)

        self._surf = ax.plot_surface(
            self.X, self.Y, self.Z,
            cmap=self.cmap, alpha=0.9, linewidth=0,
            antialiased=True,
        )
        self.fig.colorbar(self._surf, ax=ax, shrink=0.5, pad=0.1)

    def update(self, frame: int) -> list:
        azim = self.azim_start + frame * self.azim_per_frame
        self.axes[0].view_init(elev=self.elev, azim=azim)
        # 3D rotation doesn't have blit-compatible artists; return empty list
        # blit=True won't work cleanly for 3D, but we keep the interface consistent
        return []

    def build(self):
        """Override to disable blit for 3D (not supported by mpl_toolkits.mplot3d)."""
        self.setup()
        if self.config.title and self.fig is not None:
            self.fig.suptitle(self.config.title, color="white")
        import matplotlib.animation as animation
        self._anim = animation.FuncAnimation(
            self.fig,
            self.update,
            frames=self.total_frames(),
            interval=1000 // self.config.fps,
            blit=False,  # 3D rotation requires full redraw
        )
        return self._anim
