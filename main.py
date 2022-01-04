import random
import matplotlib.pyplot as plt
from tkinter import Tk, Canvas, Frame, BOTH
import math
import numpy as np
from scipy.interpolate import interp1d
from scipy import interpolate


def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


def transform_values(arr, max_val):
    epsilon = 0.000001
    m = max_val * (1/(max(arr) - min(arr) + epsilon))
    b = min(arr)
    return [m*(i - b) for i in arr]

#
# How to use scipy interpolation:
#	- in order to create the "function" that will perform the interpolation, you would do the following:
#
#	>>> f = interp1d(x, y, kind = degree)
#
#	- the "degree" argument must be an odd number. In order to best fit the polynomial and choose our
#	degree, we can represent the argument using the following equation
#
#	- len(x) - (1 + len(x)%2)
#
#	- Now, the name "f" is a function where we can access the values of "f" using "f(x)" where "x" is a number.


class Draw1D(Frame):

    def __init__(self, perlin_array):
        super().__init__()
        self.perlin_array = perlin_array
        self.initUI()

    def draw_array(self, canvas):
        # The create rectangle arguments take in x1, y1, x2, y2.
        # y1 and y2 stay constant (10 and 150).
        # x1 = s * i which is a member of range(0, len(self.perlin_array)) + padding
        # x2 = x1 + s
        array_length = len(self.perlin_array)
        y1, y2, i = 10, 200, 0
        padding = 20

        x = [i for i in range(array_length)]
        xn = np.linspace(0, array_length - 1, array_length*2)
        # print("X is: ", x, " AND Y IS: ", self.perlin_array)
        smoothened_noise = interp1d(x, self.perlin_array, kind=3, fill_value='extrapolate')
        yn = smoothened_noise(xn)

        self.perlin_array = transform_values(yn, 1)
        print("LINE 58: transformed perlin array:", self.perlin_array)

        segment = (400 / len(self.perlin_array)) if (len(self.perlin_array)) else 0
        plt.plot(xn, yn)
        plt.show()
        # 255, 255, 255 is white
        if True:
            print(self.perlin_array)
            for z in self.perlin_array:
                x1 = segment * i + padding
                x2 = x1 + segment
                color = (int(z * 255), int(z * 255), int(z * 255))
                print(color)
                canvas.create_rectangle(x1, y1, x2, y2, outline="",
                                        fill=from_rgb((int(z * 255), int(z * 255), int(z * 255))))
                print(from_rgb((int(z * 255), int(z * 255), int(z * 255))))
                i += 1

    def smooth_draw(self):
        '''
        Useless Function. Can Delete.
        '''
        x = np.linspace(0, 100)


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
        self.smooth_f = None

    def linear_interpolation(self, t):
        """
        Formulas for Linear and Cosine Interpolation: both formulas assume
        that x1 > x0 for the points {(x0, y0), (x1, y1)}

            - Linear(y0, y1, t) = y0 + t * (m(y1, y0)) where m signifies the slope between two points
            - Cosine(y0, y1, t) = Linear(y0, y1, -1 * cos(pi * t)/2 + 0.5)
        """
        assert (max(self.points.keys()) > t >= min(self.points.keys())), \
            "The value of t must be within the current range of the points in grid."

        if t in self.points:
            return self.points.get(t)

        # Can refactor the calculations for x1 and x0 using the built in key parameter in min/max
        x1 = t + min([(x - t) for x in self.points.keys() if x > t])
        x0 = t - min([abs(x - t) for x in self.points.keys() if x < t])
        y0, y1 = self.points[int(x0)], self.points[int(x1)]
        # print("The closest pair of points to t are: ", "(", x0, y0, ")", "and", "(", x1, y1, ")")
        return y0 + (t - x0) * ((y1 - y0) / (x1 - x0))

    def cosine_interpolation(self, t):
        return self.linear_interpolation(-1 * (math.cos(math.pi * t) / 2) + 0.5)

    def configure_perlin_array(self):
        self.x_values = [int(x) for x in self.points.keys()]
        # print("LINE 122", self.x_values)
        self.x_values.sort()
        self.y_values = [float(self.points[x]) for x in self.x_values]
        self.smooth_f = interp1d(self.x_values, self.y_values, kind='cubic', fill_value="extrapolate")
        x_n = np.linspace(0, len(self.x_values))
        y_n = self.smooth_f(x_n)
        # print("LINE 127", y_n)

    def plot(self):
        # Correctly map it later tomorrow
        self.configure_perlin_array()
        plt.plot(self.x_values, self.y_values, 'o--')
        plt.xlabel("X values")
        plt.ylabel("Intensity")
        plt.show()

    def plot_smooth(self, step):
        i, x = 0, []
        while i < max(self.points.keys()):
            x.append(i)
            i += step
        y = [self.cosine_interpolation(x) for x in x]
        # Currently having redundancy in the plotting configuration. Can move this to a seperate helper function.
        plt.plot(x, y)
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
    grid1.plot()
    ex = Draw1D(grid1.generate_array())
    root.geometry("500x500")
    root.mainloop()


if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
