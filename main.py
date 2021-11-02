import random

class Grid:
    points = {}

    def __init__(self, size):
        self.size = size
        self.points = Grid.points

    def interpolate_all(self, type):
        pass

    def configure(self):
        pass


def generate_seed_array(max_value, size):
    seed_array = []
    for i in range(size):
        seed_array.append(max_value * random.random())
    return seed_array


def generate_interpolation(type, input_list):
    pass


def sample_nth(input_list, n):
    for i in range(0, len(input_list), n):
        pass


def main():
    pass


if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
