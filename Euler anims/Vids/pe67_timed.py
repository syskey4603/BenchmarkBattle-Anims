from manim import *
import numpy as np
import re

config.background_color = "#0A0A15"

mono = "Consolas"
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

def pill(name, color, w=2.4, h=0.74, size=23):
    box = RoundedRectangle(corner_radius=0.12, width=w, height=h).set_fill(panel, 1).set_stroke(color, 2)
    return VGroup(box, label(name, size, color).move_to(box))

demo = [
    [3],
    [7, 4],
    [2, 4, 6],
    [8, 5, 9, 20],
    [1, 1, 1, 1, 50],
]
greedy_path = [(0,0),(1,0),(2,1),(3,2),(4,2)]
optimal_path = [(0,0),(1,1),(2,2),(3,3),(4,4)]

def tri_positions(scale=0.85, center=ORIGIN):
    pos = {}
    rows = len(demo)
    gap_x = 1.05*scale
    gap_y = 0.95*scale
    for i,row in enumerate(demo):
        n = len(row)
        for j in range(n):
            x = (j - (n-1)/2) * gap_x
            y = (rows-1-i) * gap_y - (rows-1)*gap_y/2
            pos[(i,j)] = np.array([x, y, 0]) + center
    return pos

def build_triangle(scale=0.85, center=ORIGIN, node_r=0.32, numcolor=ink):
    pos = tri_positions(scale, center)
    nodes = {}
    edges = {}
    for i,row in enumerate(demo):
        for j,val in enumerate(row):
            c = Circle(radius=node_r).set_fill(panel, 1).set_stroke(gridcol, 1.8)
            t = label(str(val), 20, numcolor, font=mono).move_to(pos[(i,j)])
            c.move_to(pos[(i,j)])
            nodes[(i,j)] = VGroup(c, t)
    for i in range(len(demo)-1):
        for j in range(len(demo[i])):
            for k in (j, j+1):
                a = pos[(i,j)]; b = pos[(i+1,k)]
                ln = Line(a, b, buff=node_r).set_stroke(gridcol, 2)
                edges[(i,j,i+1,k)] = ln
    return pos, nodes, edges

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
    times = [0.0,4.38,9.92,11.3,14.17,19.48,29.44,37.68,39.52,40.91]
    def construct(self):
        self.start()
        self.cue(0)
        pos, nodes, edges = build_triangle(scale=0.55, center=UP*0.3)
        self.play_(*[Create(e) for e in edges.values()], rt=1.3)
        self.play_(*[GrowFromCenter(n) for n in nodes.values()], rt=1.0)

        self.cue(1)
        rule = label("start at the top, step to a number below", 19, dim)
        rule.to_edge(DOWN, buff=1.0)
        self.play_(FadeIn(rule), rt=1.0)
        dot = Dot(radius=0.1, color=good).move_to(pos[(0,0)])
        self.play_(FadeIn(dot), rt=0.4)
        for (i,j) in optimal_path[1:]:
            self.play_(dot.animate.move_to(pos[(i,j)]), rt=0.35)

        self.cue(2)
        biggest = label("which path gives the biggest total?", 21, gold)
        biggest.next_to(rule, UP, buff=0.4)
        self.play_(Write(biggest), rt=1.2)

        self.cue(3)
        self.play_(FadeOut(VGroup(*nodes.values(), *edges.values(), dot, rule, biggest)), rt=0.6)
        real = label("the real triangle has one hundred rows", 24, ink)
        real.move_to(UP*1.2)
        self.play_(Write(real), rt=1.4)

        self.cue(4)
        power = label("@2^{99}\\ \\text{possible paths}", 34, bad)
        power.next_to(real, DOWN, buff=0.5)
        self.play_(Write(power), rt=1.4)

        self.cue(5)
        years = label("twenty billion years to check them all", 20, dim)
        years.next_to(power, DOWN, buff=0.5)
        self.play_(FadeIn(years), rt=1.3)

        self.cue(6)
        self.play_(FadeOut(VGroup(real, power, years)), rt=0.5)
        chips = VGroup(pill("Kimi K3", kimi), pill("Fable", fable),
                        pill("GPT-5.6 Sol", gpt), pill("Grok 4.5", grok)).arrange(RIGHT, buff=0.28)
        chips.scale(0.9).move_to(UP*0.3)
        self.play_(FadeIn(chips, shift=UP*0.2), rt=1.2)

        self.cue(7)
        nohints = label("same problem, no hints", 19, dim)
        nohints.next_to(chips, DOWN, buff=0.6)
        self.play_(Write(nohints), rt=1.1)

        self.cue(8)
        twist = label("the fastest model wasn't the one that got it right", 20, gold)
        twist.next_to(nohints, DOWN, buff=0.4)
        self.play_(Write(twist), rt=1.6)
        self.finish(45.61+1.3)


class sec2problem(base):
    times = [0.0,10.06,12.52,14.32,17.9,26.16,33.49,41.85,46.53,52.35]
    def construct(self):
        self.start()
        self.cue(0)
        title = label("Problem 67 --- Maximum Path Sum", 28)
        title.to_edge(UP, buff=0.5)
        self.play_(Write(title), rt=1.0)
        pos, nodes, edges = build_triangle(scale=0.78, center=DOWN*0.3)
        self.play_(*[Create(e) for e in edges.values()], rt=1.3)
        self.play_(*[GrowFromCenter(n) for n in nodes.values()], rt=1.0)

        self.cue(1)
        top = label("a single number at the top", 18, dim)
        top.to_edge(DOWN, buff=0.6)
        self.play_(FadeIn(top), rt=0.9)
        self.play_(nodes[(0,0)][0].animate.set_stroke(gold, 3), rt=0.6)

        self.cue(2)
        two = label("every row below gives you two choices", 18, dim)
        two.move_to(top)
        self.play_(FadeOut(top), rt=0.3); self.play_(Write(two), rt=1.1)

        self.cue(3)
        self.play_(edges[(0,0,1,0)].animate.set_stroke(gold,3),
                   edges[(0,0,1,1)].animate.set_stroke(gold,3), rt=0.8)

        self.cue(4)
        self.play_(edges[(0,0,1,0)].animate.set_stroke(gridcol,2),
                   edges[(0,0,1,1)].animate.set_stroke(gridcol,2), rt=0.4)
        add = label("add every number along your path", 18, ink)
        add.move_to(two)
        self.play_(FadeOut(two), rt=0.3); self.play_(Write(add), rt=1.1)
        dot = Dot(radius=0.1, color=good).move_to(pos[(0,0)])
        self.play_(FadeIn(dot), rt=0.4)
        for (i,j) in optimal_path[1:]:
            self.play_(dot.animate.move_to(pos[(i,j)]),
                       nodes[(i,j)][0].animate.set_stroke(good,3), rt=0.35)

        self.cue(5)
        self.play_(FadeOut(add), rt=0.3)
        goal = label("find the path with the biggest total", 20, gold)
        goal.to_edge(DOWN, buff=0.6)
        self.play_(Write(goal), rt=1.3)

        self.cue(6)
        self.play_(FadeOut(dot), FadeOut(goal),
                   *[nodes[k][0].animate.set_stroke(gridcol,1.8) for k in nodes], rt=0.6)
        small = label("for five rows, checking every path is easy", 19, ink)
        small.to_edge(DOWN, buff=0.6)
        self.play_(Write(small), rt=1.4)

        self.cue(7)
        self.play_(FadeOut(small), rt=0.3)
        hundred = label("the real triangle has one hundred rows", 21, bad)
        hundred.to_edge(DOWN, buff=0.9)
        self.play_(Write(hundred), rt=1.4)

        self.cue(8)
        scale_up = label("@2^{99}\\ \\text{paths --- impossible to brute force}", 20, bad)
        scale_up.next_to(hundred, DOWN, buff=0.4)
        self.play_(Write(scale_up), rt=1.6)
        self.finish(58.99+1.3)


class sec3grok(base):
    times = [0.0,6.38,18.82,23.56,28.52,29.52,36.46]
    def construct(self):
        self.start()
        hdr = pill("Grok 4.5", grok)
        hdr.to_corner(UL, buff=0.45)
        sub = label("checks every single path", 20, dim)
        sub.next_to(hdr, RIGHT, buff=0.45)
        self.play_(FadeIn(hdr, shift=DOWN*0.2), Write(sub), rt=1.0)

        self.cue(0)
        idea = label("branch left, branch right, at every single step", 20, grok)
        idea.move_to(UP*1.7)
        self.play_(Write(idea), rt=1.4)

        root = Dot(radius=0.09, color=grok).move_to(UP*0.9)
        self.play_(GrowFromCenter(root), rt=0.4)
        layer = [root]
        alldots = VGroup(root)
        alllines = VGroup()
        gaps = [3.2, 1.7, 0.9, 0.5]
        for depth in range(4):
            new = []
            gap = gaps[depth]
            for node in layer:
                for dx in (-1, 1):
                    child = Dot(radius=0.07, color=grok).move_to(
                        node.get_center() + DOWN*0.62 + RIGHT*dx*gap)
                    ln = Line(node.get_center(), child.get_center()).set_stroke(gridcol, 1.3)
                    alldots.add(child)
                    alllines.add(ln)
                    new.append(child)
            self.play_(*[Create(l) for l in alllines[-len(new):]],
                       *[GrowFromCenter(c) for c in new], rt=0.7)
            layer = new

        self.cue(1)
        onetotwo = label("one row down doubles the number of branches", 19, ink)
        onetotwo.to_edge(DOWN, buff=0.7)
        self.play_(Write(onetotwo), rt=1.5)

        self.cue(2)
        self.play_(FadeOut(VGroup(idea, alldots, alllines, onetotwo)), rt=0.6)
        correct = label("in theory, this is completely correct", 22, ink)
        correct.move_to(UP*1.0)
        self.play_(Write(correct), rt=1.4)

        self.cue(3)
        checks = label("if it finished, it would find the right answer", 19, dim)
        checks.next_to(correct, DOWN, buff=0.5)
        self.play_(FadeIn(checks), rt=1.4)

        self.cue(4)
        self.play_(FadeOut(VGroup(correct, checks)), rt=0.4)
        never = label("but with a hundred rows...", 22, bad)
        never.move_to(UP*0.6)
        self.play_(Write(never), rt=1.1)

        self.cue(5)
        stillgoing = label("@2^{99}\\ \\text{branches --- it just kept splitting}", 22, bad)
        stillgoing.next_to(never, DOWN, buff=0.5)
        self.play_(Write(stillgoing), rt=1.6)

        self.cue(6)
        disq = label("disqualified --- not wrong, just never finishes", 19, dim)
        disq.next_to(stillgoing, DOWN, buff=0.5)
        self.play_(Write(disq), rt=1.5)
        self.finish(49.28+1.3)


class sec4gpt(base):
    times = [0.0,9.97,17.26,19.23,20.4,25.56,32.19,40.07,41.27,43.24,48.03]
    def construct(self):
        self.start()
        hdr = pill("GPT-5.6 Sol", gpt)
        hdr.to_corner(UL, buff=0.45)
        sub = label("fastest, and the only one wrong", 20, bad)
        sub.next_to(hdr, RIGHT, buff=0.45)
        self.play_(FadeIn(hdr, shift=DOWN*0.2), Write(sub), rt=1.0)

        self.cue(0)
        greedy = label("always grab the bigger number in front of you", 20, gpt)
        greedy.move_to(UP*1.7)
        self.play_(Write(greedy), rt=1.5)

        pos, nodes, edges = build_triangle(scale=0.72, center=DOWN*0.4)
        self.play_(*[Create(e) for e in edges.values()], rt=1.0)
        self.play_(*[GrowFromCenter(n) for n in nodes.values()], rt=0.9)

        self.cue(1)
        dot = Dot(radius=0.1, color=gpt).move_to(pos[(0,0)])
        self.play_(FadeIn(dot), rt=0.4)
        for (i,j) in greedy_path[1:]:
            self.play_(dot.animate.move_to(pos[(i,j)]),
                       nodes[(i,j)][0].animate.set_stroke(gpt, 3), rt=0.5)

        self.cue(2)
        sounds = label("no lookahead, just take what's bigger right now", 18, dim)
        sounds.to_edge(DOWN, buff=0.6)
        self.play_(FadeIn(sounds), rt=1.2)

        self.cue(3)
        gtotal = label("total: 24", 26, gpt)
        gtotal.next_to(sounds, UP, buff=0.4)
        self.play_(Write(gtotal), rt=0.9)

        self.cue(4)
        self.play_(FadeOut(sounds), rt=0.3)
        trap = label("but the small number it skipped led somewhere huge", 19, bad)
        trap.to_edge(DOWN, buff=0.6)
        self.play_(Write(trap), rt=1.6)

        self.cue(5)
        dim_fades = [nodes[k][0].animate.set_stroke(gridcol, 1.8) for k in nodes]
        self.play_(FadeOut(trap), FadeOut(gtotal), dot.animate.set_opacity(0.15),
                   *dim_fades, rt=0.6)
        dot2 = Dot(radius=0.1, color=good).move_to(pos[(0,0)])
        self.play_(FadeIn(dot2), rt=0.4)
        for (i,j) in optimal_path[1:]:
            self.play_(dot2.animate.move_to(pos[(i,j)]),
                       nodes[(i,j)][0].animate.set_stroke(good, 3).set_opacity(1), rt=0.5)

        self.cue(6)
        otitle = label("true best: 83", 26, good)
        otitle.to_edge(DOWN, buff=0.9)
        self.play_(Write(otitle), rt=1.0)

        self.cue(7)
        gap = label("greedy missed it by 59, on a tiny example", 19, dim)
        gap.next_to(otitle, DOWN, buff=0.35)
        self.play_(FadeIn(gap), rt=1.3)

        self.cue(8)
        self.play_(FadeOut(VGroup(*nodes.values(), *edges.values(), dot, dot2, otitle, gap, greedy)), rt=0.5)
        real = label("on the real triangle: 6580 instead of 7273", 22, bad)
        real.move_to(UP*0.3)
        self.play_(Write(real), rt=1.6)

        self.cue(9)
        moral = label("the fastest program here, and it's flat out wrong", 19, dim)
        moral.next_to(real, DOWN, buff=0.5)
        self.play_(Write(moral), rt=1.6)
        self.finish(57.28+1.3)


class sec5fable(base):
    times = [0.0,4.86,8.4,9.63,12.34,14.2,21.14,26.37,28.66,31.3,32.86,39.52,43.6,50.78,56.37]
    def construct(self):
        self.start()
        hdr = pill("Fable", fable)
        hdr.to_corner(UL, buff=0.45)
        sub = label("proves it, step by step", 20, dim)
        sub.next_to(hdr, RIGHT, buff=0.45)
        self.play_(FadeIn(hdr, shift=DOWN*0.2), Write(sub), rt=1.0)

        self.cue(0)
        different = label("a completely different approach", 21, fable)
        different.move_to(UP*1.6)
        self.play_(Write(different), rt=1.3)

        self.cue(1)
        works = label("works backward using recursion", 19, ink)
        works.next_to(different, DOWN, buff=0.5)
        self.play_(FadeIn(works), rt=1.1)

        self.cue(2)
        question = label("what's the best total from here to the bottom?", 19, dim)
        question.next_to(works, DOWN, buff=0.35)
        self.play_(Write(question), rt=1.4)

        self.cue(3)
        self.play_(FadeOut(VGroup(different, works, question)), rt=0.5)
        pos, nodes, edges = build_triangle(scale=0.72, center=DOWN*0.4)
        self.play_(*[Create(e) for e in edges.values()], rt=1.0)
        self.play_(*[GrowFromCenter(n) for n in nodes.values()], rt=0.9)

        self.cue(4)
        askdown = label("it asks the same question about the row below", 18, fable)
        askdown.to_edge(DOWN, buff=0.6)
        self.play_(FadeIn(askdown), rt=1.2)
        arrows = VGroup()
        for i in range(len(demo)-1):
            for j in range(len(demo[i])):
                for k in (j, j+1):
                    a = Arrow(pos[(i,j)], pos[(i+1,k)], buff=0.32, stroke_width=1.6,
                              color=fable, max_tip_length_to_length_ratio=0.15)
                    arrows.add(a)
        self.play_(*[GrowArrow(a) for a in arrows], rt=1.4)

        self.cue(5)
        self.play_(FadeOut(askdown), FadeOut(arrows), rt=0.5)
        blowup = label("that alone would explode just like before", 18, bad)
        blowup.to_edge(DOWN, buff=0.6)
        self.play_(Write(blowup), rt=1.3)

        self.cue(6)
        self.play_(FadeOut(blowup), rt=0.3)
        remembers = label("but it remembers every answer it's already found", 19, good)
        remembers.to_edge(DOWN, buff=0.6)
        self.play_(Write(remembers), rt=1.5)

        self.cue(7)
        cache = RoundedRectangle(corner_radius=0.1, width=3.4, height=1.6).set_stroke(fable, 1.6).set_fill(panel,1)
        cache.to_edge(RIGHT, buff=0.7).shift(UP*1.2)
        cachelabel = label("cache", 15, dim)
        cachelabel.next_to(cache, UP, buff=0.2)
        self.play_(FadeIn(cache), FadeIn(cachelabel), rt=0.8)

        self.cue(8)
        for pos_key in [(4,2),(3,2),(2,1)]:
            self.play_(nodes[pos_key][0].animate.set_stroke(fable, 3), rt=0.35)
        entry = label(f"{demo[2][1]} solved once", 15, ink, font=mono)
        entry.move_to(cache)
        self.play_(FadeIn(entry), rt=0.5)

        self.cue(9)
        reused = label("if another path needs it, just look it up", 18, dim)
        reused.to_edge(DOWN, buff=0.6)
        self.play_(Write(reused), rt=1.4)

        self.cue(10)
        self.play_(FadeOut(VGroup(cache, cachelabel, entry, reused)), rt=0.5)
        onlyfew = label("about five thousand positions, not two to the ninety nine", 18, fable)
        onlyfew.to_edge(DOWN, buff=0.6)
        self.play_(Write(onlyfew), rt=1.6)

        self.cue(11)
        self.play_(FadeOut(onlyfew), rt=0.4)
        ans = label("7273", 34, good)
        ans.to_edge(DOWN, buff=1.0)
        self.play_(Write(ans), rt=1.0)

        self.cue(12)
        proven = label("proven correct at every single step", 18, dim)
        proven.next_to(ans, DOWN, buff=0.3)
        self.play_(FadeIn(proven), rt=1.2)

        self.cue(13)
        heavier = label("just a little heavier than it needs to be", 18, dim)
        heavier.move_to(proven)
        self.play_(FadeOut(proven), rt=0.3); self.play_(Write(heavier), rt=1.3)
        self.finish(61.10+1.3)


class sec6kimi(base):
    times = [0.0,6.94,13.41,19.47,20.77,26.78,32.24,38.62,48.01,50.52,58.5,64.09]
    def construct(self):
        self.start()
        hdr = pill("Kimi K3", kimi)
        hdr.to_corner(UL, buff=0.45)
        sub = label("lean, direct, and fastest correct", 20, dim)
        sub.next_to(hdr, RIGHT, buff=0.45)
        self.play_(FadeIn(hdr, shift=DOWN*0.2), Write(sub), rt=1.0)

        self.cue(0)
        sameanswer = label("the same correct answer, from something leaner", 20, kimi)
        sameanswer.move_to(UP*1.6)
        self.play_(Write(sameanswer), rt=1.4)

        self.cue(1)
        bottomup = label("start at the bottom row, and work upward", 20, ink)
        bottomup.next_to(sameanswer, DOWN, buff=0.5)
        self.play_(FadeIn(bottomup), rt=1.3)

        self.cue(2)
        self.play_(FadeOut(VGroup(sameanswer, bottomup)), rt=0.5)
        pos, nodes, edges = build_triangle(scale=0.72, center=DOWN*0.4)
        self.play_(*[Create(e) for e in edges.values()], rt=1.0)
        self.play_(*[GrowFromCenter(n) for n in nodes.values()], rt=0.9)

        self.cue(3)
        bottomrow = len(demo)-1
        self.play_(*[nodes[(bottomrow,j)][0].animate.set_stroke(kimi,3) for j in range(len(demo[bottomrow]))], rt=0.8)

        self.cue(4)
        pair = label("take the bigger of two neighbors, add it to the row above", 17, dim)
        pair.to_edge(DOWN, buff=0.6)
        self.play_(FadeIn(pair), rt=1.4)

        self.cue(5)
        working = [row[:] for row in demo]
        for i in range(len(demo)-2, -1, -1):
            updates = []
            for j in range(len(demo[i])):
                childL = working[i+1][j]
                childR = working[i+1][j+1]
                newval = demo[i][j] + max(childL, childR)
                working[i][j] = newval
                newtext = label(str(newval), 20, kimi, font=mono).move_to(pos[(i,j)])
                updates.append(Transform(nodes[(i,j)][1], newtext))
                updates.append(nodes[(i,j)][0].animate.set_stroke(kimi, 3))
            self.play_(*updates, rt=0.55)

        self.cue(6)
        climb = label("climb one row at a time, no recursion at all", 18, dim)
        climb.to_edge(DOWN, buff=0.6)
        self.play_(FadeOut(pair), rt=0.3); self.play_(Write(climb), rt=1.4)

        self.cue(7)
        onearray = label("just one array of numbers, updated in place", 19, kimi)
        onearray.move_to(climb)
        self.play_(FadeOut(climb), rt=0.3); self.play_(Write(onearray), rt=1.4)

        self.cue(8)
        self.play_(FadeOut(onearray), rt=0.4)
        top = label(f"top of the triangle: {working[0][0]}", 24, good)
        top.to_edge(DOWN, buff=0.9)
        self.play_(Write(top), rt=1.2)

        self.cue(9)
        real = label("on the real triangle: 7273, correct", 22, good)
        real.next_to(top, DOWN, buff=0.4)
        self.play_(Write(real), rt=1.5)

        self.cue(10)
        fastest = label("and noticeably faster than anything else that got it right", 18, dim)
        fastest.next_to(real, DOWN, buff=0.4)
        self.play_(Write(fastest), rt=1.7)
        self.finish(64.60+1.3)


class sec7eval(base):
    times = [0.0,2.29,6.45,14.3,19.77,26.8,32.2]
    def construct(self):
        self.start()
        self.cue(0)
        title = label("Side by Side", 30)
        title.to_edge(UP, buff=0.55)
        self.play_(Write(title), rt=1.0)

        rows = [
            ("Kimi K3", kimi, "bottom-up, in place", "7273  ---  fastest correct", good),
            ("Fable", fable, "memoized recursion", "7273", good),
            ("GPT-5.6 Sol", gpt, "greedy, no lookahead", "6580  ---  wrong", bad),
            ("Grok 4.5", grok, "checks every path", "never finishes", bad),
        ]
        cards = VGroup()
        for nm, col, meth, res, rc in rows:
            box = RoundedRectangle(corner_radius=0.1, width=10.8, height=0.92).set_fill(panel, 1).set_stroke(col, 1.6)
            name = label(nm, 21, col)
            name.move_to(box.get_left()+RIGHT*1.35)
            m = label(meth, 16, ink)
            m.move_to(box.get_center()+LEFT*0.5)
            r = label(res, 16, rc)
            r.move_to(box.get_right()+LEFT*1.6)
            cards.add(VGroup(box, name, m, r))
        cards.arrange(DOWN, buff=0.28).move_to(DOWN*0.1)

        self.cue(1)
        self.play_(FadeIn(cards[0], shift=RIGHT*0.25), rt=0.8)
        self.cue(2)
        self.play_(FadeIn(cards[1], shift=RIGHT*0.25), rt=0.8)
        self.cue(3)
        self.play_(FadeIn(cards[2], shift=RIGHT*0.25), rt=0.8)
        self.cue(4)
        self.play_(FadeIn(cards[3], shift=RIGHT*0.25), rt=0.8)

        self.cue(5)
        summary = label("one never finished, one finished first and was wrong", 18, dim)
        summary.next_to(cards, DOWN, buff=0.45)
        self.play_(Write(summary), rt=1.6)

        self.cue(6)
        summary2 = label("two were correct, with very different overhead", 18, good)
        summary2.next_to(summary, DOWN, buff=0.25)
        self.play_(Write(summary2), rt=1.4)
        self.finish(34.52+1.3)


class sec8verdict(base):
    times = [0.0,5.46,13.98,18.23,22.56,27.95,30.33,36.2,40.35,45.57,49.62,54.79,60.49]
    def construct(self):
        self.start()
        head = label("The Verdict", 32)
        head.to_edge(UP, buff=0.5)
        names = ["Kimi K3", "Fable", "GPT-5.6 Sol", "Grok 4.5"]
        cols = {"Kimi K3": kimi, "Fable": fable, "GPT-5.6 Sol": gpt, "Grok 4.5": grok}
        scs = VGroup()
        for nm in names:
            box = RoundedRectangle(corner_radius=0.08, width=4.6, height=0.78).set_fill(panel, 1).set_stroke(gridcol, 1.2)
            lab = label(nm, 19, cols[nm])
            lab.move_to(box.get_left()+RIGHT*1.0)
            scs.add(VGroup(box, lab))
        scs.arrange(DOWN, buff=0.22).to_edge(RIGHT, buff=0.5)
        focus = LEFT*3.2+UP*0.3

        def note(i, txt, col):
            nt = label(txt, 14, col)
            nt.move_to(scs[i][0].get_right()+LEFT*1.55)
            self.play_(FadeIn(nt, shift=LEFT*0.15), rt=0.5)

        self.cue(0)
        self.play_(Write(head), rt=0.8)
        self.play_(*[FadeIn(r[0]) for r in scs], *[FadeIn(r[1]) for r in scs], rt=1.0)
        kf = pill("Kimi K3", kimi, w=2.9, h=0.9, size=24)
        kf.move_to(focus)
        crown = Polygon([-0.4,0,0],[-0.24,0.32,0],[0,0.06,0],[0.24,0.32,0],[0.4,0,0]).set_fill(gold,1).set_stroke(gold,1).scale(0.85)
        crown.next_to(kf, UP, buff=0.12)
        self.play_(FadeIn(kf, shift=DOWN*0.2), rt=0.6)
        self.play_(FadeIn(crown, shift=DOWN*0.3), rt=0.5)

        self.cue(1)
        k1 = label("least machinery, same correct answer", 16, kimi)
        k1.next_to(kf, DOWN, buff=0.45)
        self.play_(Write(k1), rt=1.1)
        note(0, "winner", gold)

        self.cue(2)
        k2 = label("no recursion, no growing cache, just one array", 16, ink)
        k2.next_to(k1, DOWN, buff=0.22)
        self.play_(Write(k2), rt=1.2)

        self.cue(3)
        self.play_(FadeOut(VGroup(kf, crown, k1, k2)), rt=0.4)
        ff = pill("Fable", fable, w=2.9, h=0.9, size=24)
        ff.move_to(focus)
        self.play_(FadeIn(ff, shift=DOWN*0.2), rt=0.6)
        f1 = label("a very close second", 16, fable)
        f1.next_to(ff, DOWN, buff=0.45)
        self.play_(Write(f1), rt=1.0)
        note(1, "2nd, proven", fable)

        self.cue(4)
        f2 = label("proves the answer correct at every single step", 16, ink)
        f2.next_to(f1, DOWN, buff=0.22)
        self.play_(Write(f2), rt=1.2)

        self.cue(5)
        f3 = label("just carrying overhead Kimi's approach skips", 16, dim)
        f3.next_to(f2, DOWN, buff=0.22)
        self.play_(Write(f3), rt=1.2)

        self.cue(6)
        self.play_(FadeOut(VGroup(ff, f1, f2, f3)), rt=0.4)
        pf = pill("GPT-5.6 Sol", gpt, w=2.9, h=0.9, size=22)
        pf.move_to(focus)
        self.play_(FadeIn(pf, shift=DOWN*0.2), rt=0.6)
        p1 = label("fastest by far, and it was wrong", 16, bad)
        p1.next_to(pf, DOWN, buff=0.45)
        self.play_(Write(p1), rt=1.1)
        note(2, "fast, wrong", bad)

        self.cue(7)
        p2 = label("greedy never looks back or reconsiders", 16, ink)
        p2.next_to(p1, DOWN, buff=0.22)
        self.play_(Write(p2), rt=1.1)

        self.cue(8)
        p3 = label("the fastest answer isn't worth much if it's wrong", 16, dim)
        p3.next_to(p2, DOWN, buff=0.22)
        self.play_(Write(p3), rt=1.3)

        self.cue(9)
        self.play_(FadeOut(VGroup(pf, p1, p2, p3)), rt=0.4)
        rf = pill("Grok 4.5", grok, w=2.9, h=0.9, size=24)
        rf.move_to(focus)
        self.play_(FadeIn(rf, shift=DOWN*0.2), rt=0.6)
        r1 = label("wanted certainty above everything else", 16, grok)
        r1.next_to(rf, DOWN, buff=0.45)
        self.play_(Write(r1), rt=1.1)
        note(3, "never finished", bad)

        self.cue(10)
        r2 = label("but the search space doesn't care how thorough you want to be", 15, dim)
        r2.next_to(r1, DOWN, buff=0.22)
        self.play_(Write(r2), rt=1.6)

        self.cue(11)
        self.play_(FadeOut(VGroup(rf, r1, r2)), rt=0.4)
        fin1 = label("Project Euler 67", 22, dim)
        fin1.move_to(focus+UP*0.6)
        fin2 = label("7273", 40, gold)
        fin2.next_to(fin1, DOWN, buff=0.35)
        fbox = SurroundingRectangle(fin2, buff=0.2).set_stroke(gold, 2)
        self.play_(FadeIn(fin1), rt=0.6)
        self.play_(Write(fin2), rt=1.0)
        self.play_(Create(fbox), rt=0.6)

        self.cue(12)
        outro = label("fastest isn't always right, thorough isn't always finished", 16, dim)
        outro.to_edge(DOWN, buff=0.7)
        self.play_(Write(outro), rt=1.6)
        self.finish(64.11+1.3)
