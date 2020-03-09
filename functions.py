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


def find_inflection(stations: list):
    """
    Process the stations and check if the middle station is an inflection point
    :type stations: 3 survey stations
    :return: a boolean
    """
    if len(stations) != 3:
        raise Exception(f"Only 3 self.stations are accepted, {len(stations)} are given")

    st1, st2, st3 = stations
    inc_diff_12 = angle_difference(st1.inc, st2.inc)
    inc_diff_23 = angle_difference(st2.inc, st3.inc)
    azi_diff_12 = angle_difference(st1.azi, st2.azi)
    azi_diff_23 = angle_difference(st2.azi, st3.azi)

    if inc_diff_12 * inc_diff_23 < 0 or azi_diff_12 * azi_diff_23 < 0:
        return True

    if st2.equal_inc_azi(st3):
        return True

    return False
