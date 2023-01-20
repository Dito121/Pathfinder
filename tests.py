import unittest
from pathfinder import TopoMap


class test_cases(unittest.TestCase):
    def test1(self):
        elevation_test = TopoMap("elevation_test.txt")
        elevation_test.txt_to_png()
        elevation_test.find_greedy_path(6)
        self.assertEqual(
            list(elevation_test.list_of_paths[0]),
            [
                (0, 6),
                (1, 5),
                (2, 4),
                (3, 3),
                (4, 2),
                (5, 3),
                (6, 2),
                (7, 2),
                (8, 3),
                (9, 4),
                (10, 5),
                (11, 5),
                (12, 5),
                (13, 6),
            ],
        )


if __name__ == "__main__":
    unittest.main()
