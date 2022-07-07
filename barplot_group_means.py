import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from barplot_brackets import *

def barplot_group_means(
    x,
    y,
    lbls,
    error="STD", 
    p=None,
    colors="blue",
    w=0.8,
    size=(6,6),
    ylbl="Freezing (%)",
    show=False
):

    """Bar plot of group means

    @type x: list of int
    @param x: x coord for bar corresponding to each group

    @type y: list of pandas series
    @param y: Each entry in this list represents a group, and contains list of values for each individual; mean of each group is plotted
    
    @type lbls: list of strings
    @param lbls: labels for each bar, in the same order as x/y
    
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
    fig, ax = plt.subplots(figsize=size)

    bars = [group.mean() for group in y] # bar height = group mean
    if error.upper() == "STD":
        error_bars = [group.std() for group in y]  # error bar height = STD

    ax.bar(
        x=x,
        height=bars,
        tick_label=lbls,
        color=colors,
        width=w,
        yerr=error_bars,
        capsize=12
    )

    ax.set(
        # xlim=(0,5),
        ylim=(0,120),
        yticks=range(0,120,20),
        ylabel=ylbl
    )

    for i in range(len(x)):
        ax.scatter(
            x=x[i]+np.zeros(len(y[i])),
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