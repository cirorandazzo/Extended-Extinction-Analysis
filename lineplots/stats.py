import numpy as np
import pandas as pd
import pingouin as pg

import os

def run_stats(
    df,
    session_name,
    log_filepath,
    pairwise_filepath=None,

):
    """
    TODO: documentation
    """

    pivoted_df = _pivot_df(df)

    anova_summary = pg.mixed_anova(
        pivoted_df,
        dv='Freezing',
        between='Group',
        within='Time',
        subject='Subject ID',
    )

    anova_stars = anova_summary['p-unc'].apply(_get_sig_stars)
    anova_summary.insert(0,'SIG',anova_stars)

    session_title = f'----{session_name.upper()}----\n'

    with open(log_filepath,'a') as f:
        f.write(session_title)
        
        txt_summary = anova_summary.to_string(header=True, index=False,float_format="{:.3f}".format)
        f.write(txt_summary + '\n\n')

    if pairwise_filepath is not None:
        pairwise = pg.pairwise_tests(
            data=pivoted_df.reset_index(),
            dv='Freezing',
            between='Group',
            within='Time',
            subject='Subject ID'
        )

        pairwise_stars = pairwise['p-unc'].apply(_get_sig_stars)
        pairwise.insert(0,'SIG',pairwise_stars)

        with open(pairwise_filepath,'a') as f:
            f.write(session_title)
            
            txt_summary = pairwise.to_string(header=True, index=False,float_format="{:.3f}".format)
            f.write(txt_summary + '\n\n')

    return


def _pivot_df(
    df,
    dv_name='Freezing',
):
    """
    """
    new_df = df.copy()

    #---- rename BL cols as integers -(n-1) to 0, so pivot works correctly
    bl_cols = [c for c in new_df.columns if 'BL' in str(c)]
    bl_cols.sort()
    num_bl = len(bl_cols)

    if num_bl>0:
        new_bl_cols = [(i+1) - num_bl for i in range(num_bl)] # eg, BL1 ... BL4 become -3 ... 0
        rename_cols = dict(zip(bl_cols, new_bl_cols))
        new_df.rename(columns=rename_cols, inplace=True)

    #---- prepend dv_name for time columns (for pd.wide_to_long)
    new_cols = []
    for col in new_df.columns:
        if col!='Group': # cols contain a measurement of freezing
            new_cols.append(f'{dv_name}_{col}')
        else:
            new_cols.append(col)
    new_df.columns = new_cols

    #---- subject id, index --> column
    new_df['Subject ID'] = new_df.index

    #---- pivot
    new_df = pd.wide_to_long(
        new_df,
        stubnames=['Freezing'], sep='_',
        i=['Subject ID', 'Group'],
        j='Time',
        suffix='[-+]?\d+' # regex to also match negative ints
    )

    return new_df

def create_log_file(
    path,
    cohorts,
    scorer,
    filename="LOG.txt",
    sessions_logged=None,
    project="Extended Extinction",
):
    if cohorts.__class__ is list:
        if len(cohorts)==1:
            cohorts = cohorts[0]
        else:
            cohorts='_'.join(cohorts)

    filename = f"{cohorts}_{scorer}-{filename}"
    
    if not filename.endswith('.txt'):
        filename = f'{filename}.txt'
        
    filename = os.path.join(path, filename)

    if not os.path.exists(filename):
        with open(filename,'a') as f:
            f.write(project.upper() + " ANALYSIS" + "\n")
            f.write(f"Cohorts: {cohorts}\n")
            f.write(f"Scorer: {scorer}\n")
            if sessions_logged is not None:
                f.write(f"Sessions: {sessions_logged}\n" )
            f.write('\n')
    
    return filename

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