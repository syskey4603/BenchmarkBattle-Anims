# grokking.py — Grokking short, portrait 1080×1920, 23.8 s
# render: python -m manim grokking.py Grokking --resolution 1080,1920 --fps 30 -q h
# mux:    ffmpeg -i Grokking.mp4 -i voiceover.mp3 -c:v copy -c:a aac -shortest out.mp4

from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; AMB = "#FF9408"
GRN = "#83C167"; DIM = "#3A3A5A"; PRP = "#B47FFF"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Grokking(S):
    ONSETS = [
        0.00,   # 0  "Researchers trained an AI on simple maths."
        2.80,   # 1  "For a thousand steps — completely wrong."
        5.00,   # 2  "Ten thousand — still nothing."
        6.90,   # 3  "Then suddenly, with no changes to the code —"
        9.20,   # 4  (spike completes)
        9.90,   # 5  "Perfect."
        10.70,  # 6  "Every single time."
        12.10,  # 7  "They call it grokking."
        13.80,  # 8  "Here's the disturbing part."
        15.40,  # 9  "We built it."
        16.70,  # 10 "We trained it."
        18.10,  # 11 "We still don't know exactly why it happens."
        20.60,  # 12 "Your brain does this too,"
        22.20,  # 13 "by the way."
    ]

    @staticmethod
    def grok_acc(x):
        noise = np.sin(x * 43.7) * 0.013 + np.sin(x * 23.3) * 0.008
        if x < 0.80:
            return max(0., 0.04 + noise)
        t = min(1., (x - 0.80) / 0.12)
        return 0.04 + (1 / (1 + np.exp(-14 * (t - 0.5)))) * 0.94

    def make_axes(self):
        return Axes(
            x_range=[0, 10, 2], y_range=[0, 1, 0.25],
            x_length=7.0, y_length=5.5,
            axis_config={"stroke_color": DIM, "stroke_width": 1.6,
                         "include_ticks": False, "include_tip": True,
                         "tip_width": 0.14, "tip_height": 0.14},
        ).move_to(DOWN * 0.3)

    def curve_to(self, ax, x_end, col, width=4):
        pts = []
        for i in range(400):
            xn = i / 399
            if xn > x_end + 0.003: break
            pts.append(ax.c2p(xn * 10, min(self.grok_acc(xn), 1.0)))
        if len(pts) < 2:
            return VMobject()
        vm = VMobject(stroke_color=col, stroke_width=width)
        vm.set_points_smoothly([np.array(p) for p in pts])
        return vm

    def construct(self):
        self.setup()

        # 0 — hook text + axes appear
        h1 = T("Researchers trained", sz=54).move_to(UP * 1.8)
        h2 = T("an AI on simple maths.", sz=54, c=AMB).next_to(h1, DOWN, buff=0.3)

        ax   = self.make_axes()
        tx_l = T("Training Steps", sz=30, c=GRY).next_to(ax, DOWN, buff=0.3)
        ty_l = T("Accuracy",       sz=30, c=GRY).rotate(PI / 2).next_to(ax, LEFT, buff=0.3)

        self.cue(0)
        self.P(FadeIn(h1, shift=DOWN * 0.2), rt=0.5)
        self.P(FadeIn(h2, shift=DOWN * 0.2), rt=0.5)
        self.P(Create(ax), FadeIn(tx_l), FadeIn(ty_l), rt=0.6)

        # 1 — flat red line + "1000 steps — WRONG"
        self.cue(1)
        flat = self.curve_to(ax, 0.80, RED, width=4)
        w1   = T("1,000 steps — WRONG", sz=32, c=RED).move_to(ax.c2p(1.5, 0.04) + UP * 0.6)
        self.P(Create(flat, rate_func=linear), FadeIn(w1), rt=0.8)

        # 2 — "10,000 — still nothing"
        self.cue(2)
        w2 = T("10,000 — WRONG", sz=32, c=RED).move_to(ax.c2p(6.8, 0.04) + UP * 0.6)
        self.P(FadeIn(w2), rt=0.4)

        # 3 — "then suddenly…"
        self.cue(3)
        sub  = T("Then suddenly,", sz=60, c=AMB, weight=BOLD).move_to(UP * 5.5)
        sub2 = T("with no changes to the code —", sz=44).next_to(sub, DOWN, buff=0.25)
        self.P(FadeIn(sub), FadeIn(sub2), rt=0.5)

        # 4 — spike draws in green
        self.cue(4)
        spike = self.curve_to(ax, 1.0, GRN, width=5)
        self.P(Create(spike, rate_func=smooth), rt=1.8)

        # 5 — "PERFECT"
        self.cue(5)
        perf = T("PERFECT", sz=80, c=GRN, weight=BOLD).move_to(UP * 4.5)
        self.P(Write(perf), rt=0.5)

        # 6 — "every single time"
        self.cue(6)
        every = T("Every single time.", sz=70).move_to(UP * 3.4)
        self.P(FadeOut(sub), FadeOut(sub2), FadeOut(perf), rt=0.3)
        self.P(FadeIn(every), rt=0.5)

        # 7 — GROKKING reveal
        self.cue(7)
        self.P(FadeOut(VGroup(ax, flat, spike, tx_l, ty_l, w1, w2, every)), rt=0.4)

        gl   = T("They call it", sz=72).move_to(UP * 0.5)
        grok = T("GROKKING.", sz=160, c=PRP, weight=BOLD).next_to(gl, DOWN, buff=0.15)
        if grok.width > 7.8:
            grok.scale_to_fit_width(7.8)

        self.P(FadeIn(gl), rt=0.45)
        self.P(Write(grok), rt=0.5)

        # 8 — "here's the disturbing part"
        self.cue(8)
        self.P(FadeOut(VGroup(gl, grok)), rt=0.4)
        dist = T("Here's the disturbing part.", sz=60).move_to(UP * 0.3)
        self.P(FadeIn(dist), rt=0.5)

        # 9-11 — three facts, one at a time
        self.cue(9)
        f1 = T("We built it.",  sz=70).move_to(DOWN * 1.5)
        self.P(FadeIn(f1), rt=0.4)

        self.cue(10)
        f2 = T("We trained it.", sz=70).next_to(f1, DOWN, buff=0.3)
        self.P(FadeIn(f2), rt=0.4)

        self.cue(11)
        f3a = T("We still don't know",   sz=66, c=RED).next_to(f2, DOWN, buff=0.45)
        f3b = T("exactly why.",          sz=66, c=RED).next_to(f3a, DOWN, buff=0.2)
        self.P(FadeIn(f3a), FadeIn(f3b), lag_ratio=0.3, rt=0.5)

        # 12-13 — punchline
        self.cue(12)
        self.P(FadeOut(VGroup(dist, f1, f2, f3a, f3b)), rt=0.4)

        p1 = T("Your brain does this too,", sz=58, c=AMB).move_to(UP * 1.2)
        self.P(FadeIn(p1), rt=0.5)

        self.cue(13)
        p2 = T("by the way.", sz=66).next_to(p1, DOWN, buff=0.35)
        self.P(Write(p2), rt=0.5)

        self.tail(2.0)
