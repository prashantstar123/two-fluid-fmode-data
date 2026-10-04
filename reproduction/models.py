"""Model ordering, fractions, and published curve colours."""

PLOT_ORDER = (
    "DD2_ND", "DD2_NY", "DD2_NYD", "DD2Y", "DDHdY4",
    "RMF_m55_L50_NY", "RMF_m55_L60_NY", "RMF_m60_L50_NY",
    "RMF_m60_L60_NY", "RMF_m70_L40_N", "RMF_m70_L50_N",
    "RMF_m75_L40_N", "RMF_m75_L50_N",
    "GM1Y5", "CMF-crust", "SLy4", "EOS1", "EOS2", "EOS6", "EOS11", "EOS20",
)
TABLE_ORDER = (
    "EOS1", "EOS2", "EOS6", "EOS11", "EOS20", "DD2Y", "DDHdY4",
    "GM1Y5", "CMF-crust", "SLy4", "DD2_ND", "DD2_NY", "DD2_NYD",
    "RMF_m55_L50_NY", "RMF_m55_L60_NY", "RMF_m60_L50_NY",
    "RMF_m60_L60_NY", "RMF_m70_L40_N", "RMF_m70_L50_N",
    "RMF_m75_L40_N", "RMF_m75_L50_N",
)
RESONANCE_ORDER = (
    "DD2_ND", "DD2_NY", "DD2_NYD", "DD2Y", "DDHdY4", "GM1Y5",
    "CMF-crust", "SLy4", "EOS1", "EOS2", "EOS6", "EOS11", "EOS20",
)
FRACTIONS = (1, 5, 10, 20)
ALPHA = {1: 1.0, 5: 0.72, 10: 0.55, 20: 0.42}
COLORS = dict(zip(PLOT_ORDER, (
    "#1f77b4", "#4fa8e8", "#aec7e8", "#08519c", "#6baed6",
    "#d62728", "#ff9896", "#e6550d", "#fdae6b", "#8c2d04",
    "#a63603", "#e6810e", "#fd8d3c",
    "#2ca02c", "#98df8a", "#17becf", "#9467bd", "#c5b0d5",
    "#8c564b", "#e377c2", "#7f7f7f",
)))

FIGURE_NAMES = {
    1: "core_MR", 2: "core_freq", 3: "core_tau",
    4: "halo_mass", 5: "halo_frequency", 6: "resonance_access",
    7: "fig01_core_eigenfunctions", 8: "fig02_core_edge",
    9: "MR_lam", 10: "freq_mass_lam", 11: "tau_mass_lam",
    12: "higher_l_modes",
}
