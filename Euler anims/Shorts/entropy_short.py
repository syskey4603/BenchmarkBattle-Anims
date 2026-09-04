# entropy_short.py — cross entropy loss, real -log(p) curve, 32.77 s
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

def top_cap(s, sz=34, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(UP*6.3)

def bottom_cap(s, sz=32, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(DOWN*5.7)

def pulse(mob, rate=2.0, amount=0.04):
    def _upd(m, dt):
        m._pc = getattr(m, "_pc", 0.0) + dt
        s = 1.0 + amount * np.sin(m._pc * rate)
        m.scale(s / getattr(m, "_ls", 1.0))
        m._ls = s
    mob.add_updater(_upd)
    return mob


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Entropy(S):
    ONSETS = [
        0.04,   #  0  "When AI predicts the next word,"
        2.29,   #  1  "it doesn't just get graded right or wrong,"
        4.11,   #  2  "it gets graded on how confident it was."
        6.73,   #  3  "Give the correct word 90 percent confidence,"
        9.06,   #  4  "that's a small penalty."
        10.35,  #  5  "Give it only 1 percent,"
        11.64,  #  6  "even though you still got it right,"
        12.63,  #  7  "that penalty doesn't get a little bigger,"
        15.15,  #  8  "it explodes,"
        16.42,  #  9  "because the score runs your confidence through a logarithm."
        19.44,  # 10  "That's called cross entropy loss,"
        21.10,  # 11  "built to punish confident wrongness far harder than honest uncertainty,"
        25.92,  # 12  "the actual number every AI model is trying to shrink during training."
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

        # ══ BEAT 0-2 (0.04–6.73s): hook — graded on confidence, not r/w ═══
        word_lbl = T('AI predicts: "cat"', sz=38, c=WHT).move_to(UP*4.3)
        self.cue(0)
        self.P(FadeIn(word_lbl, shift=DOWN*0.15), rt=0.5)

        self.cue(1)
        not_rw = T("not just right or wrong.", sz=32, c=RED).next_to(word_lbl, DOWN, buff=0.5)
        self.P(FadeIn(not_rw), rt=0.4)

        self.cue(2)
        conf_lbl = T("graded on confidence.", sz=36, c=GLD, weight=BOLD)
        conf_lbl.next_to(not_rw, DOWN, buff=0.4)
        self.P(FadeIn(conf_lbl, shift=DOWN*0.1), rt=0.5)

        # ══ BEAT 3-4 (6.73–10.35s): scenario A — 90% confidence, small bar ═
        self.cue(3)
        self.P(FadeOut(VGroup(word_lbl, not_rw, conf_lbl)), rt=0.4)
        conf90 = T("90% confidence", sz=34, c=GRN).move_to(UP*3.5)
        self.P(FadeIn(conf90, shift=DOWN*0.15), rt=0.4)

        bar90_bg = Rectangle(width=2.5, height=0.5, fill_color="#0A0A18",
                             fill_opacity=1, stroke_color=GRY, stroke_width=1.5)
        bar90_bg.move_to(UP*2.5)
        bar90_fill = Rectangle(width=0.02, height=0.42, fill_color=GRN,
                               fill_opacity=0.9, stroke_width=0)
        bar90_fill.align_to(bar90_bg, LEFT).align_to(bar90_bg, DOWN).shift(RIGHT*0.04+UP*0.04)
        self.P(FadeIn(bar90_bg), rt=0.3)
        self.P(FadeIn(bar90_fill), rt=0.2)

        self.cue(4)
        small_lbl = T("small penalty.", sz=30, c=GRN).next_to(bar90_bg, DOWN, buff=0.35)
        self.P(bar90_fill.animate.stretch_to_fit_width(0.35).align_to(
            bar90_bg, LEFT).shift(RIGHT*0.04), rt=0.4)
        self.P(FadeIn(small_lbl), rt=0.35)

        # ══ BEAT 5-8 (10.35–16.42s): scenario B — 1% confidence, EXPLODES ═
        self.cue(5)
        self.P(FadeOut(VGroup(conf90, bar90_bg, bar90_fill, small_lbl)), rt=0.4)
        conf1 = top_cap("1% confidence", sz=34, c=AMB)
        self.P(FadeIn(conf1, shift=DOWN*0.15), rt=0.4)

        BASE_Y = -3.0
        bar1_bg = Rectangle(width=2.0, height=0.5, fill_color="#0A0A18",
                            fill_opacity=1, stroke_color=GRY, stroke_width=1.5)
        bar1_bg.move_to([-1.5, BASE_Y, 0])
        self.P(FadeIn(bar1_bg), rt=0.3)

        self.cue(6)
        stillright_lbl = T("still got it right.", sz=26, c=GRY).next_to(bar1_bg, RIGHT, buff=0.4)
        self.P(FadeIn(stillright_lbl), rt=0.4)

        self.cue(7)
        notbit_lbl = T("not a little bigger...", sz=28, c=RED).next_to(stillright_lbl, DOWN, buff=0.3)
        self.P(FadeIn(notbit_lbl), rt=0.4)

        self.cue(8)
        # the bar EXPLODES upward — 8+ units of genuinely clear space above it
        explode_bar = Rectangle(width=0.5, height=5.5, fill_color=RED,
                                fill_opacity=0.9, stroke_width=0)
        explode_bar.move_to([-1.5, BASE_Y, 0]).align_to(bar1_bg, DOWN)
        self.P(FadeOut(VGroup(stillright_lbl, notbit_lbl)), rt=0.25)
        self.P(GrowFromEdge(explode_bar, DOWN), rt=0.5)
        explode_lbl = T("EXPLODES.", sz=44, c=RED, weight=BOLD)
        explode_lbl.next_to(explode_bar, UP, buff=0.3)
        self.P(FadeIn(explode_lbl, scale=1.2), rt=0.4)

        # ══ BEAT 9 (16.42–19.44s): why — the real -log(p) curve ═══════════
        self.cue(9)
        self.P(FadeOut(VGroup(conf1, bar1_bg, explode_bar, explode_lbl)), rt=0.5)
        ax = Axes(
            x_range=[0, 1, 0.25], y_range=[0, 4, 1],
            x_length=6.0, y_length=5.0,
            axis_config={"include_tip": False, "color": GRY, "stroke_width": 1.5},
        ).move_to(DOWN*0.3)
        x_lbl = T("confidence", sz=24, c=GRY).next_to(ax.x_axis, DOWN, buff=0.2)
        y_lbl = T("penalty", sz=24, c=GRY).next_to(ax.y_axis, LEFT, buff=0.2).rotate(PI/2)
        self.P(Create(ax), rt=0.5)
        self.P(FadeIn(x_lbl), FadeIn(y_lbl), rt=0.3)

        curve = ax.plot(lambda p: -np.log(max(p, 0.02)), x_range=[0.021, 0.98],
                        color=RED, stroke_width=4)
        self.P(Create(curve), rt=0.8)

        # ══ BEAT 10 (19.44–21.10s): name it ════════════════════════════════
        self.cue(10)
        self.P(FadeOut(VGroup(ax, x_lbl, y_lbl, curve)), rt=0.45)
        name_lbl = T("cross entropy loss.", sz=48, c=GLD, weight=BOLD)
        pulse(name_lbl, rate=1.6, amount=0.03)
        self.P(Write(name_lbl), rt=0.65)

        # ══ BEAT 11 (21.10–25.92s): built to punish confident wrongness ═══
        self.cue(11)
        self.P(FadeOut(name_lbl), rt=0.4)
        punish1 = T("Punishes confident wrongness", sz=32, c=WHT).move_to(UP*1.0)
        punish2 = T("far harder than", sz=32, c=WHT).next_to(punish1, DOWN, buff=0.3)
        punish3 = T("honest uncertainty.", sz=36, c=GRN, weight=BOLD).next_to(punish2, DOWN, buff=0.3)
        self.P(FadeIn(punish1, shift=DOWN*0.15), rt=0.4)
        self.P(FadeIn(punish2, shift=DOWN*0.1), rt=0.4)
        self.P(FadeIn(punish3, shift=DOWN*0.1), rt=0.45)

        # ══ BEAT 12 (25.92s–end): the number every model shrinks ══════════
        self.cue(12)
        self.P(FadeOut(VGroup(punish1, punish2, punish3)), rt=0.4)
        final1 = T("The number every AI model", sz=34, c=WHT).move_to(UP*0.8)
        final2 = T("is trying to shrink.", sz=42, c=GLD, weight=BOLD).next_to(final1, DOWN, buff=0.35)
        self.P(FadeIn(final1, shift=DOWN*0.15), rt=0.45)
        self.P(Write(final2), rt=0.55)

        self.tail(5.6)
