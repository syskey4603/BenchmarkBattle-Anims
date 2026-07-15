from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GLD = "#FFFF00"; GRN = "#83C167"; DIM = "#2A2A3A"; AMB = "#FF9408"
CLAUDE="#E8925C"; CHATGPT="#10A37F"; GEMINI="#4285F4"; GROK="#FF4500"

# 27's Collatz trajectory (112 points, peaks at 9232)
TRAJ27 = [27,82,41,124,62,31,94,47,142,71,214,107,322,161,484,242,121,364,182,91,
274,137,412,206,103,310,155,466,233,700,350,175,526,263,790,395,1186,593,1780,890,
445,1336,668,334,167,502,251,754,377,1132,566,283,850,425,1276,638,319,958,479,1438,
719,2158,1079,3238,1619,4858,2429,7288,3644,1822,911,2734,1367,4102,2051,6154,3077,9232,4616,2308,
1154,577,1732,866,433,1300,650,325,976,488,244,122,61,184,92,46,23,70,35,106,
53,160,80,40,20,10,5,16,8,4,2,1]


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)

def cap(s, sz=32, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).to_edge(UP, buff=0.5)

def model_chip(name, color, scale=1.0):
    lbl = T(name, sz=28*scale, c=color, weight=BOLD)
    box = SurroundingRectangle(lbl, buff=0.22, corner_radius=0.12,
                               color=color, stroke_width=2.5,
                               fill_color="#15152A", fill_opacity=1)
    return VGroup(box, lbl)


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Collatz(S):
    ONSETS = [
        0.56,   #  0  "A problem a 10-year-old gets,"
        2.90,   #  1  "that no human can solve,"
        4.41,   #  2  "pick any number,"
        5.40,   #  3  "even, halve it,"
        6.66,   #  4  "odd, triple it plus 1,"
        8.40,   #  5  "repeat,"
        9.55,   #  6  "take 27,"
        10.67,  #  7  "it explodes past 9000,"
        12.60,  #  8  "crashes, climbs again,"
        14.62,  #  9  "111 steps of chaos,"
        16.72,  # 10  "then slams to 1,"
        18.53,  # 11  "every number tested falls to 1,"
        21.04,  # 12  "but nobody can prove it always will,"
        22.83,  # 13  "so we gave it to four AIs,"
        25.61,  # 14  "and here's the scary part,"
        26.46,  # 15  "none said I can't,"
        28.29,  # 16  "all four wrote confident fake proofs,"
        30.83,  # 17  "90 years unsolved,"
        31.99,  # 18  "and the AIs pretended it wasn't"
    ]

    def construct(self):
        self.setup()

        # ── 0 · "A problem a 10-year-old gets," ────────────────────────────
        h1 = T("Simple enough", sz=52).move_to(UP*0.9)
        h2 = T("for a 10-year-old.", sz=52, c=GRN, weight=BOLD).next_to(h1, DOWN, buff=0.3)
        self.cue(0)
        self.P(FadeIn(h1, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(h2, shift=DOWN*0.15), rt=0.4)

        # ── 1 · "that no human can solve," ──────────────────────────────────
        self.cue(1)
        h3 = T("No human can solve it.", sz=46, c=RED, weight=BOLD).next_to(h2, DOWN, buff=0.55)
        self.P(FadeIn(h3, shift=DOWN*0.15), rt=0.45)

        # ── 2 · "pick any number," — the RULES appear as real math ──────────
        self.cue(2)
        self.P(FadeOut(VGroup(h1, h2, h3)), rt=0.35)
        rule_hdr = cap("The rule:", sz=34, c=GRY)
        pick = T("pick any n", sz=44, c=WHT).move_to(UP*1.6)
        self.P(FadeIn(rule_hdr), rt=0.3)
        self.P(FadeIn(pick, shift=DOWN*0.15), rt=0.4)

        # ── 3 · "even, halve it," — show n/2 rule ────────────────────────────
        self.cue(3)
        even_rule = MathTex(r"n \text{ even} \;\rightarrow\; \tfrac{n}{2}",
                            font_size=46, color=BLU).move_to(UP*0.3)
        self.P(Write(even_rule), rt=0.5)

        # ── 4 · "odd, triple it plus 1," — show 3n+1 rule ────────────────────
        self.cue(4)
        odd_rule = MathTex(r"n \text{ odd} \;\rightarrow\; 3n+1",
                           font_size=46, color=AMB).next_to(even_rule, DOWN, buff=0.5)
        self.P(Write(odd_rule), rt=0.5)

        # ── 5 · "repeat," ────────────────────────────────────────────────────
        self.cue(5)
        repeat = T("repeat.", sz=40, c=GLD, weight=BOLD).next_to(odd_rule, DOWN, buff=0.5)
        self.P(FadeIn(repeat, shift=DOWN*0.15), rt=0.4)

        # ── 6 · "take 27," — set up the trajectory graph ─────────────────────
        self.cue(6)
        self.P(FadeOut(VGroup(rule_hdr, pick, even_rule, odd_rule, repeat)), rt=0.4)

        # Build axes for the hailstone plot. x = step index, y = value (log-ish scale
        # via direct linear but tall). Peak is 9232, so y up to ~9500.
        ax = Axes(
            x_range=[0, 112, 20], y_range=[0, 9500, 3000],
            x_length=6.6, y_length=6.2,
            axis_config={"include_tip": False, "color": GRY, "stroke_width": 1.6},
            y_axis_config={"include_numbers": False},
            x_axis_config={"include_numbers": False},
        ).move_to(DOWN*0.5)
        y_lbl = T("value", sz=22, c=GRY).rotate(PI/2).next_to(ax.y_axis, LEFT, buff=0.2)
        x_lbl = T("steps", sz=22, c=GRY).next_to(ax.x_axis, DOWN, buff=0.2)
        start_lbl = T("start: 27", sz=34, c=GLD, weight=BOLD).to_edge(UP, buff=0.5)

        self.P(FadeIn(start_lbl), Create(ax), FadeIn(y_lbl), FadeIn(x_lbl), rt=0.6)

        # dot at 27 (step 0)
        p0 = ax.coords_to_point(0, 27)
        dot = Dot(p0, radius=0.09, color=GLD, z_index=3)
        self.P(GrowFromCenter(dot), rt=0.3)

        # ── 7 · "it explodes past 9000," — draw path climbing to the peak ────
        self.cue(7)
        self.P(FadeOut(start_lbl), rt=0.2)
        peak_cap = cap("explodes past 9,000", sz=32, c=RED, weight=BOLD)
        # path up to the peak index (77 = value 9232)
        peak_idx = TRAJ27.index(9232)
        pts_up = [ax.coords_to_point(i, TRAJ27[i]) for i in range(peak_idx+1)]
        path_up = VMobject(color=BLU, stroke_width=2.8).set_points_as_corners(pts_up)
        peak_dot = Dot(ax.coords_to_point(peak_idx, 9232), radius=0.1, color=RED, z_index=3)
        peak_val = T("9,232", sz=28, c=RED).next_to(peak_dot, UP, buff=0.15)

        self.P(FadeIn(peak_cap), rt=0.3)
        self.P(Create(path_up), rt=1.1, rate_func=linear)
        self.P(GrowFromCenter(peak_dot), FadeIn(peak_val), rt=0.35)

        # ── 8 · "crashes, climbs again," — continue path with the chaos ──────
        self.cue(8)
        self.P(FadeOut(peak_cap), rt=0.2)
        chaos_cap = cap("crashes, climbs, chaos", sz=32, c=AMB)
        # path from peak to end
        pts_down = [ax.coords_to_point(i, TRAJ27[i]) for i in range(peak_idx, len(TRAJ27))]
        path_down = VMobject(color=AMB, stroke_width=2.8).set_points_as_corners(pts_down)
        self.P(FadeIn(chaos_cap), rt=0.3)
        self.P(Create(path_down), rt=1.3, rate_func=linear)

        # ── 9 · "111 steps of chaos," ────────────────────────────────────────
        self.cue(9)
        self.P(FadeOut(chaos_cap), rt=0.2)
        steps_cap = T("111 steps", sz=52, c=GLD, weight=BOLD).to_edge(UP, buff=0.5)
        self.P(FadeIn(steps_cap, scale=1.15), rt=0.4)

        # ── 10 · "then slams to 1," — final dot at 1 ─────────────────────────
        self.cue(10)
        self.P(FadeOut(steps_cap), rt=0.2)
        end_dot = Dot(ax.coords_to_point(len(TRAJ27)-1, 1), radius=0.12, color=GRN, z_index=4)
        end_lbl = T("= 1", sz=40, c=GRN, weight=BOLD).next_to(end_dot, UP, buff=0.2)
        slam = cap("slams to 1", sz=36, c=GRN, weight=BOLD)
        self.P(FadeIn(slam), rt=0.25)
        self.P(Flash(end_dot, color=GRN, flash_radius=0.5), GrowFromCenter(end_dot), rt=0.4)
        self.P(FadeIn(end_lbl), rt=0.3)

        # ── 11 · "every number tested falls to 1," — several small trajectories ─
        self.cue(11)
        self.P(FadeOut(VGroup(start_lbl, ax, y_lbl, x_lbl, dot, path_up, path_down,
                              peak_dot, peak_val, end_dot, end_lbl, slam)), rt=0.45)
        c11 = cap("EVERY number tested", sz=34, c=WHT)
        c11b = T("falls to 1.", sz=48, c=GRN, weight=BOLD).move_to(UP*1.5)
        # a few example numbers all arrowing down to a "1"
        one_target = T("1", sz=72, c=GRN, weight=BOLD).move_to(DOWN*2.2)
        examples = VGroup(
            T("6", sz=36, c=BLU), T("27", sz=36, c=BLU), T("97", sz=36, c=BLU),
            T("871", sz=36, c=BLU), T("6171", sz=36, c=BLU),
        ).arrange(RIGHT, buff=0.7).move_to(UP*0.2)
        arrows = VGroup(*[
            Arrow(e.get_bottom(), one_target.get_top(), color=GRY, stroke_width=2,
                  buff=0.2, max_tip_length_to_length_ratio=0.15)
            for e in examples
        ])
        self.P(FadeIn(c11), FadeIn(c11b, shift=DOWN*0.15), rt=0.4)
        self.P(LaggedStart(*[FadeIn(e) for e in examples], lag_ratio=0.1), rt=0.5)
        self.P(FadeIn(one_target, scale=1.2), rt=0.3)
        self.P(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), rt=0.6)

        # ── 12 · "but nobody can prove it always will," ─────────────────────
        self.cue(12)
        self.P(FadeOut(VGroup(c11, c11b, examples, arrows, one_target)), rt=0.4)
        np1 = T("But nobody can", sz=48).move_to(UP*0.7)
        np2 = T("prove it always will.", sz=48, c=RED, weight=BOLD).next_to(np1, DOWN, buff=0.3)
        self.P(FadeIn(np1, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(np2, shift=DOWN*0.15), rt=0.4)

        # ── 13 · "so we gave it to four AIs," — four chips ──────────────────
        self.cue(13)
        self.P(FadeOut(VGroup(np1, np2)), rt=0.35)
        c13 = cap("So we asked 4 AIs", sz=34, c=WHT)
        chips = VGroup(
            model_chip("Claude",  CLAUDE),
            model_chip("ChatGPT", CHATGPT),
            model_chip("Gemini",  GEMINI),
            model_chip("Grok",    GROK),
        ).arrange_in_grid(rows=2, cols=2, buff=0.5).move_to(DOWN*0.3)
        self.P(FadeIn(c13), rt=0.3)
        self.P(LaggedStart(*[FadeIn(c, scale=1.1) for c in chips], lag_ratio=0.12), rt=1.2)

        # ── 14 · "and here's the scary part," ────────────────────────────────
        self.cue(14)
        self.P(FadeOut(VGroup(c13, chips)), rt=0.4)
        scary = T("Here's the scary part:", sz=46, c=AMB, weight=BOLD)
        self.P(FadeIn(scary, shift=DOWN*0.15), rt=0.4)

        # ── 15 · "none said I can't," ────────────────────────────────────────
        self.cue(15)
        self.P(FadeOut(scary), rt=0.25)
        none1 = T('None said', sz=48).move_to(UP*0.7)
        none2 = T('"I can\'t."', sz=56, c=RED, weight=BOLD).next_to(none1, DOWN, buff=0.3)
        self.P(FadeIn(none1, shift=DOWN*0.15), rt=0.35)
        self.P(Write(none2), rt=0.4)

        # ── 16 · "all four wrote confident fake proofs," — fake proof doc ────
        self.cue(16)
        self.P(FadeOut(VGroup(none1, none2)), rt=0.35)
        c16 = cap("All 4 wrote", sz=32, c=WHT)
        # a mock "proof" document with lines + a big red FAKE stamp
        doc = RoundedRectangle(width=4.4, height=5.0, corner_radius=0.1,
                               fill_color="#EDE4C8", fill_opacity=1,
                               stroke_color="#B8AC88", stroke_width=2).move_to(DOWN*0.4)
        proof_title = T("Proof.", sz=26, c="#2A2A2A", weight=BOLD).move_to(doc.get_top()+DOWN*0.5)
        proof_lines = VGroup(*[
            Line(doc.get_left()+RIGHT*0.4+UP*(1.2-i*0.45),
                 doc.get_left()+RIGHT*(3.2 if i%3 else 2.4)+UP*(1.2-i*0.45),
                 color="#3A3A3A", stroke_width=2)
            for i in range(7)
        ])
        qed = MathTex(r"\therefore \; \text{QED}", font_size=30, color="#2A2A2A")
        qed.move_to(doc.get_bottom()+UP*0.6)
        self.P(FadeIn(c16), rt=0.25)
        self.P(FadeIn(doc), FadeIn(proof_title), rt=0.4)
        self.P(LaggedStart(*[Create(l) for l in proof_lines], lag_ratio=0.12), rt=0.7)
        self.P(Write(qed), rt=0.3)
        # big red FAKE stamp slams over it
        fake = T("FAKE", sz=64, c=RED, weight=BOLD).rotate(0.25).move_to(doc.get_center())
        fake_box = SurroundingRectangle(fake, buff=0.15, color=RED, stroke_width=4).rotate(0.0)
        self.P(FadeIn(VGroup(fake, fake_box), scale=1.6), rt=0.4)

        # ── 17 · "90 years unsolved," ────────────────────────────────────────
        self.cue(17)
        self.P(FadeOut(VGroup(c16, doc, proof_title, proof_lines, qed, fake, fake_box)), rt=0.4)
        yrs = T("90 years unsolved.", sz=52, c=WHT, weight=BOLD)
        self.P(FadeIn(yrs, shift=DOWN*0.15), rt=0.4)

        # ── 18 · "and the AIs pretended it wasn't" ──────────────────────────
        self.cue(18)
        self.P(FadeOut(yrs), rt=0.3)
        f1 = T("The AIs just", sz=48).move_to(UP*0.7)
        f2 = T("pretended it wasn't.", sz=50, c=RED, weight=BOLD).next_to(f1, DOWN, buff=0.3)
        self.P(FadeIn(f1, shift=DOWN*0.15), rt=0.4)
        self.P(Write(f2), rt=0.45)

        self.tail(1.0)
