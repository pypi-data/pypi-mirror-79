#!/usr/bin/env python
"""
Define core netgraph functionality.
"""
import numpy as np
import matplotlib.pyplot as plt


class _BaseGraph:
    """
    Base graph class.
    """

    def __init__(self, node_data, edge_data):
        self.node_data = node_data
        self.edge_data = edge_data

    def _get_node_attr():
        pass

    def _set_node_attr():
        pass

    def _get_edge_attr():
        pass

    def _set_edge_attr():
        pass

    def _add_node():
        pass

    def _add_edge():
        pass

    def _del_node():
        pass

    def _del_edge():
        pass

    def draw():
        pass

    def draw_edges():
        pass

    def draw_nodes():
        pass

    def draw_node_labels():
        pass

    def draw_edge_labels():
        pass


class MultiGraph(_BaseGraph):
    pass


class Graph(_MultiGraph):
    pass
