import random
import matplotlib.pyplot as plt


class Grid:
    def __init__(self):
        self.points = {}

    def interpolate_all(self):
        pass

    def __configure_plot_labels(self):
        pass

    def plot(self):
        self.x_values = [int(x) for x in self.points.keys()]
        self.x_values.sort()
        # Correctly map it later tomorrow
        self.y_values = [int(self.points[x]) for x in self.x_values]
        plt.plot(self.x_values, self.y_values)
        plt.xlabel("X values")
        plt.ylabel("Intensity")
        plt.show()


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


def generate_perlin_noise(grid, size):
    seed_array = generate_seed_array(100, size - size % 2)
    return # Need to fill out this functionn


def main():
    pass


if __name__ == '__main__':
    print("Compiled")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
