from manim import *
import numpy as np
import random

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GLD = "#FFFF00"; GRN = "#83C167"; DIM = "#2A2A3A"; AMB = "#FF9408"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)

def cap(s, sz=34, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).to_edge(UP, buff=0.5)


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


def make_dial():
    """Shortwave radio dial: arc scale + needle."""
    arc = Arc(radius=2.0, angle=PI*0.7, start_angle=PI*1.15, color=GRY, stroke_width=3)
    ticks = VGroup(*[
        Line(arc.point_from_proportion(p)*0.92, arc.point_from_proportion(p)*1.0,
             color=GRY, stroke_width=2)
        for p in np.linspace(0, 1, 9)
    ])
    needle = Line(ORIGIN, arc.point_from_proportion(0.5)*0.85, color=RED, stroke_width=4)
    hub = Dot(ORIGIN, radius=0.08, color=RED)
    freq = T("7,910 kHz", sz=26, c=GRY).move_to(DOWN*2.6)
    return VGroup(arc, ticks, needle, hub, freq), needle


def digit_wall(rows=5, cols=8):
    """Scrolling grid of random digits — the transmission."""
    grp = VGroup()
    for r in range(rows):
        for c in range(cols):
            d = T(str(random.randint(0,9)), sz=26, c=GRY)
            d.move_to(RIGHT*(c-cols/2+0.5)*0.75 + UP*(rows/2-r-0.5)*0.6)
            grp.add(d)
    return grp


class NumbersStation(S):
    ONSETS = [
        0.05,   #  0  "Right now,"
        0.87,   #  1  "a radio signal"
        1.78,   #  2  "hums on shortwave"
        2.80,   #  3  "that no government"
        3.93,   #  4  "has explained,"
        4.79,   #  5  "a flat voice"
        5.55,   #  6  "reading numbers,"
        6.37,   #  7  "over and over,"
        7.41,   #  8  "agents use it"
        8.29,   #  9  "to pass messages"
        9.12,   # 10  "with a cipher"
        9.76,   # 11  "that's mathematically unbreakable,"
        11.84,  # 12  "even with infinite"
        12.82,  # 13  "computing power,"
        13.89,  # 14  "it's called a one-time pad,"
        15.52,  # 15  "the only encryption ever"
        17.24,  # 16  "proven perfectly"
        18.06,  # 17  "secure."
        18.88,  # 18  "tune in"
        19.33,  # 19  "tonight,"
        19.71,  # 20  "you might"
        20.16,  # 21  "catch one live"
    ]

    def construct(self):
        self.setup()

        # ── 0 · "Right now," — the hook, first thing on screen, no setup ──
        hook = T("RIGHT NOW.", sz=64, c=RED, weight=BOLD)
        self.cue(0)
        self.P(FadeIn(hook, scale=1.15), rt=0.3)

        # ── 1 · "a radio signal" — dial appears ─────────────────────────────
        self.cue(1)
        self.P(FadeOut(hook), rt=0.2)
        dial, needle = make_dial()
        dial.move_to(UP*0.8)
        c1 = cap("a radio signal", sz=36, c=WHT)
        self.P(FadeIn(c1), rt=0.25)
        self.P(Create(dial), rt=0.4)

        # ── 2 · "hums on shortwave" — needle sweeps ─────────────────────────
        self.cue(2)
        self.P(FadeOut(c1), rt=0.2)
        c2 = cap("hums on shortwave", sz=36, c=WHT)
        self.P(FadeIn(c2), rt=0.25)
        self.P(Rotate(needle, angle=0.5, about_point=ORIGIN+UP*0.8), rt=0.5)

        # ── 3 · "that no government" ─────────────────────────────────────
        self.cue(3)
        self.P(FadeOut(c2), rt=0.2)
        c3 = cap("no government", sz=36, c=AMB, weight=BOLD)
        self.P(FadeIn(c3), rt=0.3)

        # ── 4 · "has explained," ─────────────────────────────────────────
        self.cue(4)
        c4 = T("has ever explained.", sz=32, c=GRY).next_to(c3, DOWN, buff=0.2)
        self.P(FadeIn(c4), rt=0.35)

        # ── 5 · "a flat voice" — clear dial, digit wall begins ──────────────
        self.cue(5)
        self.P(FadeOut(VGroup(c3, c4, dial)), rt=0.35)
        c5 = cap("a flat voice", sz=36, c=WHT)
        self.P(FadeIn(c5), rt=0.3)

        # ── 6 · "reading numbers," — digit wall appears ─────────────────────
        self.cue(6)
        self.P(FadeOut(c5), rt=0.2)
        wall = digit_wall()
        c6 = cap("reading numbers.", sz=36, c=WHT)
        self.P(FadeIn(c6), rt=0.25)
        self.P(LaggedStart(*[FadeIn(d) for d in wall], lag_ratio=0.01), rt=0.5)

        # ── 7 · "over and over," — digits shuffle to show endless repeat ────
        self.cue(7)
        self.P(FadeOut(c6), rt=0.2)
        c7 = cap("over and over.", sz=36, c=GRY)
        # shuffle a few digits to suggest ongoing transmission
        for d in random.sample(list(wall), 15):
            newd = T(str(random.randint(0,9)), sz=26, c=GRY).move_to(d)
            self.add(newd)
            self.remove(d)
        self.P(FadeIn(c7), rt=0.4)

        # ── 8 · "agents use it" ──────────────────────────────────────────
        self.cue(8)
        self.P(FadeOut(VGroup(c7, wall)), rt=0.35)
        c8 = cap("Agents use it", sz=38, c=WHT)
        self.P(FadeIn(c8), rt=0.3)

        # ── 9 · "to pass messages" ────────────────────────────────────────
        self.cue(9)
        self.P(FadeOut(c8), rt=0.2)
        c9 = cap("to pass messages", sz=38, c=WHT)
        self.P(FadeIn(c9), rt=0.3)

        # ── 10 · "with a cipher" ─────────────────────────────────────────
        self.cue(10)
        self.P(FadeOut(c9), rt=0.2)
        c10 = T("using a cipher that's", sz=38, c=WHT).move_to(UP*0.3)
        self.P(FadeIn(c10), rt=0.3)

        # ── 11 · "that's mathematically unbreakable," — lock appears ────────
        self.cue(11)
        self.P(FadeOut(c10), rt=0.25)
        unbr = T("MATHEMATICALLY", sz=42, c=RED, weight=BOLD).move_to(UP*1.0)
        unbr2 = T("UNBREAKABLE.", sz=52, c=RED, weight=BOLD).next_to(unbr, DOWN, buff=0.25)
        lock_shackle = Arc(radius=0.35, angle=PI, start_angle=0, color=GLD, stroke_width=6)
        lock_body = RoundedRectangle(width=1.0, height=0.8, corner_radius=0.1,
                                     fill_color="#15152A", fill_opacity=1,
                                     stroke_color=GLD, stroke_width=5)
        lock = VGroup(lock_shackle, lock_body).move_to(DOWN*1.3)
        lock_shackle.next_to(lock_body, UP, buff=-0.15)
        self.P(FadeIn(unbr, shift=DOWN*0.15), rt=0.35)
        self.P(FadeIn(unbr2, shift=DOWN*0.15), rt=0.35)
        self.P(FadeIn(lock, scale=1.2), rt=0.4)

        # ── 12 · "even with infinite" ─────────────────────────────────────
        self.cue(12)
        self.P(FadeOut(VGroup(unbr, unbr2)), rt=0.3)
        c12 = cap("Even with infinite", sz=36, c=WHT)
        self.P(FadeIn(c12), rt=0.3)

        # ── 13 · "computing power," — supercomputers fail against the lock ──
        self.cue(13)
        self.P(FadeOut(c12), rt=0.2)
        c13 = T("computing power.", sz=40, c=BLU, weight=BOLD).next_to(lock, UP, buff=1.0)
        # three small "computer" chips around the lock, all crossed out
        chips = VGroup(*[
            RoundedRectangle(width=0.5, height=0.35, corner_radius=0.05,
                             fill_color="#15152A", fill_opacity=1,
                             stroke_color=BLU, stroke_width=2)
            for _ in range(3)
        ])
        chips.arrange(RIGHT, buff=0.5).next_to(lock, DOWN, buff=0.5)
        crosses = VGroup(*[Cross(c, color=RED, stroke_width=3) for c in chips])
        self.P(FadeIn(c13), rt=0.35)
        self.P(FadeIn(chips), rt=0.3)
        self.P(LaggedStart(*[Create(x) for x in crosses], lag_ratio=0.15), rt=0.4)

        # ── 14 · "it's called a one-time pad," — the real math begins ───────
        self.cue(14)
        self.P(FadeOut(VGroup(c13, chips, crosses, lock)), rt=0.4)
        otp = T("ONE-TIME PAD", sz=52, c=GLD, weight=BOLD).to_edge(UP, buff=0.6)
        self.P(Write(otp), rt=0.5)

        # ── 15 · "the only encryption ever" — build the XOR math ────────────
        self.cue(15)
        msg = MathTex(r"\text{message: } 1011", font_size=34, color=WHT).move_to(UP*1.2)
        key = MathTex(r"\text{random key: } 0110", font_size=34, color=BLU).next_to(msg, DOWN, buff=0.35)
        self.P(FadeIn(msg, shift=DOWN*0.1), rt=0.4)
        self.P(FadeIn(key, shift=DOWN*0.1), rt=0.4)

        # ── 16 · "proven perfectly" — XOR resolves to ciphertext ────────────
        self.cue(16)
        xor_line = Line(msg.get_left()+LEFT*0.1+DOWN*0.05, key.get_right()+RIGHT*3.2+DOWN*0.05,
                        color=GRY, stroke_width=1.5).next_to(key, DOWN, buff=0.25)
        cipher = MathTex(r"\text{sent: } 1101", font_size=34, color=RED).next_to(xor_line, DOWN, buff=0.25)
        self.P(Create(xor_line), rt=0.3)
        self.P(Write(cipher), rt=0.45)

        # ── 17 · "secure." — perfect secrecy checkmark ──────────────────────
        self.cue(17)
        sec = T("perfectly secure.", sz=44, c=GRN, weight=BOLD).next_to(cipher, DOWN, buff=0.5)
        check = T("✓", sz=56, c=GRN).next_to(sec, RIGHT, buff=0.3)
        self.P(FadeIn(sec, shift=DOWN*0.1), rt=0.35)
        self.P(FadeIn(check, scale=1.3), rt=0.3)

        # ── 18 · "tune in" — clear to closing dial ──────────────────────────
        self.cue(18)
        self.P(FadeOut(VGroup(otp, msg, key, xor_line, cipher, sec, check)), rt=0.4)
        dial2, needle2 = make_dial()
        dial2.move_to(UP*0.6)
        c18 = T("Tune in", sz=48, c=WHT).next_to(dial2, DOWN, buff=0.6)
        self.P(FadeIn(dial2), rt=0.35)
        self.P(FadeIn(c18, shift=DOWN*0.1), rt=0.3)

        # ── 19 · "tonight," ──────────────────────────────────────────────
        self.cue(19)
        c19 = T("tonight.", sz=56, c=GLD, weight=BOLD).next_to(c18, RIGHT, buff=0.25)
        self.P(Write(c19), rt=0.35)

        # ── 20 · "you might" — LIVE indicator pulses ────────────────────────
        self.cue(20)
        live_dot = Dot(dial2.get_top()+UP*0.3, radius=0.09, color=RED)
        live_lbl = T("LIVE", sz=22, c=RED, weight=BOLD).next_to(live_dot, RIGHT, buff=0.15)
        self.P(FadeIn(VGroup(live_dot, live_lbl), scale=1.3), rt=0.3)

        # ── 21 · "catch one live" ────────────────────────────────────────
        self.cue(21)
        self.P(FadeOut(VGroup(c18, c19)), rt=0.25)
        final = T("You might catch one.", sz=44, c=WHT).next_to(dial2, DOWN, buff=0.6)
        self.P(FadeIn(final, shift=DOWN*0.1), rt=0.4)

        self.tail(1.0)
