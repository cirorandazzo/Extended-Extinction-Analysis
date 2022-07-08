import os
import datetime

from lineplot_bin_means import *

data_folder = "./data"
group = "ee1"  #TODO implement all
# sessions = "all" #TODO implement
scorer = "mel"  #TODO implement all

fig_folder = "./figures"

group_colors = ["red", "blue"]
group_labels = ["VNS", "SHAM"]

time_per_trial = 30  # seconds per trial

ee1_vns = [2,3,6,7,9,11]
ee1_sham = [1,4,5,8,10]
ee1_exclude = []

# TODO make one vns/sham group variable
groups = [ee1_vns, ee1_sham]

# ee2_vns = [1,3,6,8,9]
# ee2_sham = [2,4,5,7,10]
# ee2_exclude = [6] # cuff problems


session_names = { 
    "1afc"   : "Fear condititioning",
    "2cfrt"  : "Fear recall",
    "3ext1"  : "Extinction Day 1",
    "4ext2"  : "Extinction Day 2",
    "5ret"   : "Retention",
    "6sr1"   : "SR",
    "7sr2"   : "SR",
    "8ren"   : "Renewal",
    "9rst"   : "Reinstatement"
}

# MAKE NEW SUBFOLDER
now=datetime.datetime.now()
now=now.strftime("%Y-%m-%d")
i=0
while True:
    try:
        fig_subfolder = os.path.join(fig_folder, now, str(i))
        os.makedirs(fig_subfolder)
        break
    except FileExistsError:
        i+=1

print(fig_subfolder)

for s in session_names:
    data_file = group + "-" + s + "-" + scorer + ".csv"
    session_data_file = os.path.join(data_folder, group, data_file)

    df = pd.read_csv(session_data_file)
    df.set_index("RAT",inplace=True)

    df = 100 * df / time_per_trial  # change into percents

    fig, ax = lineplot_bin_means(
        df=df,
        group_assignments=groups,
        group_labels=group_labels,
        group_colors=group_colors,
        session_name=session_names.get(s),
        legend=False,
    )

    fig_file = os.path.join(fig_subfolder, s+".png")
    plt.savefig(fig_file)