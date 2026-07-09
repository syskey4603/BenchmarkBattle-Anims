# riemann_short.py — "Quietly hoping nobody gets there first." — 32.6 s
from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GLD = "#FFFF00"; GRN = "#83C167"; DIM = "#2A2A3A"; AMB = "#FF9408"
PRP = "#B47FFF"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)

def cap(s, sz=32, c=WHT, **kw):
    """Caption strip — sits at top edge, never fights the visual below."""
    return Text(s, font_size=sz, color=c, **kw).to_edge(UP, buff=0.5)


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


# ── reusable visual builders ─────────────────────────────────────────────────

def make_number_line(lo=1, hi=30, width=6.4):
    """A number line with prime positions marked as highlighted dots."""
    primes = {2,3,5,7,11,13,17,19,23,29}
    line = Line(LEFT * width/2, RIGHT * width/2, color=GRY, stroke_width=2)
    ticks = VGroup()
    dots = VGroup()
    for n in range(lo, hi+1):
        x = -width/2 + (n - lo) / (hi - lo) * width
        tick = Line([x, -0.06, 0], [x, 0.06, 0], color=GRY, stroke_width=1.5)
        ticks.add(tick)
        if n in primes:
            d = Dot([x, 0, 0], radius=0.075, color=GLD, z_index=2)
            dots.add(d)
    return VGroup(line, ticks), dots


def make_padlock(color=BLU, scale=1.0):
    shackle = Arc(radius=0.42, angle=PI, start_angle=0, color=color, stroke_width=6)
    shackle.move_to(UP * 0.42)
    body = RoundedRectangle(width=1.15, height=0.9, corner_radius=0.1,
                            fill_color="#15152A", fill_opacity=1,
                            stroke_color=color, stroke_width=4)
    keyhole = Circle(radius=0.09, fill_color=color, fill_opacity=1, stroke_width=0)
    keyhole.move_to(body.get_center() + UP * 0.08)
    slot = Rectangle(width=0.06, height=0.16, fill_color=color, fill_opacity=1,
                     stroke_width=0).next_to(keyhole, DOWN, buff=0.0)
    return VGroup(shackle, body, keyhole, slot).scale(scale)


def make_critical_strip():
    """Complex-plane strip 0<Re<1, with the critical line at Re=1/2,
    and 'zeros' as gold dots landing exactly on that line."""
    strip = Rectangle(width=2.4, height=5.2, fill_color="#22223A",
                      fill_opacity=0.5, stroke_color=GRY, stroke_width=1.5)
    left_edge  = Line(strip.get_corner(UL), strip.get_corner(DL), color=RED, stroke_width=2.5)
    right_edge = Line(strip.get_corner(UR), strip.get_corner(DR), color=RED, stroke_width=2.5)
    crit_line  = Line(strip.get_top(), strip.get_bottom(), color=GLD, stroke_width=3)

    lbl0   = T("Re=0", sz=18, c=RED).next_to(left_edge, LEFT, buff=0.12)
    lbl1   = T("Re=1", sz=18, c=RED).next_to(right_edge, RIGHT, buff=0.12)
    lblhalf = T("Re=1/2", sz=18, c=GLD).next_to(crit_line, UP, buff=0.15)

    # zero positions along the critical line (illustrative heights)
    heights = [-1.9, -1.2, -0.5, 0.3, 1.0, 1.7]
    zeros = VGroup(*[
        Dot(crit_line.point_from_proportion((h + 2.2) / 4.4), radius=0.07, color=GLD, z_index=3)
        for h in heights
    ])
    return VGroup(strip, left_edge, right_edge, crit_line, lbl0, lbl1, lblhalf), zeros


class Riemann(S):
    ONSETS = [
        0.08,   #  0  "There's a $1,000,000 prize"
        1.79,   #  1  "that's sat unclaimed for 25 years."
        4.13,   #  2  "The Riemann Hypothesis."
        5.75,   #  3  "A 165-year-old question"
        7.52,   #  4  "about exactly where prime numbers hide."
        11.09,  #  5  "Here's the part nobody tells you:"
        12.88,  #  6  "the encryption protecting your bank,"
        14.33,  #  7  "your messages,"
        14.93,  #  8  "your passwords —"
        16.72,  #  9  "all of it —"
        17.33,  # 10  "relies on primes being unpredictable."
        19.36,  # 11  "A full proof wouldn't hand anyone your password."
        22.08,  # 12  "But it would tell us more about primes"
        23.31,  # 13  "than we've ever known —"
        24.19,  # 14  "and some cryptographers worry"
        24.55,  # 15  "that certainty could be the first crack in the wall."
        27.23,  # 16  "The math world has wanted this solved"
        28.56,  # 17  "for over a century."
        30.05,  # 18  "Part of the security world"
        30.81,  # 19  "is quietly hoping nobody gets there first."
    ]

    def construct(self):
        self.setup()

        # ── 0 · "$1,000,000 prize" ────────────────────────────────────────
        cash = T("$1,000,000", sz=72, c=GLD, weight=BOLD).move_to(UP * 0.6)
        prize_lbl = T("PRIZE", sz=40, c=WHT).next_to(cash, DOWN, buff=0.3)
        self.cue(0)
        self.P(Write(cash), rt=0.5)
        self.P(FadeIn(prize_lbl, shift=DOWN * 0.15), rt=0.35)

        # ── 1 · "unclaimed for 25 years." ──────────────────────────────────
        self.cue(1)
        stamp_lbl = T("UNCLAIMED", sz=36, c=RED, weight=BOLD)
        stamp_box = SurroundingRectangle(stamp_lbl, buff=0.2, color=RED, stroke_width=3)
        stamp = VGroup(stamp_box, stamp_lbl).rotate(0.12).next_to(prize_lbl, DOWN, buff=0.5)
        yrs = T("25 years.", sz=30, c=GRY).next_to(stamp, DOWN, buff=0.35)
        self.P(FadeIn(stamp, scale=1.3), rt=0.4)
        self.P(FadeIn(yrs), rt=0.35)

        # ── 2 · "The Riemann Hypothesis." ───────────────────────────────────
        self.cue(2)
        self.P(FadeOut(VGroup(cash, prize_lbl, stamp, yrs)), rt=0.4)
        rh = T("The Riemann", sz=58).move_to(UP * 0.7)
        rh2 = T("Hypothesis.", sz=64, c=PRP, weight=BOLD).next_to(rh, DOWN, buff=0.3)
        self.P(FadeIn(rh, shift=DOWN * 0.15), rt=0.4)
        self.P(Write(rh2), rt=0.5)

        # ── 3 · "A 165-year-old question" ───────────────────────────────────
        self.cue(3)
        self.P(FadeOut(VGroup(rh, rh2)), rt=0.35)
        yr1 = T("1859", sz=52, c=GRY).move_to(LEFT * 1.7 + UP * 0.6)
        arrow_yr = Arrow(LEFT * 0.6, RIGHT * 0.6, color=GRY, stroke_width=2.5,
                         max_tip_length_to_length_ratio=0.2).move_to(UP * 0.6)
        yr2 = T("today", sz=52, c=WHT).move_to(RIGHT * 1.9 + UP * 0.6)
        age = T("165 years unsolved.", sz=34, c=RED, weight=BOLD).move_to(DOWN * 0.6)
        self.P(FadeIn(yr1), rt=0.35)
        self.P(GrowArrow(arrow_yr), rt=0.3)
        self.P(FadeIn(yr2), rt=0.35)
        self.P(FadeIn(age, shift=DOWN * 0.15), rt=0.4)

        # ── 4 · "where prime numbers hide." — number line reveal ─────────────
        self.cue(4)
        self.P(FadeOut(VGroup(yr1, arrow_yr, yr2, age)), rt=0.4)
        c4 = cap("Where do primes hide?", sz=34, c=WHT)
        nline, pdots = make_number_line()
        nline_grp = VGroup(nline, pdots).move_to(UP * 0.3)

        self.P(FadeIn(c4), rt=0.35)
        self.P(Create(nline), rt=0.5)
        self.P(LaggedStart(*[GrowFromCenter(d) for d in pdots], lag_ratio=0.12), rt=1.1)
        scatter_lbl = T("They look random.", sz=30, c=GRY).next_to(nline_grp, DOWN, buff=0.5)
        self.P(FadeIn(scatter_lbl), rt=0.35)

        # ── 5 · "Here's the part nobody tells you:" ──────────────────────────
        self.cue(5)
        self.P(FadeOut(VGroup(c4, nline_grp, scatter_lbl)), rt=0.4)
        nb = cap("Here's the part", sz=36, c=WHT)
        nb2 = T("nobody tells you:", sz=40, c=GLD, weight=BOLD).next_to(nb, DOWN, buff=0.25)
        self.P(FadeIn(nb), rt=0.35)
        self.P(FadeIn(nb2), rt=0.4)

        # ── 6 · "encryption protecting your bank," — lock appears ───────────
        self.cue(6)
        self.P(FadeOut(VGroup(nb, nb2)), rt=0.35)
        c6 = cap("Protects your bank", sz=32, c=WHT)
        lock = make_padlock(color=BLU, scale=1.6).move_to(DOWN * 0.4)
        self.P(FadeIn(c6), rt=0.3)
        self.P(FadeIn(lock, shift=DOWN * 0.2), rt=0.45)

        # ── 7 · "your messages," — icon appears beside lock ─────────────────
        self.cue(7)
        self.P(FadeOut(c6), rt=0.2)
        c7 = cap("your messages", sz=32, c=WHT)
        env = VGroup(
            Rectangle(width=0.7, height=0.5, fill_color="#15152A", fill_opacity=1,
                     stroke_color=GRN, stroke_width=2.5),
        )
        env_flap = Line(env[0].get_corner(UL), env[0].get_center(), color=GRN, stroke_width=2)
        env_flap2 = Line(env[0].get_corner(UR), env[0].get_center(), color=GRN, stroke_width=2)
        envelope = VGroup(env, env_flap, env_flap2).next_to(lock, LEFT, buff=0.7)
        self.P(FadeIn(c7), rt=0.25)
        self.P(FadeIn(envelope, shift=RIGHT * 0.15), rt=0.3)

        # ── 8 · "your passwords —" — key icon appears other side ────────────
        self.cue(8)
        self.P(FadeOut(c7), rt=0.2)
        c8 = cap("your passwords", sz=32, c=WHT)
        key_circ = Circle(radius=0.18, color=AMB, stroke_width=3).move_to(RIGHT * 0.0)
        key_stem = Line(ORIGIN, RIGHT * 0.45, color=AMB, stroke_width=4)
        key_stem.next_to(key_circ, RIGHT, buff=-0.05)
        key_teeth = VGroup(
            Line(key_stem.get_end(), key_stem.get_end() + DOWN * 0.12, color=AMB, stroke_width=4),
            Line(key_stem.get_end() + LEFT * 0.12, key_stem.get_end() + LEFT * 0.12 + DOWN * 0.09,
                color=AMB, stroke_width=4),
        )
        key = VGroup(key_circ, key_stem, key_teeth).next_to(lock, RIGHT, buff=0.7)
        self.P(FadeIn(c8), rt=0.3)
        self.P(FadeIn(key, shift=LEFT * 0.15), rt=0.35)

        # ── 9 · "all of it —" ────────────────────────────────────────────────
        self.cue(9)
        self.P(FadeOut(c8), rt=0.2)
        c9 = cap("ALL of it.", sz=38, c=RED, weight=BOLD)
        self.P(FadeIn(c9), rt=0.35)

        # ── 10 · "relies on primes being unpredictable." — RSA math appears ──
        self.cue(10)
        self.P(FadeOut(VGroup(c9, envelope, key)), rt=0.35)
        self.P(lock.animate.scale(0.7).move_to(UP * 2.0), rt=0.35)

        c10 = cap("Relies on primes", sz=32, c=WHT)
        c10b = T("being unpredictable.", sz=30, c=RED, weight=BOLD).next_to(c10, DOWN, buff=0.2)

        rsa = MathTex(r"p \times q = N", font_size=52, color=WHT).move_to(DOWN * 0.8)
        p_lbl = T("huge prime", sz=20, c=GLD).next_to(rsa[0][0], DOWN, buff=0.35)
        q_lbl = T("huge prime", sz=20, c=GLD).next_to(rsa[0][2], DOWN, buff=0.35)

        self.P(FadeIn(c10), rt=0.3)
        self.P(FadeIn(c10b), rt=0.3)
        self.P(Write(rsa), rt=0.5)
        self.P(FadeIn(p_lbl), FadeIn(q_lbl), rt=0.35)

        # ── 11 · "wouldn't hand anyone your password." ───────────────────────
        self.cue(11)
        self.P(FadeOut(VGroup(c10, c10b)), rt=0.3)
        c11 = cap("Wouldn't hand anyone", sz=32, c=WHT)
        c11b = T("your password.", sz=34, c=GRN, weight=BOLD).next_to(c11, DOWN, buff=0.2)
        self.P(FadeIn(c11), rt=0.35)
        self.P(FadeIn(c11b), rt=0.4)
        # lock stays closed/safe — small green check
        check = T("✓", sz=36, c=GRN).next_to(lock, RIGHT, buff=0.3)
        self.P(FadeIn(check, scale=1.4), rt=0.3)

        # ── 12 · "tell us more about primes" — zeta critical strip appears ──
        self.cue(12)
        self.P(FadeOut(VGroup(c11, c11b, check, rsa, p_lbl, q_lbl, lock)), rt=0.45)
        c12 = cap("But it would reveal", sz=32, c=WHT)
        strip_grp, zeros = make_critical_strip()
        whole_strip = VGroup(strip_grp, zeros).move_to(DOWN * 0.3)
        self.P(FadeIn(c12), rt=0.35)
        self.P(FadeIn(strip_grp), rt=0.5)

        # ── 13 · "than we've ever known —" — zeros land on the line ─────────
        self.cue(13)
        self.P(FadeOut(c12), rt=0.2)
        c13 = cap("more about primes", sz=32, c=WHT)
        self.P(FadeIn(c13), rt=0.3)
        self.P(LaggedStart(*[GrowFromCenter(z) for z in zeros], lag_ratio=0.15), rt=0.7)

        # ── 14 · "and some cryptographers worry" ────────────────────────────
        self.cue(14)
        self.P(FadeOut(c13), rt=0.2)
        c14 = cap("Some cryptographers worry:", sz=30, c=AMB, weight=BOLD)
        self.P(FadeIn(c14), rt=0.3)

        # ── 15 · "certainty could be the first crack in the wall." ──────────
        self.cue(15)
        self.P(FadeOut(VGroup(c14, strip_grp, zeros)), rt=0.4)
        lock2 = make_padlock(color=RED, scale=1.8).move_to(DOWN * 0.2)
        self.P(FadeIn(lock2), rt=0.4)
        crack1 = Line(lock2.get_top() + LEFT * 0.15, lock2.get_center() + RIGHT * 0.1,
                     color=RED, stroke_width=3)
        crack2 = Line(lock2.get_center() + RIGHT * 0.1, lock2.get_bottom() + LEFT * 0.05,
                     color=RED, stroke_width=3)
        crack_lbl = T("the first crack.", sz=32, c=RED, weight=BOLD).next_to(lock2, DOWN, buff=0.4)
        self.P(Create(crack1), rt=0.35)
        self.P(Create(crack2), rt=0.35)
        self.P(FadeIn(crack_lbl), rt=0.35)

        # ── 16 · "math world has wanted this solved" ────────────────────────
        self.cue(16)
        self.P(FadeOut(VGroup(lock2, crack1, crack2, crack_lbl)), rt=0.4)
        m1 = T("The math world", sz=48).move_to(UP * 0.6)
        m2 = T("wants it solved.", sz=52, c=BLU, weight=BOLD).next_to(m1, DOWN, buff=0.3)
        self.P(FadeIn(m1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(m2, shift=DOWN * 0.15), rt=0.4)

        # ── 17 · "for over a century." ───────────────────────────────────────
        self.cue(17)
        cent = T("For over a century.", sz=34, c=GRY).next_to(m2, DOWN, buff=0.4)
        self.P(FadeIn(cent), rt=0.4)

        # ── 18 · "Part of the security world" ────────────────────────────────
        self.cue(18)
        self.P(FadeOut(VGroup(m1, m2, cent)), rt=0.4)
        sw1 = T("Part of the", sz=48).move_to(UP * 0.9)
        sw2 = T("security world", sz=52, c=RED, weight=BOLD).next_to(sw1, DOWN, buff=0.3)
        self.P(FadeIn(sw1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(sw2, shift=DOWN * 0.15), rt=0.4)

        # ── 19 · "is quietly hoping nobody gets there first." ────────────────
        self.cue(19)
        sw3 = T("is quietly hoping", sz=40, c=GRY).next_to(sw2, DOWN, buff=0.4)
        sw4 = T("nobody gets there first.", sz=40, c=GRY).next_to(sw3, DOWN, buff=0.2)
        self.P(FadeIn(sw3, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(sw4, shift=DOWN * 0.15), rt=0.45)

        self.tail(1.0)
