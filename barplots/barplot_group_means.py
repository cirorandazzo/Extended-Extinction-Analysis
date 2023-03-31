import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from barplot_brackets import *

def barplot_group_means(
    subj_means_by_group,
    ax=None,
    group_colors=None,
    title=None,
    font_size=26,
    y_label="Freezing (%)",
    bg_color=None,
    subtitle=None,
    p=None,
    # ---barplot-specific--- #
    error="STD", 
    w=0.8,
    size=(6,6),
):

    """Bar plot of group means

    TODO: edit this, make the way it deals with groups more similar to line plot

    @type subject_means_by_group: dict
    @param subject_means_by_group: dict where keys are group labels and value for each key is a pandas series containing mean for each individual subject in a given session
    
    @type error: str
    @param error: determines whether error bars are added, "STD" or None
    
    @type p: int
    @param p: p value between 2 groups
    
    @type colors: dict
    @param colors: keys are group names, values contain color information for each bar (see Matplotlib for color picking documentation)
    
    @type w: int
    @param w: bar width

    @type size: list of float
    @param size: dimensions of figure to create if not passed a pre-existing plt.axes

    @type ylbl: str
    @param ylbl: Label for y-axis of plot

    @type show: bool
    @param show: If true, displays plot output

    @returns: fig, ax (see matplotlib)
    """

    fig = None
    if ax is None:
        fig, ax = plt.subplots(figsize=size)
    else:
        ax.clear()

    x = len(subj_means_by_group)  # how many bars? 
    
    bars = [subj_means_by_group[group].mean() for group in subj_means_by_group] # bar height = group mean

    if error.upper() == "STD":
        error_bars = [subj_means_by_group[group].std() for group in subj_means_by_group] # error bar height = STD

    if isinstance(group_colors, dict):
        group_colors = [group_colors[group] for group in subj_means_by_group]

    ax.bar(
        x=range(x),
        height=bars,
        tick_label=list(subj_means_by_group.keys()),
        color=group_colors,
        width=w,
        yerr=error_bars,
        capsize=12,
    )

    ax.set(
        # xlim=(0,5),
        ylim=(0,100),
        yticks=range(0,101,20),
        ylabel=y_label,
        title=title,
        facecolor=bg_color,
    )

    if bg_color is not None:
        ax.set_facecolor(color=bg_color)

    for i,group in enumerate(subj_means_by_group):
        ax.scatter(
            x=i+np.zeros(len(subj_means_by_group[group])),
            y=subj_means_by_group[group],
            s=60,
            color="black",
            marker="o",
            facecolors="none",
            edgecolors="black"
            )

    if subtitle is not None:
        ax.text(
            0.5, 0.95, subtitle,
            fontsize=font_size,
            color='black',
            fontstyle='italic',
            verticalalignment='center',
            horizontalalignment='center',
            transform=ax.transAxes,
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

    return fig, ax

def subj_mean_by_group(df):
    df2 = df.dropna(axis=0, subset='Group')  # drop rows without group

    subj_mean_by_group = {}
    for group in df2['Group'].unique():
        subj_means = df2[df2['Group']==group].mean(axis=1)
        subj_means.drop(columns='Group', inplace=True)
        
        subj_mean_by_group[group] = subj_means

    return subj_mean_by_group