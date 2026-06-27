# gradient_descent.py — Gradient Descent short, portrait 1080×1920, 36.1 s
# render: python -m manim gradient_descent.py GradientDescent --resolution 1080,1920 --fps 30 -q h
# mux:    ffmpeg -i GradientDescent.mp4 -i voiceover.mp3 -c:v copy -c:a aac -shortest out.mp4

from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

BLU = "#58C4DD"; GLD = "#FFFF00"; RED = "#FC6255"
AMB = "#FF9408"; GRN = "#83C167"; WHT = "#FFFDE9"; GRY = "#888899"; DIM = "#3A3A5A"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)

def Eq(s, sz=56, c=WHT):
    return MathTex(s, font_size=sz, color=c)


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class GradientDescent(S):
    ONSETS = [
        0.00,   # 0  "Every AI model you've ever used…"
        5.13,   # 1  "Imagine a blindfolded person on a mountain…"
        8.55,   # 2  "They can't see."
        10.23,  # 3  "So they feel the slope…"
        11.40,  # 4  "…and take one step downhill."
        13.54,  # 5  "Then another."
        15.26,  # 6  "Then another."
        16.54,  # 7  "This is gradient descent."
        17.99,  # 8  "The mountain is the AI's mistakes."
        20.15,  # 9  "The valley is where it gets things right."
        22.27,  # 10 "Every time ChatGPT gives you a correct answer —"
        24.63,  # 11 "that answer was found by taking billions of steps…"
        27.70,  # 12 "The most powerful technology in the world."
        31.45,  # 13 "Learned to think"
        34.08,  # 14 "by learning to fall."
    ]

    @staticmethod
    def f(x):      return x * x
    @staticmethod
    def df(x):     return 2 * x
    def step(self, x, lr=0.28): return x - lr * self.df(x)

    def make_axes(self):
        return Axes(
            x_range=[-2.7, 2.7, 1], y_range=[-0.4, 6.5, 1],
            x_length=7.2, y_length=5.8,
            axis_config={"stroke_color": DIM, "stroke_width": 1.6,
                         "include_ticks": False, "include_tip": True,
                         "tip_width": 0.15, "tip_height": 0.15},
        ).move_to(DOWN * 0.15)

    def tangent(self, ax, x, span=1.0):
        s  = self.df(x)
        dx = span / np.sqrt(1 + s * s)
        return Line(ax.c2p(x - dx, self.f(x) - s * dx),
                    ax.c2p(x + dx, self.f(x) + s * dx),
                    color=RED, stroke_width=3.8)

    def step_arrow(self, ax, x, lr=0.28):
        x2 = self.step(x, lr)
        return Arrow(ax.c2p(x, self.f(x)), ax.c2p(x2, self.f(x)),
                     color=AMB, buff=0, stroke_width=4,
                     max_tip_length_to_length_ratio=0.25)

    def construct(self):
        self.setup()

        # 0 — hook text
        t1 = T("Every AI model").move_to(UP * 2.8)
        t2 = T("you've ever used").next_to(t1, DOWN, buff=0.3)
        t3 = T("learned by doing").next_to(t2, DOWN, buff=0.3)
        t4 = T("one simple thing.", sz=58, c=GLD, weight=BOLD).next_to(t3, DOWN, buff=0.35)

        self.cue(0)
        self.P(FadeIn(t1, shift=UP * 0.2), rt=0.5)
        self.P(FadeIn(t2, shift=UP * 0.2), rt=0.45)
        self.P(FadeIn(t3, shift=UP * 0.2), rt=0.45)
        self.P(Write(t4), rt=0.55)

        # 1 — parabola (the mountain)
        self.cue(1)
        self.P(FadeOut(VGroup(t1, t2, t3, t4)), rt=0.4)

        ax   = self.make_axes()
        crv  = ax.plot(lambda x: x ** 2, x_range=[-2.55, 2.55],
                       color=BLU, stroke_width=5.5)
        area = ax.get_area(crv, x_range=[-2.55, 2.55],
                           color=[BLU, "#06091A"], opacity=0.2)

        self.P(Create(ax), rt=0.55)
        self.P(Create(crv, rate_func=smooth), FadeIn(area), rt=1.0)

        x_ball = 2.25
        ball   = Dot(ax.c2p(x_ball, self.f(x_ball)),
                     radius=0.22, color=GLD, z_index=4)
        self.P(GrowFromCenter(ball), rt=0.45)

        # 2 — tangent line shows gradient
        self.cue(2)
        tang = self.tangent(ax, x_ball, span=1.15)
        slbl = T("slope = gradient", sz=36, c=RED).move_to(DOWN * 5.0)
        self.P(Create(tang), FadeIn(slbl), rt=0.5)

        # 3 — step arrow shows negative gradient direction
        self.cue(3)
        sarr = self.step_arrow(ax, x_ball)
        nlbl = T("step = −gradient", sz=36, c=AMB).move_to(DOWN * 5.9)
        self.P(GrowArrow(sarr), FadeIn(nlbl), rt=0.5)
        self.P(FadeOut(VGroup(tang, sarr, slbl, nlbl)), rt=0.25)

        # 4-6 — three gradient descent steps, traced path, no text
        path = TracedPath(ball.get_center, stroke_color=AMB, stroke_width=4)
        self.add(path)

        x = x_ball
        for beat in [4, 5, 6]:
            self.cue(beat)
            x_new = self.step(x)
            tl    = self.tangent(ax, x, span=0.9)
            sa    = self.step_arrow(ax, x)
            self.P(Create(tl), rt=0.22)
            self.P(GrowArrow(sa), rt=0.22)
            self.P(ball.animate.move_to(ax.c2p(x_new, self.f(x_new))),
                   FadeOut(tl), FadeOut(sa), rt=0.40)
            x = x_new

        # 7 — name it
        self.cue(7)
        self.remove(path)
        self.P(FadeOut(VGroup(ax, crv, area, ball)), rt=0.3)

        gd1 = T("GRADIENT", sz=96, c=BLU, weight=BOLD).move_to(UP * 0.6)
        gd2 = T("DESCENT",  sz=96, c=BLU, weight=BOLD).next_to(gd1, DOWN, buff=0.1)
        self.P(Write(gd1), rt=0.45)
        self.P(Write(gd2), rt=0.45)

        # 8 — equation appears, parabola returns
        self.cue(8)
        self.P(FadeOut(VGroup(gd1, gd2)), rt=0.3)

        eq  = Eq(r"w \;\leftarrow\; w - \alpha \nabla L").move_to(UP * 4.6)
        ax2 = self.make_axes()
        c2  = ax2.plot(lambda x: x ** 2, x_range=[-2.55, 2.55],
                       color=BLU, stroke_width=5.5)
        self.P(Write(eq), rt=0.6)
        self.P(Create(ax2), Create(c2), rt=0.5)

        # 9 — star at the minimum
        self.cue(9)
        star = Star(5, outer_radius=0.25, color=GRN,
                    fill_opacity=1, z_index=3).move_to(ax2.c2p(0, 0))
        lmin = T("minimum — gets it right", sz=34, c=GRN).move_to(DOWN * 5.3)
        self.P(GrowFromCenter(star), FadeIn(lmin), rt=0.4)

        # 10 — training loss curve
        self.cue(10)
        self.P(FadeOut(VGroup(ax2, c2, star, eq, lmin)), rt=0.4)

        tax  = Axes(x_range=[0, 10, 2], y_range=[0, 7.5, 2],
                    x_length=7.0, y_length=5.5,
                    axis_config={"stroke_color": DIM, "stroke_width": 1.6,
                                 "include_ticks": False, "include_tip": True,
                                 "tip_width": 0.14, "tip_height": 0.14},
                    ).move_to(DOWN * 0.2)
        lc   = tax.plot(lambda x: 7.0 * np.exp(-0.52 * x) + 0.2,
                        x_range=[0, 10], color=BLU, stroke_width=5.5)
        glbl = T("ChatGPT", sz=52, c=GRN, weight=BOLD).move_to(UP * 5.6)
        slb  = T("training run", sz=36, c=GRY).move_to(UP * 4.7)

        self.P(Create(tax), FadeIn(glbl), FadeIn(slb), rt=0.4)
        self.P(Create(lc, rate_func=smooth), rt=1.8)

        # 11 — step counter
        self.cue(11)
        c1  = T("~100,000,000,000", sz=50, c=GLD, weight=BOLD).move_to(DOWN * 5.0)
        c2_ = T("gradient steps", sz=38).next_to(c1, DOWN, buff=0.25)
        self.P(Write(c1), rt=0.55)
        self.P(FadeIn(c2_), rt=0.4)

        # 12 — most powerful technology + rings
        self.cue(12)
        self.P(FadeOut(VGroup(tax, lc, glbl, slb, c1, c2_)), rt=0.4)

        mdot = Dot(DOWN * 0.5, radius=0.28, color=GLD, z_index=4)
        self.P(GrowFromCenter(mdot), rt=0.5)

        rings = [Circle(radius=0.01, color=GLD, stroke_width=2.5,
                        stroke_opacity=0.9).move_to(mdot) for _ in range(5)]
        self.add(*rings)
        self.P(*[r.animate.scale(20).set_stroke(opacity=0) for r in rings],
               lag_ratio=0.28, rt=1.4)

        pw1 = T("The most powerful",        sz=52).move_to(UP * 5.4)
        pw2 = T("technology in the world.", sz=46).next_to(pw1, DOWN, buff=0.28)
        self.P(FadeIn(pw1, shift=DOWN * 0.15), FadeIn(pw2, shift=DOWN * 0.15),
               lag_ratio=0.3, rt=0.5)

        # 13-14 — finale
        self.cue(13)
        self.P(FadeOut(VGroup(mdot, pw1, pw2)), rt=0.4)

        f1 = T("Learned to think",     sz=66).move_to(UP * 1.8)
        f2 = T("by learning to fall.", sz=62, c=BLU, weight=BOLD
               ).next_to(f1, DOWN, buff=0.4)
        self.P(FadeIn(f1, shift=UP * 0.2), rt=0.55)

        self.cue(14)
        self.P(Write(f2), rt=0.65)

        glows = [Circle(radius=0.01, color=BLU, stroke_width=2,
                        stroke_opacity=0.7).move_to(DOWN * 1.0) for _ in range(3)]
        self.add(*glows)
        self.P(*[g.animate.scale(30).set_stroke(opacity=0) for g in glows],
               lag_ratio=0.35, rt=1.2)

        self.tail(2.0)
