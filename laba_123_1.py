from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


def visualize_1d(
        abscissa: np.ndarray,
        ordinates: np.ndarray,
        points: Optional[list[tuple[int, int]]] = None,
) -> None:
    _, axis = plt.subplots(figsize=(16, 9))

    axis.plot(abscissa, ordinates, c="royalblue")

    shift = 0.05 * (ordinates.max() - ordinates.min())

    axis.set_xlim(np.min(abscissa), np.max(abscissa))
    axis.set_ylim(np.min(ordinates) - shift, np.max(ordinates) + shift)
    axis.grid(True)

    if points:
        points = list(zip(*points))
        axis.scatter(*points, s=80, c="r", marker="x")

    plt.show()


def visualize_lsm(
        abscissa: np.ndarray,
        ordinates_experiment: np.ndarray,
        ordinates_computed: np.ndarray,
        xlabel: str = "",
        ylabel: str = ""
) -> None:
    _, axis = plt.subplots(figsize=(16, 9))
    axis: plt.Axes = axis

    axis.scatter(
        abscissa,
        ordinates_experiment,
        c="red",
        s=40,
        alpha=0.6,
        label="experiment",
        marker = "X",
        linewidth = 0.25
    )
    axis.plot(
        abscissa,
        ordinates_computed,
        c="royalblue",
        label="lsm",
    )

    axis.set_xlim(np.min(abscissa), np.max(abscissa))
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)

    axis.legend()
    axis.grid()

    plt.show()


def compare_images(image1: np.ndarray, image2: np.ndarray) -> None:
    _, (axis1, axis2) = plt.subplots(1, 2, figsize=(16, 8))
    axis1: plt.Axes = axis1
    axis2: plt.Axes = axis2

    axis1.imshow(image1)
    axis2.imshow(image2)

    axis1.axis("off")
    axis2.axis("off")

    plt.show()


import numpy as np
from numbers import Real


class ShapeMismatchError(BaseException):
    pass


def get_lsm_coefficients(
        abscissa: np.ndarray,
        ordinates: np.ndarray,
) -> tuple[Real, Real]:
    x = abscissa
    y = ordinates

    if x.shape != y.shape:
        raise ShapeMismatchError()

    x_mean = np.mean(x)
    y_mean = np.mean(y)
    x_squared_mean = np.mean(x ** 2)

    xy_mean = np.mean(x * y)

    a = (xy_mean - x_mean * y_mean) / (x_squared_mean - x_mean ** 2)
    b = y_mean - a * x_mean

    return a, b


abscissa_0 = np.array([24.7, 29.8, 33.6, 37.4, 41.0, 44.7, 48.3, 51.9, 55.4, 59.0])
ordinates_0 = 1000 * np.array(
    [0.0392 / 9.941, 0.0398 / 9.934, 0.0404 / 9.932, 0.0409 / 9.931, 0.0414 / 9.931, 0.0420 / 9.928, 0.0425 / 9.927,
     0.0431 / 9.928, 0.0436 / 9.926, 0.0441 / 9.927])
abscissa = np.array([31.30, 31.68, 32.40, 33.80, 46.65, 48.22])
ordinates = np.array([0.02430, 0.02500, 0.02475, 0.02574, 0.02967, 0.03075])
abscissa_1 = np.array([31.30, 31.68, 32.40, 34.11, 33.80, 46.65, 46.60, 49.28, 48.22, 49.76])
ordinates_1 = np.array([0.02651, 0.02654, 0.02659, 0.02673, 0.02670, 0.02771, 0.02770, 0.02791, 0.02783, 0.02795])
incline_0, shift_0 = get_lsm_coefficients(abscissa_0, ordinates_0)
incline, shift = get_lsm_coefficients(abscissa, ordinates)
incline_1, shift_1 = get_lsm_coefficients(abscissa_1, ordinates_1)

visualize_lsm(
    abscissa=abscissa_0,
    ordinates_experiment=ordinates_0,
    ordinates_computed=incline_0 * abscissa_0 + shift_0,
    xlabel="T ℃ - температура",
    ylabel="R.Ом - сопротивление"
)
visualize_lsm(
    abscissa=abscissa,
    ordinates_experiment=ordinates,
    ordinates_computed=incline * abscissa + shift,
    xlabel="T ℃ - температура",
    ylabel="κ - теплопроводность газа (ВТ/м*К)"
)
visualize_lsm(
    abscissa=abscissa_1,
    ordinates_experiment=ordinates_1,
    ordinates_computed=incline_1 * abscissa_1 + shift_1,
    xlabel="T ℃ - температура",
    ylabel="κ - теплопроводность газа (ВТ/м*К)"
)
