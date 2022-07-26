group_colors = ["red", "blue"]
group_labels = ["VNS", "SHAM"]

title_size = 18
font_size = 16


session_names = { 
    "1afc"   : "(a) Fear condititioning",
    "2cfrt"  : "(b) Fear recall",
    "3ext1"  : "(c) Extinction Day 1",
    "4ext2"  : "(d) Extinction Day 2",
    "5ret"   : "(e) Retention",
    "6sr1"   : "(f) Short-Term SR",
    "7sr2"   : "(g) Long-Term SR",
    "8ren"   : "(h) Renewal",
    "9rst"   : "(i) Rst. Test"
}

ctx_a = (0.9058,0.9019,0.9019)
ctx_b = (0.9843,0.9019,0.6392)
ctx_c = (0.7921,0.8745,0.7215)
ctx_rst = (0.5333,0.1294,0.0666)

graph_backgrounds = {
    "1afc"   : ctx_a,
    "2cfrt"  : ctx_b,
    "3ext1"  : ctx_b,
    "4ext2"  : ctx_b,
    "5ret"   : ctx_b,
    "6sr1"   : ctx_b,
    "7sr2"   : ctx_b,
    "8ren"   : ctx_c,
    "9rst"   : ctx_b,
}

session_subtitles = {
    "5ret"   : "1d. post-extinction",
    "6sr1"   : "15d. post-extinction",
    "7sr2"   : "43d. post-extinction",
    "8ren"   : "48d. post-extinction",
    "9rst"   : "50d. post-extinction",
}

time_per_trial = 30  # seconds per trial
