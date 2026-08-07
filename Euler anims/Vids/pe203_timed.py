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
                 ("×", r"$\times$"), ("≈", r"$\approx$"), ("—", "---"), ("·", r"$\cdot$")]:
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

def sieveprimes(limit):
    s = [True] * (limit + 1)
    s[0] = s[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, limit + 1, i):
                s[j] = False
    return [i for i in range(limit + 1) if s[i]]

ROWS = 51
trirows = []
row = [1]
trirows.append(row[:])
for n in range(1, ROWS):
    newrow = [1] * (n + 1)
    for k in range(1, n):
        newrow[k] = row[k - 1] + row[k]
    row = newrow
    trirows.append(row[:])

primes50 = sieveprimes(50)

def sqfree(v, primes=primes50):
    for p in primes:
        if p * p > v:
            break
        if v % (p * p) == 0:
            return False
    return True

distinctvals = set()
for r in trirows:
    distinctvals.update(r)

answer = sum(v for v in distinctvals if sqfree(v))
kimianswer = sum(v for r in trirows for v in r if sqfree(v))
maxval = max(distinctvals)
ndistinct = len(distinctvals)

d8 = set()
for n in range(8):
    d8.update(trirows[n])
sum8 = sum(v for v in d8 if sqfree(v))

def trianglemini(nrows=8, center=ORIGIN, colgap=0.68, rowgap=0.6, size=24, badvals=None):
    badvals = badvals or set()
    grp = VGroup()
    for n in range(nrows):
        y = (nrows - 1) / 2 * rowgap - n * rowgap
        r = trirows[n]
        for k, v in enumerate(r):
            x = (k - n / 2) * colgap
            col = bad if v in badvals else ink
            t = label(str(v), size, col)
            t.move_to(center + np.array([x, y, 0]))
            grp.add(t)
    return grp

def bigtridots(nrows=51, center=ORIGIN, colgap=0.155, rowgap=0.112, r=0.026):
    grp = VGroup()
    for n in range(nrows):
        y = (nrows - 1) / 2 * rowgap - n * rowgap
        rw = trirows[n]
        for k, v in enumerate(rw):
            x = (k - n / 2) * colgap
            col = good if sqfree(v) else faint
            d = Dot(center + np.array([x, y, 0]), radius=r, color=col)
            grp.add(d)
    return grp

def bulgearc(p1, p2, height, color, sw=2.5):
    mid = (p1 + p2) / 2
    down = np.array([0, -1, 0]) * height
    c1 = p1 + (mid - p1) * 0.5 + down
    c2 = p2 + (mid - p2) * 0.5 + down
    return CubicBezier(p1, c1, c2, p2, color=color, stroke_width=sw)

def primechecklist(primes, center=ORIGIN, gap=0.64, r=0.27, size=15, color=fable):
    grp = VGroup()
    n = len(primes)
    for i, p in enumerate(primes):
        x = (i - (n - 1) / 2) * gap
        c = Circle(radius=r, color=color, stroke_width=2).move_to(center + np.array([x, 0, 0]))
        t = label(str(p), size, color).move_to(c)
        grp.add(VGroup(c, t))
    return grp


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
    times = [0.0, 0.57, 7.9, 14.65, 19.54, 23.55, 26.22, 29.98]
    def construct(self):
        self.start()
        self.cue(0)
        tri = trianglemini(nrows=6, colgap=0.72, rowgap=0.62)
        seen = label("you've seen this shape before", 22, dim)
        seen.to_edge(UP, buff=0.6)
        self.play_(FadeIn(seen), rt=0.6)
        self.play_(LaggedStart(*[FadeIn(t, scale=0.7) for t in tri], lag_ratio=0.04), rt=1.5)

        self.cue(1)
        tri8 = trianglemini(nrows=8, colgap=0.72, rowgap=0.62)
        self.play_(Transform(tri, tri8), rt=1.6)
        addrule = label("each one's the two above it, added together", 18, ink)
        addrule.to_edge(DOWN, buff=0.85)
        self.play_(FadeIn(addrule), rt=1.1)

        self.cue(2)
        self.play_(FadeOut(addrule), rt=0.3)
        four = trianglemini(nrows=8, colgap=0.72, rowgap=0.62, badvals={4})
        self.play_(Transform(tri, four), rt=0.8)
        fourlab = label("4 = 2 @\\times@ 2 --- a square hides inside it", 18, bad)
        fourlab.to_edge(DOWN, buff=0.85)
        self.play_(Write(fourlab), rt=1.4)

        self.cue(3)
        self.play_(FadeOut(fourlab), rt=0.3)
        goodlab = label("most of them are squarefree --- no square hides inside", 18, good)
        goodlab.to_edge(DOWN, buff=0.85)
        self.play_(Write(goodlab), rt=1.5)

        self.cue(4)
        self.play_(FadeOut(VGroup(seen, tri, goodlab)), rt=0.4)
        setup = label("so I gave the same question to four AIs --- no hints", 21, ink)
        setup.move_to(UP * 0.3)
        self.play_(Write(setup), rt=1.8)

        self.cue(5)
        self.play_(FadeOut(setup), rt=0.3)
        names = ["GPT-5.6 Sol", "Fable", "Grok 4.5", "Kimi K3"]
        cols = [gpt, fable, grok, kimi]
        chips = VGroup(*[pill(n, c, w=2.55, h=0.72, size=19) for n, c in zip(names, cols)])
        chips.arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        self.play_(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips], lag_ratio=0.15), rt=1.3)

        self.cue(6)
        nohint = label("same starting point, same rules, no help", 18, dim)
        nohint.next_to(chips, DOWN, buff=0.5)
        self.play_(FadeIn(nohint), rt=0.9)

        self.cue(7)
        self.play_(FadeOut(nohint), rt=0.3)
        twist = label("this time, the fastest one was also the only one instant", 19, gold)
        twist.next_to(chips, DOWN, buff=0.5)
        self.play_(Write(twist), rt=2.0)
        self.finish(34.155479 + 1.3)


class sec2problem(base):
    times = [0.0, 12.23, 16.39, 18.98, 21.14, 29.56, 32.23, 33.11, 37.36, 39.97, 41.88]
    def construct(self):
        self.start()
        ttl = label("Pascal's Triangle", 30)
        ttl.to_edge(UP, buff=0.55)
        self.play_(Write(ttl), rt=1.0)

        self.cue(0)
        tri = trianglemini(nrows=8, colgap=0.72, rowgap=0.6, center=DOWN * 0.2)
        self.play_(LaggedStart(*[FadeIn(t, scale=0.7) for t in tri], lag_ratio=0.03), rt=1.8)
        defn = label("squarefree: no perfect square (besides 1) divides it", 18, ink)
        defn.to_edge(DOWN, buff=0.85)
        self.play_(FadeIn(defn), rt=1.1)

        self.cue(1)
        self.play_(FadeOut(defn), rt=0.3)
        marked = trianglemini(nrows=8, colgap=0.72, rowgap=0.6, center=DOWN * 0.2, badvals={4, 20})
        self.play_(Transform(tri, marked), rt=1.0)
        exdef = label("4 = 2@\\times@2, and 20 = 2@\\times@2@\\times@5 --- not squarefree", 18, bad)
        exdef.to_edge(DOWN, buff=0.85)
        self.play_(Write(exdef), rt=1.6)

        self.cue(2)
        self.play_(FadeOut(exdef), rt=0.3)
        cnt = label(f"12 distinct numbers show up in these 8 rows", 18, dim)
        cnt.to_edge(DOWN, buff=0.85)
        self.play_(Write(cnt), rt=1.4)

        self.cue(3)
        self.play_(FadeOut(cnt), rt=0.3)
        s105 = label(f"sum of the squarefree ones @\\to@ {sum8}", 22, good)
        s105.to_edge(DOWN, buff=0.85)
        self.play_(Write(s105), rt=1.5)

        self.cue(4)
        self.play_(FadeOut(VGroup(tri, s105)), rt=0.4)
        real = label("that's the warm-up. the real question uses 51 rows", 21, ink)
        real.move_to(UP * 0.3)
        self.play_(Write(real), rt=1.8)

        self.cue(5)
        self.play_(FadeOut(real), rt=0.3)
        big = bigtridots(nrows=51, center=DOWN * 0.15)
        self.play_(FadeIn(big, run_time=1), rt=1.6)

        self.cue(6)
        dc = label(f"{ndistinct} distinct values live in there", 19, dim)
        dc.to_edge(UP, buff=1.15)
        self.play_(FadeIn(dc), rt=1.0)

        self.cue(7)
        self.hold(0.3)

        self.cue(8)
        self.play_(FadeOut(dc), rt=0.3)
        q = label("what's the sum of every squarefree one --- now?", 20, gold)
        q.to_edge(DOWN, buff=0.85)
        self.play_(Write(q), rt=2.0)

        self.cue(9)
        self.play_(FadeOut(VGroup(ttl, big, q)), rt=0.5)

        self.cue(10)
        self.finish(41.878563 + 1.3)


class sec3gpt(base):
    times = [0.0, 8.18, 11.22, 16.05, 22.95, 25.28, 28.02, 29.46, 32.1, 35.43]
    def construct(self):
        self.start()
        hdr = pill("GPT-5.6 Sol", gpt)
        hdr.to_corner(UL, buff=0.45)
        sub = label("checks every number, one at a time", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        big = label(fmtnum(maxval), 34, gpt)
        big.move_to(UP * 1.0)
        tag = label("the largest value in the whole triangle", 17, ink)
        tag.next_to(big, DOWN, buff=0.4)
        self.play_(Write(big), rt=1.2)
        self.play_(FadeIn(tag), rt=0.8)

        self.cue(1)
        self.play_(FadeOut(tag), rt=0.3)
        ticker = label("k = 2", 24, ink)
        ticker.next_to(big, DOWN, buff=0.5)
        self.play_(FadeIn(ticker), rt=0.4)
        for kv in [3, 47, 512, 9931, 84207, 1220441, 3355210]:
            nxt = label(f"k = {kv:,}", 24, ink)
            nxt.move_to(ticker)
            self.play_(Transform(ticker, nxt), rt=0.18)

        self.cue(2)
        checkmark = label("@\\checkmark@ eventually finishes --- this one's fine", 18, good)
        checkmark.next_to(ticker, DOWN, buff=0.4)
        self.play_(FadeIn(checkmark), rt=1.0)

        self.cue(3)
        self.play_(FadeOut(VGroup(big, ticker, checkmark)), rt=0.4)
        many = label(f"but there are {ndistinct} of these to check", 21, ink)
        many.move_to(UP * 0.5)
        self.play_(Write(many), rt=1.6)

        self.cue(4)
        self.play_(FadeOut(many), rt=0.3)
        clock = label("~7 minutes", 40, bad)
        clock.move_to(UP * 0.4)
        clocksub = label("trial division by every integer, not just primes", 17, dim)
        clocksub.next_to(clock, DOWN, buff=0.4)
        self.play_(Write(clock), rt=1.2)
        self.play_(FadeIn(clocksub), rt=1.0)

        self.cue(5)
        stillgo = label("still running when the other three were done", 18, ink)
        stillgo.next_to(clocksub, DOWN, buff=0.4)
        self.play_(FadeIn(stillgo), rt=1.2)

        self.cue(6)
        self.play_(FadeOut(VGroup(clock, clocksub, stillgo)), rt=0.4)
        dq = label("disqualified", 36, bad)
        dq.move_to(UP * 0.3)
        dqbox = SurroundingRectangle(dq, buff=0.25).set_stroke(bad, 2.2)
        self.play_(Write(dq), rt=1.0)
        self.play_(Create(dqbox), rt=0.6)

        self.cue(7)
        self.hold(0.3)

        self.cue(8)
        moral = label("not wrong math. just the wrong plan", 18, dim)
        moral.next_to(dqbox, DOWN, buff=0.5)
        self.play_(Write(moral), rt=1.6)

        self.cue(9)
        self.finish(35.435729 + 1.3)


class sec4fable(base):
    times = [0.0, 3.98, 9.2, 12.32, 14.35, 18.7, 19.47, 25.23, 29.66]
    def construct(self):
        self.start()
        hdr = pill("Fable", fable)
        hdr.to_corner(UL, buff=0.45)
        sub = label("you never need more than 15 primes", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        rowlab = label("51 rows means every number tops out around n = 50", 19, ink)
        rowlab.move_to(UP * 1.2)
        self.play_(Write(rowlab), rt=1.6)

        self.cue(1)
        self.play_(FadeOut(rowlab), rt=0.3)
        insight = label("a prime bigger than 50 can never divide any of them", 19, fable)
        insight.move_to(UP * 1.2)
        self.play_(Write(insight), rt=1.9)

        self.cue(2)
        chk = primechecklist(primes50, center=DOWN * 0.3)
        self.play_(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chk], lag_ratio=0.05), rt=1.4)
        onlylab = label("only these 15 primes are worth checking", 17, dim)
        onlylab.next_to(chk, DOWN, buff=0.5)
        self.play_(FadeIn(onlylab), rt=0.9)

        self.cue(3)
        self.play_(FadeOut(onlylab), rt=0.3)
        ticks = VGroup()
        for c in chk:
            tk = label("@\\checkmark@", 16, good).move_to(c[0].get_bottom() + DOWN * 0.28)
            ticks.add(tk)
        self.play_(LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.04), rt=0.9)

        self.cue(4)
        self.play_(FadeOut(VGroup(insight, chk, ticks)), rt=0.4)
        res = label(fmtnum(answer), 30, good)
        res.move_to(UP * 0.4)
        self.play_(Write(res), rt=1.4)

        self.cue(5)
        speedlab = label("under a millisecond", 22, gold)
        speedlab.next_to(res, DOWN, buff=0.4)
        self.play_(Write(speedlab), rt=1.3)

        self.cue(6)
        self.hold(0.3)

        self.cue(7)
        winlab = label("Fable's first win of the series", 20, fable)
        winlab.next_to(speedlab, DOWN, buff=0.55)
        self.play_(Write(winlab), rt=1.6)

        self.cue(8)
        self.finish(32.811521 + 1.3)


class sec5grok(base):
    times = [0.0, 2.91, 10.25, 18.79, 21.72, 23.45, 26.64]
    def construct(self):
        self.start()
        hdr = pill("Grok 4.5", grok)
        hdr.to_corner(UL, buff=0.45)
        sub = label("correct, just a lot more homework", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        approach = label("Grok also checks prime squares --- but doesn't see the shortcut", 18, ink)
        approach.move_to(UP * 1.2)
        self.play_(Write(approach), rt=1.7)

        self.cue(1)
        self.play_(FadeOut(approach), rt=0.3)
        lim = math.isqrt(maxval)
        boundlab = label(f"it sieves every prime up to {fmtnum(lim)}", 19, grok)
        boundlab.move_to(UP * 1.2)
        self.play_(Write(boundlab), rt=1.8)

        self.cue(2)
        strip = Rectangle(width=9.5, height=0.55, color=grok, fill_color=grok, fill_opacity=0.65, stroke_width=1.5)
        strip.move_to(DOWN * 0.5)
        stripL = label("2", 15, ink).next_to(strip, LEFT, buff=0.25)
        stripR = label(f"{fmtnum(lim)}", 15, ink).next_to(strip, RIGHT, buff=0.25)
        tiny = Rectangle(width=0.12, height=0.55, color=fable, fill_color=fable, fill_opacity=0.9, stroke_width=0).move_to(strip.get_left() + RIGHT * 0.06)
        tinylab = label("Fable only needed this sliver", 15, fable)
        tinylab.next_to(strip, DOWN, buff=0.35)
        self.play_(Create(strip), FadeIn(stripL), FadeIn(stripR), rt=1.3)
        self.play_(FadeIn(tiny), FadeIn(tinylab), rt=1.0)

        self.cue(3)
        self.play_(FadeOut(VGroup(boundlab, strip, stripL, stripR, tiny, tinylab)), rt=0.5)
        res = label(fmtnum(answer), 30, good)
        res.move_to(UP * 0.4)
        self.play_(Write(res), rt=1.4)
        okmark = label("@\\checkmark@ exact same answer as Fable", 18, good)
        okmark.next_to(res, DOWN, buff=0.4)
        self.play_(FadeIn(okmark), rt=1.0)

        self.cue(4)
        self.play_(FadeOut(okmark), rt=0.3)
        speedlab = label("about 3 seconds", 22, dim)
        speedlab.next_to(res, DOWN, buff=0.4)
        self.play_(Write(speedlab), rt=1.2)

        self.cue(5)
        self.hold(0.3)

        self.cue(6)
        redlab = label("solid 2nd --- no shortcuts, just brute force done right", 18, grok)
        redlab.next_to(speedlab, DOWN, buff=0.55)
        self.play_(Write(redlab), rt=1.9)
        self.finish(31.895063 + 1.3)


class sec6kimi(base):
    times = [0.0, 10.43, 12.78, 14.13, 22.11, 24.0, 32.82, 35.37]
    def construct(self):
        self.start()
        hdr = pill("Kimi K3", kimi)
        hdr.to_corner(UL, buff=0.45)
        sub = label("forgot to remove the repeats", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        rowvals = trirows[7]
        rw = VGroup(*[label(str(v), 26, ink) for v in rowvals])
        rw.arrange(RIGHT, buff=0.55).move_to(UP * 0.6)
        self.play_(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in rw], lag_ratio=0.08), rt=1.2)
        rowtag = label("one row of the triangle --- row 7", 16, dim)
        rowtag.next_to(rw, UP, buff=0.4)
        self.play_(FadeIn(rowtag), rt=0.8)

        self.cue(1)
        pairs = [(1, 6), (2, 5), (3, 4)]
        arcs = VGroup()
        for a, b in pairs:
            arc = bulgearc(rw[a].get_bottom(), rw[b].get_bottom(), 0.32, bad)
            arcs.add(arc)
        self.play_(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.2), rt=1.4)
        pairlab = label("35, 21, and 7 each show up twice in this row alone", 17, bad)
        pairlab.to_edge(DOWN, buff=0.85)
        self.play_(Write(pairlab), rt=1.8)

        self.cue(2)
        self.play_(FadeOut(pairlab), rt=0.3)
        nodedup = label("Kimi sums every appearance --- no de-duplication", 18, bad)
        nodedup.to_edge(DOWN, buff=0.85)
        self.play_(Write(nodedup), rt=1.5)

        self.cue(3)
        self.hold(0.3)

        self.cue(4)
        self.play_(FadeOut(VGroup(rw, rowtag, arcs, nodedup)), rt=0.4)
        tally = label("0", 30, ink)
        tally.move_to(UP * 0.3)
        self.play_(Write(tally), rt=0.6)
        steps = [answer // 3, answer, int(answer * 1.5), kimianswer]
        for sv in steps:
            nt = label(fmtnum(sv), 30, ink).move_to(tally)
            self.play_(Transform(tally, nt), rt=0.35)

        self.cue(5)
        wrongtag = label("@\\times@ wrong", 24, bad)
        wrongtag.next_to(tally, DOWN, buff=0.4)
        self.play_(FadeIn(wrongtag), rt=0.9)

        self.cue(6)
        ratio = label(f"almost exactly double the real answer", 19, dim)
        ratio.next_to(wrongtag, DOWN, buff=0.5)
        self.play_(Write(ratio), rt=1.7)

        self.cue(7)
        self.finish(36.758583 + 1.3)


class sec7eval(base):
    times = [0.0, 5.75, 10.26, 14.05]
    def construct(self):
        self.start()
        self.cue(0)
        ttl = label("Side by Side", 30)
        ttl.to_edge(UP, buff=0.55)
        self.play_(Write(ttl), rt=1.0)
        rows = [
            ("GPT-5.6 Sol", gpt, "every integer, no shortcut", "correct --- 7 minutes", bad),
            ("Fable", fable, "primes up to 50 only", f"{fmtnum(answer)} --- instant", good),
            ("Grok 4.5", grok, "primes up to 11 million", f"{fmtnum(answer)} --- 3 seconds", good),
            ("Kimi K3", kimi, "no de-duplication", "wrong --- double counted", bad),
        ]
        cards = VGroup()
        for nm, col, meth, res, rc in rows:
            box = RoundedRectangle(corner_radius=0.1, width=10.8, height=0.92).set_fill(panel, 1).set_stroke(col, 1.6)
            nmlab = label(nm, 20, col).move_to(box.get_left() + RIGHT * 1.5)
            mlab = label(meth, 15, ink).move_to(box.get_center() + LEFT * 0.3)
            rlab = label(res, 15, rc).move_to(box.get_right() + LEFT * 2.1)
            cards.add(VGroup(box, nmlab, mlab, rlab))
        cards.arrange(DOWN, buff=0.26).move_to(DOWN * 0.15)

        self.cue(1)
        self.play_(FadeIn(cards[0], shift=RIGHT * 0.25), rt=0.75)
        self.play_(FadeIn(cards[1], shift=RIGHT * 0.25), rt=0.75)

        self.cue(2)
        self.play_(FadeIn(cards[2], shift=RIGHT * 0.25), rt=0.75)
        self.play_(FadeIn(cards[3], shift=RIGHT * 0.25), rt=0.75)
        summ = label("two correct, one too slow, one too sloppy", 17, dim)
        summ.next_to(cards, DOWN, buff=0.4)
        self.play_(Write(summ), rt=1.6)

        self.cue(3)
        self.finish(19.285917 + 1.3)


class sec8verdict(base):
    times = [0.0, 4.79, 12.4, 16.82, 26.21, 31.03, 35.04, 43.09, 48.28]
    def construct(self):
        self.start()
        head = label("The Verdict", 32)
        head.to_edge(UP, buff=0.5)
        names = ["GPT-5.6 Sol", "Fable", "Grok 4.5", "Kimi K3"]
        cols = {"GPT-5.6 Sol": gpt, "Fable": fable, "Grok 4.5": grok, "Kimi K3": kimi}
        scs = VGroup()
        for nm in names:
            box = RoundedRectangle(corner_radius=0.08, width=4.6, height=0.78).set_fill(panel, 1).set_stroke(gridcol, 1.2)
            lab = label(nm, 18, cols[nm]).move_to(box.get_left() + RIGHT * 1.0)
            scs.add(VGroup(box, lab))
        scs.arrange(DOWN, buff=0.22).to_edge(RIGHT, buff=0.5)
        focus = LEFT * 3.2 + UP * 0.3

        def note(i, txt, col):
            nt = label(txt, 14, col)
            nt.move_to(scs[i][0].get_right() + LEFT * 1.5)
            self.play_(FadeIn(nt, shift=LEFT * 0.15), rt=0.5)

        self.cue(0)
        self.play_(Write(head), rt=0.8)
        self.play_(*[FadeIn(r[0]) for r in scs], *[FadeIn(r[1]) for r in scs], rt=1.0)
        ff = pill("Fable", fable, w=3.1, h=0.9, size=23)
        ff.move_to(focus)
        crown = Polygon([-0.4, 0, 0], [-0.24, 0.32, 0], [0, 0.06, 0], [0.24, 0.32, 0], [0.4, 0, 0]).set_fill(gold, 1).set_stroke(gold, 1).scale(0.85)
        crown.next_to(ff, UP, buff=0.12)
        self.play_(FadeIn(ff, shift=DOWN * 0.2), rt=0.6)
        self.play_(FadeIn(crown, shift=DOWN * 0.3), rt=0.5)

        self.cue(1)
        f1 = label("fifteen primes was all it ever needed", 16, fable)
        f1.next_to(ff, DOWN, buff=0.45)
        self.play_(Write(f1), rt=1.1)
        note(1, "winner", gold)
        f2 = label("correct, and under a millisecond to get there", 16, ink)
        f2.next_to(f1, DOWN, buff=0.22)
        self.play_(Write(f2), rt=1.2)

        self.cue(2)
        self.play_(FadeOut(VGroup(ff, crown, f1, f2)), rt=0.4)
        rf = pill("Grok 4.5", grok, w=3.1, h=0.9, size=23)
        rf.move_to(focus)
        self.play_(FadeIn(rf, shift=DOWN * 0.2), rt=0.6)

        self.cue(3)
        r1 = label("didn't see the shortcut, brute-forced it instead", 16, grok)
        r1.next_to(rf, DOWN, buff=0.45)
        self.play_(Write(r1), rt=1.2)
        note(2, "2nd, correct", grok)
        r2 = label("same right answer, about 3 seconds to get there", 16, ink)
        r2.next_to(r1, DOWN, buff=0.22)
        self.play_(Write(r2), rt=1.3)

        self.cue(4)
        self.play_(FadeOut(VGroup(rf, r1, r2)), rt=0.4)
        gf = pill("GPT-5.6 Sol", gpt, w=3.1, h=0.9, size=23)
        gf.move_to(focus)
        self.play_(FadeIn(gf, shift=DOWN * 0.2), rt=0.6)

        self.cue(5)
        g1 = label("checked every integer instead of just primes", 16, gpt)
        g1.next_to(gf, DOWN, buff=0.45)
        self.play_(Write(g1), rt=1.2)
        note(0, "disqualified", bad)
        g2 = label("would've gotten there --- about 7 minutes late", 16, ink)
        g2.next_to(g1, DOWN, buff=0.22)
        self.play_(Write(g2), rt=1.3)

        self.cue(6)
        self.play_(FadeOut(VGroup(gf, g1, g2)), rt=0.4)
        kf = pill("Kimi K3", kimi, w=3.1, h=0.9, size=23)
        kf.move_to(focus)
        self.play_(FadeIn(kf, shift=DOWN * 0.2), rt=0.6)

        self.cue(7)
        k1 = label("never deduplicated --- counted every repeat", 16, kimi)
        k1.next_to(kf, DOWN, buff=0.45)
        self.play_(Write(k1), rt=0.9)
        note(3, "wrong", bad)
        k2 = label("landed at almost exactly double the real total", 16, ink)
        k2.next_to(k1, DOWN, buff=0.22)
        self.play_(Write(k2), rt=1.0)
        self.play_(FadeOut(VGroup(kf, k1, k2)), rt=0.3)
        fin1 = label("Project Euler 203", 20, dim)
        fin1.move_to(focus + UP * 0.6)
        fin2 = label(fmtnum(answer), 34, gold)
        fin2.next_to(fin1, DOWN, buff=0.35)
        fbox = SurroundingRectangle(fin2, buff=0.2).set_stroke(gold, 2)
        self.play_(FadeIn(fin1), rt=0.4)
        self.play_(Write(fin2), rt=0.8)
        self.play_(Create(fbox), rt=0.4)

        self.cue(8)
        closing = label("same four next time --- probably a different winner too", 16, dim)
        closing.to_edge(DOWN, buff=0.9)
        self.play_(Write(closing), rt=1.6)
        self.finish(50.518396 + 1.3)
