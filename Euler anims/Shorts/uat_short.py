# uat_short.py — Universal Approximation Theorem, real curve morphing, 29.36 s
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

def top_cap(s, sz=32, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(UP*6.3)

def bottom_cap(s, sz=30, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(DOWN*5.7)

def pulse(mob, rate=2.0, amount=0.04):
    def _upd(m, dt):
        m._pc = getattr(m, "_pc", 0.0) + dt
        s = 1.0 + amount * np.sin(m._pc * rate)
        m.scale(s / getattr(m, "_ls", 1.0))
        m._ls = s
    mob.add_updater(_upd)
    return mob

def sigmoid(x, k, x0=0):
    return 1.0 / (1.0 + np.exp(-k * (x - x0)))


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class UAT(S):
    ONSETS = [
        0.30,   #  0  "There's a theorem called the Universal Approximation Theorem,"
        3.67,   #  1  "and it's one of the most quietly insane guarantees in math."
        6.95,   #  2  "It proves a neural network with just one hidden layer"
        9.20,   #  3  "can trace out any continuous shape that exists,"
        12.20,  #  4  "any curve, any pattern, no matter how strange,"
        14.66,  #  5  "just by stacking tiny rectangular steps"
        17.44,  #  6  "until they blend into the real thing."
        19.40,  #  7  "That's not a hope or an estimate,"
        22.02,  #  8  "it's a mathematical certainty."
        23.88,  #  9  "A network isn't guessing when it finds a pattern,"
        26.10,  # 10  "the right shape was always out there,"
        27.87,  # 11  "it just had to find it."
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

        # ══ BEAT 0-1 (0.30–6.95s): theorem name reveal ═════════════════════
        name1 = T("Universal", sz=52, c=GLD, weight=BOLD).move_to(UP*3.8)
        name2 = T("Approximation", sz=52, c=GLD, weight=BOLD).next_to(name1, DOWN, buff=0.2)
        name3 = T("Theorem", sz=52, c=GLD, weight=BOLD).next_to(name2, DOWN, buff=0.2)
        self.cue(0)
        self.P(Write(name1), rt=0.5)
        self.P(Write(name2), rt=0.5)
        self.P(Write(name3), rt=0.5)

        self.cue(1)
        insane_lbl = T("quietly insane.", sz=36, c=RED, weight=BOLD)
        insane_lbl.next_to(name3, DOWN, buff=0.5)
        self.P(FadeIn(insane_lbl, shift=DOWN*0.1), rt=0.45)

        # ══ BEAT 2-3 (6.95–12.20s): THE SIGMOID SHARPENS INTO A STEP ═══════
        self.cue(2)
        self.P(FadeOut(VGroup(name1, name2, name3, insane_lbl)), rt=0.4)
        ax = Axes(
            x_range=[-3, 3, 1], y_range=[-0.3, 1.3, 1], x_length=6.5, y_length=4.5,
            axis_config={"include_tip": False, "color": GRY, "stroke_width": 1.5},
        ).move_to(UP*2.0)
        one_lbl = T("one neuron.", sz=28, c=BLU).next_to(ax, UP, buff=0.3)
        self.P(Create(ax), rt=0.5)
        self.P(FadeIn(one_lbl), rt=0.3)

        k_tracker = ValueTracker(1.0)
        sig_curve = always_redraw(lambda: ax.plot(
            lambda x: sigmoid(x, k_tracker.get_value()), color=BLU, stroke_width=4,
            x_range=[-3, 3]
        ))
        self.add(sig_curve)
        self.P(FadeIn(sig_curve), rt=0.4)

        self.cue(3)
        sharp_lbl = T("crank the weight...", sz=28, c=AMB).next_to(ax, DOWN, buff=0.4)
        self.P(FadeIn(sharp_lbl), rt=0.3)
        self.P(k_tracker.animate.set_value(25.0), rt=1.4, rate_func=smooth)

        # ══ BEAT 4 (12.20–14.66s): now it's a sharp step ═══════════════════
        self.cue(4)
        step_lbl = T("a sharp step.", sz=32, c=GLD, weight=BOLD).next_to(ax, DOWN, buff=0.4)
        self.P(ReplacementTransform(sharp_lbl, step_lbl), rt=0.5)

        # ══ BEAT 5-6 (14.66–19.40s): TWO STEPS COMBINE INTO A BUMP ═════════
        self.cue(5)
        self.P(FadeOut(VGroup(ax, one_lbl, sig_curve, step_lbl)), rt=0.4)

        ax2 = Axes(
            x_range=[-3, 3, 1], y_range=[-0.3, 1.3, 1], x_length=6.5, y_length=4.5,
            axis_config={"include_tip": False, "color": GRY, "stroke_width": 1.5},
        ).move_to(UP*2.0)
        two_lbl = T("two steps, subtracted...", sz=28, c=WHT).next_to(ax2, UP, buff=0.3)
        self.P(Create(ax2), rt=0.4)
        self.P(FadeIn(two_lbl), rt=0.3)

        step_up = ax2.plot(lambda x: sigmoid(x, 25, -1), color=GRN, stroke_width=3)
        step_down = ax2.plot(lambda x: sigmoid(x, 25, 1), color=RED, stroke_width=3)
        self.P(Create(step_up), Create(step_down), rt=0.5)

        self.cue(6)
        bump_curve = ax2.plot(lambda x: sigmoid(x, 25, -1) - sigmoid(x, 25, 1),
                              color=GLD, stroke_width=5)
        bump_lbl = T("one bump.", sz=32, c=GLD, weight=BOLD).next_to(ax2, DOWN, buff=0.4)
        self.P(FadeOut(VGroup(step_up, step_down, two_lbl)), rt=0.3)
        self.P(Create(bump_curve), rt=0.5)
        self.P(FadeIn(bump_lbl), rt=0.3)

        # ══ BEAT 7-8 (19.40–22.02s): mathematical certainty ══════════════════
        self.cue(7)
        self.P(FadeOut(VGroup(ax2, bump_curve, bump_lbl)), rt=0.4)
        not_hope = T("Not a hope.", sz=40, c=WHT, weight=BOLD).move_to(UP*1.0)
        self.P(FadeIn(not_hope, shift=DOWN*0.15), rt=0.45)

        self.cue(8)
        certainty_lbl = T("A mathematical certainty.", sz=36, c=GLD, weight=BOLD)
        certainty_lbl.next_to(not_hope, DOWN, buff=0.5)
        pulse(certainty_lbl, rate=1.6, amount=0.03)
        self.P(Write(certainty_lbl), rt=0.6)

        # ══ BEAT 9-11 (23.88s–end): bumps stack into any shape ══════════════
        self.cue(9)
        self.P(FadeOut(VGroup(not_hope, certainty_lbl)), rt=0.4)

        ax3 = Axes(
            x_range=[-3, 3, 1], y_range=[-1.5, 1.5, 1], x_length=6.5, y_length=5.0,
            axis_config={"include_tip": False, "color": GRY, "stroke_width": 1.5},
        ).move_to(DOWN*0.5)
        target_lbl = T("any shape at all.", sz=30, c=WHT).next_to(ax3, UP, buff=0.3)
        self.P(Create(ax3), rt=0.4)
        self.P(FadeIn(target_lbl), rt=0.3)

        target_curve = ax3.plot(lambda x: np.sin(x*1.8) * np.exp(-x*x/12) * 1.3,
                                color=GRY, stroke_width=2, stroke_opacity=0.5)
        self.P(Create(target_curve), rt=0.5)

        self.cue(10)
        n_bumps = 9
        bumps = VGroup()
        for i in range(n_bumps):
            xL = -3 + i * (6/n_bumps)
            xR = xL + 6/n_bumps
            xc = (xL + xR) / 2
            h = np.sin(xc*1.8) * np.exp(-xc*xc/12) * 1.3
            bar = Rectangle(width=ax3.x_length/n_bumps*0.92,
                           height=abs(h)*ax3.y_length/3.0,
                           fill_color=GLD, fill_opacity=0.75, stroke_width=1,
                           stroke_color=GLD)
            bar.move_to(ax3.c2p(xc, h/2))
            bumps.add(bar)
        self.P(LaggedStart(*[GrowFromEdge(b, DOWN if b.get_center()[1] >= ax3.c2p(0,0)[1] else UP)
                             for b in bumps], lag_ratio=0.08), rt=1.0)

        # ══ BEAT 11 (27.87s–end): it just had to find it ═══════════════════
        self.cue(11)
        found_lbl = bottom_cap("it was always findable.", sz=30, c=GLD, weight=BOLD)
        self.P(FadeIn(found_lbl, shift=UP*0.15), rt=0.5)

        self.tail(1.5)
