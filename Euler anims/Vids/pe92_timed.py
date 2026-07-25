from manim import *
import numpy as np
import re

config.background_color = "#0A0A15"

mono = "Consolas"
grok = "#FF4500"
gpt = "#10A37F"
gem = "#4285F4"
cld = "#E8925C"
gold = "#FFD700"
bad = "#FF5555"
good = "#4ADE80"
ink = "#F2F3F7"
dim = "#FFB86C"
panel = "#10141F"
gridcol = "#2A3450"

def fixtext(s):
    s = s.replace("\\$", "\x00m\x00")
    s = s.replace("\\", " ")
    s = s.replace("%", r"\%").replace("&", r"\&").replace("#", r"\#")
    s = s.replace("_", r"\_")
    s = re.sub(r'"([^"]*)"', r"``\1''", s)
    for a, b in [("→", r"$\rightarrow$"), ("✓", r"$\checkmark$"), ("✗", r"$\times$"),
                 ("×", r"$\times$"), ("≈", r"$\approx$"), ("—", "---"),
                 ("²", r"$^2$"), ("·", r"$\cdot$")]:
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

def pill(name, color, w=2.4, h=0.74, size=23):
    box = RoundedRectangle(corner_radius=0.12, width=w, height=h).set_fill(panel, 1).set_stroke(color, 2)
    return VGroup(box, label(name, size, color).move_to(box))

def digitbox(ch, size=0.62, color=ink, edge=gridcol):
    sq = RoundedRectangle(corner_radius=0.1, width=size, height=size).set_fill(panel, 1).set_stroke(edge, 1.6)
    return VGroup(sq, label(ch, 26, color, font=mono).move_to(sq))

def numrow(s, size=0.62, color=ink, gap=0.1):
    row = VGroup(*[digitbox(ch, size, color) for ch in s])
    row.arrange(RIGHT, buff=gap)
    return row

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
    times = [0.52,1.25,2.92,6.58,9.8,10.86,16.18,22.81,26.95,31.86,34.06]
    def construct(self):
        self.start()
        self.cue(0)
        pick = label("pick any number", 26, ink)
        pick.move_to(UP*1.7)
        self.play_(Write(pick), rt=1.1)

        self.cue(1)
        sq = label("square each digit, add them up", 22, dim)
        sq.next_to(pick, DOWN, buff=0.5)
        self.play_(FadeIn(sq), rt=0.9)

        self.cue(2)
        again = label("do it again. and again.", 22, dim)
        again.next_to(sq, DOWN, buff=0.35)
        self.play_(Write(again), rt=1.0)

        self.cue(3)
        self.play_(FadeOut(pick), FadeOut(sq), FadeOut(again), rt=0.5)
        chain = numrow("44", color=cld)
        chain.move_to(UP*0.8)
        self.play_(FadeIn(chain, shift=UP*0.15), rt=0.7)

        self.cue(4)
        arrow1 = label("$\\rightarrow$ 32", 30, dim)
        arrow1.next_to(chain, RIGHT, buff=0.4)
        self.play_(Write(arrow1), rt=0.8)

        self.cue(5)
        arrow2 = label("$\\rightarrow$ 13 $\\rightarrow$ 10 $\\rightarrow$ 1", 26, dim)
        arrow2.next_to(arrow1, RIGHT, buff=0.3)
        self.play_(Write(arrow2), rt=1.2)

        self.cue(6)
        trap = label("every number gets trapped at one of two places", 20, ink)
        trap.next_to(chain, DOWN, buff=0.9)
        self.play_(Write(trap), rt=1.6)

        self.cue(7)
        self.play_(FadeOut(VGroup(chain, arrow1, arrow2, trap)), rt=0.5)
        twonums = VGroup(label("1", 60, good), label("89", 60, gold)).arrange(RIGHT, buff=1.4)
        twonums.move_to(UP*0.5)
        self.play_(FadeIn(twonums, shift=UP*0.2), rt=1.0)

        self.cue(8)
        chips = VGroup(pill("ChatGPT", gpt), pill("Gemini", gem),
                        pill("Grok", grok), pill("Claude", cld)).arrange(RIGHT, buff=0.3)
        chips.next_to(twonums, DOWN, buff=0.8)
        self.play_(FadeIn(chips, shift=UP*0.2), rt=1.0)

        self.cue(9)
        allcorrect = label("all four got the right answer this time", 20, good)
        allcorrect.next_to(chips, DOWN, buff=0.6)
        self.play_(Write(allcorrect), rt=1.4)

        self.cue(10)
        howthey = label("but how they got there tells a very different story", 20, dim)
        howthey.next_to(allcorrect, DOWN, buff=0.35)
        self.play_(Write(howthey), rt=1.6)
        self.finish(39.15+1.3)


class sec2problem(base):
    times = [0.52,1.96,4.2,5.6,6.95,8.75,10.02,11.1,13.69,22.37,32.17,35.16,39.14,44.55,46.96,47.89,52.97]
    def construct(self):
        self.start()
        self.cue(0)
        title = label("Problem 92 --- Square Digit Chains", 30)
        title.to_edge(UP, buff=0.5)
        self.play_(Write(title), rt=1.0)

        self.cue(1)
        n44 = numrow("44", color=cld)
        n44.move_to(UP*1.4+LEFT*4.5)
        self.play_(FadeIn(n44, shift=UP*0.15), rt=0.7)

        self.cue(2)
        eq1 = label("@4^2 + 4^2 = 32", 26, dim)
        eq1.next_to(n44, RIGHT, buff=0.5)
        self.play_(Write(eq1), rt=1.1)

        self.cue(3)
        n32 = numrow("32", color=cld)
        n32.next_to(eq1, RIGHT, buff=0.6)
        self.play_(FadeIn(n32, shift=RIGHT*0.15), rt=0.6)

        self.cue(4)
        eq2 = label("@3^2 + 2^2 = 13", 22, dim)
        eq2.next_to(n44, DOWN, buff=0.55).align_to(n44, LEFT)
        self.play_(Write(eq2), rt=0.9)

        self.cue(5)
        eq3 = label("@1^2 + 3^2 = 10", 22, dim)
        eq3.next_to(eq2, DOWN, buff=0.3).align_to(eq2, LEFT)
        self.play_(Write(eq3), rt=0.9)

        self.cue(6)
        eq4 = label("@1^2 + 0^2 = 1", 22, good)
        eq4.next_to(eq3, DOWN, buff=0.3).align_to(eq3, LEFT)
        self.play_(Write(eq4), rt=0.9)

        self.cue(7)
        stuck = label("hit 1, and you stay there forever", 18, good)
        stuck.next_to(eq4, DOWN, buff=0.35)
        self.play_(FadeIn(stuck), rt=0.9)

        self.cue(8)
        self.play_(FadeOut(VGroup(n44, eq1, n32, eq2, eq3, eq4, stuck)), rt=0.5)
        n85 = numrow("85", color=gold)
        n85.move_to(UP*1.2)
        self.play_(FadeIn(n85, shift=UP*0.15), rt=0.7)

        self.cue(9)
        p1 = label("@8^2 + 5^2 = 89", 26, gold)
        p1.next_to(n85, DOWN, buff=0.5)
        self.play_(Write(p1), rt=1.1)

        self.cue(10)
        p2 = label("@8^2 + 9^2 = 145 \\rightarrow 42 \\rightarrow \\dots \\rightarrow 89", 22, gold)
        p2.next_to(p1, DOWN, buff=0.4)
        self.play_(Write(p2), rt=1.6)

        self.cue(11)
        loops = label("it loops forever, always passing through 89", 19, dim)
        loops.next_to(p2, DOWN, buff=0.4)
        self.play_(FadeIn(loops), rt=1.2)

        self.cue(12)
        self.play_(FadeOut(VGroup(n85, p1, p2, loops)), rt=0.5)
        nothird = label("there is no third destination", 24, ink)
        nothird.move_to(UP*0.6)
        self.play_(Write(nothird), rt=1.3)

        self.cue(13)
        proven = label("mathematicians have actually proven it", 19, dim)
        proven.next_to(nothird, DOWN, buff=0.4)
        self.play_(FadeIn(proven), rt=1.2)

        self.cue(14)
        self.play_(FadeOut(VGroup(nothird, proven)), rt=0.4)
        question = label("out of every number below ten million", 22, ink)
        question.move_to(UP*0.6)
        self.play_(Write(question), rt=1.3)

        self.cue(15)
        question2 = label("how many end up at 89 instead of 1?", 22, gold)
        question2.next_to(question, DOWN, buff=0.4)
        self.play_(Write(question2), rt=1.3)

        self.cue(16)
        lopsided = label("the answer is more lopsided than you'd guess", 18, dim)
        lopsided.next_to(question2, DOWN, buff=0.4)
        self.play_(Write(lopsided), rt=1.4)
        self.finish(55.66+1.3)


class sec3grok(base):
    times = [0.58,6.62,11.2,16.48,17.57,22.07,27.89,29.59,36.83,39.91,45.56,46.6,49.09,55.0]
    def construct(self):
        self.start()
        hdr = pill("Grok", grok)
        hdr.to_corner(UL, buff=0.45)
        sub = label("correct, but carrying extra weight", 20, dim)
        sub.next_to(hdr, RIGHT, buff=0.45)
        self.play_(FadeIn(hdr, shift=DOWN*0.2), Write(sub), rt=1.0)

        self.cue(0)
        loop = label("for every number up to ten million", 20, ink)
        loop.move_to(UP*1.6)
        self.play_(Write(loop), rt=1.2)

        self.cue(1)
        step = label("Grok runs the chain step by step", 20, grok)
        step.next_to(loop, DOWN, buff=0.45)
        self.play_(FadeIn(step), rt=1.1)

        self.cue(2)
        self.play_(FadeOut(loop), FadeOut(step), rt=0.4)
        bag = RoundedRectangle(corner_radius=0.15, width=3.2, height=2.0).set_stroke(grok, 1.6).set_fill(panel, 1)
        bag.move_to(UP*0.4)
        baglabel = label("visited set", 17, dim)
        baglabel.next_to(bag, UP, buff=0.25)
        self.play_(FadeIn(bag), FadeIn(baglabel), rt=0.9)

        nums = ["44","32","13","10"]
        dots = VGroup(*[label(n, 18, ink, font=mono) for n in nums])
        dots.arrange(DOWN, buff=0.2).move_to(bag)

        self.cue(3)
        self.play_(FadeIn(dots[0]), rt=0.4)
        self.cue(4)
        self.play_(FadeIn(dots[1]), rt=0.4)
        self.cue(5)
        self.play_(FadeIn(dots[2]), rt=0.4)
        self.play_(FadeIn(dots[3]), rt=0.4)

        self.cue(6)
        neverused = label("that set is never actually used for anything", 19, bad)
        neverused.next_to(bag, DOWN, buff=0.5)
        self.play_(Write(neverused), rt=1.4)

        self.cue(7)
        notcache = label("not for caching, not for detecting cycles", 18, dim)
        notcache.next_to(neverused, DOWN, buff=0.3)
        self.play_(FadeIn(notcache), rt=1.2)

        self.cue(8)
        self.play_(FadeOut(VGroup(bag, baglabel, dots, neverused, notcache)), rt=0.5)
        tenmill = label("ten million times over", 20, grok)
        tenmill.move_to(UP*0.4)
        self.play_(Write(tenmill), rt=1.1)

        self.cue(9)
        overhead = label("that bookkeeping adds real overhead", 20, bad)
        overhead.next_to(tenmill, DOWN, buff=0.4)
        self.play_(Write(overhead), rt=1.2)

        self.cue(10)
        looks = label("it looks careful and safe", 19, dim)
        looks.next_to(overhead, DOWN, buff=0.35)
        self.play_(FadeIn(looks), rt=1.0)

        self.cue(11)
        weight = label("but it's just weight the program didn't need", 19, dim)
        weight.next_to(looks, DOWN, buff=0.3)
        self.play_(Write(weight), rt=1.3)

        self.cue(12)
        self.play_(FadeOut(VGroup(tenmill, overhead, looks, weight)), rt=0.4)
        result = label("correct answer, slowest of the four", 24, bad)
        result.move_to(UP*0.2)
        self.play_(Write(result), rt=1.3)

        self.cue(13)
        thorough = label("thorough and efficient aren't the same thing", 18, dim)
        thorough.next_to(result, DOWN, buff=0.4)
        self.play_(FadeIn(thorough), rt=1.3)
        self.finish(55.0+1.3)


class sec4gpt(base):
    times = [0.56,1.62,3.74,9.45,10.83,14.28,22.18,25.9,31.33,34.94,37.74,39.42,43.37,45.9,49.66,53.76,59.75,63.71,65.8,70.06]
    def construct(self):
        self.start()
        hdr = pill("ChatGPT", gpt)
        hdr.to_corner(UL, buff=0.45)
        sub = label("finds the real bound", 20, dim)
        sub.next_to(hdr, RIGHT, buff=0.45)
        self.play_(FadeIn(hdr, shift=DOWN*0.2), Write(sub), rt=1.0)

        self.cue(0)
        found = label("ChatGPT found something the others missed", 22, gpt)
        found.move_to(UP*1.7)
        self.play_(Write(found), rt=1.3)

        self.cue(1)
        sevendigit = label("ten million has seven digits", 19, ink)
        sevendigit.next_to(found, DOWN, buff=0.45)
        self.play_(FadeIn(sevendigit), rt=1.1)

        self.cue(2)
        maxdigit = label("@\\text{biggest digit squared: } 9^2 = 81", 24, dim)
        maxdigit.next_to(sevendigit, DOWN, buff=0.45)
        self.play_(Write(maxdigit), rt=1.4)

        self.cue(3)
        sevenof = label("@7 \\times 81 = 567", 30, gold)
        sevenof.next_to(maxdigit, DOWN, buff=0.5)
        self.play_(Write(sevenof), rt=1.2)

        self.cue(4)
        ceiling = label("that's the hard ceiling", 19, gold)
        ceiling.next_to(sevenof, DOWN, buff=0.35)
        self.play_(FadeIn(ceiling), rt=1.0)

        self.cue(5)
        self.play_(FadeOut(VGroup(found, sevendigit, maxdigit, sevenof, ceiling)), rt=0.5)
        onestep = label("after just one step, you're already under 567", 21, ink)
        onestep.move_to(UP*1.5)
        self.play_(Write(onestep), rt=1.5)

        self.cue(6)
        big = label("10,000,000", 34, dim)
        big.move_to(UP*0.4+LEFT*2.5)
        self.play_(FadeIn(big), rt=0.8)

        self.cue(7)
        shrink = Arrow(big.get_bottom(), big.get_bottom()+DOWN*0.8+RIGHT*2.5, buff=0.15, stroke_width=3, color=gold)
        self.play_(GrowArrow(shrink), rt=0.7)

        self.cue(8)
        small = label("567", 34, gold)
        small.next_to(shrink.get_end(), RIGHT, buff=0.3)
        self.play_(FadeIn(small, scale=0.7), rt=0.8)

        self.cue(9)
        self.play_(FadeOut(VGroup(onestep, big, shrink, small)), rt=0.5)
        table = label("precompute the answer for 1 through 567 once", 21, gpt)
        table.move_to(UP*1.4)
        self.play_(Write(table), rt=1.5)

        self.cue(10)
        grid = VGroup(*[Square(0.35).set_fill(panel,1).set_stroke(gpt,1.2) for _ in range(12)])
        grid.arrange(RIGHT, buff=0.08).move_to(UP*0.5)
        self.play_(LaggedStart(*[FadeIn(s, scale=0.7) for s in grid], lag_ratio=0.06), rt=1.2)

        self.cue(11)
        dotdot = label("...", 22, dim)
        dotdot.next_to(grid, RIGHT, buff=0.2)
        self.play_(FadeIn(dotdot), rt=0.5)

        self.cue(12)
        store = label("567 full chains, computed exactly once", 19, dim)
        store.next_to(grid, DOWN, buff=0.5)
        self.play_(FadeIn(store), rt=1.3)

        self.cue(13)
        self.play_(FadeOut(VGroup(table, grid, dotdot, store)), rt=0.5)
        loop = label("then for ten million numbers", 21, ink)
        loop.move_to(UP*1.2)
        self.play_(Write(loop), rt=1.2)

        self.cue(14)
        onelook = label("one shrink, one lookup", 24, gold)
        onelook.next_to(loop, DOWN, buff=0.5)
        self.play_(Write(onelook), rt=1.1)

        self.cue(15)
        nomore = label("no full chain ever runs twice", 19, dim)
        nomore.next_to(onelook, DOWN, buff=0.4)
        self.play_(FadeIn(nomore), rt=1.2)

        self.cue(16)
        self.play_(FadeOut(VGroup(loop, onelook, nomore)), rt=0.5)
        compare = VGroup(
            label("567 chains + 10,000,000 lookups", 20, gpt),
            label("vs.  10,000,000 full chains", 20, dim),
        ).arrange(DOWN, buff=0.35)
        compare.move_to(UP*0.5)
        self.play_(Write(compare[0]), rt=1.3)

        self.cue(17)
        self.play_(Write(compare[1]), rt=1.2)

        self.cue(18)
        grind = label("solving the small core once beats grinding ten million times", 18, dim)
        grind.next_to(compare, DOWN, buff=0.5)
        self.play_(Write(grind), rt=1.6)

        self.cue(19)
        fastest = label("clearly the fastest of the four", 22, gold)
        fastest.next_to(grind, DOWN, buff=0.4)
        self.play_(Write(fastest), rt=1.3)
        self.finish(70.06+1.3)


class sec5gemini(base):
    times = [0.52,2.16,6.95,9.51,15.13,20.16,24.34,33.83,34.55,37.61,46.79,51.99,59.55,61.68]
    def construct(self):
        self.start()
        hdr = pill("Gemini", gem)
        hdr.to_corner(UL, buff=0.45)
        sub = label("smart caching, not quite as far", 20, dim)
        sub.next_to(hdr, RIGHT, buff=0.45)
        self.play_(FadeIn(hdr, shift=DOWN*0.2), Write(sub), rt=1.0)

        self.cue(0)
        also = label("also completely correct, built on a smart idea", 21, gem)
        also.move_to(UP*1.6)
        self.play_(Write(also), rt=1.4)

        self.cue(1)
        memo = label("memoization --- a cache that remembers answers", 20, ink)
        memo.next_to(also, DOWN, buff=0.5)
        self.play_(FadeIn(memo), rt=1.3)

        self.cue(2)
        cache = RoundedRectangle(corner_radius=0.12, width=4.2, height=2.0).set_stroke(gem, 1.6).set_fill(panel,1)
        cache.move_to(DOWN*0.2)
        cachelabel = label("cache", 17, dim)
        cachelabel.next_to(cache, UP, buff=0.25)
        self.play_(FadeIn(cache), FadeIn(cachelabel), rt=0.9)

        self.cue(3)
        entries = VGroup(
            label("13 $\\rightarrow$ 89", 18, ink, font=mono),
            label("32 $\\rightarrow$ 89", 18, ink, font=mono),
        ).arrange(DOWN, buff=0.25).move_to(cache)
        self.play_(FadeIn(entries[0]), rt=0.6)

        self.cue(4)
        self.play_(FadeIn(entries[1]), rt=0.6)

        self.cue(5)
        crosspath = label("chains cross paths and funnel through the same numbers", 18, gem)
        crosspath.next_to(cache, DOWN, buff=0.55)
        self.play_(Write(crosspath), rt=1.6)

        self.cue(6)
        avoid = label("Gemini avoids a huge amount of repeated work", 19, ink)
        avoid.next_to(crosspath, DOWN, buff=0.35)
        self.play_(FadeIn(avoid), rt=1.4)

        self.cue(7)
        self.play_(FadeOut(VGroup(also, memo, cache, cachelabel, entries, crosspath, avoid)), rt=0.5)
        cost = label("but there's a cost ChatGPT's version doesn't pay", 21, bad)
        cost.move_to(UP*1.3)
        self.play_(Write(cost), rt=1.5)

        self.cue(8)
        everynum = label("every number, big or small, gets its own entry", 19, ink)
        everynum.next_to(cost, DOWN, buff=0.5)
        self.play_(FadeIn(everynum), rt=1.3)

        self.cue(9)
        tenmillentries = label("ten million dictionary lookups carry real overhead", 19, dim)
        tenmillentries.next_to(everynum, DOWN, buff=0.35)
        self.play_(Write(tenmillentries), rt=1.5)

        self.cue(10)
        self.play_(FadeOut(VGroup(cost, everynum, tenmillentries)), rt=0.5)
        sidestep = label("ChatGPT proved it only ever needed 567 entries", 20, gpt)
        sidestep.move_to(UP*0.5)
        self.play_(Write(sidestep), rt=1.5)

        self.cue(11)
        notmillions = label("not millions", 20, gpt)
        notmillions.next_to(sidestep, DOWN, buff=0.4)
        self.play_(FadeIn(notmillions), rt=0.9)

        self.cue(12)
        self.play_(FadeOut(VGroup(sidestep, notmillions)), rt=0.4)
        second = label("a very solid second place", 24, gem)
        second.move_to(UP*0.2)
        self.play_(Write(second), rt=1.3)

        self.cue(13)
        smartcaching = label("smart caching, correct answer, just not the smallest cache", 18, dim)
        smartcaching.next_to(second, DOWN, buff=0.4)
        self.play_(FadeIn(smartcaching), rt=1.4)
        self.finish(61.68+1.3)


class sec6claude(base):
    times = [0.63,3.85,7.86,10.54,15.13,18.54,23.2,30.04,31.54,33.05,43.23,46.63,49.06,57.81,62.04]
    def construct(self):
        self.start()
        hdr = pill("Claude", cld)
        hdr.to_corner(UL, buff=0.45)
        sub = label("no cleverness this time", 20, dim)
        sub.next_to(hdr, RIGHT, buff=0.45)
        self.play_(FadeIn(hdr, shift=DOWN*0.2), Write(sub), rt=1.0)

        self.cue(0)
        rare = label("a rare one --- no cleverness brought to this problem", 21, cld)
        rare.move_to(UP*1.6)
        self.play_(Write(rare), rt=1.5)

        self.cue(1)
        honest = label("honest, straightforward brute force", 21, ink)
        honest.next_to(rare, DOWN, buff=0.5)
        self.play_(FadeIn(honest), rt=1.3)

        self.cue(2)
        chains = VGroup(*[numrow(str(n), size=0.42, color=dim) for n in [1,2,3]])
        chains.arrange(DOWN, buff=0.3).move_to(DOWN*0.3+LEFT*3)
        self.play_(LaggedStart(*[FadeIn(c) for c in chains], lag_ratio=0.2), rt=0.9)

        self.cue(3)
        fromscratch = label("every chain runs step by step from scratch", 19, ink)
        fromscratch.next_to(chains, RIGHT, buff=0.6)
        self.play_(Write(fromscratch), rt=1.4)

        self.cue(4)
        nocache = label("no caching", 19, bad)
        nocache.next_to(fromscratch, DOWN, buff=0.3).align_to(fromscratch, LEFT)
        self.play_(FadeIn(nocache), rt=0.8)

        self.cue(5)
        noshortcut = label("no shortcuts", 19, bad)
        noshortcut.next_to(nocache, DOWN, buff=0.2).align_to(nocache, LEFT)
        self.play_(FadeIn(noshortcut), rt=0.8)

        self.cue(6)
        nobound = label("no bound on the numbers", 19, bad)
        nobound.next_to(noshortcut, DOWN, buff=0.2).align_to(noshortcut, LEFT)
        self.play_(FadeIn(nobound), rt=0.9)

        self.cue(7)
        self.play_(FadeOut(VGroup(rare, honest, chains, fromscratch, nocache, noshortcut, nobound)), rt=0.5)
        toclear = label("to be clear, nothing here is wrong", 22, good)
        toclear.move_to(UP*0.8)
        self.play_(Write(toclear), rt=1.4)

        self.cue(8)
        checks = label("it checks every number, every chain, correctly", 19, ink)
        checks.next_to(toclear, DOWN, buff=0.5)
        self.play_(FadeIn(checks), rt=1.4)

        self.cue(9)
        rightanswer = label("and arrives at exactly the right answer", 19, dim)
        rightanswer.next_to(checks, DOWN, buff=0.35)
        self.play_(Write(rightanswer), rt=1.3)

        self.cue(10)
        self.play_(FadeOut(VGroup(toclear, checks, rightanswer)), rt=0.5)
        thirty = label("the version you'd write in thirty seconds", 22, dim)
        thirty.move_to(UP*0.5)
        self.play_(Write(thirty), rt=1.4)

        self.cue(11)
        noinsight = label("no reuse, no insight into how small this collapses", 19, ink)
        noinsight.next_to(thirty, DOWN, buff=0.4)
        self.play_(FadeIn(noinsight), rt=1.5)

        self.cue(12)
        self.play_(FadeOut(VGroup(thirty, noinsight)), rt=0.4)
        pastdeep = label("the model that's found the deepest insight before", 21, cld)
        pastdeep.move_to(UP*0.3)
        self.play_(Write(pastdeep), rt=1.5)

        self.cue(13)
        justjob = label("this time just did the job. nothing more.", 21, dim)
        justjob.next_to(pastdeep, DOWN, buff=0.45)
        self.play_(Write(justjob), rt=1.4)
        self.finish(62.04+1.3)


class sec7eval(base):
    times = [0.56,2.65,9.2,9.83,11.65,18.04,19.5,24.08,26.31,27.63,28.12,30.72,34.21,37.0,39.4,41.79,43.24]
    def construct(self):
        self.start()
        self.cue(0)
        title = label("Side by Side", 30)
        title.to_edge(UP, buff=0.55)
        self.play_(Write(title), rt=1.0)

        rows = [
            ("ChatGPT", gpt, "bounds to 567, precomputes once", "5.91s", good),
            ("Gemini", gem, "memoized recursion", "11.18s", good),
            ("Claude", cld, "honest brute force", "17.19s", dim),
            ("Grok", grok, "brute force + unused tracking", "21.58s", bad),
        ]
        cards = VGroup()
        for nm, col, meth, res, rc in rows:
            box = RoundedRectangle(corner_radius=0.1, width=10.6, height=0.92).set_fill(panel, 1).set_stroke(col, 1.6)
            name = label(nm, 22, col)
            name.move_to(box.get_left()+RIGHT*1.2)
            m = label(meth, 17, ink)
            m.move_to(box.get_center()+LEFT*0.3)
            r = label(res, 18, rc)
            r.move_to(box.get_right()+LEFT*1.3)
            cards.add(VGroup(box, name, m, r))
        cards.arrange(DOWN, buff=0.28).move_to(DOWN*0.1)

        self.cue(1)
        self.play_(FadeIn(cards[0], shift=RIGHT*0.25), rt=0.8)
        self.cue(2)
        self.cue(3)
        self.play_(FadeIn(cards[1], shift=RIGHT*0.25), rt=0.8)
        self.cue(4)
        self.play_(FadeIn(cards[2], shift=RIGHT*0.25), rt=0.8)
        self.cue(5)
        self.cue(6)
        self.play_(FadeIn(cards[3], shift=RIGHT*0.25), rt=0.8)

        self.cue(7)
        allans = label("all four landed on 8,581,146", 20, good)
        allans.next_to(cards, DOWN, buff=0.45)
        self.play_(Write(allans), rt=1.4)

        self.cue(8)
        self.cue(9)
        self.cue(10)
        onefig = label("but only one figured out why the problem was small", 19, gold)
        onefig.next_to(allans, DOWN, buff=0.35)
        self.play_(Write(onefig), rt=1.5)

        self.cue(11)
        self.cue(12)
        self.cue(13)
        self.cue(14)
        self.cue(15)
        self.cue(16)
        self.finish(43.24+1.3)


class sec8verdict(base):
    times = [0.51,2.17,4.65,7.13,12.0,15.67,17.98,21.69,28.35,30.95,34.77,36.81,41.04,46.64,51.76,55.74,65.05,68.4]
    def construct(self):
        self.start()
        head = label("The Verdict", 32)
        head.to_edge(UP, buff=0.5)
        names = ["ChatGPT", "Gemini", "Claude", "Grok"]
        cols = {"ChatGPT": gpt, "Gemini": gem, "Claude": cld, "Grok": grok}
        scs = VGroup()
        for nm in names:
            box = RoundedRectangle(corner_radius=0.08, width=4.4, height=0.78).set_fill(panel, 1).set_stroke(gridcol, 1.2)
            lab = label(nm, 20, cols[nm])
            lab.move_to(box.get_left()+RIGHT*0.95)
            scs.add(VGroup(box, lab))
        scs.arrange(DOWN, buff=0.22).to_edge(RIGHT, buff=0.6)
        focus = LEFT*3.2+UP*0.3

        def note(i, txt, col):
            nt = label(txt, 15, col)
            nt.move_to(scs[i][0].get_right()+LEFT*1.45)
            self.play_(FadeIn(nt, shift=LEFT*0.15), rt=0.5)

        self.cue(0)
        self.play_(Write(head), rt=0.8)
        self.play_(*[FadeIn(r[0]) for r in scs], *[FadeIn(r[1]) for r in scs], rt=1.0)
        gf = pill("ChatGPT", gpt, w=2.8, h=0.9, size=26)
        gf.move_to(focus)
        crown = Polygon([-0.4,0,0],[-0.24,0.32,0],[0,0.06,0],[0.24,0.32,0],[0.4,0,0]).set_fill(gold,1).set_stroke(gold,1).scale(0.85)
        crown.next_to(gf, UP, buff=0.12)
        self.play_(FadeIn(gf, shift=DOWN*0.2), rt=0.6)
        self.play_(FadeIn(crown, shift=DOWN*0.3), rt=0.5)

        self.cue(1)
        g1 = label("the sharpest read of the problem", 17, gpt)
        g1.next_to(gf, DOWN, buff=0.45)
        self.play_(Write(g1), rt=1.0)
        note(0, "winner", gold)

        self.cue(2)
        g2 = label("saw it's really a problem about 567 numbers", 17, ink)
        g2.next_to(g1, DOWN, buff=0.22)
        self.play_(Write(g2), rt=1.0)

        self.cue(3)
        g3 = label("not ten million", 17, dim)
        g3.next_to(g2, DOWN, buff=0.22)
        self.play_(Write(g3), rt=0.9)

        self.cue(4)
        self.play_(FadeOut(VGroup(gf, crown, g1, g2, g3)), rt=0.4)
        mf = pill("Gemini", gem, w=2.8, h=0.9, size=26)
        mf.move_to(focus)
        self.play_(FadeIn(mf, shift=DOWN*0.2), rt=0.6)
        m1 = label("a strong second", 17, gem)
        m1.next_to(mf, DOWN, buff=0.45)
        self.play_(Write(m1), rt=1.0)
        note(1, "2nd, cached", gem)

        self.cue(5)
        m2 = label("memoization is real and valid, saved real work", 17, ink)
        m2.next_to(m1, DOWN, buff=0.22)
        self.play_(Write(m2), rt=1.1)

        self.cue(6)
        m3 = label("just didn't prove how small the cache could be", 17, dim)
        m3.next_to(m2, DOWN, buff=0.22)
        self.play_(Write(m3), rt=1.1)

        self.cue(7)
        self.play_(FadeOut(VGroup(mf, m1, m2, m3)), rt=0.4)
        cf = pill("Claude", cld, w=2.8, h=0.9, size=26)
        cf.move_to(focus)
        self.play_(FadeIn(cf, shift=DOWN*0.2), rt=0.6)
        c1 = label("third, and there's no shame in it", 17, cld)
        c1.next_to(cf, DOWN, buff=0.45)
        self.play_(Write(c1), rt=1.1)
        note(2, "correct, plain", cld)

        self.cue(8)
        c2 = label("the logic is completely correct", 17, ink)
        c2.next_to(c1, DOWN, buff=0.22)
        self.play_(Write(c2), rt=1.0)

        self.cue(9)
        c3 = label("just the plainest version --- no reuse, no bound", 17, dim)
        c3.next_to(c2, DOWN, buff=0.22)
        self.play_(Write(c3), rt=1.1)

        self.cue(10)
        self.play_(FadeOut(VGroup(cf, c1, c2, c3)), rt=0.4)
        rf = pill("Grok", grok, w=2.8, h=0.9, size=26)
        rf.move_to(focus)
        self.play_(FadeIn(rf, shift=DOWN*0.2), rt=0.6)
        r1 = label("last, not because anything was wrong", 17, grok)
        r1.next_to(rf, DOWN, buff=0.45)
        self.play_(Write(r1), rt=1.1)
        note(3, "slowest", bad)

        self.cue(11)
        r2 = label("it did extra work for zero payoff", 17, ink)
        r2.next_to(r1, DOWN, buff=0.22)
        self.play_(Write(r2), rt=1.0)

        self.cue(12)
        r3 = label("tracking data it never once used", 17, dim)
        r3.next_to(r2, DOWN, buff=0.22)
        self.play_(Write(r3), rt=1.0)

        self.cue(13)
        r4 = label("sometimes slow code is just carrying weight it didn't need", 16, bad)
        r4.next_to(r3, DOWN, buff=0.22)
        self.play_(Write(r4), rt=1.4)

        self.cue(14)
        self.play_(FadeOut(VGroup(rf, r1, r2, r3, r4)), rt=0.4)
        fin1 = label("Project Euler 92", 22, dim)
        fin1.move_to(focus+UP*0.6)
        fin2 = label("8,581,146", 38, gold)
        fin2.next_to(fin1, DOWN, buff=0.35)
        fbox = SurroundingRectangle(fin2, buff=0.2).set_stroke(gold, 2)
        self.play_(FadeIn(fin1), rt=0.6)
        self.play_(Write(fin2), rt=1.0)
        self.play_(Create(fbox), rt=0.6)

        self.cue(15)
        outof = label("out of the almost ten million below ten million", 18, ink)
        outof.next_to(fbox, DOWN, buff=0.5)
        self.play_(Write(outof), rt=1.4)

        self.cue(16)
        eighty5 = label("over eighty five percent end up at 89", 20, gold)
        eighty5.next_to(outof, DOWN, buff=0.35)
        self.play_(Write(eighty5), rt=1.4)

        self.cue(17)
        outro = label("same four models next time, different problem", 18, dim)
        outro.to_edge(DOWN, buff=0.7)
        self.play_(Write(outro), rt=1.5)
        self.finish(68.4+1.3)
