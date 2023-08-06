#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pandas as pd
import numpy as np


def args_to_dtype(dtype):
    """ Convert arguments in a function to a specific data type, depending on what
        actions will be done with the arguments """

    def format_args(fn):
        def wrapper(*args, **kwargs):
            args = [dtype(x) if type(x) != dtype else x for x in args]
            return fn(*args, **kwargs)

        return wrapper

    return format_args


def pd_series_to_np_array(fn):
    """ Convert pandas.Series objects to numpy.array objects.  pd.Series.values is
    10x quicker than np.array(pd.Series) """

    def wrapper(*args, **kwargs):
        args = [pd.Series(x).values if type(x) != pd.Series else x.values for x in args]
        return fn(*args, **kwargs)

    return wrapper
