# chainrule_short.py — chain rule of probability, real notation, 30.29 s
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


class ChainRule(S):
    ONSETS = [
        0.34,   #  0  "When ChatGPT writes a whole sentence,"
        2.98,   #  1  "it's not doing that all at once,"
        4.50,   #  2  "it's doing something much simpler, over and over."
        7.14,   #  3  "It calculates the probability of the first word,"
        9.81,   #  4  "then the probability of the second word given the first,"
        13.00,  #  5  "then the third given the first two,"
        15.34,  #  6  "and multiplies all of those probabilities together"
        17.19,  #  7  "to get the odds of that exact sentence."
        20.41,  #  8  "That's called the chain rule of probability,"
        22.72,  #  9  "and it means a hundred word paragraph"
        25.19,  # 10  "is really just one long multiplication problem,"
        27.30,  # 11  "one word at a time."
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

        # ══ BEAT 0-2 (0.34–7.14s): words appear ONE AT A TIME, not at once ═
        target = ["The", "cat", "sat", "down."]
        word_mobs = VGroup(*[T(w, sz=44, c=WHT) for w in target])
        word_mobs.arrange(RIGHT, buff=0.35).move_to(UP*3.6)

        self.cue(0)
        hook_lbl = top_cap("writing a sentence...", sz=32, c=WHT)
        self.P(FadeIn(hook_lbl), rt=0.4)

        self.cue(1)
        not_once = T("not all at once.", sz=34, c=RED, weight=BOLD).move_to(UP*2.4)
        self.P(FadeIn(not_once, shift=DOWN*0.15), rt=0.4)

        self.cue(2)
        self.P(FadeOut(VGroup(hook_lbl, not_once)), rt=0.35)
        # each word fades in with a visible beat between — genuinely sequential
        for i, w in enumerate(word_mobs):
            self.P(FadeIn(w, shift=DOWN*0.15), rt=0.28)
            if i < len(word_mobs)-1:
                self.W(0.18)
        one_at_time = T("one word at a time.", sz=28, c=GRY).next_to(word_mobs, DOWN, buff=0.4)
        self.P(FadeIn(one_at_time), rt=0.3)

        # ══ BEAT 3 (7.14–9.81s): P(first word) ══════════════════════════════
        self.cue(3)
        self.P(FadeOut(one_at_time), rt=0.3)
        p1 = MathTex(r"P(w_1)", font_size=56, color=BLU).move_to(UP*0.8)
        self.P(Write(p1), rt=0.55)

        # ══ BEAT 4 (9.81–13.00s): × P(second | first) ══════════════════════
        self.cue(4)
        p2 = MathTex(r"\times\ P(w_2 \mid w_1)", font_size=56, color=AMB)
        p2.next_to(p1, DOWN, buff=0.4)
        self.P(Write(p2), rt=0.65)

        # ══ BEAT 5 (13.00–15.34s): × P(third | first two) ══════════════════
        self.cue(5)
        p3 = MathTex(r"\times\ P(w_3 \mid w_1, w_2)", font_size=56, color=GRN)
        p3.next_to(p2, DOWN, buff=0.4)
        self.P(Write(p3), rt=0.6)

        # ══ BEAT 6 (15.34–17.19s): × ... multiply them all together ════════
        self.cue(6)
        dots = MathTex(r"\times\ \cdots", font_size=56, color=GRY)
        dots.next_to(p3, DOWN, buff=0.4)
        self.P(Write(dots), rt=0.5)
        together_lbl = T("all multiplied together.", sz=26, c=GRY).next_to(dots, DOWN, buff=0.35)
        self.P(FadeIn(together_lbl), rt=0.35)

        # ══ BEAT 7 (17.19–20.41s): = odds of that exact sentence ═══════════
        self.cue(7)
        self.P(FadeOut(together_lbl), rt=0.3)
        eq = MathTex(r"=\ P(\text{sentence})", font_size=56, color=GLD)
        eq.next_to(dots, DOWN, buff=0.5)
        pulse(eq, rate=1.6, amount=0.03)
        self.P(Write(eq), rt=0.7)

        # ══ BEAT 8 (20.41–22.72s): the chain rule of probability ════════════
        self.cue(8)
        self.P(FadeOut(VGroup(word_mobs, p1, p2, p3, dots, eq)), rt=0.45)
        cr_lbl = T("the chain rule", sz=48, c=GLD, weight=BOLD).move_to(UP*1.0)
        cr_lbl2 = T("of probability.", sz=48, c=GLD, weight=BOLD).next_to(cr_lbl, DOWN, buff=0.3)
        self.P(FadeIn(cr_lbl, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(cr_lbl2, shift=DOWN*0.15), rt=0.4)

        # ══ BEAT 9 (22.72–25.19s): a hundred word paragraph ═══════════════
        self.cue(9)
        self.P(FadeOut(VGroup(cr_lbl, cr_lbl2)), rt=0.35)
        hundred_lbl = T("A 100-word paragraph?", sz=34, c=WHT).move_to(UP*1.2)
        self.P(FadeIn(hundred_lbl, shift=DOWN*0.15), rt=0.45)

        # ══ BEAT 10 (25.19–27.30s): one long multiplication problem ═════════
        self.cue(10)
        # a long chain of tiny multiply symbols stretching across the screen
        chain = VGroup(*[T("\u00D7", sz=30, c=AMB) for _ in range(14)])
        chain.arrange(RIGHT, buff=0.15).move_to(DOWN*0.6)
        if chain.width > 7.4:
            chain.scale_to_fit_width(7.4)
        self.P(LaggedStart(*[FadeIn(x, scale=0.5) for x in chain], lag_ratio=0.04), rt=0.8)
        long_lbl = T("one long multiplication.", sz=32, c=AMB, weight=BOLD).next_to(chain, DOWN, buff=0.4)
        self.P(FadeIn(long_lbl), rt=0.35)

        # ══ BEAT 11 (27.30s–end): one word at a time ═══════════════════════
        self.cue(11)
        self.P(FadeOut(VGroup(hundred_lbl, chain, long_lbl)), rt=0.4)
        final_lbl = T("One word at a time.", sz=44, c=WHT, weight=BOLD)
        self.P(Write(final_lbl), rt=0.6)

        self.tail(2.0)
