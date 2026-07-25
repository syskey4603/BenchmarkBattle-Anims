from manim import *
import numpy as np, re
config.background_color="#0A0A15"
mono="Consolas"
grok="#FF4500"; gpt="#10A37F"; gem="#4285F4"; cld="#E8925C"
gold="#FFD700"; bad="#FF5555"; good="#4ADE80"
ink="#F2F3F7"; dim="#FFB86C"; panel="#10141F"; gridc="#2A3450"

def fixtext(s):
    s=s.replace("\\$","\x00M\x00").replace("\\"," ")
    s=s.replace("%",r"\%").replace("&",r"\&").replace("#",r"\#").replace("_",r"\_")
    s=re.sub(r'"([^"]*)"',r"``\1''",s)
    for a,b in [("→",r"$\rightarrow$"),("✓",r"$\checkmark$"),("✗",r"$\times$"),
                ("×",r"$\times$"),("≈",r"$\approx$"),("—","---"),("≡",r"$\equiv$"),
                ("·",r"$\cdot$"),("²",r"$^2$")]:
        s=s.replace(a,b)
    return s.replace("\x00M\x00",r"\$")
def label(s,size=24,color=ink,font=None):
    t=Text(s,font_size=size,font=font) if font else Tex(fixtext(s),font_size=size)
    return t.set_color(color)
def pill(name,color,w=2.4,h=0.74,size=23):
    b=RoundedRectangle(corner_radius=0.12,width=w,height=h).set_fill(panel,1).set_stroke(color,2)
    return VGroup(b,label(name,size,color).move_to(b))
def card(txt,size=18,color=ink,pad=0.2,stroke=gridc):
    t=label(txt,size,color)
    box=SurroundingRectangle(t,buff=pad,corner_radius=0.1).set_fill(panel,1).set_stroke(stroke,1.4)
    return VGroup(box,t)

class Base(Scene):
    times=[]
    def start(self): self.now=0.0
    def P(self,*a,rt=0.8,**k): self.play(*a,run_time=rt,**k); self.now+=rt
    def W(self,t):
        if t>0: self.wait(t); self.now+=t
    def waitfor(self,i):
        if i<len(self.times):
            g=self.times[i]-self.now
            if g>0.03: self.wait(g); self.now+=g
    def finish(self,total):
        g=total-self.now
        if g>0: self.wait(g)


class Sec01_Title(Base):
    times=[0.1,8.0,11.3]
    def construct(self):
        self.start()
        self.waitfor(0)
        t=label("Four AIs. One brutal problem.",42); t.to_edge(UP,buff=1.2)
        ep=label("Project Euler 250",24,dim); ep.next_to(t,DOWN,buff=0.3)
        self.P(Write(t),rt=1.2); self.P(FadeIn(ep),rt=0.6)
        self.waitfor(1)
        chips=VGroup(pill("ChatGPT",gpt),pill("Gemini",gem),
                     pill("Grok",grok),pill("Claude",cld)).arrange(RIGHT,buff=0.34)
        for c in chips: self.P(FadeIn(c,shift=UP*0.2),rt=0.4)
        self.waitfor(2)
        sub=label("same problem  ·  no hints",20,dim); sub.next_to(chips,DOWN,buff=0.7)
        self.P(Write(sub),rt=1.0)
        self.finish(17.1+1.2)


class Sec02_Problem(Base):
    times=[0.4,5.8,7.5,13.4,18.1,20.3,23.5,28.4,30.4,31.5,33.9]
    def construct(self):
        self.start()
        self.waitfor(0)
        title=label("Problem 250 --- 250250",30); title.to_edge(UP,buff=0.5)
        self.P(Write(title),rt=1.0)
        self.waitfor(1)
        expr=label(r"$1^1,\ 2^2,\ 3^3,\ \dots,\ 250250^{250250}$",30,ink); expr.move_to(UP*1.4)
        self.P(Write(expr),rt=1.2)
        self.waitfor(2)
        big=label("a list of 250,250 gigantic numbers",20,dim); big.next_to(expr,DOWN,buff=0.5)
        self.P(FadeIn(big),rt=0.8)
        self.waitfor(3)
        self.P(FadeOut(big),rt=0.3)
        pick=label("pick any subset --- when is the sum divisible by 250?",20,gold)
        pick.next_to(expr,DOWN,buff=0.6)
        self.P(Write(pick),rt=1.4)
        self.waitfor(4)
        self.P(FadeOut(pick),rt=0.3)
        c1=label(r"$\equiv 0 \pmod{250}$",34,good); c1.next_to(expr,DOWN,buff=0.7)
        self.P(Write(c1),rt=1.2)
        self.waitfor(5)
        cnt=label("count every such subset",20,ink); cnt.next_to(c1,DOWN,buff=0.5)
        self.P(FadeIn(cnt),rt=0.9)
        self.waitfor(6)
        huge=label("the count is astronomically large",18,dim); huge.move_to(cnt)
        self.P(FadeOut(cnt),rt=0.3); self.P(Write(huge),rt=1.1)
        self.waitfor(7)
        self.P(FadeOut(VGroup(expr,c1,huge)),rt=0.4)
        last=label("so they only want the last 16 digits",22,gold); last.move_to(UP*0.3)
        self.P(Write(last),rt=1.2)
        self.waitfor(8)
        self.waitfor(9)
        modb=label(r"answer $\bmod\ 10^{16}$",22,dim); modb.next_to(last,DOWN,buff=0.5)
        self.P(Write(modb),rt=1.0)
        self.waitfor(10)
        self.finish(36.5+1.2)


class Sec03_Approaches(Base):
    times=[0.3,2.8,5.6,10.7,12.8,15.0,18.1,20.2,24.3,29.1,32.7]
    def construct(self):
        self.start()
        self.waitfor(0)
        title=label("Two ideas everyone needs",28); title.to_edge(UP,buff=0.5)
        self.P(Write(title),rt=1.0)
        self.waitfor(1)
        i1=card("1.  reduce each $i^i$ mod 250",22,gem); i1.move_to(UP*1.3)
        self.P(FadeIn(i1,shift=UP*0.2),rt=0.9)
        self.waitfor(2)
        sub1=label("250,250 giants collapse to just 250 possible remainders",17,dim)
        sub1.next_to(i1,DOWN,buff=0.4)
        self.P(Write(sub1),rt=1.3)
        self.waitfor(3)
        self.waitfor(4)
        i2=card("2.  count subsets by remainder",22,good); i2.next_to(sub1,DOWN,buff=0.6)
        self.P(FadeIn(i2,shift=UP*0.2),rt=0.9)
        self.waitfor(5)
        sub2=label("track how many subsets land on each remainder 0...249",17,dim)
        sub2.next_to(i2,DOWN,buff=0.4)
        self.P(Write(sub2),rt=1.3)
        self.waitfor(6)
        self.waitfor(7)
        speed=label("do it fast --- or you'll never finish",18,bad); speed.next_to(sub2,DOWN,buff=0.5)
        self.P(Write(speed),rt=1.2)
        self.waitfor(8)
        self.waitfor(9)
        who=label("who actually pulled it off?",20,gold); who.next_to(speed,DOWN,buff=0.5)
        self.P(Write(who),rt=1.1)
        self.waitfor(10)
        self.finish(33.9+1.2)


class Sec04_Grok(Base):
    times=[1.9,4.1,18.0,22.2]
    def construct(self):
        self.start()
        hdr=pill("Grok",grok).to_corner(UL,buff=0.45)
        sub=label("Dynamic programming over remainders",20,dim).next_to(hdr,RIGHT,buff=0.45)
        self.P(FadeIn(hdr,shift=DOWN*0.2),Write(sub),rt=1.0)
        self.waitfor(0)
        idea=label("keep a running tally of subsets per remainder",20,grok); idea.move_to(UP*1.5)
        self.P(Write(idea),rt=1.2)
        self.waitfor(1)
        boxes=VGroup()
        for r in [0,1,2,"...",249]:
            b=RoundedRectangle(corner_radius=0.08,width=1.3,height=1.0).set_fill(panel,1).set_stroke(grok,1.5)
            lab=label(str(r),20,ink).move_to(b.get_top()+DOWN*0.3)
            cnt=label("0",22,good).move_to(b.get_bottom()+UP*0.3)
            boxes.add(VGroup(b,lab,cnt))
        boxes.arrange(RIGHT,buff=0.3).move_to(DOWN*0.3)
        self.P(LaggedStart(*[FadeIn(b,shift=UP*0.15) for b in boxes],lag_ratio=0.1),rt=1.2)
        vals=[[1,2,4],[2,5,9],[3,7,14],[4,9,18],[5,11,22]]
        for step in range(3):
            self.P(*[Transform(boxes[i][2],label(str(vals[i][step]),22,good).move_to(boxes[i][2]))
                     for i in range(len(boxes))],rt=0.5)
        self.waitfor(2)
        self.P(FadeOut(boxes),FadeOut(idea),rt=0.4)
        res=label("correct, exact --- but the slowest of the bunch",20,dim); res.move_to(UP*0.2)
        self.P(Write(res),rt=1.3)
        self.waitfor(3)
        self.finish(30.1+1.2)


class Sec05_GPT(Base):
    times=[0.4,1.5,3.7,4.5,11.2,12.8,15.9,17.4,20.6,27.9,31.0,32.4]
    def construct(self):
        self.start()
        hdr=pill("ChatGPT",gpt).to_corner(UL,buff=0.45)
        sub=label("Generating functions",20,dim).next_to(hdr,RIGHT,buff=0.45)
        self.P(FadeIn(hdr,shift=DOWN*0.2),Write(sub),rt=1.0)
        self.waitfor(0)
        self.waitfor(1)
        idea=label("turn subsets into a polynomial you multiply",20,gpt); idea.move_to(UP*1.6)
        self.P(Write(idea),rt=1.3)
        self.waitfor(2)
        self.waitfor(3)
        poly=label(r"$\prod_i \left(1 + x^{\,i^i \bmod 250}\right)$",30,ink); poly.next_to(idea,DOWN,buff=0.6)
        self.P(Write(poly),rt=1.4)
        self.waitfor(4)
        expl=label("each factor = include this number, or don't",17,dim); expl.next_to(poly,DOWN,buff=0.5)
        self.P(FadeIn(expl),rt=1.0)
        self.waitfor(5)
        self.waitfor(6)
        mod=label(r"work mod $x^{250}-1$ so exponents wrap around",17,gpt); mod.next_to(expl,DOWN,buff=0.4)
        self.P(Write(mod),rt=1.3)
        self.waitfor(7)
        self.waitfor(8)
        self.P(FadeOut(VGroup(idea,poly,expl,mod)),rt=0.4)
        coef=label(r"the coefficient of $x^0$ counts them all",20,good); coef.move_to(UP*0.3)
        self.P(Write(coef),rt=1.3)
        self.waitfor(9)
        self.waitfor(10)
        good_r=label("elegant and correct --- a strong solution",18,dim); good_r.next_to(coef,DOWN,buff=0.5)
        self.P(Write(good_r),rt=1.2)
        self.waitfor(11)
        self.finish(34.5+1.2)


class Sec06_Gemini(Base):
    times=[0.4,2.4,5.2,7.8,15.5,17.4,19.2,21.4,24.6]
    def construct(self):
        self.start()
        hdr=pill("Gemini",gem).to_corner(UL,buff=0.45)
        sub=label("Fast exponentiation on the polynomial",20,dim).next_to(hdr,RIGHT,buff=0.45)
        self.P(FadeIn(hdr,shift=DOWN*0.2),Write(sub),rt=1.0)
        self.waitfor(0)
        idea=label("many numbers share the same remainder",20,gem); idea.move_to(UP*1.6)
        self.P(Write(idea),rt=1.2)
        self.waitfor(1)
        group=label(r"so group them: $(1+x^r)^{c}$ for count $c$",26,ink); group.next_to(idea,DOWN,buff=0.5)
        self.P(Write(group),rt=1.3)
        self.waitfor(2)
        self.waitfor(3)
        fast=label("raise to that power with repeated squaring",18,gem); fast.next_to(group,DOWN,buff=0.5)
        self.P(Write(fast),rt=1.3)
        self.waitfor(4)
        self.P(FadeOut(VGroup(idea,group,fast)),rt=0.4)
        speedup=label("thousands of multiplications collapse to a handful",20,good)
        speedup.move_to(UP*0.4)
        self.P(Write(speedup),rt=1.4)
        self.waitfor(5)
        self.waitfor(6)
        fastest=label("the fastest solution of the four",22,gold); fastest.next_to(speedup,DOWN,buff=0.5)
        self.P(Write(fastest),rt=1.2)
        self.waitfor(7)
        self.waitfor(8)
        self.finish(37.8+1.2)


class Sec07_Claude(Base):
    times=[0.5,13.8,15.3,28.2,29.9,35.4,38.6]
    def construct(self):
        self.start()
        hdr=pill("Claude",cld).to_corner(UL,buff=0.45)
        sub=label("The cleanest reduction",20,dim).next_to(hdr,RIGHT,buff=0.45)
        self.P(FadeIn(hdr,shift=DOWN*0.2),Write(sub),rt=1.0)
        self.waitfor(0)
        idea=label("same grouping insight --- taken furthest",20,cld); idea.move_to(UP*1.6)
        self.P(Write(idea),rt=1.2)
        self.waitfor(1)
        step=label(r"count residues, build $(1+x^r)^{c}$, multiply mod $x^{250}-1$",18,ink)
        step.next_to(idea,DOWN,buff=0.5)
        self.P(Write(step),rt=1.4)
        self.waitfor(2)
        clean=label("no wasted work --- every step earns its place",18,dim)
        clean.next_to(step,DOWN,buff=0.5)
        self.P(FadeIn(clean),rt=1.1)
        self.waitfor(3)
        self.P(FadeOut(VGroup(idea,step,clean)),rt=0.4)
        ans=label("1425480602091519",34,good); ans.move_to(UP*0.4)
        albl=label("the last 16 digits",17,dim).next_to(ans,UP,buff=0.3)
        self.P(FadeIn(albl),Write(ans),rt=1.3)
        self.waitfor(4)
        box=SurroundingRectangle(ans,buff=0.2).set_stroke(gold,2)
        self.P(Create(box),rt=0.7)
        self.waitfor(5)
        crown=label("exact, fast, and the clearest of them all",18,gold); crown.next_to(ans,DOWN,buff=0.7)
        self.P(Write(crown),rt=1.3)
        self.waitfor(6)
        self.finish(47.8+1.2)


class Sec08_CodeLogic(Base):
    times=[0.3,3.3,11.9,13.4,18.8,25.9,33.2,36.2,38.4,41.0,43.8,45.4,48.1,51.1,53.4,58.7,63.0,68.0,74.0,80.0,86.0,92.0,98.0,104.0,110.0,116.0,122.0]
    def construct(self):
        self.start()
        self.waitfor(0)
        title=label("The code, step by step",28); title.to_edge(UP,buff=0.5)
        self.P(Write(title),rt=1.0)
        self.waitfor(1)
        code_lines=[
            "mod = 250",
            "N = 250250",
            "counts = Counter(pow(i,i,mod) for i in range(1,N+1))",
            "dp = [0]*mod",
            "dp[0] = 1",
            "for r,c in counts.items():",
            "    dp = mul(dp, poly_pow(r, c))",
            "answer = (dp[0] - 1) % 10**16",
        ]
        code=VGroup(*[label(l,20,ink if not l.strip().startswith('#') else dim,font=mono)
                      for l in code_lines])
        code.arrange(DOWN,aligned_edge=LEFT,buff=0.22).move_to(LEFT*0.6+DOWN*0.2)
        cbox=SurroundingRectangle(code,buff=0.35,corner_radius=0.1).set_fill("#0D1420",1).set_stroke(gridc,1.4)
        self.P(FadeIn(cbox),rt=0.5)
        highlights=[
            "collapse 250,250 giants to remainders",
            "collapse 250,250 giants to remainders",
            "each number to its remainder mod 250",
            "start: one empty subset, remainder 0",
            "start: one empty subset, remainder 0",
            "for every distinct remainder...",
            "fold in all c copies at once",
            "subtract the empty subset, keep 16 digits",
        ]
        # reveal each line pinned to a beat
        for k,line in enumerate(code):
            self.waitfor(2+k)
            self.P(FadeIn(line,shift=RIGHT*0.15),rt=0.6)
            note=label(highlights[k],16,dim); note.next_to(cbox,DOWN,buff=0.4)
            self.P(FadeIn(note),rt=0.5)
            if k<len(code)-1:
                self.P(FadeOut(note),rt=0.4)
        self.finish(129.4+1.2)


class Sec09_ChainOfThought(Base):
    times=[0.1,2.2,4.5,5.7,9.6,13.5,16.8,18.0,20.0,21.1]
    def construct(self):
        self.start()
        self.waitfor(0)
        title=label("Why it works",28); title.to_edge(UP,buff=0.5)
        self.P(Write(title),rt=1.0)
        self.waitfor(1)
        steps=[
            "each subset lands on one remainder",
            "we only care about remainder 0",
            "grouping equal remainders saves the day",
            "squaring the polynomial makes it fast",
            "the empty subset is the only one to drop",
        ]
        prev=None
        for k,s in enumerate(steps):
            self.waitfor(2+k if 2+k<len(self.times) else len(self.times)-1)
            c=card(s,20,[gem,gpt,good,cld,gold][k%5])
            c.move_to(UP*1.2-DOWN*k*0.0)
            if prev is not None:
                self.P(prev.animate.scale(0.9).set_opacity(0.4).shift(UP*1.1),rt=0.4)
            self.P(FadeIn(c,shift=UP*0.2),rt=0.8)
            if prev is not None: self.P(FadeOut(prev),rt=0.3)
            prev=c
        self.finish(26.4+1.2)


class Sec10_Verdict(Base):
    times=[1.1,3.4,15.2,20.1,25.0,35.0,45.6,55.0,68.0,80.0,92.0,104.0,116.0,128.0,138.0]
    def construct(self):
        self.start()
        head=label("The Verdict",32); head.to_edge(UP,buff=0.5)
        names=["Claude","Gemini","ChatGPT","Grok"]
        cols={"Claude":cld,"Gemini":gem,"ChatGPT":gpt,"Grok":grok}
        scs=VGroup()
        for nm in names:
            b=RoundedRectangle(corner_radius=0.08,width=4.4,height=0.78).set_fill(panel,1).set_stroke(gridc,1.2)
            scs.add(VGroup(b,label(nm,20,cols[nm]).move_to(b.get_left()+RIGHT*0.95)))
        scs.arrange(DOWN,buff=0.22).to_edge(RIGHT,buff=0.6)
        focus=LEFT*3.2+UP*0.3
        def note(i,txt,col):
            nt=label(txt,15,col).move_to(scs[i][0].get_right()+LEFT*1.45)
            self.P(FadeIn(nt,shift=LEFT*0.15),rt=0.5)
        self.waitfor(0)
        self.P(Write(head),rt=0.8)
        self.P(*[FadeIn(r[0]) for r in scs],*[FadeIn(r[1]) for r in scs],rt=1.0)
        self.waitfor(1)
        cf=pill("Claude",cld,w=2.8,h=0.9,size=26).move_to(focus)
        crown=Polygon([-0.4,0,0],[-0.24,0.32,0],[0,0.06,0],[0.24,0.32,0],[0.4,0,0]).set_fill(gold,1).set_stroke(gold,1).scale(0.85)
        crown.next_to(cf,UP,buff=0.12)
        self.P(FadeIn(cf,shift=DOWN*0.2),rt=0.6); self.P(FadeIn(crown,shift=DOWN*0.3),rt=0.5)
        c1=label("cleanest reduction --- exact and fast",17,cld); c1.next_to(cf,DOWN,buff=0.45)
        self.P(Write(c1),rt=1.0); note(0,"winner",gold)
        self.waitfor(2)
        self.P(FadeOut(VGroup(cf,crown,c1)),rt=0.4)
        gf=pill("Gemini",gem,w=2.8,h=0.9,size=26).move_to(focus)
        self.P(FadeIn(gf,shift=DOWN*0.2),rt=0.6)
        g1=label("fastest --- squaring trick, a hair behind",17,ink); g1.next_to(gf,DOWN,buff=0.45)
        self.P(Write(g1),rt=1.0); note(1,"2nd, fastest",gem)
        self.waitfor(3)
        self.P(FadeOut(VGroup(gf,g1)),rt=0.4)
        pf=pill("ChatGPT",gpt,w=2.8,h=0.9,size=26).move_to(focus)
        self.P(FadeIn(pf,shift=DOWN*0.2),rt=0.6)
        p1=label("generating functions --- elegant, correct",17,ink); p1.next_to(pf,DOWN,buff=0.45)
        self.P(Write(p1),rt=1.0); note(2,"3rd, correct",gpt)
        self.waitfor(4)
        self.P(FadeOut(VGroup(pf,p1)),rt=0.4)
        rf=pill("Grok",grok,w=2.8,h=0.9,size=26).move_to(focus)
        self.P(FadeIn(rf,shift=DOWN*0.2),rt=0.6)
        r1=label("plain DP --- correct but the slowest",17,dim); r1.next_to(rf,DOWN,buff=0.45)
        self.P(Write(r1),rt=1.0); note(3,"4th, slowest",bad)
        self.waitfor(5)
        self.P(FadeOut(VGroup(rf,r1)),rt=0.4)
        pat=label("each model keeps failing the same way",18,gold); pat.move_to(focus+UP*0.5)
        self.P(Write(pat),rt=1.2)
        self.waitfor(6)
        pat2=label("the losers reach for brute force over insight",16,dim); pat2.next_to(pat,DOWN,buff=0.4)
        self.P(FadeIn(pat2),rt=1.0)
        self.waitfor(7)
        self.P(FadeOut(VGroup(pat,pat2)),rt=0.4)
        for i in range(8, len(self.times)-1):
            self.waitfor(i)
        fin1=label("Project Euler 250",22,dim); fin1.move_to(focus+UP*0.7)
        fin2=label("1425480602091519",30,gold); fin2.next_to(fin1,DOWN,buff=0.35)
        fbox=SurroundingRectangle(fin2,buff=0.2).set_stroke(gold,2)
        self.P(FadeIn(fin1),rt=0.5); self.P(Write(fin2),rt=1.0); self.P(Create(fbox),rt=0.6)
        self.waitfor(len(self.times)-1)
        outro=label("Claude takes the crown --- same four next time",17,dim); outro.to_edge(DOWN,buff=0.7)
        self.P(Write(outro),rt=1.4)
        self.finish(144.4+1.2)
