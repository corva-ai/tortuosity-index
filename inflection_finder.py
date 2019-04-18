from functions import angle_difference


class InflectionPointFinder:
    """
    This class is used to determine if there is an inflection point
    in the given stations.
    """
    def __init__(self, stations: list):
        if len(stations) != 3:
            raise Exception(f"Only 3 stations are accepted, {len(stations)} are given")

        self.st1 = stations[0]
        self.st2 = stations[1]
        self.st3 = stations[2]

        # if there is a straight line then hold the last stable sign
        self.previous_stable_sign = None

    def process(self):
        """
        Process the stations and check if the middle station is an inflection point
        :return: a boolean
        """
        if angle_difference(self.st1.inc, self.st2.inc) * angle_difference(self.st2.inc, self.st3.inc) < 0 \
                or angle_difference(self.st1.azi, self.st2.azi) * angle_difference(self.st2.azi, self.st3.azi) < 0:
            return True
        elif self.st2.equal_inc_azi(self.st3):
            return True

        return False
