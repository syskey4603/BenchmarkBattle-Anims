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

DEMO = [[7,53,183,439,863],[627,343,773,959,943],[447,283,463,29,23],
        [217,623,3,399,853],[960,376,682,962,300]]
N = 5; CS = 0.72; GAP = 0.05
GREEDY = [(4,3,962),(1,4,943),(3,1,623),(2,2,463),(0,0,7)]
OPTPATH = [(0,4,863),(1,3,959),(2,2,463),(3,1,623),(4,0,960)]
FULL = 13938; GREEDY_FULL = 13070

def _latexify(s):
    s = s.replace("\\", " ")
    s = s.replace("%", r"\%").replace("&", r"\&").replace("#", r"\#")
    s = re.sub(r'"([^"]*)"', r"``\1''", s)
    s = s.replace("2¹⁵", r"$2^{15}$")
    s = s.replace("n³", r"$n^3$").replace("n²", r"$n^2$")
    s = s.replace("→", r"$\rightarrow$")
    s = s.replace("✓", r"$\checkmark$").replace("✗", r"$\times$")
    s = s.replace("×", r"$\times$").replace("≈", r"$\approx$")
    s = s.replace("·", r"$\cdot$")
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

def cellcol(v):
    if v < 100:  return "#161B2E"
    if v < 400:  return "#1A2540"
    if v < 700:  return "#1E3356"
    return "#22456E"

def grid_group(data=None):
    if data is None: data = DEMO
    n = len(data); g = VGroup()
    for r in range(n):
        for c in range(n):
            v = data[r][c]
            sq = Square(side_length=CS)
            sq.set_fill(cellcol(v), opacity=1).set_stroke(gridcol, width=1)
            sq.move_to(RIGHT*(c-(n-1)/2)*(CS+GAP) + UP*((n-1)/2-r)*(CS+GAP))
            t = label(str(v), 13, "#9FB6D4", font=mono); t.move_to(sq)
            g.add(VGroup(sq, t))
    return g

def topbar(scene, name, col, sub):
    c = pill(name, col); c.to_corner(UL, buff=0.45)
    s = label(sub, 20, dim); s.next_to(c, RIGHT, buff=0.45)
    scene.play(FadeIn(c, shift=DOWN*0.2), Write(s), run_time=1.1)
    return VGroup(c, s)

class Sec1_Intro(Scene):
    def construct(self):
        if MGL: self.add(background())
        random.seed(3)
        nums = VGroup()
        for r in range(8):
            for c in range(15):
                t = label(str(random.randint(1, 999)), 13, "#22304A", font=mono)
                t.move_to(RIGHT*(c-7)*1.12 + UP*(3.3 - r*0.95))
                nums.add(t)
        nums.set_opacity(0.5)
        nums.add_updater(lambda m, dt: m.shift(RIGHT*dt*0.06))
        self.add(nums)

        l1 = label("Four AI models.", 46)
        self.play(Write(l1), run_time=1.3)
        self.wait(2.64)

        chips = VGroup(pill("ChatGPT", gpt), pill("Gemini", gem),
                       pill("Grok", grok), pill("Claude", cld))
        chips.arrange(RIGHT, buff=0.34).shift(DOWN*0.1)
        self.play(l1.animate.to_edge(UP, buff=0.9).scale(0.7), run_time=0.7)
        for c in chips:
            self.play(FadeIn(c, shift=UP*0.25), run_time=0.7)
        self.wait(2.26)

        same = label("same problem  ·  same wording  ·  no hints", 22, dim)
        same.next_to(chips, DOWN, buff=0.7)
        self.play(Write(same), run_time=1.4)
        self.wait(3.77)

        self.play(FadeOut(same), FadeOut(l1), run_time=0.6)
        pe = label("Project Euler", 40)
        pe_sub = label("hundreds of math + programming problems", 20, dim)
        pe_sub2 = label("that get harder the deeper you go", 20, dim)
        peg = VGroup(pe, pe_sub, pe_sub2).arrange(DOWN, buff=0.3)
        peg.shift(UP*1.4)
        self.play(chips.animate.shift(DOWN*1.2).scale(0.85), run_time=0.7)
        self.play(Write(pe), run_time=0.9)
        self.play(FadeIn(pe_sub, shift=UP*0.15), run_time=1.0)
        self.wait(2.64)
        self.play(FadeIn(pe_sub2, shift=UP*0.15), run_time=1.0)
        self.wait(4.15)

        self.play(FadeOut(peg), run_time=0.5)
        prompt = label("not just who's right --- how they think", 26)
        prompt.shift(UP*1.5)
        self.play(Write(prompt), run_time=1.6)
        axes = VGroup(pill("efficiency", gem, w=2.6),
                      pill("accuracy", good, w=2.6),
                      pill("clarity", cld, w=2.6))
        axes.arrange(RIGHT, buff=0.4).next_to(prompt, DOWN, buff=0.7)
        for a in axes:
            self.play(GrowFromCenter(a), run_time=0.6)
        self.wait(0.94)
        self.play(LaggedStart(*[a.animate.scale(1.06) for a in axes],
                              lag_ratio=0.15), run_time=0.9)
        self.play(LaggedStart(*[a.animate.scale(1/1.06) for a in axes],
                              lag_ratio=0.15), run_time=0.9)
        self.wait(1.89)
        nums.clear_updaters()
        self.play(FadeOut(VGroup(nums, chips, prompt, axes)), run_time=0.9)

class Sec2_Problem(Scene):
    def construct(self):
        if MGL: self.add(background())
        title = label("Problem 345 --- Matrix Sum", 30)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.0)

        cells = grid_group(); cells.shift(LEFT*2.9 + DOWN*0.3)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cells],
                              lag_ratio=0.012), run_time=1.6)

        r1 = label("one pick per row", 22); 
        r2 = label("no two share a column", 22)
        rules = VGroup(r1, r2).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        rules.to_edge(RIGHT, buff=0.7).shift(UP*1.6)
        self.play(Write(r1), run_time=1.3)
        self.wait(1.30)
        self.play(Write(r2), run_time=1.6)
        self.wait(2.16)

        marks = VGroup()
        for (r, c, v) in OPTPATH:
            d = Dot(radius=0.13); d.set_fill(gold, opacity=0.95)
            d.move_to(cells[r*N+c].get_center())
            marks.add(d)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in marks],
                              lag_ratio=0.18), run_time=2.0)
        self.wait(2.16)

        rook = label("15 rooks, none attacking", 19, dim)
        rook.next_to(rules, DOWN, buff=0.6, aligned_edge=LEFT)
        self.play(FadeIn(rook), run_time=0.8)
        for (r, c, v) in OPTPATH:
            rl = Rectangle(width=N*(CS+GAP)-GAP, height=CS)
            rl.set_fill(gem, opacity=0.10).set_stroke(gem, width=1)
            rl.move_to([cells[2*N+2].get_center()[0], cells[r*N].get_center()[1], 0])
            cl = Rectangle(width=CS, height=N*(CS+GAP)-GAP)
            cl.set_fill(gpt, opacity=0.10).set_stroke(gpt, width=1)
            cl.move_to([cells[c].get_center()[0], cells[2*N+2].get_center()[1], 0])
            self.play(FadeIn(rl), FadeIn(cl), run_time=0.18)
            self.play(FadeOut(rl), FadeOut(cl), run_time=0.18)
        self.wait(1.73)

        goal = label("maximize the total", 26, gold)
        goal.next_to(rook, DOWN, buff=0.55, aligned_edge=LEFT)
        self.play(Write(goal), run_time=1.2)
        run = 0
        sumtxt = label("sum: 0", 22, gold); sumtxt.to_corner(DR, buff=0.6)
        self.add(sumtxt)
        for i, (r, c, v) in enumerate(OPTPATH):
            self.play(Indicate(marks[i], color=gold, scale_factor=1.5),
                      run_time=0.3)
            run += v
            nt = label(f"sum: {run}", 22, gold); nt.move_to(sumtxt)
            self.play(Transform(sumtxt, nt), run_time=0.2)
        self.wait(2.60)

        self.play(FadeOut(marks), FadeOut(sumtxt), run_time=0.4)
        instinct = label('"just take the biggest" --- maybe not', 21, dim)
        instinct.next_to(goal, DOWN, buff=0.55, aligned_edge=LEFT)
        self.play(Write(instinct), run_time=1.6)
        self.wait(4.33)

        self.play(FadeOut(VGroup(rules, rook, goal, instinct)), run_time=0.5)
        self.play(cells.animate.scale(0.8).shift(LEFT*0.3+UP*0.2), run_time=0.6)
        f1 = label("15!", 54, gold); f1.shift(RIGHT*2.6 + DOWN*0.2)
        self.play(Write(f1), run_time=1.0)
        self.wait(2.16)
        f2 = label("1,307,674,368,000", 40, gold); f2.move_to(f1)
        self.play(ReplacementTransform(f1, f2), run_time=1.0)
        self.wait(2.16)
        f3 = label("≈ 1.3 trillion ways", 34, gold); f3.move_to(f2)
        self.play(ReplacementTransform(f2, f3), run_time=1.0)
        self.wait(3.03)

        strat = label("can't check them all --- need a strategy", 22, ink)
        strat.next_to(f3, DOWN, buff=0.5)
        self.play(Write(strat), run_time=1.8)
        self.wait(5.19)
        self.play(FadeOut(VGroup(title, cells, f3, strat)), run_time=0.9)

class Sec3_Grok(Scene):
    def construct(self):
        if MGL: self.add(background())
        hdr = topbar(self, "Grok", grok, "Greedy --- biggest available, block, repeat")

        cells = grid_group(); cells.shift(LEFT*2.2 + DOWN*0.45)
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.012),
                  run_time=1.2)

        rule = VGroup(label("1. find the max", 19, dim),
                      label("2. take it", 19, dim),
                      label("3. block its row + col", 19, dim),
                      label("4. repeat 15x", 19, dim)
                      ).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
        rule.to_edge(RIGHT, buff=0.7).shift(UP*0.8)
        for r in rule:
            self.play(FadeIn(r, shift=LEFT*0.15), run_time=0.55)
        self.wait(4.59)

        total_txt = label("total: 0", 26, grok); total_txt.to_corner(DR, buff=0.6)
        self.add(total_txt)
        total = 0; used_r, used_c = set(), set()
        say = ["962", "943", "623", "463", "7"]

        for i, (r, c, v) in enumerate(GREEDY):
            dims = []
            for rr in range(N):
                for cc in range(N):
                    if rr in used_r or cc in used_c:
                        dims.append(cells[rr*N+cc][0].animate
                                    .set_fill("#0D0F18", opacity=0.55)
                                    .set_stroke("#141826", width=0.5))
            if dims: self.play(*dims, run_time=0.3)
            idx = r*N + c
            self.play(cells[idx][0].animate.set_fill(grok, opacity=0.92)
                      .set_stroke(grok, width=2.5), run_time=0.4)
            self.play(Flash(cells[idx].get_center(), color=grok,
                            line_length=0.16, num_lines=8, flash_radius=0.4),
                      run_time=0.3)
            total += v
            nt = label(f"total: {total}", 26, grok); nt.move_to(total_txt)
            self.play(Transform(total_txt, nt), run_time=0.25)
            self.wait(0.55 if i < 3 else 0.3)

        self.wait(2.62)

        self.play(FadeOut(rule), run_time=0.4)
        res1 = label("Grok: 13070", 30, bad)
        res1.to_edge(RIGHT, buff=0.9).shift(UP*0.8)
        self.play(Write(res1), run_time=1.0)
        self.wait(3.93)

        res2 = label("correct: 13938", 30, good)
        res2.next_to(res1, DOWN, buff=0.35, aligned_edge=RIGHT)
        self.play(Write(res2), run_time=1.0)
        gap = label("off by 868", 24, "#FF9999")
        gap.next_to(res2, DOWN, buff=0.3, aligned_edge=RIGHT)
        self.play(FadeIn(gap, shift=UP*0.15), run_time=0.7)
        self.wait(5.25)

        self.play(cells[4*N+3][0].animate.set_fill(grok, opacity=1)
                  .set_stroke(gold, width=3), run_time=0.5)
        rl = Rectangle(width=N*(CS+GAP)-GAP, height=CS)
        rl.set_fill(bad, opacity=0.15).set_stroke(bad, width=1.5)
        rl.move_to([cells[2*N+2].get_center()[0], cells[4*N].get_center()[1], 0])
        cl = Rectangle(width=CS, height=N*(CS+GAP)-GAP)
        cl.set_fill(bad, opacity=0.15).set_stroke(bad, width=1.5)
        cl.move_to([cells[3].get_center()[0], cells[2*N+2].get_center()[1], 0])
        self.play(FadeIn(rl), FadeIn(cl), run_time=0.8)
        self.wait(4.59)

        lockmsg = label("locked cells were needed elsewhere", 19, dim)
        lockmsg.to_edge(DOWN, buff=1.3)
        self.play(FadeIn(lockmsg), run_time=1.0)
        self.wait(6.56)
        self.play(FadeOut(rl), FadeOut(cl), FadeOut(lockmsg), run_time=0.5)

        lesson = label("local best  $\\neq$  global best", 28, ink)
        lesson.to_edge(DOWN, buff=1.2)
        self.play(Write(lesson), run_time=1.8)
        self.wait(6.56)

        self.play(FadeOut(lesson), run_time=0.4)
        fast = label("fastest today --- 0.1 ms --- and it's wrong", 20, dim)
        fast.to_edge(DOWN, buff=1.2)
        self.play(Write(fast), run_time=1.8)
        stamp = label("WRONG", 44, bad); stamp.rotate(PI/14)
        stamp.move_to(cells.get_center())
        box = SurroundingRectangle(stamp, buff=0.18); box.set_stroke(bad, 3)
        wrong = VGroup(stamp, box)
        self.play(GrowFromCenter(wrong), run_time=0.5)
        for _ in range(2):
            self.play(wrong.animate.set_color(ink), run_time=0.18)
            self.play(wrong.animate.set_color(bad), run_time=0.18)
        self.wait(5.25)
        self.play(FadeOut(VGroup(hdr, cells, total_txt, res1, res2, gap,
                                 fast, wrong)), run_time=0.9)

class Sec4_ChatGPT(Scene):
    def construct(self):
        if MGL: self.add(background())
        hdr = topbar(self, "ChatGPT", gpt, "Dynamic programming with a bitmask")

        switches = VGroup()
        for i in range(15):
            c = Circle(radius=0.16)
            c.set_fill("#141A2A", opacity=1).set_stroke(dim, width=1.5)
            switches.add(c)
        switches.arrange(RIGHT, buff=0.22).shift(UP*1.6)
        lab = label("one switch per column --- ON means used", 19, dim)
        lab.next_to(switches, DOWN, buff=0.4)
        self.play(LaggedStart(*[GrowFromCenter(s) for s in switches],
                              lag_ratio=0.05), run_time=1.6)
        self.play(FadeIn(lab), run_time=0.8)
        self.wait(4.68)

        def set_on(idxs, rt=0.5):
            anims = []
            for i, s in enumerate(switches):
                on = i in idxs
                anims.append(s.animate
                    .set_fill(gpt if on else "#141A2A", opacity=1)
                    .set_stroke(gpt if on else dim, width=2 if on else 1.5))
            self.play(*anims, run_time=rt)

        stl = label("any pattern = a state", 20, gpt); stl.next_to(lab, DOWN, buff=0.45)
        set_on({1, 3}); self.play(FadeIn(stl), run_time=0.6)
        self.wait(2.93)
        set_on({0, 4, 7, 9})
        self.wait(3.51)

        cnt1 = label("2¹⁵ states", 32, gold); cnt1.shift(DOWN*0.7)
        self.play(Write(cnt1), run_time=0.9)
        self.wait(2.34)
        cnt2 = label("33,000 states", 32, gold); cnt2.move_to(cnt1)
        self.play(ReplacementTransform(cnt1, cnt2), run_time=0.9)
        self.wait(4.10)

        vs = label("vs 1.3 trillion --- tiny by comparison", 19, dim)
        vs.next_to(cnt2, DOWN, buff=0.3)
        self.play(FadeIn(vs), run_time=1.0)
        self.wait(5.85)
        self.play(FadeOut(VGroup(switches, lab, stl, cnt2, vs)), run_time=0.7)

        sub3 = [row[:3] for row in DEMO[:3]]
        dp = [-1]*8; dp[0] = 0; rows_states = []
        for ri in range(3):
            nd = [-1]*8
            for mask in range(8):
                if dp[mask] < 0: continue
                if bin(mask).count("1") != ri: continue
                for col in range(3):
                    if mask & (1 << col): continue
                    nm = mask | (1 << col); v = dp[mask] + sub3[ri][col]
                    if v > nd[nm]: nd[nm] = v
            dp = nd; rows_states.append(dp[:])

        cap = label("a table: best score for each state", 20, dim); cap.shift(UP*2.0)
        self.play(FadeIn(cap), run_time=1.0)
        CW, CH = 1.25, 0.5
        hdrs = VGroup(*[label(bin(m)[2:].zfill(3), 14, gpt, font=mono)
                        for m in range(8)])
        for m, h in enumerate(hdrs):
            h.move_to(RIGHT*(m-3.5)*(CW+0.12) + UP*1.25)
        self.play(LaggedStart(*[FadeIn(h, shift=DOWN*0.1) for h in hdrs],
                              lag_ratio=0.05), run_time=1.0)
        self.wait(2.93)

        rowcap = label("process row by row, update the best", 19, dim)
        rowcap.next_to(cap, DOWN, buff=0.0).shift(DOWN*0.0)
        rowcap.move_to(cap)
        self.play(Transform(cap, rowcap), run_time=0.6)
        table_grp = VGroup()
        for ri in range(3):
            rl = label(f"row {ri}", 15, dim, font=mono)
            rl.move_to(LEFT*5.6 + UP*(0.55 - ri*(CH+0.12)))
            table_grp.add(rl)
            self.play(FadeIn(rl), run_time=0.3)
            cells_row = VGroup()
            for m in range(8):
                bgc = Rectangle(width=CW, height=CH)
                bgc.set_fill("#121728", opacity=1).set_stroke("#2A3450", width=0.6)
                val = rows_states[ri][m]
                tx = label("—" if val < 0 else str(val), 14,
                       ink if val >= 0 else "#2A3142", font=mono)
                tx.move_to(bgc)
                cell = VGroup(bgc, tx)
                cell.move_to(RIGHT*(m-3.5)*(CW+0.12) + UP*(0.55 - ri*(CH+0.12)))
                cells_row.add(cell)
            self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in cells_row],
                                  lag_ratio=0.06), run_time=0.9)
            best_m = max(range(8), key=lambda m: rows_states[ri][m])
            table_grp.add(cells_row)
            self.play(cells_row[best_m][0].animate
                      .set_fill(gpt, opacity=0.4).set_stroke(gpt, width=1.6),
                      run_time=0.4)
            self.wait(2.05)

        ans = label("all switches on  →  13938  ✓", 24, good)
        ans.to_edge(DOWN, buff=1.2)
        self.play(Write(ans), run_time=1.4)
        self.wait(4.10)

        slow = label("but: 80 ms --- slowest correct answer", 20, dim)
        slow.next_to(ans, DOWN, buff=0.0); slow.move_to(ans)
        self.play(FadeOut(ans), run_time=0.3)
        self.play(Write(slow), run_time=1.6)
        self.wait(4.10)

        scale1 = label("each extra column doubles the states", 20, dim)
        scale1.move_to(slow)
        self.play(Transform(slow, scale1), run_time=0.6)
        self.wait(4.68)
        scale2 = label("30 columns  →  over a billion", 22, bad)
        scale2.move_to(slow)
        self.play(Transform(slow, scale2), run_time=0.8)
        self.wait(6.44)
        self.play(FadeOut(VGroup(hdr, cap, hdrs, slow, table_grp)), run_time=0.9)

class Sec5_Gemini(Scene):
    def construct(self):
        if MGL: self.add(background())
        hdr = topbar(self, "Gemini", gem, "Hungarian algorithm --- a known problem")

        recog = label("recognized what the others missed", 22, dim)
        recog.shift(UP*2.2)
        self.play(Write(recog), run_time=1.6)
        self.wait(2.66)

        name = label("the assignment problem", 28, gem); name.shift(UP*1.3)
        self.play(Write(name), run_time=1.2)
        badge = pill("solved in 1955", "#8899AA", w=2.6, h=0.6, size=18)
        badge.next_to(name, DOWN, buff=0.4)
        self.play(FadeIn(badge, shift=DOWN*0.2), run_time=0.8)
        self.wait(3.73)

        cx = label("guaranteed optimal in $n^3$ --- thousands, not trillions", 20, ink)
        cx.next_to(badge, DOWN, buff=0.5)
        self.play(Write(cx), run_time=2.0)
        self.wait(4.79)
        self.play(FadeOut(VGroup(recog, name, badge, cx)), run_time=0.6)

        n = 4
        sub4 = [row[:n] for row in DEMO[:n]]
        match = [(0, 3), (1, 2), (2, 0), (3, 1)]
        lp = [LEFT*3.1 + UP*(1.55 - i*0.95) for i in range(n)]
        rp = [RIGHT*3.1 + UP*(1.55 - i*0.95) for i in range(n)]
        ld = VGroup(*[Dot(p, radius=0.14) for p in lp])
        rd = VGroup(*[Dot(p, radius=0.14) for p in rp])
        for d in ld: d.set_fill(gem, opacity=1)
        for d in rd: d.set_fill(gem, opacity=1)
        ll = VGroup(*[label(f"row {i}", 15, gem) for i in range(n)])
        rl = VGroup(*[label(f"col {i}", 15, gem) for i in range(n)])
        for i in range(n):
            ll[i].next_to(ld[i], LEFT, buff=0.25)
            rl[i].next_to(rd[i], RIGHT, buff=0.25)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in [*ld, *rd]],
                              lag_ratio=0.07), run_time=1.2)
        self.play(FadeIn(ll), FadeIn(rl), run_time=0.8)

        edges = VGroup()
        for r in range(n):
            for c in range(n):
                e = Line(lp[r], rp[c]); e.set_stroke("#1E2A40", width=1)
                edges.add(e)
        self.play(LaggedStart(*[ShowCreation(e) for e in edges],
                              lag_ratio=0.02), run_time=1.6)
        self.wait(2.66)

        cap = label("locks in the best pairings, one by one", 19, dim)
        cap.to_edge(DOWN, buff=1.4)
        self.play(FadeIn(cap), run_time=0.8)
        gold_lines = VGroup()
        for r, c in match:
            gl = Line(lp[r], rp[c]); gl.set_stroke(gold, width=3.4)
            gold_lines.add(gl)
            self.play(ShowCreation(gl),
                      ld[r].animate.set_fill(gold, opacity=1),
                      rd[c].animate.set_fill(gold, opacity=1), run_time=0.7)
        self.wait(4.79)

        self.play(FadeOut(cap), run_time=0.4)
        story = label("but the real story is what Gemini wrote", 20, gem)
        story.to_edge(DOWN, buff=1.5)
        self.play(Write(story), run_time=1.8)
        self.wait(2.66)

        self.play(FadeOut(VGroup(edges, gold_lines, ld, rd, ll, rl)),
                  story.animate.to_edge(UP, buff=1.4).set_color(dim),
                  run_time=0.8)
        panel = RoundedRectangle(corner_radius=0.14, width=10.2, height=2.1)
        panel.set_fill("#0C101C", opacity=1).set_stroke("#22304A", width=1.2)
        lines = VGroup(
            label("from scipy.optimize import linear_sum_assignment", 18,
              "#9FB6D4", font=mono),
            label("ri, ci = linear_sum_assignment(-M)", 18, "#9FB6D4",
              font=mono),
            label("answer = M[ri, ci].sum()    # 13938", 18, good,
              font=mono),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        lines.move_to(panel)
        grp = VGroup(panel, lines); grp.shift(DOWN*0.2)
        self.play(FadeIn(panel), run_time=0.6)
        for ln in lines:
            self.play(Write(ln), run_time=1.1)
        three = label("three lines.", 22, gem); three.next_to(panel, DOWN, buff=0.4)
        self.play(FadeIn(three, shift=UP*0.15), run_time=0.8)
        self.wait(4.26)

        ans = label("13938  ✓     0.3 ms --- fastest correct", 22, good)
        ans.move_to(three)
        self.play(ReplacementTransform(three, ans), run_time=0.8)
        self.wait(5.32)

        lesson = label("sometimes the best move is using what exists", 20, dim)
        lesson.next_to(ans, DOWN, buff=0.0); lesson.move_to(ans)
        self.play(FadeOut(ans), run_time=0.3)
        self.play(Write(lesson), run_time=2.0)
        self.wait(5.32)
        self.play(FadeOut(VGroup(hdr, story, panel, lines, lesson)),
                  run_time=0.9)

class Sec6_Claude(Scene):
    def construct(self):
        if MGL: self.add(background())
        hdr = topbar(self, "Claude", cld, "Branch and bound --- explore, estimate, cut")

        chess = label("like a chess player reading the board", 22, dim)
        chess.shift(UP*2.2)
        self.play(Write(chess), run_time=1.8)
        self.wait(3.14)
        chess2 = label("ignore the clearly-losing lines", 22, dim)
        chess2.move_to(chess)
        self.play(ReplacementTransform(chess, chess2), run_time=0.8)
        self.wait(5.02)
        self.play(FadeOut(chess2), run_time=0.5)

        best_lbl = label("best so far: ---", 21, gold); best_lbl.to_corner(UR, buff=0.55)
        self.play(FadeIn(best_lbl), run_time=0.5)
        dive_vals = [863, 959, 463, 623, 960]
        dive_cols = ["col 4", "col 3", "col 2", "col 1", "col 0"]
        chain_pos = [UP*2.0 + LEFT*2.6 + DOWN*i*0.92 for i in range(5)]
        run = 0; prev = None; chain = VGroup()
        for i, (v, cl, p) in enumerate(zip(dive_vals, dive_cols, chain_pos)):
            d = Dot(p, radius=0.15); d.set_fill(cld, opacity=1)
            t = label(f"row {i}: {cl} (+{v})", 16, ink); t.next_to(d, RIGHT, buff=0.3)
            grp = VGroup(d, t); chain.add(grp)
            anims = [GrowFromCenter(d), FadeIn(t, shift=LEFT*0.15)]
            if prev is not None:
                e = Line(prev.get_center(), p); e.set_stroke(cld, width=2)
                chain.add(e); anims.append(ShowCreation(e))
            self.play(*anims, run_time=0.6)
            run += v
            nb = label(f"best so far: {run}", 21, gold); nb.move_to(best_lbl)
            self.play(Transform(best_lbl, nb), run_time=0.25)
            prev = d
        self.wait(4.39)

        est = label("before going deeper: a quick ceiling estimate", 19, dim)
        est.to_edge(DOWN, buff=1.4)
        self.play(Write(est), run_time=2.0)
        self.wait(5.02)
        est2 = label("if every remaining pick went perfectly...", 19, dim)
        est2.move_to(est)
        self.play(Transform(est, est2), run_time=0.7)
        self.wait(4.39)

        self.play(FadeOut(est), run_time=0.4)
        root = chain_pos[0]
        branches = VGroup()
        specs = [(UP*2.0 + RIGHT*1.6, "col 3", "ceiling 3428"),
                 (UP*2.0 + RIGHT*4.2, "col 2", "ceiling 3404")]
        for (bp, lbl, ceil) in specs:
            e = Line(root, bp); e.set_stroke("#33405A", width=1.6)
            d = Dot(bp, radius=0.14); d.set_fill("#33405A", opacity=1)
            t = label(lbl, 15, dim); t.next_to(d, UP, buff=0.18)
            c = label(ceil, 15, bad); c.next_to(d, DOWN, buff=0.2)
            self.play(ShowCreation(e), GrowFromCenter(d), FadeIn(t),
                      run_time=0.6)
            self.play(FadeIn(c, shift=UP*0.1), run_time=0.5)
            cut = label("$<$ 3868  →  cut", 15, bad); cut.next_to(c, DOWN, buff=0.15)
            self.play(FadeIn(cut), run_time=0.4)
            self.play(VGroup(e, d, t, c, cut).animate.set_opacity(0.25),
                      run_time=0.5)
            branches.add(VGroup(e, d, t, c, cut))
            self.wait(2.51)

        insight = label("one early cut removes millions of combinations", 19, cld)
        insight.to_edge(DOWN, buff=1.3)
        self.play(Write(insight), run_time=2.0)
        self.wait(5.64)

        self.play(FadeOut(insight), run_time=0.4)
        ans = label("13938  ✓     1.8 ms", 24, good); ans.to_edge(DOWN, buff=1.3)
        self.play(Write(ans), run_time=1.2)
        self.wait(3.76)

        nolib = label("no library --- pruning logic built by hand", 20, dim)
        nolib.next_to(ans, DOWN, buff=0.0); nolib.move_to(ans)
        self.play(FadeOut(ans), run_time=0.3)
        self.play(Write(nolib), run_time=1.8)
        self.wait(5.02)
        most = label("the most original solution of the four", 20, cld)
        most.move_to(nolib)
        self.play(Transform(nolib, most), run_time=0.7)
        self.wait(6.27)
        self.play(FadeOut(VGroup(hdr, best_lbl, chain, branches, nolib)),
                  run_time=0.9)

class Sec7_Compare(Scene):
    def construct(self):
        if MGL: self.add(background())
        import math
        title = label("Runtime --- log scale (each step = 10x slower)", 24)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.4)

        axis = Line(LEFT*4.8, RIGHT*4.8); axis.set_stroke(gridcol, 2)
        axis.shift(DOWN*0.1)
        self.play(ShowCreation(axis), run_time=0.8)
        lo, hi = math.log10(0.05), math.log10(200)
        def xp(t): return (math.log10(t)-lo)/(hi-lo)*9.6 - 4.8
        ticks = VGroup()
        for v in [0.1, 1, 10, 100]:
            tk = Line(RIGHT*xp(v)+DOWN*0.3, RIGHT*xp(v)+DOWN*0.5)
            tk.set_stroke(gridcol, 1.2)
            tl = label(f"{v} ms", 13, dim); tl.move_to(RIGHT*xp(v)+DOWN*0.85)
            ticks.add(VGroup(tk, tl))
        self.play(LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.1),
                  run_time=1.0)
        self.wait(7.06)

        entries = [("Grok", grok, 0.1, "fastest, wrong", True),
                   ("Gemini", gem, 0.3, "correct, 3 lines", False),
                   ("Claude", cld, 1.8, "correct, by hand", False),
                   ("ChatGPT", gpt, 80.0, "correct, 44x slower", False)]
        dots_grp = VGroup()
        waits = [1.2, 1.2, 1.6, 2.4]
        for i, (nm, col, t, note, wrong) in enumerate(entries):
            d = Dot(RIGHT*xp(t)+DOWN*0.1, radius=0.16); d.set_fill(col, opacity=1)
            tag = label(f"{nm} --- {t} ms", 17, bad if wrong else col)
            tag.move_to(RIGHT*xp(t) + UP*(0.7 + (i % 2)*0.6))
            sub = label(note, 14, dim); sub.next_to(tag, UP, buff=0.12)
            ln = Line(tag.get_bottom()+DOWN*0.05, d.get_center()+UP*0.18)
            ln.set_stroke("#33405A", 1)
            dots_grp.add(VGroup(d, tag, sub, ln))
            self.play(GrowFromCenter(d), FadeIn(tag, shift=DOWN*0.12),
                      FadeIn(sub), ShowCreation(ln), run_time=0.7)
            if wrong:
                x = label("✗", 22, bad); x.next_to(d, DOWN, buff=0.12)
                self.play(FadeIn(x), run_time=0.3)
                dots_grp.add(x)
            self.wait(waits[i])

        s1 = label("three correct --- 0.3, 1.8, 80 ms", 20, ink)
        s2 = label("one wrong --- four very different routes", 20, dim)
        summ = VGroup(s1, s2).arrange(DOWN, buff=0.22); summ.to_edge(DOWN, buff=0.8)
        self.play(Write(s1), run_time=1.2)
        self.play(FadeIn(s2, shift=UP*0.15), run_time=1.0)
        self.wait(17.64)
        self.play(FadeOut(VGroup(title, axis, ticks, dots_grp, summ)),
                  run_time=0.9)

class Sec8_Verdict(Scene):
    def construct(self):
        if MGL: self.add(background())
        head = label("The Verdict", 34); head.to_edge(UP, buff=0.6)
        self.play(Write(head), run_time=1.0)
        self.wait(2.33)

        gchip = pill("Gemini", gem, w=3.2, h=1.0, size=30)
        cchip = pill("Claude", cld, w=3.2, h=1.0, size=30)
        finalists = VGroup(gchip, cchip).arrange(RIGHT, buff=1.6); finalists.shift(UP*0.8)
        self.play(FadeIn(gchip, shift=RIGHT*0.3),
                  FadeIn(cchip, shift=LEFT*0.3), run_time=1.2)
        self.wait(2.79)

        gsub = VGroup(label("the one you'd want at work", 16, dim),
                      label("proven tool, 3 lines", 16, dim)
                      ).arrange(DOWN, buff=0.14)
        gsub.next_to(gchip, DOWN, buff=0.3)
        self.play(FadeIn(gsub), run_time=1.0)
        self.wait(5.59)

        csub = VGroup(label("more impressive reasoning", 16, dim),
                      label("hand-built, near library speed", 16, dim)
                      ).arrange(DOWN, buff=0.14)
        csub.next_to(cchip, DOWN, buff=0.3)
        self.play(FadeIn(csub), run_time=1.0)
        self.wait(6.05)

        crown = Polygon([-0.42, 0, 0], [-0.25, 0.34, 0], [0, 0.06, 0],
                        [0.25, 0.34, 0], [0.42, 0, 0])
        crown.set_fill(gold, opacity=1).set_stroke(gold, width=1); crown.scale(0.85)
        crown.next_to(cchip, UP, buff=0.18).shift(UP*1.5).set_opacity(0)
        self.add(crown)
        self.play(crown.animate.shift(DOWN*1.5).set_opacity(1), run_time=0.8)
        self.play(cchip.animate.scale(1.08), gchip.animate.set_opacity(0.5),
                  gsub.animate.set_opacity(0.4), run_time=0.7)
        self.wait(3.26)

        why = VGroup(
            label("knowing a library exists is knowledge", 19, ink),
            label("building branch and bound is understanding", 19, cld)
        ).arrange(DOWN, buff=0.2)
        why.to_edge(DOWN, buff=1.2)
        self.play(Write(why[0]), run_time=1.6)
        self.play(Write(why[1]), run_time=1.6)
        self.wait(5.59)
        self.play(FadeOut(VGroup(gchip, cchip, gsub, csub, crown, why)),
                  run_time=0.7)

        wchip = pill("Grok", grok, w=3.0, h=0.95, size=28); wchip.shift(UP*1.4)
        self.play(FadeIn(wchip, shift=DOWN*0.2), run_time=0.8)
        worst = label("the worst --- but not for bad code", 20, ink)
        worst.next_to(wchip, DOWN, buff=0.5)
        self.play(Write(worst), run_time=1.8)
        self.wait(3.26)

        clean = label("clean, easy to understand", 18, dim)
        clean.next_to(worst, DOWN, buff=0.35)
        self.play(FadeIn(clean), run_time=1.0)
        self.wait(4.65)

        fw = label("fastest --- but the wrong answer", 22, bad)
        fw.next_to(clean, DOWN, buff=0.4)
        self.play(Write(fw), run_time=1.6)
        self.wait(4.65)
        self.play(FadeOut(VGroup(wchip, worst, clean, fw)), run_time=0.6)

        fin1 = label("the answer to Problem 345", 24, dim)
        fin2 = label("13,938", 66, gold)
        fin = VGroup(fin1, fin2).arrange(DOWN, buff=0.35); fin.shift(UP*0.2)
        self.play(FadeIn(fin1), run_time=0.8)
        self.play(Write(fin2), run_time=1.2)
        box = SurroundingRectangle(fin2, buff=0.25); box.set_stroke(gold, 2)
        self.play(ShowCreation(box), run_time=0.8)
        three = label("three of four models got it", 18, good)
        three.next_to(box, DOWN, buff=0.4)
        self.play(FadeIn(three, shift=UP*0.15), run_time=1.0)
        self.wait(6.05)

        outro = label("same four models next time --- different problem", 19, dim)
        outro.to_edge(DOWN, buff=0.9)
        self.play(Write(outro), run_time=2.0)
        self.wait(5.59)
        self.play(FadeOut(VGroup(head, fin, box, three, outro)), run_time=1.0)
