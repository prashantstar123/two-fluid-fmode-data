"""Published halo rendering recipes, using only released numerical records."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from .models import PLOT_ORDER as EOS_ORDER, FRACTIONS, ALPHA, COLORS, RESONANCE_ORDER as RES_EOS
from .data import open_data
META = {"Creator": "Matplotlib", "CreationDate": None, "ModDate": None}

def groups(rows: list[dict]) -> list[list[dict]]:
    rows = sorted(rows, key=lambda r: r["source_index"])
    answer = []
    for row in rows:
        if not answer or row["source_index"] != answer[-1][-1]["source_index"] + 1:
            answer.append([row])
        else:
            answer[-1].append(row)
    return answer

def axes_style(ax) -> None:
    ax.minorticks_on()
    ax.tick_params(which="major", direction="in", top=True, right=True,
                   length=5.5, width=1.2, labelsize=10)
    ax.tick_params(which="minor", direction="in", top=True, right=True,
                   length=3.0, width=0.8)
    for spine in ax.spines.values():
        spine.set_linewidth(1.2)
    ax.grid(True, color="0.82", linewidth=0.5, alpha=0.8)

def eos_legend(fig, bottom: float, left: float, **spacing) -> None:
    handles = [Line2D([0], [0], color=COLORS[e], lw=1.8, label=e) for e in EOS_ORDER]
    legend = fig.legend(handles=handles, loc="upper center", ncol=5,
                        fontsize=9.1, frameon=True, columnspacing=0.95,
                        handlelength=1.8, handletextpad=0.4,
                        bbox_to_anchor=(0.5, 0.998), borderaxespad=0.15)
    fig.canvas.draw()
    y0 = legend.get_window_extent().transformed(fig.transFigure.inverted()).y0
    fig.subplots_adjust(top=y0 - 0.035, bottom=bottom, left=left,
                        right=0.985, **spacing)

def plot_mass(mr, ref, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.6, 7.1))
    for eos in EOS_ORDER:
        c = COLORS[eos]
        r = sorted((r for r in ref if r["eos"] == eos), key=lambda r: r["M"])
        ax.plot([v["value"] for v in r], [v["M"] for v in r], ":", color=c, lw=1.25)
        for fraction in FRACTIONS:
            rows = [r for r in mr if r["eos"] == eos and r["fraction"] == fraction]
            for segment in groups([r for r in rows if r["halo"] == 1]):
                ax.plot([r["R"] for r in segment], [r["M"] for r in segment],
                        "--", color=c, lw=1.5, alpha=ALPHA[fraction])
            core = [r for r in rows if r["halo"] == 0]
            if core:
                ax.plot([r["R"] for r in core], [r["M"] for r in core],
                        "X", color=c, ms=4.0, mew=0.65,
                        alpha=min(1.0, ALPHA[fraction] + 0.2))
    ax.set(xlim=(6, 98), ylim=(0.5, 2.9))
    ax.set_xlabel(r"$R\ [{\rm km}]$", fontsize=14)
    ax.set_ylabel(r"$M\ [M_\odot]$", fontsize=14)
    axes_style(ax)
    handles = [Line2D([0], [0], color="k", ls="--", label="2F halo"),
               Line2D([0], [0], color="k", marker="X", ls="none", ms=4.5, label="2F core"),
               Line2D([0], [0], color="k", ls=":", label="1F (pure NM)")]
    handles += [Line2D([0], [0], color="0.25", ls="--", lw=2.0, alpha=ALPHA[f],
                       label=rf"$F_{{\rm DM}}={f}\%$") for f in FRACTIONS]
    ax.legend(handles=handles, loc="upper right", fontsize=9, framealpha=0.95)
    eos_legend(fig, bottom=0.10, left=0.105)
    fig.savefig(out / "halo_mass.pdf", bbox_inches="tight", metadata=META)
    plt.close(fig)

def plot_frequency(freq, ref, out: Path) -> int:
    fig, axes = plt.subplots(2, 2, figsize=(8.6, 8.3))
    ylimits = {1: (0.6, 3.02), 5: (0.08, 2.62), 10: (0.05, 2.62), 20: (0.0, 2.62)}
    isolated = 0
    for ax, fraction in zip(axes.ravel(), FRACTIONS):
        for eos in EOS_ORDER:
            c = COLORS[eos]
            r = sorted((r for r in ref if r["eos"] == eos), key=lambda r: r["M"])
            ax.plot([v["M"] for v in r], [v["value"] for v in r], ":", color=c, lw=1.2)
            rows = [r for r in freq if r["eos"] == eos and r["fraction"] == fraction]
            for segment in groups([r for r in rows if r["halo"] == 1]):
                if len(segment) > 1:
                    ax.plot([r["M"] for r in segment], [r["f"] for r in segment],
                            "--", color=c, lw=1.5)
                else:
                    isolated += 1
                    ax.plot(segment[0]["M"], segment[0]["f"], "o", color=c,
                            ms=3.8, markeredgecolor="k", markeredgewidth=0.35, zorder=4)
            core = [r for r in rows if r["halo"] == 0]
            if core:
                ax.plot([r["M"] for r in core], [r["f"] for r in core],
                        "X", color=c, ms=4.0, mew=0.65)
        ax.set(xlim=(0.4, 2.86), ylim=ylimits[fraction])
        ax.set_xlabel(r"$M\ [M_\odot]$", fontsize=12)
        ax.set_ylabel(r"$f\ [{\rm kHz}]$", fontsize=12)
        axes_style(ax)
        label_y, label_va = (0.96, "top") if fraction == 20 else (0.045, "bottom")
        ax.text(0.97, label_y, rf"$F_{{\rm DM}}={fraction}\%$", transform=ax.transAxes,
                ha="right", va=label_va, fontsize=10.5,
                bbox=dict(boxstyle="round,pad=0.23", fc="white", ec="0.5", alpha=0.95))
    axes.ravel()[0].legend(handles=[
        Line2D([0], [0], color="k", ls="--", label="2F halo (DM-led)"),
        Line2D([0], [0], color="k", marker="o", ls="none", ms=3.8, label="Isolated halo point"),
        Line2D([0], [0], color="k", marker="X", ls="none", ms=4.0, label="2F core"),
        Line2D([0], [0], color="k", ls=":", label="1F (pure NM)")],
        loc="upper left", fontsize=8.0, framealpha=0.95)
    eos_legend(fig, bottom=0.07, left=0.08, hspace=0.22, wspace=0.22)
    fig.savefig(out / "halo_frequency.pdf", bbox_inches="tight", metadata=META)
    plt.close(fig)
    return isolated

def plot_access(table, out: Path) -> dict:
    g, msun = 6.67430e-11, 1.98892e30
    selected = [r for r in table if r["eos"] in RES_EOS]
    assert len(selected) == 52
    fig, ax = plt.subplots(figsize=(3.8, 2.9))
    ratios = []
    for r in selected:
        f, radius = r["fDM1p4"] * 1000, r["RDM1p4"] * 1000
        q = 2 * np.pi * f * np.sqrt(radius**3 / (g * 1.4 * msun))
        ratios.append(q)
        x = FRACTIONS.index(r["fraction"]) + (RES_EOS.index(r["eos"]) - 6) * 0.042
        ax.plot(x, q, "o", ms=3.6, color=COLORS[r["eos"]], mec="k", mew=0.25, zorder=3)
    ax.axhline(1, color="k", lw=1.0, ls="--", zorder=2)
    ax.axhspan(0.6, 1.0, color="0.55", alpha=0.13, zorder=1)
    ax.text(-0.42, 1.02, r"$f_\alpha=f_{L1}$", ha="left", va="bottom", fontsize=8)
    ax.set_xlabel(r"$F_{\rm DM}$ [%]", fontsize=10)
    ax.set_ylabel(r"$f_\alpha/f_{L1}=\sqrt{\alpha_h}$", fontsize=10)
    ax.set_xticks([0, 1, 2, 3], ["1", "5", "10", "20"])
    ax.set(xlim=(-0.55, 3.55), ylim=(0.6, 1.85))
    ax.tick_params(direction="in", top=True, right=True, labelsize=8.5)
    ax.grid(alpha=0.25, zorder=0)
    handles = [Line2D([0], [0], marker="o", ls="none", color=COLORS[e], mec="k",
                      mew=0.25, ms=3.5, label=e) for e in RES_EOS]
    ax.legend(handles=handles, loc="center right", fontsize=6.8, ncol=2,
              framealpha=0.95, borderpad=0.4, handletextpad=0.2, columnspacing=0.7)
    fig.tight_layout(pad=0.55)
    fig.savefig(out / "resonance_access.pdf", metadata=META)
    plt.close(fig)
    q = np.asarray(ratios)
    assert np.all(q > 1)
    return {"count": len(q), "min": float(q.min()), "max": float(q.max()),
            "mean": float(q.mean()), "population_sigma": float(q.std()), "passes": 0}

def render(out):
    mr=[];freq=[];ref_mr=[];ref_freq=[];table=[]
    with open_data("halo_sequences.h5") as f:
        for eos in EOS_ORDER:
            g=f[eos]
            for key,target in (("pure_nm_mr",ref_mr),("pure_nm_frequency",ref_freq)):
                h=g[key]
                target.extend(dict(eos=eos,M=float(m),value=float(v)) for m,v in zip(h["M"],h["value"]))
            for p in FRACTIONS:
                h=g[f"F{p}"]
                table.append(dict(eos=eos,fraction=p,RDM1p4=h.attrs["RDM1p4"],fDM1p4=h.attrs["fDM1p4"]))
                for key,target in (("mr",mr),("frequency",freq)):
                    z=h[key]
                    target.extend(dict(eos=eos,fraction=p,**{k:z[k][i].item() for k in z}) for i in range(len(z["M"])))
    with plt.rc_context({"font.family":"DejaVu Sans","mathtext.fontset":"dejavusans",
                         "font.size":10,"pdf.fonttype":42,"axes.unicode_minus":False}):
        plot_mass(mr,ref_mr,out)
        isolated=plot_frequency(freq,ref_freq,out)
        stats=plot_access(table,out)
    return {"mr_points":len(mr),"frequency_points":len(freq),"isolated_points":isolated,"resonance":stats}
