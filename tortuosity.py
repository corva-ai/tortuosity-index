from typing import List

import numpy as np
import pandas as pd

from functions import find_inflection
from trajectory import Station, calculate_and_set_single_tortuosity


class TortuosityIndex:
    def __init__(self):
        self.stations = None
        self.final_tortuosity_index = None

    def __len__(self):
        return len(self.stations)

    def __getitem__(self, index):
        return self.stations[index]

    def set_stations(self, stations: List[str]):
        """
        Set the stations
        :param stations: list of survey rows in csv comma separated format
        :return: None
        """
        self.stations = []
        for st_data in stations:
            st = Station()
            values = st_data.strip().split(',')
            values = [float(v) for v in values]
            st.set_data(values)

            if (len(self.stations) == 0) or (len(self.stations) > 0 and st.md > self.stations[-1].md):
                self.stations.append(st)

    def process(self):
        """
        To process and calculate for Tortuosity Index
        :return: None
        """
        # indices of the inflection points
        inflection_indices = []
        # not including the first and last elements, this is the middle point for every 3 stations
        for index in range(1, len(self.stations) - 1):
            is_inflection = find_inflection(self.stations[index - 1: index + 2])
            self.stations[index].is_inflection = is_inflection
            if is_inflection:
                inflection_indices.append(index)

        if not inflection_indices:
            print("Strange, no inflection point.")
            return

        # adding the first and last points as inflection points
        inflection_indices = [0] + inflection_indices + [len(self.stations) - 1]
        self.stations[0].is_inflection = True
        self.stations[-1].is_inflection = True

        for index in inflection_indices[1:]:
            calculate_and_set_single_tortuosity(self.stations[index - 1], self.stations[index])

        df = pd.DataFrame.from_records([s.to_dict() for s in self.stations])

        df['total_ti'] = 0
        last_total_ti = 0
        for index, row in df.iterrows():
            if row['is_inflection']:
                # number of inflection points from surface to the current point
                n_inflections = sum(df.iloc[0:index+1]['is_inflection']) - 1
                if n_inflections >= 1:
                    # measured depth from surface to the current station; usually equal to the measured depth
                    # of the current station since the first station md is 0
                    Lc = df.iloc[index].md - df.iloc[0].md

                    # sum of individual tortuosity indices from surface to the current station
                    sum_tis = sum(df.iloc[0:index + 1]['ti'])
                    if sum_tis > 0:
                        # computing the surveying frequency scaling factor
                        f_SF = self.compute_survey_frequency_scaling_factor(max_index=index)

                        # modified tortuosity index equation
                        last_total_ti = f_SF * Lc ** 2 * ((n_inflections - 1) / n_inflections) * (1 / Lc) * sum_tis

            df.loc[index, 'cumulative_ti'] = last_total_ti

        self.final_tortuosity_index = last_total_ti

        return df

    def compute_survey_frequency_scaling_factor(self, min_index: int = 0, max_index: int = None) -> float:
        """
        to compute f_SF (survey frequency scaling factor)
        start from the first station till the maximum given survey index
        :param min_index: the lower boundary index (inclusive)
        :param max_index: the upper boundary index (inclusive)
        :return:
        """
        if max_index is None or not 1 < max_index < len(self):
            max_index = len(self) - 1

        if min_index is None or not 0 < min_index < len(self) - 1:
            min_index = 0

        distance = self.compute_average_distance(min_index, max_index)
        scaling_factor = compute_scaling_factor(distance)
        return scaling_factor

    def compute_average_distance(self, min_index: int, max_index: int) -> float:
        mds = np.array(list(map(lambda x: x.md, self.stations[min_index: max_index + 1])))
        diffs = np.ediff1d(mds)
        # average distance between stations
        distance = np.nanmean(diffs)

        return float(distance)


def compute_scaling_factor(distance: float) -> float:
    """
    The scaling factor concept idea is from the following paper:
    "Baumgartner, T., Lin, C., Liu, Y., Mendonsa, A., & Zimpfer, D. (2019, March).
    Using Big Data to Study the Impact of Wellbore Tortuosity on Drilling, Completions,
    and Production Performance. In SPE/IADC International Drilling Conference and Exhibition.
    Society of Petroleum Engineers."

    :param distance: , [ft]
    :return:
    """
    if distance < 30:
        return 0.3 / (0.3 + 0.025 * (30 - distance))

    if distance > 30:
        return 0.3 / (0.3 - (0.05 / 30) * (distance - 30))

    return 1
