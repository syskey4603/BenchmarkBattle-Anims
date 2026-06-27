# sycophancy.py — Sycophancy short, portrait 1080×1920, 26.1 s
# render: python -m manim sycophancy.py Sycophancy --resolution 1080,1920 --fps 30 -q h
# mux:    ffmpeg -i Sycophancy.mp4 -i voiceover.mp3 -c:v copy -c:a aac -shortest out.mp4

from manim import *

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 30
config.background_color = "#1C1C2E"
config.frame_height     = 8.0 * 1920 / 1080

WHT  = "#FFFDE9"; GRY = "#888899"; RED = "#FC6255"; AMB = "#FF9408"
CLAU = "#E8925C"; CGPT = "#10A37F"; GGEM = "#4285F4"; GROK = "#FF4500"


def T(s, sz=48, c=WHT, **kw):
    return Text(s, font_size=sz, color=c, **kw)

def chip(name, col):
    bg  = RoundedRectangle(corner_radius=0.2, width=3.5, height=1.2,
                           fill_color="#111111", fill_opacity=1,
                           stroke_color=col, stroke_width=2)
    bar = Rectangle(width=0.22, height=1.2, fill_color=col,
                    fill_opacity=1, stroke_width=0).align_to(bg, LEFT)
    nm  = T(name, 30, col, weight=BOLD).move_to(bg.get_center() + RIGHT*0.15 + UP*0.12)
    bd  = T("backs down", 20, RED).next_to(nm, DOWN, buff=0.06)
    return VGroup(bg, bar, nm, bd)


class S(Scene):
    ONSETS = []
    def setup(self):          self._t = 0.0
    def P(self, *a, rt=0.6, **kw): self.play(*a, run_time=rt, **kw); self._t += rt
    def W(self, t):
        if t > 0: self.wait(t); self._t += t
    def cue(self, i):         self.W(max(self.ONSETS[i] - self._t, 0))
    def tail(self, t=1.5):    self.W(t)


class Sycophancy(S):
    ONSETS = [
        0.00,   # 0  "Here's something AI companies don't talk about."
        5.48,   # 1  "Ask ChatGPT a hard maths problem."
        7.73,   # 2  "Get an answer."
        8.15,   # 3  "Now tell it it's wrong — even when it isn't."
        10.96,  # 4  "Watch what happens."
        12.94,  # 5  "It backs down."
        13.98,  # 6  "Every major AI does this."
        15.08,  # 7  "Researchers call it sycophancy…"
        19.62,  # 8  "Your AI isn't giving you the right answer."
        22.16,  # 9  "It's giving you the answer it thinks you want to hear."
        23.54,  # 10 "You're not using a calculator."
        25.00,  # 11 "A very expensive yes-man."
    ]

    def bubble(self, speaker, msg, sc=CGPT, bg="#0F1F1A", w=7.2):
        box = RoundedRectangle(corner_radius=0.22, width=w, height=1.1,
                               fill_color=bg, fill_opacity=1,
                               stroke_color=sc, stroke_width=1.5)
        lbl = T(speaker, sz=20, c=sc).move_to(box.get_corner(UL) + RIGHT*0.35 + DOWN*0.22)
        txt = T(msg, sz=28)
        txt.move_to(box.get_center() + DOWN*0.1)
        if txt.width > w - 0.7:
            txt.scale_to_fit_width(w - 0.7)
        return VGroup(box, lbl, txt)

    def construct(self):
        self.setup()

        # 0 — hook
        h1 = T("Here's something",  sz=54).move_to(UP * 2.6)
        h2 = T("AI companies",      sz=70, c=RED, weight=BOLD).next_to(h1, DOWN, buff=0.3)
        h3 = T("don't talk about.", sz=54).next_to(h2, DOWN, buff=0.3)

        self.cue(0)
        self.P(FadeIn(h1, shift=DOWN * 0.2), rt=0.6)
        self.P(Write(h2), rt=0.7)
        self.P(FadeIn(h3, shift=UP * 0.2), rt=0.5)

        # 1 — question bubble
        self.cue(1)
        self.P(FadeOut(VGroup(h1, h2, h3)), rt=0.4)

        bq = self.bubble("You", "What is the square root of 144?",
                         sc="#7777AA", bg="#0F0F1F").move_to(UP * 3.8)
        self.P(FadeIn(bq, shift=LEFT * 0.2), rt=0.4)

        # 2 — AI answers correctly
        self.cue(2)
        bai = self.bubble("AI", "The answer is 12.")
        bai.next_to(bq, DOWN, buff=0.3)
        self.P(FadeIn(bai, shift=RIGHT * 0.2), rt=0.4)

        # 3 — user pushes back
        self.cue(3)
        bpu = self.bubble("You", "No, that's wrong.",
                          sc="#7777AA", bg="#0F0F1F")
        bpu.next_to(bai, DOWN, buff=0.3)
        cav = T("(even though it isn't)", sz=28, c=AMB).next_to(bpu, DOWN, buff=0.22)
        self.P(FadeIn(bpu, shift=LEFT * 0.2), rt=0.5)
        self.P(FadeIn(cav), rt=0.4)

        # 4 — AI caves, original answer turns red
        self.cue(4)
        bca = self.bubble("AI", "I apologize, you may be right.",
                          sc=RED, bg="#1F0F0F")
        bca.next_to(bpu, DOWN, buff=0.3)
        self.P(bai[0].animate.set_stroke(color=RED),
               bai[2].animate.set_color(RED),
               FadeIn(bca, shift=RIGHT * 0.2), rt=0.5)

        # 5 — BACKS DOWN
        self.cue(5)
        bd1 = T("BACKS", sz=140, c=RED, weight=BOLD).move_to(DOWN * 3.2)
        bd2 = T("DOWN.", sz=140, c=RED, weight=BOLD).next_to(bd1, DOWN, buff=0.1)
        self.P(Write(bd1), Write(bd2), lag_ratio=0.5, rt=0.52)

        # 6 — four model chips
        self.cue(6)
        self.P(FadeOut(VGroup(bq, bai, bpu, cav, bca, bd1, bd2)), rt=0.4)

        every  = T("Every major AI does this.", sz=44).move_to(UP * 5.5)
        chips  = VGroup(
            chip("CLAUDE",  CLAU).move_to(UP * 2.8 + LEFT  * 1.82),
            chip("CHATGPT", CGPT).move_to(UP * 2.8 + RIGHT * 1.82),
            chip("GEMINI",  GGEM).move_to(UP * 1.2 + LEFT  * 1.82),
            chip("GROK",    GROK).move_to(UP * 1.2 + RIGHT * 1.82),
        )
        self.P(FadeIn(every, shift=DOWN * 0.2), rt=0.4)
        self.P(*[FadeIn(c) for c in chips], lag_ratio=0.2, rt=0.35)

        # 7 — SYCOPHANCY
        self.cue(7)
        self.P(FadeOut(VGroup(every, chips)), rt=0.4)

        res = T("Researchers call it", sz=44, c=GRY).move_to(UP * 3.2)
        syl = T("SYCOPHANCY.", sz=100, c=AMB, weight=BOLD).move_to(UP * 1.4)
        ul  = Line(syl.get_left(), syl.get_right(),
                   color=AMB, stroke_width=3).next_to(syl, DOWN, buff=0.1)
        d1  = T("Models changing correct answers", sz=34).move_to(DOWN * 0.5)
        d2  = T("under social pressure.",          sz=34).next_to(d1, DOWN, buff=0.2)

        self.P(FadeIn(res, shift=DOWN * 0.2), rt=0.5)
        self.P(Write(syl), Create(ul), rt=0.8)
        self.P(FadeIn(d1, shift=UP * 0.2), FadeIn(d2, shift=UP * 0.2),
               lag_ratio=0.3, rt=0.4)

        # 8 — not the right answer
        self.cue(8)
        self.P(FadeOut(VGroup(res, syl, ul, d1, d2)), rt=0.4)

        r1 = T("Your AI isn't giving you", sz=50).move_to(UP * 1.5)
        r2 = T("the RIGHT answer.", sz=58, c=RED, weight=BOLD).next_to(r1, DOWN, buff=0.3)
        self.P(FadeIn(r1, shift=UP * 0.2), rt=0.4)
        self.P(Write(r2), rt=0.5)

        # 9 — the answer it wants you to hear
        self.cue(9)
        p1 = T("It gives you",         sz=46, c=GRY).move_to(DOWN * 1.4)
        p2 = T("the answer you WANT.", sz=46).next_to(p1, DOWN, buff=0.22)
        self.P(FadeIn(p1), FadeIn(p2), lag_ratio=0.3, rt=0.45)

        # 10-11 — YES-MAN
        self.cue(10)
        self.P(FadeOut(VGroup(r1, r2, p1, p2)), rt=0.3)

        yes = T("YES-MAN.", sz=150, c=RED, weight=BOLD).move_to(ORIGIN)
        if yes.width > 7.6:
            yes.scale_to_fit_width(7.6)
        sub = T("A very expensive one.", sz=40, c=GRY).next_to(yes, DOWN, buff=0.35)

        self.cue(11)
        self.P(Write(yes), rt=0.7)
        self.P(FadeIn(sub), rt=0.4)
        self.tail(1.2)
