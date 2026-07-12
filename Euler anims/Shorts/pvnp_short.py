# pvnp_short.py — "$1,000,000 ... for whoever does." — 28.1 s
from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GLD = "#FFFF00"; GRN = "#83C167"; DIM = "#2A2A3A"; AMB = "#FF9408"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)

def cap(s, sz=32, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).to_edge(UP, buff=0.5)


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


# ── reusable visual builders ─────────────────────────────────────────────────

def make_grid(n=6, size=4.2):
    """n x n grid of cells with 2x3 thick box dividers (sudoku-style)."""
    cell = size / n
    lines = VGroup()
    for i in range(n + 1):
        w = 3.5 if i % 3 == 0 else 1.2
        lines.add(Line([-size/2, -size/2 + i*cell, 0], [size/2, -size/2 + i*cell, 0],
                       color=GRY, stroke_width=w))
        lines.add(Line([-size/2 + i*cell, -size/2, 0], [-size/2 + i*cell, size/2, 0],
                       color=GRY, stroke_width=w))
    return lines, cell


def grid_cell_pos(row, col, n=6, size=4.2):
    cell = size / n
    x = -size/2 + cell * (col + 0.5)
    y = size/2 - cell * (row + 0.5)
    return np.array([x, y, 0])


class PvNP(S):
    ONSETS = [
        0.03,   #  0  "So — solve this sudoku. It takes real effort."
        2.76,   #  1  "Now — I hand you a finished one."
        4.88,   #  2  "Checking if it's correct?"
        6.88,   #  3  "Seconds."
        8.26,   #  4  "That gap — hard to solve, easy to check — is called P vs NP."
        12.73,  #  5  "Every password on Earth is protected by that gap being permanent."
        15.82,  #  6  "If someone proves the gap doesn't actually exist —"
        18.20,  #  7  "that solving is always secretly as fast as checking —"
        20.78,  #  8  "every encryption system on the planet will break."
        23.59,  #  9  "Nobody has ever proven it."
        25.45,  # 10  "$1,000,000 is sitting on the table for whoever does."
    ]

    def construct(self):
        self.setup()

        # ── 0 · "Solve this sudoku. It takes real effort." ──────────────────
        c0 = cap("Solve this.", sz=38, c=WHT)
        grid_lines, cell = make_grid()
        grid_lines.move_to(DOWN * 0.4)

        # a partial set of filled digits + empty cells, filled in one-by-one
        # to visually represent "effort" — LaggedStart is slow and deliberate
        filled_positions = [(0,1,"5"), (0,4,"2"), (1,0,"6"), (1,3,"9"), (2,2,"1"),
                            (2,5,"4"), (3,0,"3"), (3,3,"8"), (4,1,"7"), (4,4,"5"),
                            (5,2,"2"), (5,5,"9")]
        digits = VGroup()
        for r, cidx, val in filled_positions:
            pos = grid_cell_pos(r, cidx) + grid_lines.get_center()
            digits.add(T(val, sz=28, c=WHT).move_to(pos))

        self.cue(0)
        self.P(FadeIn(c0), rt=0.35)
        self.P(Create(grid_lines), rt=0.5)
        # slow, deliberate, one at a time — this IS the "effort"
        self.P(LaggedStart(*[FadeIn(d, scale=1.2) for d in digits], lag_ratio=0.35), rt=1.7)

        effort_lbl = T("Real effort.", sz=30, c=RED, weight=BOLD).next_to(grid_lines, DOWN, buff=0.4)
        self.P(FadeIn(effort_lbl), rt=0.3)

        # ── 1 · "Now — I hand you a finished one." ───────────────────────────
        self.cue(1)
        self.P(FadeOut(VGroup(c0, effort_lbl)), rt=0.3)
        c1 = cap("Now, a finished one.", sz=36, c=WHT)

        # remaining cells fill in ALL AT ONCE — contrast with the slow fill above
        remaining = [(r, c2) for r in range(6) for c2 in range(6)
                    if (r, c2) not in [(a,b) for a,b,_ in filled_positions]]
        fill_vals = ["4","8","1","6","3","9","2","5","7","1","4","8",
                    "6","2","9","5","3","7","4","1","6","2","8","3"]
        more_digits = VGroup()
        for (r, cidx), val in zip(remaining, fill_vals):
            pos = grid_cell_pos(r, cidx) + grid_lines.get_center()
            more_digits.add(T(val, sz=28, c=GRN).move_to(pos))

        self.P(FadeIn(c1), rt=0.35)
        self.P(FadeIn(more_digits), rt=0.5)  # all at once — instant completion

        # ── 2 · "Checking if it's correct?" ───────────────────────────────────
        self.cue(2)
        self.P(FadeOut(c1), rt=0.25)
        c2 = cap("Checking it's correct?", sz=34, c=WHT)
        self.P(FadeIn(c2), rt=0.4)

        # ── 3 · "Seconds." — fast green scan-line sweeps the grid ────────────
        self.cue(3)
        self.P(FadeOut(c2), rt=0.2)
        c3 = T("SECONDS.", sz=52, c=GRN, weight=BOLD).to_edge(UP, buff=0.5)

        scan = Rectangle(width=4.3, height=0.15, fill_color=GRN, fill_opacity=0.7,
                         stroke_width=0).move_to(grid_lines.get_top())
        self.P(FadeIn(c3), rt=0.3)
        self.P(scan.animate.move_to(grid_lines.get_bottom()), rt=0.55, rate_func=linear)
        check = T("✓", sz=80, c=GRN, weight=BOLD).move_to(grid_lines.get_center())
        self.P(FadeOut(scan), Write(check), rt=0.35)

        # ── 4 · "That gap ... is called P vs NP." ────────────────────────────
        self.cue(4)
        self.P(FadeOut(VGroup(c3, grid_lines, digits, more_digits, check)), rt=0.4)

        hard_lbl = T("HARD to solve", sz=38, c=RED, weight=BOLD).move_to(UP * 1.6)
        easy_lbl = T("EASY to check", sz=38, c=GRN, weight=BOLD).next_to(hard_lbl, DOWN, buff=0.5)
        gap_arrow = DoubleArrow(hard_lbl.get_bottom() + DOWN*0.05,
                               easy_lbl.get_top() + UP*0.05,
                               color=GLD, stroke_width=3, buff=0.05)
        gap_lbl = T("THE GAP", sz=24, c=GLD).next_to(gap_arrow, RIGHT, buff=0.3)

        self.P(FadeIn(hard_lbl, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(easy_lbl, shift=DOWN*0.15), rt=0.4)
        self.P(GrowArrow(gap_arrow), FadeIn(gap_lbl), rt=0.45)

        pvnp = T("P  vs  NP", sz=56, c=WHT, weight=BOLD).next_to(easy_lbl, DOWN, buff=0.7)
        self.P(Write(pvnp), rt=0.6)

        # ── 5 · "Every password on Earth ... permanent." ─────────────────────
        self.cue(5)
        self.P(FadeOut(VGroup(hard_lbl, easy_lbl, gap_arrow, gap_lbl, pvnp)), rt=0.4)

        c5 = cap("Protects every password", sz=32, c=WHT)
        c5b = T("on Earth.", sz=36, c=BLU, weight=BOLD).next_to(c5, DOWN, buff=0.2)

        shackle = Arc(radius=0.5, angle=PI, start_angle=0, color=BLU, stroke_width=7)
        shackle.move_to(UP * 0.5)
        body = RoundedRectangle(width=1.35, height=1.05, corner_radius=0.12,
                                fill_color="#15152A", fill_opacity=1,
                                stroke_color=BLU, stroke_width=5)
        keyhole = Circle(radius=0.11, fill_color=BLU, fill_opacity=1, stroke_width=0)
        keyhole.move_to(body.get_center() + UP * 0.1)
        lock = VGroup(shackle, body, keyhole)

        self.P(FadeIn(c5), rt=0.3)
        self.P(FadeIn(c5b), rt=0.3)
        self.P(FadeIn(lock, shift=DOWN * 0.2), rt=0.5)

        perm_lbl = T("Permanent.", sz=32, c=GRY).next_to(lock, DOWN, buff=0.5)
        self.P(FadeIn(perm_lbl), rt=0.4)

        # ── 6 · "If someone proves the gap doesn't actually exist —" ─────────
        self.cue(6)
        self.P(FadeOut(VGroup(c5, c5b, perm_lbl)), rt=0.35)
        c6 = cap("If the gap isn't real —", sz=32, c=AMB, weight=BOLD)
        self.P(FadeIn(c6), rt=0.4)
        # lock starts to glow ominously
        self.P(lock.animate.set_color(AMB), rt=0.4)

        # ── 7 · "that solving is always secretly as fast as checking —" ──────
        self.cue(7)
        self.P(FadeOut(c6), rt=0.25)
        c7 = T("solving = checking.", sz=36, c=AMB, weight=BOLD).to_edge(UP, buff=0.5)
        self.P(FadeIn(c7), rt=0.45)

        # ── 8 · "every encryption system ... will break." — lock shatters ────
        self.cue(8)
        self.P(FadeOut(c7), rt=0.3)
        c8 = T("EVERY SYSTEM", sz=44, c=RED, weight=BOLD).to_edge(UP, buff=0.5)
        c8b = T("BREAKS.", sz=56, c=RED, weight=BOLD).next_to(c8, DOWN, buff=0.25)
        self.P(FadeIn(c8), rt=0.3)
        self.P(FadeIn(c8b), rt=0.35)

        # crack lines draw across the lock, then it shatters into pieces
        crack1 = Line(lock.get_top() + LEFT*0.2, lock.get_center() + RIGHT*0.15,
                     color=RED, stroke_width=3.5)
        crack2 = Line(lock.get_center() + RIGHT*0.15, lock.get_bottom() + LEFT*0.1,
                     color=RED, stroke_width=3.5)
        self.P(Create(crack1), Create(crack2), rt=0.4)

        shard1 = body.copy().set_color(RED)
        shard2 = shackle.copy().set_color(RED)
        self.P(
            FadeOut(body), FadeOut(shackle), FadeOut(keyhole),
            shard1.animate.shift(DOWN*0.6 + LEFT*0.5).rotate(-0.4).set_opacity(0),
            shard2.animate.shift(UP*0.4 + RIGHT*0.6).rotate(0.5).set_opacity(0),
            FadeOut(crack1), FadeOut(crack2),
            rt=0.6
        )

        # ── 9 · "Nobody has ever proven it." ──────────────────────────────────
        self.cue(9)
        self.P(FadeOut(VGroup(c8, c8b)), rt=0.35)
        nb = T("Nobody has", sz=52).move_to(UP * 0.6)
        nb2 = T("ever proven it.", sz=56, c=GLD, weight=BOLD).next_to(nb, DOWN, buff=0.3)
        self.P(FadeIn(nb, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(nb2, shift=DOWN*0.15), rt=0.45)

        # ── 10 · "$1,000,000 is sitting on the table for whoever does." ──────
        self.cue(10)
        self.P(FadeOut(VGroup(nb, nb2)), rt=0.35)
        cash = T("$1,000,000", sz=76, c=GLD, weight=BOLD).move_to(UP * 0.7)
        table_lbl = T("on the table.", sz=38, c=WHT).next_to(cash, DOWN, buff=0.35)
        for_lbl = T("For whoever does.", sz=32, c=GRY).next_to(table_lbl, DOWN, buff=0.35)
        self.P(Write(cash), rt=0.6)
        self.P(FadeIn(table_lbl, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(for_lbl, shift=DOWN*0.15), rt=0.4)

        self.tail(1.0)
