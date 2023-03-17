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
    subtitle=None,
):

    """
    Given a matplotlib axis, plots errorbar for a single session.

    TODO: document
    """

    df_binned = _make_bins(df)
    
    # Separate into groups
    data = []
    # [df_binned.loc[f'A{group}'] for group in group_assignments]

    for group in group_assignments:
        animal_ids = [f'A{i}' for i in group]  # appends "A" to animal numbers
        data.append(df_binned.loc[animal_ids])

    group_mean_by_bin = [group_df.mean() for group_df in data]
    group_error_by_bin = [group_df.sem() for group_df in data] 
    group_sizes = [len(grp) for grp in data]

    # Plot
    p_vals = _make_axes(
        ax,
        session_name,
        group_mean_by_bin,
        group_error_by_bin,
        group_sizes,
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

    return p_vals


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
    cohort,
    scorer,
    data_folder='./data',
    session_codes=None,
    time_per_trial=30
):
    """
    Reads dfs from XLSX file named {cohort}-{scorer}.xlsx (eg, ee1-cdr.xlsx)

    parameters
    - cohorts (string): group name of data file to read (eg, 'EE1')
    - scorer (string): scorer initials of data file to read (eg, 'cdr')
    - data_folder (string): string containing file path to data folder. default is '.data'
    - session_codes: list of strings. names of sheets to read from this file, or None for all sheets (default).
    - time per trial: maximum scoring length per trial. default=30, since each trial is scored out of 30 seconds.
    
    Also:
    - Re-indexes df to cohort–animal ID (eg, 'EE1A1')
    - Change seconds into percents
    """
    
    file_path = os.path.join(data_folder, f'{cohort.lower()}-{scorer.lower()}.xlsx')
    
    df_dict = pd.read_excel(
        file_path,
        sheet_name=session_codes, # all sheets
        header=0, # first row header
        index_col=0, # first column index
    )

    for session in df_dict:  # normalize to percent
        df_dict[session] = df_dict[session]/time_per_trial*100
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
    project,
    cohort,
    scorer,
    sessions_plotted,
    p_vals,
    existing_subfolder=None,
    log_filename = "LOG",
    cohort_in_filenames = True,
):
    """
    TODO: document

    """

    if cohort_in_filenames:
        fig_filename = f"{cohort}_{scorer}-{fig_filename}"
        log_filename = f"{cohort}_{scorer}-{log_filename}"

    if existing_subfolder is not None:
        fig_subfolder = existing_subfolder
    else:
        # Make new subfolder
        fig_subfolder = _make_fig_subfolder(fig_folder)


    if not log_filename.endswith('.txt'):
        log_filename = f'{log_filename}.txt'
        
    log_filename = os.path.join(fig_subfolder, log_filename)
    
    # Make new log file if necessary
    if not os.path.exists(log_filename):
        with open(log_filename,'a') as f:
            f.write(project.upper() + " ANALYSIS" + "\n")
            f.write("Cohort: " + cohort + "\n")
            f.write("Scorer: " + scorer + "\n\n")
        

    # Save figure
    fig_file = os.path.join(fig_subfolder, fig_filename)
    plt.savefig(
        f"{fig_file}.png",
        bbox_inches="tight",
    )

    # Write p-vals to log
    _log_pvals(fig_filename, sessions_plotted, p_vals, log_filename)

    return fig_subfolder




#--- LOCAL HELPERS ---#

def _make_fig_subfolder(fig_folder):
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


def _log_pvals(
        fig_filename,
        sessions_plotted,
        p_vals, 
        log_filename
):
    with open(log_filename,'a') as f:
        f.write(f"\nFigure: {fig_filename} \n")
        for s_i, s_name in enumerate(sessions_plotted):
            f.write(f"---{s_name}---\n")
            session_p_vals = p_vals[s_i]
            for bin_no, p in enumerate(session_p_vals):
                p = np.around(p,5)
                if p<=0.05:
                    f.write("*")
                f.write(f"{bin_no+1!s}: {p!s} \n")
            f.write("\n")


def _make_bins(df):
    '''
    Make new dataframe of bins, which consist of average of 2 trials

    Notes on baseline trials:
        - Denoted by "BL#" in original dataframe
        - In binned output, BL trials are numbered -(n-1) to 0 rather than being labeled with a string (makes graphing easier); n = number of bl bins
    '''

    df_binned = pd.DataFrame(index=df.index) # new df with same index

    num_bl_trials = len([s for s in df.columns if "BL" in str(s).upper()])  # count number of baseline sessions in data
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
        a = (2*i)+1
        b = (2*i)+2

        trial = i+1

        df_binned[trial] = df.loc[:,a:b].mean(axis=1)
    
    return df_binned


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
    show_sig,
    show_legend,
    y_label,
    data,
    bg_color,
    line_width = 3
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