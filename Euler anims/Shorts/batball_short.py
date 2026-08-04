# batball_short.py — illustration-first, 28.4 s
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

def top_cap(s, sz=36, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(UP*6.3)

def bottom_cap(s, sz=34, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(DOWN*5.7)


def make_bat(x, y, color=AMB):
    body = RoundedRectangle(width=0.55, height=2.0, corner_radius=0.25,
                            fill_color=color, fill_opacity=0.9, stroke_color=WHT,
                            stroke_width=2)
    handle = RoundedRectangle(width=0.22, height=0.6, corner_radius=0.1,
                              fill_color=color, fill_opacity=0.9, stroke_color=WHT,
                              stroke_width=2)
    handle.next_to(body, DOWN, buff=-0.05)
    return VGroup(body, handle).move_to([x, y, 0])

def make_ball(x, y, r=0.42, color=WHT):
    ball = Circle(radius=r, fill_color=color, fill_opacity=1, stroke_color=RED,
                 stroke_width=2.5).move_to([x, y, 0])
    seam1 = Arc(radius=r*0.9, angle=PI*0.7, start_angle=PI*0.65,
               color=RED, stroke_width=2).move_arc_center_to([x, y, 0])
    seam2 = Arc(radius=r*0.9, angle=PI*0.7, start_angle=PI*1.65,
               color=RED, stroke_width=2).move_arc_center_to([x, y, 0])
    return VGroup(ball, seam1, seam2)

def price_tag(text, x, y, color=WHT, sz=34):
    lbl = T(text, sz=sz, c="#0A0A0A", weight=BOLD)
    tag = RoundedRectangle(width=lbl.width+0.5, height=lbl.height+0.35,
                           corner_radius=0.12, fill_color=color, fill_opacity=1,
                           stroke_color=WHT, stroke_width=1.5)
    tag.move_to([x, y, 0])
    lbl.move_to(tag.get_center())
    return VGroup(tag, lbl)


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class BatBall(S):
    ONSETS = [
        0.17,   #  0  "A bat and a ball cost $1.10 total,"
        3.87,   #  1  "the bat costs $1 more than the ball,"
        5.74,   #  2  "how much is the ball."
        7.18,   #  3  "Pause, trust your gut."
        8.81,   #  4  "If you said 10 cents, you're wrong,"
        11.45,  #  5  "and most people say exactly that."
        13.36,  #  6  "The ball is 5 cents,"
        14.56,  #  7  "the bat is $1.05,"
        16.15,  #  8  "that's $1.10 total, and exactly $1 more."
        19.67,  #  9  "Your brain solved an easier question"
        22.11,  # 10  "and handed you that answer instead."
        23.85,  # 11  "That's the same shortcut a language model takes by default."
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

        # ══ BEAT 0 (0.17–3.87s): bat + ball sweep in, combined price tag ═══
        bat = make_bat(-1.3, 2.8)
        ball = make_ball(1.3, 2.6)
        bat.shift(LEFT * 9)
        ball.shift(RIGHT * 9)
        self.cue(0)
        self.P(bat.animate.shift(RIGHT * 9), rt=0.6, rate_func=rush_from)
        self.P(ball.animate.shift(LEFT * 9), rt=0.5, rate_func=rush_from)

        total_tag = price_tag("$1.10 total", 0, 0.2, color=GLD, sz=36)
        self.P(FadeIn(total_tag, shift=UP*0.15), rt=0.45)

        # ── 1 · "the bat costs $1 more than the ball," ────────────────────
        self.cue(1)
        more_arrow = Arrow(bat.get_top()+UP*0.1, ball.get_top()+UP*0.1, color=AMB,
                           stroke_width=3, buff=0.15)
        more_lbl = T("+$1 more", sz=26, c=AMB, weight=BOLD).next_to(more_arrow, UP, buff=0.15)
        self.P(GrowArrow(more_arrow), rt=0.4)
        self.P(FadeIn(more_lbl), rt=0.3)

        # ── 2 · "how much is the ball." — question mark over ball's tag ───
        self.cue(2)
        qtag = price_tag("?", 1.3, 1.4, color=RED, sz=40)
        self.P(FadeIn(qtag, scale=1.3), rt=0.45)

        # ══ BEAT 3 (7.18–8.81s): pause ═══════════════════════════════════
        self.cue(3)
        pause_lbl = top_cap("pause. trust your gut.", sz=34, c=GLD)
        self.P(FadeIn(pause_lbl, shift=DOWN*0.15), rt=0.4)

        # ══ BEAT 4 (8.81–11.45s): crowd of "10¢" guesses ════════════════════
        self.cue(4)
        self.P(FadeOut(pause_lbl), rt=0.25)
        guesses = VGroup(*[
            T("10¢", sz=30, c=RED, weight=BOLD)
            for _ in range(5)
        ])
        gx = [-2.6, -1.3, 0, 1.3, 2.6]
        for g, x in zip(guesses, gx):
            g.move_to([x, -1.3, 0])
        self.P(LaggedStart(*[FadeIn(g, shift=DOWN*0.15) for g in guesses], lag_ratio=0.1), rt=0.6)

        # ── 5 · "and most people say exactly that." ───────────────────────
        self.cue(5)
        most_lbl = T("most people.", sz=32, c=RED).next_to(guesses, DOWN, buff=0.4)
        self.P(FadeIn(most_lbl), rt=0.35)
        wrong_x = Cross(guesses, color=RED, stroke_width=7)
        self.P(Create(wrong_x), rt=0.4)

        # ══ BEAT 6 (13.36–14.56s): ball tag flips to 5¢ ═══════════════════
        self.cue(6)
        self.P(FadeOut(VGroup(guesses, most_lbl, wrong_x, qtag,
                              more_arrow, more_lbl)), rt=0.4)
        real_ball_tag = price_tag("5\u00A2", 1.3, 1.4, color=GRN, sz=40)
        self.P(FadeIn(real_ball_tag, scale=1.2), rt=0.45)

        # ── 7 · "the bat is $1.05," ────────────────────────────────────────
        self.cue(7)
        real_bat_tag = price_tag("$1.05", -1.3, 4.9, color=GRN, sz=36)
        self.P(FadeIn(real_bat_tag, shift=DOWN*0.15), rt=0.45)

        # ══ BEAT 8 (16.15–19.67s): the check — sum and difference confirmed ═
        self.cue(8)
        check1 = T("5\u00A2 + $1.05 = $1.10 \u2713", sz=28, c=WHT).move_to(DOWN*3.0)
        self.P(FadeIn(check1, shift=UP*0.15), rt=0.5)
        check2 = T("$1.05 \u2212 5\u00A2 = $1.00 \u2713", sz=28, c=WHT).next_to(check1, DOWN, buff=0.3)
        self.P(FadeIn(check2, shift=UP*0.15), rt=0.5)

        # ══ BEAT 9 (19.67–22.11s): the real Q silently swaps to an easier one ═
        self.cue(9)
        self.P(FadeOut(VGroup(bat, ball, total_tag, more_arrow, more_lbl,
                              real_ball_tag, real_bat_tag, check1, check2)), rt=0.45)
        real_q = T('"$1 MORE than the ball"', sz=34, c=WHT).move_to(UP*2.0)
        self.P(FadeIn(real_q, shift=DOWN*0.15), rt=0.4)

        # ── 10 · "and handed you that answer instead." — the swap ────────
        self.cue(10)
        strike = Line(real_q.get_left(), real_q.get_right(), color=RED, stroke_width=4)
        self.P(Create(strike), rt=0.35)
        easy_q = T('"the bat is $1"', sz=38, c=RED, weight=BOLD).next_to(real_q, DOWN, buff=0.5)
        self.P(FadeIn(easy_q, shift=DOWN*0.15), rt=0.4)
        swap_lbl = bottom_cap("your brain solved THIS instead.", sz=32, c=RED)
        self.P(FadeIn(swap_lbl, shift=UP*0.15), rt=0.4)

        # ══ BEAT 11 (23.85s–end): the AI mirror ══════════════════════════════
        self.cue(11)
        self.P(FadeOut(VGroup(real_q, strike, easy_q, swap_lbl)), rt=0.4)

        chip_lbl = T("language model", sz=32, c=CGPT, weight=BOLD)
        chip_box = SurroundingRectangle(chip_lbl, buff=0.25, corner_radius=0.15,
                                        color=CGPT, stroke_width=2.5,
                                        fill_color="#0D1A16", fill_opacity=1)
        chip = VGroup(chip_box, chip_lbl).move_to(UP*1.4)
        self.P(FadeIn(chip, shift=DOWN*0.15), rt=0.4)

        ai_guess = T("10\u00A2", sz=52, c=RED, weight=BOLD).next_to(chip, DOWN, buff=0.5)
        self.P(Write(ai_guess), rt=0.4)
        default_lbl = T("same shortcut, by default.", sz=34, c=WHT).next_to(ai_guess, DOWN, buff=0.5)
        self.P(FadeIn(default_lbl, shift=DOWN*0.1), rt=0.45)

        self.tail(3.0)
