# widgets_short.py — continuous motion, no static holds, 30.66 s
from manim import *
import numpy as np

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; BLU = "#58C4DD"
GLD = "#FFFF00"; GRN = "#83C167"; DIM = "#2A2A3A"; AMB = "#FF9408"
CGPT = "#10A37F"; ELEC = "#4FE3FF"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)

def top_cap(s, sz=36, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(UP*6.3)

def bottom_cap(s, sz=34, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(DOWN*5.7)


def make_gear(x, y, r=0.32, color=AMB, teeth=8):
    """A real gear shape that ROTATES CONTINUOUSLY once given an updater —
    this is the fix for 'nothing moves during holds'."""
    hub = Circle(radius=r*0.55, color=color, fill_color="#15152A", fill_opacity=1,
                stroke_width=2.5)
    ring = Circle(radius=r, color=color, stroke_width=2.5)
    tooth_grp = VGroup()
    for i in range(teeth):
        ang = i * TAU / teeth
        tooth = Rectangle(width=r*0.28, height=r*0.32, fill_color=color,
                          fill_opacity=1, stroke_width=0)
        tooth.move_to(r*1.12*np.array([np.cos(ang), np.sin(ang), 0]))
        tooth.rotate(ang)
        tooth_grp.add(tooth)
    gear = VGroup(tooth_grp, ring, hub)
    gear.move_to([x, y, 0])
    return gear

def make_bar(x, y, width=0.55, height=0.1, color=ELEC):
    bg = Rectangle(width=width, height=height, fill_color="#0A0A18",
                  fill_opacity=1, stroke_color=GRY, stroke_width=1).move_to([x,y,0])
    fill = Rectangle(width=0.001, height=height-0.02, fill_color=color,
                     fill_opacity=1, stroke_width=0)
    fill.align_to(bg, LEFT).set_y(y)
    return bg, fill

def spin(mob, speed=2.2):
    mob.add_updater(lambda m, dt: m.rotate(dt * speed))
    return mob


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Widgets(S):
    ONSETS = [
        0.20,   #  0  "5 machines make 5 widgets in 5 minutes."
        2.80,   #  1  "How long do 100 machines take to make 100 widgets."
        5.60,   #  2  "Pause, trust your gut."
        7.09,   #  3  "If you said 100 minutes, you're wrong,"
        9.48,   #  4  "70% of people say exactly that."
        12.02,  #  5  "Each machine makes its own widget in 5 minutes, all at once,"
        15.43,  #  6  "so 100 machines still take just 5 minutes."
        18.20,  #  7  "This exact question was tested on an AI."
        20.50,  #  8  "It gave the same wrong answer humans do."
        24.10,  #  9  "That was GPT-3, an older model,"
        25.45,  # 10  "newer ones mostly know this specific answer now."
        27.50,  # 11  "But memorizing one question isn't the same as fixing the habit."
    ]

    def construct(self):
        self.setup()

        grid = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-7, 7, 1], x_length=8, y_length=14.2,
            background_line_style={"stroke_color": "#34344E", "stroke_width": 0.7,
                                   "stroke_opacity": 0.4},
            axis_config={"stroke_opacity": 0},
        )
        grid.set_z_index(-10)
        self.add(grid)

        # ══ BEAT 0 (0.20–2.80s): 5 gears, spinning, bars filling in sync ═══
        gxs = [-2.8, -1.4, 0, 1.4, 2.8]
        gears = VGroup(*[make_gear(x, 2.8) for x in gxs])
        for g in gears:
            spin(g)
        bars_bg = VGroup(); bars_fill = VGroup()
        for x in gxs:
            bg, fl = make_bar(x, 1.9)
            bars_bg.add(bg); bars_fill.add(fl)

        self.cue(0)
        self.P(LaggedStart(*[GrowFromCenter(g) for g in gears], lag_ratio=0.08), rt=0.6)
        self.P(FadeIn(bars_bg), rt=0.3)
        # bars fill SIMULTANEOUSLY — this IS "5 machines, 5 minutes, at once"
        self.play(*[fl.animate.stretch_to_fit_width(0.55).align_to(bg, LEFT)
                   for fl, bg in zip(bars_fill, bars_bg)], run_time=1.1)
        self._t += 1.1
        widgets_out = VGroup(*[
            Square(0.16, fill_color=WHT, fill_opacity=1, stroke_width=0).move_to([x, 1.5, 0])
            for x in gxs
        ])
        self.P(LaggedStart(*[FadeIn(w, scale=1.6) for w in widgets_out], lag_ratio=0.05), rt=0.35)
        setup_lbl = top_cap("5 machines. 5 widgets. 5 min.", sz=32, c=WHT)
        self.P(FadeIn(setup_lbl), rt=0.3)

        # ══ BEAT 1 (2.80–5.60s): multiply into an 8x10 grid of 100 ═════════
        self.cue(1)
        self.P(FadeOut(VGroup(setup_lbl, bars_bg, bars_fill, widgets_out)), rt=0.3)
        for g in gears:
            g.clear_updaters()  # stop rotation before the shape-transform below
        small_gears = VGroup()
        for row in range(8):
            for col in range(10):
                sg = make_gear(-3.15 + col*0.7, 4.3 - row*0.55, r=0.13, color=AMB, teeth=6)
                small_gears.add(sg)
        self.P(ReplacementTransform(gears, small_gears), rt=0.75)
        for sg in small_gears:
            spin(sg, speed=np.random.uniform(1.8, 2.8))  # resume motion after transform
        hundred_lbl = T("100 machines.", sz=40, c=AMB, weight=BOLD).move_to(DOWN*2.0)
        self.P(FadeIn(hundred_lbl, shift=UP*0.15), rt=0.4)

        # ══ BEAT 2 (5.60–7.09s): pause ═══════════════════════════════════
        self.cue(2)
        self.P(FadeOut(hundred_lbl), rt=0.25)
        pause_lbl = T("pause. trust your gut.", sz=36, c=GLD).move_to(DOWN*2.0)
        self.P(FadeIn(pause_lbl), rt=0.4)

        # ══ BEAT 3 (7.09–9.48s): WRONG model — sequential wave + racing timer ═
        self.cue(3)
        self.P(FadeOut(pause_lbl), rt=0.25)
        seq_lbl = T("if machines take turns...", sz=30, c=RED).move_to(DOWN*2.0)
        self.P(FadeIn(seq_lbl), rt=0.35)
        timer = T("1 min", sz=44, c=RED, weight=BOLD).move_to(DOWN*3.0)
        self.P(FadeIn(timer), rt=0.3)
        # one efficient wave animation — a color sweep across all 80 gears,
        # replacing what would otherwise be 80 separate render calls
        self.play(
            LaggedStart(*[sg.animate.set_color(RED) for sg in small_gears], lag_ratio=0.009),
            run_time=1.0
        )
        self._t += 1.0
        timer_end = T("100 min", sz=44, c=RED, weight=BOLD).move_to(timer)
        self.P(Transform(timer, timer_end), rt=0.3)

        # ══ BEAT 4 (9.48–12.02s): 70% of people — proportional crowd ═══════
        self.cue(4)
        self.P(FadeOut(VGroup(seq_lbl, timer)), rt=0.3)
        crowd = VGroup(*[Dot(radius=0.09) for _ in range(20)])
        crowd.arrange_in_grid(rows=4, cols=5, buff=0.35).move_to(DOWN*2.2)
        for i, d in enumerate(crowd):
            d.set_color(RED if i < 14 else GRN)  # 14/20 = 70%
        self.P(LaggedStart(*[GrowFromCenter(d) for d in crowd], lag_ratio=0.03), rt=0.6)
        pct_lbl = T("70% say 100 min.", sz=30, c=RED, weight=BOLD).next_to(crowd, DOWN, buff=0.35)
        self.P(FadeIn(pct_lbl), rt=0.35)

        # ══ BEAT 5 (12.02–15.43s): the CORRECT model — all light up together ═
        self.cue(5)
        self.P(FadeOut(VGroup(crowd, pct_lbl)), rt=0.4)
        correct_lbl = top_cap("all working AT ONCE:", sz=34, c=GRN)
        self.P(FadeIn(correct_lbl), rt=0.35)
        # every gear flashes green SIMULTANEOUSLY — the actual payoff visual
        self.play(*[sg.animate.set_color(GRN) for sg in small_gears], run_time=0.5)
        self._t += 0.5

        # ══ BEAT 6 (15.43–18.20s): still just 5 minutes ═════════════════════
        self.cue(6)
        five_lbl = T("still 5 minutes.", sz=52, c=GRN, weight=BOLD).move_to(DOWN*2.2)
        self.P(Write(five_lbl), rt=0.55)

        # ══ BEAT 7 (18.20–20.50s): tested on an AI ═════════════════════════
        self.cue(7)
        self.P(FadeOut(VGroup(correct_lbl, five_lbl, small_gears)), rt=0.45)
        tested_lbl = T("This exact question", sz=40, c=WHT).move_to(UP*1.6)
        tested_lbl2 = T("was tested on an AI.", sz=40, c=WHT).next_to(tested_lbl, DOWN, buff=0.3)
        self.P(FadeIn(tested_lbl, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(tested_lbl2, shift=DOWN*0.15), rt=0.4)

        # ══ BEAT 8 (20.50–24.10s): AI gives the wrong answer ═══════════════
        self.cue(8)
        self.P(FadeOut(VGroup(tested_lbl, tested_lbl2)), rt=0.35)
        chip_lbl = T("AI", sz=44, c=CGPT, weight=BOLD)
        chip_box = SurroundingRectangle(chip_lbl, buff=0.3, corner_radius=0.18,
                                        color=CGPT, stroke_width=3,
                                        fill_color="#0D1A16", fill_opacity=1)
        chip = VGroup(chip_box, chip_lbl).move_to(UP*1.6)
        self.P(FadeIn(chip, scale=1.2), rt=0.4)
        ai_wrong = T("\"100 minutes.\"", sz=40, c=RED, weight=BOLD).next_to(chip, DOWN, buff=0.5)
        self.P(FadeIn(ai_wrong, shift=DOWN*0.15), rt=0.4)
        wrong_x2 = Cross(ai_wrong, color=RED, stroke_width=5)
        self.P(Create(wrong_x2), rt=0.35)

        # ══ BEAT 9 (24.10–25.45s): that was GPT-3 ══════════════════════════
        self.cue(9)
        gpt3_lbl = T("GPT-3.", sz=44, c=GRY, weight=BOLD).next_to(ai_wrong, DOWN, buff=0.6)
        self.P(FadeIn(gpt3_lbl, shift=DOWN*0.1), rt=0.4)

        # ══ BEAT 10 (25.45–27.50s): older model ════════════════════════════
        self.cue(10)
        older_lbl = T("an older model.", sz=32, c=GRY).next_to(gpt3_lbl, DOWN, buff=0.3)
        self.P(FadeIn(older_lbl), rt=0.4)

        # ══ BEAT 11 (27.50s–end): memorizing vs fixing the habit ══════════
        self.cue(11)
        self.P(FadeOut(VGroup(chip, ai_wrong, wrong_x2, gpt3_lbl, older_lbl)), rt=0.4)
        habit1 = T("Memorizing one answer", sz=36, c=WHT).move_to(UP*0.6)
        habit2 = T("isn't the same as", sz=36, c=WHT).next_to(habit1, DOWN, buff=0.25)
        habit3 = T("fixing the habit.", sz=42, c=GLD, weight=BOLD).next_to(habit2, DOWN, buff=0.3)
        self.P(FadeIn(habit1, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(habit2, shift=DOWN*0.15), rt=0.35)
        self.P(FadeIn(habit3, shift=DOWN*0.15), rt=0.45)

        self.tail(1.5)
