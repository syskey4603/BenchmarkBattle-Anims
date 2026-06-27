try:
    from manimlib import *
    MGL = True
except Exception:
    from manim import *
    MGL = False
    ShowCreation = Create

import numpy as np
import random
import re

if not MGL:
    config.background_color = "#0A0A15"

mono = "Consolas"

grok = "#FF4500"; gpt = "#10A37F"; gem = "#4285F4"; cld = "#E8925C"
gold = "#FFD700"; bad = "#FF5555"; good = "#4ADE80"
ink  = "#F2F3F7"; dim = "#FFB86C"; gridcol = "#2A3A5A"; panel = "#10141F"

answer = "4640261571849533"
zeroclue = "2321386104303845"
clues = [
    ("5616185650518293", 2),
    ("3847439647293047", 1),
    ("2321386104303845", 0),
    ("9742855507068353", 3),
    ("6913859173121360", 1),
]

def _latexify(s):
    s = s.replace("\\", " ")
    s = s.replace("%", r"\%").replace("&", r"\&").replace("#", r"\#")
    s = s.replace("_", r"\_")
    s = re.sub(r'"([^"]*)"', r"``\1''", s)
    s = s.replace("→", r"$\rightarrow$")
    s = s.replace("✓", r"$\checkmark$").replace("✗", r"$\times$")
    s = s.replace("×", r"$\times$").replace("≈", r"$\approx$")
    s = s.replace("·", r"$\cdot$").replace("≠", r"$\neq$")
    s = s.replace("<", r"$<$").replace(">", r"$>$")
    s = s.replace("—", "---")
    return s

def label(s, size=24, color=ink, font=None):
    if font:
        t = Text(s, font_size=size, font=font)
    else:
        t = Tex(_latexify(s), font_size=size)
    t.set_color(color)
    return t

def background():
    r = Rectangle(width=30, height=18, stroke_width=0)
    r.set_fill("#0A0A15", opacity=1)
    return r

def pill(name, col, w=2.4, h=0.74, size=23):
    box = RoundedRectangle(corner_radius=0.12, width=w, height=h)
    box.set_fill(panel, opacity=1).set_stroke(col, width=2)
    lab = label(name, size, col); lab.move_to(box)
    return VGroup(box, lab)

def tilerow(s, tile=0.46, buff=0.07, color=ink, boxcol=gridcol, fs=22):
    """Row of monospace digit tilerow (boxes). s may contain spaces (skipped)."""
    g = VGroup()
    for ch in s:
        if ch == " ":
            continue
        sq = Square(side_length=tile)
        sq.set_fill(panel, opacity=1).set_stroke(boxcol, width=1.2)
        t = label(ch, fs, color, font=mono); t.move_to(sq)
        g.add(VGroup(sq, t))
    g.arrange(RIGHT, buff=buff)
    return g

def digits(s, fs=22, color="#9FB6D4", buff=0.10):
    g = VGroup(*[label(ch, fs, color, font=mono) for ch in s if ch != " "])
    g.arrange(RIGHT, buff=buff)
    return g

def topbar(scene, name, col, sub):
    c = pill(name, col); c.to_corner(UL, buff=0.45)
    s = label(sub, 20, dim); s.next_to(c, RIGHT, buff=0.45)
    scene.play(FadeIn(c, shift=DOWN*0.2), Write(s), run_time=1.0)
    return VGroup(c, s)

class Base(Scene):
    """Base scene. Background only — no ambient particles. The explanation
    itself carries all motion."""
    def setup(self):
        super().setup()
        if MGL:
            self.add(background())

class Sec1_Intro(Base):
    def construct(self):
        ep = label("Episode 2", 26, dim); ep.to_edge(UP, buff=0.8)
        title = label("Four models. One problem.", 42)
        self.play(FadeIn(ep, shift=DOWN*0.2), run_time=1.46)
        self.play(Write(title), run_time=3.27)
        self.wait(1.36)

        chips = VGroup(pill("ChatGPT", gpt), pill("Gemini", gem),
                       pill("Grok", grok), pill("Claude", cld))
        chips.arrange(RIGHT, buff=0.34).shift(DOWN*0.2)
        self.play(title.animate.shift(UP*1.6).scale(0.62), run_time=1.27)
        for c in chips:
            self.play(FadeIn(c, shift=UP*0.3), run_time=1.27)

        conds = VGroup(label("same problem", 19, dim), label("same wording", 19, dim),
                       label("no hints", 19, dim)).arrange(RIGHT, buff=0.6)
        conds.next_to(chips, DOWN, buff=0.6)
        for c in conds:
            self.play(FadeIn(c, scale=1.15), run_time=1.09)
        self.wait(1.36)

        recap = label("last episode", 20, dim); recap.next_to(conds, DOWN, buff=0.7)
        self.play(FadeIn(recap), run_time=1.09)
        c_gpt = label("✓", 26, good).next_to(chips[0], UP, buff=0.15)
        c_gem = label("✓", 26, good).next_to(chips[1], UP, buff=0.15)
        c_cld = label("✓", 26, good).next_to(chips[3], UP, buff=0.15)
        x_grk = label("✗", 28, bad).next_to(chips[2], UP, buff=0.15)
        self.play(chips[2][0].animate.set_stroke(bad, 3), FadeIn(x_grk, scale=1.3),
                  run_time=1.46)
        self.play(LaggedStart(FadeIn(c_gpt, scale=1.2), FadeIn(c_gem, scale=1.2),
                              FadeIn(c_cld, scale=1.2), lag_ratio=0.25), run_time=2.18)
        self.wait(2.00)

        self.play(FadeOut(VGroup(c_gpt, c_gem, c_cld, x_grk)),
                  chips[2][0].animate.set_stroke(grok, 2),
                  FadeOut(recap), run_time=1.27)
        q = label("does the pattern hold?", 26, gold); q.next_to(conds, DOWN, buff=0.7)
        self.play(Write(q), run_time=2.55)
        self.wait(2.00)

        self.play(FadeOut(q), run_time=0.72)
        tag = label("one question --- four ways of thinking", 22, dim)
        tag.next_to(conds, DOWN, buff=0.7)
        self.play(chips[0].animate.shift(LEFT*0.3), chips[3].animate.shift(RIGHT*0.3),
                  run_time=1.09)
        self.play(Write(tag), run_time=2.91)
        self.wait(2.00)
        self.play(FadeOut(VGroup(ep, title, chips, conds, tag)), run_time=1.64)

class Sec2_Problem(Base):
    def construct(self):
        title = label("Problem 185 --- Number Mind", 30); title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.73)

        secret = tilerow("? ? ? ?", tile=0.6, color=dim, fs=28)
        secret.move_to(UP*1.6)
        slab = label("secret (hidden)", 16, dim); slab.next_to(secret, UP, buff=0.2)
        self.play(FadeIn(slab), LaggedStart(*[FadeIn(t, scale=0.7) for t in secret],
                  lag_ratio=0.1), run_time=1.73)
        guess = digits("3 9 1 4", fs=26, color=ink); guess.next_to(secret, DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(d, shift=UP*0.1) for d in guess],
                  lag_ratio=0.08), run_time=1.57)
        self.play(guess[0].animate.set_color(good), guess[2].animate.set_color(good),
                  run_time=1.04)
        cnt = label("2 in the right position", 18, good); cnt.next_to(guess, DOWN, buff=0.4)
        self.play(Write(cnt), run_time=1.73)
        self.wait(2.00)
        self.play(FadeOut(VGroup(secret, slab, guess, cnt)), run_time=0.87)

        board = tilerow("? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?", tile=0.42, color=dim, fs=18)
        board.scale(0.95).to_edge(UP, buff=1.3)
        blab = label("the 16-digit secret", 17, dim); blab.next_to(board, UP, buff=0.22)
        self.play(FadeIn(blab), LaggedStart(*[FadeIn(t) for t in board],
                  lag_ratio=0.03), run_time=2.08)
        clue_rows = VGroup()
        for gtext, c in clues[:3]:
            row = digits(gtext, fs=16, color="#9FB6D4")
            tag = label(f"{c}", 16, gem if c else bad)
            tagbox = VGroup(Square(0.34).set_stroke(gem if c else bad,1.4)
                            .set_fill(panel,1), tag)
            tag.move_to(tagbox[0])
            tagbox.next_to(row, RIGHT, buff=0.4)
            clue_rows.add(VGroup(row, tagbox))
        clue_rows.arrange(DOWN, buff=0.28).next_to(board, DOWN, buff=0.5)
        for r in clue_rows:
            self.play(FadeIn(r[0], shift=RIGHT*0.1), run_time=0.69)
            self.play(GrowFromCenter(r[1]), run_time=0.52)
        self.wait(1.75)

        emph = label("you get the count --- never which positions", 18, dim)
        emph.next_to(clue_rows, DOWN, buff=0.45)
        self.play(Write(emph),
                  *[Indicate(r[1], color=gold, scale_factor=1.25) for r in clue_rows],
                  run_time=2.78)
        self.wait(2.00)
        self.play(FadeOut(VGroup(clue_rows, emph, blab)), run_time=0.87)

        s1 = label("16 digits", 38, gold); s1.move_to(ORIGIN)
        self.play(board.animate.to_edge(UP, buff=1.0), run_time=0.87)
        self.play(Write(s1), run_time=1.39)
        s2 = label("$10^{16}$ combinations", 36, gold); s2.move_to(s1)
        self.play(ReplacementTransform(s1, s2), run_time=1.57)
        s3 = label("10 quadrillion --- far too many to try", 28, gold); s3.move_to(s2)
        self.play(ReplacementTransform(s2, s3), run_time=1.57)
        self.wait(2.00)
        self.play(FadeOut(s3), run_time=0.69)

        zc = digits(zeroclue, fs=22, color=bad); zc.move_to(UP*0.1)
        ztag = label("0 correct", 20, bad); ztag.next_to(zc, UP, buff=0.3)
        self.play(FadeIn(ztag), LaggedStart(*[FadeIn(d) for d in zc],
                  lag_ratio=0.03), run_time=1.73)
        strikes = VGroup()
        for d in zc:
            ln = Line(d.get_corner(DL), d.get_corner(UR)).set_stroke(bad, 3)
            strikes.add(ln)
        self.play(LaggedStart(*[ShowCreation(s) for s in strikes],
                  lag_ratio=0.06), run_time=2.78)
        fact = label("16 facts you know are false --- before searching at all", 18, dim)
        fact.next_to(zc, DOWN, buff=0.55)
        self.play(Write(fact), run_time=3.47)
        self.wait(2.00)
        self.play(FadeOut(VGroup(title, board, zc, ztag, strikes, fact)), run_time=1.57)

class Sec3_Grok(Base):
    def construct(self):
        hdr = topbar(self, "Grok", grok, "Simulated annealing --- borrowed from physics")

        axes_line = Line(LEFT*5, RIGHT*5).set_stroke(gridcol, 1.5).shift(DOWN*1.8)
        pts = [RIGHT*x + UP*(0.85*np.sin(x*1.15) - 0.10*x) for x in np.linspace(-4.6,4.6,90)]
        curve = VMobject().set_points_smoothly(pts).set_stroke("#3A4A66", 2.5).shift(DOWN*0.3)
        self.play(ShowCreation(curve), ShowCreation(axes_line), run_time=3.29)
        elab = label("error landscape --- we want the lowest point", 18, dim)
        elab.to_edge(DOWN, buff=0.7)
        self.play(FadeIn(elab), run_time=2.03)
        ball = Dot(radius=0.16, color=grok).move_to(pts[10] + DOWN*0.3)
        self.play(GrowFromCenter(ball), run_time=1.26)
        valley = min(range(len(pts)), key=lambda i: pts[i][1])
        for idx in [10, 24, 17, 34, 27, 45, 38, valley]:
            self.play(ball.animate.move_to(pts[idx] + DOWN*0.3), run_time=0.76)
        self.wait(2.00)
        self.play(FadeOut(VGroup(curve, axes_line, elab)),
                  ball.animate.to_corner(UL, buff=1.5).scale(0.85), run_time=1.78)

        guess = digits("8731950264817403", fs=20, color="#9FB6D4")
        guess.move_to(UP*1.5)
        glab = label("random 16-digit guess", 17, dim); glab.next_to(guess, UP, buff=0.25)
        self.play(FadeIn(glab), LaggedStart(*[FadeIn(d) for d in guess],
                  lag_ratio=0.02), run_time=2.54)
        meter = label("total error: 31", 24, grok); meter.next_to(guess, DOWN, buff=0.6)
        self.play(Write(meter), run_time=1.78)
        self.wait(2.00)

        for val, idx in [(27,3),(22,9),(18,12),(13,6)]:
            ch = str(random.randint(0,9))
            newt = label(ch, 20, grok, font=mono).move_to(guess[idx])
            self.play(Transform(guess[idx], newt), run_time=0.63)
            nm = label(f"total error: {val}", 24, grok).move_to(meter)
            self.play(Transform(meter, nm), guess[idx].animate.set_color("#9FB6D4"),
                      run_time=0.89)
        self.wait(1.62)

        stuck = label("stuck? --- a random jump to escape", 18, dim)
        stuck.next_to(meter, DOWN, buff=0.5)
        ji = random.randint(0,15)
        self.play(Write(stuck), Indicate(guess[ji], color=gold, scale_factor=1.7),
                  run_time=3.55)
        self.wait(2.00)

        self.play(FadeOut(stuck), run_time=0.76)
        creative = label("optimization, not deduction --- a different way of seeing it", 18, dim)
        creative.next_to(meter, DOWN, buff=0.5)
        self.play(Write(creative), run_time=5.07)
        self.wait(2.00)
        self.play(FadeOut(VGroup(guess, glab, meter, creative, ball)), run_time=1.26)

        seed = label("random.seed(42)", 30, grok, font=mono); seed.move_to(UP*1.0)
        box = SurroundingRectangle(seed, buff=0.2).set_stroke(bad, 2.5)
        self.play(Write(seed), run_time=2.28)
        self.play(ShowCreation(box), run_time=1.52)
        same = label("same seed --- same run --- same answer every time", 19, ink)
        same.next_to(box, DOWN, buff=0.5)
        self.play(Write(same), run_time=4.57)
        self.wait(2.00)
        chg = label("change the seed --- no guarantee it lands on the answer", 19, bad)
        chg.next_to(same, DOWN, buff=0.4)
        self.play(Write(chg), run_time=4.57)
        self.wait(2.00)
        lesson = label("a lucky run with a fixed seed --- not a real solution", 18, dim)
        lesson.next_to(chg, DOWN, buff=0.4)
        self.play(Write(lesson), run_time=4.57)
        self.wait(2.00)
        self.play(FadeOut(VGroup(hdr, seed, box, same, chg, lesson)), run_time=2.28)

class Sec4_ChatGPT(Base):
    def construct(self):
        hdr = topbar(self, "ChatGPT", gpt, "Recursive backtracking --- the direct approach")

        boxes = tilerow("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _", tile=0.44, color=dim, fs=18)
        boxes.scale(0.95).move_to(UP*1.5)
        cap = label("fill left to right, trying each digit", 18, dim)
        cap.next_to(boxes, UP, buff=0.3)
        self.play(FadeIn(cap), LaggedStart(*[FadeIn(b) for b in boxes],
                  lag_ratio=0.03), run_time=3.75)
        for i, ch in enumerate(answer[:6]):
            for tv in [str((int(ch)+4)%10), str((int(ch)+7)%10), ch]:
                tt = label(tv, 18, gpt, font=mono).move_to(boxes[i][1])
                self.play(Transform(boxes[i][1], tt), run_time=0.34)
            boxes[i][0].set_fill(gpt, opacity=0.3)
        self.wait(2.00)

        self.play(FadeOut(cap), run_time=0.86)
        clue = digits(clues[0][0], fs=18, color="#9FB6D4")
        clue.next_to(boxes, DOWN, buff=0.7)
        ctag = label("needs exactly 2", 17, gpt); ctag.next_to(clue, RIGHT, buff=0.4)
        self.play(FadeIn(clue, shift=RIGHT*0.1), Write(ctag), run_time=2.87)
        run = label("matched so far: 1", 19, gpt); run.next_to(clue, DOWN, buff=0.5)
        self.play(Write(run), run_time=2.01)
        self.wait(1.81)
        d1 = label("count exceeds target  →  dead branch", 17, bad)
        d2 = label("too few positions left  →  dead branch", 17, bad)
        deads = VGroup(d1, d2).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        deads.next_to(run, DOWN, buff=0.45)
        self.play(Write(d1), run_time=3.45)
        self.play(Write(d2), run_time=3.45)
        self.wait(2.00)
        self.play(FadeOut(VGroup(clue, ctag, run, deads)), run_time=1.15)

        trans = label("completely transparent", 26, gpt); trans.move_to(DOWN*0.2)
        self.play(Write(trans), run_time=3.45)
        sub = label("every decision visible --- straight from the problem statement", 17, dim)
        sub.next_to(trans, DOWN, buff=0.4)
        self.play(Write(sub), run_time=4.61)
        self.wait(2.00)

        rel = label("right answer every time --- nothing random", 19, good)
        rel.next_to(sub, DOWN, buff=0.45)
        self.play(Write(rel),
                  *[boxes[i][0].animate.set_stroke(good, 1.6) for i in range(6)],
                  run_time=4.61)
        self.wait(2.00)
        worth = label("reliable and readable --- that's worth something", 18, dim)
        worth.move_to(rel)
        self.play(FadeOut(rel), run_time=0.86)
        self.play(Write(worth), run_time=5.18)
        self.wait(2.00)
        self.play(FadeOut(VGroup(hdr, boxes, trans, sub, worth)), run_time=2.59)

class Sec5_Gemini(Base):
    def construct(self):
        hdr = topbar(self, "Gemini", gem, "Smarter backtracking --- two upgrades")

        up1 = pill("1   zero-clue elimination", gem, w=5.4, h=0.8, size=21)
        up2 = pill("2   precomputed lookahead", gem, w=5.4, h=0.8, size=21)
        ups = VGroup(up1, up2).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        self.play(FadeIn(up1, shift=RIGHT*0.3), run_time=2.00)
        self.play(FadeIn(up2, shift=RIGHT*0.3), run_time=2.00)
        self.wait(2.00)
        self.play(up2.animate.set_opacity(0.3), up1.animate.to_edge(UP, buff=1.3),
                  run_time=2.00)
        self.play(FadeOut(up2), run_time=0.86)

        zc = digits(zeroclue, fs=22, color=bad); zc.move_to(UP*0.3)
        ztag = label("0 correct", 18, bad); ztag.next_to(zc, UP, buff=0.25)
        self.play(FadeIn(ztag), LaggedStart(*[FadeIn(d) for d in zc],
                  lag_ratio=0.03), run_time=2.85)
        strikes = VGroup(*[Line(d.get_corner(DL), d.get_corner(UR)).set_stroke(bad,3)
                           for d in zc])
        self.play(LaggedStart(*[ShowCreation(s) for s in strikes],
                  lag_ratio=0.05), run_time=4.28)
        elim = label("16 digits ruled out before the search even starts", 18, dim)
        elim.next_to(zc, DOWN, buff=0.55)
        self.play(Write(elim), run_time=5.69)
        self.wait(2.00)
        self.play(FadeOut(VGroup(zc, ztag, strikes, elim, up1)), run_time=1.43)

        mf = label("max_future --- best each clue can still reach", 20, gem)
        mf.to_edge(UP, buff=1.3)
        self.play(Write(mf), run_time=4.55)
        rows, cols, cell = 4, 8, 0.6
        grid = VGroup(); cellmap = {}
        random.seed(2)
        for r in range(rows):
            for c in range(cols):
                sq = Square(cell).set_fill("#121728",1).set_stroke("#2A3450",0.6)
                val = max(0, 3 - (c//3) - random.randint(0,1))
                t = label(str(val), 15, "#9FB6D4", font=mono); t.move_to(sq)
                cg = VGroup(sq,t)
                cg.move_to(RIGHT*(c-(cols-1)/2)*(cell+0.06)+UP*((rows-1)/2-r)*(cell+0.06))
                cg.shift(DOWN*0.3); grid.add(cg); cellmap[(r,c)] = cg
        for r in range(rows):
            self.play(LaggedStart(*[FadeIn(cellmap[(r,c)], scale=0.8) for c in range(cols)],
                      lag_ratio=0.05), run_time=1.71)
        self.wait(2.00)

        dist1 = label("not: are there enough positions left?", 18, dim)
        dist2 = label("but: enough where the digit is still possible?", 18, gem)
        dist = VGroup(dist1, dist2).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        dist.next_to(grid, DOWN, buff=0.5)
        self.play(Write(dist1), run_time=4.28)
        self.play(Write(dist2),
                  *[cellmap[(1,c)][0].animate.set_stroke(gem,1.6) for c in range(cols)],
                  run_time=4.55)
        self.wait(2.00)
        self.play(FadeOut(VGroup(mf, grid, dist)), run_time=1.43)

        res = label("far fewer dead ends --- a much smaller search", 22, good)
        res.move_to(UP*0.3)
        self.play(Write(res), run_time=5.12)
        fore = label("same approach as ChatGPT --- with real foresight", 18, dim)
        fore.next_to(res, DOWN, buff=0.45)
        self.play(Write(fore), run_time=5.69)
        self.wait(2.00)
        self.play(FadeOut(VGroup(hdr, res, fore)), run_time=2.57)

class Sec6_Claude(Base):
    def construct(self):
        hdr = topbar(self, "Claude", cld, "Constraint satisfaction --- model it, then solve")

        frame = label("find 16 digits so all 22 counts match exactly", 22)
        frame.move_to(UP*1.8)
        self.play(Write(frame), run_time=4.94)
        self.wait(2.00)
        csp = label("a constraint satisfaction problem", 26, cld)
        csp.next_to(frame, DOWN, buff=0.5)
        self.play(Write(csp), run_time=3.95)
        self.wait(2.00)
        self.play(FadeOut(frame), csp.animate.to_edge(UP, buff=1.2), run_time=1.48)

        vb = tilerow("x x x x x x x x x x x x x x x x", tile=0.42, color=cld, fs=18)
        vb.scale(0.95).move_to(UP*0.5)
        vlab = label("16 variables  ·  each 0--9", 17, dim); vlab.next_to(vb, UP, buff=0.3)
        self.play(FadeIn(vlab), LaggedStart(*[FadeIn(b, scale=0.8) for b in vb],
                  lag_ratio=0.03), run_time=3.45)
        self.wait(2.00)

        cons = VGroup()
        for gtext, c in clues[:3]:
            cons.add(label(f"matches({gtext[:8]}...) = {c}", 17, "#9FB6D4", font=mono))
        cons.arrange(DOWN, buff=0.22).next_to(vb, DOWN, buff=0.55)
        for line in cons:
            self.play(FadeIn(line, shift=RIGHT*0.1), run_time=1.12)
        more = label("...and 19 more", 16, dim); more.next_to(cons, DOWN, buff=0.25)
        self.play(FadeIn(more), run_time=1.23)
        self.wait(2.00)

        self.play(FadeOut(VGroup(cons, more, vlab)), run_time=0.99)
        solver = pill("OR-Tools", cld, w=3.6, h=1.0, size=28)
        solver.next_to(vb, DOWN, buff=0.8)
        slab = label("Google's industrial constraint solver", 16, dim)
        slab.next_to(solver, DOWN, buff=0.3)
        arr = Arrow(vb.get_bottom(), solver.get_top(), buff=0.15, stroke_width=3, color=cld)
        self.play(GrowArrow(arr), FadeIn(solver, shift=UP*0.2), run_time=2.22)
        self.play(FadeIn(slab), run_time=1.23)
        self.wait(2.00)

        prop = label("constraint propagation eliminates values fast", 17, dim)
        prop.next_to(slab, DOWN, buff=0.4)
        self.play(Write(prop), run_time=3.95)
        self.play(solver[0].animate.set_stroke(gold, 3.5), run_time=0.99)
        self.play(solver[0].animate.set_stroke(cld, 2), run_time=0.99)
        self.wait(1.71)

        self.play(FadeOut(prop), run_time=0.74)
        ans = digits(answer, fs=24, color=good); ans.next_to(solver, DOWN, buff=0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=0.7) for d in ans],
                  lag_ratio=0.04), run_time=2.97)
        ms = label("100 ms", 24, gold); ms.next_to(ans, DOWN, buff=0.3)
        self.play(Write(ms), run_time=1.73)
        self.wait(2.00)

        self.play(FadeOut(VGroup(vb, arr, solver, slab, ans, ms)), run_time=1.23)
        ins = label("recognize the shape --- reach for the right tool", 22, cld)
        ins.move_to(UP*0.2)
        self.play(Write(ins), run_time=4.94)
        last = label("the same instinct Gemini used with scipy last time", 18, dim)
        last.next_to(ins, DOWN, buff=0.4)
        self.play(Write(last), run_time=4.94)
        self.wait(2.00)
        self.play(FadeOut(VGroup(hdr, csp, ins, last)), run_time=2.22)

class Sec7_Eval(Base):
    def construct(self):
        title = label("Side by Side", 30); title.to_edge(UP, buff=0.55)
        self.play(Write(title), run_time=5.72)

        rows = [
            ("Grok", grok, "simulated annealing", "needs seed 42", bad),
            ("ChatGPT", gpt, "backtracking", "reliable, clear", good),
            ("Gemini", gem, "elim + lookahead", "tighter search", good),
            ("Claude", cld, "CSP + OR-Tools", "100 ms", gold),
        ]
        cards = VGroup()
        for nm, col, method, note, ncol in rows:
            box = RoundedRectangle(corner_radius=0.1, width=10.2, height=0.92)
            box.set_fill(panel,1).set_stroke(col,1.6)
            name = label(nm, 22, col); name.move_to(box.get_left()+RIGHT*1.25)
            meth = label(method, 18, ink); meth.move_to(box.get_center()+LEFT*0.2)
            nt = label(note, 17, ncol); nt.move_to(box.get_right()+LEFT*1.6)
            cards.add(VGroup(box, name, meth, nt))
        cards.arrange(DOWN, buff=0.28).move_to(DOWN*0.15)

        waits = [1.3, 1.3, 1.5, 2.2]
        for i, card in enumerate(cards):
            self.play(FadeIn(card, shift=RIGHT*0.25), run_time=4.01)
            self.wait(waits[i])

        checks = VGroup(*[label("✓", 22, good).next_to(c[0], LEFT, buff=0.15) for c in cards])
        self.play(LaggedStart(*[FadeIn(x, scale=1.3) for x in checks],
                  lag_ratio=0.1), run_time=5.72)
        ans = digits(answer, fs=24, color=good); ans.next_to(cards, DOWN, buff=0.5)
        alab = label("all four reached it", 17, dim); alab.next_to(ans, UP, buff=0.2)
        self.play(FadeIn(alab), LaggedStart(*[FadeIn(d, scale=0.7) for d in ans],
                  lag_ratio=0.03), run_time=6.85)
        self.wait(2.00)

        star = label("* Grok only with seed 42", 16, bad); star.next_to(ans, DOWN, buff=0.3)
        self.play(checks[0].animate.set_color(bad), FadeIn(star), run_time=4.57)
        self.wait(2.00)
        self.play(FadeOut(VGroup(title, cards, checks, ans, alab, star)), run_time=5.14)

class Sec8_Verdict(Base):
    def construct(self):
        head = label("The Verdict", 32); head.to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=3.51)

        names = ["Claude", "Gemini", "ChatGPT", "Grok"]
        cols = {"Claude":cld, "Gemini":gem, "ChatGPT":gpt, "Grok":grok}
        rows = VGroup()
        for nm in names:
            box = RoundedRectangle(corner_radius=0.08, width=4.4, height=0.78)
            box.set_fill(panel,1).set_stroke("#2A3450",1.2)
            lab = label(nm, 20, cols[nm]); lab.move_to(box.get_left()+RIGHT*0.95)
            verdict = label("", 16, dim)
            rows.add(VGroup(box, lab, verdict))
        rows.arrange(DOWN, buff=0.22).to_edge(RIGHT, buff=0.6)
        self.play(LaggedStart(*[FadeIn(r[0]) for r in rows],
                  *[FadeIn(r[1]) for r in rows], lag_ratio=0.05), run_time=4.20)

        def set_note(i, text, col):
            nt = label(text, 15, col)
            nt.move_to(rows[i][0].get_right()+LEFT*1.45)
            self.play(FadeIn(nt, shift=LEFT*0.15), run_time=2.11)
            rows[i][2] = nt
            return nt

        focus_pos = LEFT*3.2 + UP*0.3

        cfoc = pill("Claude", cld, w=2.8, h=0.9, size=26); cfoc.move_to(focus_pos)
        self.play(FadeIn(cfoc, shift=DOWN*0.2), run_time=2.46)
        cfast = label("100 ms", 30, gold); cfast.next_to(cfoc, DOWN, buff=0.4)
        self.play(Write(cfast), run_time=3.51)
        self.wait(2.00)
        cwhy = label("model it right,\nuse the right solver", 17, dim)
        cwhy.next_to(cfast, DOWN, buff=0.4)
        self.play(FadeIn(cwhy), run_time=3.51)
        set_note(0, "fastest", gold)
        self.wait(2.00)
        self.play(FadeOut(VGroup(cfoc, cfast, cwhy)), run_time=1.75)

        gfoc = pill("Gemini", gem, w=2.8, h=0.9, size=26); gfoc.move_to(focus_pos)
        self.play(FadeIn(gfoc, shift=DOWN*0.2), run_time=2.46)
        crown = Polygon([-0.4,0,0],[-0.24,0.32,0],[0,0.06,0],[0.24,0.32,0],[0.4,0,0])
        crown.set_fill(gold,1).set_stroke(gold,1).scale(0.85)
        crown.next_to(gfoc, UP, buff=0.12).shift(UP*1.3).set_opacity(0)
        self.add(crown)
        self.play(crown.animate.shift(DOWN*1.3).set_opacity(1), run_time=2.80)
        gp = VGroup(
            label("the lookahead isn't obvious", 17, ink),
            label("most stop at backtrack + check", 17, dim),
            label("Gemini built a tighter bound", 17, ink),
            label("cutting branches early", 17, gem),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        gp.next_to(gfoc, DOWN, buff=0.45)
        for p in gp:
            self.play(Write(p), run_time=4.91)
            self.wait(1.49)
        set_note(1, "true credit", gold)
        algo = label("real algorithmic thinking", 17, good); algo.next_to(gp, DOWN, buff=0.35)
        self.play(Write(algo), run_time=5.60)
        self.wait(2.00)
        self.play(FadeOut(VGroup(gfoc, crown, gp, algo)), run_time=1.75)

        pfoc = pill("ChatGPT", gpt, w=2.8, h=0.9, size=26); pfoc.move_to(focus_pos)
        self.play(FadeIn(pfoc, shift=DOWN*0.2), run_time=2.46)
        pp = VGroup(
            label("the clear, direct version", 17, ink),
            label("nothing wrong --- it's correct", 17, dim),
            label("just not the fastest", 17, dim),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        pp.next_to(pfoc, DOWN, buff=0.45)
        for p in pp:
            self.play(Write(p), run_time=4.91)
            self.wait(1.49)
        set_note(2, "correct, slower", ink)
        self.wait(2.00)
        self.play(FadeOut(VGroup(pfoc, pp)), run_time=1.75)

        rfoc = pill("Grok", grok, w=2.8, h=0.9, size=26); rfoc.move_to(focus_pos)
        self.play(FadeIn(rfoc, shift=DOWN*0.2), run_time=2.46)
        rp = VGroup(
            label("annealing is genuinely clever", 17, ink),
            label("great for huge, hard problems", 17, dim),
            label("but here a unique answer", 17, ink),
            label("backtracking nails in seconds", 17, dim),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        rp.next_to(rfoc, DOWN, buff=0.4)
        for p in rp:
            self.play(Write(p), run_time=4.55)
            self.wait(1.20)
        set_note(3, "wrong fit", bad)
        seedn = label("correct with seed 42 --- not in general", 16, bad)
        seedn.next_to(rp, DOWN, buff=0.35)
        self.play(Write(seedn), run_time=6.31)
        self.wait(2.00)
        self.play(FadeOut(VGroup(rfoc, rp, seedn)), run_time=1.75)

        fin1 = label("Project Euler 185", 22, dim); fin1.move_to(LEFT*3.2 + UP*0.6)
        fin2 = digits(answer, fs=30, color=gold); fin2.next_to(fin1, DOWN, buff=0.4)
        self.play(FadeIn(fin1), run_time=2.46)
        self.play(LaggedStart(*[FadeIn(d, scale=0.7) for d in fin2],
                  lag_ratio=0.04), run_time=5.60)
        fbox = SurroundingRectangle(fin2, buff=0.2).set_stroke(gold,2)
        self.play(ShowCreation(fbox), run_time=2.80)
        self.wait(2.00)

        outro = label("same four models --- different problem --- next time", 18, dim)
        outro.to_edge(DOWN, buff=0.7)
        self.play(Write(outro), run_time=7.71)
        self.wait(2.00)
        self.play(FadeOut(VGroup(head, rows, fin1, fin2, fbox, outro)), run_time=3.51)
