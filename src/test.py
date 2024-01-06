import numpy as np


def generate_circle_coordinates(radius, num_points=30):
    theta = np.linspace(0, 2*np.pi, num_points)
    x = 30 + radius * np.cos(theta)
    y = 30 + radius * np.sin(theta)
    return x, y


def circular_list_generator(my_list):
    index = 0
    while True:
        yield my_list[index]
        index = (index + 1) % len(my_list)


circular_gen = circular_list_generator(
    list(generate_circle_coordinates(30)[0]))
for _ in range(100):
    next_number = next(circular_gen)
    print(next_number)
