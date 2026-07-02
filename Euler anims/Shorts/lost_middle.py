# lost_middle.py — "Lost in the Middle" short, portrait 1080×1920, 55 s
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


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


def make_u_axes():
    """U-shaped attention curve: parabola high at ends, low in middle."""
    ax = Axes(
        x_range=[0, 1, 0.5], y_range=[0, 1, 0.5],
        x_length=7.0, y_length=3.4,
        axis_config={"include_tip": False, "color": GRY, "stroke_width": 1.5},
        x_axis_config={"include_numbers": False},
        y_axis_config={"include_numbers": False},
    ).move_to(DOWN * 0.4)

    # True parabola: high at x=0 and x=1, minimum at x=0.5
    u = lambda x: 4 * (x - 0.5) ** 2 * 0.88 + 0.06
    curve = ax.plot(u, x_range=[0.01, 0.99, 0.004], color=BLU, stroke_width=3.5)

    area_l = ax.get_area(curve, x_range=[0.01, 0.26], color=GRN, opacity=0.45)
    area_m = ax.get_area(curve, x_range=[0.26, 0.74], color=RED, opacity=0.38)
    area_r = ax.get_area(curve, x_range=[0.74, 0.99], color=GRN, opacity=0.45)

    lbl_s = T("START",  sz=30, c=GRN).next_to(ax.x_axis.n2p(0.0), DOWN, buff=0.28)
    lbl_m = T("MIDDLE", sz=30, c=RED).next_to(ax.x_axis.n2p(0.5), DOWN, buff=0.28)
    lbl_e = T("END",    sz=30, c=GRN).next_to(ax.x_axis.n2p(1.0), DOWN, buff=0.28)
    lbl_y = T("attention", sz=22, c=GRY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.28)

    return ax, curve, area_l, area_m, area_r, lbl_s, lbl_m, lbl_e, lbl_y


def make_prompt_blocks():
    """Word-block grid coloured by attention zone (9 rows × 7 cols)."""
    rows, cols, bw, bh, gx, gy = 9, 7, 0.70, 0.22, 0.10, 0.10
    grp = VGroup()
    for r in range(rows):
        col, op = (GRN, 0.80) if (r < 2 or r > 6) else (DIM, 0.22)
        for c in range(cols):
            rect = Rectangle(width=bw, height=bh,
                             fill_color=col, fill_opacity=op, stroke_width=0)
            rect.move_to(RIGHT * c * (bw + gx) + DOWN * r * (bh + gy))
            grp.add(rect)
    grp.center()
    return grp


class LostInMiddle(S):
    # Onsets from pocketsphinx continuous decoder — absolute word timestamps
    ONSETS = [
        0.15,   #  0  "The longer your ChatGPT prompt, the less of it gets read."
        3.51,   #  1  "Not a metaphor."
        4.68,   #  2  "The math."
        6.03,   #  3  "When a transformer processes your message,"
        7.90,   #  4  "it computes an attention score for every token — every word."
        11.62,  #  5  "Those scores have to sum to one."
        13.42,  #  6  "Just like softmax."
        15.01,  #  7  "But they don't distribute evenly."
        16.44,  #  8  "They form a U-shape."
        17.95,  #  9  "First sentence: high attention."
        19.83,  # 10  "Last sentence: high attention."
        21.80,  # 11  "Everything in the middle? Starved."
        24.54,  # 12  "Stanford measured it."
        25.91,  # 13  "When the answer was placed in the middle of a long context,"
        29.82,  # 14  "accuracy dropped thirty percent."
        31.85,  # 15  "Same information. Same model."
        33.71,  # 16  "Just moved to the middle."
        35.00,  # 17  "This isn't a bug."
        36.14,  # 18  "It's attention sinks — architecture routes probability mass away from middle tokens."
        41.58,  # 19  "So if you write a 500-word prompt with your key instruction buried in paragraph three,"
        46.08,  # 20  "the model mathematically underweights it."
        48.31,  # 21  "Most important thing you need ChatGPT to do?"
        51.36,  # 22  "First sentence or last sentence."
        52.46,  # 23  "Never the middle."
        53.10,  # 24  "The middle is where your instructions go to die."
    ]

    def construct(self):
        self.setup()

        # ── 0 · hook ────────────────────────────────────────────────────────
        cgpt = T("ChatGPT", sz=60, c=CGPT, weight=BOLD).move_to(UP * 2.2)
        h1   = T("The longer your prompt,",   sz=44).move_to(UP * 0.6)
        h2   = T("the less gets read.",        sz=44, c=RED).next_to(h1, DOWN, buff=0.28)

        self.cue(0)
        self.P(FadeIn(cgpt, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(h1,   shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(h2,   shift=DOWN * 0.15), rt=0.35)

        # ── 1 · "Not a metaphor." ────────────────────────────────────────────
        self.cue(1)
        self.P(FadeOut(VGroup(cgpt, h1, h2)), rt=0.3)
        nm = T("Not a metaphor.", sz=60).move_to(UP * 0.5)
        self.P(FadeIn(nm, shift=DOWN * 0.15), rt=0.4)

        # ── 2 · "The math." ──────────────────────────────────────────────────
        self.cue(2)
        self.P(FadeOut(nm), rt=0.25)
        tm1 = T("The",   sz=60).move_to(UP * 0.9)
        tm2 = T("math.", sz=84, c=GLD, weight=BOLD).next_to(tm1, DOWN, buff=0.28)
        self.P(FadeIn(tm1,  shift=DOWN * 0.15), rt=0.35)
        self.P(Write(tm2),                      rt=0.45)

        # ── 3 · "When a transformer processes your message," ─────────────────
        self.cue(3)
        self.P(FadeOut(VGroup(tm1, tm2)), rt=0.3)
        w3a = T("When a transformer",     sz=44).move_to(UP * 5.5)
        w3b = T("processes your message,", sz=40, c=GRY).next_to(w3a, DOWN, buff=0.2)
        self.P(FadeIn(w3a, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(w3b, shift=DOWN * 0.15), rt=0.30)

        # ── 4 · "…attention score for every token" + formula ─────────────────
        self.cue(4)
        w4a = T("it computes",          sz=44).move_to(UP * 4.2)
        w4b = T("an attention score",   sz=44, c=BLU).next_to(w4a, DOWN, buff=0.2)
        w4c = T("for every token.",     sz=40, c=GRY).next_to(w4b, DOWN, buff=0.18)
        score_eq = MathTex(
            r"\alpha_i = \frac{e^{\,q\cdot k_i/\sqrt{d}}}{\displaystyle\sum_j e^{\,q\cdot k_j/\sqrt{d}}}",
            font_size=48, color=WHT
        ).move_to(DOWN * 1.2)
        self.P(FadeIn(w4a, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(w4b, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(w4c, shift=DOWN * 0.15), rt=0.30)
        self.P(Write(score_eq), rt=0.65)

        # ── 5 · "Those scores have to sum to one." ───────────────────────────
        self.cue(5)
        self.P(FadeOut(VGroup(w3a, w3b, w4a, w4b, w4c)), rt=0.25)
        sum_hdr = T("Those scores must sum to:", sz=38, c=GRY).move_to(UP * 5.4)
        sum_eq  = MathTex(r"\sum_i \alpha_i \;=\; 1.0",
                          font_size=60, color=GLD).move_to(UP * 4.0)
        self.P(FadeIn(sum_hdr, shift=DOWN * 0.15), rt=0.4)
        self.P(Write(sum_eq),                       rt=0.5)

        # ── 6 · "Just like softmax." ─────────────────────────────────────────
        self.cue(6)
        jls = T("Just like softmax.", sz=46, c=GRY).move_to(UP * 2.8)
        self.P(FadeIn(jls, shift=DOWN * 0.15), rt=0.4)

        # ── 7 · "But they don't distribute evenly." ──────────────────────────
        self.cue(7)
        self.P(FadeOut(VGroup(sum_hdr, sum_eq, jls, score_eq)), rt=0.3)
        bde1 = T("But they don't",      sz=52).move_to(UP * 5.5)
        bde2 = T("distribute evenly.",  sz=52, c=RED).next_to(bde1, DOWN, buff=0.28)
        self.P(FadeIn(bde1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(bde2, shift=DOWN * 0.15), rt=0.35)

        # ── 8 · "They form a U-shape." — axes + curve draw ───────────────────
        self.cue(8)
        self.P(FadeOut(VGroup(bde1, bde2)), rt=0.25)
        ax, curve, area_l, area_m, area_r, lbl_s, lbl_m, lbl_e, lbl_y = make_u_axes()
        u_hdr = T("They form a U-shape.", sz=46).move_to(UP * 5.5)

        # Create axes + header simultaneously, then curve, then labels
        self.P(FadeIn(u_hdr), Create(ax), rt=0.5)
        self.P(Create(curve, rate_func=smooth), rt=0.42)
        self.P(FadeIn(lbl_s), FadeIn(lbl_m), FadeIn(lbl_e), FadeIn(lbl_y), rt=0.30)

        # ── 9 · "First sentence: high attention." ────────────────────────────
        self.cue(9)
        self.P(FadeOut(u_hdr), rt=0.25)
        hi1a = T("First sentence:",  sz=46).move_to(UP * 5.5)
        hi1b = T("HIGH attention",   sz=52, c=GRN, weight=BOLD).next_to(hi1a, DOWN, buff=0.22)
        self.P(FadeIn(hi1a, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(hi1b, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(area_l), rt=0.4)

        # ── 10 · "Last sentence: high attention." ────────────────────────────
        self.cue(10)
        self.P(FadeOut(VGroup(hi1a, hi1b)), rt=0.25)
        hi2a = T("Last sentence:",  sz=46).move_to(UP * 5.5)
        hi2b = T("HIGH attention",  sz=52, c=GRN, weight=BOLD).next_to(hi2a, DOWN, buff=0.22)
        self.P(FadeIn(hi2a, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(hi2b, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(area_r), rt=0.4)

        # ── 11 · "Everything in the middle? Starved." ────────────────────────
        self.cue(11)
        self.P(FadeOut(VGroup(hi2a, hi2b)), rt=0.25)
        mid_a = T("Everything in the middle?", sz=44).move_to(UP * 5.5)
        mid_b = T("STARVED.", sz=76, c=RED, weight=BOLD).next_to(mid_a, DOWN, buff=0.22)
        self.P(FadeIn(mid_a,  shift=DOWN * 0.15), rt=0.35)
        self.P(Write(mid_b),                       rt=0.45)
        self.P(FadeIn(area_m), rt=0.45)

        # ── 12 · "Stanford measured it." ─────────────────────────────────────
        self.cue(12)
        self.P(FadeOut(VGroup(ax, curve, area_l, area_m, area_r,
                              lbl_s, lbl_m, lbl_e, lbl_y,
                              mid_a, mid_b)), rt=0.35)
        stan = T("Stanford measured it.", sz=54).move_to(UP * 0.5)
        self.P(FadeIn(stan, shift=DOWN * 0.15), rt=0.4)

        # ── 13 · "When the answer was placed in the middle…" ─────────────────
        self.cue(13)
        self.P(FadeOut(stan), rt=0.25)
        w13a = T("When the key answer",       sz=44).move_to(UP * 5.5)
        w13b = T("sat in the middle",         sz=40, c=GRY).next_to(w13a, DOWN, buff=0.2)
        w13c = T("of a long context…",        sz=40, c=GRY).next_to(w13b, DOWN, buff=0.16)
        self.P(FadeIn(w13a, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(w13b, shift=DOWN * 0.15), rt=0.3)
        self.P(FadeIn(w13c, shift=DOWN * 0.15), rt=0.3)

        # Accuracy comparison bars — positioned well below text labels
        bar_h   = 3.0
        bar_s   = Rectangle(width=1.4, height=bar_h,
                             fill_color=GRN, fill_opacity=0.85, stroke_width=0)
        bar_m   = Rectangle(width=1.4, height=bar_h * 0.70,
                             fill_color=RED, fill_opacity=0.85, stroke_width=0)
        bar_s.align_to(DOWN * 3.8, DOWN).shift(LEFT  * 1.95)
        bar_m.align_to(DOWN * 3.8, DOWN).shift(RIGHT * 1.95)

        lbl_bs = T("START",  sz=28, c=GRN).next_to(bar_s, DOWN, buff=0.22)
        lbl_bm = T("MIDDLE", sz=28, c=RED).next_to(bar_m, DOWN, buff=0.22)

        self.P(FadeIn(bar_s), FadeIn(lbl_bs), rt=0.5)
        self.P(FadeIn(bar_m), FadeIn(lbl_bm), rt=0.5)

        # ── 14 · "accuracy dropped thirty percent." ───────────────────────────
        self.cue(14)
        pct_s   = T("100%",  sz=30, c=GRN).next_to(bar_s, UP, buff=0.2)
        pct_m   = T("70%",   sz=30, c=RED).next_to(bar_m, UP, buff=0.2)
        drop    = T("−30%",  sz=72, c=RED, weight=BOLD).move_to(UP * 2.6)
        self.P(FadeIn(drop, shift=DOWN * 0.2), rt=0.45)
        self.P(FadeIn(pct_s), FadeIn(pct_m),  rt=0.35)

        # ── 15 · "Same information. Same model." ─────────────────────────────
        self.cue(15)
        self.P(FadeOut(VGroup(w13a, w13b, w13c)), rt=0.25)
        sm1 = T("Same information.", sz=50).move_to(UP * 5.5)
        sm2 = T("Same model.",       sz=50, c=GRY).next_to(sm1, DOWN, buff=0.22)
        self.P(FadeIn(sm1, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(sm2, shift=DOWN * 0.15), rt=0.3)

        # ── 16 · "Just moved to the middle." ─────────────────────────────────
        self.cue(16)
        self.P(FadeOut(VGroup(sm1, sm2)), rt=0.25)
        mv1 = T("Just moved to",  sz=54).move_to(UP * 5.5)
        mv2 = T("the middle.",    sz=64, c=RED, weight=BOLD).next_to(mv1, DOWN, buff=0.25)
        self.P(FadeIn(mv1, shift=DOWN * 0.15), rt=0.35)
        self.P(Write(mv2), rt=0.4)

        # ── 17 · "This isn't a bug." ──────────────────────────────────────────
        self.cue(17)
        self.P(FadeOut(VGroup(bar_s, bar_m, lbl_bs, lbl_bm,
                              drop, pct_s, pct_m, mv1, mv2)), rt=0.35)
        bug = T("This isn't a bug.", sz=60).move_to(UP * 0.5)
        self.P(FadeIn(bug, shift=DOWN * 0.15), rt=0.4)

        # ── 18 · "It's attention sinks…" ─────────────────────────────────────
        self.cue(18)
        self.P(FadeOut(bug), rt=0.25)
        as1 = T("It's attention sinks.",       sz=52, c=BLU, weight=BOLD).move_to(UP * 5.5)
        as2 = T("The architecture",            sz=42).next_to(as1, DOWN, buff=0.28)
        as3 = T("systematically routes",        sz=42).next_to(as2, DOWN, buff=0.2)
        as4 = T("probability mass",             sz=42, c=AMB).next_to(as3, DOWN, buff=0.2)
        as5 = T("away from middle tokens.",    sz=38, c=GRY).next_to(as4, DOWN, buff=0.2)
        self.P(FadeIn(as1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(as2, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(as3, shift=DOWN * 0.15), rt=0.3)
        self.P(FadeIn(as4, shift=DOWN * 0.15), rt=0.3)
        self.P(FadeIn(as5, shift=DOWN * 0.15), rt=0.3)

        # ── 19 · "500-word prompt / key instruction buried…" ─────────────────
        self.cue(19)
        self.P(FadeOut(VGroup(as1, as2, as3, as4, as5)), rt=0.35)
        p19a = T("Your 500-word prompt:",            sz=44).move_to(UP * 5.5)
        p19b = T("key instruction in paragraph 3.",  sz=36, c=RED).next_to(p19a, DOWN, buff=0.22)
        self.P(FadeIn(p19a, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(p19b, shift=DOWN * 0.15), rt=0.3)

        # Word-block grid centred on screen
        blocks = make_prompt_blocks()
        blocks.move_to(ORIGIN)

        # Highlight row-4, col-3 (middle zone) as the buried key instruction
        key_block = blocks[4 * 7 + 3]
        key_rect  = SurroundingRectangle(key_block, buff=0.08,
                                          color=GLD, stroke_width=3)
        key_lbl   = T("key instruction", sz=22, c=GLD).next_to(key_rect, RIGHT, buff=0.15)

        self.P(FadeIn(blocks), rt=0.5)
        self.P(Create(key_rect), FadeIn(key_lbl), rt=0.4)

        # ── 20 · "the model mathematically underweights it." ─────────────────
        self.cue(20)
        self.P(FadeOut(VGroup(p19a, p19b)), rt=0.25)
        uw1 = T("The model",          sz=54).move_to(UP * 5.5)
        uw2 = T("mathematically",     sz=48, c=RED).next_to(uw1, DOWN, buff=0.22)
        uw3 = T("underweights it.",   sz=54, c=RED, weight=BOLD).next_to(uw2, DOWN, buff=0.22)
        self.P(FadeIn(uw1, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(uw2, shift=DOWN * 0.15), rt=0.3)
        self.P(FadeIn(uw3, shift=DOWN * 0.15), rt=0.3)

        # ── 21 · "Most important thing you need ChatGPT to do?" ──────────────
        self.cue(21)
        self.P(FadeOut(VGroup(blocks, key_rect, key_lbl, uw1, uw2, uw3)), rt=0.35)
        mi1 = T("Most important thing",      sz=48).move_to(UP * 2.4)
        mi2 = T("you need ChatGPT to do?",   sz=42, c=GRY).next_to(mi1, DOWN, buff=0.28)
        self.P(FadeIn(mi1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(mi2, shift=DOWN * 0.15), rt=0.35)

        # ── 22 · "First sentence or last sentence." ───────────────────────────
        self.cue(22)
        self.P(FadeOut(VGroup(mi1, mi2)), rt=0.25)
        r1 = T("First sentence",    sz=56, c=GRN, weight=BOLD).move_to(UP * 1.6)
        r2 = T("or last sentence.", sz=56, c=GRN, weight=BOLD).next_to(r1, DOWN, buff=0.3)
        self.P(FadeIn(r1, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(r2, shift=DOWN * 0.15), rt=0.3)

        # ── 23 · "Never the middle."  (0.64 s — minimal) ────────────────────
        self.cue(23)
        self.P(FadeOut(VGroup(r1, r2)), rt=0.25)
        ntm = T("Never the middle.", sz=66, c=RED, weight=BOLD).move_to(UP * 0.5)
        self.P(Write(ntm), rt=0.35)

        # ── 24 · closer ──────────────────────────────────────────────────────
        self.cue(24)
        die1 = T("The middle is where",     sz=46).move_to(UP * 2.0)
        die2 = T("your instructions",       sz=46, c=GRY).next_to(die1, DOWN, buff=0.28)
        die3 = T("go to die.",              sz=70, c=RED, weight=BOLD).next_to(die2, DOWN, buff=0.32)
        self.P(FadeOut(ntm), rt=0.25)
        self.P(FadeIn(die1, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(die2, shift=DOWN * 0.15), rt=0.3)
        self.P(Write(die3), rt=0.5)

        self.tail(2.0)
