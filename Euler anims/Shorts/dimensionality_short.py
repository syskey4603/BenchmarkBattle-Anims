# dimensionality_short.py — curse of dimensionality, geometric visuals, 32.64 s
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


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Dimensionality(S):
    ONSETS = [
        0.32,   #  0  "Here's something genuinely strange"
        1.61,   #  1  "about the space AI thinks in."
        3.78,   #  2  "In two or three dimensions, nearest neighbor makes obvious sense,"
        7.10,   #  3  "some points are close, some are far."
        9.65,   #  4  "Push into thousands of dimensions,"
        11.87,  #  5  "exactly where AI embeddings live,"
        12.86,  #  6  "and the geometry breaks down."
        16.12,  #  7  "As dimensions increase, the distance to the closest point"
        18.93,  #  8  "and the distance to the farthest point start to converge,"
        21.57,  #  9  "nearly every point ends up roughly the same distance from every other."
        26.10,  # 10  "It's called the curse of dimensionality,"
        28.30,  # 11  "a real, provable property of high dimensional space."
    ]

    def construct(self):
        self.setup()

        grid = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-7, 7, 1], x_length=8, y_length=14.2,
            background_line_style={"stroke_color": "#34344E", "stroke_width": 0.7,
                                   "stroke_opacity": 0.4},
            axis_config={"stroke_opacity": 0},
        )
        grid.set_z_index(-10)
        self.add(grid)

        # ══ BEAT 0-1 (0.32–3.78s): hook ═══════════════════════════════════
        hook1 = T("Something strange", sz=44, c=WHT, weight=BOLD).move_to(UP*3.5)
        self.cue(0)
        self.P(FadeIn(hook1, shift=DOWN*0.15), rt=0.5)

        self.cue(1)
        hook2 = T("about the space AI thinks in.", sz=30, c=GRY).next_to(hook1, DOWN, buff=0.35)
        self.P(FadeIn(hook2), rt=0.45)

        # ══ BEAT 2-3 (3.78–9.65s): 2D scatter — clear near/far distances ═══
        self.cue(2)
        self.P(FadeOut(VGroup(hook1, hook2)), rt=0.4)
        dim_lbl = top_cap("2 dimensions.", sz=36, c=BLU)
        self.P(FadeIn(dim_lbl), rt=0.35)

        pts_2d = VGroup(
            Dot([-1.8, 3.5, 0], radius=0.1, color=WHT),
            Dot([-1.3, 3.7, 0], radius=0.1, color=WHT),   # close pair
            Dot([1.6, 2.0, 0], radius=0.1, color=WHT),
            Dot([-0.4, 0.9, 0], radius=0.1, color=WHT),   # far from others
            Dot([2.2, 4.0, 0], radius=0.1, color=WHT),
        )
        near_line = Line(pts_2d[0].get_center(), pts_2d[1].get_center(), color=GRN, stroke_width=2.5)
        far_line = Line(pts_2d[1].get_center(), pts_2d[3].get_center(), color=RED, stroke_width=2.5)
        self.P(LaggedStart(*[GrowFromCenter(p) for p in pts_2d], lag_ratio=0.15), rt=0.6)
        self.P(Create(near_line), Create(far_line), rt=0.5)

        self.cue(3)
        near_lbl = T("close.", sz=24, c=GRN).next_to(near_line, UP, buff=0.1)
        far_lbl = T("far.", sz=24, c=RED).next_to(far_line, RIGHT, buff=0.1)
        self.P(FadeIn(near_lbl), FadeIn(far_lbl), rt=0.4)
        obvious_lbl = T("obviously different.", sz=28, c=WHT).move_to(UP*0.5)
        self.P(FadeIn(obvious_lbl), rt=0.4)

        # ══ BEAT 4 (9.65–11.87s): push into thousands of dimensions ════════
        self.cue(4)
        self.P(FadeOut(VGroup(dim_lbl, obvious_lbl, near_lbl, far_lbl)), rt=0.4)
        push_lbl = top_cap("push the dimensions...", sz=32, c=AMB)
        self.P(FadeIn(push_lbl), rt=0.35)
        dim_counter = T("2", sz=90, c=GLD, weight=BOLD).move_to(UP*1.0)
        self.P(FadeIn(dim_counter, scale=0.6), rt=0.4)
        for val in ["10", "100", "1,000", "10,000"]:
            new_counter = T(val, sz=90, c=GLD, weight=BOLD).move_to(UP*1.0)
            self.P(Transform(dim_counter, new_counter), rt=0.35)

        # ══ BEAT 5 (11.87–12.86s): exactly where embeddings live ════════════
        self.cue(5)
        embed_lbl = T("where AI embeddings live.", sz=26, c=GRY).next_to(dim_counter, DOWN, buff=0.5)
        self.P(FadeIn(embed_lbl), rt=0.4)

        # ══ BEAT 6 (12.86–16.12s): the points start to blur together ═══════
        self.cue(6)
        self.P(FadeOut(VGroup(push_lbl, dim_counter, embed_lbl, near_line, far_line)), rt=0.45)
        break_lbl = T("the geometry", sz=36, c=RED).move_to(UP*3.5)
        break_lbl2 = T("breaks down.", sz=40, c=RED, weight=BOLD).next_to(break_lbl, DOWN, buff=0.3)
        self.P(FadeIn(break_lbl, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(break_lbl2, shift=DOWN*0.15), rt=0.4)
        # the same points now look roughly equidistant — visually demonstrated
        self.P(pts_2d.animate.arrange_in_grid(rows=1, cols=5, buff=0.75).move_to(UP*1.2), rt=0.6)

        # ══ BEAT 7-9 (16.12–26.10s): the convergence graph — real payoff ═══
        self.cue(7)
        self.P(FadeOut(VGroup(break_lbl, break_lbl2, pts_2d)), rt=0.45)
        ax = Axes(
            x_range=[0, 10, 2], y_range=[0, 2, 0.5],
            x_length=6.2, y_length=5.0,
            axis_config={"include_tip": False, "color": GRY, "stroke_width": 1.5},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).move_to(DOWN*0.6)
        x_lbl = T("dimensions \u2192", sz=22, c=GRY).next_to(ax.x_axis, DOWN, buff=0.2)
        self.P(Create(ax), rt=0.5)
        self.P(FadeIn(x_lbl), rt=0.3)

        far_curve = ax.plot(lambda x: 0.75 * np.exp(-x/6) + 1.0, x_range=[0.1, 9.8],
                            color=RED, stroke_width=3.5)
        far_pt_lbl = T("farthest point", sz=20, c=RED).next_to(ax.c2p(2, 1.55), UP, buff=0.15)
        self.P(Create(far_curve), rt=0.6)
        self.P(FadeIn(far_pt_lbl), rt=0.3)

        self.cue(8)
        near_curve = ax.plot(lambda x: -0.75 * np.exp(-x/6) + 1.0, x_range=[0.1, 9.8],
                             color=GRN, stroke_width=3.5)
        near_pt_lbl = T("closest point", sz=20, c=GRN).next_to(ax.c2p(2, 0.45), DOWN, buff=0.15)
        self.P(Create(near_curve), rt=0.6)
        self.P(FadeIn(near_pt_lbl), rt=0.3)
        conv_lbl = T("converging...", sz=26, c=WHT).next_to(ax, UP, buff=0.3)
        self.P(FadeIn(conv_lbl), rt=0.35)

        # ══ BEAT 9 (21.57–26.10s): nearly the same distance ═════════════════
        self.cue(9)
        self.P(FadeOut(conv_lbl), rt=0.25)
        same_dist = bottom_cap("roughly the same distance", sz=30, c=WHT)
        same_dist2 = T("from everything.", sz=28, c=GLD, weight=BOLD).next_to(same_dist, UP, buff=0.25)
        self.P(FadeIn(same_dist2), rt=0.4)
        self.P(FadeIn(same_dist), rt=0.4)

        # ══ BEAT 10 (26.10–28.30s): curse of dimensionality ═════════════════
        self.cue(10)
        self.P(FadeOut(VGroup(ax, x_lbl, far_curve, near_curve, far_pt_lbl,
                              near_pt_lbl, same_dist, same_dist2)), rt=0.5)
        curse_lbl = T("the curse of", sz=44, c=GLD, weight=BOLD).move_to(UP*0.7)
        curse_lbl2 = T("dimensionality.", sz=44, c=GLD, weight=BOLD).next_to(curse_lbl, DOWN, buff=0.3)
        pulse(curse_lbl2, rate=1.6, amount=0.03)
        self.P(FadeIn(curse_lbl, shift=DOWN*0.15), rt=0.4)
        self.P(Write(curse_lbl2), rt=0.5)

        # ══ BEAT 11 (28.30s–end): real, provable property ═══════════════════
        self.cue(11)
        real_lbl = T("Real. Provable.", sz=34, c=WHT).next_to(curse_lbl2, DOWN, buff=0.5)
        self.P(FadeIn(real_lbl, shift=DOWN*0.1), rt=0.45)

        self.tail(4.0)
