# softmax_short.py — Hallucination short, portrait 1080×1920, 42.87 s
# render: python -m manim softmax_short.py Softmax --resolution 1080,1920 --fps 30 -q h
# mux:    ffmpeg -i Softmax.mp4 -i voiceover.mp3 -c:v copy -c:a aac -shortest out.mp4
#
# Onsets from pocketsphinx continuous decoder (word-level, absolute timestamps).
# Zone rule: text above y=4.5 only, math/visuals in -3 to +3, nothing overlaps.

from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT  = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GLD  = "#FFFF00"; GRN = "#83C167"; DIM = "#2A2A3A"; AMB = "#FF9408"
CGPT = "#10A37F"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)


# ── probability bar helper ────────────────────────────────────────────────────
def dist_bar(segments, width=7.2, height=0.85, cy=0.0):
    """
    segments = [(fraction, colour, short_label), ...]  — must sum ≈ 1.0
    Returns a VGroup that can be FadeIn/FadeOut as one unit.
    cy = vertical centre in Manim coords.
    """
    grp = VGroup()
    bg  = Rectangle(width=width, height=height,
                    fill_color="#12122A", fill_opacity=1,
                    stroke_color=GRY, stroke_width=1.5)
    bg.move_to(UP * cy)
    grp.add(bg)

    x = -width / 2
    for frac, col, lbl in segments:
        w = frac * width
        rect = Rectangle(width=max(w - 0.04, 0.02), height=height - 0.12,
                         fill_color=col, fill_opacity=0.85, stroke_width=0)
        rect.move_to(RIGHT * (x + w / 2) + UP * cy)
        grp.add(rect)
        if lbl and w > 0.5:
            txt = T(lbl, sz=20, c=WHT)
            txt.move_to(rect.get_center())
            if txt.width > w - 0.12:
                txt.scale_to_fit_width(w - 0.12)
            grp.add(txt)
        x += w

    # "= 1.0" marker at right edge
    marker = T("= 1.0", sz=24, c=GLD)
    marker.next_to(bg, RIGHT, buff=0.22)
    grp.add(marker)
    return grp


# ── base scene ────────────────────────────────────────────────────────────────
class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Softmax(S):
    ONSETS = [
        0.060,  #  0  "ChatGPT just made something up."
        2.010,  #  1  "That's not a glitch."
        3.020,  #  2  "That's the equation."
        4.140,  #  3  "At every single word, the model runs a function"
        7.040,  #  4  "called softmax."
        8.500,  #  5  "It takes a list of every word it knows —"
        10.250, #  6  "a hundred thousand of them —"
        11.440, #  7  "and forces the probabilities to sum to exactly one."
        14.490, #  8  "No exceptions."
        15.320, #  9  "There is no option that means I don't know."
        17.730, # 10  "The architecture doesn't have one."
        19.640, # 11  "It must distribute 100% of its confidence across something."
        23.150, # 12  "So when you ask about a paper that doesn't exist,"
        25.430, # 13  "or a person it's never seen,"
        27.080, # 14  "or a date it has no data for —"
        29.050, # 15  "it doesn't stop."
        30.100, # 16  "It can't stop."
        31.500, # 17  "It finds whatever looks most like a plausible answer."
        35.900, # 18  "Hallucination isn't ChatGPT failing at its job."
        38.550, # 19  "It's ChatGPT doing its job perfectly."
        40.620, # 20  "The math just doesn't have room for uncertainty."
    ]

    def construct(self):
        self.setup()

        # ── 0 · "ChatGPT just made something up." ─────────────
        cg  = T("ChatGPT", sz=64, c=CGPT, weight=BOLD).move_to(UP * 2.0)
        msu = T("just made something up.", sz=48).next_to(cg, DOWN, buff=0.3)
        # fake hallucinated quote in a bubble
        fake_lbl = T('"The Eiffel Tower was built in 1832."', sz=30, c=GRY)
        fake_box = SurroundingRectangle(fake_lbl, buff=0.22, corner_radius=0.15,
                                        color=GRY, stroke_width=1.2,
                                        fill_color="#1A1A2E", fill_opacity=1)
        fake_grp = VGroup(fake_box, fake_lbl).move_to(DOWN * 1.8)

        self.cue(0)
        self.P(FadeIn(cg, shift=DOWN * 0.15), rt=0.45)
        self.P(FadeIn(msu, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(fake_grp), rt=0.4)

        # ── 1 · "That's not a glitch." ─────────────────────────
        self.cue(1)
        self.P(FadeOut(VGroup(cg, msu, fake_grp)), rt=0.3)
        ng = T("That's not a glitch.", sz=54).move_to(UP * 0.5)
        self.P(FadeIn(ng, shift=DOWN * 0.15), rt=0.45)

        # ── 2 · "That's the equation." ─────────────────────────
        self.cue(2)
        eq_lbl = T("That's the", sz=54).move_to(UP * 1.2)
        eq_lbl2 = T("equation.", sz=64, c=GLD, weight=BOLD).next_to(eq_lbl, DOWN, buff=0.25)
        self.P(FadeOut(ng), rt=0.25)
        self.P(FadeIn(eq_lbl, shift=DOWN * 0.15), rt=0.4)
        self.P(Write(eq_lbl2), rt=0.45)

        # ── 3 · "at every single word, the model runs a function" ─
        self.cue(3)
        self.P(FadeOut(VGroup(eq_lbl, eq_lbl2)), rt=0.3)
        every = T("At every single word,", sz=48).move_to(UP * 5.5)
        runs  = T("the model runs a function", sz=42, c=GRY).next_to(every, DOWN, buff=0.25)
        self.P(FadeIn(every, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(runs,  shift=DOWN * 0.15), rt=0.35)

        # ── 4 · "called softmax." + formula ────────────────────
        self.cue(4)
        called = T("called", sz=52).move_to(UP * 1.2)
        sm_word = T("softmax.", sz=76, c=BLU, weight=BOLD).next_to(called, DOWN, buff=0.25)
        self.P(FadeIn(called,  shift=DOWN * 0.15), rt=0.4)
        self.P(Write(sm_word), rt=0.5)

        sm_eq = MathTex(
            r"\text{softmax}(z)_i = \dfrac{e^{z_i}}{\displaystyle\sum_{j} e^{z_j}}",
            font_size=46, color=WHT
        ).move_to(DOWN * 1.6)
        self.P(Write(sm_eq), rt=0.65)

        # ── 5 · "takes a list of every word it knows" ──────────
        self.cue(5)
        self.P(FadeOut(VGroup(every, runs, called, sm_word)), rt=0.3)
        list_lbl = T("a list of every word it knows", sz=44).move_to(UP * 5.5)
        self.P(FadeIn(list_lbl, shift=DOWN * 0.15), rt=0.4)

        # ── 6 · "a hundred thousand of them" + bar appears ─────
        self.cue(6)
        hun_lbl = T("100,000 of them.", sz=58, c=GLD, weight=BOLD).move_to(UP * 4.2)
        self.P(FadeIn(hun_lbl, shift=DOWN * 0.15), rt=0.4)

        # Token bar with typical "confident" distribution
        conf_bar = dist_bar([
            (0.61, BLU,  "likely tokens"),
            (0.24, CGPT, "less likely"),
            (0.15, RED,  "rare"),
        ], cy=0.6)
        self.P(FadeIn(conf_bar), rt=0.5)

        # ── 7 · "forces probabilities to sum to exactly one" ───
        self.cue(7)
        self.P(FadeOut(VGroup(list_lbl, hun_lbl)), rt=0.25)
        sum_hdr = T("Forces them to sum", sz=46).move_to(UP * 5.5)
        self.P(FadeIn(sum_hdr, shift=DOWN * 0.15), rt=0.4)

        sum_eq = MathTex(
            r"\sum_{i} \; p_i \;=\; 1.000",
            font_size=60, color=GLD
        ).move_to(UP * 4.0)
        self.P(Write(sum_eq), rt=0.55)

        # highlight bar = always full
        full_label = T("always full — no exceptions", sz=30, c=GRY).next_to(conf_bar, DOWN, buff=0.35)
        self.P(FadeIn(full_label), rt=0.4)

        # ── 8 · "No exceptions." ───────────────────────────────
        self.cue(8)
        self.P(FadeOut(VGroup(sm_eq, conf_bar, sum_hdr, sum_eq, full_label)), rt=0.25)
        no_ex = T("No exceptions.", sz=72, c=RED, weight=BOLD).move_to(UP * 0.5)
        self.P(Write(no_ex), rt=0.4)

        # ── 9 · "no option that means I don't know" ────────────
        self.cue(9)
        self.P(FadeOut(no_ex), rt=0.25)
        no_opt1 = T("There is no option", sz=50).move_to(UP * 5.4)
        no_opt2 = T("that means", sz=50).next_to(no_opt1, DOWN, buff=0.25)
        idk_txt = T('"I don\'t know"', sz=62, c=RED, weight=BOLD).next_to(no_opt2, DOWN, buff=0.3)
        self.P(FadeIn(no_opt1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(no_opt2, shift=DOWN * 0.15), rt=0.35)
        self.P(Write(idk_txt), rt=0.45)

        # bar with the IDK slot explicitly missing
        missing_bar = dist_bar([
            (0.55, BLU,  "tokens..."),
            (0.45, CGPT, "more tokens..."),
        ], cy=0.6)

        idk_outline = Rectangle(width=1.5, height=0.85,
                                stroke_color=RED, stroke_width=2.5,
                                fill_color="#1A1A2E", fill_opacity=1)
        idk_outline.move_to(missing_bar[0].get_right() + RIGHT * 0.95)
        idk_slot_lbl = T("???", sz=28, c=RED).move_to(idk_outline.get_center())
        cross1 = Line(idk_outline.get_corner(UL), idk_outline.get_corner(DR),
                      color=RED, stroke_width=3)
        cross2 = Line(idk_outline.get_corner(UR), idk_outline.get_corner(DL),
                      color=RED, stroke_width=3)
        idk_grp = VGroup(idk_outline, idk_slot_lbl, cross1, cross2)

        self.P(FadeIn(missing_bar), rt=0.5)
        self.P(FadeIn(idk_grp), rt=0.4)

        # ── 10 · "The architecture doesn't have one." ──────────
        self.cue(10)
        arch = T("The architecture", sz=44, c=GRY).move_to(DOWN * 3.2)
        arch2 = T("doesn't have one.", sz=48, c=RED, weight=BOLD).next_to(arch, DOWN, buff=0.25)
        self.P(FadeIn(arch,  shift=UP * 0.15), rt=0.4)
        self.P(FadeIn(arch2, shift=UP * 0.15), rt=0.35)

        # ── 11 · "must distribute 100% confidence across something" ─
        self.cue(11)
        self.P(FadeOut(VGroup(no_opt1, no_opt2, idk_txt, missing_bar,
                              idk_grp, arch, arch2)), rt=0.35)

        must1 = T("It MUST distribute", sz=50, c=WHT).move_to(UP * 5.4)
        must2 = T("100% of its confidence", sz=44, c=GLD, weight=BOLD).next_to(must1, DOWN, buff=0.25)
        must3 = T("across SOMETHING.", sz=48, c=WHT).next_to(must2, DOWN, buff=0.25)
        self.P(FadeIn(must1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(must2, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(must3, shift=DOWN * 0.15), rt=0.35)

        # full bar — uncertainty forced into plausible-looking tokens
        forced_bar = dist_bar([
            (0.38, BLU,  "plausible"),
            (0.29, CGPT, "plausible"),
            (0.21, AMB,  "plausible"),
            (0.12, RED,  "rest"),
        ], cy=0.5)
        self.P(FadeIn(forced_bar), rt=0.5)

        # ── 12 · "paper that doesn't exist" ────────────────────
        self.cue(12)
        self.P(FadeOut(VGroup(must1, must2, must3, forced_bar)), rt=0.3)

        q1 = T("You ask about", sz=42, c=GRY).move_to(UP * 5.5)
        p1 = T("a paper that doesn't exist.", sz=46, c=RED).next_to(q1, DOWN, buff=0.3)
        self.P(FadeIn(q1, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(p1, shift=DOWN * 0.15), rt=0.4)

        # ── 13 · "or a person it's never seen" ─────────────────
        self.cue(13)
        self.P(FadeOut(VGroup(q1, p1)), rt=0.25)
        p2 = T("A person it's", sz=46).move_to(UP * 5.5)
        p2b = T("never seen.", sz=50, c=RED).next_to(p2, DOWN, buff=0.3)
        self.P(FadeIn(p2,  shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(p2b, shift=DOWN * 0.15), rt=0.35)

        # ── 14 · "or a date it has no data for" ────────────────
        self.cue(14)
        self.P(FadeOut(VGroup(p2, p2b)), rt=0.25)
        p3 = T("A date it has", sz=46).move_to(UP * 5.5)
        p3b = T("no data for.", sz=50, c=RED).next_to(p3, DOWN, buff=0.3)
        self.P(FadeIn(p3,  shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(p3b, shift=DOWN * 0.15), rt=0.35)

        # ── 15 · "it doesn't stop." ────────────────────────────
        self.cue(15)
        self.P(FadeOut(VGroup(p3, p3b)), rt=0.25)
        ds = T("It doesn't stop.", sz=66, c=WHT, weight=BOLD).move_to(UP * 0.5)
        self.P(Write(ds), rt=0.45)

        # ── 16 · "It can't stop." ──────────────────────────────
        self.cue(16)
        cs = T("It can't stop.", sz=76, c=RED, weight=BOLD).next_to(ds, DOWN, buff=0.45)
        self.P(Write(cs), rt=0.45)

        # ── 17 · "finds whatever looks most like a plausible answer" ─
        self.cue(17)
        self.P(FadeOut(VGroup(ds, cs)), rt=0.3)

        finds1 = T("It finds whatever", sz=50).move_to(UP * 5.4)
        finds2 = T("looks most like", sz=50).next_to(finds1, DOWN, buff=0.25)
        finds3 = T("a plausible answer.", sz=50, c=AMB, weight=BOLD).next_to(finds2, DOWN, buff=0.25)
        self.P(FadeIn(finds1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(finds2, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(finds3, shift=DOWN * 0.15), rt=0.4)

        # Show a "confident" hallucinated answer below
        hall_txt = T('"The paper argues that neural networks\nwere first proposed in 1923."',
                     sz=28, c=GRY)
        hall_box = SurroundingRectangle(hall_txt, buff=0.25, corner_radius=0.15,
                                        color=CGPT, stroke_width=2,
                                        fill_color="#0D1A12", fill_opacity=1)
        conf_chip = T("99.3% confident", sz=26, c=GRN)
        hall_all = VGroup(hall_box, hall_txt).move_to(DOWN * 1.2)
        conf_chip.next_to(hall_all, DOWN, buff=0.3)

        self.P(FadeIn(hall_all), rt=0.5)
        self.P(FadeIn(conf_chip), rt=0.4)

        # ── 18 · "Hallucination isn't ChatGPT failing at its job." ─
        self.cue(18)
        self.P(FadeOut(VGroup(finds1, finds2, finds3, hall_all, conf_chip)), rt=0.35)

        h1 = T("Hallucination isn't", sz=50).move_to(UP * 2.2)
        h2 = T("ChatGPT failing", sz=54, c=CGPT).next_to(h1, DOWN, buff=0.28)
        h3 = T("at its job.", sz=50).next_to(h2, DOWN, buff=0.28)
        self.P(FadeIn(h1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(h2, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(h3, shift=DOWN * 0.15), rt=0.35)

        # ── 19 · "It's ChatGPT doing its job perfectly." ────────
        self.cue(19)
        self.P(FadeOut(VGroup(h1, h2, h3)), rt=0.3)

        p_1 = T("It's ChatGPT", sz=54).move_to(UP * 1.8)
        p_2 = T("doing its job", sz=54, c=GRN).next_to(p_1, DOWN, buff=0.28)
        p_3 = Text("perfectly.", font_size=68, color=GLD, weight=BOLD).next_to(p_2, DOWN, buff=0.28)
        self.P(FadeIn(p_1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(p_2, shift=DOWN * 0.15), rt=0.35)
        self.P(Write(p_3), rt=0.45)

        # ── 20 · "The math just doesn't have room for uncertainty." ─
        self.cue(20)
        self.P(FadeOut(VGroup(p_1, p_2, p_3)), rt=0.3)

        m1 = T("The math just",          sz=56, c=WHT).move_to(UP * 1.8)
        m2 = T("doesn't have room",       sz=52, c=WHT).next_to(m1, DOWN, buff=0.3)
        m3 = T("for uncertainty.",         sz=58, c=RED, weight=BOLD).next_to(m2, DOWN, buff=0.35)
        self.P(FadeIn(m1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(m2, shift=DOWN * 0.15), rt=0.35)
        self.P(Write(m3), rt=0.5)

        self.tail(3.0)
