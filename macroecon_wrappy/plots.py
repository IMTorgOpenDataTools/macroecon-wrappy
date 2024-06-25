#!/usr/bin/env python3
"""
Tools for plotting techniques
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from . import load

import pandas as pd
import numpy as np
import plotnine as p9

import warnings


def graph_ts(df, cols=[], recession_bars=True, log_y=True, conf_region=False, height=3, width=6):
    """Create a timeseries graph with typical econometric characteristics.
    Notes:
        - ensure to use `p.save(buf, verbose = False)` for efficient saving

    #TODO: integrate with Measure
    """
    warnings.filterwarnings('ignore')

    if len(cols)==1:
        aesthetics = p9.aes(x='date', y=cols[0], group=1)
        g = (
            p9.ggplot() 
            + p9.geom_smooth(df, aesthetics)
            + p9.theme(figure_size=(width, height))
        )
    elif len(cols)>1:
        '''#alternative approach to melt()
        tmp = df
        tmp['id'] = tmp.index
        tmp = pd.wide_to_long(tmp, ["value"], i='id', j="grp")
        tmp['grp'] = [x[1] for x in tmp.index]
        '''
        tmp = df
        tmp = tmp.reset_index()
        tmp = pd.melt(tmp, id_vars='date', value_vars=['value1', 'value2'], var_name='grp', value_name='value')
        
        aesthetics = p9.aes(x='date', y='value', color='factor(grp)')
        g = (
            p9.ggplot() 
            + p9.geom_smooth(tmp, aesthetics)
            + p9.theme(figure_size=(width, height))
        )
    else:
        raise Exception('need at least one columns to graph')
    if recession_bars:
        if 'bars_df' not in globals():
            bars_df = load.get_recession_bars()
        mn = np.min(df['date'])
        mx = np.max(df['date'])
        bars_mod = bars_df[bars_df.peak > mn]
        bars_mod = bars_mod[bars_mod.trough < mx]
        g = g + p9.geom_rect(
            bars_mod, 
            p9.aes(xmin='peak', xmax='trough', ymin=0, ymax=np.inf), 
            alpha=0.1, fill='#595959'
        )
    if log_y:
        g = g + p9.scale_y_log10()
    if conf_region:
        g = g + p9.geom_smooth(tmp, aesthetics, method='lm')
    return g