import unittest
import json
from typing import List

import numpy as np

from tortuosity import TortuosityIndex
from functions import angle_difference, distance


class Test(unittest.TestCase):
    def test1(self):
        file_path = r"../resources/SampleSurvey.csv"
        print("State path: ", file_path)
        with open(file_path) as file:
            lines = file.readlines()
            lines = lines[1:]  # removing the header row

            tortuosity = TortuosityIndex()
            tortuosity.set_stations(lines)
            df = tortuosity.process()

            if df is not None:
                file_name = f"../resources/TortuasityIndexResults.csv"
                df.to_csv(file_name, columns=['md', 'inc', 'azi', 'x', 'y', 'z', 'is_inflection', 'ti', 'cumulative_ti'])

                with open(file_name, "a") as the_file:
                    the_file.write(f"\nFinal Tortuosity Index: {round(tortuosity.final_tortuosity_index, 2)}")

    def test_functions(self):
        # distance
        point0 = np.array([0, 0, 0])
        point1 = np.array([1, 1, 1])
        np.testing.assert_allclose(np.sqrt(3), distance(point0, point1), atol=0.00001)

        # angle difference
        self.assertEqual(-20, angle_difference(10, 350))
        self.assertEqual(20.0, angle_difference(350, 10))
