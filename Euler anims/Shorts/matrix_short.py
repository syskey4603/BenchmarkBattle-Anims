# matrix_short.py — real matrix multiply, scale-up grid, 23.68 s
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

def top_cap(s, sz=36, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(UP*6.3)

def bottom_cap(s, sz=34, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(DOWN*5.7)

def pulse(mob, rate=2.2, amount=0.06):
    """Gentle continuous breathing scale — proper dt-based updater, not a
    buggy self._t reference (that bug already cost a rebuild once)."""
    mob._pulse_clock = 0.0
    base_scale = 1.0
    def _upd(m, dt):
        m._pulse_clock += dt
        s = 1.0 + amount * np.sin(m._pulse_clock * rate)
        m.scale(s / getattr(m, "_last_pulse_s", 1.0))
        m._last_pulse_s = s
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


class Matrix(S):
    ONSETS = [
        0.03,   #  0  "Every word ChatGPT has ever written comes from one operation, repeated billions of times."
        4.76,   #  1  "Multiply a list of numbers by a grid of numbers,"
        7.44,   #  2  "get a new list of numbers."
        9.05,   #  3  "That's it."
        10.06,  #  4  "That's matrix multiplication,"
        11.57,  #  5  "freshman year linear algebra."
        12.83,  #  6  "Stack enough of these on top of each other,"
        15.67,  #  7  "deep enough,"
        16.21,  #  8  "and the output starts to look like understanding."
        18.36,  #  9  "There's no separate thinking step in there."
        20.24,  # 10  "It's one operation, repeated at a scale"
        22.12,  # 11  "no human brain could hold."
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

        # ══ BEAT 0 (0.03–4.76s): one operation, pulsing continuously ══════
        one_op = Circle(radius=0.9, color=GLD, stroke_width=4,
                        fill_color="#1A1800", fill_opacity=0.6).move_to(UP*2.0)
        op_lbl = T("ONE", sz=44, c=GLD, weight=BOLD).move_to(one_op.get_center()+UP*0.2)
        op_lbl2 = T("operation", sz=26, c=GLD).move_to(one_op.get_center()+DOWN*0.3)
        pulse(one_op, rate=1.8, amount=0.05)

        self.cue(0)
        self.P(FadeIn(one_op, scale=0.6), rt=0.5)
        self.P(Write(op_lbl), rt=0.4)
        self.P(FadeIn(op_lbl2), rt=0.3)
        billions_lbl = bottom_cap("repeated billions of times.", sz=32, c=WHT)
        self.P(FadeIn(billions_lbl, shift=UP*0.15), rt=0.4)

        # ══ BEAT 1 (4.76–7.44s): the real multiply — vector × matrix ══════
        self.cue(1)
        self.P(FadeOut(VGroup(one_op, op_lbl, op_lbl2, billions_lbl)), rt=0.4)

        vec = VGroup(T("1", sz=44, c=BLU), T("2", sz=44, c=BLU))
        vec.arrange(RIGHT, buff=0.5)
        vec_box = SurroundingRectangle(vec, buff=0.25, color=BLU, stroke_width=2.5)
        vec_grp = VGroup(vec_box, vec).move_to(UP*3.2)

        times_lbl = T("\u00D7", sz=48, c=GRY).next_to(vec_grp, DOWN, buff=0.35)

        mat = VGroup(
            T("3", sz=40, c=AMB), T("1", sz=40, c=AMB),
            T("2", sz=40, c=AMB), T("4", sz=40, c=AMB),
        )
        mat.arrange_in_grid(rows=2, cols=2, buff=0.5)
        mat_box = SurroundingRectangle(mat, buff=0.25, color=AMB, stroke_width=2.5)
        mat_grp = VGroup(mat_box, mat).next_to(times_lbl, DOWN, buff=0.35)

        self.P(FadeIn(vec_grp, shift=DOWN*0.15), rt=0.45)
        self.P(FadeIn(times_lbl), rt=0.25)
        self.P(FadeIn(mat_grp, shift=DOWN*0.15), rt=0.45)

        # ══ BEAT 2 (7.44–9.05s): result appears, connections highlight ═════
        self.cue(2)
        eq_lbl = T("=", sz=44, c=WHT).next_to(mat_grp, DOWN, buff=0.35)
        result = VGroup(T("7", sz=44, c=GRN), T("9", sz=44, c=GRN))
        result.arrange(RIGHT, buff=0.5)
        result_box = SurroundingRectangle(result, buff=0.25, color=GRN, stroke_width=2.5)
        result_grp = VGroup(result_box, result).next_to(eq_lbl, DOWN, buff=0.35)
        self.P(FadeIn(eq_lbl), rt=0.25)
        self.P(FadeIn(result_grp, scale=1.15), rt=0.5)

        # ══ BEAT 3 (9.05–10.06s): that's it ═══════════════════════════════
        self.cue(3)
        thats_it = T("That's it.", sz=40, c=WHT).next_to(result_grp, DOWN, buff=0.5)
        self.P(FadeIn(thats_it, shift=DOWN*0.1), rt=0.4)

        # ══ BEAT 4-5 (10.06–12.83s): named — matrix multiplication ════════
        self.cue(4)
        self.P(FadeOut(thats_it), rt=0.25)
        name_lbl = T("matrix multiplication.", sz=32, c=GLD, weight=BOLD).next_to(result_grp, DOWN, buff=0.5)
        self.P(FadeIn(name_lbl, shift=DOWN*0.1), rt=0.4)

        self.cue(5)
        fresh_lbl = T("freshman year linear algebra.", sz=26, c=GRY).next_to(name_lbl, DOWN, buff=0.3)
        self.P(FadeIn(fresh_lbl), rt=0.4)

        # ══ BEAT 6-7 (12.83–16.21s): SCALE UP — small grid multiplies out ═
        self.cue(6)
        self.P(FadeOut(VGroup(vec_grp, times_lbl, mat_grp, eq_lbl, result_grp,
                              name_lbl, fresh_lbl)), rt=0.45)
        stack_lbl = top_cap("stack these on top", sz=32, c=WHT)
        self.P(FadeIn(stack_lbl), rt=0.35)

        cells = VGroup()
        for row in range(9):
            for col in range(7):
                c = Square(0.34, fill_color=AMB, fill_opacity=0.5,
                          stroke_color=AMB, stroke_width=1).move_to(
                    [-2.4+col*0.42, 3.2-row*0.42, 0])
                cells.add(c)
        self.P(LaggedStart(*[FadeIn(c, scale=0.5) for c in cells], lag_ratio=0.008), rt=0.9)

        self.cue(7)
        deep_lbl = T("of each other. deep.", sz=32, c=AMB, weight=BOLD).next_to(stack_lbl, DOWN, buff=0.4)
        self.P(FadeIn(deep_lbl, shift=DOWN*0.1), rt=0.4)
        # every cell flickers independently — genuine continuous motion,
        # each with its own phase so the grid never looks frozen
        def make_flicker(phase_offset):
            def _upd(m, dt):
                m._flicker_t = getattr(m, "_flicker_t", phase_offset) + dt
                op = 0.35 + 0.35 * (np.sin(m._flicker_t * 2.4) * 0.5 + 0.5)
                m.set_fill(opacity=op)
            return _upd
        for c in cells:
            c.add_updater(make_flicker(np.random.uniform(0, 6.28)))

        # ══ BEAT 8 (16.21–18.36s): looks like understanding ════════════════
        self.cue(8)
        self.P(FadeOut(VGroup(stack_lbl, deep_lbl)), rt=0.35)
        under_lbl = T("starts to look like", sz=34, c=WHT).move_to(DOWN*2.4)
        under_lbl2 = T("understanding.", sz=40, c=GRN, weight=BOLD).next_to(under_lbl, DOWN, buff=0.3)
        self.P(FadeIn(under_lbl, shift=UP*0.15), rt=0.4)
        self.P(FadeIn(under_lbl2, shift=UP*0.15), rt=0.4)

        # ══ BEAT 9 (18.36–20.24s): no separate thinking step ═══════════════
        self.cue(9)
        self.P(FadeOut(VGroup(under_lbl, under_lbl2)), rt=0.35)
        no_think = T("No separate", sz=34, c=RED).move_to(DOWN*2.4)
        no_think2 = T("\"thinking\" step.", sz=38, c=RED, weight=BOLD).next_to(no_think, DOWN, buff=0.3)
        self.P(FadeIn(no_think, shift=UP*0.15), rt=0.4)
        self.P(FadeIn(no_think2, shift=UP*0.15), rt=0.4)

        # ══ BEAT 10-11 (20.24–end): one operation, unholdable scale ════════
        self.cue(10)
        self.P(FadeOut(VGroup(no_think, no_think2)), rt=0.35)
        one_more = T("One operation.", sz=42, c=WHT, weight=BOLD).move_to(DOWN*2.4)
        self.P(FadeIn(one_more, shift=UP*0.15), rt=0.45)

        self.cue(11)
        scale_lbl = T("No human brain", sz=36, c=GLD).next_to(one_more, DOWN, buff=0.4)
        scale_lbl2 = T("could hold this.", sz=36, c=GLD, weight=BOLD).next_to(scale_lbl, DOWN, buff=0.2)
        self.P(FadeIn(scale_lbl, shift=UP*0.15), rt=0.4)
        self.P(FadeIn(scale_lbl2, shift=UP*0.15), rt=0.45)

        self.tail(1.5)
