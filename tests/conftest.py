"""pytest configuration and shared fixtures."""

import pytest
import numpy as np


@pytest.fixture
def x_array():
    return np.linspace(-5.0, 5.0, 100)


@pytest.fixture
def complex_grid_small():
    re = np.linspace(-2.0, 2.0, 30)
    im = np.linspace(-2.0, 2.0, 30)
    RE, IM = np.meshgrid(re, im)
    return RE + 1j * IM
