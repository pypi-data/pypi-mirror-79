#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cython: language_level=3

"""

"""

#import networkx as nx
#import mechanical_components.wires as wires
#import matplotlib.pyplot as plt

try:
    _open_source = True
    import mechanical_components.optimization.wires_protected as protected_module

except (ModuleNotFoundError, ImportError) as e:
    _open_source = False

from  mechanical_components.optimization.common import RoutingOptimizer


class WiringOptimizer(protected_module.WiringOptimizer if _open_source==True else RoutingOptimizer):
    def __init__(self, waypoints, routes):
        WiringOptimizer.__init__(self, waypoints, routes)
    

            
            
            
        