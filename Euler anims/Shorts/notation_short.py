# notation_short.py — "I promise half of you are about to fight" — 27.4 s
from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GLD = "#FFFF00"; GRN = "#83C167"; DIM = "#2A2A3A"; AMB = "#FF9408"
CLAUDE="#E8925C"; CHATGPT="#10A37F"; GEMINI="#4285F4"; GROK="#FF4500"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)

def cap(s, sz=32, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).to_edge(UP, buff=0.5)

def model_chip(name, color, sz=28):
    lbl = T(name, sz=sz, c=color, weight=BOLD)
    box = SurroundingRectangle(lbl, buff=0.22, corner_radius=0.12,
                               color=color, stroke_width=2.5,
                               fill_color="#15152A", fill_opacity=1)
    return VGroup(box, lbl)


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Notation(S):
    # Onsets from ffmpeg silencedetect phrase boundaries (pocketsphinx word
    # recognition failed on this recording — falling back to amplitude-based
    # pause detection per the channel's own established fallback method).
    ONSETS = [
        0.36,   #  0  "Solve this right now,"
        1.94,   #  1  "pause the video."
        3.01,   #  2  "6 divided by 2,"
        4.56,   #  3  "times the quantity 1 plus 2."
        6.86,   #  4  "Got your answer?"
        8.25,   #  5  "We asked 4 AIs the exact same problem."
        11.07,  #  6  "Two said 9."
        12.39,  #  7  "Two said 1."
        13.44,  #  8  "It's not a bug... real notation fight for decades,"
        17.44,  #  9  "even calculators disagree,"
        19.53,  # 10  "Texas Instruments says one thing,"
        21.51,  # 11  "Casio says another."
        23.11,  # 12  "Comment your answer below,"
        24.39,  # 13  "I promise half of you"
        25.47,  # 14  "are about to fight about it."
    ]

    def construct(self):
        self.setup()

        # ── 0 · "Solve this right now," ──────────────────────────────────
        hook = T("SOLVE THIS", sz=62, c=GLD, weight=BOLD)
        self.cue(0)
        self.P(FadeIn(hook, scale=1.15), rt=0.25)

        # ── 1 · "pause the video." ───────────────────────────────────────
        self.cue(1)
        pause_lbl = T("pause the video.", sz=40, c=WHT).next_to(hook, DOWN, buff=0.35)
        self.P(FadeIn(pause_lbl, shift=DOWN*0.1), rt=0.3)

        # ── 2 · "6 divided by 2," — equation begins ─────────────────────
        self.cue(2)
        self.P(FadeOut(VGroup(hook, pause_lbl)), rt=0.3)
        eq1 = MathTex(r"6 \div 2", font_size=76, color=WHT).move_to(UP*1.0)
        self.P(Write(eq1), rt=0.5)

        # ── 3 · "times the quantity 1 plus 2." — equation completes ──────
        self.cue(3)
        eq2 = MathTex(r"\times(1+2)", font_size=76, color=WHT).next_to(eq1, RIGHT, buff=0.15)
        self.P(Write(eq2), rt=0.6)
        qmark = T("= ?", sz=64, c=GLD, weight=BOLD).next_to(VGroup(eq1, eq2), DOWN, buff=0.5)
        self.P(FadeIn(qmark, scale=1.2), rt=0.4)

        # ── 4 · "Got your answer?" ────────────────────────────────────────
        self.cue(4)
        got_lbl = T("Got your answer?", sz=34, c=GRY).next_to(qmark, DOWN, buff=0.5)
        self.P(FadeIn(got_lbl), rt=0.4)

        # ══ SCENE: 4 AIs, same problem (5) ═══════════════════════════════
        self.cue(5)
        self.P(FadeOut(got_lbl), rt=0.25)
        c5 = cap("4 AIs. Same problem.", sz=34, c=WHT)
        self.P(FadeIn(c5), rt=0.35)

        chips = VGroup(
            model_chip("Claude",  CLAUDE),
            model_chip("ChatGPT", CHATGPT),
            model_chip("Gemini",  GEMINI),
            model_chip("Grok",    GROK),
        ).arrange_in_grid(rows=2, cols=2, buff=0.5).move_to(DOWN*2.3)
        self.P(LaggedStart(*[FadeIn(c, scale=1.1) for c in chips], lag_ratio=0.15), rt=0.9)

        # ── 6 · "Two said 9." — two chips migrate to a "9" camp ─────────
        self.cue(6)
        self.P(FadeOut(c5), rt=0.25)
        self.P(FadeOut(VGroup(eq1, eq2, qmark)), rt=0.3)

        nine_lbl = T("9", sz=110, c=GRN, weight=BOLD).move_to(LEFT*2.0 + UP*1.2)
        claude_c, chatgpt_c = chips[0], chips[1]
        self.P(
            claude_c.animate.next_to(nine_lbl, DOWN, buff=0.5).shift(LEFT*0.95),
            chatgpt_c.animate.next_to(nine_lbl, DOWN, buff=0.5).shift(RIGHT*0.95),
            rt=0.55
        )
        self.P(Write(nine_lbl), rt=0.4)

        # ── 7 · "Two said 1." — other two chips migrate to a "1" camp ────
        self.cue(7)
        one_lbl = T("1", sz=110, c=RED, weight=BOLD).move_to(RIGHT*2.0 + UP*1.2)
        gemini_c, grok_c = chips[2], chips[3]
        self.P(
            gemini_c.animate.next_to(one_lbl, DOWN, buff=0.5).shift(LEFT*0.95),
            grok_c.animate.next_to(one_lbl, DOWN, buff=0.5).shift(RIGHT*0.95),
            rt=0.5
        )
        self.P(Write(one_lbl), rt=0.35)

        vs_lbl = T("vs", sz=32, c=GRY).move_to(UP*1.2)
        self.P(FadeIn(vs_lbl), rt=0.3)

        # ══ SCENE: why — the two valid readings (8-11) ═══════════════════
        self.cue(8)
        self.P(FadeOut(VGroup(nine_lbl, one_lbl, vs_lbl, claude_c, chatgpt_c,
                              gemini_c, grok_c)), rt=0.4)
        why1 = T("Not a bug.", sz=44, c=WHT, weight=BOLD).move_to(UP*1.6)
        why2 = T("A real notation fight,", sz=32, c=GRY).next_to(why1, DOWN, buff=0.35)
        why3 = T("decades old.", sz=32, c=GRY).next_to(why2, DOWN, buff=0.15)
        self.P(FadeIn(why1, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(why2, shift=DOWN*0.1), rt=0.35)
        self.P(FadeIn(why3, shift=DOWN*0.1), rt=0.35)

        # two competing groupings, shown as real math side by side
        left_eq = MathTex(r"(6 \div 2)\times(1{+}2)", font_size=34, color=GRN).move_to(LEFT*1.9+DOWN*1.0)
        left_res = MathTex(r"=9", font_size=44, color=GRN).next_to(left_eq, DOWN, buff=0.3)
        right_eq = MathTex(r"6 \div (2(1{+}2))", font_size=34, color=RED).move_to(RIGHT*1.9+DOWN*1.0)
        right_res = MathTex(r"=1", font_size=44, color=RED).next_to(right_eq, DOWN, buff=0.3)
        self.P(FadeIn(left_eq, shift=UP*0.1), rt=0.4)
        self.P(FadeIn(left_res), rt=0.3)
        self.P(FadeIn(right_eq, shift=UP*0.1), rt=0.4)
        self.P(FadeIn(right_res), rt=0.3)

        # ── 9 · "even calculators disagree," ─────────────────────────────
        self.cue(9)
        self.P(FadeOut(VGroup(why1, why2, why3)), rt=0.35)
        calc_lbl = cap("Even calculators disagree.", sz=32, c=GLD)
        self.P(FadeIn(calc_lbl), rt=0.4)

        # ── 10 · "Texas Instruments says one thing," — calculator icon ────
        self.cue(10)
        ti_body = RoundedRectangle(width=1.6, height=2.6, corner_radius=0.15,
                                   fill_color="#1A1A2E", fill_opacity=1,
                                   stroke_color=GRN, stroke_width=2.5)
        ti_body.move_to(left_eq.get_center()+UP*0.1)
        ti_screen = RoundedRectangle(width=1.3, height=0.7, corner_radius=0.05,
                                     fill_color="#0A2A1A", fill_opacity=1,
                                     stroke_color=GRN, stroke_width=1.5)
        ti_screen.move_to(ti_body.get_top()+DOWN*0.55)
        ti_disp = T("9", sz=32, c=GRN, weight=BOLD).move_to(ti_screen.get_center())
        ti_lbl = T("Texas Instruments", sz=18, c=GRN).next_to(ti_body, DOWN, buff=0.25)
        self.P(FadeOut(VGroup(left_eq, left_res, right_eq, right_res)), rt=0.3)
        self.P(FadeIn(ti_body), FadeIn(ti_screen), rt=0.4)
        self.P(Write(ti_disp), rt=0.3)
        self.P(FadeIn(ti_lbl), rt=0.3)

        # ── 11 · "Casio says another." — second calculator icon ──────────
        self.cue(11)
        casio_body = ti_body.copy().set_color(RED).move_to(right_eq.get_center()+UP*0.1)
        casio_screen = ti_screen.copy()
        casio_screen.set_fill(color="#2A0A0A").set_stroke(color=RED)
        casio_screen.move_to(casio_body.get_top()+DOWN*0.55)
        casio_disp = T("1", sz=32, c=RED, weight=BOLD).move_to(casio_screen.get_center())
        casio_lbl = T("Casio", sz=18, c=RED).next_to(casio_body, DOWN, buff=0.25)
        self.P(FadeIn(casio_body), FadeIn(casio_screen), rt=0.4)
        self.P(Write(casio_disp), rt=0.3)
        self.P(FadeIn(casio_lbl), rt=0.3)

        # ══ SCENE: closing dare (12-14) ═══════════════════════════════════
        self.cue(12)
        self.P(FadeOut(VGroup(calc_lbl, ti_body, ti_screen, ti_disp, ti_lbl,
                              casio_body, casio_screen, casio_disp, casio_lbl)), rt=0.4)

        # two chat bubbles arguing, mirroring the "comment war" this baits
        bubble9 = RoundedRectangle(width=2.2, height=0.9, corner_radius=0.3,
                                   fill_color=GRN, fill_opacity=0.9, stroke_width=0)
        bubble9.move_to(LEFT*1.6+UP*0.8)
        b9_txt = T("IT'S 9!", sz=32, c="#0A2A1A", weight=BOLD).move_to(bubble9.get_center())
        bubble1 = RoundedRectangle(width=2.2, height=0.9, corner_radius=0.3,
                                   fill_color=RED, fill_opacity=0.9, stroke_width=0)
        bubble1.move_to(RIGHT*1.6+DOWN*0.4)
        b1_txt = T("NO, IT'S 1!", sz=28, c="#2A0A0A", weight=BOLD).move_to(bubble1.get_center())

        comment_lbl = T("Comment your answer.", sz=34, c=WHT, weight=BOLD).move_to(UP*2.2)
        self.P(FadeIn(comment_lbl, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(bubble9, scale=1.2), Write(b9_txt), rt=0.4)

        # ── 13 · "I promise half of you" ─────────────────────────────────
        self.cue(13)
        self.P(FadeIn(bubble1, scale=1.2), Write(b1_txt), rt=0.4)

        # ── 14 · "are about to fight about it." ──────────────────────────
        self.cue(14)
        fight_lbl = T("Fight about it.", sz=40, c=GLD, weight=BOLD).move_to(DOWN*2.4)
        self.P(Write(fight_lbl), rt=0.5)

        self.tail(1.7)
