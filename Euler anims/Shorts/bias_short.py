# bias_short.py — "predicting a word, not rolling dice" — 27.5 s
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


def user_bubble(text, cy=0, width=5.2):
    lbl = T(text, sz=26, c=WHT)
    if lbl.width > width - 0.5:
        lbl.scale_to_fit_width(width - 0.5)
    box = RoundedRectangle(width=width, height=0.8, corner_radius=0.25,
                           fill_color=BLU, fill_opacity=0.9, stroke_width=0)
    box.move_to(UP*cy)
    lbl.move_to(box.get_center())
    return VGroup(box, lbl)


def make_histogram(numbers, heights, highlight, width=6.4, max_h=2.8, cy=-0.6):
    """Bar chart across sampled numbers 1-100. highlight = set of tall bars."""
    n = len(numbers)
    bar_w = width / n * 0.65
    gap = width / n
    grp = VGroup()
    labels = VGroup()
    base_y = cy - max_h/2
    for i, (num, h) in enumerate(zip(numbers, heights)):
        x = -width/2 + gap*(i+0.5)
        color = GLD if num in highlight else GRY
        bar = Rectangle(width=bar_w, height=h, fill_color=color,
                        fill_opacity=0.9, stroke_width=0)
        bar.move_to([x, base_y + h/2, 0])
        grp.add(bar)
        lbl = T(str(num), sz=16, c=(GLD if num in highlight else GRY))
        lbl.move_to([x, base_y - 0.22, 0])
        labels.add(lbl)
    baseline = Line([-width/2-0.1, base_y, 0], [width/2+0.1, base_y, 0],
                    color=GRY, stroke_width=1.5)
    return VGroup(baseline, grp, labels), grp


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Bias(S):
    ONSETS = [
        0.09,   #  0  "Ask any AI for a random number 1 to 100."
        3.38,   #  1  "It'll definitely say 37,"
        5.11,   #  2  "73, or 47,"
        6.74,   #  3  "way more than it should."
        8.55,   #  4  "Here's why. It's not running"
        11.10,  #  5  "a random number generator."
        12.40,  #  6  "It's predicting the next word,"
        14.09,  #  7  "based on how humans write"
        15.70,  #  8  "when they think they're being random."
        17.43,  #  9  "Humans always pick primes,"
        19.92,  # 10  "numbers ending in 7,"
        21.51,  # 11  "never round numbers."
        24.08,  # 12  closing
    ]

    def construct(self):
        self.setup()

        # ── 0 · "Ask any AI for a random number 1 to 100." ─────────────────
        cgpt_lbl = T("ChatGPT", sz=28, c=CGPT, weight=BOLD).to_edge(UP, buff=0.5)
        prompt = user_bubble("give me a random number\n1 to 100", cy=4.6)
        self.cue(0)
        self.P(FadeIn(cgpt_lbl), rt=0.2)
        self.P(FadeIn(prompt, shift=LEFT*0.1), rt=0.5)

        # ── 1 · "It'll definitely say 37," ─────────────────────────────────
        self.cue(1)
        n37 = T("37", sz=90, c=GLD, weight=BOLD).move_to(UP*2.2)
        self.P(Write(n37), rt=0.5)

        # ── 2 · "73, or 47," ─────────────────────────────────────────────
        self.cue(2)
        n73 = T("73", sz=64, c=GLD, weight=BOLD).next_to(n37, LEFT, buff=1.0).shift(DOWN*0.3)
        n47 = T("47", sz=64, c=GLD, weight=BOLD).next_to(n37, RIGHT, buff=1.0).shift(DOWN*0.3)
        self.P(FadeIn(n73, shift=UP*0.1), FadeIn(n47, shift=UP*0.1), rt=0.5)

        # ── 3 · "way more than it should." — histogram reveal ──────────────
        self.cue(3)
        self.P(FadeOut(VGroup(cgpt_lbl, prompt, n37, n73, n47)), rt=0.35)

        sample_nums = [10, 20, 27, 37, 42, 47, 50, 63, 73, 84, 90, 100]
        sample_hts  = [0.05, 0.05, 0.9, 2.6, 1.4, 2.4, 0.05, 0.3, 2.5, 0.15, 0.05, 0.05]
        hist, bars = make_histogram(sample_nums, sample_hts, highlight={37, 47, 73})
        hist.move_to(UP*0.6)
        way_more = T("way more than it should.", sz=30, c=RED, weight=BOLD).next_to(hist, DOWN, buff=0.7)

        self.P(Create(hist[0]), rt=0.3)
        self.P(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.06), rt=0.7)
        self.P(FadeIn(hist[2]), rt=0.3)
        self.P(FadeIn(way_more, shift=DOWN*0.1), rt=0.4)

        # ── 4 · "Here's why. It's not running" — RNG icon crossed out ───────
        self.cue(4)
        self.P(FadeOut(way_more), rt=0.25)
        why = cap("Here's why.", sz=36, c=WHT)
        self.P(FadeIn(why), rt=0.3)

        dice = VGroup(*[
            RoundedRectangle(width=0.5, height=0.5, corner_radius=0.08,
                             fill_color="#15152A", fill_opacity=1,
                             stroke_color=GRY, stroke_width=2)
            for _ in range(1)
        ])
        die_dots = VGroup(*[Dot(radius=0.05, color=GRY) for _ in range(5)])
        for d, pos in zip(die_dots, [UL*0.12, UR*0.12, ORIGIN, DL*0.12, DR*0.12]):
            d.move_to(dice[0].get_center() + pos)
        die_grp = VGroup(dice, die_dots).move_to(DOWN*1.5)
        self.P(FadeIn(die_grp), rt=0.35)
        die_x = Cross(die_grp, color=RED, stroke_width=5)
        self.P(Create(die_x), rt=0.4)

        # ── 5 · "a random number generator." ─────────────────────────────
        self.cue(5)
        rng_lbl = T("not a random", sz=26, c=RED).next_to(die_grp, DOWN, buff=0.3)
        rng_lbl2 = T("number generator.", sz=26, c=RED).next_to(rng_lbl, DOWN, buff=0.1)
        self.P(FadeIn(rng_lbl), FadeIn(rng_lbl2), rt=0.4)

        # ══ SCENE: predicting the next word (6-8) ═══════════════════════════
        self.cue(6)
        self.P(FadeOut(VGroup(why, hist, bars, die_grp, die_x, rng_lbl, rng_lbl2)), rt=0.4)

        sentence = T('"a random number is', sz=30, c=WHT).move_to(UP*1.6)
        sentence2 = T('...  ___"', sz=30, c=WHT).next_to(sentence, DOWN, buff=0.15)
        self.P(FadeIn(sentence), FadeIn(sentence2), rt=0.4)
        predict_lbl = T("predicting the next word", sz=26, c=AMB).next_to(sentence2, DOWN, buff=0.4)
        self.P(FadeIn(predict_lbl, shift=DOWN*0.1), rt=0.4)

        # ── 7 · "based on how humans write" — token probability bars ───────
        self.cue(7)
        self.P(FadeOut(predict_lbl), rt=0.25)
        # mini probability distribution over candidate "next word" tokens
        cand_nums = ["37", "73", "47", "12", "84", "50"]
        cand_probs = [0.34, 0.22, 0.19, 0.03, 0.02, 0.01]
        prob_bars = VGroup()
        prob_labels = VGroup()
        bx = -2.6
        for cn, cp in zip(cand_nums, cand_probs):
            h = cp * 4.5
            bar = Rectangle(width=0.6, height=h, fill_color=GLD if cp > 0.1 else GRY,
                            fill_opacity=0.85, stroke_width=0)
            bar.move_to([bx, -1.2 + h/2, 0])
            lbl = T(cn, sz=20, c=WHT).next_to(bar, DOWN, buff=0.15)
            prob_bars.add(bar)
            prob_labels.add(lbl)
            bx += 0.95
        self.P(LaggedStart(*[GrowFromEdge(b, DOWN) for b in prob_bars], lag_ratio=0.1), rt=0.55)
        self.P(FadeIn(prob_labels), rt=0.3)
        human_lbl = T("based on human writing", sz=24, c=GRY).move_to(DOWN*2.6)
        self.P(FadeIn(human_lbl), rt=0.35)

        # ── 8 · "when they think they're being random." ─────────────────────
        self.cue(8)
        random_lbl = T('"being random."', sz=26, c=BLU).next_to(human_lbl, DOWN, buff=0.3)
        self.P(FadeIn(random_lbl), rt=0.4)

        # ══ SCENE: humans have the same bias (9-11) ══════════════════════════
        self.cue(9)
        self.P(FadeOut(VGroup(sentence, sentence2, prob_bars, prob_labels,
                              human_lbl, random_lbl)), rt=0.4)
        # simple person icons all "picking" the same numbers
        def person(color=WHT):
            head = Circle(radius=0.14, fill_color=color, fill_opacity=1, stroke_width=0)
            body = Arc(radius=0.22, angle=PI, start_angle=0, color=color,
                      fill_color=color, fill_opacity=1, stroke_width=0)
            body.next_to(head, DOWN, buff=0.02)
            return VGroup(head, body)

        people = VGroup(*[person(WHT) for _ in range(5)])
        people.arrange(RIGHT, buff=0.55).move_to(UP*1.6)
        humans_lbl = T("Humans do this too.", sz=34, c=WHT, weight=BOLD).next_to(people, UP, buff=0.4)
        self.P(FadeIn(humans_lbl, shift=DOWN*0.1), rt=0.4)
        self.P(LaggedStart(*[FadeIn(p, scale=1.2) for p in people], lag_ratio=0.1), rt=0.6)

        picks = VGroup(*[T("37", sz=24, c=GLD, weight=BOLD).next_to(p, DOWN, buff=0.15) for p in people])
        self.P(FadeIn(picks), rt=0.4)
        primes_lbl = T("always primes.", sz=26, c=GLD).next_to(picks, DOWN, buff=0.4)
        self.P(FadeIn(primes_lbl), rt=0.35)

        # ── 10 · "numbers ending in 7," ─────────────────────────────────────
        self.cue(10)
        self.P(FadeOut(primes_lbl), rt=0.25)
        end7_lbl = T("numbers ending in 7.", sz=28, c=GLD, weight=BOLD).next_to(picks, DOWN, buff=0.4)
        self.P(FadeIn(end7_lbl, shift=DOWN*0.1), rt=0.4)

        # ── 11 · "never round numbers." — round numbers crossed out ────────
        self.cue(11)
        self.P(FadeOut(VGroup(humans_lbl, people, picks, end7_lbl)), rt=0.4)
        round_nums = VGroup(*[T(str(n), sz=32, c=GRY) for n in [10, 20, 30, 40, 50]])
        round_nums.arrange(RIGHT, buff=0.5).move_to(UP*0.8)
        never_lbl = T("NEVER round numbers.", sz=34, c=RED, weight=BOLD).next_to(round_nums, DOWN, buff=0.5)
        self.P(FadeIn(round_nums), rt=0.4)
        round_x = Cross(round_nums, color=RED, stroke_width=4)
        self.P(Create(round_x), rt=0.4)
        self.P(FadeIn(never_lbl, shift=DOWN*0.1), rt=0.4)

        # ══ SCENE: closing — learned bias, code fix (12) ════════════════════
        self.cue(12)
        self.P(FadeOut(VGroup(round_nums, round_x, never_lbl)), rt=0.4)

        learned = T("The AI learned this", sz=36, c=WHT).move_to(UP*2.2)
        learned2 = T("bias from us.", sz=40, c=AMB, weight=BOLD).next_to(learned, DOWN, buff=0.3)
        self.P(FadeIn(learned, shift=DOWN*0.1), rt=0.4)
        self.P(FadeIn(learned2, shift=DOWN*0.1), rt=0.4)

        # code block appearing as the fix
        code_box = RoundedRectangle(width=6.0, height=1.6, corner_radius=0.15,
                                    fill_color="#0D0D1A", fill_opacity=1,
                                    stroke_color=GRN, stroke_width=2.5)
        code_box.next_to(learned2, DOWN, buff=0.6)
        code_txt = Text("random.randint(1, 100)", font="monospace", font_size=26, color=GRN)
        code_txt.move_to(code_box.get_center())
        self.P(FadeIn(code_box), rt=0.35)
        self.P(Write(code_txt), rt=0.5)

        # uniform distribution mini-histogram as proof
        uniform_hts = [0.9]*10
        uniform_nums = list(range(10, 101, 10))
        uni_hist, uni_bars = make_histogram(uniform_nums, uniform_hts, highlight=set(),
                                            width=5.6, max_h=1.0, cy=-2.6)
        for b in uni_bars:
            b.set_color(GRN)
        uni_lbl = T("uniform. actually random.", sz=24, c=GRN).next_to(uni_hist, DOWN, buff=0.3)
        self.P(FadeIn(uni_hist), rt=0.4)
        self.P(FadeIn(uni_lbl), rt=0.35)

        self.tail(1.0)
