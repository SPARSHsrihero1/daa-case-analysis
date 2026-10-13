"""
DAA Assignment — Best, Worst and Average Case Analysis
Interactive Animation: Linear Search + Insertion Sort
Student: Sparsh Srivastava | Roll: 590022251 | B17 | Sem 4 | Sec I

Run: python animation.py
Controls:
  - Next / Prev buttons to step through algorithm
  - Case buttons (Best / Avg / Worst) to switch input scenario
  - Algorithm buttons (Linear Search / Insertion Sort) to switch algorithm
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button, RadioButtons
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
#  COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
COL_DEFAULT  = "#4682B4"   # steelblue  — untouched element
COL_COMPARE  = "#FFA500"   # orange     — currently being examined
COL_SORTED   = "#2E8B57"   # seagreen   — confirmed sorted / found
COL_KEY      = "#CC2200"   # crimson    — target key / pivot
COL_SHIFT    = "#9370DB"   # medium purple — element being shifted

# ─────────────────────────────────────────────────────────────────────────────
#  STATE DATACLASS  (plain dict for clarity)
#  keys: array, highlights {idx: colour}, label, comparisons, swaps, done
# ─────────────────────────────────────────────────────────────────────────────

def make_state(array, highlights, label, comparisons, swaps, done=False):
    return dict(
        array=list(array),
        highlights=dict(highlights),
        label=label,
        comparisons=comparisons,
        swaps=swaps,
        done=done,
    )

# ─────────────────────────────────────────────────────────────────────────────
#  LINEAR SEARCH  —  generate all steps
# ─────────────────────────────────────────────────────────────────────────────
def generate_linear_search_steps(array, key):
    steps = []
    n = len(array)
    cmp = 0
    steps.append(make_state(
        array, {},
        f"Initial array. Searching for key = {key}",
        0, 0
    ))
    for i in range(n):
        cmp += 1
        if array[i] == key:
            steps.append(make_state(
                array, {i: COL_KEY},
                f"Step {cmp}: Comparing A[{i}] = {array[i]} with key = {key}  →  MATCH FOUND!",
                cmp, 0, done=True
            ))
            # colour all confirmed sorted positions
            hl = {j: COL_SORTED for j in range(i + 1)}
            hl[i] = COL_KEY
            steps.append(make_state(
                array, hl,
                f"✅ Key {key} found at index {i}.  Total comparisons = {cmp}",
                cmp, 0, done=True
            ))
            return steps
        else:
            steps.append(make_state(
                array, {i: COL_COMPARE},
                f"Step {cmp}: Comparing A[{i}] = {array[i]} with key = {key}  →  No match, continue",
                cmp, 0
            ))
    steps.append(make_state(
        array, {},
        f"❌ Key {key} NOT found in array.  Total comparisons = {cmp}  →  O(n)",
        cmp, 0, done=True
    ))
    return steps

# ─────────────────────────────────────────────────────────────────────────────
#  INSERTION SORT  —  generate all steps
# ─────────────────────────────────────────────────────────────────────────────
def generate_insertion_sort_steps(array):
    steps = []
    A = list(array)
    n = len(A)
    cmp = 0
    swaps = 0

    steps.append(make_state(
        A, {},
        "Initial unsorted array. Insertion Sort will begin.",
        0, 0
    ))

    for j in range(1, n):
        key_val = A[j]
        steps.append(make_state(
            A, {j: COL_KEY},
            f"Pass j={j}: Pick key = A[{j}] = {key_val}  (sorted prefix: A[0..{j-1}])",
            cmp, swaps
        ))
        i = j - 1
        while i >= 0 and A[i] > key_val:
            cmp += 1
            swaps += 1
            A[i + 1] = A[i]
            hl = {k: COL_SORTED for k in range(i)}
            hl[i] = COL_SHIFT
            hl[i + 1] = COL_COMPARE
            steps.append(make_state(
                A, hl,
                f"  A[{i}]={A[i+1]} > key={key_val}: shift A[{i}] → A[{i+1}]  "
                f"(comparisons={cmp}, shifts={swaps})",
                cmp, swaps
            ))
            i -= 1
        # final comparison (loop exit)
        if i >= 0:
            cmp += 1
            steps.append(make_state(
                A, {i: COL_SORTED},
                f"  A[{i}]={A[i]} ≤ key={key_val}: stop shifting  (comparisons={cmp})",
                cmp, swaps
            ))
        A[i + 1] = key_val
        hl_insert = {k: COL_SORTED for k in range(j + 1)}
        hl_insert[i + 1] = COL_KEY
        steps.append(make_state(
            A, hl_insert,
            f"  Insert key={key_val} at position {i+1}.  Sorted prefix: A[0..{j}]",
            cmp, swaps
        ))

    hl_done = {k: COL_SORTED for k in range(n)}
    steps.append(make_state(
        A, hl_done,
        f"✅ Array fully sorted: {A}  |  Total comparisons={cmp}, shifts={swaps}",
        cmp, swaps, done=True
    ))
    return steps

# ─────────────────────────────────────────────────────────────────────────────
#  SCENARIO DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────
SCENARIOS = {
    "Linear Search": {
        "Best":  {"array": [3, 7, 1, 9, 4], "key": 3,
                  "desc": "Best Case — Key at index 0 → O(1)"},
        "Avg":   {"array": [3, 7, 1, 9, 4], "key": 9,
                  "desc": "Average Case — Key at middle → O(n)"},
        "Worst": {"array": [3, 7, 1, 9, 4], "key": 5,
                  "desc": "Worst Case — Key absent → O(n)"},
    },
    "Insertion Sort": {
        "Best":  {"array": [1, 2, 3, 4, 5],
                  "desc": "Best Case — Already sorted → O(n)"},
        "Avg":   {"array": [3, 1, 4, 5, 2],
                  "desc": "Average Case — Random order → O(n²)"},
        "Worst": {"array": [5, 4, 3, 2, 1],
                  "desc": "Worst Case — Reverse sorted → O(n²)"},
    },
}

COMPLEXITY_INFO = {
    "Linear Search":  {"Best": "O(1)", "Avg": "O(n)",  "Worst": "O(n)"},
    "Insertion Sort": {"Best": "O(n)", "Avg": "O(n²)", "Worst": "O(n²)"},
}

# ─────────────────────────────────────────────────────────────────────────────
#  ANIMATION CLASS
# ─────────────────────────────────────────────────────────────────────────────
class AlgorithmAnimation:
    def __init__(self):
        self.algorithm = "Linear Search"
        self.case = "Best"
        self.steps = []
        self.step_idx = 0

        # ── Build figure layout ──────────────────────────────────────────────
        self.fig = plt.figure(figsize=(14, 8))
        self.fig.patch.set_facecolor("#1e1e2e")

        # Main array axis
        self.ax_main = self.fig.add_axes([0.05, 0.30, 0.62, 0.50])
        self.ax_main.set_facecolor("#1e1e2e")

        # Info panel (right)
        self.ax_info = self.fig.add_axes([0.70, 0.30, 0.28, 0.50])
        self.ax_info.set_facecolor("#2a2a3e")
        self.ax_info.axis("off")

        # Title axis
        self.ax_title = self.fig.add_axes([0.05, 0.82, 0.90, 0.12])
        self.ax_title.set_facecolor("#1e1e2e")
        self.ax_title.axis("off")

        # Label axis (step label at bottom of array)
        self.ax_label = self.fig.add_axes([0.05, 0.20, 0.62, 0.09])
        self.ax_label.set_facecolor("#1e1e2e")
        self.ax_label.axis("off")

        # ── Widgets ───────────────────────────────────────────────────────────
        ax_prev  = self.fig.add_axes([0.05, 0.08, 0.12, 0.07])
        ax_next  = self.fig.add_axes([0.20, 0.08, 0.12, 0.07])
        ax_reset = self.fig.add_axes([0.35, 0.08, 0.12, 0.07])

        self.btn_prev  = Button(ax_prev,  "◀ Prev",  color="#3a3a5e", hovercolor="#5a5a8e")
        self.btn_next  = Button(ax_next,  "Next ▶",  color="#3a3a5e", hovercolor="#5a5a8e")
        self.btn_reset = Button(ax_reset, "⟳ Reset", color="#3a3a5e", hovercolor="#5a5a8e")

        for btn in [self.btn_prev, self.btn_next, self.btn_reset]:
            btn.label.set_color("white")
            btn.label.set_fontsize(11)

        # Case radio
        ax_case = self.fig.add_axes([0.52, 0.01, 0.18, 0.15])
        ax_case.set_facecolor("#2a2a3e")
        self.radio_case = RadioButtons(ax_case, ("Best", "Avg", "Worst"),
                                       active=0, activecolor=COL_SORTED)
        for lbl in self.radio_case.labels:
            lbl.set_color("white"); lbl.set_fontsize(10)

        # Algorithm radio
        ax_algo = self.fig.add_axes([0.72, 0.01, 0.26, 0.15])
        ax_algo.set_facecolor("#2a2a3e")
        self.radio_algo = RadioButtons(ax_algo, ("Linear Search", "Insertion Sort"),
                                       active=0, activecolor=COL_SORTED)
        for lbl in self.radio_algo.labels:
            lbl.set_color("white"); lbl.set_fontsize(10)

        # ── Event connections ─────────────────────────────────────────────────
        self.btn_next.on_clicked(self._next)
        self.btn_prev.on_clicked(self._prev)
        self.btn_reset.on_clicked(self._reset)
        self.radio_case.on_clicked(self._on_case_change)
        self.radio_algo.on_clicked(self._on_algo_change)

        # ── Initial load ──────────────────────────────────────────────────────
        self._load_scenario()
        self._render()

    # ── Scenario loading ─────────────────────────────────────────────────────
    def _load_scenario(self):
        sc = SCENARIOS[self.algorithm][self.case]
        if self.algorithm == "Linear Search":
            self.steps = generate_linear_search_steps(sc["array"], sc["key"])
        else:
            self.steps = generate_insertion_sort_steps(sc["array"])
        self.step_idx = 0

    # ── Button callbacks ─────────────────────────────────────────────────────
    def _next(self, event):
        if self.step_idx < len(self.steps) - 1:
            self.step_idx += 1
        self._render()

    def _prev(self, event):
        if self.step_idx > 0:
            self.step_idx -= 1
        self._render()

    def _reset(self, event):
        self.step_idx = 0
        self._render()

    def _on_case_change(self, label):
        self.case = label
        self._load_scenario()
        self._render()

    def _on_algo_change(self, label):
        self.algorithm = label
        self.case = "Best"
        # sync radio_case back to Best (index 0)
        self.radio_case.set_active(0)
        self._load_scenario()
        self._render()

    # ── Main render ──────────────────────────────────────────────────────────
    def _render(self):
        state = self.steps[self.step_idx]
        arr = state["array"]
        hl  = state["highlights"]
        n   = len(arr)

        # ── Clear axes ───────────────────────────────────────────────────────
        self.ax_main.cla()
        self.ax_info.cla()
        self.ax_title.cla()
        self.ax_label.cla()

        for ax in [self.ax_main, self.ax_info, self.ax_title, self.ax_label]:
            ax.set_facecolor("#1e1e2e")
            ax.axis("off")
        self.ax_info.set_facecolor("#2a2a3e")

        # ── Title ────────────────────────────────────────────────────────────
        sc_desc = SCENARIOS[self.algorithm][self.case]["desc"]
        title_str = (f"{self.algorithm}  |  {sc_desc}"
                     f"  |  Step {self.step_idx + 1} / {len(self.steps)}")
        self.ax_title.text(0.5, 0.5, title_str,
                           ha="center", va="center",
                           fontsize=12, fontweight="bold", color="white",
                           transform=self.ax_title.transAxes)

        # ── Array bars ───────────────────────────────────────────────────────
        bar_w = 0.7
        max_val = max(arr) if arr else 1
        for i, val in enumerate(arr):
            colour = hl.get(i, COL_DEFAULT)
            bar_h = val / max_val * 0.85
            rect = mpatches.FancyBboxPatch(
                (i - bar_w / 2, 0), bar_w, bar_h,
                boxstyle="round,pad=0.04",
                facecolor=colour, edgecolor="white", linewidth=1.2
            )
            self.ax_main.add_patch(rect)
            # value label above bar
            self.ax_main.text(i, bar_h + 0.03, str(val),
                              ha="center", va="bottom",
                              fontsize=13, fontweight="bold", color="white")
            # index label below bar
            self.ax_main.text(i, -0.07, f"[{i}]",
                              ha="center", va="top",
                              fontsize=9, color="#aaaaaa")

        self.ax_main.set_xlim(-0.8, n - 0.2)
        self.ax_main.set_ylim(-0.12, 1.10)

        # ── Step label ───────────────────────────────────────────────────────
        self.ax_label.text(0.5, 0.5, state["label"],
                           ha="center", va="center",
                           fontsize=10, color="#e0e0ff",
                           wrap=True, transform=self.ax_label.transAxes)

        # ── Info panel ───────────────────────────────────────────────────────
        cinfo = COMPLEXITY_INFO[self.algorithm]
        self.ax_info.axis("off")

        info_lines = [
            ("Algorithm", self.algorithm),
            ("Case", self.case),
            ("", ""),
            ("─── Complexity ───", ""),
            ("Best Case",  cinfo["Best"]),
            ("Avg Case",   cinfo["Avg"]),
            ("Worst Case", cinfo["Worst"]),
            ("", ""),
            ("─── Current Step ───", ""),
            ("Comparisons", str(state["comparisons"])),
            ("Shifts/Swaps", str(state["swaps"])),
        ]

        y = 0.95
        for key, val in info_lines:
            if key.startswith("─"):
                self.ax_info.text(0.5, y, key, ha="center", va="top",
                                  fontsize=9, color="#88aaff",
                                  transform=self.ax_info.transAxes)
            elif key == "":
                pass
            else:
                self.ax_info.text(0.05, y, f"{key}:", ha="left", va="top",
                                  fontsize=9, color="#cccccc",
                                  transform=self.ax_info.transAxes)
                col = "white"
                if val in ("O(1)", "O(n)", "O(n log n)"):
                    col = "#90ee90"
                elif val in ("O(n²)",):
                    col = "#ff9999"
                self.ax_info.text(0.95, y, val, ha="right", va="top",
                                  fontsize=9, fontweight="bold", color=col,
                                  transform=self.ax_info.transAxes)
            y -= 0.09

        # Done badge
        if state["done"]:
            self.ax_info.text(0.5, 0.08, "✅ COMPLETE",
                              ha="center", va="center",
                              fontsize=11, fontweight="bold", color=COL_SORTED,
                              transform=self.ax_info.transAxes,
                              bbox=dict(boxstyle="round,pad=0.3",
                                        facecolor="#003300", edgecolor=COL_SORTED))

        # ── Legend ───────────────────────────────────────────────────────────
        legend_patches = [
            mpatches.Patch(color=COL_DEFAULT, label="Unvisited"),
            mpatches.Patch(color=COL_COMPARE, label="Comparing"),
            mpatches.Patch(color=COL_SHIFT,   label="Shifting"),
            mpatches.Patch(color=COL_SORTED,  label="Sorted/Found"),
            mpatches.Patch(color=COL_KEY,     label="Key/Pivot"),
        ]
        self.ax_main.legend(handles=legend_patches,
                            loc="upper right", fontsize=8,
                            facecolor="#2a2a3e", edgecolor="gray",
                            labelcolor="white")

        self.fig.canvas.draw_idle()

    # ── Show ─────────────────────────────────────────────────────────────────
    def show(self):
        plt.show()


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    anim = AlgorithmAnimation()
    anim.show()
