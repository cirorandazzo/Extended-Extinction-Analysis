import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import scipy.stats as stats

import os
import datetime

#--- EXTERNAL HELPERS---#

def lineplot_bin_means(
    ax,
    df,
    group_assignments,
    group_labels,
    group_colors=None,
    session_name=None,
    show_legend=True,
    show_sig=True,
    title_size=24,
    font_size=16,
    y_label="% Freezing",
    bg_color=None,
):

    """
    Given a matplotlib axis, plots errorbar for a single session.

    TODO: document
    """

    df_binned = _make_bins(df)
    
    # Separate into groups
    data = [df_binned.loc[group] for group in group_assignments]
    group_mean_by_bin = [group_df.mean() for group_df in data]
    group_error_by_bin = [group_df.sem() for group_df in data] 

    # Set Default Font Sizes
    plt.rc('font', size=font_size)
    plt.rc(
        'axes',
        titlesize=title_size,
        labelsize=font_size
    )

    # Plot
    p_vals = _make_axes(
        ax,
        session_name,
        group_mean_by_bin,
        group_error_by_bin,
        group_labels,
        group_colors,
        font_size,
        title_size,
        show_sig,
        show_legend,
        y_label,
        data,
        bg_color
    )

    return p_vals


def get_date_string(date_format="%Y-%m-%d"):
    """
    Returns string of current date in date_format
    """
    now = datetime.datetime.now()
    return now.strftime(date_format)


def get_df(
    cohort,
    session_code,
    scorer,
    data_folder,
    time_per_trial=30
):
    """
    - Reads df from CSV file
    - Re-indexes df to animal ID ("RAT")
    - Change seconds into percents
    """
    # session data
    file_name = cohort + "-" + session_code + "-" + scorer + ".csv"
    file_path = os.path.join(data_folder, cohort, file_name)

    df = pd.read_csv(file_path)  # make df from file
    df.set_index("RAT",inplace=True)  # reindex to animal ID

    df = 100 * df / time_per_trial  # change into percents

    return df


def save_fig(
    fig_folder,
    fig_filename,
    project,
    cohort,
    scorer,
    sessions_plotted,
    p_vals,
    log_filename = "log.txt",
):
    """
    TODO: document

    """

    date = get_date_string()

    i=0
    while True:
        try:
            fig_subfolder = os.path.join(fig_folder, date, str(i))
            os.makedirs(fig_subfolder)

            log_filename = os.path.join(fig_subfolder, log_filename)
            with open(log_filename,'a') as f:
                f.write(project.upper() + " ANALYSIS" + "\n")
                f.write("Cohort: " + cohort + "\n")
                f.write("Scorer: " + scorer + "\n\n")

            break
        except FileExistsError:
            i+=1
    
    fig_file = os.path.join(fig_subfolder, fig_filename)
    
    plt.savefig(
        fig_file+".png",
        bbox_inches="tight",
    )

    with open(log_filename,'a') as f:
        for s_i, s_name in enumerate(sessions_plotted):
            f.write("---" + s_name + "---\n")
            session_p_vals = p_vals[s_i]
            for i, p in enumerate(session_p_vals):
                p = np.around(p,5)
                if p<=0.05:
                    f.write("*")
                f.write(str(i+1) + ": " + str(p) + "\n")
            f.write("\n")


#--- LOCAL HELPERS ---#

def _make_bins(df):
    '''
    Make new dataframe of bins, which consist of average of 2 trials

    Notes on baseline trials:
        - Denoted by "BL#" in original dataframe
        - In binned output, BL trials are numbered -(n-1) to 0 rather than being labeled with a string (makes graphing easier); n = number of bl bins
    '''

    df_binned = pd.DataFrame(index=df.index) # new df with same index

    num_bl_trials = len([s for s in df.columns if "BL" in s.upper()])  # count number of baseline sessions in data
    num_bl_bins = int(num_bl_trials/2)
    num_nonbl_bins = int(df.shape[1] / 2) - num_bl_bins

    # binning baseline sessions
    for i in range(0, num_bl_bins):
        # names of bl bins in original df
        a = "BL"+str((2*i)+1)
        b = "BL"+str((2*i)+2)
        
        trial = 1-(num_bl_bins-i)  # bl bins are called -(n-1) to 0; n= # bl bins

        df_binned[trial] = df.loc[:,a:b].mean(axis=1) # add bl bin to new df

    # binning non-BL sessions
    for i in range(0, num_nonbl_bins):
        a = str((2*i)+1)
        b = str((2*i)+2)

        trial = i+1

        df_binned[trial] = df.loc[:,a:b].mean(axis=1)
    
    return df_binned


def _make_axes(
    ax,
    session_name,
    group_mean_by_bin,
    group_error_by_bin,
    group_labels,
    group_colors,
    font_size,
    title_size,
    show_sig,
    show_legend,
    y_label,
    data,
    bg_color,
):
    """
    Given an Axes and a session, plot errorbar for each group in that session. Returns numpy array containing p-values between groups for each bin in this session.
    """
    # plot errorbar for each group, on same Axes
    for grp_i in range(0,len(group_mean_by_bin)):
        ax.errorbar(
            x=group_mean_by_bin[grp_i].index,
            y=group_mean_by_bin[grp_i],
            yerr=group_error_by_bin[grp_i],
            label=group_labels[grp_i],
            color=group_colors[grp_i],
            marker=".", markersize=font_size,
            capsize=8,
            elinewidth=2,
            capthick=2,
        )

    # manually set xlim, otherwise some are squished
    xmin = min(group_mean_by_bin[0].index)-0.5
    xmax = max(group_mean_by_bin[0].index)+0.5

    ax.set(
        title=session_name,
        xlim=[xmin,xmax],
        xticks=list(group_mean_by_bin[0].index),  #[i for i in range(1,len(group_mean_by_bin[0])+1)],
        ylim=[0,100],
        ylabel= y_label,
        
    )

    if bg_color is not None:
        ax.set_facecolor(color=bg_color)

    p_vals = stats.ttest_ind(data[0],data[1], nan_policy="omit")[1]

    if show_sig:
        _label_significance(ax, group_mean_by_bin, group_error_by_bin, p_vals, title_size)
        
    _add_x_labels(ax, trials=group_mean_by_bin[0].index)

    # TODO : annotate for VNS label on top

    if show_legend:
        ax.legend()

    return p_vals


def _add_x_labels(ax, trials):
    """
    Given an Axes, renames all trials >=0 as "BL#.
    
    If only 1 BL session, simply calls this "BL" (rather than "BL1")
    """
    num_bl_bins = sum(map(lambda i: i<=0, trials))  # count BL trials, index <=0

    x_labels = []
    for c in trials:
        if c<=0:  # for BL bins
            if num_bl_bins==1:  # label "BL" if only 1
                x_labels.append("BL")
            else:  # else, label "BL1" thru "BL#"
                x_labels.append("BL"+str(c+num_bl_bins))
        else:
            x_labels.append(str(c))

    ax.set_xticklabels(
        labels = x_labels
    )


def _label_significance(
    ax,
    group_mean_by_bin,
    group_error_by_bin,
    p_vals,
    font_size=None,
):
    """
    Given an Axes and p-values, adds text/stars labelling significance to the Axes.
    """
    for i, p in enumerate(p_vals):
        bin = group_mean_by_bin[0].index[i]  # get bin ID. necessary for BLs (bin != i)

        bin_group_means = [group[bin] for group in group_mean_by_bin]
        
        max_group_mean = max(bin_group_means)
        max_group_id = bin_group_means.index(max_group_mean)
        
        error_of_max = group_error_by_bin[max_group_id][bin]
            
        if p > 0.06:
            bin_label=None
        elif p > 0.05 and p < 0.06:
            bin_label = "p=0.05"
        else:
            bin_label = _get_sig_stars(p)
        
    ax.text(
            x=bin,
            y=max_group_mean + error_of_max + 5,
            s=bin_label,
            horizontalalignment="center",
            fontsize=font_size,
        )


def _get_sig_stars(p):
    """
    Given a p-value, returns string containing star label, as follows:
        - < .0005:       ***
        - [.0005, .005): **
        - [.005, .05):   *
        - >= 0.05: (empty string)
    
    
    """

    if p>=.05:
        return ""
    elif p<0.05 and p>=.005:
        return "*"
    elif p<.005 and p>= .0005:
        return "**"
    else:
        return "***"