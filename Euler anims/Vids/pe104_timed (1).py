from manim import *
import numpy as np
import math
import re

config.background_color = "#0A0A15"

mono = "DejaVu Sans Mono"
grok = "#FF4500"
gpt = "#10A37F"
kimi = "#9D6FFF"
fable = "#E8925C"
gold = "#FFD700"
bad = "#FF5555"
good = "#4ADE80"
ink = "#F2F3F7"
dim = "#FFB86C"
panel = "#10141F"
gridcol = "#2A3450"
faint = "#3A3F55"

def fixtext(s):
    s = s.replace("\\$", "\x00m\x00")
    s = s.replace("\\", " ")
    s = s.replace("%", r"\%").replace("&", r"\&").replace("#", r"\#")
    s = s.replace("_", r"\_")
    s = re.sub(r'"([^"]*)"', r"``\1''", s)
    for a, b in [("→", r"$\rightarrow$"), ("✓", r"$\checkmark$"), ("✗", r"$\times$"),
                 ("×", r"$\times$"), ("≈", r"$\approx$"), ("—", "---"), ("·", r"$\cdot$"), ("φ", r"$\varphi$")]:
        s = s.replace(a, b)
    s = s.replace("\x00m\x00", r"\$")
    return s

def label(s, size=24, color=ink, font=None):
    if font:
        t = Text(s, font_size=size, font=font)
    elif s.lstrip().startswith("@"):
        t = MathTex(s.lstrip()[1:], font_size=size)
    else:
        t = Tex(fixtext(s), font_size=size)
    return t.set_color(color)

def pill(name, color, w=2.7, h=0.74, size=23):
    box = RoundedRectangle(corner_radius=0.12, width=w, height=h).set_fill(panel, 1).set_stroke(color, 2)
    return VGroup(box, label(name, size, color).move_to(box))

def fmtnum(n):
    return f"{n:,}"

def bulgearc(p1, p2, height, color, sw=2.5):
    mid = (p1 + p2) / 2
    down = np.array([0, -1, 0]) * height
    c1 = p1 + (mid - p1) * 0.5 + down
    c2 = p2 + (mid - p2) * 0.5 + down
    return CubicBezier(p1, c1, c2, p2, color=color, stroke_width=sw)

answer_idx = 329468
ndigits = 68855
head9 = "245681739"
tail9 = "352786941"

def digitrow(s, size=22, color=ink, gap=0.34):
    grp = VGroup(*[label(c, size, color) for c in s])
    grp.arrange(RIGHT, buff=gap)
    return grp

def bigstrip(width=9.0, y=0, color=ink):
    line = Line(LEFT * width / 2, RIGHT * width / 2, color=gridcol, stroke_width=6).move_to(UP * y)
    ticks = VGroup()
    for i in range(1, 24):
        x = -width / 2 + width * i / 24
        t = Line(UP * 0.06, DOWN * 0.06, color=faint, stroke_width=1.5).move_to(UP * y + RIGHT * x)
        ticks.add(t)
    return VGroup(line, ticks)


class base(Scene):
    times = []
    def start(self):
        self.now = 0.0
    def play_(self, *a, rt=0.8, **k):
        self.play(*a, run_time=rt, **k)
        self.now += rt
    def hold(self, t):
        if t > 0:
            self.wait(t)
            self.now += t
    def cue(self, i):
        if i < len(self.times):
            gap = self.times[i] - self.now
            if gap > 0.03:
                self.wait(gap)
                self.now += gap
    def finish(self, total):
        gap = total - self.now
        if gap > 0:
            self.wait(gap)


class sec1title(base):
    times = [0.0, 1.62, 5.07, 7.17, 8.35, 14.02, 20.4, 22.86, 27.07, 31.84, 37.06]
    def construct(self):
        self.start()
        self.cue(0)
        seq = [1, 1]
        nums = VGroup(*[label(str(v), 28, ink) for v in seq])
        nums.arrange(RIGHT, buff=0.5).move_to(UP * 0.5)
        self.play_(FadeIn(nums[0]), rt=0.4)
        self.play_(FadeIn(nums[1]), rt=0.4)

        self.cue(1)
        rule = label("1 + 1 = 2", 20, dim)
        rule.next_to(nums, DOWN, buff=0.6)
        two = label("2", 28, ink).move_to(RIGHT * 1.0 + UP * 0.5)
        self.play_(FadeIn(rule), rt=0.6)
        self.play_(FadeIn(two), rt=0.4)
        nums.add(two)

        self.cue(2)
        self.play_(FadeOut(rule), rt=0.3)
        for v in [3, 5, 8, 13]:
            nv = label(str(v), 28, ink)
            nv.next_to(nums, RIGHT, buff=0.5)
            self.play_(FadeIn(nv), rt=0.3)
            nums.add(nv)
        seen = label("you've probably seen this before", 18, dim)
        seen.to_edge(DOWN, buff=0.85)
        self.play_(FadeIn(seen), rt=0.8)

        self.cue(3)
        self.play_(FadeOut(VGroup(nums, seen)), rt=0.4)
        far = label("but keep going far enough...", 22, ink)
        far.move_to(UP * 0.3)
        self.play_(Write(far), rt=1.3)

        self.cue(4)
        self.play_(FadeOut(far), rt=0.3)
        strip = bigstrip(width=8.5, y=0.0)
        biglab = label("tens of thousands of digits long", 19, gold)
        biglab.to_edge(DOWN, buff=0.85)
        self.play_(Create(strip[0]), rt=1.0)
        self.play_(LaggedStart(*[Create(t) for t in strip[1]], lag_ratio=0.04), rt=1.0)
        self.play_(FadeIn(biglab), rt=0.9)

        self.cue(5)
        self.play_(FadeOut(biglab), rt=0.3)
        tailrow = digitrow(tail9, 20, gold)
        tailrow.next_to(strip, DOWN, buff=0.5).align_to(strip, RIGHT).shift(LEFT * 0.3)
        taillab = label("last nine digits --- one through nine, each exactly once", 17, gold)
        taillab.next_to(tailrow, DOWN, buff=0.35)
        self.play_(FadeIn(tailrow, shift=UP * 0.15), rt=0.9)
        self.play_(FadeIn(taillab), rt=0.9)

        self.cue(6)
        self.play_(FadeOut(VGroup(tailrow, taillab)), rt=0.4)
        headrow = digitrow(head9, 20, dim)
        headrow.next_to(strip, DOWN, buff=0.5).align_to(strip, LEFT).shift(RIGHT * 0.3)
        headlab = label("the first nine digits do the same thing too", 17, dim)
        headlab.next_to(headrow, DOWN, buff=0.35)
        self.play_(FadeIn(headrow, shift=UP * 0.15), rt=0.9)
        self.play_(FadeIn(headlab), rt=0.9)

        self.cue(7)
        self.play_(FadeOut(headlab), rt=0.3)
        both = label("both ends --- same huge number", 20, ink)
        both.next_to(headrow, DOWN, buff=0.35)
        self.play_(Write(both), rt=1.4)

        self.cue(8)
        self.play_(FadeOut(VGroup(strip, headrow, both)), rt=0.4)
        names = ["Kimi K3", "Fable", "GPT-5.6 Sol", "Grok 4.5"]
        cols = [kimi, fable, gpt, grok]
        chips = VGroup(*[pill(n, c, w=2.55, h=0.72, size=18) for n, c in zip(names, cols)])
        chips.arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        self.play_(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips], lag_ratio=0.15), rt=1.3)

        self.cue(9)
        nohint = label("no hints", 18, dim)
        nohint.next_to(chips, DOWN, buff=0.5)
        self.play_(FadeIn(nohint), rt=0.7)
        self.hold(1.3)
        self.play_(FadeOut(nohint), rt=0.3)
        twist = label("this one needs real math to even be possible", 18, gold)
        twist.next_to(chips, DOWN, buff=0.5)
        self.play_(Write(twist), rt=1.8)
        self.finish(37.056979 + 1.3)


class sec2problem(base):
    times = [0.0, 2.46, 7.38, 15.49, 18.1, 20.5, 22.66, 32.54, 37.0, 39.39, 43.73, 45.87, 50.72, 53.38, 58.25, 60.86, 63.95, 68.86]
    def construct(self):
        self.start()
        ttl = label("Pandigital Fibonacci Ends", 28)
        ttl.to_edge(UP, buff=0.55)
        self.play_(Write(ttl), rt=1.0)

        self.cue(0)
        big = label(f"~{ndigits:,} digits long", 26, bad)
        big.move_to(UP * 1.0)
        strip = bigstrip(width=8.0, y=-0.4)
        self.play_(Write(big), rt=1.2)
        self.play_(Create(strip[0]), LaggedStart(*[Create(t) for t in strip[1]], lag_ratio=0.03), rt=1.0)

        self.cue(1)
        costlab = label("computing that in full, every single check", 18, ink)
        costlab.to_edge(DOWN, buff=0.85)
        self.play_(FadeIn(costlab), rt=1.0)

        self.cue(2)
        scalelab = label("hundreds of thousands of checks --- growing every step", 17, dim)
        scalelab.next_to(costlab, UP, buff=0.3)
        self.play_(FadeIn(scalelab), rt=1.1)

        self.cue(3)
        self.play_(FadeOut(VGroup(big, strip, costlab, scalelab)), rt=0.4)
        split = label("two separate problems buried in here", 22, gold)
        split.move_to(UP * 0.3)
        self.play_(Write(split), rt=1.5)

        self.cue(4)
        self.play_(FadeOut(split), rt=0.3)
        p1 = label("first --- checking the last nine digits", 20, ink)
        p1.move_to(UP * 1.1)
        self.play_(Write(p1), rt=1.3)

        self.cue(5)
        nowhole = label("you don't need the whole number for that", 18, dim)
        nowhole.next_to(p1, DOWN, buff=0.5)
        self.play_(FadeIn(nowhole), rt=1.0)

        self.cue(6)
        self.play_(FadeOut(nowhole), rt=0.3)
        a, b = 1, 1
        atxt = label(f"a = {a}", 22, ink)
        btxt = label(f"b = {b}", 22, ink)
        pair = VGroup(atxt, btxt).arrange(RIGHT, buff=0.8)
        pair.next_to(p1, DOWN, buff=0.5)
        modlab = label("keep dividing by a billion, keep the remainder", 16, dim)
        modlab.next_to(pair, DOWN, buff=0.35)
        self.play_(FadeIn(pair), rt=0.8)
        self.play_(FadeIn(modlab), rt=0.9)

        self.cue(7)
        for _ in range(4):
            a, b = b, (a + b) % 1000
            na = label(f"a = {a}", 22, ink)
            nb = label(f"b = {b}", 22, ink)
            npair = VGroup(na, nb).arrange(RIGHT, buff=0.8).move_to(pair)
            self.play_(Transform(pair, npair), rt=0.35)
        foreverlab = label("last nine digits behave the same, forever", 18, good)
        foreverlab.next_to(modlab, DOWN, buff=0.4)
        self.play_(FadeIn(foreverlab), rt=1.0)

        self.cue(8)
        smalllab = label("the number driving that stays small the entire time", 17, good)
        smalllab.next_to(foreverlab, DOWN, buff=0.35)
        self.play_(FadeIn(smalllab), rt=1.1)

        self.cue(9)
        self.play_(FadeOut(VGroup(p1, pair, modlab, foreverlab, smalllab)), rt=0.4)
        p2 = label("the first nine digits --- a different problem", 20, ink)
        p2.move_to(UP * 1.1)
        self.play_(Write(p2), rt=1.5)

        self.cue(10)
        needbig = label("can't get those from a remainder --- you need to know how big it is", 17, dim)
        needbig.next_to(p2, DOWN, buff=0.5)
        self.play_(FadeIn(needbig), rt=1.4)

        self.cue(11)
        self.play_(FadeOut(needbig), rt=0.3)
        trick = label("there's a trick for that too", 19, gold)
        trick.next_to(p2, DOWN, buff=0.5)
        self.play_(Write(trick), rt=1.1)

        self.cue(12)
        phi = label("@\\varphi = \\dfrac{1+\\sqrt{5}}{2}", 28, gold)
        phi.next_to(trick, DOWN, buff=0.5)
        goldlab = label("Fibonacci numbers grow at a rate tied to the golden ratio", 16, ink)
        goldlab.next_to(phi, DOWN, buff=0.35)
        self.play_(Write(phi), rt=1.4)
        self.play_(FadeIn(goldlab), rt=1.0)

        self.cue(13)
        self.play_(FadeOut(goldlab), rt=0.3)
        logform = label("@F_n \\approx 10^{\\,n\\log_{10}\\varphi \\,-\\, \\log_{10}\\sqrt{5}}", 26, gold)
        logform.next_to(phi, DOWN, buff=0.5)
        self.play_(Write(logform), rt=1.6)

        self.cue(14)
        nofull = label("without ever writing out the full number", 18, good)
        nofull.next_to(logform, DOWN, buff=0.4)
        self.play_(FadeIn(nofull), rt=1.0)

        self.cue(15)
        self.play_(FadeOut(VGroup(p2, trick, phi, logform, nofull)), rt=0.5)
        recap = label("two puzzles: track the end forever...", 19, ink)
        recap.move_to(UP * 0.4)
        self.play_(Write(recap), rt=1.4)

        self.cue(16)
        recap2 = label("...and know the beginning, without computing the middle", 19, ink)
        recap2.next_to(recap, DOWN, buff=0.4)
        self.play_(Write(recap2), rt=1.6)

        self.cue(17)
        self.finish(68.866667 + 1.3)


class sec3gpt(base):
    times = [0.0, 3.0, 10.76, 17.73, 25.29, 26.36, 31.23]
    def construct(self):
        self.start()
        hdr = pill("GPT-5.6 Sol", gpt)
        hdr.to_corner(UL, buff=0.45)
        sub = label("both halves, the expensive way", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        setup = label("solves both halves the more expensive way", 20, ink)
        setup.move_to(UP * 1.2)
        self.play_(Write(setup), rt=1.5)

        self.cue(1)
        self.play_(FadeOut(setup), rt=0.3)
        endlab = label("the ending: recalculates fresh at every index", 19, gpt)
        endlab.move_to(UP * 1.1)
        resetsym = label("resets each time --- no memory of the last check", 17, bad)
        resetsym.next_to(endlab, DOWN, buff=0.5)
        self.play_(Write(endlab), rt=1.4)
        self.play_(FadeIn(resetsym), rt=0.8)

        self.cue(2)
        restart = label("restarts over and over instead of building on what it knows", 16, dim)
        restart.next_to(resetsym, DOWN, buff=0.4)
        self.play_(FadeIn(restart), rt=1.4)

        self.cue(3)
        self.play_(FadeOut(VGroup(endlab, resetsym, restart)), rt=0.4)
        beglab = label("the beginning: computes the actual real number", 19, gpt)
        beglab.move_to(UP * 1.0)
        digits = digitrow("6885" + "\u2026", 22, ink)
        digits.next_to(beglab, DOWN, buff=0.5)
        self.play_(Write(beglab), rt=1.4)
        self.play_(FadeIn(digits), rt=0.9)

        self.cue(4)
        fulllab = label(f"the full thing --- about {ndigits:,} digits long", 17, dim)
        fulllab.next_to(digits, DOWN, buff=0.4)
        self.play_(FadeIn(fulllab), rt=1.1)

        self.cue(5)
        ok = label("both pieces done properly", 18, good)
        ok.next_to(fulllab, DOWN, buff=0.4)
        self.play_(FadeIn(ok), rt=0.9)
        self.hold(0.4)
        close = label("the most expensive honest version of each one", 18, bad)
        close.next_to(ok, DOWN, buff=0.4)
        self.play_(Write(close), rt=1.3)
        self.finish(31.233 + 1.3)


class sec4fable(base):
    times = [0.0, 3.13, 12.08, 17.22]
    def construct(self):
        self.start()
        hdr = pill("Fable", fable)
        hdr.to_corner(UL, buff=0.45)
        sub = label("speeds up both halves at once", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        only = label("the only one that speeds up both halves at once", 21, fable)
        only.move_to(UP * 1.1)
        self.play_(Write(only), rt=1.7)

        self.cue(1)
        tailtxt = label("tail carried forward --- never recalculated", 18, good)
        tailtxt.next_to(only, DOWN, buff=0.5)
        headtxt = label("front straight to the logarithm estimate --- no giant number built", 18, good)
        headtxt.next_to(tailtxt, DOWN, buff=0.3)
        self.play_(FadeIn(tailtxt), rt=1.1)
        self.play_(FadeIn(headtxt), rt=1.3)

        self.cue(2)
        same = label("same correct method as everyone else, underneath", 18, ink)
        same.next_to(headtxt, DOWN, buff=0.5)
        self.play_(FadeIn(same), rt=1.3)
        self.hold(0.3)
        close = label("just not paying for either expensive part", 20, gold)
        close.next_to(same, DOWN, buff=0.4)
        self.play_(Write(close), rt=1.3)
        self.finish(17.216604 + 1.3)


class sec5grok(base):
    times = [0.0, 1.65, 2.6, 9.71, 14.24, 18.66, 20.13, 25.73]
    def construct(self):
        self.start()
        hdr = pill("Grok 4.5", grok)
        hdr.to_corner(UL, buff=0.45)
        sub = label("speeds up one half of this", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        setup = label("speeds up one half of this", 20, grok)
        setup.move_to(UP * 1.2)
        self.play_(Write(setup), rt=1.3)

        self.cue(1)
        self.hold(0.1)

        self.cue(2)
        self.play_(FadeOut(setup), rt=0.3)
        endlab = label("the ending --- same story as GPT, recalculating fresh", 18, bad)
        endlab.move_to(UP * 1.1)
        self.play_(Write(endlab), rt=1.6)

        self.cue(3)
        beglab = label("the beginning --- uses the logarithm trick instead", 18, good)
        beglab.next_to(endlab, DOWN, buff=0.45)
        self.play_(Write(beglab), rt=1.5)

        self.cue(4)
        straight = label("straight to an estimate --- no massive number ever created", 16, dim)
        straight.next_to(beglab, DOWN, buff=0.4)
        self.play_(FadeIn(straight), rt=1.2)

        self.cue(5)
        half = label("half the savings", 22, gold)
        half.next_to(straight, DOWN, buff=0.5)
        self.play_(Write(half), rt=1.0)

        self.cue(6)
        recap = label("slow way of tracking the tail, fast way of handling the front", 16, ink)
        recap.next_to(half, DOWN, buff=0.4)
        self.play_(FadeIn(recap), rt=1.2)

        self.cue(7)
        self.finish(25.728521 + 1.3)


class sec6kimi(base):
    times = [0.0, 2.14, 7.91, 12.17, 14.3, 15.39, 18.52, 20.65, 23.74]
    def construct(self):
        self.start()
        hdr = pill("Kimi K3", kimi)
        hdr.to_corner(UL, buff=0.45)
        sub = label("does the opposite trade", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        setup = label("does the opposite trade", 21, kimi)
        setup.move_to(UP * 1.2)
        self.play_(Write(setup), rt=1.4)

        self.cue(1)
        self.play_(FadeOut(setup), rt=0.3)
        endlab = label("the ending --- carries the remainder forward the whole time", 18, good)
        endlab.move_to(UP * 1.1)
        self.play_(Write(endlab), rt=1.7)

        self.cue(2)
        neverstart = label("one step building on the last, never starting over", 16, dim)
        neverstart.next_to(endlab, DOWN, buff=0.4)
        self.play_(FadeIn(neverstart), rt=1.1)

        self.cue(3)
        beglab = label("the beginning --- builds the real number, full sized", 18, bad)
        beglab.next_to(neverstart, DOWN, buff=0.45)
        self.play_(Write(beglab), rt=1.5)

        self.cue(4)
        self.hold(0.1)

        self.cue(5)
        readoff = label("reads off the leading digits directly", 16, dim)
        readoff.next_to(beglab, DOWN, buff=0.4)
        self.play_(FadeIn(readoff), rt=1.0)

        self.cue(6)
        self.play_(FadeOut(VGroup(endlab, neverstart, beglab, readoff)), rt=0.4)
        saves = label("saves time on the half Grok didn't", 19, good)
        saves.move_to(UP * 0.5)
        self.play_(Write(saves), rt=1.3)

        self.cue(7)
        spends = label("spends time on the half Grok saved", 19, bad)
        spends.next_to(saves, DOWN, buff=0.4)
        self.play_(Write(spends), rt=1.3)

        self.cue(8)
        self.finish(23.745292 + 1.3)


class sec7evalverdict(base):
    times = [0.0, 6.92, 14.36, 19.45, 21.46, 23.17, 27.79, 33.36, 39.54, 47.51, 49.48, 56.84, 60.15, 62.48, 63.4]
    def construct(self):
        self.start()
        head = label("Eval & Verdict", 30)
        head.to_edge(UP, buff=0.55)
        self.play_(Write(head), rt=1.0)

        self.cue(0)
        allfour = label(f"all four land on index {fmtnum(answer_idx)}", 21, gold)
        allfour.move_to(UP * 1.1)
        self.play_(Write(allfour), rt=1.7)

        names = ["GPT-5.6 Sol", "Grok 4.5", "Kimi K3", "Fable"]
        cols = {"GPT-5.6 Sol": gpt, "Grok 4.5": grok, "Kimi K3": kimi, "Fable": fable}
        scs = VGroup()
        for nm in names:
            box = RoundedRectangle(corner_radius=0.08, width=4.6, height=0.78).set_fill(panel, 1).set_stroke(gridcol, 1.2)
            lab = label(nm, 18, cols[nm]).move_to(box.get_left() + RIGHT * 1.0)
            scs.add(VGroup(box, lab))
        scs.arrange(DOWN, buff=0.22).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.2)
        focus = LEFT * 3.2 + UP * 0.1

        def note(i, txt, col):
            nt = label(txt, 14, col)
            nt.move_to(scs[i][0].get_right() + LEFT * 1.5)
            self.play_(FadeIn(nt, shift=LEFT * 0.15), rt=0.5)

        self.cue(1)
        self.play_(FadeOut(allfour), rt=0.3)
        self.play_(*[FadeIn(r[0]) for r in scs], *[FadeIn(r[1]) for r in scs], rt=1.0)
        gf = pill("GPT-5.6 Sol", gpt, w=3.1, h=0.9, size=22)
        gf.move_to(focus)
        self.play_(FadeIn(gf, shift=DOWN * 0.2), rt=0.6)

        self.cue(2)
        g1 = label("pays for both expensive parts", 16, gpt)
        g1.next_to(gf, DOWN, buff=0.45)
        self.play_(Write(g1), rt=1.3)

        self.cue(3)
        note(0, "slowest", bad)

        self.cue(4)
        self.play_(FadeOut(VGroup(gf, g1)), rt=0.4)
        rf = pill("Grok 4.5", grok, w=3.1, h=0.9, size=22)
        rf.move_to(focus)
        self.play_(FadeIn(rf, shift=DOWN * 0.2), rt=0.6)

        self.cue(5)
        r1 = label("saves on the front with the logarithm trick", 16, grok)
        r1.next_to(rf, DOWN, buff=0.45)
        self.play_(Write(r1), rt=1.3)

        self.cue(6)
        r2 = label("still recalculates the tail from scratch each time", 16, ink)
        r2.next_to(r1, DOWN, buff=0.22)
        self.play_(Write(r2), rt=1.4)
        note(1, "3rd", dim)

        self.cue(7)
        self.play_(FadeOut(VGroup(rf, r1, r2)), rt=0.4)
        kf = pill("Kimi K3", kimi, w=3.1, h=0.9, size=22)
        kf.move_to(focus)
        self.play_(FadeIn(kf, shift=DOWN * 0.2), rt=0.6)

        self.cue(8)
        k1 = label("the reverse --- keeps the tail running efficiently", 16, kimi)
        k1.next_to(kf, DOWN, buff=0.45)
        self.play_(Write(k1), rt=1.3)
        k2 = label("but still builds the real number for the front", 16, ink)
        k2.next_to(k1, DOWN, buff=0.22)
        self.play_(Write(k2), rt=1.3)
        note(2, "2nd", dim)

        self.cue(9)
        self.play_(FadeOut(VGroup(kf, k1, k2)), rt=0.4)
        ff = pill("Fable", fable, w=3.1, h=0.9, size=22)
        ff.move_to(focus)
        crown = Polygon([-0.4, 0, 0], [-0.24, 0.32, 0], [0, 0.06, 0], [0.24, 0.32, 0], [0.4, 0, 0]).set_fill(gold, 1).set_stroke(gold, 1).scale(0.85)
        crown.next_to(ff, UP, buff=0.12)
        self.play_(FadeIn(ff, shift=DOWN * 0.2), rt=0.6)
        self.play_(FadeIn(crown, shift=DOWN * 0.3), rt=0.5)

        self.cue(10)
        f1 = label("does both at once --- efficient the entire way through", 16, fable)
        f1.next_to(ff, DOWN, buff=0.45)
        self.play_(Write(f1), rt=1.5)
        note(3, "winner", gold)

        self.cue(11)
        winlab = label("the winner's Fable", 22, gold)
        winlab.next_to(f1, DOWN, buff=0.5)
        self.play_(Write(winlab), rt=1.4)

        self.cue(12)
        self.play_(FadeOut(VGroup(ff, crown, f1, winlab)), rt=0.3)
        idxlab = label(f"index {fmtnum(answer_idx)}", 24, gold)
        idxlab.move_to(focus + UP * 0.9)
        headrow = digitrow(head9, 18, dim)
        tailrow = digitrow(tail9, 18, gold)
        headrow.next_to(idxlab, DOWN, buff=0.4)
        tailrow.next_to(headrow, DOWN, buff=0.25)
        self.play_(FadeIn(idxlab), rt=0.4)
        self.play_(FadeIn(headrow), rt=0.6)
        self.play_(FadeIn(tailrow), rt=0.6)
        moral = label("it's really just about not undoing your own progress", 17, dim)
        moral.to_edge(DOWN, buff=0.85)
        self.play_(Write(moral), rt=1.0)
        self.finish(63.404271 + 1.3)
