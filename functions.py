import numpy as np


def distance(point1: np.array, point2: np.array):
    """
    Distance of a point to another one in 3d space
    :param point1: a 3d point
    :param point2: another 3d point
    :return: a float value
    """
    return np.linalg.norm(point2 - point1)


def angle_difference(b1: float, b2: float):
    """
    To compute the difference between the two angles
    :param b1: first angle
    :param b2: second angle
    :return: difference with direction (sign)
    """
    r = (b2 - b1) % 360.0
    # Python modulus has same sign as divisor, which is positive here,
    # so no need to consider negative case
    if r >= 180.0:
        r -= 360.0
    return r
