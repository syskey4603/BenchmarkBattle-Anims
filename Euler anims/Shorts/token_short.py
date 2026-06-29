from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GRN = "#83C167"; GLD = "#FFFF00"; AMB = "#FF9408"; DIM = "#3A3A5A"
TK1 = "#58C4DD"; TK2 = "#FC6255"; TK3 = "#83C167"; TK4 = "#FF9408"


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


class TokenShort(S):
    ONSETS = [
        0.00,   # 0  "Ask ChatGPT to write you exactly fifty words."
        3.31,   # 1  "Count them yourself."
        4.58,   # 2  "It's wrong — often by five or ten."
        6.89,   # 3  "Here's why that's weird."
        8.26,   # 4  "AI doesn't read in words. It reads in tokens —"
        11.43,  # 5  "subword chunks that don't line up with what we call a word."
        14.76,  # 6  "The word 'strawberry' might be three tokens."
        17.97,  # 7  "'Unbelievable' might be four."
        21.56,  # 8  "Ask it to count what it wrote, and it has to guess."
        25.90,  # 9  "It created the text. It cannot audit it."
    ]

    def tbox(self, word, col, sz=62):
        """Coloured token box — the hero visual element."""
        txt = T(word, sz=sz, c=col)
        box = RoundedRectangle(
            width=txt.width + 0.32, height=txt.height + 0.28,
            corner_radius=0.12, fill_color="#12122A",
            fill_opacity=0.9, stroke_color=col, stroke_width=2.5,
        )
        txt.move_to(box.get_center())
        return VGroup(box, txt)

    def para_lines(self, center=ORIGIN):
        """Visual representation of a paragraph as grey lines."""
        widths = [6.4, 6.8, 6.1, 5.8, 3.9]
        lines  = VGroup(*[
            RoundedRectangle(width=w, height=0.28, corner_radius=0.08,
                             fill_color="#3A3A5A", fill_opacity=0.8,
                             stroke_width=0)
            for w in widths
        ]).arrange(DOWN, buff=0.18)
        lines.move_to(center)
        return lines

    def construct(self):
        self.setup()

        # 0 — user prompt → AI writes "50 words"
        prompt  = T("Write me exactly 50 words.", sz=40, c=GRY).move_to(UP * 5.0)
        para    = self.para_lines(center=UP * 1.5)
        ai_says = T("Word count: 50  ✓", sz=40, c=GRN).move_to(DOWN * 1.2)

        self.cue(0)
        self.P(FadeIn(prompt, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(para), rt=0.5)
        self.P(FadeIn(ai_says), rt=0.4)

        # 1 — "count them yourself" — real counter drops in
        self.cue(1)
        real_lbl = T("Actual:", sz=38, c=WHT).move_to(DOWN * 2.8 + LEFT * 1.5)
        real_num = T("43", sz=90, c=RED, weight=BOLD).next_to(real_lbl, RIGHT, buff=0.3)
        self.P(FadeIn(real_lbl), Write(real_num), rt=0.45)

        # 2 — "it's wrong" — AI's claim turns red
        self.cue(2)
        cross = T("≠ 50", sz=50, c=RED, weight=BOLD).next_to(ai_says, RIGHT, buff=0.3)
        self.P(ai_says.animate.set_color(RED), FadeIn(cross), rt=0.4)
        self.W(1.51)

        # 3 — "here's why that's weird" — clean transition
        self.cue(3)
        self.P(FadeOut(VGroup(prompt, para, ai_says, cross, real_lbl, real_num)), rt=0.3)
        why = T("Here's why.", sz=70, c=AMB, weight=BOLD).move_to(ORIGIN)
        self.P(FadeIn(why, shift=UP * 0.2), rt=0.45)
        self.W(0.62)

        # 4 — "AI reads in TOKENS" with simple split example
        self.cue(4)
        self.P(FadeOut(why), rt=0.3)

        l1 = T("AI doesn't read in words.", sz=50).move_to(UP * 4.5)
        l2 = T("It reads in",               sz=50).next_to(l1, DOWN, buff=0.3)
        l3 = T("TOKENS.",  sz=80, c=BLU, weight=BOLD).next_to(l2, DOWN, buff=0.3)

        self.P(FadeIn(l1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(l2, shift=DOWN * 0.15), rt=0.35)
        self.P(Write(l3), rt=0.45)

        # quick split demo: "Hello world" → two boxes
        hw  = T("Hello world", sz=50, c=GRY).move_to(DOWN * 1.2)
        tb1 = self.tbox("Hello", TK1, sz=56)
        tb2 = self.tbox("world", TK2, sz=56)
        trow = VGroup(tb1, tb2).arrange(RIGHT, buff=0.2).move_to(DOWN * 2.8)

        self.P(FadeIn(hw), rt=0.3)
        self.P(FadeOut(hw), FadeIn(trow), rt=0.5)
        self.W(0.62)

        # 5 — "subword chunks" — concept text
        self.cue(5)
        self.P(FadeOut(VGroup(l1, l2, l3, trow)), rt=0.3)

        c1 = T("subword chunks",                   sz=54, c=WHT, weight=BOLD).move_to(UP * 4.5)
        c2 = T("that don't line up",                sz=46).next_to(c1, DOWN, buff=0.28)
        c3 = T("with what we call a word.",          sz=44).next_to(c2, DOWN, buff=0.24)
        self.P(FadeIn(c1), rt=0.4)
        self.P(FadeIn(c2), FadeIn(c3), lag_ratio=0.3, rt=0.45)
        self.W(2.13)

        # 6 — HERO VISUAL: "strawberry" splits into 3 coloured token boxes
        self.cue(6)
        self.P(FadeOut(VGroup(c1, c2, c3)), rt=0.3)

        sb_word  = T("strawberry", sz=72, c=WHT).move_to(UP * 4.2)
        one_word = T("1 word", sz=34, c=GRY).next_to(sb_word, DOWN, buff=0.2)
        self.P(FadeIn(sb_word, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(one_word), rt=0.3)
        self.W(0.25)

        tk_s  = self.tbox("straw", TK1)
        tk_b  = self.tbox("ber",   TK2)
        tk_r  = self.tbox("ry",    TK3)
        sb_row = VGroup(tk_s, tk_b, tk_r).arrange(RIGHT, buff=0.16).move_to(UP * 1.8)

        arr = Arrow(sb_word.get_bottom() + DOWN * 0.05,
                    sb_row.get_top()   + UP   * 0.05,
                    color=GRY, buff=0.08, stroke_width=2,
                    max_tip_length_to_length_ratio=0.14)

        lbl3 = T("3 tokens", sz=38, c=GRY).next_to(sb_row, DOWN, buff=0.38)

        self.P(Create(arr), rt=0.3)
        self.P(LaggedStart(*[GrowFromCenter(t) for t in [tk_s, tk_b, tk_r]],
                            lag_ratio=0.2), rt=0.55)
        self.P(FadeIn(lbl3), rt=0.3)
        self.W(1.28)

        # 7 — "Unbelievable" splits into 4 tokens
        self.cue(7)
        ub_word  = T("Unbelievable", sz=68, c=WHT).move_to(DOWN * 0.5)
        self.P(FadeIn(ub_word), rt=0.4)
        self.W(0.35)

        u1 = self.tbox("Un",   TK1, sz=54)
        u2 = self.tbox("be",   TK2, sz=54)
        u3 = self.tbox("liev", TK3, sz=54)
        u4 = self.tbox("able", TK4, sz=54)
        ub_row = VGroup(u1, u2, u3, u4).arrange(RIGHT, buff=0.14).move_to(DOWN * 2.3)
        if ub_row.width > 7.6:
            ub_row.scale_to_fit_width(7.6)

        lbl4   = T("4 tokens", sz=36, c=GRY).next_to(ub_row, DOWN, buff=0.32)
        neq    = T("tokens  ≠  words", sz=46, c=RED, weight=BOLD).move_to(DOWN * 5.0)

        self.P(LaggedStart(*[GrowFromCenter(u) for u in [u1,u2,u3,u4]], lag_ratio=0.18), rt=0.55)
        self.P(FadeIn(lbl4), rt=0.3)
        self.P(FadeIn(neq, shift=UP * 0.15), rt=0.4)
        self.W(1.74)

        # 8 — "ask it to count — it has to guess"
        self.cue(8)
        self.P(FadeOut(VGroup(sb_word, one_word, arr, sb_row, lbl3,
                               ub_word, ub_row, lbl4, neq)), rt=0.3)

        q1    = T("Ask it to count what it wrote.", sz=46).move_to(UP * 4.0)
        guess = T("It has to guess.", sz=76, c=RED, weight=BOLD).move_to(UP * 2.0)
        ai2   = T("AI says: 50 ✓",  sz=44, c=GRN).move_to(DOWN * 0.2)
        act2  = T("Reality:  43 ✗",  sz=44, c=RED).move_to(DOWN * 1.4)

        self.P(FadeIn(q1, shift=DOWN * 0.15), rt=0.4)
        self.P(Write(guess), rt=0.5)
        self.P(FadeIn(ai2), rt=0.35)
        self.P(FadeIn(act2), rt=0.35)
        self.W(2.24)

        # 9 — punchline
        self.cue(9)
        self.P(FadeOut(VGroup(q1, guess, ai2, act2)), rt=0.3)

        p1 = T("It created the text.",      sz=54).move_to(UP * 4.2)
        p2 = T("It cannot audit it.",        sz=54, c=RED, weight=BOLD).next_to(p1, DOWN, buff=0.32)
        p3 = T("The thing you're trusting", sz=44, c=GRY).next_to(p2, DOWN, buff=0.55)
        p4 = T("to write your emails",      sz=44, c=GRY).next_to(p3, DOWN, buff=0.22)
        p5 = T("doesn't know",              sz=50, c=WHT).next_to(p4, DOWN, buff=0.25)
        p6 = T("how long they are.",        sz=50, c=RED).next_to(p5, DOWN, buff=0.22)
        go = T("Go test it right now.", sz=52, c=GLD, weight=BOLD).move_to(DOWN * 5.2)

        self.P(FadeIn(p1, shift=UP * 0.2), rt=0.45)
        self.P(FadeIn(p2, shift=UP * 0.2), rt=0.4)
        self.P(FadeIn(p3), FadeIn(p4), lag_ratio=0.3, rt=0.45)
        self.P(FadeIn(p5), FadeIn(p6), lag_ratio=0.3, rt=0.45)
        self.P(Write(go), rt=0.5)
        self.tail(2.5)
