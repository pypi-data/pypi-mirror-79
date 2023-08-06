#!/usr/bin/env python

"""
Related work:

https://github.com/Phlya/adjustText
"""

import numpy as np
import matplotlib.pyplot as plt


def get_label_positions(anchor_positions, label_objects, ax,
                        total_iterations = 50,
                        initial_temperature = 1.0,
):

    # initialize label positions outside of all other artists
    _initialize_label_positions(label_objects, ax)

    # find better positions using a force-directed layout (Fruchterman-Reingold).
    temperatures = _get_temperatures(initial_temperature, total_iterations)
    for temperature in temperatures:
        _update_label_positions(label_objects, ax)

    pass


def _get_artists(ax):
    artists = ax.get_children()
    # remove the background patch from the list of artists; according to
    # https://github.com/matplotlib/matplotlib/blob/0b797a1a0377036785ef1d5609b08ef9c76d289a/lib/matplotlib/axes/_base.py#L4192
    # this is always the last item
    artists = artists[:-1]

    # TODO: filter out all artists not created by the user
    return artists


def _initialize_label_positions(label_objects, ax, delta_radius, delta_angle):
    # Probe in a spiral or concentric rings around the anchor point.
    # Return the first position not within an artist (but still within the axis).

    total_labels = len(label_objects)
    label_positions = np.zeros((total_labels, 2))
    for ii, label_object in enumerate(label_objects):
        # TODO
        pass

    for label_object, label_position in zip(label_objects, label_positions):
        label_object.set_xy(label_position)

    return label_objects


def _update_label_positions(label_objects, ax, temperature):
    # compute net force acting on each label

    # compute displacement

    # update position while ensuring that labels remain within axis

    pass


def _attraction():
    pass


def _repulsion():
    pass


def _get_shortest_distance(path1, path2):
    return distance


def test():

    from matplotlib.patches import Circle

    fig, ax = plt.subplots(1,1)

    # add a bunch of artists
    n = 10
    xy = np.random.rand(n, 2)
    for ii in range(n):
        c = Circle(xy[ii], np.random.rand(1))
        ax.add_artist(c)


    pass


if __name__ == '__main__':
    pass
