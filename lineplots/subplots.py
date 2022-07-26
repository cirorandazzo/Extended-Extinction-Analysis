import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from subplot_helpers import *
from defaults import *
# from lineplot_bin_means import *

data_folder = "./data"
project = "Extended Extinction"
cohort = "ee1"  #TODO implement all
# sessions = "all" #TODO implement
scorer = "mel"  #TODO implement all

fig_folder = "./figures"
save_figs = True
colored_backgrounds=True

ee1_vns = [2,3,6,7,9,11]
ee1_sham = [1,4,5,8,10]
ee1_exclude = []

# TODO make one vns/sham group variable
groups = [ee1_vns, ee1_sham]

# ee2_vns = [1,3,6,8,9]
# ee2_sham = [2,4,5,7,10]
# ee2_exclude = [6] # cuff problems

# to_plot = ["1afc", "2cfrt", "3ext1", "4ext2"] 
# fig_filename = "ROW1"

rows_to_plot = ["ROW1","ROW2"]

# TODO: de-jank this?
def figure_details(fig_filename):
    if fig_filename=="ROW1":
        to_plot = ["1afc","2cfrt","3ext1","4ext2"]

        rel_widths = [2.5,1,4,4]
        rows = 1
        cols = 4
        size = (21,5)
        subplot_spacing = 0.05

    elif fig_filename=="ROW2":
        to_plot = ["5ret","6sr1","7sr2","8ren", "REINSTATEMENT","9rst"]

        rel_widths = [1,1,1,1,0.25,1]
        rows = 1
        cols = 6
        size = (21,5) 
        subplot_spacing = 0.1

    return to_plot, rel_widths, rows, cols, size, subplot_spacing

# TODO: make subplot function
# TODO: add arrows?
#   https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.ConnectionPatch.html?highlight=connectionpatch#matplotlib.patches.ConnectionPatch

set_font_sizes(title_size, font_size)

for fig_index, fig_filename in enumerate(rows_to_plot):
    
    to_plot, rel_widths, rows, cols, size, subplot_spacing = figure_details(fig_filename)
    
    fig, axes = plt.subplots(
        nrows=rows,
        ncols=cols,
        figsize=size,
        sharey=True,
        gridspec_kw={'width_ratios':rel_widths}
    )

    # plt.tick_params(axis="both",which="major",labelsize=font_size)

    p_vals = []
    for i, ax in enumerate(axes):
        s = to_plot[i]  # session code
        try:
            s_name = session_names[s]  # full session name from dict

            session_df = get_df(cohort, s, scorer, data_folder)

            y_label = "% Freezing" if i==0 else None
            show_legend = (i==0) and fig_filename=="ROW1" #TODO make this less sus

            if colored_backgrounds:
                bg_color= graph_backgrounds.get(s)
            else:
                bg_color=None

            session_p_vals = lineplot_bin_means(
                ax,
                session_df,
                groups,
                group_labels,
                group_colors=group_colors,
                session_name=s_name,
                show_legend=show_legend,
                title_size=title_size,
                font_size=font_size,
                y_label=y_label,
                bg_color=bg_color
            )
        except KeyError:
            # Not a session with data! Graph as a callout
            # TODO: generalize
            ax.set(
                facecolor=ctx_rst,
                xlim=(0,1),
                ylim=(0,1),
            )

            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)

            ax.text(
                0.5, 0.5, 'REINSTATEMENT',
                fontsize=title_size+2,
                rotation='vertical',
                color='white',
                fontweight='bold',
                verticalalignment='center',
                horizontalalignment='center',
                transform=ax.transAxes,
                )

        p_vals.append(session_p_vals)

    plt.subplots_adjust(wspace=subplot_spacing)
    

    fig.text(0.5, 0, 'Bin (2-trial average)', ha='center')

    if save_figs:
        if fig_index==0: # fig_subfolder doesn't exist yet
            fig_subfolder=None

        fig_subfolder = save_fig(
            fig_folder,
            fig_filename,
            project,
            cohort,
            scorer,
            to_plot,
            p_vals,
            existing_subfolder=fig_subfolder  # if not 1st iteration, populated with created subfolder
        )
    
    plt.close(fig)