# Group Info
ee1_vns = [2,3,6,7,9,11]
ee1_sham = [1,4,5,8,10]
ee1_exclude = []

ee2_vns = [1,3,6,8,9,11,12]
ee2_sham = [2,4,5,7,10]
ee2_exclude = [6]

eet_vns = []
eet_sham = [1,2,4,5,6,7]
eet_exclude = [3]

# combined group data includes cohort in animal ID. it aint pretty, but itll (probably) work
ee1_2_vns = ["EE1A2","EE1A3","EE1A6","EE1A7","EE1A9","EE1A11",
             "EE2A1","EE2A3","EE2A6","EE2A8","EE2A9","EE2A11","EE2A12"]
ee1_2_sham = ["EE1A1","EE1A4","EE1A5","EE1A8","EE1A10",
              "EE2A2","EE2A4","EE2A5","EE2A7","EE2A10"]

groups = {
    "EE1": {
        "VNS": ee1_vns,
        "SHAM": ee1_sham
    },
    "EE2": {
        "VNS": ee2_vns,
        "SHAM": ee2_sham
    },
    "EE1_2": {
        "VNS": ee1_2_vns,
        "SHAM": ee1_2_sham
    },
    "EET": { # no vns
        "CTRL": eet_sham
    }
}