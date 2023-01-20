from collections import OrderedDict
from PIL import Image
from PIL import ImageColor
import random


class TopoMap:
    def __init__(self, name_txt: str):
        self.name_txt = name_txt
        self.name_png = f"{self.name_txt[:-3]}png"
        self.list_of_sums = []
        self.list_of_paths = []
        self.smallest_change_paths = []
        self.set_data()
        self.txt_to_png()

    def set_data(self):
        self.data = OrderedDict()
        self.min_data = 10000
        self.max_data = 0

        with open(self.name_txt, "r") as file:
            file = file.readlines()
            height, width = 0, 0

            for i in range(len(file)):
                file[i] = file[i].split()
                height += 1

                for j in range(len(file[i])):
                    if i == 0:
                        width += 1

                    self.data[(i, j)] = int(file[i][j])
                    self.min_data = min(self.min_data, self.data[(i, j)])
                    self.max_data = max(self.max_data, self.data[(i, j)])

            self.size_data = (width, height)

    def txt_to_png(self):
        self.image = Image.new("RGBA", self.size_data, "white")

        for key, value in self.data.items():
            grayscale = (value - self.min_data) // (
                (self.max_data - self.min_data) // 256 + 1
            )
            self.image.putpixel(
                (key[1], key[0]), (grayscale, grayscale, grayscale, 255)
            )
        self.image.save(self.name_png)

    def find_greedy_path(self, starting_row: int):
        row = starting_row
        col = 0
        summ = 0
        self.path = OrderedDict()
        current = self.data[(row, col)]
        self.path[(col, row)] = self.data[(row, col)]

        while col < self.size_data[1] - 1:
            right = self.data[(row, col + 1)]
            right_up = right if row < 1 else self.data[(row - 1, col + 1)]
            right_down = (
                right if row + 1 >= self.size_data[0] else self.data[(row + 1, col + 1)]
            )

            diffs = [
                abs(current - right),
                abs(current - right_down),
                abs(current - right_up),
            ]
            min_diff = min(diffs)
            summ += min_diff

            if min_diff == diffs[0]:
                current = right
            elif diffs[1] == diffs[2] == min_diff:
                current = diffs[random.randint(1, 2)]
                if current == right_down:
                    row += 1
                else:
                    row -= 1
            elif min_diff == diffs[1]:
                current = right_down
                row += 1
            elif min_diff == diffs[2]:
                current = right_up
                row -= 1

            col += 1
            self.path[(col, row)] = self.data[(row, col)]

        self.list_of_paths.append(self.path)
        self.list_of_sums.append(summ)

    def get_smallest_change_paths(self):
        self.min_sum = min(self.list_of_sums)
        for i in range(len(self.list_of_sums)):
            if self.list_of_sums[i] == self.min_sum:
                self.smallest_change_paths.append(self.list_of_paths[i])
        return self.smallest_change_paths

    def chart_greedy_path(self, paths: list = None, color: str = "red"):
        if paths is None:
            paths = self.list_of_paths
        for i in range(len(paths)):
            for key in paths[i]:
                self.image.putpixel(key, ImageColor.getcolor(color, "RGBA"))
        self.image.save(self.name_png)


if __name__ == "__main__":
    elevation_small = TopoMap("elevation_small.txt")
    for i in range(elevation_small.size_data[0]):
        elevation_small.find_greedy_path(i)
    elevation_small.chart_greedy_path()
    elevation_small.chart_greedy_path(
        paths=elevation_small.get_smallest_change_paths(), color="blue"
    )

    elevation_large = TopoMap("elevation_large.txt")
    for i in range(elevation_large.size_data[0]):
        elevation_large.find_greedy_path(i)
    elevation_large.chart_greedy_path()
    elevation_large.chart_greedy_path(
        paths=elevation_large.get_smallest_change_paths(), color="blue"
    )
