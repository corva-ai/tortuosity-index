from trajectory import Station, calculate_and_set_single_tortuosity
from inflection_finder import InflectionPointFinder
import pandas as pd


class TortuosityIndex:
    def __init__(self):
        self.stations = None
        self.final_tortuosity_index = None

    def set_stations_by_json(self, stations_json: list):
        """
        Set the stations
        :param stations_json: list of json objects
        :return: None
        """
        self.stations = []
        for st_json in stations_json:
            st = Station()
            st.set_data(st_json)

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
        for idx in range(1, len(self.stations) - 1):
            finder = InflectionPointFinder(self.stations[idx - 1: idx + 2])
            is_inflection = finder.process()
            self.stations[idx].is_inflection = is_inflection
            if is_inflection:
                inflection_indices.append(idx)

        if len(inflection_indices) == 0:
            print("Strange, no inflection point.")
        else:
            inflection_indices = [0] + inflection_indices + [len(self.stations) - 1]
            self.stations[0].is_inflection = True
            self.stations[-1].is_inflection = True
            print("Inflection points indices: ", inflection_indices)

            for idx in inflection_indices[1:]:
                calculate_and_set_single_tortuosity(self.stations[idx - 1], self.stations[idx])

            df = pd.DataFrame.from_records([s.to_dict() for s in self.stations])

            df['total_ti'] = 0
            last_total_ti = 0
            for idx, row in df.iterrows():
                if row['is_inflection']:
                    n = sum(df.iloc[0:idx+1]['is_inflection']) - 1
                    if n >= 1:
                        Lc = df.iloc[idx].md - df.iloc[0].md
                        last_total_ti = Lc ** 2 * ((n - 1) / n) * (1 / Lc) * sum(df.iloc[0:idx+1]['ti'])
                        print(f"Tortuosity Index at {round(self.stations[idx].md, 2)} ft: {round(last_total_ti, 2)}")

                df.loc[idx, 'total_ti'] = last_total_ti

            self.final_tortuosity_index = last_total_ti

            return df
