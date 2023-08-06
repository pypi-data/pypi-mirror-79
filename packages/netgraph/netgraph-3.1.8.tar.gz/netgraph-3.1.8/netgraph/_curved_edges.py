#!/usr/bin/env python
import numpy as np
import matplotlib.patches
import matplotlib.pyplot as plt

import scipy.interpolate as si

from _utils import (
    _get_unique_nodes,
)
from _layout import (
    get_fruchterman_reingold_layout,
    _clip_to_frame,
)


# Adapted from https://stackoverflow.com/a/35007804/2912349
def bspline(cv, n=100, degree=3, periodic=False):
    """ Calculate n samples on a bspline

        cv :      Array ov control vertices
        n  :      Number of samples to return
        degree:   Curve degree
        periodic: True - Curve is closed
    """
    cv = np.asarray(cv)
    count = cv.shape[0]

    # Closed curve
    if periodic:
        kv = np.arange(-degree,count+degree+1)
        factor, fraction = divmod(count+degree+1, count)
        cv = np.roll(np.concatenate((cv,) * factor + (cv[:fraction],)),-1,axis=0)
        degree = np.clip(degree,1,degree)

    # Opened curve
    else:
        degree = np.clip(degree,1,count-1)
        kv = np.clip(np.arange(count+degree+1)-degree,0,count-degree)

    # Return samples
    max_param = count - (degree * (1-periodic))
    spl = si.BSpline(kv, cv, degree)
    return spl(np.linspace(0,max_param,n))


def _get_parallel_path(path, delta):
    # initialise output
    orthogonal_unit_vector = np.zeros_like(path)

    tangents = path[2:] - path[:-2] # using the central difference approximation
    orthogonal_unit_vector[1:-1] = _get_orthogonal_unit_vector(tangents)

    # handle start and end points
    orthogonal_unit_vector[ 0] = _get_orthogonal_unit_vector(np.atleast_2d([path[ 1] - path[ 0]]))
    orthogonal_unit_vector[-1] = _get_orthogonal_unit_vector(np.atleast_2d([path[-1] - path[-2]]))

    return path + delta * orthogonal_unit_vector


def _get_orthogonal_unit_vector(v):
    # adapted from https://stackoverflow.com/a/16890776/2912349
    v = v / np.linalg.norm(v, axis=-1)[:, None] # unit vector
    w = np.c_[-v[:,1], v[:,0]]                  # orthogonal vector
    w = w / np.linalg.norm(w, axis=-1)[:, None] # orthogonal unit vector
    return w


def _shorten_path_by(path, distance):
    """
    Cut path off at the end by `distance`.
    """
    distance_to_end = np.linalg.norm(path - path[-1], axis=1)
    idx = np.where(distance_to_end - distance >= 0)[0][-1] # i.e. the last valid point

    # We could truncate the  path using `path[:idx+1]` and return here.
    # However, if the path is not densely sampled, the error will be large.
    # Therefor, we compute a point that is on the line from the last valid point to
    # the end point, and append it to the truncated path.
    vector = path[idx] - path[-1]
    unit_vector = vector / np.linalg.norm(vector)
    new_end_point = path[-1] + distance * unit_vector

    return np.concatenate([path[:idx+1], new_end_point[None, :]], axis=0)


class CurvedArrow(matplotlib.patches.Polygon):

    def __init__(self, path,
                 width       = 0.05,
                 head_width  = 0.10,
                 head_length = 0.15,
                 offset      = 0.,
                 shape       = 'full',
                 *args, **kwargs):

        # book keeping
        self.path        = path
        self.width       = width
        self.head_width  = head_width
        self.head_length = head_length
        self.shape       = shape
        self.offset      = offset

        vertices = self._get_vertices()
        matplotlib.patches.Polygon.__init__(self, list(map(tuple, vertices)),
                                            closed=True, *args, **kwargs)


    def _get_vertices(self):
        # Determine the actual endpoint (and hence path) of the arrow given the offset;
        # assume an ordered path from source to target, i.e. from arrow base to arrow head.
        arrow_path      = _shorten_path_by(self.path, self.offset)
        arrow_tail_path = _shorten_path_by(arrow_path, self.head_length)

        head_vertex_tip  = arrow_path[-1]
        head_vertex_base = arrow_tail_path[-1]
        (dx, dy), = _get_orthogonal_unit_vector(np.atleast_2d(head_vertex_tip - head_vertex_base)) * self.head_width / 2.

        if self.shape is 'full':
            tail_vertices_right = _get_parallel_path(arrow_tail_path, -self.width / 2.)
            tail_vertices_left  = _get_parallel_path(arrow_tail_path,  self.width / 2.)
            head_vertex_right = head_vertex_base - np.array([dx, dy])
            head_vertex_left  = head_vertex_base + np.array([dx, dy])

            vertices = np.concatenate([
                tail_vertices_right[::-1],
                tail_vertices_left,
                head_vertex_left[None,:],
                head_vertex_tip[None,:],
                head_vertex_right[None,:],
            ])

        elif self.shape is 'right':
            tail_vertices_right = _get_parallel_path(arrow_tail_path, -self.width / 2.)
            head_vertex_right  = head_vertex_base - np.array([dx, dy])

            vertices = np.concatenate([
                tail_vertices_right[::-1],
                arrow_tail_path,
                head_vertex_tip[None,:],
                head_vertex_right[None,:],
            ])

        elif self.shape is 'left':
            tail_vertices_left = _get_parallel_path(arrow_tail_path,  self.width / 2.)
            head_vertex_left = head_vertex_base + np.array([dx, dy])

            vertices = np.concatenate([
                arrow_tail_path[::-1],
                tail_vertices_left,
                head_vertex_left[None,:],
                head_vertex_tip[None,:],
            ])

        else:
            raise ValueError("Argument 'shape' needs to one of: 'left', 'right', 'full', not '{}'.".format(self.shape))

        return vertices


def test_simple_line():
    x = np.linspace(-1, 1, 1000)
    y = np.sqrt(1. - x**2)
    plot_arrow(x, y)


def test_complicated_line():
    random_points = np.random.rand(5, 2)
    x, y = bspline(random_points, n=1000).T
    plot_arrow(x, y)


def plot_arrow(x, y):
    path = np.c_[x, y]
    arrow = CurvedArrow(path,
                        width       = 0.05,
                        head_width  = 0.1,
                        head_length = 0.15,
                        offset      = 0.1,
                        facecolor   = 'red',
                        edgecolor   = 'black',
                        alpha       = 0.5,
                        shape       = 'full',
    )
    fig, ax = plt.subplots(1,1)
    ax.add_artist(arrow)
    ax.plot(x, y, color='black', alpha=0.1) # plot path for reference
    ax.set_aspect("equal")
    plt.show()


def _get_edge_paths(edge_list, node_positions,
                    total_control_points_per_edge = 11,
                    bspline_degree                = 5,
                    origin                        = np.array([0, 0]),
                    scale                         = np.array([1, 1]),
                    k                             = None,
                    initial_temperature           = 0.1,
                    total_iterations              = 50,
                    node_size                     = None,
                    fixed_nodes                   = None,
                    *args, **kwargs):

    # Create a new graph, in which each edge is split into multiple segments;
    # there are total_control_points + 1 segments / edges for each original edge.
    new_edge_list, edge_to_control_points = _insert_control_points(edge_list,
                                                                   total_control_points_per_edge)

    # Initialize the positions of the control points to positions on the original edge.
    control_point_positions = _initialize_control_point_positions(edge_to_control_points, node_positions,
                                                                  origin = origin,
                                                                  scale  = scale,
    )
    node_positions.update(control_point_positions)

    # If the spacing of nodes is approximately k,
    # the spacing of control points should be k / (total control points per edge + 1)
    unique_nodes = _get_unique_nodes(edge_list)
    total_nodes = len(unique_nodes)
    if k is None:
        area = np.product(scale)
        k = np.sqrt(area / float(total_nodes)) / (total_control_points_per_edge + 1)

    node_positions = get_fruchterman_reingold_layout(new_edge_list,
                                                     node_positions      = node_positions,
                                                     scale               = scale,
                                                     origin              = origin,
                                                     k                   = k,
                                                     initial_temperature = initial_temperature,
                                                     total_iterations    = total_iterations,
                                                     node_size           = node_size,
                                                     fixed_nodes         = fixed_nodes,
    )

    # Fit a BSpline to each set of control points (+ anchors).
    edge_to_path = dict()
    for (source, target), control_points in edge_to_control_points.items():
        control_point_positions = [node_positions[node] for node in control_points]
        control_point_positions = [node_positions[source]] + control_point_positions + [node_positions[target]]
        path = bspline(np.array(control_point_positions), degree=bspline_degree)
        edge_to_path[(source, target)] = path

    return edge_to_path


def _insert_control_points(edge_list, n=3):
    new_edge_list = []
    edge_to_control_points = dict()

    ctr = np.max(edge_list) + 1 # TODO: this assumes that nodes are integers; should probably use large random node IDs instead
    for source, target in edge_list:
        control_points = list(range(ctr, ctr+n))
        sources = [source] + control_points
        targets = control_points + [target]
        new_edge_list.extend(zip(sources, targets))
        edge_to_control_points[(source, target)] = control_points
        ctr += n

    return new_edge_list, edge_to_control_points


def _initialize_control_point_positions(edge_to_control_points, node_positions,
                                        origin      = np.array([0, 0]),
                                        scale       = np.array([1, 1]),
                                        loop_radius = 0.1,
):
    control_point_positions = dict()
    for (source, target), control_points in edge_to_control_points.items():
        edge_origin = node_positions[source]
        delta = node_positions[target] - node_positions[source]
        distance = np.linalg.norm(delta)

        if distance > 1e-12:
            unit_vector = delta / distance
            for ii, control_point in enumerate(control_points):
                # y = mx + b
                m = (ii+1) * distance / (len(control_points) + 1)
                control_point_positions[control_point] = m * unit_vector + edge_origin

        else:
            # Source and target have the same position (probably a self-loop),
            # such that using the strategy employed above the control points also end up at the same position.
            # Instead we want to make a loop.

            # To minimise overlap with edges, we want the loop to be
            # on the side of the node away from the centroid of the graph.
            centroid = np.mean(list(node_positions.values()), axis=0)
            delta = edge_origin - centroid
            distance = np.linalg.norm(delta)
            unit_vector = delta / distance
            loop_center = edge_origin + loop_radius * unit_vector

            loop_control_point_angles = np.linspace(0, 2*np.pi, len(control_points)+2)[1:-1]
            start_angle = _get_angle_between(np.array([1., 0.]), edge_origin-loop_center)
            loop_control_point_angles = (loop_control_point_angles + start_angle) % (2*np.pi)

            loop_control_point_positions = np.array([_get_point_on_a_circle(loop_center, loop_radius, angle) for angle in loop_control_point_angles])

            # ensure that the loop stays within the bounding box
            loop_control_point_positions = _clip_to_frame(loop_control_point_positions, origin, scale)

            for ii, control_point in enumerate(control_points):
                control_point_positions[control_point] = loop_control_point_positions[ii]

    return control_point_positions


def _initialize_edge_control_point_positions():
    pass


def _initialize_loop_control_point_positions():
    pass


def _get_angle_between(v1, v2):
    """
    Compute the signed angle between two vectors.

    Adapted from:
    https://stackoverflow.com/a/16544330/2912349
    """
    x1, y1 = v1
    x2, y2 = v2
    dot = x1*x2 + y1*y2
    det = x1*y2 - y1*x2
    angle = np.arctan2(det, dot)
    return angle


def _get_point_on_a_circle(origin, radius, angle):
    x0, y0 = origin
    x = x0 + radius * np.cos(angle)
    y = y0 + radius * np.sin(angle)
    return np.array([x, y])


def test_curved_edges():

    import matplotlib.pyplot as plt; # plt.ion()

    from _main import Graph
    from toy_graphs import unballanced_tree as edge_list

    node_positions = get_fruchterman_reingold_layout(edge_list, node_size=1.)

    # fig, ax = plt.subplots(1,1)
    # Graph(edge_list, node_positions=node_positions)

    # add self-loops
    for node in node_positions:
        edge_list.append((node, node))

    edge_to_path = _get_edge_paths(edge_list, node_positions=node_positions)

    fig, ax = plt.subplots(1,1)
    for edge, path in edge_to_path.items():
        # x, y = path.T
        # ax.plot(x, y)
        arrow = CurvedArrow(path,
                            width       = 0.01,
                            head_width  = 0.02,
                            head_length = 0.03,
                            offset      = 0.001,
                            facecolor   = 'red',
                            # edgecolor   = 'black',
                            edgecolor   = None,
                            alpha       = 0.5,
                            shape       = 'full',
        )
        ax.add_artist(arrow)

    plt.show()


if __name__ == '__main__':
    # plt.ion()
    # test_simple_line()
    # test_complicated_line()
    test_curved_edges()
