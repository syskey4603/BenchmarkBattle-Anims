# cantor_short.py — "He was destroyed for discovering it." short, 38 s
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

def card(mob, stroke=GRY, fill="#15152A", buff=0.28):
    box = SurroundingRectangle(mob, buff=buff, corner_radius=0.15,
                               color=stroke, stroke_width=2.2,
                               fill_color=fill, fill_opacity=1)
    box.set_z_index(mob.z_index - 1)
    return box


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Cantor(S):
    # Onsets from pocketsphinx continuous decoder — real word-level timing
    ONSETS = [
        0.06,   #  0  "In 1874,"
        0.98,   #  1  "a mathematician proved something impossible."
        3.46,   #  2  "Not all infinities are the same size."
        5.94,   #  3  "Georg Cantor showed that the infinity of whole numbers —"
        8.92,   #  4  "one, two, three, forever —"
        10.94,  #  5  "is actually smaller than the infinity of real numbers"
        13.30,  #  6  "between zero and one."
        14.84,  #  7  "Infinity had sizes."
        16.19,  #  8  "Nobody had ever imagined that."
        18.05,  #  9  "The most powerful mathematician in Germany,"
        19.29,  # 10  "Leopold Kronecker,"
        21.46,  # 11  "called it 'scientific charlatanism'"
        23.25,  # 12  "and spent years blocking Cantor's career, personally."
        26.41,  # 13  "Cantor suffered severe breakdowns for the rest of his life."
        29.30,  # 14  "He died in 1918."
        30.80,  # 15  "In a sanatorium."
        31.77,  # 16  "Still convinced he was right."
        33.12,  # 17  "He was."
        34.13,  # 18  "Every mathematician alive today"
        35.75,  # 19  "builds on the infinity"
        36.67,  # 20  "he was destroyed for discovering."
    ]

    def construct(self):
        self.setup()

        # ── 0 · "In 1874," ────────────────────────────────────────────────
        yr = T("1874", sz=90, c=GLD, weight=BOLD).move_to(UP * 1.0)
        self.cue(0)
        self.P(FadeIn(yr, shift=DOWN * 0.2), rt=0.4)

        # ── 1 · "a mathematician proved something impossible." ──────────────
        self.cue(1)
        m1 = T("a mathematician", sz=46).next_to(yr, DOWN, buff=0.5)
        m2 = T("proved something", sz=46).next_to(m1, DOWN, buff=0.25)
        m3 = T("impossible.", sz=56, c=RED, weight=BOLD).next_to(m2, DOWN, buff=0.3)
        self.P(FadeIn(m1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(m2, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(m3, shift=DOWN * 0.15), rt=0.4)

        # ── 2 · "Not all infinities are the same size." ─────────────────────
        self.cue(2)
        self.P(FadeOut(VGroup(yr, m1, m2, m3)), rt=0.35)
        n1 = T("Not all infinities", sz=52).move_to(UP * 0.8)
        n2 = T("are the same size.", sz=52, c=BLU, weight=BOLD).next_to(n1, DOWN, buff=0.3)
        self.P(FadeIn(n1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(n2, shift=DOWN * 0.15), rt=0.4)

        # ── 3 · "Georg Cantor showed that the infinity of whole numbers —" ──
        self.cue(3)
        self.P(FadeOut(VGroup(n1, n2)), rt=0.3)
        gc = T("Georg Cantor", sz=54, c=GLD, weight=BOLD).move_to(UP * 5.6)
        wn_hdr = T("the infinity of whole numbers:", sz=34, c=GRY).move_to(UP * 4.3)
        self.P(FadeIn(gc, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(wn_hdr, shift=DOWN * 0.15), rt=0.35)

        # whole-number list: 1, 2, 3, 4, 5, ...
        whole_nums = VGroup(*[T(str(n), sz=42, c=WHT) for n in range(1, 6)])
        whole_nums.add(T("...", sz=42, c=GRY))
        whole_nums.arrange(RIGHT, buff=0.5).move_to(UP * 2.6)

        # ── 4 · "one, two, three, forever —" ──────────────────────────────
        self.cue(4)
        self.P(LaggedStart(*[FadeIn(n, shift=DOWN * 0.1) for n in whole_nums],
                           lag_ratio=0.15), rt=0.9)

        # ── 5 · "is actually smaller than the infinity of real numbers" ─────
        self.cue(5)
        vs = T("SMALLER THAN", sz=40, c=RED, weight=BOLD).move_to(UP * 1.3)
        rn_hdr = T("the infinity of real numbers", sz=34, c=GRY).next_to(vs, DOWN, buff=0.35)
        self.P(Write(vs), rt=0.5)
        self.P(FadeIn(rn_hdr, shift=DOWN * 0.15), rt=0.4)

        # ── 6 · "between zero and one." — the diagonal argument ─────────────
        self.cue(6)
        between = T("between 0 and 1.", sz=44, c=BLU).next_to(rn_hdr, DOWN, buff=0.3)
        self.P(FadeIn(between, shift=DOWN * 0.15), rt=0.4)

        # Three sample decimals, digits laid out so we can highlight a diagonal
        digit_rows = [
            ["3", "5", "8", "2", "7"],
            ["7", "1", "4", "9", "0"],
            ["1", "4", "1", "5", "9"],
        ]
        row_mobs = VGroup()
        digit_mobs = []  # [[Text,...], ...] for diagonal access
        for i, row in enumerate(digit_rows):
            prefix = T("0.", sz=30, c=GRY)
            digits = VGroup(*[T(d, sz=30, c=WHT) for d in row])
            digits.arrange(RIGHT, buff=0.16)
            full = VGroup(prefix, digits).arrange(RIGHT, buff=0.08)
            full.move_to(DOWN * (1.6 + i * 0.55))
            row_mobs.add(full)
            digit_mobs.append(digits)
        row_mobs.move_to(DOWN * 2.3)
        # re-layout after centering the group
        for i, full in enumerate(row_mobs):
            full.move_to(DOWN * (1.7 + i * 0.6))

        self.P(FadeIn(row_mobs), rt=0.5)

        # Highlight the diagonal digit in each row (digit i of row i)
        diag_boxes = VGroup(*[
            SurroundingRectangle(digit_mobs[i][i], buff=0.05, color=GLD, stroke_width=2.5)
            for i in range(3)
        ])
        self.P(Create(diag_boxes), rt=0.45)

        # ── 7 · "Infinity had sizes." — build the new number, show it's missing ─
        self.cue(7)
        new_lbl = T("+1 each digit →", sz=26, c=GLD).next_to(row_mobs, DOWN, buff=0.35)
        new_num = T("0.4 2 2 ...", sz=34, c=GLD, weight=BOLD).next_to(new_lbl, DOWN, buff=0.2)
        not_on_list = T("not on the list.", sz=26, c=RED).next_to(new_num, DOWN, buff=0.2)

        self.P(FadeOut(diag_boxes), rt=0.2)
        self.P(FadeIn(new_lbl, shift=DOWN * 0.1), rt=0.3)
        self.P(Write(new_num), rt=0.4)
        self.P(FadeIn(not_on_list), rt=0.3)

        self.P(FadeOut(VGroup(gc, wn_hdr, whole_nums, vs, rn_hdr, between,
                              row_mobs, new_lbl, new_num, not_on_list)), rt=0.4)
        h1 = T("Infinity", sz=64, c=WHT, weight=BOLD).move_to(UP * 0.8)
        h2 = T("had sizes.", sz=68, c=GLD, weight=BOLD).next_to(h1, DOWN, buff=0.3)
        self.P(FadeIn(h1, shift=DOWN * 0.15), rt=0.4)
        self.P(Write(h2), rt=0.5)

        # ── 8 · "Nobody had ever imagined that." ─────────────────────────
        self.cue(8)
        self.P(FadeOut(VGroup(h1, h2)), rt=0.3)
        nb1 = T("Nobody had ever", sz=48).move_to(UP * 0.6)
        nb2 = T("imagined that.", sz=52, c=GRY).next_to(nb1, DOWN, buff=0.3)
        self.P(FadeIn(nb1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(nb2, shift=DOWN * 0.15), rt=0.4)

        # ── 9 · "The most powerful mathematician in Germany," ─────────────
        self.cue(9)
        self.P(FadeOut(VGroup(nb1, nb2)), rt=0.3)
        p1 = T("The most powerful", sz=42).move_to(UP * 5.6)
        p2 = T("mathematician in Germany:", sz=40, c=GRY).next_to(p1, DOWN, buff=0.25)
        self.P(FadeIn(p1, shift=DOWN * 0.15), rt=0.35)
        self.P(FadeIn(p2, shift=DOWN * 0.15), rt=0.35)

        # ── 10 · "Leopold Kronecker," ──────────────────────────────────────
        self.cue(10)
        kro_lbl = T("Leopold Kronecker", sz=56, c=RED, weight=BOLD).move_to(UP * 2.6)
        self.P(Write(kro_lbl), rt=0.5)

        # ── 11 · 'called it "scientific charlatanism"' ────────────────────
        self.cue(11)
        quote1 = T('"scientific', sz=44, c=WHT).move_to(UP * 0.6)
        quote2 = T('charlatanism."', sz=44, c=WHT).next_to(quote1, DOWN, buff=0.22)
        self.P(FadeIn(quote1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(quote2, shift=DOWN * 0.15), rt=0.35)

        # ── 12 · "and spent years blocking Cantor's career, personally." ──
        self.cue(12)
        self.P(FadeOut(VGroup(p1, p2, kro_lbl, quote1, quote2)), rt=0.4)
        bl1 = T("Spent years", sz=50).move_to(UP * 1.2)
        bl2 = T("blocking his career.", sz=50, c=RED, weight=BOLD).next_to(bl1, DOWN, buff=0.3)
        bl3 = T("Personally.", sz=44, c=GRY).next_to(bl2, DOWN, buff=0.3)
        self.P(FadeIn(bl1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(bl2, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(bl3, shift=DOWN * 0.15), rt=0.35)

        # ── 13 · "Cantor suffered severe breakdowns for the rest of his life." ─
        self.cue(13)
        self.P(FadeOut(VGroup(bl1, bl2, bl3)), rt=0.35)
        sb1 = T("Cantor suffered", sz=50).move_to(UP * 0.9)
        sb2 = T("severe breakdowns", sz=50, c=RED).next_to(sb1, DOWN, buff=0.28)
        sb3 = T("for the rest of his life.", sz=40, c=GRY).next_to(sb2, DOWN, buff=0.3)
        self.P(FadeIn(sb1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(sb2, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(sb3, shift=DOWN * 0.15), rt=0.35)

        # ── 14 · "He died in 1918." ─────────────────────────────────────
        self.cue(14)
        self.P(FadeOut(VGroup(sb1, sb2, sb3)), rt=0.3)
        died = T("He died in 1918.", sz=56).move_to(UP * 1.4)
        self.P(FadeIn(died, shift=DOWN * 0.15), rt=0.45)

        # ── 15 · "In a sanatorium." ────────────────────────────────────
        self.cue(15)
        san = T("In a sanatorium.", sz=48, c=GRY).next_to(died, DOWN, buff=0.4)
        self.P(FadeIn(san, shift=DOWN * 0.15), rt=0.4)

        # ── 16 · "Still convinced he was right." ──────────────────────
        self.cue(16)
        conv = T("Still convinced", sz=44).next_to(san, DOWN, buff=0.5)
        conv2 = T("he was right.", sz=48, c=GLD, weight=BOLD).next_to(conv, DOWN, buff=0.25)
        self.P(FadeIn(conv, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(conv2, shift=DOWN * 0.15), rt=0.4)

        # ── 17 · "He was." ─────────────────────────────────────────────
        self.cue(17)
        self.P(FadeOut(VGroup(died, san, conv, conv2)), rt=0.35)
        hw = T("He was.", sz=90, c=GLD, weight=BOLD).move_to(UP * 0.5)
        self.P(Write(hw), rt=0.5)

        # ── 18 · "Every mathematician alive today" ────────────────────
        self.cue(18)
        self.P(FadeOut(hw), rt=0.3)
        e1 = T("Every mathematician", sz=46).move_to(UP * 1.2)
        e2 = T("alive today", sz=46).next_to(e1, DOWN, buff=0.28)
        self.P(FadeIn(e1, shift=DOWN * 0.15), rt=0.4)
        self.P(FadeIn(e2, shift=DOWN * 0.15), rt=0.35)

        # ── 19 · "builds on the infinity" ──────────────────────────────
        self.cue(19)
        e3 = T("builds on the infinity", sz=46, c=BLU).next_to(e2, DOWN, buff=0.3)
        self.P(FadeIn(e3, shift=DOWN * 0.15), rt=0.4)

        # ── 20 · "he was destroyed for discovering." ───────────────────
        self.cue(20)
        e4 = T("he was destroyed", sz=50, c=RED, weight=BOLD).next_to(e3, DOWN, buff=0.35)
        e5 = T("for discovering.", sz=50, c=RED, weight=BOLD).next_to(e4, DOWN, buff=0.22)
        self.P(FadeIn(e4, shift=DOWN * 0.15), rt=0.4)
        self.P(Write(e5), rt=0.5)

        self.tail(1.5)
