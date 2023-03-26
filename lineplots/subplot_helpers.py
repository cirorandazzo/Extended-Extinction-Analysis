import numpy as np
import pandas as pd
import pingouin as pg

import matplotlib.pyplot as plt
import scipy.stats as stats

import os
import datetime

#--- EXTERNAL HELPERS---#

def lineplot_means(
    ax,
    df,
    group_colors=None,
    session_name=None,
    show_legend=True,
    title_size=24,
    font_size=16,
    y_label="% Freezing",
    bg_color=None,
    subtitle=None,
    show_sig=True,
    p_vals=None,
):

    """
    Given a matplotlib axis, plots errorbar for a single session.

    TODO: document
    """

    group_labels = list(df['Group'].unique())

    # Separate into groups
    data = [df.loc[df['Group']==group] for group in group_labels]
    
    group_mean_by_bin = [group_df.mean() for group_df in data]
    group_error_by_bin = [group_df.sem() for group_df in data] 
    group_sizes = [len(grp) for grp in data]

    # Plot
    _make_axes(
        ax,
        session_name,
        group_mean_by_bin,
        group_error_by_bin,
        group_sizes,
        group_labels,
        group_colors,
        font_size,
        title_size,
        show_legend,
        y_label,
        bg_color,
        p_vals=None # TODO: add pvals from ANOVA
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
    
    return


def get_date_string(date_format="%Y-%m-%d"):
    """
    Returns string of current date in date_format
    """
    now = datetime.datetime.now()
    return now.strftime(date_format)


def set_font_sizes(title_size, font_size):
    font = {'size'      : font_size}
    
    axes = {'titlesize' : title_size,
            'labelsize' : font_size}

    plt.rc('font', **font)
    plt.rc('axes', **axes)


def get_df_from_csv(
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

def get_df_from_xlsx(
    file_path,
    cohort = "multiple",
    session_codes=None,
    time_per_trial=30
):
    """
    Reads dfs from XLSX file

    parameters
    - file_path: full file path to XLSX file to be read
    - cohort: string containing groups.
    - session_codes: list of strings. names of sheets to read from this file, or None for all sheets (default).
    - time per trial: maximum scoring length per trial. default=30, since each trial is scored out of 30 seconds.
    
    Also:
    - Re-indexes df to cohort-animal ID (eg, 'EE1A1')
    - Change seconds into percents
    """
    
    df_dict = pd.read_excel(
        file_path,
        sheet_name=session_codes, # all sheets
        header=0, # first row header
        index_col=0, # first column index
    )

    for session in df_dict: 
        df_dict[session]
        if cohort == "multiple" and df_dict[session].index.name == "Group": # concatenate group + animal ID 
            new_index = (df_dict[session].index + df_dict[session]["Animal ID"]).values
            df_dict[session].set_index(new_index, inplace=True)
            df_dict[session].drop("Animal ID", axis=1, inplace=True)

        df_dict[session] = df_dict[session]/time_per_trial*100 # normalize to percent
    # if isinstance(df_dict, pd.DataFrame):
    #     # only 1 session, so pd.read_excel() returns a dataframe
    #     return df_dict  
    # else:
    #     # >1 session, pd.read_excel() returns dictionary of dataframes (sheet_name:pd.DataFrame)
    #     all_sessions = df_dict.keys()
    #     dfs = []

    #     for session in all_sessions:
    #         session_df = df_dict.get(session)
    #         session_df.name = session
    #         dfs.append(session_df)
    
    #     return dfs
    return df_dict



def save_fig(
    fig_folder,
    fig_filename,
    cohort,
    scorer,
    existing_subfolder=None,
    log_filename = "LOG",
    cohort_in_filename = True,
):
    """
    TODO: document

    """

    if cohort_in_filename:
        fig_filename = f"{cohort}_{scorer}-{fig_filename}"

    if existing_subfolder is not None:
        fig_subfolder = existing_subfolder
    else:
        # Make new subfolder
        fig_subfolder = make_fig_subfolder(fig_folder)

    # Save figure
    fig_file = os.path.join(fig_subfolder, fig_filename)
    plt.savefig(
        f"{fig_file}.png",
        bbox_inches="tight",
    )

    return fig_subfolder


def make_fig_subfolder(fig_folder):
    date = get_date_string()
    i=0
    while True:
        try:
            fig_subfolder = os.path.join(fig_folder, date, str(i))
            os.makedirs(fig_subfolder)

            break
        except FileExistsError:
            i+=1
    return fig_subfolder


#--- LOCAL HELPERS ---#

def add_group_column(
    df,
    group_dict
):
    """
    TODO: document

    group_dict: dictionary. keys are group labels, values are animal IDs within that group. eg, {"EE1": [1,3,4]}, "EE2": [2,5,6]}
    """

    group_codes_by_id = [None] * len(df.index)

    for group in group_dict:
        if len(group_dict[group])==0:
            continue
        elif 'A' in group_dict[group][0]:
            break  # combined data already has prefixes
        else:
            group_dict[group] = [f'A{i}' for i in group_dict[group]]  # appends "A" to animal numbers

    for i, animal in enumerate(df.index):
        for group in group_dict:
            if animal in group_dict[group]:
                group_codes_by_id[i] = group
                break

    df['Group'] = group_codes_by_id

    return df

def _make_axes(
    ax,
    session_name,
    group_mean_by_bin,
    group_error_by_bin,
    group_sizes,
    group_labels,
    group_colors,
    font_size,
    title_size,
    show_legend,
    y_label,
    bg_color,
    line_width = 3,
    p_vals=None,
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
            label= group_labels[grp_i] + " (%(n)i)"%{'n':group_sizes[grp_i]},
            color=group_colors[grp_i],
            marker=".", markersize=font_size,
            capsize=8,
            elinewidth=line_width,
            capthick=line_width,
            linewidth=line_width
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

    if p_vals is not None:
        _label_significance(ax, group_mean_by_bin, group_error_by_bin, p_vals, title_size)
        
    _add_x_labels(ax, trials=group_mean_by_bin[0].index)

    # TODO : annotate for VNS label on top

    if show_legend:
        ax.legend()

    return


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
