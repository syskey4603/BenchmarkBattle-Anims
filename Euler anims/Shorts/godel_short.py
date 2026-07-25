# godel_short.py — Gödel's Incompleteness Theorem, pure math explainer, 53.7 s
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
    return Text(s, font_size=sz, color=c, **kw).to_edge(UP, buff=0.5)

def card(mob, stroke=GRY, fill="#15152A", buff=0.28):
    box = SurroundingRectangle(mob, buff=buff, corner_radius=0.15,
                               color=stroke, stroke_width=2.3,
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


class Godel(S):
    ONSETS = [
        0.77,   #  0  "In 1931,"
        1.71,   #  1  "Kurt Gödel proved something that changed mathematics forever."
        4.47,   #  2  "Take any formal system"
        5.87,   #  3  "built on consistent axioms,"
        7.26,   #  4  "powerful enough to describe basic arithmetic."
        9.31,   #  5  "Gödel found a way to make that system"
        11.02,  #  6  "talk about itself,"
        12.13,  #  7  "by turning every statement into a number."
        14.36,  #  8  "Once statements become numbers,"
        16.07,  #  9  "the system can make statements about its own statements."
        18.51,  # 10  "So Gödel constructed one specific statement."
        20.67,  # 11  "Call it G."
        21.90,  # 12  "G asserts this:"
        23.03,  # 13  "I am not provable in this system."
        25.56,  # 14  "Now follow the logic."
        26.70,  # 15  "Suppose the system can prove G."
        28.92,  # 16  "Then it just proved a statement claiming it has no proof,"
        30.00,  # 17  "so it proved something false."
        32.05,  # 18  "Suppose instead the system cannot prove G."
        34.33,  # 19  "Then G's claim about itself is correct,"
        36.84,  # 20  "which makes G true,"
        38.49,  # 21  "but unprovable inside the system."
        40.60,  # 22  "So if the system is consistent,"
        43.39,  # 23  "G is true and unprovable,"
        44.31,  # 24  "at the same time, forever."
        46.40,  # 25  "Any consistent system"
        47.41,  # 26  "strong enough for arithmetic"
        49.10,  # 27  "contains true statements"
        51.27,  # 28  "it can never prove."
    ]

    def construct(self):
        self.setup()

        # ── 0 · "In 1931," ────────────────────────────────────────────────
        yr = T("1931", sz=100, c=GLD, weight=BOLD)
        self.cue(0)
        self.P(FadeIn(yr, shift=DOWN*0.2), rt=0.35)

        # ── 1 · "Kurt Gödel proved something that changed mathematics forever." ─
        self.cue(1)
        self.P(FadeOut(yr), rt=0.25)
        name = T("Kurt Gödel", sz=56, c=GLD, weight=BOLD).move_to(UP*1.0)
        sub = T("proved something that", sz=36, c=WHT).next_to(name, DOWN, buff=0.4)
        sub2 = T("changed mathematics forever.", sz=36, c=WHT).next_to(sub, DOWN, buff=0.2)
        self.P(FadeIn(name, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(sub, shift=DOWN*0.1), rt=0.35)
        self.P(FadeIn(sub2, shift=DOWN*0.1), rt=0.35)

        # ══ SCENE: THE FORMAL SYSTEM (beats 2-4) ════════════════════════════
        # A persistent container that axioms drop into — builds progressively.
        self.cue(2)
        self.P(FadeOut(VGroup(name, sub, sub2)), rt=0.35)

        sys_box = RoundedRectangle(width=5.6, height=3.9, corner_radius=0.2,
                                   stroke_color=BLU, stroke_width=3,
                                   fill_color="#12122A", fill_opacity=1).move_to(UP*0.2)
        sys_lbl = T("formal system", sz=30, c=BLU).next_to(sys_box, UP, buff=0.3)
        self.P(Create(sys_box), FadeIn(sys_lbl), rt=0.5)

        # ── 3 · "built on consistent axioms," — axiom symbols drop in ────────
        self.cue(3)
        axioms = VGroup(
            MathTex(r"\vdash", font_size=40, color=WHT),
            MathTex(r"\forall x", font_size=36, color=WHT),
            MathTex(r"\exists y", font_size=36, color=WHT),
            MathTex(r"P \Rightarrow Q", font_size=36, color=WHT),
        ).arrange_in_grid(rows=2, cols=2, buff=0.55).move_to(sys_box.get_center()+UP*0.85)
        consist_lbl = T("consistent", sz=24, c=GRN).next_to(axioms, DOWN, buff=0.3)
        self.P(LaggedStart(*[FadeIn(a, scale=1.2) for a in axioms], lag_ratio=0.2), rt=0.7)
        self.P(FadeIn(consist_lbl), rt=0.3)

        # ── 4 · "powerful enough to describe basic arithmetic." ─────────────
        self.cue(4)
        arith = MathTex(r"1+1=2", font_size=30, color=AMB).next_to(consist_lbl, DOWN, buff=0.3)
        self.P(FadeIn(arith, shift=DOWN*0.1), rt=0.5)

        # ══ SCENE: GÖDEL NUMBERING — statements become numbers (beats 5-9) ══
        self.cue(5)
        self.P(FadeOut(VGroup(sys_box, sys_lbl, axioms, consist_lbl, arith)), rt=0.4)
        c5 = cap("Gödel found a way", sz=34, c=WHT)
        c5b = T("to make it talk", sz=34, c=WHT).next_to(c5, DOWN, buff=0.2)
        self.P(FadeIn(c5), FadeIn(c5b), rt=0.4)

        # ── 6 · "talk about itself," ─────────────────────────────────────
        self.cue(6)
        c6 = T("about itself.", sz=40, c=GLD, weight=BOLD).next_to(c5b, DOWN, buff=0.3)
        self.P(FadeIn(c6, shift=DOWN*0.1), rt=0.4)

        # ── 7 · "by turning every statement into a number." — the key visual ─
        self.cue(7)
        self.P(FadeOut(VGroup(c5, c5b, c6)), rt=0.35)

        stmt = MathTex(r"\forall x\,(P(x)\Rightarrow Q(x))", font_size=40, color=WHT)
        stmt_box = card(stmt, stroke=WHT)
        stmt_grp = VGroup(stmt_box, stmt).move_to(UP*1.6)

        arrow = Arrow(UP*0.4, DOWN*0.2, color=GLD, stroke_width=4,
                     max_tip_length_to_length_ratio=0.25).next_to(stmt_grp, DOWN, buff=0.35)
        arrow_lbl = T("encode", sz=22, c=GLD).next_to(arrow, RIGHT, buff=0.2)

        num = T("2,431,907,558", sz=40, c=GLD, weight=BOLD)
        num_box = card(num, stroke=GLD, fill="#1A1800")
        num_grp = VGroup(num_box, num).next_to(arrow, DOWN, buff=0.35)

        self.P(FadeIn(stmt_grp), rt=0.5)
        self.P(GrowArrow(arrow), FadeIn(arrow_lbl), rt=0.4)
        self.P(FadeIn(num_grp, shift=UP*0.15), rt=0.5)

        # ── 8 · "Once statements become numbers," ───────────────────────────
        self.cue(8)
        c8 = cap("statements → numbers", sz=32, c=GLD)
        self.P(FadeIn(c8), rt=0.4)

        # ── 9 · "the system can make statements about its own statements." ──
        self.cue(9)
        self.P(FadeOut(c8), rt=0.25)
        # the number feeds back INTO the statement box — visualizing self-reference
        feedback = CurvedArrow(num_grp.get_left()+LEFT*0.1, stmt_grp.get_left()+LEFT*0.1,
                               color=PRP, angle=-PI*0.9)
        fb_lbl = T("math can talk", sz=26, c=PRP).next_to(feedback, LEFT, buff=0.15).rotate(PI/2)
        self.P(Create(feedback), rt=0.5)
        self.P(FadeIn(fb_lbl), rt=0.3)
        talk_lbl = T("about math.", sz=30, c=PRP, weight=BOLD).next_to(num_grp, DOWN, buff=0.5)
        self.P(FadeIn(talk_lbl, shift=DOWN*0.1), rt=0.4)

        # ══ SCENE: THE STATEMENT G (beats 10-14) ════════════════════════════
        self.cue(10)
        self.P(FadeOut(VGroup(stmt_grp, arrow, arrow_lbl, num_grp, feedback, fb_lbl, talk_lbl)),
               rt=0.45)
        c10 = cap("Gödel built one", sz=34, c=WHT)
        c10b = T("specific statement.", sz=38, c=WHT).next_to(c10, DOWN, buff=0.25)
        self.P(FadeIn(c10), FadeIn(c10b), rt=0.5)

        # ── 11 · "Call it G." ────────────────────────────────────────────
        self.cue(11)
        self.P(FadeOut(VGroup(c10, c10b)), rt=0.3)
        g_lbl = T("G", sz=90, c=GLD, weight=BOLD).move_to(UP*1.2)
        self.P(Write(g_lbl), rt=0.5)

        # ── 12 · "G asserts this:" ───────────────────────────────────────
        self.cue(12)
        asserts = T("asserts:", sz=34, c=GRY).next_to(g_lbl, DOWN, buff=0.3)
        self.P(FadeIn(asserts), rt=0.4)

        # ── 13 · "I am not provable in this system." — self-reference loop ──
        self.cue(13)
        self.P(FadeOut(asserts), rt=0.25)
        g_stmt = T('"I am not provable', sz=32, c=WHT).next_to(g_lbl, DOWN, buff=0.4)
        g_stmt2 = T('in this system."', sz=32, c=WHT).next_to(g_stmt, DOWN, buff=0.15)
        g_grp = VGroup(g_stmt, g_stmt2)
        # curling self-reference arrow: from the end of the statement back up to G
        loop = CurvedArrow(g_grp.get_right()+RIGHT*0.15, g_lbl.get_right()+RIGHT*0.15,
                           color=RED, angle=-PI*0.85)
        self.P(FadeIn(g_grp), rt=0.5)
        self.P(Create(loop), rt=0.55)

        # ══ SCENE: THE TWO-BRANCH PROOF (beats 14-21) ═══════════════════════
        self.cue(14)
        self.P(FadeOut(VGroup(g_lbl, g_stmt, g_stmt2, loop)), rt=0.4)
        logic_hdr = T("Follow the logic.", sz=44, c=WHT, weight=BOLD)
        self.P(FadeIn(logic_hdr, shift=DOWN*0.15), rt=0.4)

        # ── 15 · "Suppose the system can prove G." — fork begins ────────────
        self.cue(15)
        self.P(FadeOut(logic_hdr), rt=0.3)
        fork_root = T("Can the system prove G?", sz=32, c=WHT).move_to(UP*5.4)
        branch_l = Line(fork_root.get_bottom(), fork_root.get_bottom()+DOWN*0.8+LEFT*2.3,
                        color=GRY, stroke_width=2.5)
        branch_r = Line(fork_root.get_bottom(), fork_root.get_bottom()+DOWN*0.8+RIGHT*2.3,
                        color=GRY, stroke_width=2.5)
        yes_lbl = T("YES", sz=26, c=GRN).next_to(branch_l.get_end(), DOWN, buff=0.15)
        no_lbl = T("NO", sz=26, c=RED).next_to(branch_r.get_end(), DOWN, buff=0.15)
        self.P(FadeIn(fork_root), rt=0.4)
        self.P(Create(branch_l), Create(branch_r), rt=0.5)
        self.P(FadeIn(yes_lbl), FadeIn(no_lbl), rt=0.35)

        # ── 16 · "Then it just proved a statement claiming it has no proof," ─
        self.cue(16)
        yes_txt1 = T("proves a statement", sz=24, c=GRY).next_to(yes_lbl, DOWN, buff=0.35)
        yes_txt2 = T("claiming no proof exists", sz=22, c=GRY).next_to(yes_txt1, DOWN, buff=0.12)
        self.P(FadeIn(yes_txt1), FadeIn(yes_txt2), rt=0.5)

        # ── 17 · "so it proved something false." — branch 1 resolves ────────
        self.cue(17)
        yes_result = T("PROVED FALSE", sz=26, c=RED, weight=BOLD).next_to(yes_txt2, DOWN, buff=0.3)
        yes_x = T("✗ inconsistent", sz=22, c=RED).next_to(yes_result, DOWN, buff=0.15)
        self.P(FadeIn(yes_result, scale=1.15), rt=0.4)
        self.P(FadeIn(yes_x), rt=0.35)

        # ── 18 · "Suppose instead the system cannot prove G." ───────────────
        self.cue(18)
        no_txt1 = T("system has no", sz=24, c=GRY).next_to(no_lbl, DOWN, buff=0.35)
        no_txt2 = T("proof of G", sz=22, c=GRY).next_to(no_txt1, DOWN, buff=0.12)
        self.P(FadeIn(no_txt1), FadeIn(no_txt2), rt=0.5)

        # ── 19 · "Then G's claim about itself is correct," ──────────────────
        self.cue(19)
        no_result = T("G IS RIGHT", sz=26, c=GRN, weight=BOLD).next_to(no_txt2, DOWN, buff=0.3)
        self.P(FadeIn(no_result, scale=1.15), rt=0.5)

        # ── 20 · "which makes G true," ───────────────────────────────────
        self.cue(20)
        no_check = T("G is TRUE", sz=24, c=GRN).next_to(no_result, DOWN, buff=0.2)
        self.P(FadeIn(no_check), rt=0.4)

        # ── 21 · "but unprovable inside the system." ────────────────────────
        self.cue(21)
        no_unpr = T("but unprovable", sz=22, c=AMB).next_to(no_check, DOWN, buff=0.15)
        self.P(FadeIn(no_unpr), rt=0.45)

        # ══ SCENE: CONVERGENCE — the resolved paradox (beats 22-24) ═════════
        self.cue(22)
        self.P(FadeOut(VGroup(fork_root, branch_l, branch_r, yes_lbl, yes_txt1, yes_txt2,
                              yes_result, yes_x, no_lbl, no_txt1, no_txt2, no_result,
                              no_check, no_unpr)), rt=0.5)
        consist_stmt = T("If the system is consistent...", sz=36, c=WHT).move_to(UP*1.0)
        self.P(FadeIn(consist_stmt, shift=DOWN*0.15), rt=0.5)

        # ── 23 · "G is true and unprovable," ─────────────────────────────
        self.cue(23)
        result1 = T("G is TRUE", sz=48, c=GRN, weight=BOLD).next_to(consist_stmt, DOWN, buff=0.5)
        result2 = T("and UNPROVABLE.", sz=48, c=RED, weight=BOLD).next_to(result1, DOWN, buff=0.25)
        self.P(FadeIn(result1, shift=DOWN*0.1), rt=0.4)
        self.P(FadeIn(result2, shift=DOWN*0.1), rt=0.45)

        # ── 24 · "at the same time, forever." ────────────────────────────
        self.cue(24)
        forever = T("Both. Forever.", sz=34, c=GLD, weight=BOLD).next_to(result2, DOWN, buff=0.5)
        self.P(FadeIn(forever, shift=DOWN*0.1), rt=0.45)

        # ══ SCENE: THE GENERAL THEOREM (beats 25-28) ════════════════════════
        self.cue(25)
        self.P(FadeOut(VGroup(consist_stmt, result1, result2, forever)), rt=0.45)
        gen1 = T("Any consistent system", sz=40, c=WHT).move_to(UP*1.4)
        self.P(FadeIn(gen1, shift=DOWN*0.15), rt=0.4)

        # ── 26 · "strong enough for arithmetic" ──────────────────────────
        self.cue(26)
        gen2 = T("strong enough for arithmetic", sz=36, c=BLU).next_to(gen1, DOWN, buff=0.3)
        self.P(FadeIn(gen2, shift=DOWN*0.1), rt=0.5)

        # ── 27 · "contains true statements" ──────────────────────────────
        self.cue(27)
        gen3 = T("contains true statements", sz=40, c=GLD, weight=BOLD).next_to(gen2, DOWN, buff=0.4)
        self.P(FadeIn(gen3, shift=DOWN*0.1), rt=0.5)

        # ── 28 · "it can never prove." ────────────────────────────────────
        self.cue(28)
        gen4 = T("it can never prove.", sz=44, c=RED, weight=BOLD).next_to(gen3, DOWN, buff=0.4)
        self.P(Write(gen4), rt=0.6)

        self.tail(2.2)
