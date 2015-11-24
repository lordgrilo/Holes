"""

Holes
========

    Holes (ho) is a Python package for the pre-processing, manipulation, and
    study of the structure, dynamics, and functions of the homological structure of
    complex networks.

    http://lordgrilo.github.com/

Using
-----

    Just write in Python

    >>> import Holes as ho
    
"""
#    Copyright (C) 2012-2020 by
#    Giovanni Petri  <petri.giovanni@gmail.com>
#    All rights reserved.
#    BSD license.
#
#

from __future__ import absolute_import

import sys, os
if sys.version_info[:2] < (2, 6):
    m = "Python version 2.6 or later is required for NetworkX (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

import pickle
import numpy as np
import networkx as nx
import pylab 
import matplotlib.pyplot as plt


import Holes.classes
from Holes.classes import *

import Holes.drawing
from Holes.drawing import * 

import Holes.measures
from Holes.measures import * 

import Holes.operations
from Holes.operations import *

import Holes.perseus_utils
from Holes.perseus_utils import *





