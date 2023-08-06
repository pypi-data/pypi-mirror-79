#!/usr/bin/env python
"""
Automated label placement.

Approach
1. Determine where stuff is.
   - Get all plot elements using ax.get_children();
     Extract paths. If it is a closed path, cordon off that area.
   - Convert to image. Determine background pixels.
2. Initial placement of labels?
   - randomly?
   - at closest possible point?
3. Optimise label placement using a force directed layout.
"""

import numpy as np
import matplotlib.pyplot as plt



if __name__ == '__main__':
    pass
