from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GLD = "#FFFF00"; GRN = "#83C167"; DIM = "#2A2A3A"; AMB = "#FF9408"
CGPT = "#10A37F"; GPT4_COL = "#AB68FF"


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


class ConfidentWrong(S):
    ONSETS = [
        0.03,   #  0  "GPT-4 gives more confident answers than GPT-3.5."
        4.82,   #  1  "It's also more confidently wrong."
        6.79,   #  2  "Why?"
        7.42,   #  3  "Bigger models are trained on human feedback."
        10.04,  #  4  "Raters can't verify hard answers —"
        12.02,  #  5  "so they reward confident fluent responses."
        14.54,  #  6  "The model learns: certainty scores better than accuracy."
        17.55,  #  7  "Scale increases how right it sounds faster than how right it is."
        21.50,  #  8  "The gap between those two things is the danger zone."
        24.01,  #  9  "The most dangerous AI isn't the one that says I don't know."
        27.06,  # 10  "It's the one that never does."
    ]

    def construct(self):
        self.setup()

        # ── 0 · "GPT-4 gives more confident answers than GPT-3.5." ──────────
        lbl35 = T("GPT-3.5", sz=38, c=CGPT, weight=BOLD).move_to(UP*4.2 + LEFT*1.9)
        box35 = card(lbl35, stroke=CGPT)
        ans35 = T('"I think it might\nbe around 1832…"', sz=28, c=GRY)
        ans35.next_to(VGroup(box35, lbl35), DOWN, buff=0.4)

        lbl4 = T("GPT-4", sz=38, c=GPT4_COL, weight=BOLD).move_to(UP*4.2 + RIGHT*1.9)
        box4 = card(lbl4, stroke=GPT4_COL)
        ans4 = T('"It is definitively\n1832."', sz=28, c=WHT)
        ans4.next_to(VGroup(box4, lbl4), DOWN, buff=0.4)

        self.cue(0)
        self.P(Create(box35), FadeIn(lbl35), rt=0.4)
        self.P(FadeIn(ans35, shift=DOWN*0.1), rt=0.4)
        self.P(Create(box4), FadeIn(lbl4), rt=0.4)
        self.P(FadeIn(ans4, shift=DOWN*0.1), rt=0.4)

        # ── 1 · "It's also more confidently wrong." ──────────────────────────
        self.cue(1)
        wrong  = T("WRONG.", sz=58, c=RED, weight=BOLD).move_to(ans4.get_center())
        x_mark = Cross(VGroup(box4, lbl4), color=RED, stroke_width=5)
        self.P(FadeOut(ans4), rt=0.2)
        self.P(Write(wrong), rt=0.35)
        self.P(Create(x_mark), rt=0.35)

        # ── 2 · "Why?"  (0.63 s) ─────────────────────────────────────────────
        self.cue(2)
        self.P(FadeOut(VGroup(box35, lbl35, ans35, box4, lbl4, wrong, x_mark)), rt=0.25)
        why = T("Why?", sz=110, c=GLD, weight=BOLD).move_to(UP * 0.5)
        self.P(Write(why), rt=0.35)

        # ── 3 · "Bigger models are trained on human feedback." ───────────────
        self.cue(3)
        self.P(FadeOut(why), rt=0.25)
        b1 = T("Bigger models",      sz=52).move_to(UP * 5.5)
        b2 = T("are trained on",     sz=46, c=GRY).next_to(b1, DOWN, buff=0.25)
        b3 = T("human feedback.",    sz=52, c=AMB, weight=BOLD).next_to(b2, DOWN, buff=0.25)
        self.P(FadeIn(b1, shift=DOWN*0.15), rt=0.35)
        self.P(FadeIn(b2, shift=DOWN*0.15), rt=0.3)
        self.P(FadeIn(b3, shift=DOWN*0.15), rt=0.35)

        rater_lbl = T("HUMAN RATER", sz=30, c=GLD)
        rater_box = card(rater_lbl, stroke=GLD, fill="#1A1800")
        rater = VGroup(rater_box, rater_lbl).move_to(DOWN * 1.4)
        self.P(FadeIn(rater, shift=DOWN*0.1), rt=0.4)

        # ── 4 · "Raters can't verify hard answers —" ─────────────────────────
        self.cue(4)
        self.P(FadeOut(VGroup(b1, b2, b3)), rt=0.25)
        r1 = T("Raters can't",         sz=50).move_to(UP * 5.5)
        r2 = T("verify hard answers.", sz=46, c=RED).next_to(r1, DOWN, buff=0.25)
        self.P(FadeIn(r1, shift=DOWN*0.15), rt=0.35)
        self.P(FadeIn(r2, shift=DOWN*0.15), rt=0.35)

        # ── 5 · "so they reward confident fluent responses." ─────────────────
        self.cue(5)
        self.P(FadeOut(VGroup(r1, r2)), rt=0.25)
        s1 = T("So they reward",      sz=50).move_to(UP * 5.5)
        s2 = T("confident fluent",    sz=50, c=GPT4_COL).next_to(s1, DOWN, buff=0.25)
        s3 = T("responses.",          sz=50, c=GPT4_COL).next_to(s2, DOWN, buff=0.2)
        self.P(FadeIn(s1, shift=DOWN*0.15), rt=0.35)
        self.P(FadeIn(s2, shift=DOWN*0.15), rt=0.3)
        self.P(FadeIn(s3, shift=DOWN*0.15), rt=0.3)

        # ── 6 · "certainty scores better than accuracy" — bars appear ────────
        self.cue(6)
        self.P(FadeOut(VGroup(rater, s1, s2, s3)), rt=0.35)

        bw = 0.88; gap_i = 0.14; base_y = -3.0
        H = {"35c": 1.55, "35a": 1.40, "4c": 3.30, "4a": 1.85}

        def bar(h, col, x):
            r = Rectangle(width=bw, height=h, fill_color=col,
                          fill_opacity=0.88, stroke_width=0)
            r.align_to(DOWN * abs(base_y), DOWN).shift(RIGHT * x)
            return r

        x35c = -1.75; x35a = x35c + bw + gap_i
        x4c  =  0.65; x4a  = x4c  + bw + gap_i

        b35c = bar(H["35c"], BLU,  x35c)
        b35a = bar(H["35a"], GRN,  x35a)
        b4c  = bar(H["4c"],  BLU,  x4c)
        b4a  = bar(H["4a"],  GRN,  x4a)

        def bar_lbl(txt, col, rect, direction=UP):
            l = T(txt, sz=22, c=col)
            l.next_to(rect, direction, buff=0.15)
            return l

        l35c = bar_lbl("confident", BLU, b35c)
        l35a = bar_lbl("accurate",  GRN, b35a)
        l4c  = bar_lbl("confident", BLU, b4c)
        l4a  = bar_lbl("accurate",  GRN, b4a)

        g35 = T("GPT-3.5", sz=28, c=CGPT,     weight=BOLD).move_to(RIGHT*(x35c+(bw*2+gap_i)/2)+DOWN*4.2)
        g4  = T("GPT-4",   sz=28, c=GPT4_COL, weight=BOLD).move_to(RIGHT*(x4c +(bw*2+gap_i)/2)+DOWN*4.2)

        cert1 = T("Certainty scores better", sz=36).move_to(UP * 5.5)
        cert2 = T("than accuracy.",          sz=42, c=RED, weight=BOLD).next_to(cert1, DOWN, buff=0.2)

        self.P(FadeIn(cert1, shift=DOWN*0.15), rt=0.35)
        self.P(FadeIn(cert2, shift=DOWN*0.15), rt=0.3)
        self.P(FadeIn(g35), FadeIn(g4), rt=0.3)
        self.P(GrowFromEdge(b35c, DOWN), GrowFromEdge(b35a, DOWN),
               GrowFromEdge(b4c,  DOWN), GrowFromEdge(b4a,  DOWN), rt=0.55)
        self.P(FadeIn(l35c), FadeIn(l35a), FadeIn(l4c), FadeIn(l4a), rt=0.3)

        # ── 7 · "sounds right faster than is right" — gap revealed ───────────
        self.cue(7)
        self.P(FadeOut(VGroup(cert1, cert2)), rt=0.25)

        gap_h = H["4c"] - H["4a"]
        gap_rect = Rectangle(
            width=bw * 2 + gap_i, height=gap_h,
            fill_color=RED, fill_opacity=0.22,
            stroke_color=RED, stroke_width=1.8
        )
        # top of gap_rect = top of conf bar; bottom = top of acc bar
        gap_rect.move_to(
            RIGHT * (x4c + (bw*2+gap_i)/2) +
            DOWN  * (abs(base_y) - H["4a"] - gap_h/2)
        )

        sc1 = T("Sounds right ↑",  sz=44, c=BLU).move_to(UP * 5.5)
        sc2 = T("faster than",     sz=40, c=GRY).next_to(sc1, DOWN, buff=0.22)
        sc3 = T("is right ↑",      sz=44, c=GRN).next_to(sc2, DOWN, buff=0.22)

        self.P(FadeIn(sc1, shift=DOWN*0.15), rt=0.35)
        self.P(FadeIn(sc2, shift=DOWN*0.15), rt=0.28)
        self.P(FadeIn(sc3, shift=DOWN*0.15), rt=0.28)
        self.P(FadeIn(gap_rect), rt=0.5)

        # ── 8 · "the gap is the danger zone" ─────────────────────────────────
        self.cue(8)
        self.P(FadeOut(VGroup(sc1, sc2, sc3)), rt=0.25)
        dz = T("DANGER ZONE", sz=52, c=RED, weight=BOLD).move_to(UP * 5.5)
        arrow = Arrow(
            dz.get_bottom() + DOWN*0.1,
            gap_rect.get_top() + UP*0.08,
            color=RED, stroke_width=3, buff=0.05,
            max_tip_length_to_length_ratio=0.2
        )
        self.P(Write(dz), rt=0.4)
        self.P(Create(arrow), rt=0.4)

        # ── 9 · "most dangerous AI isn't the one that says I don't know" ──────
        self.cue(9)
        self.P(FadeOut(VGroup(
            b35c, b35a, l35c, l35a, g35,
            b4c,  b4a,  l4c,  l4a,  g4,
            gap_rect, dz, arrow
        )), rt=0.4)

        idk = T('"I don\'t know."', sz=54, c=GRY).move_to(UP * 2.0)
        safe_lbl = T("✓  SAFE", sz=40, c=GRN).next_to(idk, DOWN, buff=0.35)
        self.P(FadeIn(idk,     shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(safe_lbl, shift=DOWN*0.1), rt=0.35)

        # ── 10 · "It's the one that never does." ──────────────────────────────
        self.cue(10)
        self.P(FadeOut(VGroup(idk, safe_lbl)), rt=0.25)
        f1 = T("It's the one",     sz=58).move_to(UP * 1.6)
        f2 = T("that never does.", sz=66, c=RED, weight=BOLD).next_to(f1, DOWN, buff=0.38)
        self.P(FadeIn(f1, shift=DOWN*0.15), rt=0.35)
        self.P(Write(f2), rt=0.45)

        self.tail(1.5)
