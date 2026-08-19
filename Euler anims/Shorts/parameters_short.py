# parameters_short.py — trillion parameters, real callback visuals, 29.31 s
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

def top_cap(s, sz=34, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(UP*6.3)

def bottom_cap(s, sz=32, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(DOWN*5.7)

def pulse(mob, rate=2.0, amount=0.05):
    def _upd(m, dt):
        m._pc = getattr(m, "_pc", 0.0) + dt
        s = 1.0 + amount * np.sin(m._pc * rate)
        m.scale(s / getattr(m, "_ls", 1.0))
        m._ls = s
    mob.add_updater(_upd)
    return mob

def make_knob(x, y, r=0.35, color=AMB):
    """A literal adjustable knob — dial with a pointer that oscillates."""
    dial = Circle(radius=r, color=color, stroke_width=3,
                 fill_color="#15152A", fill_opacity=1)
    pointer = Line(ORIGIN, UP*r*0.75, color=WHT, stroke_width=4)
    dial_grp = VGroup(dial, pointer).move_to([x, y, 0])
    return dial_grp

def oscillate(mob, rate=1.3, amount=0.5):
    """Rotates back and forth — visualizes 'being nudged, adjusted.'"""
    def _upd(m, dt):
        m._oc = getattr(m, "_oc", np.random.uniform(0, 6.28)) + dt
        target = amount * np.sin(m._oc * rate)
        delta = target - getattr(m, "_last_o", 0.0)
        m.rotate(delta, about_point=m.get_center())
        m._last_o = target
    mob.add_updater(_upd)
    return mob


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Parameters(S):
    ONSETS = [
        0.21,   #  0  "Every time a company brags their AI has a trillion parameters,"
        4.46,   #  1  "here's what that actually means."
        6.24,   #  2  "Remember those grids of numbers we've been multiplying?"
        7.89,   #  3  "Every single number inside every one of those grids is a parameter."
        12.22,  #  4  "A trillion parameters just means a trillion individual numbers,"
        15.38,  #  5  "sitting in enormous grids,"
        16.55,  #  6  "and during training, the model nudges each one slightly, over and over,"
        20.84,  #  7  "until the whole grid produces better answers."
        22.14,  #  8  "It's not some abstract unit of intelligence,"
        24.60,  #  9  "it's a trillion tiny adjustable knobs,"
        26.48,  # 10  "and that's genuinely all it is."
    ]

    def construct(self):
        self.setup()

        grid_bg = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-7, 7, 1], x_length=8, y_length=14.2,
            background_line_style={"stroke_color": "#34344E", "stroke_width": 0.7,
                                   "stroke_opacity": 0.4},
            axis_config={"stroke_opacity": 0},
        )
        grid_bg.set_z_index(-10)
        self.add(grid_bg)

        # ══ BEAT 0 (0.21–4.46s): the brag ═══════════════════════════════
        brag1 = T("\"a TRILLION", sz=44, c=GLD, weight=BOLD).move_to(UP*2.4)
        brag2 = T("parameters.\"", sz=44, c=GLD, weight=BOLD).next_to(brag1, DOWN, buff=0.25)
        self.cue(0)
        self.P(FadeIn(brag1, shift=DOWN*0.15), rt=0.5)
        self.P(FadeIn(brag2, shift=DOWN*0.15), rt=0.45)

        # ══ BEAT 1 (4.46–6.24s): what does that mean ═══════════════════
        self.cue(1)
        self.P(FadeOut(VGroup(brag1, brag2)), rt=0.35)
        mean_lbl = T("What does that mean?", sz=36, c=WHT)
        self.P(FadeIn(mean_lbl, shift=DOWN*0.15), rt=0.45)

        # ══ BEAT 2 (6.24–7.89s): callback — the grid of numbers ═══════════
        self.cue(2)
        self.P(FadeOut(mean_lbl), rt=0.3)
        callback_lbl = top_cap("remember these?", sz=34, c=BLU)
        small_grid_vals = [["3","1"],["2","4"]]
        cells = VGroup()
        for r in range(2):
            for c in range(2):
                cell_txt = T(small_grid_vals[r][c], sz=40, c=AMB)
                cell_box = SurroundingRectangle(cell_txt, buff=0.2, color=AMB, stroke_width=2.5)
                cells.add(VGroup(cell_box, cell_txt))
        cells.arrange_in_grid(rows=2, cols=2, buff=0.15).move_to(UP*2.0)
        self.P(FadeIn(callback_lbl), rt=0.35)
        self.P(FadeIn(cells, shift=DOWN*0.15), rt=0.5)

        # ══ BEAT 3 (7.89–12.22s): one cell = one parameter ═══════════════
        self.cue(3)
        self.P(FadeOut(callback_lbl), rt=0.3)
        highlight = SurroundingRectangle(cells[0], buff=0.08, color=GLD, stroke_width=4)
        self.P(Create(highlight), rt=0.4)
        param_lbl = T("= 1 parameter.", sz=34, c=GLD, weight=BOLD).next_to(cells, DOWN, buff=0.5)
        self.P(FadeIn(param_lbl, shift=DOWN*0.1), rt=0.4)
        every_lbl = T("Every number in every grid.", sz=26, c=GRY).next_to(param_lbl, DOWN, buff=0.35)
        self.P(FadeIn(every_lbl), rt=0.4)

        # ══ BEAT 4 (12.22–15.38s): SCALE UP — explode into massive grid ═══
        self.cue(4)
        self.P(FadeOut(VGroup(cells, highlight, param_lbl, every_lbl)), rt=0.4)
        trillion_lbl = T("A trillion", sz=48, c=WHT, weight=BOLD).move_to(UP*5.0)
        trillion_lbl2 = T("individual numbers.", sz=40, c=AMB).next_to(trillion_lbl, DOWN, buff=0.3)
        self.P(FadeIn(trillion_lbl, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(trillion_lbl2, shift=DOWN*0.15), rt=0.4)

        big_cells = VGroup()
        for row in range(10):
            for col in range(7):
                sq = Square(0.36, fill_color=AMB, fill_opacity=0.55,
                          stroke_color=AMB, stroke_width=1).move_to(
                    [-2.3+col*0.44, 2.5-row*0.44, 0])
                big_cells.add(sq)
        self.P(LaggedStart(*[FadeIn(c, scale=0.4) for c in big_cells], lag_ratio=0.006), rt=0.9)

        # ══ BEAT 5 (15.38–16.55s): enormous grids ═══════════════════════════
        self.cue(5)
        enormous_lbl = bottom_cap("sitting in enormous grids.", sz=30, c=WHT)
        self.P(FadeIn(enormous_lbl, shift=UP*0.15), rt=0.4)

        # ══ BEAT 6 (16.55–20.84s): TRAINING — a value visibly changing ══════
        self.cue(6)
        self.P(FadeOut(enormous_lbl), rt=0.3)
        train_lbl = bottom_cap("training: nudge each one...", sz=28, c=GRN)
        self.P(FadeIn(train_lbl), rt=0.35)
        # one cell pulls forward and its value visibly ticks through changes
        sample_cell = big_cells[34]  # roughly central
        sample_out = Square(0.36*2.2, fill_color=AMB, fill_opacity=0.55,
                           stroke_color=AMB, stroke_width=2.5).move_to(DOWN*2.0)
        self.P(ReplacementTransform(sample_cell.copy(), sample_out), rt=0.5)
        val_txt = T("0.42", sz=40, c=WHT, weight=BOLD).move_to(sample_out.get_center())
        self.P(FadeIn(val_txt), rt=0.3)
        vals = ["0.37", "0.51", "0.29", "0.44"]
        for v in vals:
            new_val = T(v, sz=40, c=WHT, weight=BOLD).move_to(sample_out.get_center())
            self.P(Transform(val_txt, new_val), rt=0.5)

        # ══ BEAT 7 (20.84–22.14s): whole grid, better answers ═══════════════
        self.cue(7)
        self.P(FadeOut(VGroup(train_lbl, sample_out, val_txt)), rt=0.35)
        better_lbl = bottom_cap("whole grid \u2192 better answers.", sz=30, c=GRN)
        self.P(FadeIn(better_lbl, shift=UP*0.15), rt=0.45)

        # ══ BEAT 8 (22.14–24.60s): not abstract ══════════════════════════════
        self.cue(8)
        self.P(FadeOut(VGroup(trillion_lbl, trillion_lbl2, big_cells, better_lbl)), rt=0.5)
        not_abstract = T("Not some abstract", sz=36, c=WHT).move_to(UP*1.0)
        not_abstract2 = T("unit of intelligence.", sz=36, c=WHT).next_to(not_abstract, DOWN, buff=0.3)
        self.P(FadeIn(not_abstract, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(not_abstract2, shift=DOWN*0.15), rt=0.4)

        # ══ BEAT 9 (24.60–26.48s): a trillion tiny knobs ═════════════════════
        self.cue(9)
        self.P(FadeOut(VGroup(not_abstract, not_abstract2)), rt=0.35)
        knob_row = VGroup(*[make_knob(x, 1.4) for x in [-2.4, -1.2, 0, 1.2, 2.4]])
        for k in knob_row:
            oscillate(k, rate=np.random.uniform(1.0, 1.8), amount=np.random.uniform(0.35, 0.6))
        self.P(LaggedStart(*[GrowFromCenter(k) for k in knob_row], lag_ratio=0.1), rt=0.6)
        knobs_lbl = T("tiny adjustable knobs.", sz=34, c=AMB, weight=BOLD).next_to(knob_row, DOWN, buff=0.5)
        self.P(FadeIn(knobs_lbl, shift=DOWN*0.1), rt=0.4)

        # ══ BEAT 10 (26.48s–end): that's genuinely all it is ═════════════════
        self.cue(10)
        final_lbl = T("That's genuinely", sz=38, c=WHT).next_to(knobs_lbl, DOWN, buff=0.5)
        final_lbl2 = T("all it is.", sz=44, c=GLD, weight=BOLD).next_to(final_lbl, DOWN, buff=0.25)
        self.P(FadeIn(final_lbl, shift=DOWN*0.1), rt=0.4)
        self.P(Write(final_lbl2), rt=0.5)

        self.tail(2.0)
