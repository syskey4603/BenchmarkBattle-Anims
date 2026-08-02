# sequence_short_v3.py — grid background, sweeping entrances, connecting beam
from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080
# frame: 8.0 wide x 14.22 tall -> half extents +/-4.0 horiz, +/-7.11 vert

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GLD = "#FFFF00"; GRN = "#83C167"; DIM = "#2A2A3A"; AMB = "#FF9408"
CLAUDE="#E8925C"; CHATGPT="#10A37F"; GEMINI="#4285F4"; GROK="#FF4500"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)

def top_cap(s, sz=38, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(UP*6.3)

def bottom_cap(s, sz=36, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(DOWN*5.7)

def model_dot(color, label, x, y=0, sz=22):
    d = Dot(radius=0.13, color=color)
    d.move_to(RIGHT*x + UP*y)
    l = T(label, sz=sz, c=color).next_to(d, UP, buff=0.15)
    return VGroup(d, l)


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Sequence(S):
    ONSETS = [
        0.24,   #  0  "2, 4, 8, 16, what comes next."
        2.89,   #  1  "Pause, answer in your head."
        4.44,   #  2  "You said 32."
        5.71,   #  3  "So did every AI I asked, instantly, no hesitation."
        9.68,   #  4  "Here's the problem."
        11.00,  #  5  "32 isn't the only right answer."
        11.68,  #  6  "Infinite different patterns fit those same 4 numbers,"
        15.37,  #  7  "and diverge after."
        16.75,  #  8  "Nobody calculated anything."
        18.13,  #  9  "Everyone just guessed the obvious one."
        20.90,  # 10  "This matters more than it sounds."
        22.68,  # 11  "Every time AI predicts a trend or forecasts a number,"
        25.75,  # 12  "it's making this exact same guess,"
        27.40,  # 13  "dressed up as a calculation."
    ]

    def construct(self):
        self.setup()

        # ── persistent background grid — fills "empty" space with texture,
        # never faded out, never part of any collision math (z-indexed behind
        # everything). This alone kills the flat-black bland feeling.
        grid = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-7, 7, 1],
            x_length=8, y_length=14.2,
            background_line_style={"stroke_color": "#34344E", "stroke_width": 0.7,
                                   "stroke_opacity": 0.4},
            axis_config={"stroke_opacity": 0},
        )
        grid.set_z_index(-10)
        self.add(grid)

        # ══ SCENE 1 (0 – 9.68s): sequence sweeps in from the LEFT ══════════
        xs = [-3.0, -1.5, 0.0, 1.5]
        vals = [2, 4, 8, 16]
        dots = VGroup()
        nums = VGroup()
        SEQ_Y = 4.3
        for x, v in zip(xs, vals):
            d = Dot([x, SEQ_Y, 0], radius=0.16, color=WHT, z_index=3)
            n = T(str(v), sz=62, c=WHT, weight=BOLD).next_to(d, UP, buff=0.3)
            dots.add(d); nums.add(n)
        connectors = VGroup(*[
            Line([xs[i]+0.19, SEQ_Y, 0], [xs[i+1]-0.19, SEQ_Y, 0], color=GRY, stroke_width=2.5)
            for i in range(3)
        ])
        seq_grp = VGroup(dots, nums, connectors)

        qmark_x = 2.75
        qdot = Dot([qmark_x, SEQ_Y, 0], radius=0.16, color=GLD, z_index=3)
        qmark = T("?", sz=68, c=GLD, weight=BOLD).next_to(qdot, UP, buff=0.3)
        qconn = Line([xs[3]+0.19, SEQ_Y, 0], [qmark_x-0.19, SEQ_Y, 0], color=GLD, stroke_width=3)
        q_grp = VGroup(qconn, qdot, qmark)

        self.cue(0)
        # sweep the whole sequence in from off the LEFT edge
        seq_grp.shift(LEFT * 9)
        self.P(seq_grp.animate.shift(RIGHT * 9), rt=0.85, rate_func=rush_from)
        self.P(Create(qconn), GrowFromCenter(qdot), Write(qmark), rt=0.5)

        # ── 1 · "Pause, answer in your head." ────────────────────────────
        self.cue(1)
        pause_lbl = top_cap("pause. guess it.", sz=42, c=GLD)
        self.P(FadeIn(pause_lbl, shift=DOWN*0.2), rt=0.4)

        # ── 2 · "You said 32." ────────────────────────────────────────────
        self.cue(2)
        self.P(FadeOut(pause_lbl), rt=0.2)
        guess32 = T("32", sz=68, c=GLD, weight=BOLD).move_to(qmark.get_center())
        self.P(Transform(qmark, guess32), rt=0.4)

        # ── 3 · "instantly, no hesitation." — chips RISE from below ───────
        self.cue(3)
        chip_row = VGroup(
            model_dot(CLAUDE, "Claude", -2.0, y=-4.0),
            model_dot(CHATGPT, "ChatGPT", -0.65, y=-4.0),
            model_dot(GEMINI, "Gemini", 0.65, y=-4.0),
            model_dot(GROK, "Grok", 2.0, y=-4.0),
        )
        chip_row.shift(DOWN * 9)
        self.P(chip_row.animate.shift(UP * 9), rt=0.7, rate_func=rush_from)
        agree_lbl = T("all said 32. instantly.", sz=32, c=GRY).move_to(DOWN*5.3)
        self.P(FadeIn(agree_lbl, shift=UP*0.1), rt=0.35)

        # connecting beam — links the bottom AI answer to the top question,
        # using the full "empty" middle of the canvas on purpose.
        beam = Line(chip_row.get_top(), qdot.get_center(), color=GLD,
                   stroke_width=2.5, stroke_opacity=0.55)
        self.P(Create(beam, rate_func=linear), rt=0.4)
        self.P(FadeOut(beam), rt=0.3)

        # ══ SCENE 2 (9.68 – 20.90s): branches sweep in from the RIGHT ══════
        self.cue(4)
        self.P(FadeOut(VGroup(chip_row, agree_lbl)), rt=0.35)
        problem_lbl = T("Here's the problem.", sz=48, c=RED, weight=BOLD).move_to(DOWN*1.0)
        self.P(FadeIn(problem_lbl, shift=DOWN*0.15), rt=0.4)

        # ── 5 · "32 isn't the only right answer." ─────────────────────────
        self.cue(5)
        self.P(FadeOut(problem_lbl), rt=0.25)
        not_only = T("not the only answer.", sz=38, c=RED).move_to(DOWN*1.0)
        self.P(FadeIn(not_only, shift=DOWN*0.1), rt=0.4)

        # ── 6 · "Infinite different patterns... same 4 numbers," ─────────
        self.cue(6)
        self.P(FadeOut(not_only), rt=0.25)
        alt_vals = [("30", RED, 2.6), ("22", BLU, 1.6), ("50", GRN, 0.6)]
        alt_paths = VGroup()
        alt_labels = VGroup()
        start_pt = dots[3].get_center()
        for val, col, y in alt_vals:
            end_pt = [qmark_x, y, 0]
            path = Line(start_pt, end_pt, color=col, stroke_width=3)
            adot = Dot(end_pt, radius=0.12, color=col, z_index=3)
            albl = T(val, sz=36, c=col, weight=BOLD).next_to(adot, RIGHT, buff=0.2)
            alt_paths.add(VGroup(path, adot))
            alt_labels.add(albl)
        # sweep the label set in from the right, paths draw normally
        alt_labels.shift(RIGHT * 7)
        self.P(LaggedStart(*[Create(p) for p in alt_paths], lag_ratio=0.2), rt=0.6)
        self.P(alt_labels.animate.shift(LEFT * 7), rt=0.5, rate_func=rush_from)

        # ── 7 · "and diverge after." ──────────────────────────────────────
        self.cue(7)
        infinite_lbl = bottom_cap("infinite valid answers.", sz=34, c=WHT)
        self.P(FadeIn(infinite_lbl, shift=UP*0.15), rt=0.4)

        # ── 8 · "Nobody calculated anything." ─────────────────────────────
        self.cue(8)
        self.P(FadeOut(infinite_lbl), rt=0.2)
        nobody_lbl = bottom_cap("Nobody calculated it.", sz=36, c=WHT)
        self.P(FadeIn(nobody_lbl, shift=UP*0.1), rt=0.4)

        # ── 9 · "Everyone just guessed the obvious one." ──────────────────
        self.cue(9)
        self.P(FadeOut(nobody_lbl), rt=0.2)
        guessed_lbl = bottom_cap("Everyone just guessed.", sz=40, c=GLD, weight=BOLD)
        self.P(FadeIn(guessed_lbl, shift=UP*0.1), rt=0.4)

        # ══ SCENE 3 (20.90 – 22.68s): the pivot ═══════════════════════════
        self.cue(10)
        self.P(FadeOut(VGroup(seq_grp, q_grp, alt_paths, alt_labels, guessed_lbl)), rt=0.4)
        matters1 = T("This matters", sz=68, c=WHT, weight=BOLD).move_to(UP*1.2)
        matters2 = T("more than it sounds.", sz=54, c=AMB).next_to(matters1, DOWN, buff=0.4)
        self.P(FadeIn(matters1, shift=UP*0.3), rt=0.35)
        self.P(FadeIn(matters2, shift=DOWN*0.2), rt=0.4)

        # ══ SCENE 4 (22.68s – end): diagonal trend sweep ═══════════════════
        self.cue(11)
        self.P(FadeOut(VGroup(matters1, matters2)), rt=0.4)

        predict_lbl = top_cap("AI predicts a trend...", sz=40, c=WHT)
        self.P(FadeIn(predict_lbl, shift=DOWN*0.15), rt=0.35)

        trend_pts = [(-3.3,-4.2), (-2.1,-2.9), (-0.9,-1.4), (0.3,0.4), (1.4,2.1)]
        trend = VMobject(color=BLU, stroke_width=5.5)
        trend.set_points_as_corners([[x,y,0] for x,y in trend_pts])
        trend_dots = VGroup(*[Dot([x,y,0], radius=0.11, color=BLU) for x,y in trend_pts])
        self.P(Create(trend), rt=0.6)
        self.P(LaggedStart(*[GrowFromCenter(d) for d in trend_dots], lag_ratio=0.12), rt=0.5)

        dash_cont = DashedLine([1.4,2.1,0], [2.5,3.2,0], color=GLD, stroke_width=5,
                               dash_length=0.14)
        cont_dot = Dot([2.5,3.2,0], radius=0.14, color=GLD)
        self.P(Create(dash_cont), GrowFromCenter(cont_dot), rt=0.5)

        # ── 12 · "it's making this exact same guess," ─────────────────────
        self.cue(12)
        same_guess_lbl = T("same guess.", sz=34, c=GLD).next_to(cont_dot, DOWN, buff=0.3)
        self.P(FadeIn(same_guess_lbl, shift=UP*0.15), rt=0.4)

        # ── 13 · "dressed up as a calculation." ───────────────────────────
        self.cue(13)
        self.P(FadeOut(predict_lbl), rt=0.25)
        dressed_lbl = bottom_cap("dressed up as a calculation.", sz=36, c=RED, weight=BOLD)
        self.P(FadeIn(dressed_lbl, shift=UP*0.15), rt=0.5)

        self.tail(1.2)
