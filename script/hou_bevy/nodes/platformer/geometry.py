from hou import Vector3


def reorder_points(
    p0: Vector3,
    p1: Vector3,
    p2: Vector3,
    p3: Vector3,
    first_axis: str | None,
):
    order = [0, 1, 2, 3]
    if first_axis == "Y":
        if p0[1] > p1[1]:
            if p1[0] > p2[0]:
                order = [3, 0, 1, 2]

        if p0[1] < p1[1]:
            if p1[0] > p2[0]:
                order = [2, 1, 0, 3]
    else:
        if p0[0] > p1[0]:
            if p1[1] < p2[1]:
                order = [2, 3, 0, 1]

        elif p1[0] > p0[0]:
            if p2[1] > p1[1]:
                order = [3, 2, 1, 0]

    points = [p0, p1, p2, p3]

    reorded_points = []
    for i in order:
        reorded_points.append(points[i])

    return (reorded_points, points)
