def make_bins(df):
    '''
    Make new dataframe of bins, which consist of average of 2 trials

    Notes on baseline trials:
        - Denoted by "BL#" in original dataframe
        - In binned output, BL trials are numbered -(n-1) to 0 rather than being labeled with a string (makes graphing easier); n = number of bl bins
    '''
    import pandas as pd

    group_col = df['Group']
    df2 = df.drop('Group',axis=1)

    df_binned = pd.DataFrame(index=df2.index) # new df with same index

    num_bl_trials = len([s for s in df2.columns if "BL" in str(s).upper()])  # count number of baseline sessions in data
    num_bl_bins = int(num_bl_trials/2)
    num_nonbl_bins = int(df2.shape[1] / 2) - num_bl_bins

    # binning baseline sessions
    for i in range(0, num_bl_bins):
        # names of bl bins in original df
        a = "BL"+str((2*i)+1)
        b = "BL"+str((2*i)+2)
        
        trial = 1-(num_bl_bins-i)  # bl bins are called -(n-1) to 0; n= # bl bins

        df_binned[trial] = df2.loc[:,a:b].mean(axis=1) # add bl bin to new df

    # binning non-BL sessions
    for i in range(0, num_nonbl_bins):
        a = (2*i)+1
        b = (2*i)+2

        trial = i+1

        df_binned[trial] = df2.loc[:,a:b].mean(axis=1)
    
    df_binned['Group'] = group_col

    return df_binned