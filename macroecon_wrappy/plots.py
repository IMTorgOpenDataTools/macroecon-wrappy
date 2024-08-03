#!/usr/bin/env python3
"""
Tools for plotting techniques
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from . import load
from . import Measure

import pandas as pd
import numpy as np
import plotnine as p9
import altair as alt

import warnings
alt.data_transformers.disable_max_rows()



def graph_ts_js(df_or_measure, cols=[], recession_bars=True, log_scale='xy', interval_selection=True, conf_region=False, height=3, width=6, type='js', return_type=False):
    """Create a timeseries graph with typical econometric characteristics.
    Notes:
        - ensure to use `p.save(buf, verbose = False)` for efficient saving

    """

    #(chart)type
    if type=='js':
        pass
    elif type=='offline':
        alt.renderers.enable("browser", offline=True)
    elif type=='svg':
        alt.renderers.enable("svg")
    elif type=='png':
        alt.renderers.enable("png", scale_factor=2, ppi=144)
    else:
        raise Exception(f'arg type {type} is not available')

    #chart base
    if isinstance(df_or_measure, pd.DataFrame):
        recession_bars = False
        df = df_or_measure
        df.index.set_names(['timestamp'], inplace=True)
        data = df.reset_index() \
            .dropna(axis=0) \
            .rename(columns={'timestamp':'x', cols[0]: 'y'})
    elif isinstance(df_or_measure, Measure):
        measure = df_or_measure
        if len(cols)>0:
            for col in cols:
                if col not in measure.df().columns:
                    raise Exception(f"arg {col} contains metrics not in Measure")
        else:
            cols = measure.df().columns.to_list()
        long = measure.to_long() \
            .reset_index() \
            .dropna(axis=0) \
            .rename(columns={'timestamp':'x', 'value': 'y'})
        data = long[long['grp'].isin(cols)]
        rect_data = measure.get_cycle().df()
    base = alt.Chart(data, width=600, height=200)

    #scales
    if log_scale!=None:
        if log_scale == 'x':
            points = base.mark_line().encode(
                alt.X('x:T').scale(type='log'),
                alt.Y('y:Q'),
                alt.Color('grp')
            )
        if log_scale == 'y':
            points = base.mark_line().encode(
                alt.X('x:T'),
                alt.Y('y:Q').scale(type='log'),
                alt.Color('grp')
            )
        if log_scale == 'xy':
            points = base.mark_line().encode(
                alt.X('x:T').scale(type='log'),
                alt.Y('y:Q').scale(type='log'),
            )
    else:
        points = base.mark_line().encode(
            alt.X('x:T'),
            alt.Y('y:Q')
            )
        
    #recession bars
    if recession_bars:
        '''
        rect_data = pd.DataFrame({
            "x1": [-2, 1],
            "x2": [-1, 2]
        })'''
        rect = alt.Chart(rect_data).mark_rect(opacity=0.9).encode(
            x="start",
            x2="end",
            color=alt.ColorValue("#e6e6e6")
        )
    else:
        rect = None

    #interval selection
    if interval_selection:
        brush = alt.selection_interval(encodings=['x'])
        #works:
        #upper = points.encode(alt.X('x').scale(domain=brush))
        tmpx = points.encoding.x
        upper = points.encode(tmpx.scale(domain=brush))
        #fails:
        #upper = points
        #upper.encoding.x = alt.X('x:Q').scale(domain=brush)
        #upper.encoding.x = points.encoding.x.scale(domain=brush)
        lower = points.properties(height=60).add_params(brush)

    if rect:
        chart = (rect + upper) & (rect + lower)
    else:
        chart = upper & lower

    """
    if return_type=='json':
        return chart.to_json()
    elif return_type=='inline':
        return chart.save('chart.html', inline=True)
    else:
        return True
    """
    return chart







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