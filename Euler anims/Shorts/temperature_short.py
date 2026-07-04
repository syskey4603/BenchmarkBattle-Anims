# temperature_short.py — "It was always gambling." short, 25 s
from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GLD = "#FFFF00"; GRN = "#83C167"; DIM = "#2A2A3A"; AMB = "#FF9408"
CGPT = "#10A37F"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)


def make_die(n, sz=2.2, fill="#15152A", stroke=WHT):
    """Clean die face with n dots."""
    face = Square(side_length=sz, fill_color=fill, fill_opacity=1,
                  stroke_color=stroke, stroke_width=2.8)
    r = sz * 0.23
    pos = {
        1: [(0, 0)],
        2: [(-r, r), (r, -r)],
        3: [(-r, r), (0, 0), (r, -r)],
        4: [(-r, r), (r, r), (-r, -r), (r, -r)],
        5: [(-r, r), (r, r), (0, 0), (-r, -r), (r, -r)],
        6: [(-r, r), (r, r), (-r, 0), (r, 0), (-r, -r), (r, -r)],
    }
    dots = VGroup(*[
        Dot(point=face.get_center() + RIGHT*x + UP*y,
            radius=sz * 0.085, color=stroke)
        for x, y in pos.get(n, [(0, 0)])
    ])
    return VGroup(face, dots)


def dist_bar(segments, width=7.0, height=0.82, cy=0.0):
    """Horizontal probability bar. segments = [(frac, color, label), ...]"""
    grp = VGroup()
    bg = Rectangle(width=width, height=height,
                   fill_color="#12122A", fill_opacity=1,
                   stroke_color=GRY, stroke_width=1.5).move_to(UP * cy)
    grp.add(bg)
    x = -width / 2
    for frac, col, lbl in segments:
        w = frac * width
        rect = Rectangle(width=max(w - 0.05, 0.02), height=height - 0.12,
                         fill_color=col, fill_opacity=0.88, stroke_width=0)
        rect.move_to(RIGHT * (x + w / 2) + UP * cy)
        grp.add(rect)
        if lbl and w > 0.55:
            t = T(lbl, sz=22, c=WHT)
            t.move_to(rect.get_center())
            if t.width > w - 0.12:
                t.scale_to_fit_width(w - 0.12)
            grp.add(t)
        x += w
    grp.add(T("= 1.0", sz=22, c=GLD).next_to(bg, RIGHT, buff=0.2))
    return grp


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Temperature(S):
    ONSETS = [
        0.03,   #  0  "Ask ChatGPT the same question twice."
        2.25,   #  1  "You get different answers."
        3.63,   #  2  "Not because it's thinking differently."
        5.22,   #  3  "At every single word, it rolls dice."
        7.10,   #  4  "Weighted dice —"
        8.48,   #  5  "a probability distribution across a hundred thousand possible next words."
        12.44,  #  6  "The highest weight usually wins."
        14.51,  #  7  "But randomness gets injected."
        16.17,  #  8  "That randomness is called temperature."
        18.39,  #  9  "Set it to zero."
        19.81,  # 10  "Every answer becomes identical. Forever."
        22.75,  # 11  "It was never thinking."
        23.75,  # 12  "It was always gambling."
    ]

    def construct(self):
        self.setup()

        # ── 0 · "Ask ChatGPT the same question twice." ─────────────────────
        cgpt  = T("ChatGPT", sz=64, c=CGPT, weight=BOLD).move_to(UP * 2.4)
        same1 = T("same question →", sz=40).move_to(UP * 0.6)
        same2 = T("same question →", sz=40, c=GRY).next_to(same1, DOWN, buff=0.3)

        self.cue(0)
        self.P(FadeIn(cgpt,  shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(same1, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(same2, shift=DOWN * 0.15), rt=0.3)

        # ── 1 · "You get different answers." ───────────────────────────────
        self.cue(1)
        ans1 = T('"Paris."',  sz=50, c=GRN).move_to(DOWN * 1.5)
        ans2 = T('"France."', sz=50, c=AMB).next_to(ans1, DOWN, buff=0.3)
        self.P(FadeOut(VGroup(same1, same2)), rt=0.25)
        self.P(FadeIn(ans1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(ans2, shift=DOWN * 0.15), rt=0.3)

        # ── 2 · "Not because it's thinking differently." ───────────────────
        self.cue(2)
        self.P(FadeOut(VGroup(cgpt, ans1, ans2)), rt=0.3)
        nb1 = T("Not because it's",     sz=52).move_to(UP * 0.8)
        nb2 = T("thinking differently.", sz=52, c=RED).next_to(nb1, DOWN, buff=0.3)
        self.P(FadeIn(nb1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(nb2, shift=DOWN * 0.15), rt=0.35)

        # ── 3 · "At every single word, it rolls dice." ─────────────────────
        self.cue(3)
        self.P(FadeOut(VGroup(nb1, nb2)), rt=0.3)
        ev_lbl   = T("At every single word,", sz=42).move_to(UP * 5.5)
        die      = make_die(3).move_to(UP * 0.8)
        roll_lbl = T("it rolls dice.", sz=56, c=GLD, weight=BOLD).move_to(DOWN * 1.6)
        self.P(FadeIn(ev_lbl,   shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(die),                          rt=0.4)
        self.P(FadeIn(roll_lbl, shift=DOWN * 0.15), rt=0.35)

        # ── 4 · "Weighted dice —" ──────────────────────────────────────────
        self.cue(4)
        # Flash die through two faces to show randomness, then hold
        die5 = make_die(5).move_to(die.get_center())
        die2 = make_die(2).move_to(die.get_center())
        self.P(Transform(die, die5), rt=0.28)
        self.P(Transform(die, die2), rt=0.28)
        self.P(FadeOut(roll_lbl), rt=0.18)
        w_lbl = T("Weighted dice.", sz=56, c=AMB, weight=BOLD).move_to(DOWN * 1.6)
        self.P(FadeIn(w_lbl, shift=DOWN * 0.15), rt=0.3)

        # ── 5 · "probability distribution / 100k next words" ───────────────
        self.cue(5)
        self.P(FadeOut(VGroup(ev_lbl, die, w_lbl)), rt=0.3)
        bar_hdr = T("100,000 possible next words", sz=36, c=GRY).move_to(UP * 5.5)
        bar = dist_bar([
            (0.58, BLU,  "likely"),
            (0.25, CGPT, "less"),
            (0.17, RED,  "rare"),
        ], cy=0.4)
        self.P(FadeIn(bar_hdr, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(bar),                         rt=0.5)

        # ── 6 · "The highest weight usually wins." ─────────────────────────
        self.cue(6)
        hw1 = T("Highest weight", sz=46).move_to(UP * 4.2)
        hw2 = T("USUALLY wins.", sz=52, c=BLU, weight=BOLD).next_to(hw1, DOWN, buff=0.25)
        self.P(FadeOut(bar_hdr), rt=0.25)
        self.P(FadeIn(hw1, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(hw2, shift=DOWN * 0.15), rt=0.35)

        # ── 7 · "But randomness gets injected." ───────────────────────────
        self.cue(7)
        self.P(FadeOut(VGroup(hw1, hw2)), rt=0.25)
        rand_bar = dist_bar([
            (0.30, BLU,  ""),
            (0.22, GRN,  ""),
            (0.18, AMB,  ""),
            (0.17, CGPT, ""),
            (0.13, RED,  ""),
        ], cy=0.4)
        rnd1 = T("But randomness",  sz=46, c=RED).move_to(UP * 4.2)
        rnd2 = T("gets injected.",  sz=46, c=RED).next_to(rnd1, DOWN, buff=0.22)
        self.P(FadeOut(bar), FadeIn(rand_bar), rt=0.45)
        self.P(FadeIn(rnd1, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(rnd2, shift=DOWN * 0.15), rt=0.3)

        # ── 8 · "That randomness is called temperature." ───────────────────
        self.cue(8)
        self.P(FadeOut(VGroup(rand_bar, rnd1, rnd2)), rt=0.35)
        th1   = T("That randomness",  sz=50, c=GRY).move_to(UP * 2.0)
        th2   = T("is called",        sz=46).next_to(th1, DOWN, buff=0.28)
        t_word = T("temperature.", sz=76, c=RED, weight=BOLD).next_to(th2, DOWN, buff=0.28)
        self.P(FadeIn(th1,    shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(th2,    shift=DOWN * 0.15), rt=0.35)
        self.P(Write(t_word),                      rt=0.5)

        # ── 9 · "Set it to zero." ─────────────────────────────────────────
        self.cue(9)
        self.P(FadeOut(VGroup(th1, th2, t_word)), rt=0.3)
        t_one  = MathTex(r"T = 1.0", font_size=76, color=AMB).move_to(UP * 1.0)
        t_zero = MathTex(r"T = 0",   font_size=76, color=GRN).move_to(UP * 1.0)
        self.P(FadeIn(t_one, shift=DOWN * 0.15), rt=0.35)
        self.P(Transform(t_one, t_zero), rt=0.4)

        # ── 10 · "Every answer becomes identical. Forever." ────────────────
        self.cue(10)
        self.P(FadeOut(t_one), rt=0.3)
        frozen = dist_bar([
            (0.95, GRN, '"Paris."'),
            (0.05, DIM, ""),
        ], cy=0.5)
        id1  = T("Every answer:", sz=46).move_to(UP * 5.5)
        id2  = T("IDENTICAL.",    sz=72, c=GRN, weight=BOLD).next_to(id1, DOWN, buff=0.25)
        self.P(FadeIn(id1,    shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(id2,    shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(frozen),                     rt=0.45)
        forever = T("Forever.", sz=58, c=GLD, weight=BOLD).move_to(DOWN * 2.5)
        self.P(Write(forever), rt=0.4)

        # ── 11 · "It was never thinking." ─────────────────────────────────
        self.cue(11)
        self.P(FadeOut(VGroup(id1, id2, frozen, forever)), rt=0.25)
        nv = T("It was never thinking.", sz=50, c=GRY).move_to(UP * 0.5)
        self.P(FadeIn(nv, shift=DOWN * 0.15), rt=0.4)

        # ── 12 · "It was always gambling." ────────────────────────────────
        self.cue(12)
        self.P(FadeOut(nv), rt=0.25)
        gb1 = T("It was always",  sz=58).move_to(UP * 1.4)
        gb2 = T("gambling.",      sz=88, c=RED, weight=BOLD).next_to(gb1, DOWN, buff=0.38)
        self.P(FadeIn(gb1, shift=DOWN * 0.15), rt=0.4)
        self.P(Write(gb2),                      rt=0.5)

        self.tail(1.5)
