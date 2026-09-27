"""Problem 7: implement and plot one-dimensional interpolation without interp1d."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


def _validate_inputs(x, y, X):
    """Convert inputs to float arrays and check the interpolation preconditions."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    X = np.asarray(X, dtype=float)

    if x.ndim != 1 or y.ndim != 1 or X.ndim != 1:
        raise ValueError("x、y、X 都必須是一維陣列")
    if len(x) != len(y):
        raise ValueError("x 與 y 必須有相同的資料點數量")
    if len(x) < 2:
        raise ValueError("至少需要兩個資料點")
    if not (np.isfinite(x).all() and np.isfinite(y).all() and np.isfinite(X).all()):
        raise ValueError("輸入不可包含 NaN 或無限大")
    if np.any(np.diff(x) <= 0):
        raise ValueError("x 必須嚴格遞增，且不可有重複值")
    if X.size and (X.min() < x[0] or X.max() > x[-1]):
        raise ValueError("X 必須位於已知資料 x 的範圍內")

    return x, y, X


def _nearest_interpolation(x, y, X):
    """Choose the y value belonging to the closest known x coordinate."""
    right = np.searchsorted(x, X, side="left")
    right = np.clip(right, 0, len(x) - 1)
    left = np.clip(right - 1, 0, len(x) - 1)

    # If both points are equally close, choose the point on the left.
    choose_right = np.abs(x[right] - X) < np.abs(X - x[left])
    indices = np.where(choose_right, right, left)
    return y[indices]


def _linear_interpolation(x, y, X):
    """Interpolate each requested coordinate along a straight line segment."""
    interval = np.searchsorted(x, X, side="right") - 1
    interval = np.clip(interval, 0, len(x) - 2)

    x_left = x[interval]
    x_right = x[interval + 1]
    y_left = y[interval]
    y_right = y[interval + 1]
    ratio = (X - x_left) / (x_right - x_left)
    return y_left + ratio * (y_right - y_left)


def _natural_cubic_spline(x, y, X):
    """Compute a natural cubic spline using the tridiagonal algorithm."""
    point_count = len(x)
    h = np.diff(x)

    alpha = np.zeros(point_count)
    alpha[1:-1] = (
        3.0 * (y[2:] - y[1:-1]) / h[1:]
        - 3.0 * (y[1:-1] - y[:-2]) / h[:-1]
    )

    lower_solution = np.ones(point_count)
    upper_ratio = np.zeros(point_count)
    right_solution = np.zeros(point_count)

    for i in range(1, point_count - 1):
        lower_solution[i] = (
            2.0 * (x[i + 1] - x[i - 1]) - h[i - 1] * upper_ratio[i - 1]
        )
        upper_ratio[i] = h[i] / lower_solution[i]
        right_solution[i] = (
            alpha[i] - h[i - 1] * right_solution[i - 1]
        ) / lower_solution[i]

    a = y[:-1].copy()
    b = np.zeros(point_count - 1)
    c = np.zeros(point_count)
    d = np.zeros(point_count - 1)

    # Natural boundary conditions: S''(x_0) = S''(x_n) = 0.
    for j in range(point_count - 2, -1, -1):
        c[j] = right_solution[j] - upper_ratio[j] * c[j + 1]
        b[j] = (y[j + 1] - y[j]) / h[j] - h[j] * (c[j + 1] + 2.0 * c[j]) / 3.0
        d[j] = (c[j + 1] - c[j]) / (3.0 * h[j])

    interval = np.searchsorted(x, X, side="right") - 1
    interval = np.clip(interval, 0, point_count - 2)
    dx = X - x[interval]
    return a[interval] + b[interval] * dx + c[interval] * dx**2 + d[interval] * dx**3


def interpolate(x, y, X, option):
    """Return interpolated values using nearest, linear, or cubic spline interpolation."""
    x, y, X = _validate_inputs(x, y, X)
    normalized_option = str(option).lower()

    if normalized_option == "nearest":
        return _nearest_interpolation(x, y, X)
    if normalized_option == "linear":
        return _linear_interpolation(x, y, X)
    if normalized_option in {"spline", "cubic"}:
        return _natural_cubic_spline(x, y, X)

    raise ValueError("option 必須是 'nearest'、'linear'、'spline' 或 'cubic'")


def my_interp_plotter(x, y, X, option, show=True):
    """Calculate the requested interpolation and plot it with the original data."""
    x, y, X = _validate_inputs(x, y, X)
    Y = interpolate(x, y, X, option)
    normalized_option = str(option).lower()
    title_option = "cubic" if normalized_option in {"spline", "cubic"} else normalized_option

    plt.figure(figsize=(8, 5))
    plt.plot(X, Y, color="blue", label="interpolation")
    plt.plot(x, y, "ro", label="data points")
    plt.title(f"{title_option} interpolation of data")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(alpha=0.2)
    plt.tight_layout()

    if show:
        plt.show()

    return Y


def run_test_cases():
    """Run the textbook data through all three interpolation methods."""
    x = np.array([0.0, 0.1, 0.15, 0.35, 0.6, 0.7, 0.95, 1.0])
    y = np.array([1.0, 0.8187, 0.7408, 0.4966, 0.3012, 0.2466, 0.1496, 0.1353])
    X = np.linspace(0.0, 1.0, 101)

    for option in ("nearest", "linear", "cubic"):
        my_interp_plotter(x, y, X, option)


if __name__ == "__main__":
    run_test_cases()
