from collections import OrderedDict
from PIL import Image
from PIL import ImageColor
import random

list_of_paths = []
list_of_sums = []
smallest_change_paths = []


class TopoMap:
    def __init__(self, name_txt):
        self.name_txt = name_txt
        self.name_png = f'{self.name_txt[:-3]}png'
        self.set_data()
        self.txt_to_png()

    def set_data(self):
        self.data = OrderedDict()
        self.min_data = 10000
        self.max_data = 0

        with open(self.name_txt, 'r') as f:
            lines = f.readlines()
            width = 0
            height = 0

            for i in range(len(lines)):
                lines[i] = lines[i].split()
                height += 1

                for j in range(len(lines[i])):
                    if i == 0:
                        width += 1

                    self.data[(i, j)] = int(lines[i][j])
                    self.min_data = min(self.min_data, self.data[(i, j)])
                    self.max_data = max(self.max_data, self.data[(i, j)])

            self.size_data = (width, height)

    def txt_to_png(self):
        self.image = Image.new('RGBA', self.size_data, 'white')

        for key, value in self.data.items():
            grayscale = (value - self.min_data) // ((self.max_data - self.min_data)//256 + 1)
            self.image.putpixel((key[1], key[0]), (grayscale, grayscale, grayscale, 255))
        self.image.save(self.name_png)

    def find_greedy_path(self, starting_row):
        row = starting_row
        col = 0
        self.sum = 0
        self.path = OrderedDict()
        current = self.data[(row, col)]
        self.path[(col, row)] = self.data[(row, col)]

        while col < self.size_data[1]-1:
            right = self.data[(row, col+1)]

            right_up = right if row < 1 else self.data[(row-1, col+1)]

            right_down = right if row+1 >= self.size_data[0] else self.data[(row+1, col+1)]

            diffs = [abs(current - right), abs(current - right_down), abs(current - right_up)]
            min_diff = min(diffs)
            self.sum += min_diff

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

        list_of_paths.append(self.path)
        list_of_sums.append(self.sum)

    def chart_greedy_path(self, paths=list_of_paths, color='red'):

        for i in range(len(paths)):
            for key in paths[i]:
                self.image.putpixel(key, ImageColor.getcolor(color, 'RGBA'))
        self.image.save(self.name_png)


'''
elevation_small = TopoMap('elevation_small.txt')

for i in range(elevation_small.size_data[0]):
    elevation_small.find_greedy_path(i)

smallest_change = min(list_of_sums)
for i in range(len(list_of_sums)):
    if list_of_sums[i] == smallest_change:
        smallest_change_paths.append(list_of_paths[i])

elevation_small.chart_greedy_path()
elevation_small.chart_greedy_path(paths=smallest_change_paths, color='blue')
'''

'''
elevation_large = TopoMap('elevation_large.txt')

for i in range(elevation_large.size_data[0]):
    elevation_large.find_greedy_path(i)

smallest_change = min(list_of_sums)
for i in range(len(list_of_sums)):
    if list_of_sums[i] == smallest_change:
        smallest_change_paths.append(list_of_paths[i])

elevation_large.chart_greedy_path()
elevation_large.chart_greedy_path(paths=smallest_change_paths, color='blue')
'''

'''
elevation_test = TopoMap('elevation_test.txt')
elevation_test.txt_to_png()
elevation_test.find_greedy_path(6)
elevation_test.chart_greedy_path()
'''


'''
if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Read elevations from a text file.')
    parser.add_argument('file', help='file to read')
    args = parser.parse_args()

    file = Path(args.file)
    if file.is_file():
        get_data(file)
    else:
        print(f"{file} does not exist!")
        exit(1)
'''
