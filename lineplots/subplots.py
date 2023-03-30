import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
# import matplotlib.image as img

from subplot_helpers import *
from stats import run_stats, create_log_file

from make_bins import make_bins

from defaults import *
from ee_group_info import *


#------ DATA INFO - Fill in ------#

# Project
data_folder = "./data"
project = "Extended Extinction"
# cohorts = ["EE1","EE2"]
cohorts = ["EET"]  # combined EE1 + EE2 data
# rows_to_plot = ["ROW1","ROW2"]  # 2 rows of subplots. 
rows_to_plot = ["EET"]
scorer = "hp"


#------ FIGURE INFO ------#
fig_folder = "./figures"
save_figs = True
colored_backgrounds=True


# TODO: add arrows?
#   https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.ConnectionPatch.html?highlight=connectionpatch#matplotlib.patches.ConnectionPatch
# TODO: refactor lineplot_means, it is probably redundant.
#   would likely be better to directly call the helper functions somewhere.

set_font_sizes(title_size, font_size)

# shock = img.imread('./lineplots/lightning.png')

fig_subfolder = make_fig_subfolder(fig_folder)

log_filepath = create_log_file(
        fig_subfolder,
        cohorts,
        scorer,
        project=project
    )

posthoc_filepath = create_log_file(
        fig_subfolder,
        cohorts,
        scorer,
        project=project,
        filename='PAIRWISE.txt'
    )

for cohort in cohorts:
    for fig_index, fig_filename in enumerate(rows_to_plot):
        
        to_plot, rel_widths, rows, cols, size, subplot_spacing, session_names = figure_details(fig_filename)
        
        fig, axes = plt.subplots(
            nrows=rows,
            ncols=cols,
            figsize=size,
            sharey=True,
            gridspec_kw={'width_ratios':rel_widths}
        )

        # plt.tick_params(axis="both",which="major",labelsize=font_size)

        file_path = os.path.join(data_folder, f'{cohort.lower()}-{scorer.lower()}.xlsx')

        all_dfs = get_df_from_xlsx(file_path)

        for i, ax in enumerate(axes):
            s = to_plot[i]  # session code

            try:
                s_name = session_names[s.upper()]  # full session name from dict

                session_df = all_dfs[s.upper()]

                y_label = "% Freezing" if i==0 else None
                show_legend = (i==0) and (fig_filename=="ROW1" or fig_filename=="EET") #first panel of ROW1. TODO make this less sus

                if colored_backgrounds:
                    bg_color= graph_backgrounds.get(s.upper())
                else:
                    bg_color=None

                # if s == '1-AFC':  # TODO: bracket w/ lightning bolt for AFC
                #     ax.annotate('',
                #         xy = (2.5,-10),
                #         # xy=(.75,4.25),
                #         xytext=(2.5,-15),
                #         xycoords='data',
                #         ha='center',
                #         va='bottom',
                #         annotation_clip=False,
                #         arrowprops=dict(arrowstyle='-[, widthB=5.0, lengthB=.75'),
                #     )

                session_df = add_group_column(session_df,groups[cohort])

                session_df = make_bins(session_df)

                run_stats(
                    session_df,
                    s_name,
                    log_filepath,
                    posthoc_filepath=posthoc_filepath,
                )

                lineplot_means(
                    ax,
                    session_df,
                    group_colors=group_colors,
                    session_name=s_name,
                    show_legend=show_legend,
                    title_size=title_size,
                    font_size=font_size,
                    y_label=y_label,
                    bg_color=bg_color,
                    subtitle=session_subtitles.get(s)
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

        plt.subplots_adjust(wspace=subplot_spacing)
        

        fig.text(0.5, 0, 'Bin (2-trial average)', ha='center')

        if save_figs:
            fig_subfolder = save_fig(
                fig,
                fig_folder,
                fig_filename,
                cohort,
                scorer,
                existing_subfolder=fig_subfolder,  # if not 1st iteration, populated with created subfolder
                pickle_fig=True,
            )
        
        plt.close(fig)