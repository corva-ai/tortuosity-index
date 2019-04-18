import numpy as np
from functions import distance


class Station:
    """
    This class represent a survey station.
    """
    def __init__(self):
        self.md = None
        self.inc = None
        self.azi = None
        self.x = None
        self.y = None
        self.z = None
        self.vs = None
        self.is_inflection = False
        self.ti = 0  # single TI
        self.total_ti = None  # TI till this station

    def set_data(self, data: dict):
        self.md = data["measured_depth"]
        self.inc = data["inclination"]
        self.azi = data["azimuth"]
        self.x = data["northing"]
        self.y = data["easting"]
        self.z = data["tvd"]
        self.vs = data.get("vertical_section", None)

    def _get_3d_point(self):
        return np.array([self.x, self.y, self.z])

    def equal_inc_azi(self, other):
        if isinstance(other, Station):
            if self.inc == other.inc and self.azi == other.azi:
                return True
        return False

    @property
    def p(self):
        return self._get_3d_point()

    def to_dict(self):
        return {
            'md': self.md,
            'inc': self.inc,
            'azi': self.azi,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'vs': self.vs,
            'is_inflection': self.is_inflection,
            'ti': self.ti,
            'total_ti': self.total_ti
        }


def is_straight(st1: Station, st2: Station):
    """
    To check if it is a straight line from the first station to the next
    :param st1:
    :param st2:
    :return:
    """
    if st1.inc == st2.inc and st1.azi == st2.azi:
        return True

    return False


def calculate_and_set_single_tortuosity(st1: Station, st2: Station):
    """
    Compute and return tortuosity from station 1 to station 2
    Station 2 has a higher MD compared to Station 1
    :param st1:
    :param st2:
    :return: individual/single TI
    """
    if st2.md < st1.md:
        raise ValueError(f"MD of the station 2 ({st2.md}) should be larger than station 1 ({st1.md}).")

    ti = np.abs((st2.md - st1.md) / (distance(st2.p, st1.p))) - 1
    if ti < 0:
        ti = 0

    st2.ti = ti
    return ti
