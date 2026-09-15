# jl_short.py — Johnson-Lindenstrauss Lemma, continuous compression, 33.13 s
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

def top_cap(s, sz=32, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(UP*6.4)

def bottom_cap(s, sz=30, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw).move_to(DOWN*5.9)

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


class JLLemma(S):
    ONSETS = [
        0.06,   #  0  "There's a theorem that sounds like it shouldn't be possible."
        3.06,   #  1  "Take a massive set of points in an absurdly high number of dimensions,"
        6.14,   #  2  "randomly project them into a much smaller number of dimensions,"
        10.52,  #  3  "and the distances between them barely change."
        12.12,  #  4  "It's called the Johnson-Lindenstrauss lemma,"
        18.27,  #  5  "proven, not approximate."
        20.48,  #  6  "The dimensions you need only depend on how many points you have,"
        24.29,  #  7  "not how many dimensions you started with."
        26.49,  #  8  "It's the real reason AI can compress enormous data down,"
        29.77,  #  9  "without losing which points are close,"
        32.08,  # 10  "and which are far."
    ]

    def construct(self):
        self.setup()

        grid = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-7, 7, 1], x_length=8, y_length=14.2,
            background_line_style={"stroke_color": "#34344E", "stroke_width": 0.7,
                                   "stroke_opacity": 0.35},
            axis_config={"stroke_opacity": 0},
        )
        grid.set_z_index(-10)
        self.add(grid)

        # ══ BEAT 0: hook ═══════════════════════════════════════════════════
        hook1 = T("Shouldn't be possible.", sz=40, c=RED, weight=BOLD).move_to(UP*4.5)
        self.cue(0)
        self.P(FadeIn(hook1, shift=DOWN*0.15), rt=0.6)

        # ══ BEAT 1: spread-out point cloud, "absurdly high dimensions" ═════
        self.cue(1)
        self.P(FadeOut(hook1), rt=0.4)

        dim_lbl = T("1,000 dimensions", sz=34, c=AMB, weight=BOLD).move_to(UP*5.0)
        self.P(FadeIn(dim_lbl, shift=DOWN*0.15), rt=0.4)

        rng = np.random.default_rng(3)
        n_pts = 7
        wide_positions = [[rng.uniform(-3.3, 3.3), rng.uniform(1.0, 3.8), 0] for _ in range(n_pts)]
        points = VGroup(*[Dot(p, radius=0.11, color=WHT) for p in wide_positions])
        self.P(LaggedStart(*[GrowFromCenter(p) for p in points], lag_ratio=0.1), rt=0.6)

        # two specific points highlighted with a measured distance line
        pA, pB = points[2], points[5]
        pA.set_color(GLD); pB.set_color(GLD)
        dist_line = always_redraw(lambda: Line(pA.get_center(), pB.get_center(),
                                               color=GLD, stroke_width=2.5))
        self.add(dist_line)

        def current_dist():
            return np.linalg.norm(pA.get_center() - pB.get_center())

        dist_lbl = always_redraw(lambda: T(f"distance: {current_dist():.2f}", sz=24, c=GLD)
                                 .next_to(VGroup(pA, pB), DOWN, buff=0.5).shift(DOWN*0.3))
        self.add(dist_lbl)

        # ══ BEAT 2: THE POINT CLOUD COMPRESSES — same points, new positions ═
        self.cue(2)
        self.P(FadeOut(dim_lbl), rt=0.3)
        compress_lbl = T("randomly project down...", sz=28, c=BLU).move_to(UP*5.0)
        self.P(FadeIn(compress_lbl), rt=0.35)

        # compress: OTHER points move to a genuinely different-looking
        # arrangement, but the highlighted pair's distance is explicitly
        # controlled to stay close to its original value — that's the
        # actual claim being illustrated, not just "everything shrinks"
        orig_dist = np.linalg.norm(np.array(wide_positions[2]) - np.array(wide_positions[5]))
        new_center = np.array([0.0, 1.8, 0.0])
        angle = rng.uniform(0, 2*np.pi)
        half_d = orig_dist * 0.94 / 2  # ~6% change — genuinely "barely changed"
        direction = np.array([np.cos(angle), np.sin(angle), 0.0])
        pA_target = new_center + half_d * direction
        pB_target = new_center - half_d * direction

        tight_positions = []
        other_idx = 0
        for i in range(n_pts):
            if i == 2:
                tight_positions.append(pA_target)
            elif i == 5:
                tight_positions.append(pB_target)
            else:
                jitter = rng.uniform(-1.4, 1.4, 3) * np.array([1, 1, 0])
                tight_positions.append(new_center + jitter)

        self.P(*[pt.animate.move_to(pos) for pt, pos in zip(points, tight_positions)],
              rt=1.3, rate_func=smooth)
        new_dim_lbl = T("50 dimensions", sz=34, c=BLU, weight=BOLD).move_to(UP*5.0)
        self.P(ReplacementTransform(compress_lbl, new_dim_lbl), rt=0.4)

        # ══ BEAT 3: the SAME distance, barely changed ═══════════════════════
        self.cue(3)
        barely_lbl = T("barely changed.", sz=30, c=GRN, weight=BOLD)
        barely_lbl.next_to(dist_lbl, DOWN, buff=0.4)
        self.P(FadeIn(barely_lbl, shift=DOWN*0.1), rt=0.5)

        # ══ BEAT 4-5: name it ══════════════════════════════════════════════
        self.cue(4)
        self.P(FadeOut(VGroup(new_dim_lbl, points, dist_line, dist_lbl, barely_lbl)), rt=0.5)
        name1 = T("Johnson-", sz=48, c=GLD, weight=BOLD).move_to(UP*2.0)
        name2 = T("Lindenstrauss", sz=48, c=GLD, weight=BOLD).next_to(name1, DOWN, buff=0.2)
        name3 = T("Lemma.", sz=48, c=GLD, weight=BOLD).next_to(name2, DOWN, buff=0.2)
        self.P(Write(name1), rt=0.4)
        self.P(Write(name2), rt=0.45)
        self.P(Write(name3), rt=0.4)

        self.cue(5)
        proven_lbl = T("Proven. Not approximate.", sz=30, c=WHT)
        proven_lbl.next_to(name3, DOWN, buff=0.5)
        self.P(FadeIn(proven_lbl, shift=DOWN*0.1), rt=0.45)

        # ══ BEAT 6-7: what determines the needed dimensions ═════════════════
        self.cue(6)
        self.P(FadeOut(VGroup(name1, name2, name3, proven_lbl)), rt=0.45)
        depends1 = T("Depends on how many", sz=32, c=WHT).move_to(UP*1.2)
        depends2 = T("points you have.", sz=36, c=GLD, weight=BOLD).next_to(depends1, DOWN, buff=0.3)
        self.P(FadeIn(depends1, shift=DOWN*0.15), rt=0.45)
        self.P(FadeIn(depends2, shift=DOWN*0.1), rt=0.45)

        self.cue(7)
        not_lbl = T("Not how many dimensions", sz=28, c=GRY).next_to(depends2, DOWN, buff=0.5)
        not_lbl2 = T("you started with.", sz=28, c=GRY).next_to(not_lbl, DOWN, buff=0.15)
        self.P(FadeIn(not_lbl), rt=0.35)
        self.P(FadeIn(not_lbl2), rt=0.35)

        # ══ BEAT 8-10: close ═══════════════════════════════════════════════
        self.cue(8)
        self.P(FadeOut(VGroup(depends1, depends2, not_lbl, not_lbl2)), rt=0.45)
        compress_data = T("AI compresses enormous data.", sz=32, c=WHT, weight=BOLD)
        compress_data.move_to(UP*0.8)
        self.P(FadeIn(compress_data, shift=DOWN*0.15), rt=0.5)

        self.cue(9)
        close_lbl = T("close stays close.", sz=32, c=GRN).next_to(compress_data, DOWN, buff=0.5)
        self.P(FadeIn(close_lbl, shift=DOWN*0.1), rt=0.45)

        self.cue(10)
        far_lbl = T("far stays far.", sz=32, c=RED).next_to(close_lbl, DOWN, buff=0.3)
        pulse(far_lbl, rate=1.6, amount=0.03)
        self.P(FadeIn(far_lbl, shift=DOWN*0.1), rt=0.45)

        self.tail(2.0)
