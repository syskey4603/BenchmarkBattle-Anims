from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT  = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"
BLU  = "#58C4DD"; GLD = "#FFFF00"; DIM = "#3A3A5A"
CLAU = "#E8925C"; GROK = "#FF4500"; GRN = "#83C167"; AMB = "#FF9408"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)

def Eq(s, sz=80, c=WHT):
    return MathTex(s, font_size=sz, color=c)


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class ClaudeCantSolve(S):
    ONSETS = [
        0.00,   # 0  "Claude is ranked the best AI for coding and reasoning."
        2.99,   # 1  "I gave it a graph theory problem."
        4.78,   # 2  "It tried to solve it by checking every possible answer."
        7.47,   # 3  "A 40-node network has 10^61 possible spanning trees."
        12.06,  # 4  "For context — atoms in the observable universe? 10^80."
        16.84,  # 5  [dramatic pause — spinner starts]
        18.42,  # 6  "Claude was still running hours later."
        20.36,  # 7  "Grok solved the same problem in milliseconds —"
        22.93,  # 8  "using an algorithm published in 1956."
        25.76,  # 9  "The most advanced AI in the world."
        28.54,  # 10 "Beaten by a textbook from seventy years ago."
    ]

    def make_graph(self, center=DOWN*0.3, r=1.4):
        pos = [center + r*np.array([np.cos(PI/2 + i*2*PI/6),
                                     np.sin(PI/2 + i*2*PI/6), 0])
               for i in range(6)]
        nodes = VGroup(*[Dot(p, radius=0.16, color=BLU, z_index=2) for p in pos])
        epairs = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,2),(1,4),(2,5)]
        edges  = VGroup(*[Line(pos[i], pos[j], color=DIM, stroke_width=2)
                          for i,j in epairs])
        return nodes, edges, pos, epairs

    def construct(self):
        self.setup()

        # 0 — Claude = #1 hook
        cl   = T("CLAUDE", sz=120, c=CLAU, weight=BOLD).move_to(UP*1.8)
        sub  = T("#1 AI for coding and reasoning", sz=34, c=GRY).next_to(cl, DOWN, buff=0.3)
        tag  = T("so they say.", sz=38, c=WHT).next_to(sub, DOWN, buff=0.28)

        self.cue(0)
        self.P(Write(cl), rt=0.5)
        self.P(FadeIn(sub, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(tag, shift=DOWN*0.15), rt=0.35)
        self.W(1.9)

        # 1 — graph theory problem: small network appears
        self.cue(1)
        self.P(FadeOut(VGroup(cl, sub, tag)), rt=0.3)

        nodes, edges, pos, epairs = self.make_graph()
        glbl = T("graph theory problem", sz=38, c=GRY).move_to(DOWN*3.8)
        lbl2 = T("(40 nodes in the real thing)", sz=28, c=DIM).next_to(glbl, DOWN, buff=0.2)

        self.P(Create(edges), rt=0.4)
        self.P(LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.06), rt=0.4)
        self.P(FadeIn(glbl), FadeIn(lbl2), rt=0.3)
        self.W(0.35)

        # 2 — checking every possible answer: spanning trees flash
        self.cue(2)
        brute = T("brute force:", sz=48, c=RED, weight=BOLD).move_to(UP*5.5)
        check = T("check every spanning tree", sz=36).next_to(brute, DOWN, buff=0.25)
        self.P(FadeIn(brute), FadeIn(check), rt=0.35)

        # flash 4 different spanning tree subsets on the same graph
        tree_subsets = [
            [(0,1),(1,2),(2,3),(3,4),(4,5)],
            [(0,2),(2,5),(5,4),(4,3),(3,1)],
            [(0,5),(5,2),(2,1),(1,4),(4,3)],
            [(0,1),(0,2),(2,3),(3,4),(4,5)],
        ]
        for ts in tree_subsets:
            hl = VGroup(*[Line(pos[i], pos[j], color=GLD,
                               stroke_width=5, z_index=1) for i,j in ts])
            self.P(FadeIn(hl), rt=0.18)
            self.P(FadeOut(hl), rt=0.12)

        count = T("1 ... 2 ... 3 ...", sz=40, c=RED).move_to(UP*4.2)
        self.P(FadeIn(count), rt=0.3)
        self.W(0.44)

        # 3 — 10^61 SLAMS IN (the big reveal)
        self.cue(3)
        self.P(FadeOut(VGroup(nodes, edges, glbl, lbl2, brute, check, count)), rt=0.3)

        big_num  = Eq(r"10^{61}", sz=210, c=RED).move_to(UP*1.0)
        lbl_a    = T("possible spanning trees", sz=38).move_to(DOWN*1.8)
        lbl_b    = T("in a 40-node network",   sz=32, c=GRY).next_to(lbl_a, DOWN, buff=0.2)

        self.P(Write(big_num), rt=0.5)
        # little shake for emphasis
        self.P(big_num.animate.shift(RIGHT*0.1), rt=0.06)
        self.P(big_num.animate.shift(LEFT*0.2), rt=0.06)
        self.P(big_num.animate.shift(RIGHT*0.1), rt=0.06)
        self.P(FadeIn(lbl_a, shift=UP*0.2), FadeIn(lbl_b, shift=UP*0.2),
               lag_ratio=0.3, rt=0.4)
        self.W(3.25)

        # 4 — universe comparison: side by side
        self.cue(4)
        self.P(FadeOut(VGroup(big_num, lbl_a, lbl_b)), rt=0.3)

        ctx  = T("For context:", sz=48, c=GRY).move_to(UP*5.5)
        n1   = Eq(r"10^{61}", sz=110, c=RED).move_to(UP*3.0 + LEFT*1.9)
        l1   = T("spanning trees", sz=28, c=RED).next_to(n1, DOWN, buff=0.18)
        n2   = Eq(r"10^{80}", sz=110, c=BLU).move_to(UP*3.0 + RIGHT*1.9)
        l2   = T("atoms in universe", sz=28, c=BLU).next_to(n2, DOWN, buff=0.18)
        vs   = T("vs", sz=42, c=GRY).move_to(UP*3.0)
        note = T("both are incomprehensibly large", sz=30, c=GRY).move_to(UP*0.8)

        self.P(FadeIn(ctx), rt=0.4)
        self.P(Write(n1), FadeIn(l1), rt=0.5)
        self.P(FadeIn(vs), rt=0.2)
        self.P(Write(n2), FadeIn(l2), rt=0.5)
        self.P(FadeIn(note, shift=UP*0.15), rt=0.4)
        self.W(2.58)

        # 5 — dramatic pause: loading spinner fills the silence
        self.cue(5)
        self.P(FadeOut(VGroup(ctx, n1, l1, vs, n2, l2, note)), rt=0.3)

        spinner = Arc(radius=0.75, start_angle=PI/2, angle=-TAU*0.78,
                      color=CLAU, stroke_width=12).move_to(ORIGIN)
        self.P(Create(spinner), rt=0.4)
        # rotate through the 1.58s silence
        self.P(Rotate(spinner, TAU, about_point=ORIGIN, rate_func=linear), rt=0.88)

        # 6 — "Claude was still running"
        self.cue(6)
        cl2  = T("CLAUDE", sz=62, c=CLAU, weight=BOLD).move_to(DOWN*1.6)
        dots = T("still running...", sz=40, c=GRY).move_to(DOWN*2.6)
        self.P(FadeIn(cl2), FadeIn(dots),
               Rotate(spinner, TAU, about_point=ORIGIN, rate_func=linear),
               rt=1.0)
        self.W(0.94)

        # 7 — Grok milliseconds
        self.cue(7)
        self.P(FadeOut(VGroup(spinner, cl2, dots)), rt=0.3)

        gr   = T("GROK", sz=110, c=GROK, weight=BOLD).move_to(UP*3.8)
        ms   = T("12 ms", sz=130, c=GRN, weight=BOLD).move_to(UP*1.6)
        tick = T("correct answer", sz=38, c=GRN).next_to(ms, DOWN, buff=0.28)

        self.P(Write(gr), rt=0.45)
        self.P(Write(ms), rt=0.4)
        self.P(FadeIn(tick), rt=0.3)
        self.W(1.12)

        # 8 — Kruskal's / 1956
        self.cue(8)
        alg = T("Kruskal's Algorithm", sz=48, c=AMB).move_to(DOWN*1.7)
        yr  = T("Published  1956", sz=40, c=GRY).next_to(alg, DOWN, buff=0.25)
        self.P(FadeIn(alg, shift=UP*0.2), rt=0.45)
        self.P(FadeIn(yr),  rt=0.35)
        self.W(2.03)

        # 9 — "most advanced AI in the world"
        self.cue(9)
        self.P(FadeOut(VGroup(gr, ms, tick, alg, yr)), rt=0.3)

        a1 = T("The most advanced", sz=56).move_to(UP*1.6)
        a2 = T("AI in the world.",  sz=56).next_to(a1, DOWN, buff=0.3)
        self.P(FadeIn(a1, shift=UP*0.2), rt=0.45)
        self.P(FadeIn(a2, shift=UP*0.2), rt=0.4)
        self.W(1.63)

        # 10 — punchline: beaten by a textbook
        self.cue(10)
        self.P(FadeOut(VGroup(a1, a2)), rt=0.3)

        p1  = T("Beaten by a textbook", sz=58, c=RED, weight=BOLD).move_to(UP*2.5)
        p2  = T("from 70 years ago.",   sz=52).next_to(p1, DOWN, buff=0.35)
        yr2 = T("1956", sz=160, c=GLD, weight=BOLD).move_to(DOWN*1.6)

        self.P(FadeIn(p1, shift=UP*0.2), rt=0.45)
        self.P(FadeIn(p2), rt=0.35)
        self.P(Write(yr2), rt=0.45)
        self.tail(1.5)
