import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from barplot_brackets import *

def barplot_group_means(
    y,
    lbls,
    fig=None,
    ax=None,
    error="STD", 
    p=None,
    colors="blue",
    bg_color=None,
    w=0.8,
    size=(6,6),
    ylbl="Freezing (%)",
    show=False,
    title=None,
):

    """Bar plot of group means

    TODO: edit this, make the way it deals with groups more similar to line plot

    @type y: list of pandas series
    @param y: Each entry in this list represents a group, and contains list of values for each individual; mean of each group is plotted
    
    @type lbls: list of strings
    @param lbls: labels for each bar, in the same order as y
    
    @type error: str
    @param error: determines whether error bars are added, "STD" or None
    
    @type p: int
    @param p: p value between 2 groups
    
    @type colors: see matplotlib documentation
    @param colors: contains color information for each bar
    
    @type w: int
    @param w: bar width

    @type size: list of float
    @param size: size of figure (in inches, probably?)

    @type ylbl: str
    @param ylbl: Label for y-axis of plot

    @type show: bool
    @param show: If true, displays plot output

    @returns: fig, ax (see matplotlib)
    """

    # Graph
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=size)
    else:
        ax.clear()

    if isinstance(y, pd.Series):
        y = [y]  # handle only 1 group being passed as a pandas Series.

    x = len(y)  # how many bars?
    bars = [group.mean() for group in y] # bar height = group mean

    if error.upper() == "STD":
        error_bars = [group.std() for group in y]  # error bar height = STD

    ax.bar(
        x=range(x),
        height=bars,
        tick_label=lbls,
        color=colors,
        width=w,
        yerr=error_bars,
        capsize=12,
    )

    ax.set(
        # xlim=(0,5),
        ylim=(0,100),
        yticks=range(0,101,20),
        ylabel=ylbl,
        title=title,
    )

    if bg_color is not None:
        ax.set_facecolor(color=bg_color)

    for i in range(x):
        ax.scatter(
            x=i+np.zeros(len(y[i])),
            y=y[i],
            s=60,
            color="black",
            marker="o",
            facecolors="none",
            edgecolors="black"
            )

    if p is not None:
        barplot_brackets(
            lbar=0,
            rbar=1,
            label=p,
            center=x,
            height=bars,
            yerr=error_bars,
            fs=16
        )

    if show:
        plt.show(fig)

    return fig, ax