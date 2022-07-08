import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


def lineplot_bin_means(
    df,
    group_assignments,
    group_labels,
    group_colors=None,
    legend=True,
    session_name=None,
    show_sig=True,
    size=(6,6),
    ylbl="% Freezing",
):

    """
    TODO: document
        
    """

    df_binned, bl_bins = make_bins(df)
    
    # Separate into groups
    data = [df_binned.loc[group] for group in group_assignments]
    group_mean_by_bin = [group_df.mean() for group_df in data]
    group_error_by_bin = [group_df.sem() for group_df in data] 

    # Plot
    fig, ax = plt.subplots(figsize=size)

    # plot errorbar for each group, on same Axes
    for grp_i in range(0,len(group_mean_by_bin)):
        ax.errorbar(
            x=group_mean_by_bin[grp_i].index,
            y=group_mean_by_bin[grp_i],
            yerr=group_error_by_bin[grp_i],
            label=group_labels[grp_i],
            color=group_colors[grp_i],
            marker=".", markersize=12,
            capsize=4,
        )

    ax.set(
        title=session_name,
        xticks=list(group_mean_by_bin[0].index),  #[i for i in range(1,len(group_mean_by_bin[0])+1)],
        ylim=[0,100],
        ylabel= ylbl,
    )

    p_vals = stats.ttest_ind(data[0],data[1])[1]

    if show_sig:
        for i in range(0,len(p_vals)):
            p = p_vals[i]

            bin = group_mean_by_bin[0].index[i]

            bin_group_means = [group[bin] for group in group_mean_by_bin]
            max_group_mean = max(bin_group_means)
            max_group_id = bin_group_means.index(max_group_mean)
            error_of_max = group_error_by_bin[max_group_id][bin]
            
            if p > 0.06:
                bin_label=None
            elif p > 0.05 and p < 0.06:
                bin_label = "p=0.05"
            else:
                bin_label = get_sig_stars(p)
        
        ax.text(
            x=bin,
            y=max_group_mean + error_of_max + 5,
            s=bin_label
        )
        
                
    # Labelling BL sessions
    x_labels = []
    for c in group_mean_by_bin[0].index:
        if c<=0:  # for BL bins
            if bl_bins==1:  # label "BL" if only 1
                x_labels.append("BL")
            else:  # else, label "BL1" thru "BL#"
                x_labels.append("BL"+str(c+bl_bins))
        else:
            x_labels.append(str(c))

    ax.set_xticklabels(
        labels = x_labels
    )

    # TODO : annotate for VNS label on top

    if legend:
        ax.legend()

    return fig, ax


def make_bins(df):
    '''
    Make new dataframe of bins, which consist of average of 2 trials
    '''
    # Bins of 2 trials

    df_bins = pd.DataFrame(index=df.index)

    bl_sessions = [s for s in df.columns if "BL" in s.upper()]  # count number of baseline sessions in data

    bl_bins = int(len(bl_sessions)/2)
    bins = int(df.shape[1] / 2) - bl_bins

    # binning baseline sessions
    for i in range(0,bl_bins):
        a = "BL"+str(2*i+1)
        b = "BL"+str((2*i)+2)
        
        trial = 1-(bl_bins-i)  # bl bins are called -(n-1) to 0; n= # bl bins

        df_bins[trial] = df.loc[:,a:b].mean(axis=1)

    # bins
    for i in range(0,bins):
        a = str((2*i)+1)
        b = str((2*i)+2)

        trial = i+1

        df_bins[trial] = df.loc[:,a:b].mean(axis=1)
    
    return df_bins, bl_bins

def get_sig_stars(p):
    if p<0.05 and p>=.005:
        return "*"
    elif p<.005 and p>= .0005:
        return "**"
    else:
        return "***"