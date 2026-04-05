"""
Complex plane operations: domain coloring, complex grids, Möbius transforms.
No matplotlib imports — pure math only.
"""

from __future__ import annotations

import colorsys

import numpy as np


def complex_grid(
    re_range: tuple[float, float],
    im_range: tuple[float, float],
    re_n: int = 300,
    im_n: int = 300,
) -> np.ndarray:
    """
    Return a 2D complex ndarray of shape (im_n, re_n) covering the rectangle.
    Indexing: result[j, i] = re_range[i] + 1j * im_range[j]
    """
    re = np.linspace(re_range[0], re_range[1], re_n)
    im = np.linspace(im_range[0], im_range[1], im_n)
    RE, IM = np.meshgrid(re, im)
    return RE + 1j * IM


def domain_color(z_values: np.ndarray, brightness_cycles: float = 1.0) -> np.ndarray:
    """
    Standard domain coloring: map complex values to RGB image.

    - Hue encodes arg(z)  in [0, 2π] → [0, 1]
    - Lightness oscillates with log|z| to show magnitude rings
    - Saturation is constant at 0.9

    Parameters:
        z_values:          Complex ndarray of any shape (H, W)
        brightness_cycles: Controls how fast lightness oscillates with |z|.
                           Higher = more rings visible.

    Returns:
        (H, W, 3) float32 array in [0, 1]
    """
    phase = np.angle(z_values)                       # -π to π
    mag = np.log1p(np.abs(z_values))                 # [0, ∞), compressed
    hue = (phase + np.pi) / (2 * np.pi)              # [0, 1]
    lightness = 0.5 + 0.4 * np.sin(mag * np.pi * brightness_cycles)
    saturation = np.full_like(hue, 0.9)

    H, W = hue.shape
    rgb = np.zeros((H, W, 3), dtype=np.float32)
    for i in range(H):
        for j in range(W):
            r, g, b = colorsys.hls_to_rgb(
                float(hue[i, j]),
                float(np.clip(lightness[i, j], 0.0, 1.0)),
                float(saturation[i, j]),
            )
            rgb[i, j] = (r, g, b)
    return rgb


def domain_color_fast(z_values: np.ndarray, brightness_cycles: float = 1.0) -> np.ndarray:
    """
    Vectorized domain coloring (faster than domain_color for large grids).
    Uses HSV → RGB conversion via matplotlib.colors instead of per-pixel colorsys.
    """
    from matplotlib.colors import hsv_to_rgb

    phase = np.angle(z_values)
    mag = np.log1p(np.abs(z_values))
    H = (phase + np.pi) / (2 * np.pi)
    V = 0.5 + 0.4 * np.sin(mag * np.pi * brightness_cycles)
    V = np.clip(V, 0.0, 1.0)
    S = np.full_like(H, 0.85)

    # matplotlib hsv_to_rgb expects (..., 3) with H in [0,1], S in [0,1], V in [0,1]
    hsv = np.stack([H, S, V], axis=-1)
    return hsv_to_rgb(hsv).astype(np.float32)


def mobius(z: np.ndarray, a: complex, b: complex, c: complex, d: complex) -> np.ndarray:
    """
    Möbius transformation: w = (az + b) / (cz + d)
    Returns complex ndarray of same shape as z.
    """
    denom = c * z + d
    with np.errstate(divide="ignore", invalid="ignore"):
        result = (a * z + b) / denom
    return result


def inversion(z: np.ndarray) -> np.ndarray:
    """Complex inversion: w = 1/z"""
    with np.errstate(divide="ignore", invalid="ignore"):
        return 1.0 / z
