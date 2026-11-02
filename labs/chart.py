"""Shared chart helper for the labs: one consistent, static SVG per lab (result.svg).

Optional: if matplotlib isn't installed the lab still runs and prints its tables.
Style follows STYLE.md (Lab charts): white surface, recessive grid, 2 px lines, at most three series
in the fixed categorical order, a legend for two or more series plus direct labels at the line ends,
text in text colours (never the series colour), and an optional dashed reference line.
Output is deterministic (fixed SVG id salt, no timestamp) so re-running a lab doesn't churn git.
"""
import pathlib

SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]          # blue, orange, aqua: all-pairs safe as a set of three
TEXT, TEXT_2, GRID, AXIS, REF = "#0b0b0b", "#52514e", "#e7e6e2", "#bdbcb6", "#7a7974"


def line_chart(path, x, series, *, title, xlabel, ylabel, logx=False, logy=False,
               ypercent=False, yprefix="", xpercent=False, ref=None, ref_at="left", xticks=None, xticklabels=None, ylim=None, note=None):
    """series: {label: [y values]} in display order (max 3). ref: (y value, label) or None."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.ticker import FuncFormatter
    except ImportError:
        print(f"\n(chart skipped: install matplotlib to write {pathlib.Path(path).name})")
        return
    assert 1 <= len(series) <= 3, "fold extra series into another chart"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ai-system-design-primer",
        "font.family": "sans-serif",
        "font.sans-serif": ["Inter", "Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 10, "axes.edgecolor": AXIS, "axes.labelcolor": TEXT_2,
        "xtick.color": TEXT_2, "ytick.color": TEXT_2, "text.color": TEXT,
    })
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    fig.patch.set_facecolor("white")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.grid(True, axis="y", color=GRID, linewidth=0.75)
    ax.set_axisbelow(True)
    if logx:
        ax.set_xscale("log")
    if logy:
        ax.set_yscale("log")
    many = len(x) > 12
    for (label, ys), colour in zip(series.items(), SERIES):
        ax.plot(x, ys, color=colour, linewidth=1.6, label=label, solid_capstyle="round",
                marker=None if many else "o", markersize=6, markeredgecolor="white", markeredgewidth=1.2)
    if ylim:
        ax.set_ylim(*ylim)
    if ref:
        ax.axhline(ref[0], color=REF, linewidth=1, linestyle=(0, (4, 3)))
        right = ref_at == "right"
        ax.annotate(ref[1], (1 if right else 0, ref[0]), xycoords=("axes fraction", "data"),
                    xytext=(-4 if right else 4, 4), textcoords="offset points", fontsize=9,
                    color=TEXT_2, ha="right" if right else "left")
    ax.yaxis.set_major_formatter(FuncFormatter(
        (lambda v, _: f"{v:.0%}") if ypercent else (lambda v, _: f"{yprefix}{v:,.10g}")))
    ax.xaxis.set_major_formatter(FuncFormatter(
        (lambda v, _: f"{v:.0%}") if xpercent else (lambda v, _: f"{v:,.10g}")))
    if xticks is not None:
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels or [f"{t:,.10g}" for t in xticks])
        ax.minorticks_off()
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold", color=TEXT, pad=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if len(series) > 1:
        ax.legend(frameon=False, loc="best", fontsize=9, labelcolor=TEXT_2)
    if note:
        fig.text(0.01, 0.01, note, fontsize=8, color=TEXT_2)
    fig.tight_layout(rect=(0, 0.04 if note else 0, 0.84 if len(series) > 1 else 1, 1))
    if len(series) > 1:                           # direct labels at line ends, spread so none overlap
        to_px = ax.transData.transform
        ends = sorted(((to_px((x[-1], ys[-1]))[1], label, ys[-1]) for label, ys in series.items()))
        placed, gap = [], 13.0                    # pixels between label centres
        for py, label, yv in ends:
            target = max(py, placed[-1] + gap) if placed else py
            placed.append(target)
            ax.annotate(label, (x[-1], yv), xytext=(6, (target - py) * 72 / fig.dpi),
                        textcoords="offset points", va="center", fontsize=9, color=TEXT_2,
                        annotation_clip=False)
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)
    print(f"\nChart written to {pathlib.Path(path).name}")
