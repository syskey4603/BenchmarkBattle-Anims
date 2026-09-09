# pe179_short.py — PE179 3-model comparison, distinct technique visuals, 30.02 s
from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GLD = "#FFFF00"; GRN = "#83C167"; DIM = "#2A2A3A"; AMB = "#FF9408"
CHATGPT = "#10A37F"; CLAUDE = "#E8925C"; GEMINI = "#4285F4"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)

def top_cap(s, sz=32, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(UP*6.3)

def bottom_cap(s, sz=30, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(DOWN*5.7)

def model_chip(name, color, sz=34):
    lbl = T(name, sz=sz, c=color, weight=BOLD)
    box = SurroundingRectangle(lbl, buff=0.25, corner_radius=0.15,
                               color=color, stroke_width=2.5,
                               fill_color="#15152A", fill_opacity=1)
    return VGroup(box, lbl)

def pulse(mob, rate=2.0, amount=0.04):
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


class PE179(S):
    ONSETS = [
        0.05,   #  0  "Project Euler problem 179,"
        1.94,   #  1  "find every number below ten million"
        3.96,   #  2  "with the same divisor count as the number right after it."
        6.18,   #  3  "GPT-6 Astra started with brute force,"
        8.51,   #  4  "checking every divisor for every number one at a time,"
        10.84,  #  5  "nearly 40,000 tokens before it switched."
        14.09,  #  6  "Claude Opus 5 went straight to a sieve,"
        16.09,  #  7  "marking off every multiple of each divisor all at once,"
        19.18,  #  8  "under 15,000 tokens, right on the first try."
        22.47,  #  9  "Gemini 3.1 Pro used that same sieve idea,"
        23.92,  # 10  "but built it from prime factorizations instead,"
        27.64,  # 11  "matching Claude's efficiency almost exactly."
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

        # ══ BEAT 0-2 (0.05–6.18s): one-line problem intro ══════════════════
        pe_lbl = T("Project Euler #179", sz=42, c=GLD, weight=BOLD).move_to(UP*4.5)
        self.cue(0)
        self.P(FadeIn(pe_lbl, shift=DOWN*0.15), rt=0.5)

        self.cue(1)
        ex1 = T("14", sz=44, c=WHT).move_to(UP*2.6 + LEFT*1.3)
        ex2 = T("15", sz=44, c=WHT).move_to(UP*2.6 + RIGHT*1.3)
        arrow = Arrow(ex1.get_right(), ex2.get_left(), color=GLD, stroke_width=3, buff=0.2)
        self.P(FadeIn(ex1), rt=0.35)
        self.P(GrowArrow(arrow), FadeIn(ex2), rt=0.4)

        self.cue(2)
        same_lbl = T("same divisor count?", sz=32, c=GRN).move_to(UP*1.0)
        self.P(FadeIn(same_lbl, shift=DOWN*0.1), rt=0.4)
        million_lbl = T("under 10,000,000.", sz=28, c=GRY).next_to(same_lbl, DOWN, buff=0.35)
        self.P(FadeIn(million_lbl), rt=0.35)

        # ══ BEAT 3-5 (6.18–14.09s): GPT-6 Astra — BRUTE FORCE ═══════════════
        self.cue(3)
        self.P(FadeOut(VGroup(pe_lbl, ex1, ex2, arrow, same_lbl, million_lbl)), rt=0.4)
        chip1 = model_chip("GPT-6 Astra", CHATGPT).move_to(UP*4.7)
        self.P(FadeIn(chip1, shift=DOWN*0.15), rt=0.4)
        bf_lbl = T("brute force.", sz=32, c=RED, weight=BOLD).next_to(chip1, DOWN, buff=0.4)
        self.P(FadeIn(bf_lbl), rt=0.35)

        self.cue(4)
        # sequential per-number check: numbers light up ONE AT A TIME
        nums = VGroup(*[T(str(n), sz=30, c=WHT) for n in range(1, 8)])
        nums.arrange(RIGHT, buff=0.45).move_to(UP*2.4)
        self.P(FadeIn(nums), rt=0.3)
        check_marks = VGroup()
        for i, n in enumerate(nums):
            n.set_color(RED)
            cm = T("\u2713", sz=20, c=RED).next_to(n, DOWN, buff=0.15)
            check_marks.add(cm)
            self.P(FadeIn(cm), rt=0.15)
        one_time_lbl = T("one number at a time.", sz=26, c=GRY).next_to(nums, DOWN, buff=0.8)
        self.P(FadeIn(one_time_lbl), rt=0.35)

        self.cue(5)
        self.P(FadeOut(VGroup(nums, check_marks, one_time_lbl)), rt=0.35)
        tok1 = T("40,000", sz=64, c=RED, weight=BOLD).move_to(UP*0.5)
        self.P(Write(tok1), rt=0.6)
        tok1_lbl = T("tokens.", sz=32, c=RED).next_to(tok1, DOWN, buff=0.3)
        self.P(FadeIn(tok1_lbl), rt=0.3)

        # ══ BEAT 6-8 (14.09–19.18s): Claude Opus 5 — SIEVE ═══════════════════
        self.cue(6)
        self.P(FadeOut(VGroup(chip1, bf_lbl, tok1, tok1_lbl)), rt=0.4)
        chip2 = model_chip("Claude Opus 5", CLAUDE).move_to(UP*4.7)
        self.P(FadeIn(chip2, shift=DOWN*0.15), rt=0.4)
        sieve_lbl = T("a sieve.", sz=32, c=GRN, weight=BOLD).next_to(chip2, DOWN, buff=0.4)
        self.P(FadeIn(sieve_lbl), rt=0.35)

        self.cue(7)
        # PARALLEL marking: all multiples light up AT ONCE
        nums2 = VGroup(*[T(str(n), sz=28, c=WHT) for n in range(1, 13)])
        nums2.arrange_in_grid(rows=2, cols=6, buff=0.4).move_to(UP*2.2)
        self.P(FadeIn(nums2), rt=0.3)
        multiples_of_3 = [nums2[2], nums2[5], nums2[8], nums2[11]]  # 3,6,9,12
        self.P(*[m.animate.set_color(GRN) for m in multiples_of_3], rt=0.4)
        all_once_lbl = T("every multiple, all at once.", sz=24, c=GRY).next_to(nums2, DOWN, buff=0.5)
        self.P(FadeIn(all_once_lbl), rt=0.35)

        self.cue(8)
        self.P(FadeOut(VGroup(nums2, all_once_lbl)), rt=0.35)
        tok2 = T("15,000", sz=64, c=GRN, weight=BOLD).move_to(UP*0.5)
        self.P(Write(tok2), rt=0.55)
        tok2_lbl = T("tokens. first try.", sz=30, c=GRN).next_to(tok2, DOWN, buff=0.3)
        self.P(FadeIn(tok2_lbl), rt=0.35)

        # ══ BEAT 9-11 (22.47–end): Gemini 3.1 Pro — PRIME FACTORIZATION ═════
        self.cue(9)
        self.P(FadeOut(VGroup(chip2, sieve_lbl, tok2, tok2_lbl)), rt=0.4)
        chip3 = model_chip("Gemini 3.1 Pro", GEMINI).move_to(UP*4.7)
        self.P(FadeIn(chip3, shift=DOWN*0.15), rt=0.4)
        same_idea_lbl = T("same sieve idea.", sz=30, c=WHT).next_to(chip3, DOWN, buff=0.4)
        self.P(FadeIn(same_idea_lbl), rt=0.35)

        self.cue(10)
        self.P(FadeOut(same_idea_lbl), rt=0.3)
        # prime factorization visual: 12 = 2^2 * 3^1
        factor_eq = MathTex(r"12 = 2^2 \times 3^1", font_size=48, color=GEMINI)
        factor_eq.move_to(UP*2.6)
        self.P(Write(factor_eq), rt=0.6)
        formula_lbl = MathTex(r"d(12) = (2{+}1)(1{+}1) = 6", font_size=38, color=WHT)
        formula_lbl.next_to(factor_eq, DOWN, buff=0.5)
        self.P(Write(formula_lbl), rt=0.7)

        self.cue(11)
        self.P(FadeOut(VGroup(chip3, factor_eq, formula_lbl)), rt=0.4)
        match_lbl = T("matches Claude's efficiency,", sz=32, c=WHT).move_to(UP*1.0)
        match_lbl2 = T("almost exactly.", sz=40, c=GEMINI, weight=BOLD)
        match_lbl2.next_to(match_lbl, DOWN, buff=0.35)
        pulse(match_lbl2, rate=1.6, amount=0.03)
        self.P(FadeIn(match_lbl, shift=DOWN*0.15), rt=0.4)
        self.P(Write(match_lbl2), rt=0.55)

        self.tail(2.0)
