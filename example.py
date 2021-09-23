import random
import matplotlib.pyplot as plt
import sys


def generate_random_points(num_points):
    return [
        (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)) for _ in range(num_points)
    ]


def plot(points, hull_polygon, out_file_name):
    plt.figure()
    plt.gca().set_aspect("equal")

    x, y = zip(*points)

    for i, (x, y) in enumerate(points):
        plt.text(x, y, str(i), horizontalalignment="center", verticalalignment="center")

    n = len(hull_polygon)
    for i in range(n):
        xs = [points[hull_polygon[i]][0], points[hull_polygon[(i + 1) % n]][0]]
        ys = [points[hull_polygon[i]][1], points[hull_polygon[(i + 1) % n]][1]]
        plt.plot(xs, ys, "b-", linewidth=0.4)

    plt.savefig(out_file_name, dpi=300)


def orientation(u, v, w) -> float:
    uw_x = u[0] - w[0]
    uw_y = u[1] - w[1]

    vw_x = v[0] - w[0]
    vw_y = v[1] - w[1]

    return uw_x * vw_y - uw_y * vw_x


def find_leftmost_index(points):
    i_min = 0
    x_min = sys.float_info.max
    for i, (x, _) in enumerate(points):
        if x < x_min:
            x_min = x
            i_min = i
    return i_min


def find_next(points, current_index):
    next_index = (current_index + 1) % len(points)
    for i in range(len(points)):
        if orientation(points[current_index], points[i], points[next_index]) > 0.0:
            next_index = i
    return next_index


def convex_hull(points):

    n = len(points)

    assert n > 2, "we need at least 3 points"

    hull = []

    leftmost_index = find_leftmost_index(points)

    current_index = leftmost_index
    next_index = 0
    indices_set = set(range(n))

    while True:
        hull.append(current_index)

        next_index = find_next(points, current_index)

        if next_index == leftmost_index:
            # stop if next point is the leftmost point
            break

        indices_set.remove(next_index)
        current_index = next_index

    return hull


if __name__ == "__main__":
    num_points = 20
    points = generate_random_points(num_points)
    hull = convex_hull(points)
    plot(points, hull, "jarvis-march.png")
