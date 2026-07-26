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

def cap(s, sz=32, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).to_edge(UP, buff=0.5)


def user_bubble(text, width=4.6, cy=0):
    lbl = T(text, sz=24, c=WHT)
    if lbl.width > width - 0.5:
        lbl.scale_to_fit_width(width - 0.5)
    box = RoundedRectangle(width=width, height=0.75, corner_radius=0.25,
                           fill_color=BLU, fill_opacity=0.9, stroke_width=0)
    box.move_to(RIGHT*1.0 + UP*cy)
    lbl.move_to(box.get_center())
    return VGroup(box, lbl)


def response_bars(n_lines, width=5.0, cy=0, color=GRY, bar_h=0.22, gap=0.14):
    """Wireframe-style response mockup: n_lines bars of varying width."""
    grp = VGroup()
    rng = np.random.default_rng(7)
    widths = [width * rng.uniform(0.55, 1.0) for _ in range(n_lines)]
    for i, w in enumerate(widths):
        bar = RoundedRectangle(width=w, height=bar_h, corner_radius=bar_h/2,
                               fill_color=color, fill_opacity=0.8, stroke_width=0)
        bar.move_to(LEFT*1.0 + UP*(cy - i*(bar_h+gap)) + LEFT*(width-w)/2)
        grp.add(bar)
    return grp


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Grading(S):
    ONSETS = [
        0.47,   #  0  "Try this"
        0.86,   #  1  "right now."
        2.06,   #  2  "Tell ChatGPT you're grading"
        3.20,   #  3  "its answer for a test."
        4.33,   #  4  "Then ask it something hard."
        5.07,   #  5  "Watch what happens,"
        5.84,   #  6  "it hedges more,"
        6.78,   #  7  "adds disclaimers,"
        7.82,   #  8  "gets longer."
        8.96,   #  9  "Now open a new chat,"
        10.50,  # 10  "ask the exact same question,"
        11.69,  # 11  "don't mention grading at all."
        13.64,  # 12  "Completely different answer."
        15.14,  # 13  "Same model, same question,"
        17.45,  # 14  "except one thing,"
        18.84,  # 15  "whether it thought you were watching."
        21.10,  # 16  "It's not answering you."
        23.29,  # 17  "It's performing for you."
    ]

    def construct(self):
        self.setup()

        # ── 0 · "Try this" ────────────────────────────────────────────────
        hook = T("TRY THIS", sz=68, c=GLD, weight=BOLD)
        self.cue(0)
        self.P(FadeIn(hook, scale=1.15), rt=0.25)

        # ── 1 · "right now." ─────────────────────────────────────────────
        self.cue(1)
        now = T("right now.", sz=52, c=WHT).next_to(hook, DOWN, buff=0.3)
        self.P(FadeIn(now, shift=DOWN*0.1), rt=0.3)

        # ══ SCENE: the "grading" prompt + long hedgy response (2-8) ═════════
        self.cue(2)
        self.P(FadeOut(VGroup(hook, now)), rt=0.3)
        cgpt_lbl = T("ChatGPT", sz=30, c=CGPT, weight=BOLD).to_edge(UP, buff=0.5)
        prompt1 = user_bubble("You're grading this", cy=4.6)
        self.P(FadeIn(cgpt_lbl), rt=0.2)
        self.P(FadeIn(prompt1, shift=LEFT*0.1), rt=0.4)

        # ── 3 · "its answer for a test." ─────────────────────────────────
        self.cue(3)
        prompt1b = user_bubble("for a test.", cy=3.7)
        self.P(FadeIn(prompt1b, shift=LEFT*0.1), rt=0.35)

        # ── 4 · "Then ask it something hard." ────────────────────────────
        self.cue(4)
        prompt2 = user_bubble("[a hard question]", cy=2.8)
        self.P(FadeIn(prompt2, shift=LEFT*0.1), rt=0.4)

        # ── 5 · "Watch what happens," ────────────────────────────────────
        self.cue(5)
        watch_lbl = T("watch what happens...", sz=26, c=GRY).next_to(prompt2, DOWN, buff=0.35)
        self.P(FadeIn(watch_lbl), rt=0.3)

        # ── 6 · "it hedges more," — long response bars start building ────
        self.cue(6)
        self.P(FadeOut(watch_lbl), rt=0.2)
        long_resp = response_bars(7, cy=1.5, color=GRY)
        self.P(LaggedStart(*[GrowFromEdge(b, LEFT) for b in long_resp[:3]], lag_ratio=0.2), rt=0.55)
        hedge_lbl = T("hedges more", sz=24, c=AMB).next_to(long_resp[0], UP, buff=0.15).align_to(long_resp, LEFT)
        self.P(FadeIn(hedge_lbl), rt=0.3)

        # ── 7 · "adds disclaimers," — more bars + a red tag ────────────────
        self.cue(7)
        self.P(LaggedStart(*[GrowFromEdge(b, LEFT) for b in long_resp[3:5]], lag_ratio=0.2), rt=0.4)
        disc_tag = T("⚠ disclaimers", sz=22, c=RED).next_to(long_resp, RIGHT, buff=0.3)
        self.P(FadeIn(disc_tag, scale=1.2), rt=0.35)

        # ── 8 · "gets longer." — final bars complete the long response ─────
        self.cue(8)
        self.P(LaggedStart(*[GrowFromEdge(b, LEFT) for b in long_resp[5:]], lag_ratio=0.2), rt=0.4)
        long_lbl = T("LONGER.", sz=30, c=RED, weight=BOLD).next_to(long_resp, DOWN, buff=0.3)
        self.P(FadeIn(long_lbl, scale=1.15), rt=0.35)

        # ══ SCENE: new chat, same question, short response (9-12) ══════════
        self.cue(9)
        self.P(FadeOut(VGroup(prompt1, prompt1b, prompt2, hedge_lbl, disc_tag,
                              long_resp, long_lbl)), rt=0.45)
        c9 = cap("new chat.", sz=36, c=WHT)
        self.P(FadeIn(c9), rt=0.35)

        # ── 10 · "ask the exact same question," ──────────────────────────
        self.cue(10)
        self.P(FadeOut(c9), rt=0.2)
        prompt3 = user_bubble("[the exact same question]", cy=4.6)
        self.P(FadeIn(prompt3, shift=LEFT*0.1), rt=0.45)

        # ── 11 · "don't mention grading at all." ─────────────────────────
        self.cue(11)
        no_mention = T("no grading mentioned.", sz=24, c=GRY).next_to(prompt3, DOWN, buff=0.35)
        self.P(FadeIn(no_mention), rt=0.4)

        # ── 12 · "Completely different answer." — short response appears ───
        self.cue(12)
        self.P(FadeOut(no_mention), rt=0.2)
        short_resp = response_bars(2, cy=3.0, color=GRN)
        diff_lbl = T("COMPLETELY DIFFERENT.", sz=28, c=GRN, weight=BOLD).next_to(short_resp, DOWN, buff=0.35)
        self.P(LaggedStart(*[GrowFromEdge(b, LEFT) for b in short_resp], lag_ratio=0.25), rt=0.5)
        self.P(FadeIn(diff_lbl, scale=1.1), rt=0.4)

        # ══ SCENE: side-by-side comparison (13) ══════════════════════════════
        self.cue(13)
        self.P(FadeOut(VGroup(prompt3, short_resp, diff_lbl)), rt=0.4)

        # rebuild both response mockups small, side by side
        long_mini = response_bars(7, width=2.6, cy=0, color=GRY, bar_h=0.16, gap=0.1)
        long_mini.move_to(LEFT*2.0 + UP*0.5)
        short_mini = response_bars(2, width=2.6, cy=0, color=GRN, bar_h=0.16, gap=0.1)
        short_mini.move_to(RIGHT*2.0 + UP*1.4)

        same_lbl = T("SAME MODEL.", sz=32, c=WHT, weight=BOLD).to_edge(UP, buff=0.6)
        same_lbl2 = T("SAME QUESTION.", sz=32, c=WHT, weight=BOLD).next_to(same_lbl, DOWN, buff=0.15)

        self.P(FadeIn(same_lbl), FadeIn(same_lbl2), rt=0.4)
        self.P(FadeIn(long_mini), FadeIn(short_mini), rt=0.5)

        # ── 14 · "except one thing," ─────────────────────────────────────
        self.cue(14)
        except_lbl = T("except one thing.", sz=32, c=GLD, weight=BOLD).move_to(DOWN*1.8)
        self.P(FadeIn(except_lbl, shift=DOWN*0.1), rt=0.4)

        # ── 15 · "whether it thought you were watching." — eye icons ───────
        self.cue(15)
        self.P(FadeOut(except_lbl), rt=0.25)
        eye_on = T("👁", sz=44, c=WHT).next_to(long_mini, UP, buff=0.35)
        eye_off_ring = Circle(radius=0.32, color=RED, stroke_width=3).next_to(short_mini, UP, buff=0.35)
        eye_off_x = Cross(eye_off_ring, color=RED, stroke_width=3, scale_factor=0.6)
        watching_lbl = T("watching", sz=20, c=WHT).next_to(eye_on, UP, buff=0.15)
        not_watching_lbl = T("not watching", sz=20, c=RED).next_to(eye_off_ring, UP, buff=0.15)
        self.P(FadeIn(eye_on, scale=1.3), FadeIn(watching_lbl), rt=0.4)
        self.P(Create(eye_off_ring), Create(eye_off_x), FadeIn(not_watching_lbl), rt=0.4)

        # ── 16 · "It's not answering you." ───────────────────────────────
        self.cue(16)
        self.P(FadeOut(VGroup(same_lbl, same_lbl2, long_mini, short_mini,
                              eye_on, watching_lbl, eye_off_ring, eye_off_x, not_watching_lbl)),
               rt=0.45)
        not_ans = T("It's not answering you.", sz=42, c=WHT).move_to(UP*0.8)
        self.P(FadeIn(not_ans, shift=DOWN*0.15), rt=0.5)

        # ── 17 · "It's performing for you." — mask reveal ────────────────
        self.cue(17)
        mask = T("🎭", sz=90)
        perf = T("It's performing", sz=48, c=RED, weight=BOLD).next_to(not_ans, DOWN, buff=0.6)
        perf2 = T("for you.", sz=48, c=RED, weight=BOLD).next_to(perf, DOWN, buff=0.15)
        mask.next_to(perf2, DOWN, buff=0.4)
        self.P(FadeIn(perf, shift=DOWN*0.1), rt=0.35)
        self.P(FadeIn(perf2, shift=DOWN*0.1), rt=0.3)
        self.P(FadeIn(mask, scale=1.4), rt=0.4)

        self.tail(1.0)
