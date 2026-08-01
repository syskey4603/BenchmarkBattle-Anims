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

scale = 0.27
ax = 5 * scale
ay = 10 * scale
gapdeg = 4.5

def epoint(t):
    return np.array([ax * np.cos(t), ay * np.sin(t), 0.0])

def ellipsering(center=ORIGIN, color=gridcol, stroke=2.8):
    start = np.pi / 2 + np.radians(gapdeg)
    end = np.pi / 2 - np.radians(gapdeg) + 2 * np.pi
    ring = ParametricFunction(epoint, t_range=[start, end, 0.02], color=color, stroke_width=stroke)
    ring.shift(center)
    return ring

def gapmarks(center=ORIGIN, color=gold):
    a = epoint(np.pi / 2 + np.radians(gapdeg)) + center
    b = epoint(np.pi / 2 - np.radians(gapdeg)) + center
    return VGroup(Dot(a, radius=0.05, color=color), Dot(b, radius=0.05, color=color))

def topoint(x, y, center=ORIGIN):
    return np.array([x * scale, y * scale, 0.0]) + center

def normalreal(x, y):
    nx, ny = 4 * x, y
    n = math.hypot(nx, ny)
    return nx / n, ny / n

def tangentreal(x, y):
    nx, ny = normalreal(x, y)
    return -ny, nx

def nexthit(px, py, dx, dy):
    a = 4 * dx * dx + dy * dy
    b = 8 * px * dx + 2 * py * dy
    c = 4 * px * px + py * py - 100
    disc = b * b - 4 * a * c
    t1 = (-b + math.sqrt(disc)) / (2 * a)
    t2 = (-b - math.sqrt(disc)) / (2 * a)
    ts = [t for t in (t1, t2) if t > 1e-9]
    return px + max(ts) * dx, py + max(ts) * dy

def reflectvec(dx, dy, x, y):
    nx, ny = normalreal(x, y)
    dot = dx * nx + dy * ny
    return dx - 2 * dot * nx, dy - 2 * dot * ny

def runsim(exitcheck, maxiter=1500):
    px, py = 0.0, 10.1
    qx, qy = 1.4, -9.6
    dx, dy = qx - px, qy - py
    x, y = px, py
    pts = [(px, py)]
    n = 0
    for _ in range(maxiter):
        nx_, ny_ = nexthit(x, y, dx, dy)
        pts.append((nx_, ny_))
        if exitcheck(nx_, ny_):
            return n, pts
        n += 1
        dx, dy = reflectvec(dx, dy, nx_, ny_)
        x, y = nx_, ny_
    return None, pts

correcthits, correctpts = runsim(lambda x, y: -0.01 <= x <= 0.01 and y > 0)
grokhits, grokpts = runsim(lambda x, y: -0.01 <= x <= 0.01)

def pathmobject(pts, color=ink, stroke=1.7, center=ORIGIN, upto=None, frm=0, opacity=1.0):
    seq = pts[frm:upto + 1] if upto is not None else pts[frm:]
    coords = [topoint(x, y, center) for x, y in seq]
    vm = VMobject()
    vm.set_points_as_corners(coords)
    vm.set_stroke(color, stroke, opacity=opacity)
    return vm


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
    times = [0.0, 7.08, 14.71, 19.46, 23.98, 31.52]
    def construct(self):
        self.start()
        self.cue(0)
        ring = ellipsering(stroke=3.0)
        gm = gapmarks()
        self.play_(Create(ring), rt=1.2)
        self.play_(FadeIn(gm), rt=0.4)
        beam = pathmobject(correctpts, color=gold, stroke=2.4, upto=2)
        self.play_(Create(beam), rt=1.3)

        self.cue(1)
        fuller = pathmobject(correctpts, color=gold, stroke=1.9, upto=22)
        self.play_(Transform(beam, fuller), rt=3.2)
        flash = Dot(topoint(*correctpts[0]), radius=0.1, color=WHITE)
        self.play_(FadeIn(flash, scale=2.2), FadeOut(flash), rt=0.7)

        self.cue(2)
        self.play_(FadeOut(VGroup(ring, gm, beam)), rt=0.6)
        ttl = label("Project Euler 144", 34)
        ttl.move_to(UP * 0.7)
        self.play_(Write(ttl), rt=1.2)

        self.cue(3)
        sub = label("a real jump up in difficulty --- actual geometry now", 19, dim)
        sub.next_to(ttl, DOWN, buff=0.5)
        self.play_(Write(sub), rt=1.6)

        self.cue(4)
        self.play_(FadeOut(VGroup(ttl, sub)), rt=0.5)
        chips = VGroup(pill("Kimi K3", kimi), pill("Fable", fable),
                       pill("GPT-5.6 Sol", gpt), pill("Grok 4.5", grok)).arrange(RIGHT, buff=0.26)
        chips.scale(0.85).move_to(UP * 0.3)
        self.play_(FadeIn(chips, shift=UP * 0.2), rt=1.2)
        nohints = label("no hints", 18, dim)
        nohints.next_to(chips, DOWN, buff=0.55)
        self.play_(Write(nohints), rt=0.7)

        self.cue(5)
        self.play_(FadeOut(nohints), rt=0.3)
        twist = label("this time, the model that's been most reliable is the one that couldn't even finish", 18, gold)
        twist.next_to(chips, DOWN, buff=0.55)
        self.play_(Write(twist), rt=2.4)
        self.finish(35.50 + 1.3)


class sec2problem(base):
    times = [0.36, 11.21, 13.16, 18.16, 25.02, 33.16]
    def construct(self):
        self.start()
        self.cue(0)
        ttl = label("Problem 144 --- Multiple Reflections", 27)
        ttl.to_edge(UP, buff=0.5)
        self.play_(Write(ttl), rt=1.0)
        cen = DOWN * 0.25
        ring = ellipsering(center=cen, stroke=2.6)
        gm = gapmarks(center=cen)
        self.play_(Create(ring), rt=1.1)
        self.play_(FadeIn(gm), rt=0.4)
        beam = pathmobject(correctpts, color=gold, stroke=2.1, center=cen, upto=1)
        self.play_(Create(beam), rt=0.9)
        hitdot = Dot(topoint(*correctpts[1], center=cen), radius=0.06, color=gold)
        self.play_(FadeIn(hitdot), rt=0.35)

        self.cue(1)
        rule = label("every bounce follows one rule", 18, dim)
        rule.to_edge(DOWN, buff=0.9)
        self.play_(Write(rule), rt=1.1)

        self.cue(2)
        xh, yh = correctpts[1]
        tdx, tdy = tangentreal(xh, yh)
        tvec = np.array([tdx, tdy, 0.0])
        tanline = Line(hitdot.get_center() - tvec * 0.65, hitdot.get_center() + tvec * 0.65).set_stroke(kimi, 2.0)
        law = label("angle in = angle out", 19, gold)
        law.next_to(rule, UP, buff=0.4)
        self.play_(FadeOut(rule), rt=0.3)
        self.play_(Create(tanline), Write(law), rt=1.2)

        self.cue(3)
        self.play_(FadeOut(VGroup(law, tanline, hitdot)), rt=0.4)
        more = pathmobject(correctpts, color=gold, stroke=2.1, center=cen, upto=7)
        self.play_(Transform(beam, more), rt=1.7)
        bb = label("bounce, bounce, bounce", 18, ink)
        bb.to_edge(DOWN, buff=0.9)
        self.play_(FadeIn(bb), rt=0.9)
        slit = label("the slit is barely wide enough to matter", 16, dim)
        slit.next_to(bb, DOWN, buff=0.3)
        self.play_(FadeIn(slit), rt=1.1)

        self.cue(4)
        self.play_(FadeOut(VGroup(bb, slit)), rt=0.4)
        hard = label("simple to say --- hard to compute", 20, bad)
        hard.to_edge(DOWN, buff=0.9)
        self.play_(Write(hard), rt=1.4)
        errl = label("one wrong angle throws off every bounce after it", 16, dim)
        errl.next_to(hard, DOWN, buff=0.3)
        self.play_(FadeIn(errl), rt=1.3)

        self.cue(5)
        self.play_(FadeOut(VGroup(hard, errl)), rt=0.4)
        q = label("how many times does it hit the wall before it escapes?", 20, gold)
        q.to_edge(DOWN, buff=0.9)
        self.play_(Write(q), rt=1.8)
        self.finish(37.50 + 1.3)


class sec3gpt(base):
    times = [0.0, 5.65, 14.35]
    def construct(self):
        self.start()
        hdr = pill("GPT-5.6 Sol", gpt)
        hdr.to_corner(UL, buff=0.45)
        sub = label("vectors in, vectors out", 19, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        p0 = topoint(*correctpts[0])
        p1 = topoint(*correctpts[1])
        dot0 = Dot(p0, radius=0.07, color=gpt)
        arrow = Arrow(p0, p1, buff=0, stroke_width=3.2, color=gpt, max_tip_length_to_length_ratio=0.18)
        vlabel = label("position and direction, as vectors", 18, ink)
        vlabel.to_edge(DOWN, buff=0.8)
        self.play_(FadeIn(dot0), GrowArrow(arrow), rt=1.0)
        self.play_(Write(vlabel), rt=1.3)

        self.cue(1)
        self.play_(FadeOut(VGroup(dot0, arrow, vlabel)), rt=0.4)
        ring = ellipsering(stroke=2.6)
        gm = gapmarks()
        self.play_(Create(ring), FadeIn(gm), rt=1.0)
        fullpath = pathmobject(correctpts, color=gpt, stroke=1.5)
        self.play_(Create(fullpath), rt=6.4)

        self.cue(2)
        self.play_(FadeOut(gm), rt=0.001)
        n354 = label(f"{correcthits} bounces --- exactly right", 24, good)
        n354.to_edge(DOWN, buff=0.85)
        self.play_(Write(n354), rt=1.4)
        fastest = label("and the fastest solution here", 17, dim)
        fastest.next_to(n354, DOWN, buff=0.3)
        self.play_(FadeIn(fastest), rt=1.1)
        self.finish(24.17 + 1.3)


class sec4fable(base):
    times = [0.43, 14.52, 17.85, 22.93]
    def construct(self):
        self.start()
        hdr = pill("Fable", fable)
        hdr.to_corner(UL, buff=0.45)
        sub = label("same answer, different road", 19, dim)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        cen = DOWN * 0.3
        xh, yh = correctpts[1]
        hp = topoint(xh, yh, center=cen)
        tdx, tdy = tangentreal(xh, yh)
        tvec = np.array([tdx, tdy, 0.0])
        tanline = Line(hp - tvec * 0.8, hp + tvec * 0.8).set_stroke(gridcol, 2.0)
        inray = Line(topoint(*correctpts[0], center=cen), hp).set_stroke(fable, 2.4)
        thetalabel = label("@\\theta_{in}", 22, fable).next_to(hp, UP + LEFT, buff=0.35)
        formula = label("@\\theta_{out} = 2\\theta_{tan} - \\theta_{in}", 24, ink)
        formula.to_edge(DOWN, buff=0.9)
        self.play_(Create(tanline), Create(inray), rt=1.1)
        self.play_(Write(thetalabel), rt=0.8)
        self.play_(Write(formula), rt=1.6)

        self.cue(1)
        self.play_(FadeOut(VGroup(tanline, inray, thetalabel, formula)), rt=0.5)
        ring = ellipsering(center=cen, stroke=2.6)
        gm = gapmarks(center=cen)
        samepath = pathmobject(correctpts, color=fable, stroke=1.5, center=cen)
        self.play_(Create(ring), FadeIn(gm), rt=0.8)
        self.play_(Create(samepath), rt=2.0)
        routed = label("same physics, just routed through trig instead", 17, dim)
        routed.to_edge(DOWN, buff=0.85)
        self.play_(FadeIn(routed), rt=1.3)

        self.cue(2)
        self.play_(FadeOut(routed), rt=0.3)
        overhead = label("a little more work, every single bounce", 17, dim)
        overhead.to_edge(DOWN, buff=0.85)
        self.play_(Write(overhead), rt=1.2)

        self.cue(3)
        self.play_(FadeOut(overhead), rt=0.001)
        n354 = label(f"also {correcthits} --- just a bit more overhead", 22, good)
        n354.move_to(DOWN * 0.2)
        self.play_(Write(n354), rt=1.4)
        self.finish(22.93 + 1.3)


class sec5grok(base):
    times = [0.42, 6.38, 22.17, 29.81]
    def construct(self):
        self.start()
        hdr = pill("Grok 4.5", grok)
        hdr.to_corner(UL, buff=0.45)
        sub = label("physics is fine --- the exit check isn't", 19, bad)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        ring = ellipsering(stroke=2.6)
        gm = gapmarks()
        self.play_(Create(ring), FadeIn(gm), rt=1.0)
        gpath = pathmobject(grokpts, color=grok, stroke=1.6, upto=40)
        self.play_(Create(gpath), rt=2.0)
        fine = label("every reflection here is correct", 17, dim)
        fine.to_edge(DOWN, buff=0.85)
        self.play_(FadeIn(fine), rt=1.1)

        self.cue(1)
        self.play_(FadeOut(fine), rt=0.3)
        band = Rectangle(width=0.09, height=ay * 2.15, color=bad, fill_opacity=0.16, stroke_width=1.4, stroke_color=bad)
        band.move_to(ORIGIN)
        checktext = label("checks only how close to the middle --- left and right", 17, bad)
        checktext.to_edge(DOWN, buff=0.85)
        self.play_(FadeIn(band), rt=0.8)
        self.play_(Write(checktext), rt=1.6)
        self.play_(FadeOut(checktext), rt=0.3)
        nevertext = label("never whether that's the top, or the bottom", 17, bad)
        nevertext.to_edge(DOWN, buff=0.85)
        self.play_(Write(nevertext), rt=1.4)

        gfull = pathmobject(grokpts, color=grok, stroke=1.6)
        self.play_(Transform(gpath, gfull), rt=4.6)
        stoppoint = topoint(*grokpts[-1])
        ring2 = Circle(radius=0.14, color=bad, stroke_width=3.0).move_to(stoppoint)
        self.play_(FadeOut(nevertext), rt=0.3)
        self.play_(Create(ring2), rt=0.6)
        exitline = label(f"\"exit\" at bounce {grokhits} --- but that's the bottom", 17, bad)
        exitline.to_edge(DOWN, buff=0.85)
        self.play_(Write(exitline), rt=1.6)

        self.cue(2)
        self.play_(FadeOut(VGroup(exitline, band)), rt=0.3)
        ghost = pathmobject(correctpts, color=dim, stroke=1.3, frm=grokhits, opacity=0.55)
        realexit = label("the real exit was still 193 bounces away", 17, dim)
        realexit.to_edge(DOWN, buff=0.85)
        self.play_(Create(ghost), rt=1.8)
        self.play_(Write(realexit), rt=1.5)

        self.cue(3)
        self.play_(FadeOut(VGroup(ring, gm, gpath, ring2, ghost, realexit)), rt=0.001)
        wrong = label(f"{grokhits} instead of {correcthits}", 26, bad)
        wrong.move_to(DOWN * 0.2)
        self.play_(Write(wrong), rt=1.5)
        self.finish(33.90 + 1.3)


class sec6kimi(base):
    times = [0.4, 3.61, 17.15, 18.64, 23.46, 26.92]
    def construct(self):
        self.start()
        hdr = pill("Kimi K3", kimi)
        hdr.to_corner(UL, buff=0.45)
        sub = label("won last time --- this time, it never stops", 19, bad)
        sub.next_to(hdr, RIGHT, buff=0.4)
        self.play_(FadeIn(hdr, shift=DOWN * 0.2), Write(sub), rt=1.0)

        self.cue(0)
        samephys = label("same physics as everyone else", 18, ink)
        samephys.move_to(UP * 1.5)
        self.play_(Write(samephys), rt=1.1)

        self.cue(1)
        self.play_(FadeOut(samephys), rt=0.3)
        checka = label("@x = 0", 30, bad)
        checka.move_to(LEFT * 2.6 + UP * 0.3)
        labela = label("Kimi's check", 16, dim).next_to(checka, DOWN, buff=0.35)
        checkb = label("@-0.01 \\le x \\le 0.01", 30, good)
        checkb.move_to(RIGHT * 2.2 + UP * 0.3)
        labelb = label("what it needed", 16, dim).next_to(checkb, DOWN, buff=0.35)
        self.play_(Write(checka), FadeIn(labela), rt=1.0)
        self.play_(Write(checkb), FadeIn(labelb), rt=1.0)

        self.cue(2)
        self.play_(FadeOut(VGroup(checka, labela, checkb, labelb)), rt=0.5)
        livecap = label("the actual x-value at every near miss", 18, dim)
        livecap.to_edge(UP, buff=1.3)
        self.play_(Write(livecap), rt=1.2)

        self.cue(3)
        samples = [(161, 0.006073), (192, -0.003333), (354, -0.009849), (385, -0.00044)]
        readout = label(f"bounce {samples[0][0]}:  x = {samples[0][1]:+.6f}", 22, kimi, font=mono)
        readout.move_to(ORIGIN)
        self.play_(Write(readout), rt=0.9)

        self.cue(4)
        for bn, xv in samples[1:]:
            nextread = label(f"bounce {bn}:  x = {xv:+.6f}", 22, kimi, font=mono)
            nextread.move_to(ORIGIN)
            self.play_(Transform(readout, nextread), rt=0.75)
        neverzero = label("never, not once, exactly zero", 18, bad)
        neverzero.next_to(readout, DOWN, buff=0.6)
        self.play_(FadeIn(neverzero), rt=1.1)

        self.cue(5)
        self.play_(FadeOut(VGroup(livecap, readout, neverzero)), rt=0.001)
        forever = label("so it just keeps bouncing --- forever", 22, bad)
        forever.move_to(UP * 0.2)
        self.play_(Write(forever), rt=1.6)
        onecomp = label("one overly strict comparison, and that's enough", 17, dim)
        onecomp.next_to(forever, DOWN, buff=0.45)
        self.play_(FadeIn(onecomp), rt=1.4)
        self.finish(30.53 + 1.3)


class sec7eval(base):
    times = [0.0, 5.05, 11.33, 19.69]
    def construct(self):
        self.start()
        self.cue(0)
        ttl = label("Side by Side", 30)
        ttl.to_edge(UP, buff=0.55)
        self.play_(Write(ttl), rt=1.0)
        rows = [
            ("GPT-5.6 Sol", gpt, "vectors, directly", f"{correcthits} --- fast and clean", good),
            ("Fable", fable, "angles and trig", f"{correcthits} --- more overhead", good),
            ("Grok 4.5", grok, "checks x only", f"{grokhits} --- stopped too early", bad),
            ("Kimi K3", kimi, "checks for exact zero", "never stops", bad),
        ]
        cards = VGroup()
        for nm, col, meth, res, rc in rows:
            box = RoundedRectangle(corner_radius=0.1, width=10.8, height=0.92).set_fill(panel, 1).set_stroke(col, 1.6)
            nmlab = label(nm, 20, col).move_to(box.get_left() + RIGHT * 1.5)
            mlab = label(meth, 16, ink).move_to(box.get_center() + LEFT * 0.4)
            rlab = label(res, 16, rc).move_to(box.get_right() + LEFT * 1.9)
            cards.add(VGroup(box, nmlab, mlab, rlab))
        cards.arrange(DOWN, buff=0.26).move_to(DOWN * 0.15)

        self.cue(1)
        self.play_(FadeIn(cards[0], shift=RIGHT * 0.25), rt=0.75)
        self.play_(FadeIn(cards[1], shift=RIGHT * 0.25), rt=0.75)

        self.cue(2)
        self.play_(FadeIn(cards[2], shift=RIGHT * 0.25), rt=0.75)
        self.play_(FadeIn(cards[3], shift=RIGHT * 0.25), rt=0.75)
        summ = label("two right, one jumped the gun, one still running", 17, dim)
        summ.next_to(cards, DOWN, buff=0.4)
        self.play_(Write(summ), rt=1.6)
        self.finish(19.69 + 1.3)


class sec8verdict(base):
    times = [0.37, 9.25, 16.28, 22.49, 26.76, 31.1, 46.21]
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
        gf = pill("GPT-5.6 Sol", gpt, w=3.1, h=0.9, size=23)
        gf.move_to(focus)
        crown = Polygon([-0.4, 0, 0], [-0.24, 0.32, 0], [0, 0.06, 0], [0.24, 0.32, 0], [0.4, 0, 0]).set_fill(gold, 1).set_stroke(gold, 1).scale(0.85)
        crown.next_to(gf, UP, buff=0.12)
        self.play_(FadeIn(gf, shift=DOWN * 0.2), rt=0.6)
        self.play_(FadeIn(crown, shift=DOWN * 0.3), rt=0.5)

        self.cue(1)
        g1 = label("stuck to vectors, the entire way through", 16, gpt)
        g1.next_to(gf, DOWN, buff=0.45)
        self.play_(Write(g1), rt=1.1)
        note(0, "winner", gold)
        g2 = label("no detours --- the cleanest and the fastest", 16, ink)
        g2.next_to(g1, DOWN, buff=0.22)
        self.play_(Write(g2), rt=1.2)

        self.cue(2)
        self.play_(FadeOut(VGroup(gf, crown, g1, g2)), rt=0.4)
        ff = pill("Fable", fable, w=3.1, h=0.9, size=23)
        ff.move_to(focus)
        self.play_(FadeIn(ff, shift=DOWN * 0.2), rt=0.6)
        f1 = label("a really close second, honestly", 16, fable)
        f1.next_to(ff, DOWN, buff=0.45)
        self.play_(Write(f1), rt=1.0)
        note(1, "2nd, proven", fable)
        f2 = label("same correct answer, a bit more overhead per bounce", 16, ink)
        f2.next_to(f1, DOWN, buff=0.22)
        self.play_(Write(f2), rt=1.3)

        self.cue(3)
        self.play_(FadeOut(VGroup(ff, f1, f2)), rt=0.4)
        rf = pill("Grok 4.5", grok, w=3.1, h=0.9, size=23)
        rf.move_to(focus)
        self.play_(FadeIn(rf, shift=DOWN * 0.2), rt=0.6)
        r1 = label("the mistake wasn't the hard part", 16, grok)
        r1.next_to(rf, DOWN, buff=0.45)
        self.play_(Write(r1), rt=1.1)
        note(2, "wrong exit", bad)
        r2 = label("it only checked half of what it needed to", 16, ink)
        r2.next_to(r1, DOWN, buff=0.22)
        self.play_(Write(r2), rt=1.2)

        self.cue(4)
        self.play_(FadeOut(VGroup(rf, r1, r2)), rt=0.4)
        kf = pill("Kimi K3", kimi, w=3.1, h=0.9, size=23)
        kf.move_to(focus)
        self.play_(FadeIn(kf, shift=DOWN * 0.2), rt=0.6)
        k1 = label("last episode's winner, taken down by one comparison", 15, kimi)
        k1.next_to(kf, DOWN, buff=0.45)
        self.play_(Write(k1), rt=1.3)
        note(3, "never stops", bad)
        k2 = label("exact instead of close enough --- enough to run forever", 15, ink)
        k2.next_to(k1, DOWN, buff=0.22)
        self.play_(Write(k2), rt=1.4)

        self.cue(5)
        self.play_(FadeOut(VGroup(kf, k1, k2)), rt=0.4)
        fin1 = label("Project Euler 144", 20, dim)
        fin1.move_to(focus + UP * 0.6)
        fin2 = label(f"{correcthits}", 40, gold)
        fin2.next_to(fin1, DOWN, buff=0.35)
        fbox = SurroundingRectangle(fin2, buff=0.2).set_stroke(gold, 2)
        self.play_(FadeIn(fin1), rt=0.6)
        self.play_(Write(fin2), rt=1.0)
        self.play_(Create(fbox), rt=0.6)
        moral = label("sometimes the hard part isn't the physics", 16, dim)
        moral.to_edge(DOWN, buff=0.9)
        self.play_(Write(moral), rt=1.5)

        self.cue(6)
        self.play_(FadeOut(moral), rt=0.3)
        closing = label("same four next time --- probably a different winner too", 16, dim)
        closing.to_edge(DOWN, buff=0.9)
        self.play_(Write(closing), rt=1.6)
        self.finish(49.88 + 1.3)
