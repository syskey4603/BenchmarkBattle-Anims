from manim import *
import numpy as np
import math
import re

config.background_color = "#0A0A15"

mono = "DejaVu Sans Mono"
grok = "#FF4500"
gpt = "#10A37F"
kimi = "#9D6FFF"
claude = "#E8925C"
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
                 ("×", r"$\times$"), ("≈", r"$\approx$"), ("—", "---"), ("·", r"$\cdot$"), ("≤", r"$\leq$")]:
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

LIMIT = 100_000_000
SMALL_BOUND = 10_000
Q_BOUND = 50_000_000
NUM_SMALL_PRIMES = 1229
NUM_BIG_PRIMES = 3_001_134
BSEARCH_STEPS = 22
ANSWER = 17_427_258


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


def dotcluster(n, center=ORIGIN, side=2.2, r=0.02, color=good):
    cols = int(math.sqrt(n))
    rows = (n + cols - 1) // cols
    dots = VGroup()
    for i in range(n):
        x = (i % cols) / max(cols - 1, 1) * side - side / 2
        y = (i // cols) / max(rows - 1, 1) * side - side / 2
        dots.add(Dot(center + np.array([x, y, 0]), radius=r, color=color))
    return dots


class sec1title(base):
    times = [0.0, 3.79, 6.07, 7.13, 9.68, 14.36, 18.69, 25.68, 28.84, 31.49]
    def construct(self):
        self.start()
        self.cue(0)
        ttl = label("semiprimes", 28, ink)
        ttl.move_to(UP * 1.2)
        sub = label("numbers with exactly two prime factors", 19, dim)
        sub.next_to(ttl, DOWN, buff=0.4)
        self.play_(Write(ttl), rt=1.0)
        self.play_(FadeIn(sub), rt=0.6)

        self.cue(1)
        four = label("4 = 2 \u00d7 2", 26, good)
        four.move_to(DOWN * 0.6 + LEFT * 3.2)
        self.play_(FadeIn(four, shift=UP * 0.2), rt=0.6)

        self.cue(2)
        six = label("6 = 2 \u00d7 3", 26, good)
        six.move_to(DOWN * 0.6)
        self.play_(FadeIn(six, shift=UP * 0.2), rt=0.6)

        self.cue(3)
        eight = label("8 = 2 \u00d7 2 \u00d7 2", 26, bad)
        eight.move_to(DOWN * 0.6 + RIGHT * 3.2)
        self.play_(FadeIn(eight, shift=UP * 0.2), rt=0.6)
        badtag = label("three factors --- not two", 16, bad)
        badtag.next_to(eight, DOWN, buff=0.3)
        self.play_(FadeIn(badtag), rt=0.5)

        self.cue(4)
        self.play_(FadeOut(VGroup(ttl, sub, four, six, eight, badtag)), rt=0.3)
        pe = label("Project Euler 187", 26, gold)
        pe.move_to(UP * 0.5)
        self.play_(Write(pe), rt=1.1)

        self.cue(5)
        goal = label(f"every semiprime below {fmtnum(LIMIT)}", 20, ink)
        goal.next_to(pe, DOWN, buff=0.5)
        self.play_(FadeIn(goal), rt=1.0)

        self.cue(6)
        self.play_(FadeOut(goal), rt=0.3)
        brute = label("checking a hundred million numbers one at a time", 18, bad)
        brute.next_to(pe, DOWN, buff=0.5)
        self.play_(Write(brute), rt=1.3)
        self.hold(1.5)
        self.play_(FadeOut(VGroup(pe, brute)), rt=0.4)
        sharper = label("there's a much sharper way to think about this", 20, ink)
        sharper.move_to(UP * 0.3)

        self.cue(7)
        self.play_(Write(sharper), rt=1.6)

        self.cue(8)
        self.play_(FadeOut(sharper), rt=0.3)
        names = ["Claude", "GPT-5.6 Sol", "Kimi K3", "Grok 4.5"]
        cols = [claude, gpt, kimi, grok]
        chips = VGroup(*[pill(n, c, w=2.55, h=0.72, size=18) for n, c in zip(names, cols)])
        chips.arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        self.play_(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips], lag_ratio=0.25), rt=2.0)

        self.cue(9)
        twocosts = label("two separate technical choices, stacking on top of each other", 17, gold)
        twocosts.next_to(chips, DOWN, buff=0.5)
        self.play_(Write(twocosts), rt=1.4)
        self.finish(33.452313 + 1.3)


class sec2problem(base):
    times = [0.0, 6.47, 16.81, 21.83, 25.56, 30.81, 41.98, 46.15, 61.04, 67.46, 72.25]
    def construct(self):
        self.start()
        ttl = label("Counting Semiprimes", 28)
        ttl.to_edge(UP, buff=0.55)
        self.play_(Write(ttl), rt=1.0)

        self.cue(0)
        defn = label("a semiprime is p \u00d7 q --- both prime, possibly equal", 20, ink)
        defn.move_to(UP * 1.2)
        self.play_(Write(defn), rt=1.7)

        self.cue(1)
        self.play_(FadeOut(defn), rt=0.3)
        insight = label("first insight: p can't be bigger than the square root of the limit", 19, gold)
        insight.move_to(UP * 1.2)
        self.play_(Write(insight), rt=1.9)
        why = label("if both factors were bigger, the product would already blow past it", 17, dim)
        why.next_to(insight, DOWN, buff=0.5)
        self.play_(FadeIn(why), rt=1.4)

        self.cue(2)
        self.play_(FadeOut(VGroup(insight, why)), rt=0.4)
        sqrtcalc = label(f"@\\sqrt{{10^8}} \\approx {SMALL_BOUND}", 30, gold)
        sqrtcalc.move_to(UP * 0.8)
        self.play_(Write(sqrtcalc), rt=1.2)
        tiny = label("that's the entire candidate list for p --- tiny", 18, ink)
        tiny.next_to(sqrtcalc, DOWN, buff=0.5)
        self.play_(FadeIn(tiny), rt=1.0)

        self.cue(3)
        self.play_(FadeOut(VGroup(sqrtcalc, tiny)), rt=0.4)
        foreach = label("for each small prime p, count primes q in [p, limit / p]", 19, ink)
        foreach.move_to(UP * 0.8)
        self.play_(Write(foreach), rt=1.6)
        code1 = label("upper = limit / p", 20, dim, font=mono)
        code1.next_to(foreach, DOWN, buff=0.5)
        self.play_(FadeIn(code1), rt=0.9)

        self.cue(4)
        code2 = label("count primes between p and upper", 20, dim, font=mono)
        code2.next_to(code1, DOWN, buff=0.35)
        self.play_(FadeIn(code2), rt=1.1)

        self.cue(5)
        self.play_(FadeOut(VGroup(foreach, code1, code2)), rt=0.4)
        loop = label(f"a loop over roughly {fmtnum(NUM_SMALL_PRIMES)} small primes", 20, ink)
        loop.move_to(UP * 0.8)
        self.play_(Write(loop), rt=1.5)
        engineering = label("the real engineering problem hides in that one lookup", 18, gold)
        engineering.next_to(loop, DOWN, buff=0.5)
        self.play_(FadeIn(engineering), rt=1.3)

        self.cue(6)
        self.play_(FadeOut(VGroup(loop, engineering)), rt=0.4)
        need = label("how many primes exist below a given number --- instantly", 19, ink)
        need.move_to(UP * 0.5)
        self.play_(Write(need), rt=1.7)
        howmany = label(f"and you need that answer about {fmtnum(NUM_SMALL_PRIMES)} times", 18, dim)
        howmany.next_to(need, DOWN, buff=0.5)
        self.play_(FadeIn(howmany), rt=1.2)

        self.cue(7)
        self.play_(FadeOut(VGroup(need, howmany)), rt=0.4)
        contrast = dotcluster(NUM_SMALL_PRIMES, center=LEFT * 3.0 + DOWN * 0.3, side=1.6, r=0.018, color=good)
        smalllab = label(f"{fmtnum(NUM_SMALL_PRIMES)} questions", 17, good)
        smalllab.next_to(contrast, UP, buff=0.35)
        self.play_(LaggedStart(*[FadeIn(d, scale=0.4) for d in contrast], lag_ratio=0.001), rt=1.3)
        self.play_(FadeIn(smalllab), rt=0.6)
        bigbox = Rectangle(width=3.2, height=2.4, color=bad, fill_color=bad, fill_opacity=0.35, stroke_width=1.5)
        bigbox.move_to(RIGHT * 3.0 + DOWN * 0.3)
        biglab = label(f"{fmtnum(Q_BOUND)} possible answers", 17, bad)
        biglab.next_to(bigbox, UP, buff=0.35)
        self.play_(FadeIn(bigbox), rt=0.9)
        self.play_(FadeIn(biglab), rt=0.6)

        self.cue(8)
        vs = label("only ever asking about a tiny fraction of them", 18, gold)
        vs.to_edge(DOWN, buff=0.85)
        self.play_(Write(vs), rt=1.6)

        self.cue(9)
        self.play_(FadeOut(VGroup(contrast, smalllab, bigbox, biglab, vs)), rt=0.5)
        recap = label("two problems: build the list fast, answer the count fast", 19, ink)
        recap.move_to(UP * 0.3)
        self.play_(Write(recap), rt=1.8)

        self.cue(10)
        self.finish(72.300833 + 1.3)


class sec3claude(base):
    times = [0.0, 8.68, 16.42, 20.02, 30.65, 38.81, 43.42, 45.54]
    def construct(self):
        self.start()
        hdr = pill("Claude", claude)
        hdr.to_corner(UL, buff=0.45)
        sub = label("falls behind at the very first step", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        setup = label("falls behind at the very first step", 20, claude)
        setup.move_to(UP * 1.2)
        self.play_(Write(setup), rt=1.5)
        code = label("for j in range(i*i, limit, i): mark j composite", 17, dim, font=mono)
        code.next_to(setup, DOWN, buff=0.5)
        self.play_(FadeIn(code), rt=1.1)

        self.cue(1)
        onestep = label("a normal loop --- one multiple at a time", 19, bad)
        onestep.next_to(code, DOWN, buff=0.5)
        self.play_(Write(onestep), rt=1.3)
        stepdemo = VGroup()
        nums = [6, 12, 18, 24, 30, 36]
        row = VGroup(*[label(str(n), 18, ink) for n in nums])
        row.arrange(RIGHT, buff=0.6).next_to(onestep, DOWN, buff=0.6)
        self.play_(LaggedStart(*[FadeIn(t) for t in row], lag_ratio=0.05), rt=0.7)
        marker = SurroundingRectangle(row[0], buff=0.1).set_stroke(bad, 2.2)
        self.play_(Create(marker), rt=0.25)
        for i in range(1, len(row)):
            newmark = SurroundingRectangle(row[i], buff=0.1).set_stroke(bad, 2.2)
            self.play_(Transform(marker, newmark), rt=0.22)

        self.cue(2)
        self.play_(FadeOut(VGroup(code, onestep, row, marker)), rt=0.4)
        correct = label("same logic, same correct result", 19, good)
        correct.move_to(UP * 1.0)
        self.play_(FadeIn(correct), rt=1.0)
        bytecode = label("actual Python bytecode, once per multiple, every time", 17, dim)
        bytecode.next_to(correct, DOWN, buff=0.5)
        self.play_(FadeIn(bytecode), rt=1.2)

        self.cue(3)
        self.play_(FadeOut(VGroup(correct, bytecode)), rt=0.4)
        counting = label("but for counting, Claude goes with binary search", 20, good)
        counting.move_to(UP * 1.0)
        self.play_(Write(counting), rt=1.6)
        sortedlab = label("sorted list, bisect calls", 18, ink)
        sortedlab.next_to(counting, DOWN, buff=0.5)
        self.play_(FadeIn(sortedlab), rt=0.9)
        steps = label(f"about {BSEARCH_STEPS} comparisons per lookup", 18, dim)
        steps.next_to(sortedlab, DOWN, buff=0.35)
        self.play_(FadeIn(steps), rt=1.0)

        self.cue(4)
        self.play_(FadeOut(VGroup(counting, sortedlab, steps)), rt=0.4)
        recap1 = label("one slow decision at the start", 19, bad)
        recap1.move_to(UP * 0.6)
        self.play_(Write(recap1), rt=1.2)

        self.cue(5)
        recap2 = label("one fast one right after", 19, good)
        recap2.next_to(recap1, DOWN, buff=0.4)
        self.play_(Write(recap2), rt=1.1)
        better = label("better off than paying for both", 18, ink)
        better.next_to(recap2, DOWN, buff=0.45)

        self.cue(6)
        self.play_(FadeIn(better), rt=1.0)

        self.cue(7)
        behind = label("still behind anyone who got that first sieve step right", 18, dim)
        behind.next_to(better, DOWN, buff=0.4)
        self.play_(Write(behind), rt=1.6)
        self.finish(49.088938 + 1.3)


class sec4gpt(base):
    times = [0.0, 3.40, 6.50, 14.03, 18.23]
    def construct(self):
        self.start()
        hdr = pill("GPT-5.6 Sol", gpt)
        hdr.to_corner(UL, buff=0.45)
        sub = label("pays for the slow choice at both steps", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        setup = label("pays for the slow choice at both steps", 20, bad)
        setup.move_to(UP * 1.1)
        self.play_(Write(setup), rt=1.4)

        self.cue(1)
        samesieve = label("same one-multiple-at-a-time loop that Claude uses", 18, ink)
        samesieve.next_to(setup, DOWN, buff=0.5)
        self.play_(FadeIn(samesieve), rt=1.3)

        self.cue(2)
        self.play_(FadeOut(VGroup(setup, samesieve)), rt=0.4)
        prefix = label(f"builds a running total across all {fmtnum(Q_BOUND)} positions", 18, bad)
        prefix.move_to(UP * 0.8)
        self.play_(Write(prefix), rt=1.6)
        onlyneeds = label(f"to answer {fmtnum(NUM_SMALL_PRIMES)} lookups", 18, dim)
        onlyneeds.next_to(prefix, DOWN, buff=0.4)
        self.play_(FadeIn(onlyneeds), rt=1.0)

        self.cue(3)
        self.play_(FadeOut(VGroup(prefix, onlyneeds)), rt=0.4)
        notwrong = label("nothing here is incorrect", 20, ink)
        notwrong.move_to(UP * 0.5)
        self.play_(Write(notwrong), rt=1.2)

        self.cue(4)
        stacked = label("two loops, each bigger than it needed to be, stacked together", 18, bad)
        stacked.next_to(notwrong, DOWN, buff=0.5)
        self.play_(Write(stacked), rt=1.8)
        self.finish(21.995125 + 1.3)


class sec5grok(base):
    times = [0.0, 0.21, 14.61, 26.42, 53.1, 61.29]
    def construct(self):
        self.start()
        hdr = pill("Grok 4.5", grok)
        hdr.to_corner(UL, buff=0.45)
        sub = label("builds the list the fast way first", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(1)
        setup = label("builds the prime list the fast way first", 20, grok)
        setup.move_to(UP * 1.2)
        self.play_(Write(setup), rt=1.4)
        code = label("sieve[i*i::i] = bytearray(...)", 18, dim, font=mono)
        code.next_to(setup, DOWN, buff=0.5)
        self.play_(FadeIn(code), rt=1.0)
        oneline = label("one line --- marks an entire stretch at once", 18, good)
        oneline.next_to(code, DOWN, buff=0.4)
        self.play_(Write(oneline), rt=1.3)
        bulk = label("a bulk memory operation, closer to the hardware", 17, dim)
        bulk.next_to(oneline, DOWN, buff=0.35)
        self.play_(FadeIn(bulk), rt=1.2)

        self.cue(2)
        self.play_(FadeOut(VGroup(setup, code, oneline, bulk)), rt=0.4)
        prefixsetup = label("but to count primes below a number, it builds a prefix array", 19, ink)
        prefixsetup.move_to(UP * 1.1)
        self.play_(Write(prefixsetup), rt=1.8)
        code2 = label("running total += 1 if prime, store it, every position", 17, dim, font=mono)
        code2.next_to(prefixsetup, DOWN, buff=0.5)
        self.play_(FadeIn(code2), rt=1.3)

        self.cue(3)
        works = label("which works --- any lookup after is one array read", 18, good)
        works.next_to(code2, DOWN, buff=0.4)
        self.play_(Write(works), rt=1.5)

        self.cue(4)
        self.play_(FadeOut(VGroup(prefixsetup, code2, works)), rt=0.4)
        strip = Rectangle(width=9.0, height=0.5, color=bad, fill_color=bad, fill_opacity=0.6, stroke_width=1.2)
        strip.move_to(UP * 0.6)
        stripL = label("0", 15, ink).next_to(strip, LEFT, buff=0.25)
        stripR = label(f"{fmtnum(Q_BOUND)}", 15, ink).next_to(strip, RIGHT, buff=0.25)
        self.play_(Create(strip), FadeIn(stripL), FadeIn(stripR), rt=1.1)
        touchlab = label(f"the loop touches every single position --- {fmtnum(Q_BOUND)} of them", 17, bad)
        touchlab.next_to(strip, DOWN, buff=0.4)
        self.play_(FadeIn(touchlab), rt=1.2)

        self.cue(5)
        tiny = Rectangle(width=0.18, height=0.5, color=good, fill_color=good, fill_opacity=0.9, stroke_width=0)
        tiny.move_to(strip.get_left() + RIGHT * 0.09)
        tinylab = label(f"only {fmtnum(NUM_SMALL_PRIMES)} were ever going to be asked about", 16, good)
        tinylab.next_to(touchlab, DOWN, buff=0.35)
        self.play_(FadeIn(tiny), rt=0.7)
        self.play_(FadeIn(tinylab), rt=0.9)
        self.finish(64.193708 + 1.3)


class sec6kimi(base):
    times = [0.0, 5.15, 16.74, 26.56, 33.59, 46.41]
    def construct(self):
        self.start()
        hdr = pill("Kimi K3", kimi)
        hdr.to_corner(UL, buff=0.45)
        sub = label("same fast list, a dramatically cheaper lookup", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        same = label("builds that exact same fast prime list", 20, kimi)
        same.move_to(UP * 1.2)
        self.play_(Write(same), rt=1.3)
        callback = label("same bulk slice assignment as Grok", 17, dim)
        callback.next_to(same, DOWN, buff=0.4)
        self.play_(FadeIn(callback), rt=1.0)

        self.cue(1)
        self.play_(FadeOut(VGroup(same, callback)), rt=0.4)
        keeps = label("keeps the primes as a plain sorted list", 19, ink)
        keeps.move_to(UP * 1.1)
        self.play_(Write(keeps), rt=1.4)
        code = label("bisect_right(primes, n)", 19, good, font=mono)
        code.next_to(keeps, DOWN, buff=0.5)
        self.play_(FadeIn(code), rt=0.9)

        self.cue(2)
        binsearch = label("binary search", 24, good)
        binsearch.next_to(code, DOWN, buff=0.4)
        self.play_(Write(binsearch), rt=1.0)
        primerow = VGroup(*[Dot(radius=0.05, color=faint) for _ in range(21)])
        primerow.arrange(RIGHT, buff=0.28).move_to(DOWN * 0.9)
        self.play_(FadeIn(primerow), rt=0.7)
        marker = Dot(primerow[10].get_center(), radius=0.09, color=gold)
        self.play_(FadeIn(marker), rt=0.4)
        halves = [10, 15, 17, 18]
        for h in halves:
            self.play_(marker.animate.move_to(primerow[h].get_center()), rt=0.3)
        jumplab = label("jumps to the middle, throws away half, every comparison", 17, dim)
        jumplab.next_to(primerow, DOWN, buff=0.45)
        self.play_(FadeIn(jumplab), rt=1.2)

        self.cue(3)
        self.play_(FadeOut(VGroup(keeps, code, binsearch, primerow, marker, jumplab)), rt=0.4)
        scalelab = label(f"for a list of {fmtnum(NUM_BIG_PRIMES)} primes", 20, ink)
        scalelab.move_to(UP * 0.6)
        self.play_(Write(scalelab), rt=1.4)
        stepslab = label(f"that's about {BSEARCH_STEPS} comparisons to land exactly right", 19, good)
        stepslab.next_to(scalelab, DOWN, buff=0.5)
        self.play_(Write(stepslab), rt=1.5)

        self.cue(4)
        self.play_(FadeOut(VGroup(scalelab, stepslab)), rt=0.4)
        shorter = label("the code is shorter too --- no fifty-million-step loop", 18, ink)
        shorter.move_to(UP * 0.4)
        self.play_(Write(shorter), rt=1.4)
        direct = label(f"just answer it directly, {fmtnum(NUM_SMALL_PRIMES)} times, {BSEARCH_STEPS} steps each", 17, dim)
        direct.next_to(shorter, DOWN, buff=0.45)
        self.play_(FadeIn(direct), rt=1.3)

        self.cue(5)
        self.play_(FadeOut(VGroup(shorter, direct)), rt=0.4)
        cheaper = label("dramatically cheaper --- for the twelve hundred questions that matter", 18, gold)
        cheaper.move_to(UP * 0.3)
        self.play_(Write(cheaper), rt=1.8)
        self.finish(51.308354 + 1.3)


class sec7evalverdict(base):
    times = [0.0, 23.43, 26.91, 27.63, 32.13, 35.17, 39.38, 44.89, 47.07, 49.97, 53.45, 57.66]
    def construct(self):
        self.start()
        head = label("Eval & Verdict", 30)
        head.to_edge(UP, buff=0.55)
        self.play_(Write(head), rt=1.0)

        self.cue(0)
        allfour = label(f"all four land on {fmtnum(ANSWER)}", 21, gold)
        allfour.move_to(UP * 1.1)
        self.play_(Write(allfour), rt=1.9)

        names = ["Kimi K3", "Grok 4.5", "Claude", "GPT-5.6 Sol"]
        cols = {"Kimi K3": kimi, "Grok 4.5": grok, "Claude": claude, "GPT-5.6 Sol": gpt}
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

        self.play_(FadeOut(allfour), rt=0.3)
        self.play_(*[FadeIn(r[0]) for r in scs], *[FadeIn(r[1]) for r in scs], rt=1.0)
        kf = pill("Kimi K3", kimi, w=3.1, h=0.9, size=22)
        kf.move_to(focus)
        crown = Polygon([-0.4, 0, 0], [-0.24, 0.32, 0], [0, 0.06, 0], [0.24, 0.32, 0], [0.4, 0, 0]).set_fill(gold, 1).set_stroke(gold, 1).scale(0.85)
        crown.next_to(kf, UP, buff=0.12)
        self.play_(FadeIn(kf, shift=DOWN * 0.2), rt=0.6)
        self.play_(FadeIn(crown, shift=DOWN * 0.3), rt=0.5)
        self.hold(1.0)

        self.cue(1)
        k1 = label("bulk instruction per prime, binary search per lookup", 16, kimi)
        k1.next_to(kf, DOWN, buff=0.45)
        self.play_(Write(k1), rt=1.4)
        note(0, "winner", gold)

        self.cue(2)
        k2 = label("fastest by a wide margin", 16, ink)
        k2.next_to(k1, DOWN, buff=0.22)
        self.play_(Write(k2), rt=1.0)

        self.cue(3)
        self.play_(FadeOut(VGroup(kf, crown, k1, k2)), rt=0.35)
        gf = pill("Grok 4.5", grok, w=3.1, h=0.9, size=22)
        gf.move_to(focus)
        self.play_(FadeIn(gf, shift=DOWN * 0.2), rt=0.5)
        g1 = label("same fast list, but precomputes for numbers", 16, grok)
        g1.next_to(gf, DOWN, buff=0.45)
        g2 = label("it was never going to ask about", 16, grok)
        g2.next_to(g1, DOWN, buff=0.18)
        self.play_(Write(g1), rt=1.1)
        self.play_(Write(g2), rt=0.9)
        note(1, "2nd, dead weight", dim)

        self.cue(4)
        self.play_(FadeOut(VGroup(gf, g1, g2)), rt=0.35)
        cf = pill("Claude", claude, w=3.1, h=0.9, size=22)
        cf.move_to(focus)
        self.play_(FadeIn(cf, shift=DOWN * 0.2), rt=0.5)
        c1 = label("slower sieve loop, but the cheap binary search after", 16, claude)
        c1.next_to(cf, DOWN, buff=0.45)
        self.play_(Write(c1), rt=1.3)
        note(2, "3rd", dim)

        self.cue(5)
        self.play_(FadeOut(VGroup(cf, c1)), rt=0.35)
        gpf = pill("GPT-5.6 Sol", gpt, w=3.1, h=0.9, size=22)
        gpf.move_to(focus)
        self.play_(FadeIn(gpf, shift=DOWN * 0.2), rt=0.5)
        p1 = label("slow sieve, plus the expensive full range count", 16, gpt)
        p1.next_to(gpf, DOWN, buff=0.45)
        self.play_(Write(p1), rt=1.2)
        p2 = label("slowest of the four, paying the bigger cost twice", 16, ink)
        p2.next_to(p1, DOWN, buff=0.22)
        self.play_(Write(p2), rt=1.2)
        note(3, "slowest", bad)

        self.cue(6)
        self.play_(FadeOut(VGroup(gpf, p1, p2)), rt=0.35)
        lesson = label("the winner's Kimi --- don't build an answer for every question", 18, gold)
        lesson.move_to(focus + UP * 0.5)
        self.play_(Write(lesson), rt=1.9)

        self.cue(7)
        lesson2 = label("when you only ever have twelve hundred real ones", 17, ink)
        lesson2.next_to(lesson, DOWN, buff=0.35)
        self.play_(FadeIn(lesson2), rt=1.3)

        self.cue(8)
        self.play_(FadeOut(VGroup(lesson, lesson2)), rt=0.3)
        aside1 = label("Grok: respectable --- one oversized loop going nowhere", 16, grok)
        aside1.move_to(focus + UP * 0.3)
        self.play_(Write(aside1), rt=1.6)

        self.cue(9)
        self.play_(FadeOut(aside1), rt=0.3)
        aside2 = label("Claude: a slower first step still saved real time downstream", 16, claude)
        aside2.move_to(focus + UP * 0.3)
        self.play_(Write(aside2), rt=1.7)

        self.cue(10)
        self.play_(FadeOut(aside2), rt=0.3)
        final = label(fmtnum(ANSWER), 30, gold)
        final.move_to(focus + UP * 0.3)
        fbox = SurroundingRectangle(final, buff=0.2).set_stroke(gold, 2)
        finaltag = label("semiprimes below a hundred million", 15, dim)
        finaltag.next_to(final, DOWN, buff=0.35)
        self.play_(Write(final), rt=0.8)
        self.play_(Create(fbox), rt=0.35)
        self.play_(FadeIn(finaltag), rt=0.6)

        self.cue(11)
        moral = label("twelve hundred questions, asked directly, beats fifty million answers, mostly wasted", 15, dim)
        moral.to_edge(DOWN, buff=0.8)
        self.play_(Write(moral), rt=1.5)
        self.finish(59.543313 + 1.3)
