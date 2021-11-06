import random
import matplotlib.pyplot as plt
from tkinter import Tk, Canvas, Frame, BOTH
import math


def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


class Draw1D(Frame):

    def __init__(self, perlin_array):
        super().__init__()
        self.perlin_array = perlin_array
        self.initUI()

    def draw_array(self, canvas):
        i = 1
        # 255, 255, 255 is white
        if self.perlin_array:
            print(self.perlin_array)
            for z in self.perlin_array:
                canvas.create_rectangle(i * 20, 10, 5, 200, outline="red",
                                        fill=from_rgb((int(z * 255), int(z * 255), int(z * 255))))
                print(from_rgb((int(z * 255), int(z * 255), int(z * 255))))
                i += 1

    def initUI(self):
        self.master.title("1D Perlin Noise")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        self.draw_array(canvas)
        canvas.pack(fill=BOTH, expand=1)


class Grid:
    def __init__(self):
        self.points = {}
        self.x_values = 0
        self.y_values = 0

    def linear_interpolation(self, t):
        """
        Formulas for Linear and Cosine Interpolation: both formulas assume
        that x1 > x0 for the points {(x0, y0), (x1, y1)}

            - Linear(y0, y1, t) = y0 + t * (m(y1, y0)) where m signifies the slope between two points
            - Cosine(y0, y1, t) = Linear(y0, y1, -1 * cos(pi * t)/2 + 0.5)
        """
        if t in self.points:
            return self.points.get(t)
        x_1 = t + min([(x - t) for x in self.points.keys() if x > t])
        x_0 = t - min([abs(x - t) for x in self.points.keys() if x < t])
        print("The closest pair of points to t are: ", "(", x_1, x_0, ")")
        return
        # x_plus = min([(x - t) for x in self.points.keys() if x > t])
        # x_minus = min([abs(x - t) for x in self.points.keys() if x < t])
        # print(x_plus, x_minus)

    def configure_perlin_array(self):
        self.x_values = [int(x) for x in self.points.keys()]
        self.x_values.sort()
        self.y_values = [float(self.points[x]) for x in self.x_values]

    def plot(self):
        # Correctly map it later tomorrow
        self.configure_perlin_array()
        plt.plot(self.x_values, self.y_values)
        plt.xlabel("X values")
        plt.ylabel("Intensity")
        plt.show()

    def generate_array(self):
        self.configure_perlin_array()
        return self.y_values


def generate_seed_array(max_value, size):
    seed_array = []
    for i in range(size):
        seed_array.append(max_value * random.random())
    return seed_array


def generate_interpolation(type, input_list):
    pass


def sample_nth(grid, seed_list, step_size, scale):
    """
    :param grid: this will be the grid instance that the function will add points to
    :param seed_list: this is the randomly generated array that the function will pull from
    :param scale: this will be a number from 0 to 1.0 that we will multiply by the number
    that we pull from
    :return: None

    """
    curr_index = 0
    while curr_index < len(seed_list) - 1:
        grid.points[curr_index] = grid.points.get(curr_index, 0) + scale * seed_list[curr_index]
        curr_index += step_size
    grid.points[len(seed_list) - 1] = grid.points[0]


def draw1d():
    pass


def recurse_sample(grid, seed_list, step_size, scale):
    if step_size == 0:
        return
    sample_nth(grid, seed_list, step_size, scale)
    recurse_sample(grid, seed_list, step_size // 2, scale / 2)


def generate_perlin_noise(grid, size):
    seed_array = generate_seed_array(1, size - (size % 2))
    recurse_sample(grid, seed_array, len(seed_array), 1)


def main():
    root = Tk()
    grid1 = Grid()
    generate_perlin_noise(grid1, 64)
    ex = Draw1D(grid1.generate_array())
    root.geometry("500x500")
    root.mainloop()


if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
