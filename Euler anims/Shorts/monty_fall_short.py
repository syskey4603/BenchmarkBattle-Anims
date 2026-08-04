# monty_fall_short.py — illustration-first, minimal captions, 29.93 s
from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080
# frame: 8.0 wide x 14.22 tall -> half extents +/-4.0 horiz, +/-7.11 vert

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GLD = "#FFFF00"; GRN = "#83C167"; DIM = "#2A2A3A"; AMB = "#FF9408"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)

def top_cap(s, sz=38, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(UP*6.3)

def bottom_cap(s, sz=36, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(DOWN*5.7)


def make_door(num, x, y=1.5, w=1.5, h=2.4, color=WHT):
    """A recognizable door: frame, center panel line, doorknob, number."""
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.08,
                             fill_color="#2A2A42", fill_opacity=1,
                             stroke_color=color, stroke_width=3)
    frame.move_to([x, y, 0])
    panel = Line(frame.get_top()+DOWN*0.15, frame.get_bottom()+UP*0.15,
                color=color, stroke_width=1.5, stroke_opacity=0.5)
    knob = Dot(frame.get_center()+RIGHT*(w*0.28), radius=0.06, color=GLD)
    label = T(str(num), sz=30, c=color, weight=BOLD).next_to(frame, UP, buff=0.2)
    return VGroup(frame, panel, knob), label


def make_host(x=0, y=4.8, blindfolded=False):
    """Simple person icon; blindfold = the whole puzzle's crux, made visible."""
    head = Circle(radius=0.42, color=WHT, fill_color="#D9B896", fill_opacity=1,
                 stroke_width=0)
    body = Arc(radius=0.62, angle=PI, start_angle=0, color=WHT,
              fill_color="#3A5A7A", fill_opacity=1, stroke_width=0)
    body.next_to(head, DOWN, buff=0.02)
    grp = VGroup(body, head).move_to([x, y, 0])
    if blindfolded:
        blind = Rectangle(width=0.7, height=0.16, fill_color="#1A1A1A",
                          fill_opacity=1, stroke_width=0)
        blind.move_to(head.get_center())
        qmark = T("?", sz=26, c=RED, weight=BOLD).next_to(head, UP, buff=0.1)
        return VGroup(grp, blind), qmark
    else:
        eye_l = Dot(head.get_center()+LEFT*0.14+UP*0.02, radius=0.05, color="#1A1A1A")
        eye_r = Dot(head.get_center()+RIGHT*0.14+UP*0.02, radius=0.05, color="#1A1A1A")
        return VGroup(grp, eye_l, eye_r), None


def prob_bar(frac_a, label_a, col_a, label_b, col_b, width=4.0, height=0.7, y=0):
    """Two-segment probability bar — visual weight, not just a typed fraction."""
    bg = Rectangle(width=width, height=height, fill_color="#12122A",
                  fill_opacity=1, stroke_color=GRY, stroke_width=1.5).move_to(UP*y)
    fill_a = Rectangle(width=width*frac_a, height=height-0.1, fill_color=col_a,
                       fill_opacity=0.9, stroke_width=0)
    fill_a.align_to(bg, LEFT).shift(RIGHT*0.05).set_y(y)
    fill_b = Rectangle(width=width*(1-frac_a), height=height-0.1, fill_color=col_b,
                       fill_opacity=0.9, stroke_width=0)
    fill_b.align_to(bg, RIGHT).shift(LEFT*0.05).set_y(y)
    la = T(label_a, sz=22, c="#0A0A0A", weight=BOLD)
    la.move_to(fill_a.get_center()) if frac_a > 0.18 else la.next_to(fill_a, UP, buff=0.1)
    lb = T(label_b, sz=22, c="#0A0A0A", weight=BOLD)
    lb.move_to(fill_b.get_center()) if (1-frac_a) > 0.18 else lb.next_to(fill_b, UP, buff=0.1)
    return VGroup(bg, fill_a, fill_b, la, lb)


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class MontyFall(S):
    ONSETS = [
        0.34,   # 0  "Three doors, one prize, you pick door 1."
        3.27,   # 1  "This time the host has no idea what's behind any door."
        6.36,   # 2  "He opens door 3 at random, it happens to show a goat."
        9.82,   # 3  "Should you switch."
        11.37,  # 4  "Pause, think it through."
        12.89,  # 5  "Most people say switch, 2 in 3 odds, classic Monty Hall."
        17.34,  # 6  "That's wrong here."
        19.40,  # 7  "The host didn't know anything, so this isn't the same puzzle."
        22.39,  # 8  "Switching now gives you no advantage, it's a flat 50/50."
        26.32,  # 9  "One detail changed, and the famous answer stopped applying."
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

        # ══ BEAT 0 (0.34–3.27s): three real doors, pick door 1 ═════════════
        d1, l1 = make_door(1, -2.2, color=GLD)
        d2, l2 = make_door(2, 0.0, color=WHT)
        d3, l3 = make_door(3, 2.2, color=WHT)
        doors = VGroup(d1, d2, d3).move_to(UP*1.5)
        labels = VGroup(l1, l2, l3)
        doors.shift(DOWN * 12)  # sweep up from below
        labels.shift(DOWN * 12)

        self.cue(0)
        self.P(VGroup(doors, labels).animate.shift(UP * 12), rt=0.8, rate_func=rush_from)
        pick_glow = SurroundingRectangle(d1, buff=0.08, color=GLD, stroke_width=4)
        self.P(Create(pick_glow), rt=0.4)

        # ══ BEAT 1 (3.27–6.36s): host appears — BLINDFOLDED ════════════════
        self.cue(1)
        host_grp, host_q = make_host(x=0, y=4.8, blindfolded=True)
        host_grp.shift(UP * 9)  # drop in from above
        self.P(host_grp.animate.shift(DOWN * 9), rt=0.6, rate_func=rush_from)
        self.P(FadeIn(host_q, scale=1.3), rt=0.35)
        no_idea_lbl = top_cap("no idea what's behind any door.", sz=32, c=RED)
        self.P(FadeIn(no_idea_lbl, shift=DOWN*0.15), rt=0.4)

        # ══ BEAT 2 (6.36–9.82s): door 3 opens at random — goat revealed ═════
        self.cue(2)
        self.P(FadeOut(no_idea_lbl), rt=0.25)
        # door 3 "opens": fade its frame, reveal a goat behind it
        goat = T("\U0001F410", sz=64).move_to(d3.get_center())
        self.P(d3.animate.set_opacity(0.15), rt=0.5)
        self.P(FadeIn(goat, scale=1.3), rt=0.5)
        random_lbl = T("(picked at random)", sz=24, c=GRY).next_to(d3, DOWN, buff=1.6)
        self.P(FadeIn(random_lbl), rt=0.35)

        # ══ BEAT 3 (9.82–11.37s): should you switch? doors 1 & 2 pulse ══════
        self.cue(3)
        self.P(FadeOut(random_lbl), rt=0.2)
        switch_q = T("SWITCH?", sz=52, c=GLD, weight=BOLD).move_to(DOWN*1.2)
        self.P(FadeIn(switch_q, scale=1.15), rt=0.35)
        pick_glow2 = SurroundingRectangle(d2, buff=0.08, color=BLU, stroke_width=4)
        self.P(Create(pick_glow2), rt=0.35)

        # ══ BEAT 4 (11.37–12.89s): pause ═════════════════════════════════
        self.cue(4)
        self.P(FadeOut(switch_q), rt=0.25)
        pause_lbl = T("pause.", sz=44, c=WHT).move_to(DOWN*1.2)
        self.P(FadeIn(pause_lbl), rt=0.4)

        # ══ BEAT 5 (12.89–17.34s): the classic Monty Hall — 2/3 bar ═════════
        self.cue(5)
        self.P(FadeOut(VGroup(pause_lbl, pick_glow, pick_glow2, goat, d3)), rt=0.4)
        self.P(FadeOut(VGroup(doors, labels, host_grp, host_q)), rt=0.35)

        classic_lbl = top_cap("Classic Monty Hall:", sz=36, c=GRY)
        self.P(FadeIn(classic_lbl), rt=0.35)

        # a knowing host (eyes open) + the famous 2/3 bar
        know_host, _ = make_host(x=-2.0, y=2.5, blindfolded=False)
        know_lbl = T("host KNOWS", sz=24, c=GRN).next_to(know_host, DOWN, buff=0.3)
        self.P(FadeIn(know_host, shift=DOWN*0.1), rt=0.4)
        self.P(FadeIn(know_lbl), rt=0.3)

        bar_classic = prob_bar(2/3, "SWITCH", GRN, "STAY", GRY, y=-1.5)
        self.P(FadeIn(bar_classic, shift=UP*0.1), rt=0.5)
        two_thirds = T("2/3 vs 1/3", sz=30, c=WHT).next_to(bar_classic, DOWN, buff=0.35)
        self.P(FadeIn(two_thirds), rt=0.35)

        # ══ BEAT 6 (17.34–19.40s): WRONG HERE — big red X ═══════════════════
        self.cue(6)
        wrong_x = Cross(VGroup(bar_classic, two_thirds), color=RED, stroke_width=8)
        wrong_lbl = T("WRONG HERE.", sz=48, c=RED, weight=BOLD).move_to(UP*5.0)
        self.P(Create(wrong_x), rt=0.4)
        self.P(FadeIn(wrong_lbl, scale=1.2), rt=0.4)

        # ══ BEAT 7 (19.40–22.39s): back to OUR host — blindfold emphasized ══
        self.cue(7)
        self.P(FadeOut(VGroup(classic_lbl, know_host, know_lbl, bar_classic,
                              two_thirds, wrong_x, wrong_lbl)), rt=0.45)
        blind_host, blind_q = make_host(x=0, y=3.0, blindfolded=True)
        self.P(FadeIn(blind_host, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(blind_q, scale=1.3), rt=0.3)
        didnt_know_lbl = T("Our host didn't know", sz=36, c=RED, weight=BOLD).next_to(blind_host, DOWN, buff=0.4)
        didnt_know_lbl2 = T("anything.", sz=36, c=RED, weight=BOLD).next_to(didnt_know_lbl, DOWN, buff=0.15)
        self.P(FadeIn(didnt_know_lbl), rt=0.35)
        self.P(FadeIn(didnt_know_lbl2), rt=0.35)

        # ══ BEAT 8 (22.39–26.32s): the real 50/50 bar ════════════════════════
        self.cue(8)
        self.P(FadeOut(VGroup(didnt_know_lbl, didnt_know_lbl2)), rt=0.35)
        bar_real = prob_bar(0.5, "SWITCH", BLU, "STAY", AMB, y=-1.5)
        self.P(FadeIn(bar_real, shift=UP*0.1), rt=0.5)
        fifty_lbl = T("a flat 50/50.", sz=36, c=WHT, weight=BOLD).next_to(bar_real, DOWN, buff=0.35)
        self.P(FadeIn(fifty_lbl), rt=0.4)

        # ══ BEAT 9 (26.32s–end): one detail changed — side by side ══════════
        self.cue(9)
        self.P(FadeOut(VGroup(blind_host, blind_q, bar_real, fifty_lbl)), rt=0.45)

        left_host, left_q = make_host(x=-1.7, y=1.5, blindfolded=False)
        right_host, right_q = make_host(x=1.7, y=1.5, blindfolded=True)
        left_lbl = T("host KNOWS", sz=24, c=GRN).next_to(left_host, DOWN, buff=0.3)
        right_lbl = T("host DOESN'T", sz=24, c=RED).next_to(right_host, DOWN, buff=0.3)
        left_res = T("→ 2/3", sz=32, c=GRN, weight=BOLD).next_to(left_lbl, DOWN, buff=0.3)
        right_res = T("→ 1/2", sz=32, c=RED, weight=BOLD).next_to(right_lbl, DOWN, buff=0.3)
        self.P(FadeIn(left_host), FadeIn(right_host), FadeIn(right_q), rt=0.4)
        self.P(FadeIn(left_lbl), FadeIn(right_lbl), rt=0.35)
        self.P(FadeIn(left_res), FadeIn(right_res), rt=0.4)

        one_detail = bottom_cap("One detail changed everything.", sz=34, c=GLD, weight=BOLD)
        self.P(FadeIn(one_detail, shift=UP*0.15), rt=0.45)

        self.tail(1.5)
