group_colors = ["red", "blue"]
group_labels = ["VNS", "SHAM"]

title_size = 18
font_size = 16


session_names = { 
    "1-AFC"   : "(a) Fear condititioning",
    "2-CFRT"  : "(b) Fear recall",
    "3-EXT1"  : "(c) Extinction Day 1",
    "4-EXT2"  : "(d) Extinction Day 2",
    "5-RET"   : "(e) Retention",
    "6-SR1"   : "(f) Short-Term SR",
    "7-SR2"   : "(g) Long-Term SR",
    "8-REN"   : "(h) Renewal",
    "9-RST"   : "(i) Rst. Test"
}

ctx_a = (0.9058,0.9019,0.9019)
ctx_b = (0.9843,0.9019,0.6392)
ctx_c = (0.7921,0.8745,0.7215)
ctx_rst = (0.5333,0.1294,0.0666)

graph_backgrounds = {
    "1-AFC"   : ctx_a,
    "2-CFRT"  : ctx_b,
    "3-EXT1"  : ctx_b,
    "4-EXT2"  : ctx_b,
    "5-RET"   : ctx_b,
    "6-SR1"   : ctx_b,
    "7-SR2"   : ctx_b,
    "8-REN"   : ctx_c,
    "9-RST"   : ctx_b,
}

session_subtitles = {
    "5-RET"   : "1d. post-extinction",
    "6-SR1"   : "15d. post-extinction",
    "7-SR2"   : "43d. post-extinction",
    "8-REN"   : "48d. post-extinction",
    "9-RST"   : "50d. post-extinction",
}

time_per_trial = 30  # seconds per trial
