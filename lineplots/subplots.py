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

to_plot = ["5ret","6sr1","7sr2","8ren","9rst"]
fig_filename = "ROW2"

rel_widths = [1,1,1,1,1]
rows = 1
cols = 5
size = (17,6)
 
fig, axes = plt.subplots(
    nrows=rows,
    ncols=cols,
    figsize=size,
    sharey=True,
    gridspec_kw={'width_ratios':rel_widths}
)

p_vals = []
for i, ax in enumerate(axes):
    s = to_plot[i]  # session code
    s_name = session_names.get(s)  # full session name from dict

    session_df = get_df(cohort, s, scorer, data_folder)

    y_label = "% Freezing" if i==0 else None
    show_legend = (i==0) and fig_filename=="ROW1" #TODO make this less sus

    session_p_vals = lineplot_bin_means(
        ax,
        session_df,
        groups,
        group_labels,
        group_colors=group_colors,
        session_name=s_name,
        show_legend=show_legend,
        title_size=16,
        font_size=12,
        y_label=y_label
    )
    
    p_vals.append(session_p_vals)

plt.subplots_adjust(wspace=0.05)

if save_figs:
    save_fig(
        fig_folder,
        fig_filename,
        project,
        cohort,
        scorer,
        to_plot,
        p_vals,
    )