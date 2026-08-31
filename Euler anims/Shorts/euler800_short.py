# euler800_short.py — the log trick, lean 5-scene structure, 28.4 s
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


class Euler800(S):
    ONSETS = [
        0.26,   #  0  "800 is what's called a hybrid integer,"
        1.97,   #  1  "2 to the 5th times 5 squared."
        4.95,   #  2  "Simple enough to check by hand."
        6.63,   #  3  "But the actual problem asks about a number"
        8.78,   #  4  "with over 4 million digits,"
        10.60,  #  5  "you can't calculate that directly,"
        12.48,  #  6  "no computer on earth holds a number that large."
        15.95,  #  7  "Here's the trick."
        17.05,  #  8  "Take the logarithm of both sides,"
        19.03,  #  9  "and comparing two impossibly huge numbers"
        21.70,  # 10  "turns into just adding two small ones."
        23.31,  # 11  "That single trick is what makes an unsolvable problem solvable."
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

        # ══ SCENE 1 (0.26–4.95s): 800 = hybrid integer, real equation ═════
        n800 = T("800", sz=90, c=GLD, weight=BOLD).move_to(UP*3.5)
        self.cue(0)
        self.P(FadeIn(n800, scale=0.7), rt=0.5)
        hybrid_lbl = T("hybrid integer.", sz=34, c=WHT).next_to(n800, DOWN, buff=0.4)
        self.P(FadeIn(hybrid_lbl), rt=0.4)

        # ── 1 · "2 to the 5th times 5 squared." — real equation builds ────
        self.cue(1)
        eq = MathTex(r"2^5 \times 5^2 = 800", font_size=56, color=AMB)
        eq.next_to(hybrid_lbl, DOWN, buff=0.6)
        self.P(Write(eq), rt=0.9)

        # ══ SCENE 2 (4.95–6.63s): simple by hand ══════════════════════════
        self.cue(2)
        check_lbl = T("check by hand.", sz=32, c=GRN).next_to(eq, DOWN, buff=0.5)
        check_mark = T("\u2713", sz=44, c=GRN).next_to(check_lbl, RIGHT, buff=0.25)
        self.P(FadeIn(check_lbl), FadeIn(check_mark, scale=1.3), rt=0.5)

        # ══ SCENE 3 (6.63–15.95s): the SCALE problem, real contrast ═══════
        self.cue(3)
        self.P(FadeOut(VGroup(n800, hybrid_lbl, eq, check_lbl, check_mark)), rt=0.5)
        real_q = MathTex(r"800800^{800800}", font_size=52, color=WHT).move_to(UP*3.5)
        self.P(FadeIn(real_q, shift=DOWN*0.15), rt=0.5)

        self.cue(4)
        digits_lbl = T("over 4,000,000 digits.", sz=36, c=RED, weight=BOLD)
        digits_lbl.next_to(real_q, DOWN, buff=0.5)
        self.P(FadeIn(digits_lbl, shift=DOWN*0.1), rt=0.5)

        self.cue(5)
        cant_lbl = T("can't calculate that directly.", sz=30, c=GRY)
        cant_lbl.next_to(digits_lbl, DOWN, buff=0.5)
        self.P(FadeIn(cant_lbl), rt=0.5)

        self.cue(6)
        # a computer icon, crossed out, next to the impossible number
        comp_body = RoundedRectangle(width=1.6, height=1.1, corner_radius=0.1,
                                     fill_color="#15152A", fill_opacity=1,
                                     stroke_color=RED, stroke_width=2.5)
        comp_screen = RoundedRectangle(width=1.3, height=0.75, corner_radius=0.06,
                                       fill_color="#0A0A18", fill_opacity=1,
                                       stroke_color=RED, stroke_width=1.5)
        comp_screen.move_to(comp_body.get_center()+UP*0.05)
        comp = VGroup(comp_body, comp_screen).next_to(cant_lbl, DOWN, buff=0.5)
        comp_x = Cross(comp, color=RED, stroke_width=5)
        no_hold_lbl = T("no computer holds it.", sz=28, c=RED, weight=BOLD)
        no_hold_lbl.next_to(comp, DOWN, buff=0.4)
        self.P(FadeIn(comp), rt=0.4)
        self.P(Create(comp_x), rt=0.4)
        self.P(FadeIn(no_hold_lbl), rt=0.4)

        # ══ SCENE 4 (15.95–23.31s): THE TRICK — huge shrinks to small ═════
        self.cue(7)
        self.P(FadeOut(VGroup(real_q, digits_lbl, cant_lbl, comp, comp_x, no_hold_lbl)), rt=0.5)
        trick_lbl = T("Here's the trick.", sz=44, c=GLD, weight=BOLD).move_to(UP*4.5)
        self.P(FadeIn(trick_lbl, shift=DOWN*0.15), rt=0.5)

        self.cue(8)
        before_eq = MathTex(r"p^q \cdot q^p \leq N", font_size=48, color=WHT)
        before_eq.next_to(trick_lbl, DOWN, buff=0.6)
        log_lbl = T("take the log of both sides.", sz=28, c=AMB)
        log_lbl.next_to(before_eq, DOWN, buff=0.4)
        self.P(FadeIn(before_eq, shift=DOWN*0.1), rt=0.5)
        self.P(FadeIn(log_lbl), rt=0.4)

        self.cue(9)
        arrow = Arrow(before_eq.get_bottom()+DOWN*1.0, before_eq.get_bottom()+DOWN*2.0,
                     color=GLD, stroke_width=4)
        huge_lbl = T("impossibly huge", sz=26, c=RED).next_to(arrow, LEFT, buff=0.4).rotate(PI/2)
        self.P(GrowArrow(arrow), rt=0.4)
        self.P(FadeIn(huge_lbl), rt=0.35)

        after_eq = MathTex(r"q\ln p + p\ln q \leq \ln N", font_size=48, color=GRN)
        after_eq.next_to(arrow, DOWN, buff=0.5)
        self.P(FadeOut(log_lbl), rt=0.25)
        self.P(Write(after_eq), rt=0.7)

        # ── 10 · "turns into just adding two small ones." ──────────────────
        self.cue(10)
        small_lbl = T("two small numbers, just added.", sz=28, c=GRN)
        small_lbl.next_to(after_eq, DOWN, buff=0.5)
        self.P(FadeIn(small_lbl, shift=DOWN*0.1), rt=0.5)

        # ══ SCENE 5 (23.31s–end): close ═══════════════════════════════════
        self.cue(11)
        self.P(FadeOut(VGroup(trick_lbl, before_eq, arrow, after_eq, small_lbl)), rt=0.5)
        close1 = T("Unsolvable", sz=48, c=WHT, weight=BOLD).move_to(UP*1.0)
        close2 = T("becomes solvable.", sz=48, c=GLD, weight=BOLD).next_to(close1, DOWN, buff=0.35)
        pulse(close2, rate=1.6, amount=0.03)
        self.P(FadeIn(close1, shift=DOWN*0.15), rt=0.45)
        self.P(Write(close2), rt=0.6)

        self.tail(3.7)
