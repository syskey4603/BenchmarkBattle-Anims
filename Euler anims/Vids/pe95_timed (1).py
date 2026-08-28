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

def bulgearc(p1, p2, height, color, sw=2.5):
    mid = (p1 + p2) / 2
    down = np.array([0, -1, 0]) * height
    c1 = p1 + (mid - p1) * 0.5 + down
    c2 = p2 + (mid - p2) * 0.5 + down
    return CubicBezier(p1, c1, c2, p2, color=color, stroke_width=sw)

chain = [14316, 19116, 31704, 47616, 83328, 177792, 295488, 629072, 589786, 294896,
         358336, 418904, 366556, 274924, 275444, 243760, 376736, 381028, 285778, 152990,
         122410, 97946, 48976, 45946, 22976, 22744, 19916, 17716]
answer_start = 14316
answer_len = 28

def loopnodes(n, center=ORIGIN, radius=2.6):
    pts = []
    for i in range(n):
        ang = PI / 2 - 2 * PI * i / n
        pts.append(center + radius * np.array([np.cos(ang), np.sin(ang), 0]))
    return pts

def divisors(n):
    ds = []
    for i in range(1, n):
        if n % i == 0:
            ds.append(i)
    return ds


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
    times = [0.0, 1.7, 6.97, 8.75, 15.32, 18.69, 22.31, 24.49, 31.68]
    def construct(self):
        self.start()
        self.cue(0)
        a = Circle(radius=0.42, color=fable, fill_color=panel, fill_opacity=1).move_to(LEFT * 1.6 + UP * 0.6)
        b = Circle(radius=0.42, color=gpt, fill_color=panel, fill_opacity=1).move_to(RIGHT * 1.6 + UP * 0.6)
        al = label("A", 26, fable).move_to(a)
        bl = label("B", 26, gpt).move_to(b)
        tag = label("amicable pairs --- you've probably heard of these", 19, dim)
        tag.to_edge(UP, buff=0.6)
        self.play_(FadeIn(tag), rt=0.9)
        self.play_(FadeIn(VGroup(a, al)), rt=0.5)
        self.play_(FadeIn(VGroup(b, bl)), rt=0.5)

        self.cue(1)
        arc1 = bulgearc(a.get_top(), b.get_top(), 0.55, dim)
        arc2 = bulgearc(b.get_bottom(), a.get_bottom(), 0.55, dim)
        self.play_(Create(arc1), rt=0.6)
        self.play_(Create(arc2), rt=0.6)
        rule = label("each one's divisors add up to the other", 17, ink)
        rule.to_edge(DOWN, buff=0.85)
        self.play_(FadeIn(rule), rt=0.8)

        self.cue(2)
        self.play_(FadeOut(VGroup(tag, rule)), rt=0.4)
        chaintag = label("turns out that idea can chain", 21, ink)
        chaintag.to_edge(UP, buff=0.6)
        self.play_(Write(chaintag), rt=1.3)

        self.cue(3)
        pts = loopnodes(6, center=DOWN * 0.4, radius=2.1)
        nodes = VGroup(*[Dot(p, radius=0.11, color=dim) for p in pts])
        letters = ["A", "B", "C", "D", "E", "F"]
        lbls = VGroup(*[label(letters[i], 16, dim).next_to(pts[i], pts[i] - (DOWN * 0.4), buff=0.18) for i in range(6)])
        arrows = VGroup()
        for i in range(6):
            arrows.add(bulgearc(pts[i], pts[(i + 1) % 6], 0.0, gold, sw=2.0))
        self.play_(FadeOut(VGroup(a, al, b, bl, arc1, arc2)), rt=0.4)
        self.play_(LaggedStart(*[FadeIn(n, scale=0.6) for n in nodes], lag_ratio=0.12), rt=1.0)
        self.play_(LaggedStart(*[FadeIn(l) for l in lbls], lag_ratio=0.1), rt=0.6)
        self.play_(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.12), rt=1.4)
        loopclosed = label("eventually, sometimes, it loops all the way back", 17, gold)
        loopclosed.to_edge(DOWN, buff=0.85)
        self.play_(FadeIn(loopclosed), rt=0.9)

        self.cue(4)
        self.play_(FadeOut(VGroup(chaintag, nodes, lbls, arrows, loopclosed)), rt=0.5)
        q = label("longest one of those loops --- under a million", 22, ink)
        q.move_to(UP * 0.3)
        self.play_(Write(q), rt=1.9)

        self.cue(5)
        self.play_(FadeOut(q), rt=0.3)
        names = ["Kimi K3", "Fable", "GPT-5.6 Sol", "Grok 4.5"]
        cols = [kimi, fable, gpt, grok]
        chips = VGroup(*[pill(n, c, w=2.55, h=0.72, size=18) for n, c in zip(names, cols)])
        chips.arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        self.play_(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips], lag_ratio=0.15), rt=1.3)

        self.cue(6)
        nohint = label("no hints", 18, dim)
        nohint.next_to(chips, DOWN, buff=0.5)
        self.play_(FadeIn(nohint), rt=0.7)

        self.cue(7)
        self.play_(FadeOut(nohint), rt=0.3)
        twist = label("everyone gets it right --- but two things stack this time", 18, gold)
        twist.next_to(chips, DOWN, buff=0.5)
        self.play_(Write(twist), rt=1.9)

        self.cue(8)
        self.finish(31.681688 + 1.3)


class sec2problem(base):
    times = [0.0, 2.06, 4.27, 7.92, 11.35, 15.27, 16.48, 18.43, 24.65, 25.81, 31.25, 33.18, 38.7]
    def construct(self):
        self.start()
        ttl = label("Amicable Chains", 30)
        ttl.to_edge(UP, buff=0.55)
        self.play_(Write(ttl), rt=1.0)

        self.cue(0)
        n = 28
        ds = divisors(n)
        nlab = label(f"proper divisors of {n}", 20, ink)
        nlab.move_to(UP * 1.3)
        dlab = label(", ".join(str(d) for d in ds), 24, dim)
        dlab.next_to(nlab, DOWN, buff=0.5)
        self.play_(Write(nlab), rt=1.1)
        self.play_(FadeIn(dlab), rt=0.9)

        self.cue(1)
        s = sum(ds)
        arrow1 = label(f"add them up --- {s}", 22, good)
        arrow1.next_to(dlab, DOWN, buff=0.5)
        self.play_(Write(arrow1), rt=1.1)

        self.cue(2)
        again = label("do it again to that one. again.", 18, ink)
        again.next_to(arrow1, DOWN, buff=0.45)
        self.play_(FadeIn(again), rt=0.9)

        self.cue(3)
        self.play_(FadeOut(VGroup(nlab, dlab, arrow1, again)), rt=0.4)
        outcome1 = label("sometimes you crash down to 1", 19, bad)
        outcome1.move_to(UP * 0.6)
        self.play_(FadeIn(outcome1), rt=0.8)

        self.cue(4)
        outcome2 = label("sometimes you shoot past a million", 19, bad)
        outcome2.next_to(outcome1, DOWN, buff=0.4)
        self.play_(FadeIn(outcome2), rt=0.9)

        self.cue(5)
        outcome3 = label("but sometimes, it loops back to where it started", 19, good)
        outcome3.next_to(outcome2, DOWN, buff=0.4)
        self.play_(Write(outcome3), rt=1.5)

        self.cue(6)
        chaindef = label("that's an amicable chain --- length can be way more than 2", 18, gold)
        chaindef.next_to(outcome3, DOWN, buff=0.45)
        self.play_(Write(chaindef), rt=1.6)

        self.cue(7)
        self.play_(FadeOut(VGroup(outcome1, outcome2, outcome3, chaindef)), rt=0.4)
        scale = label("do this for every starting number up to a million", 21, ink)
        scale.move_to(UP * 0.5)
        self.play_(Write(scale), rt=1.7)

        self.cue(8)
        needlab = label("you need the proper-divisor sum for basically every number", 18, dim)
        needlab.next_to(scale, DOWN, buff=0.5)
        self.play_(FadeIn(needlab), rt=1.1)

        self.cue(9)
        slowlab = label("trial dividing from scratch --- genuinely too slow here", 18, bad)
        slowlab.next_to(needlab, DOWN, buff=0.4)
        self.play_(Write(slowlab), rt=1.5)

        self.cue(10)
        self.play_(FadeOut(VGroup(scale, needlab, slowlab)), rt=0.4)
        twodec = label("two real decisions matter", 22, ink)
        twodec.move_to(UP * 0.5)
        self.play_(Write(twodec), rt=1.4)

        self.cue(11)
        d1 = label("how do you build that lookup table fast", 19, dim)
        d1.next_to(twodec, DOWN, buff=0.5)
        d2 = label("how do you check if you've already seen a number", 19, dim)
        d2.next_to(d1, DOWN, buff=0.3)
        self.play_(FadeIn(d1), rt=1.0)
        self.play_(FadeIn(d2), rt=1.0)

        self.cue(12)
        self.finish(38.699583 + 1.3)


class sec3gpt(base):
    times = [0.0, 2.75, 5.35, 6.62, 11.25, 15.43]
    def construct(self):
        self.start()
        hdr = pill("GPT-5.6 Sol", gpt)
        hdr.to_corner(UL, buff=0.45)
        sub = label("builds the table the direct way", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        concept = label("for every number, add it to all its multiples", 20, ink)
        concept.move_to(UP * 1.3)
        self.play_(Write(concept), rt=1.6)

        self.cue(1)
        six = label("6", 34, gpt).move_to(LEFT * 4.2 + DOWN * 0.3)
        targets = [12, 18, 24, 30, 36]
        tpos = [RIGHT * (-1.6 + 1.5 * i) + DOWN * 0.3 for i in range(len(targets))]
        tlabs = VGroup(*[label(str(v), 22, ink).move_to(tpos[i]) for i, v in enumerate(targets)])
        self.play_(FadeIn(six), rt=0.6)
        self.play_(LaggedStart(*[FadeIn(t) for t in tlabs], lag_ratio=0.15), rt=1.0)
        arrows = VGroup(*[Arrow(six.get_right(), tlabs[i].get_left(), buff=0.15, color=gpt, stroke_width=2.2, max_tip_length_to_length_ratio=0.12) for i in range(len(targets))])

        self.cue(2)
        self.play_(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), rt=1.3)
        sweeplab = label("every multiple, one at a time", 16, dim)
        sweeplab.to_edge(DOWN, buff=0.85)
        self.play_(FadeIn(sweeplab), rt=0.8)

        self.cue(3)
        self.play_(FadeOut(VGroup(concept, six, tlabs, arrows, sweeplab)), rt=0.4)
        scale = label("do that for every number up to a million", 20, ink)
        scale.move_to(UP * 0.4)
        self.play_(Write(scale), rt=1.6)

        self.cue(4)
        ok = label("correct --- a completely reasonable way to build it", 18, good)
        ok.next_to(scale, DOWN, buff=0.5)
        self.play_(FadeIn(ok), rt=1.1)

        self.cue(5)
        slow = label("just not the fastest --- touching a huge number of entries", 18, bad)
        slow.next_to(ok, DOWN, buff=0.4)
        self.play_(Write(slow), rt=1.7)
        self.finish(20.096458 + 1.3)


class sec4fable(base):
    times = [0.0, 4.71, 16.12, 22.33, 25.54]
    def construct(self):
        self.start()
        hdr = pill("Fable", fable)
        hdr.to_corner(UL, buff=0.45)
        sub = label("same table, through prime factorization", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        n = label("28", 34, fable).move_to(UP * 1.3)
        factor = label("2 \u00d7 2 \u00d7 7", 26, ink)
        factor.next_to(n, DOWN, buff=0.4)
        self.play_(Write(n), rt=0.8)
        self.play_(FadeIn(factor), rt=1.0)
        tag = label("break it into prime factors first", 18, dim)
        tag.next_to(factor, DOWN, buff=0.4)
        self.play_(FadeIn(tag), rt=0.9)

        self.cue(1)
        self.play_(FadeOut(VGroup(n, factor, tag)), rt=0.4)
        formula = label("@\\sigma(n) = \\prod \\dfrac{p^{a+1}-1}{p-1}", 30, fable)
        formula.move_to(UP * 0.6)
        self.play_(Write(formula), rt=1.8)
        flabel = label("hands you the full divisor sum directly", 18, ink)
        flabel.next_to(formula, DOWN, buff=0.5)
        self.play_(FadeIn(flabel), rt=1.0)

        self.cue(2)
        self.play_(FadeOut(VGroup(formula, flabel)), rt=0.4)
        contrast = label("fixed work per number --- not touching millions of entries", 19, good)
        contrast.move_to(UP * 0.3)
        self.play_(Write(contrast), rt=1.9)

        self.cue(3)
        same = label("same table, same numbers", 19, ink)
        same.next_to(contrast, DOWN, buff=0.5)
        self.play_(FadeIn(same), rt=1.1)

        self.cue(4)
        half = label("built in about half the time", 22, gold)
        half.next_to(same, DOWN, buff=0.4)
        self.play_(Write(half), rt=1.4)
        self.finish(25.536667 + 1.3)


class sec5grok(base):
    times = [0.0, 2.81, 9.24, 10.74, 17.66]
    def construct(self):
        self.start()
        hdr = pill("Grok 4.5", grok)
        hdr.to_corner(UL, buff=0.45)
        sub = label("carrying both costs at once", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        c1 = label("slower table --- the direct add-to-every-multiple method", 18, grok)
        c1.move_to(UP * 1.0)
        self.play_(Write(c1), rt=1.6)

        self.cue(1)
        c2 = label("plus the list-based check while walking each chain", 18, grok)
        c2.next_to(c1, DOWN, buff=0.45)
        self.play_(Write(c2), rt=1.6)
        box1 = SurroundingRectangle(c1, buff=0.15).set_stroke(bad, 1.5)
        box2 = SurroundingRectangle(c2, buff=0.15).set_stroke(bad, 1.5)
        self.play_(Create(box1), Create(box2), rt=0.8)

        self.cue(2)
        neither = label("neither one alone is a huge deal", 17, dim)
        neither.next_to(c2, DOWN, buff=0.55)
        self.play_(FadeIn(neither), rt=1.0)

        self.cue(3)
        self.play_(FadeOut(neither), rt=0.3)
        stack = label("stack them together --- biggest gap of the four", 20, bad)
        stack.next_to(c2, DOWN, buff=0.55)
        self.play_(Write(stack), rt=1.6)

        self.cue(4)
        close = label("correct the whole way --- just paying both costs instead of one", 17, ink)
        close.next_to(stack, DOWN, buff=0.5)
        self.play_(Write(close), rt=1.9)
        self.finish(17.664479 + 1.3)


class sec6kimi(base):
    times = [0.0, 5.01, 11.71, 12.71, 14.31, 16.81, 18.82, 22.72]
    def construct(self):
        self.start()
        hdr = pill("Kimi K3", kimi)
        hdr.to_corner(UL, buff=0.45)
        sub = label("same fast table, slower walk", 18, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        same = label("uses that same fast, prime-factorization table Fable does", 19, ink)
        same.move_to(UP * 1.2)
        self.play_(Write(same), rt=1.8)

        self.cue(1)
        self.play_(FadeOut(same), rt=0.3)
        differ = label("differs in the chain-walking part", 20, kimi)
        differ.move_to(UP * 1.2)
        self.play_(Write(differ), rt=1.4)
        boxes = VGroup(*[RoundedRectangle(corner_radius=0.08, width=1.0, height=0.6).set_stroke(kimi, 1.6).set_fill(panel, 1) for _ in range(5)])
        boxes.arrange(RIGHT, buff=0.2).move_to(DOWN * 0.6)
        vals = [83328, 177792, 295488, 629072, 589786]
        vlabs = VGroup(*[label(str(v), 12, ink).move_to(boxes[i]) for i, v in enumerate(vals)])
        self.play_(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.1), rt=0.9)
        self.play_(LaggedStart(*[FadeIn(v) for v in vlabs], lag_ratio=0.1), rt=0.7)

        self.cue(2)
        scanbox = SurroundingRectangle(boxes[0], buff=0.08).set_stroke(gold, 2.5)
        checklab = label("is it here?", 15, gold).next_to(boxes, UP, buff=0.35)
        self.play_(FadeIn(checklab), rt=0.6)
        self.play_(Create(scanbox), rt=0.3)
        for i in range(1, 5):
            newbox = SurroundingRectangle(boxes[i], buff=0.08).set_stroke(gold, 2.5)
            self.play_(Transform(scanbox, newbox), rt=0.25)

        self.cue(3)
        self.play_(FadeOut(VGroup(differ, boxes, vlabs, scanbox, checklab)), rt=0.4)
        fine = label("works fine --- chains here aren't long", 19, good)
        fine.move_to(UP * 0.6)
        self.play_(FadeIn(fine), rt=1.0)

        self.cue(4)
        slower = label("a list scan gets slightly slower the longer that list gets", 17, dim)
        slower.next_to(fine, DOWN, buff=0.5)
        self.play_(FadeIn(slower), rt=1.2)

        self.cue(5)
        self.play_(FadeOut(VGroup(fine, slower)), rt=0.4)
        summary = label("fast table, slightly slower walk", 21, kimi)
        summary.move_to(UP * 0.3)
        self.play_(Write(summary), rt=1.5)

        self.cue(6)
        behind = label("still lands right behind Fable", 19, ink)
        behind.next_to(summary, DOWN, buff=0.45)
        self.play_(FadeIn(behind), rt=1.1)

        self.cue(7)
        self.finish(22.720583 + 1.3)


class sec7eval(base):
    times = [0.0, 5.88, 9.72, 14.15, 17.98, 21.18, 23.79]
    def construct(self):
        self.start()
        self.cue(0)
        ttl = label("Side by Side", 30)
        ttl.to_edge(UP, buff=0.55)
        self.play_(Write(ttl), rt=1.0)
        sub = label(f"four correct answers --- all landing on {fmtnum(answer_start)}, chain length {answer_len}", 16, dim)
        sub.next_to(ttl, DOWN, buff=0.3)
        self.play_(FadeIn(sub), rt=1.0)

        rows = [
            ("Fable", fable, "fast table, quick lookup", "fastest overall", good),
            ("Kimi K3", kimi, "fast table, slower lookup", "close behind", good),
            ("GPT-5.6 Sol", gpt, "slower table, quick lookup", "middle of the pack", dim),
            ("Grok 4.5", grok, "slower table, slower lookup", "slowest of the four", bad),
        ]
        cards = VGroup()
        for nm, col, meth, res, rc in rows:
            box = RoundedRectangle(corner_radius=0.1, width=10.8, height=0.92).set_fill(panel, 1).set_stroke(col, 1.6)
            nmlab = label(nm, 19, col).move_to(box.get_left() + RIGHT * 1.6)
            mlab = label(meth, 15, ink).move_to(box.get_center() + LEFT * 0.2)
            rlab = label(res, 15, rc).move_to(box.get_right() + LEFT * 2.0)
            cards.add(VGroup(box, nmlab, mlab, rlab))
        cards.arrange(DOWN, buff=0.26).move_to(DOWN * 0.35)

        self.cue(1)
        self.play_(FadeIn(cards[0], shift=RIGHT * 0.25), rt=0.85)

        self.cue(2)
        self.play_(FadeIn(cards[1], shift=RIGHT * 0.25), rt=0.85)

        self.cue(3)
        self.play_(FadeIn(cards[2], shift=RIGHT * 0.25), rt=0.85)

        self.cue(4)
        self.play_(FadeIn(cards[3], shift=RIGHT * 0.25), rt=0.85)

        self.cue(5)
        self.hold(0.2)

        self.cue(6)
        self.finish(23.78725 + 1.3)


class sec8verdict(base):
    times = [0.0, 9.69, 11.55, 14.88, 17.86, 20.92, 22.52, 24.06, 26.54, 30.3, 35.69, 39.07, 44.44]
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
            nt.move_to(scs[i][0].get_right() + LEFT * 1.6)
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
        f1 = label("two decisions working together", 16, fable)
        f1.next_to(ff, DOWN, buff=0.45)
        self.play_(Write(f1), rt=1.2)
        note(1, "winner", gold)

        self.cue(2)
        f2 = label("prime-factorization table, efficient membership check", 15, ink)
        f2.next_to(f1, DOWN, buff=0.22)
        self.play_(Write(f2), rt=1.3)

        self.cue(3)
        self.play_(FadeOut(VGroup(ff, crown, f1, f2)), rt=0.4)
        kf = pill("Kimi K3", kimi, w=3.1, h=0.9, size=23)
        kf.move_to(focus)
        self.play_(FadeIn(kf, shift=DOWN * 0.2), rt=0.6)

        self.cue(4)
        k1 = label("same smart table, slightly slower walk", 16, kimi)
        k1.next_to(kf, DOWN, buff=0.45)
        self.play_(Write(k1), rt=1.3)
        note(3, "2nd, close", kimi)

        self.cue(5)
        self.play_(FadeOut(VGroup(kf, k1)), rt=0.4)
        gf = pill("GPT-5.6 Sol", gpt, w=3.1, h=0.9, size=23)
        gf.move_to(focus)
        self.play_(FadeIn(gf, shift=DOWN * 0.2), rt=0.6)

        self.cue(6)
        g1 = label("direct table-building isn't wrong, just not quickest", 16, gpt)
        g1.next_to(gf, DOWN, buff=0.45)
        self.play_(Write(g1), rt=1.3)
        note(0, "solid, correct", dim)

        self.cue(7)
        self.hold(0.2)

        self.cue(8)
        self.play_(FadeOut(VGroup(gf, g1)), rt=0.4)
        rf = pill("Grok 4.5", grok, w=3.1, h=0.9, size=23)
        rf.move_to(focus)
        self.play_(FadeIn(rf, shift=DOWN * 0.2), rt=0.6)

        self.cue(9)
        r1 = label("the only one paying both costs at once", 16, grok)
        r1.next_to(rf, DOWN, buff=0.45)
        self.play_(Write(r1), rt=1.3)
        note(2, "correct, slowest", bad)

        self.cue(10)
        self.play_(FadeOut(VGroup(rf, r1)), rt=0.4)
        pts = loopnodes(answer_len, center=LEFT * 2.6 + DOWN * 0.1, radius=1.85)
        loopdots = VGroup(*[Dot(p, radius=0.065, color=gold) for p in pts])
        loopedges = VGroup(*[bulgearc(pts[i], pts[(i + 1) % answer_len], 0.0, dim, sw=1.6) for i in range(answer_len)])
        startlab = label(fmtnum(answer_start), 16, gold).next_to(pts[0], UP, buff=0.18)
        self.play_(LaggedStart(*[FadeIn(d, scale=0.5) for d in loopdots], lag_ratio=0.03), rt=1.1)
        self.play_(LaggedStart(*[Create(e) for e in loopedges], lag_ratio=0.03), rt=1.6)
        self.play_(FadeIn(startlab), rt=0.5)

        self.cue(11)
        lenlab = label(f"{answer_len} numbers long", 26, gold)
        lenlab.next_to(loopdots, RIGHT, buff=0.8).shift(UP * 0.6)
        backlab = label("looping right back to where it started", 17, ink)
        backlab.next_to(lenlab, DOWN, buff=0.35)
        self.play_(Write(lenlab), rt=1.1)
        self.play_(FadeIn(backlab), rt=0.9)

        self.cue(12)
        moral = label("the gap wasn't one big idea --- it was two smaller ones, stacked", 16, dim)
        moral.to_edge(DOWN, buff=0.8)
        self.play_(Write(moral), rt=2.0)
        self.finish(44.438313 + 1.3)
