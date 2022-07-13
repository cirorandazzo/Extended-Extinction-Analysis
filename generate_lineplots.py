import os
import datetime

from lineplot_bin_means import *

data_folder = "./data"
project = "Extended Extinction"
group = "ee1"  #TODO implement all
# sessions = "all" #TODO implement
scorer = "mel"  #TODO implement all

fig_folder = "./figures"
save_figs = True

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
    "6sr1"   : "SR1",
    "7sr2"   : "SR2",
    "8ren"   : "Renewal",
    "9rst"   : "Reinstatement"
}

left_sessions = ["1afc","5ret"]
legend_sessions = ["4ext2"]

# MAKE NEW SUBFOLDER
now=datetime.datetime.now()
now=now.strftime("%Y-%m-%d")

text_file="log.txt"
i=0
while save_figs:
    try:
        fig_subfolder = os.path.join(fig_folder, now, str(i))
        os.makedirs(fig_subfolder)

        text_file = os.path.join(fig_subfolder, text_file)
        with open(text_file,'a') as f:
            f.write(project.upper() + " ANALYSIS" + "\n")
            f.write("Group: " + group + "\n")
            f.write("Scorer: " + scorer + "\n\n")

        break
    except FileExistsError:
        i+=1


figs = []
axes = []

for s in session_names:
    data_file = group + "-" + s + "-" + scorer + ".csv"
    session_data_file = os.path.join(data_folder, group, data_file)
    session = session_names.get(s)

    df = pd.read_csv(session_data_file)
    df.set_index("RAT",inplace=True)

    df = 100 * df / time_per_trial  # change into percents

    legend = s in legend_sessions
    ylbl = "% Freezing" if s in left_sessions else None

    fig, ax, p_vals = lineplot_bin_means(
        df=df,
        group_assignments=groups,
        group_labels=group_labels,
        group_colors=group_colors,
        session_name=session,
        legend=legend,
        ylbl=ylbl,
        size=("scale",6),
        title_size=18,
        font_size=14,
    )

    figs.append(fig)
    axes.append(ax)

    if save_figs:
        fig_file = os.path.join(fig_subfolder, s)
        plt.savefig(
            fig_file+".png",
            bbox_inches="tight",
        )
        with open(text_file,'a') as f:
            f.write("---" + session + "---\n")
            for i in range(0,len(p_vals)):
                p = np.around(p_vals[i],5)
                if p<=0.05:
                    f.write("*")
                f.write(str(i+1) + ": " + str(p) + "\n")
            f.write("\n")



# if save_figs:
#     fig_file = os.path.join(fig_subfolder, s)
#     plt.savefig(fig_file+".png")
#     with open(text_file,'a') as f:
#         f.write(session + "\n")