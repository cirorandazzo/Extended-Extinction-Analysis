group_colors = ["red", "blue"]
group_labels = ["VNS", "SHAM"]

title_size = 18
font_size = 16


session_names = { 
    "1-afc"   : "(a) Fear condititioning",
    "2-cfrt"  : "(b) Fear recall",
    "3-ext1"  : "(c) Extinction Day 1",
    "4-ext2"  : "(d) Extinction Day 2",
    "5-ret"   : "(e) Retention",
    "6-sr1"   : "(f) Short-Term SR",
    "7-sr2"   : "(g) Long-Term SR",
    "8-ren"   : "(h) Renewal",
    "9-rst"   : "(i) Rst. Test"
}

ctx_a = (0.9058,0.9019,0.9019)
ctx_b = (0.9843,0.9019,0.6392)
ctx_c = (0.7921,0.8745,0.7215)
ctx_rst = (0.5333,0.1294,0.0666)

graph_backgrounds = {
    "1-afc"   : ctx_a,
    "2-cfrt"  : ctx_b,
    "3-ext1"  : ctx_b,
    "4-ext2"  : ctx_b,
    "5-ret"   : ctx_b,
    "6-sr1"   : ctx_b,
    "7-sr2"   : ctx_b,
    "8-ren"   : ctx_c,
    "9-rst"   : ctx_b,
}

session_subtitles = {
    "5-ret"   : "1d. post-extinction",
    "6-sr1"   : "15d. post-extinction",
    "7-sr2"   : "43d. post-extinction",
    "8-ren"   : "48d. post-extinction",
    "9-rst"   : "50d. post-extinction",
}

time_per_trial = 30  # seconds per trial
