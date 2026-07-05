from manim import *
import numpy as np
import re
config.background_color = "#0A0A15"

mono="Consolas"
grok="#FF4500"; gpt="#10A37F"; gem="#4285F4"; cld="#E8925C"
gold="#FFD700"; bad="#FF5555"; good="#4ADE80"
ink="#F2F3F7"; dim="#FFB86C"; panel="#10141F"; gridc="#2A3450"
peter_c="#5AB1FF"; colin_c="#FF8C5A"

def fixtext(s):
    s=s.replace("\\$", "\x00MONEY\x00")
    s=s.replace("\\"," ")
    s=s.replace("%",r"\%").replace("&",r"\&").replace("#",r"\#")
    s=s.replace("_",r"\_")
    s=re.sub(r'"([^"]*)"',r"``\1''",s)
    for a,b in [("\u2192",r"$\rightarrow$"),("\u2713",r"$\checkmark$"),("\u2717",r"$\times$"),
                ("\u00d7",r"$\times$"),("\u2248",r"$\approx$"),("\u2014","---"),
                ("\u2260",r"$\neq$"),("\u00b7",r"$\cdot$")]:
        s=s.replace(a,b)
    s=s.replace("\x00MONEY\x00", r"\$")
    return s

def label(s,size=24,color=ink,font=None):
    t=Text(s,font_size=size,font=font) if font else Tex(fixtext(s),font_size=size)
    return t.set_color(color)
def pill(name,color,w=2.4,h=0.74,size=23):
    b=RoundedRectangle(corner_radius=0.12,width=w,height=h).set_fill(panel,1).set_stroke(color,2)
    return VGroup(b,label(name,size,color).move_to(b))

PIPS={1:[(0,0)],2:[(-1,1),(1,-1)],3:[(-1,1),(0,0),(1,-1)],
      4:[(-1,1),(1,1),(-1,-1),(1,-1)],5:[(-1,1),(1,1),(0,0),(-1,-1),(1,-1)],
      6:[(-1,1),(1,1),(-1,0),(1,0),(-1,-1),(1,-1)]}
def die(val,size=0.7,face=panel,edge=ink,pip=ink):
    sq=RoundedRectangle(corner_radius=0.12,width=size,height=size).set_fill(face,1).set_stroke(edge,2)
    g=VGroup(sq)
    off=size*0.26
    for (dx,dy) in PIPS[val]:
        d=Dot(radius=size*0.07,color=pip).move_to(sq.get_center()+np.array([dx*off,dy*off,0]))
        g.add(d)
    return g

def dice_row(vals,size=0.6,gap=0.14,edge=ink,pip=ink):
    g=VGroup(*[die(v,size,panel,edge,pip) for v in vals]).arrange(RIGHT,buff=gap)
    return g

def bar(frac,width=7.0,height=0.5,fillc=peter_c,restc=colin_c):
    base=RoundedRectangle(corner_radius=0.08,width=width,height=height).set_fill(restc,0.9).set_stroke(width=0)
    fillw=max(0.001,width*frac)
    fil=RoundedRectangle(corner_radius=0.08,width=fillw,height=height).set_fill(fillc,1).set_stroke(width=0)
    fil.align_to(base,LEFT)
    return VGroup(base,fil)

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


class Sec1_Intro(Base):
    times=[0.37,10.94,14.84,17.34,23.36,28.32,31.18,33.84]
    def construct(self):
        self.start()
        self.waitfor(0)
        l1=label("OpenAI raised \\$100{,}000{,}000{,}000",30,gold); l1.move_to(UP*1.6)
        self.P(Write(l1),rt=1.2)
        l2=label("the most funded AI in history",22,dim); l2.next_to(l1,DOWN,buff=0.4)
        self.P(FadeIn(l2),rt=0.8)
        l3=label("today it lost to a dice problem",26,ink); l3.next_to(l2,DOWN,buff=0.5)
        self.P(Write(l3),rt=1.2)
        sub=label("...that a free model solved exactly",20,bad); sub.next_to(l3,DOWN,buff=0.35)
        self.P(FadeIn(sub),rt=1.0)

        self.waitfor(1)  # the setup
        self.P(FadeOut(VGroup(l1,l2,l3,sub)),rt=0.6)
        peter=dice_row([4,3,4,2,1,3,4,2,4],size=0.5,edge=peter_c,pip=peter_c).move_to(UP*1.4)
        plab=label("Peter --- nine 4-sided dice",20,peter_c); plab.next_to(peter,UP,buff=0.3)
        self.P(FadeIn(plab),LaggedStart(*[FadeIn(d,scale=0.6) for d in peter],lag_ratio=0.05),rt=1.4)

        self.waitfor(2)  # Colin six six-sided
        colin=dice_row([6,5,3,6,4,6],size=0.66,edge=colin_c,pip=colin_c).move_to(DOWN*0.3)
        clab=label("Colin --- six 6-sided dice",20,colin_c); clab.next_to(colin,UP,buff=0.3)
        self.P(FadeIn(clab),LaggedStart(*[FadeIn(d,scale=0.6) for d in colin],lag_ratio=0.06),rt=1.2)

        self.waitfor(3)  # highest total wins / chance Peter wins
        q=label("highest total wins --- what's the chance Peter wins?",20,ink)
        q.to_edge(DOWN,buff=0.9)
        self.P(Write(q),rt=1.4)

        self.waitfor(4)  # gave it to four models
        self.P(FadeOut(VGroup(peter,plab,colin,clab,q)),rt=0.5)
        chips=VGroup(pill("ChatGPT",gpt),pill("Gemini",gem),
                     pill("Grok",grok),pill("Claude",cld)).arrange(RIGHT,buff=0.34)
        for c in chips: self.P(FadeIn(c,shift=UP*0.2),rt=0.4)

        self.waitfor(5)  # three got it right
        three=label("three got it exactly right",22,good); three.next_to(chips,DOWN,buff=0.7)
        ck=VGroup(*[label("✓",24,good).next_to(chips[k],UP,buff=0.12) for k in (1,2,3)])
        self.P(Write(three),LaggedStart(*[FadeIn(x,scale=1.2) for x in ck],lag_ratio=0.15),rt=1.2)

        self.waitfor(6)  # the expensive one did not
        self.P(FadeOut(three),rt=0.3)
        xg=label("✗",26,bad).next_to(chips[0],UP,buff=0.12)
        miss=label("the most expensive one did not",22,bad); miss.next_to(chips,DOWN,buff=0.7)
        self.P(chips[0][0].animate.set_stroke(bad,3),FadeIn(xg,scale=1.2),Write(miss),rt=1.2)

        self.waitfor(7)  # reason is fascinating
        self.P(FadeOut(miss),rt=0.3)
        why=label("and the reason why is fascinating",20,dim); why.next_to(chips,DOWN,buff=0.7)
        self.P(Write(why),rt=1.2)
        self.finish(38.81+1.3)


class Sec2_Problem(Base):
    times=[0.0,6.24,11.14,17.2,24.1,29.26,34.24,41.92,48.68,55.73,60.01,64.54]
    def construct(self):
        self.start()
        self.waitfor(0)
        title=label("Problem 205 --- a dice bet",30); title.to_edge(UP,buff=0.5)
        self.P(Write(title),rt=1.0)

        self.waitfor(1)  # Peter nine 4-sided, low 9 high 36
        peter=dice_row([1,1,1,1,1,1,1,1,1],size=0.46,edge=peter_c,pip=peter_c).move_to(UP*1.7)
        plab=label("Peter --- nine 4-sided",18,peter_c); plab.next_to(peter,LEFT,buff=0.4)
        self.P(FadeIn(plab),FadeIn(peter),rt=1.0)
        prange=label("total: 9 ... 36",18,peter_c); prange.next_to(peter,RIGHT,buff=0.4)
        self.P(Write(prange),rt=0.9)

        self.waitfor(2)  # show all-ones=9 then all-fours=36
        self.P(*[Transform(peter[i],die(4,0.46,panel,peter_c,peter_c).move_to(peter[i])) for i in range(9)],rt=0.9)

        self.waitfor(3)  # Colin six 6-sided, low 6 high 36
        colin=dice_row([1,1,1,1,1,1],size=0.56,edge=colin_c,pip=colin_c).move_to(UP*0.4)
        clab=label("Colin --- six 6-sided",18,colin_c); clab.next_to(colin,LEFT,buff=0.4)
        crange=label("total: 6 ... 36",18,colin_c); crange.next_to(colin,RIGHT,buff=0.4)
        self.P(FadeIn(clab),FadeIn(colin),Write(crange),rt=1.0)

        self.waitfor(4)  # both reach 36 but Colin dips lower
        spread=label("both reach 36 --- but Colin spreads much wider",18,dim)
        spread.to_edge(DOWN,buff=1.4)
        self.P(Write(spread),rt=1.2)

        self.waitfor(5)  # the average trap
        self.P(FadeOut(VGroup(peter,plab,prange,colin,clab,crange,spread)),rt=0.5)
        avg=VGroup(label("Peter average  =  22.5",22,peter_c),
                   label("Colin average  =  21.0",22,colin_c)).arrange(DOWN,buff=0.35)
        avg.move_to(UP*0.6)
        self.P(Write(avg[0]),rt=0.8); self.P(Write(avg[1]),rt=0.8)

        self.waitfor(6)  # you'd think Peter wins, move on
        trap=label("higher average --- so Peter wins? not so fast.",20,gold)
        trap.next_to(avg,DOWN,buff=0.6)
        self.P(Write(trap),rt=1.3)

        self.waitfor(7)  # averages don't decide a matchup
        self.P(FadeOut(avg),FadeOut(trap),rt=0.5)
        nope=label("averages don't decide a single matchup",22,ink); nope.move_to(UP*0.4)
        self.P(Write(nope),rt=1.3)

        self.waitfor(8)  # what matters: how often Peter > Colin
        matt=label("what matters: how often is Peter's total higher?",20,dim)
        matt.next_to(nope,DOWN,buff=0.45)
        self.P(Write(matt),rt=1.4)

        self.waitfor(9)  # Colin spread changes picture
        self.P(FadeOut(nope),FadeOut(matt),rt=0.4)
        b=bar(0.5731,width=7.5).move_to(ORIGIN)
        plbl=label("Peter wins",16,peter_c).next_to(b,UP,buff=0.2).align_to(b,LEFT)
        clbl=label("Colin wins / ties",16,colin_c).next_to(b,UP,buff=0.2).align_to(b,RIGHT)
        self.P(FadeIn(b[0]),FadeIn(plbl),FadeIn(clbl),rt=0.6)

        self.waitfor(10)  # exact fraction
        exact=label("the answer is an exact fraction",20,ink); exact.next_to(b,DOWN,buff=0.5)
        self.P(GrowFromEdge(b[1],LEFT),rt=1.0); self.P(Write(exact),rt=0.9)

        self.waitfor(11)  # the word exact tripped the expensive one
        key=label("and that word --- exact --- is what tripped the expensive one",18,bad)
        key.next_to(exact,DOWN,buff=0.4)
        self.P(Write(key),rt=1.5)
        self.finish(68.8+1.3)


class Sec3_Gemini(Base):
    times=[0.58,11.15,17.44,20.53,26.81,34.74,40.63,45.38,50.61,55.2,61.39]
    def construct(self):
        self.start()
        self.waitfor(0)
        hdr=pill("Gemini",gem).to_corner(UL,buff=0.45)
        sub=label("Convolution --- build the distribution",20,dim).next_to(hdr,RIGHT,buff=0.45)
        self.P(FadeIn(hdr,shift=DOWN*0.2),Write(sub),rt=1.0)

        self.waitfor(1)  # don't list every combo, know how likely each total
        idea=label("don't list every roll --- find how likely each total is",20,gem)
        idea.move_to(UP*1.8)
        self.P(Write(idea),rt=1.4)

        self.waitfor(2)  # start with one die, equal faces
        axes=VGroup(); base=DOWN*1.5
        one=VGroup(*[Rectangle(width=0.5,height=0.9).set_fill(gem,0.8).set_stroke(width=0)
                     for _ in range(4)]).arrange(RIGHT,buff=0.12)
        one.next_to(base,UP,buff=0).move_to(LEFT*3.5+DOWN*0.8)
        olab=label("1 die --- flat",16,dim).next_to(one,DOWN,buff=0.2)
        self.P(FadeIn(olab),LaggedStart(*[GrowFromEdge(b,DOWN) for b in one],lag_ratio=0.1),rt=1.0)

        self.waitfor(3)  # add a second, totals spread
        heights=[0.2,0.45,0.7,0.95,0.7,0.45,0.2]
        two=VGroup(*[Rectangle(width=0.32,height=h).set_fill(gem,0.85).set_stroke(width=0) for h in heights]).arrange(RIGHT,buff=0.08,aligned_edge=DOWN)
        two.move_to(LEFT*0.2+DOWN*0.7)
        tlab=label("2 dice --- spreads",16,dim).next_to(two,DOWN,buff=0.2)
        self.P(FadeIn(tlab),LaggedStart(*[GrowFromEdge(b,DOWN) for b in two],lag_ratio=0.06),rt=1.0)

        self.waitfor(4)  # do nine and six times, bell shape
        hs=[0.12,0.22,0.36,0.52,0.68,0.82,0.93,0.99,0.99,0.93,0.82,0.68,0.52,0.36,0.22,0.12]
        bell=VGroup(*[Rectangle(width=0.22,height=h).set_fill(gem,0.9).set_stroke(width=0) for h in hs]).arrange(RIGHT,buff=0.05,aligned_edge=DOWN)
        bell.move_to(RIGHT*3.4+DOWN*0.7)
        blab=label("9 dice --- bell",16,dim).next_to(bell,DOWN,buff=0.2)
        self.P(FadeIn(blab),LaggedStart(*[GrowFromEdge(b,DOWN) for b in bell],lag_ratio=0.04),rt=1.2)

        self.waitfor(5)  # two compact tables
        self.P(FadeOut(VGroup(one,olab,two,tlab,bell,blab,idea)),rt=0.5)
        tbl=label("two compact tables --- every total + its count",20,gem); tbl.move_to(UP*0.3)
        self.P(Write(tbl),rt=1.3)

        self.waitfor(6)  # compare: ways Colin lower
        self.P(FadeOut(tbl),rt=0.3)
        comp=label("for each Peter total, count the ways Colin lands lower",18,dim)
        comp.move_to(UP*0.4)
        self.P(Write(comp),rt=1.4)

        self.waitfor(7)  # result exactly 0.5731441
        self.P(FadeOut(comp),rt=0.3)
        ans=label("0.5731441",40,good); ans.move_to(UP*0.2)
        self.P(Write(ans),rt=1.0)

        self.waitfor(8)  # Peter wins ~57%
        b=bar(0.5731,width=7).next_to(ans,DOWN,buff=0.5)
        pw=label("Peter wins ~57%",18,peter_c).next_to(b,DOWN,buff=0.3)
        self.P(FadeIn(b[0]),GrowFromEdge(b[1],LEFT),rt=1.0); self.P(FadeIn(pw),rt=0.6)

        self.waitfor(9)  # nine small beat six big
        beat=label("nine small dice really do beat six big ones",18,ink); beat.next_to(pw,DOWN,buff=0.3)
        self.P(Write(beat),rt=1.2)

        self.waitfor(10)  # least work -> crown
        crown=label("exact answer, least work --- the winner",18,gold); crown.next_to(beat,DOWN,buff=0.3)
        self.P(Write(crown),rt=1.3)
        self.finish(67.29+1.3)


class Sec4_Grok(Base):
    times=[0.0,8.1,12.28,20.56,24.76,31.45,37.08,46.93]
    def construct(self):
        self.start()
        self.waitfor(0)
        hdr=pill("Grok",grok).to_corner(UL,buff=0.45)
        sub=label("Brute force --- just count everything",20,dim).next_to(hdr,RIGHT,buff=0.45)
        self.P(FadeIn(hdr,shift=DOWN*0.2),Write(sub),rt=1.0)

        self.waitfor(1)  # nothing clever, count
        nc=label("no cleverness --- just count every outcome",20,grok); nc.move_to(UP*1.7)
        self.P(Write(nc),rt=1.3)

        self.waitfor(2)  # 4^9 ~ 260k, 6^6 ~ 46k
        counts=VGroup(
            label("Peter:  $4^9$  =  262,144 outcomes",22,peter_c),
            label("Colin:  $6^6$  =  46,656 outcomes",22,colin_c),
        ).arrange(DOWN,buff=0.4).move_to(UP*0.4)
        self.P(Write(counts[0]),rt=0.9); self.P(Write(counts[1]),rt=0.9)

        self.waitfor(3)  # totally manageable
        man=label("totally manageable for a computer",18,dim); man.next_to(counts,DOWN,buff=0.5)
        self.P(Write(man),rt=1.2)

        self.waitfor(4)  # tally each total
        self.P(FadeOut(VGroup(nc,counts,man)),rt=0.5)
        tally=label("tally how many ways each total can happen",20,grok); tally.move_to(UP*0.5)
        self.P(Write(tally),rt=1.3)

        self.waitfor(5)  # compare directly
        comp=label("then compare the two directly",18,dim); comp.next_to(tally,DOWN,buff=0.45)
        self.P(Write(comp),rt=1.2)

        self.waitfor(6)  # 0.5731441, exact same
        self.P(FadeOut(tally),FadeOut(comp),rt=0.4)
        ans=label("0.5731441",40,good); ans.move_to(UP*0.3)
        same=label("exactly right --- same as Gemini",20,ink); same.next_to(ans,DOWN,buff=0.45)
        self.P(Write(ans),rt=1.0); self.P(FadeIn(same),rt=0.8)

        self.waitfor(7)  # 2nd: more raw work, honest
        snd=label("just behind --- more raw work, but honest and correct",18,dim)
        snd.next_to(same,DOWN,buff=0.4)
        self.P(Write(snd),rt=1.5)
        self.finish(49.02+1.3)


class Sec5_Claude(Base):
    times=[0.68,8.93,16.67,22.24,25.38,31.63,35.49,43.7]
    def construct(self):
        self.start()
        self.waitfor(0)
        hdr=pill("Claude",cld).to_corner(UL,buff=0.45)
        sub=label("Correct --- just the long way",20,dim).next_to(hdr,RIGHT,buff=0.45)
        self.P(FadeIn(hdr,shift=DOWN*0.2),Write(sub),rt=1.0)

        self.waitfor(1)  # did NOT fail, got it right
        ok=label("Claude did not fail this one",24,good); ok.move_to(UP*1.6)
        self.P(Write(ok),rt=1.2)
        sub2=label("it just took the most laborious path",20,dim); sub2.next_to(ok,DOWN,buff=0.4)
        self.P(FadeIn(sub2),rt=0.9)

        self.waitfor(2)  # logic sound: count outcomes not averages
        self.P(FadeOut(VGroup(ok,sub2)),rt=0.4)
        logic=label("counts outcomes --- not averages",22,cld); logic.move_to(UP*0.9)
        self.P(Write(logic),rt=1.2)
        ins=label("the very insight the expensive model missed",18,dim); ins.next_to(logic,DOWN,buff=0.4)
        self.P(FadeIn(ins),rt=1.0)

        self.waitfor(3)  # built distributions, compared
        self.P(FadeOut(VGroup(logic,ins)),rt=0.4)
        built=label("built both distributions, compared them",20,ink); built.move_to(UP*0.5)
        self.P(Write(built),rt=1.2)

        self.waitfor(4)  # heavier method, full enumeration
        heavy=label("but leaned on heavy full enumeration",18,dim); heavy.next_to(built,DOWN,buff=0.45)
        self.P(Write(heavy),rt=1.2)

        self.waitfor(5)  # slower, more work
        slow=label("slower --- more work than it needed",18,dim); slow.next_to(heavy,DOWN,buff=0.3)
        self.P(Write(slow),rt=1.1)

        self.waitfor(6)  # but exactly 0.5731441 every time
        self.P(FadeOut(VGroup(built,heavy,slow)),rt=0.4)
        ans=label("0.5731441",40,good); ans.move_to(UP*0.3)
        every=label("the correct answer, every single time",18,ink); every.next_to(ans,DOWN,buff=0.45)
        self.P(Write(ans),rt=1.0); self.P(FadeIn(every),rt=0.8)

        self.waitfor(7)  # solid third, respectable
        third=label("a solid third --- right answer, just less efficient",18,dim)
        third.next_to(every,DOWN,buff=0.4)
        self.P(Write(third),rt=1.5)
        self.finish(52.08+1.3)


class Sec6_ChatGPT(Base):
    times=[0.46,7.2,11.65,17.48,22.12,26.51,33.08,41.19,45.59,51.04,56.06,63.62,68.95]
    def construct(self):
        self.start()
        self.waitfor(0)
        hdr=pill("ChatGPT",gpt).to_corner(UL,buff=0.45)
        sub=label("The \\$100B model --- the only miss",20,bad).next_to(hdr,RIGHT,buff=0.45)
        self.P(FadeIn(hdr,shift=DOWN*0.2),Write(sub),rt=1.0)

        self.waitfor(1)  # decided to simulate
        sim=label("instead of counting --- it simulated",22,gpt); sim.move_to(UP*1.7)
        self.P(Write(sim),rt=1.2)

        self.waitfor(2)  # loop: roll, check, repeat 2M
        loop=label("roll all the dice, check the winner, repeat",18,dim); loop.next_to(sim,DOWN,buff=0.4)
        self.P(Write(loop),rt=1.2)

        self.waitfor(3)  # rolling animation — show dice changing
        peter=dice_row([2,4,1,3,4,2,3,1,4],size=0.4,edge=peter_c,pip=peter_c).move_to(UP*0.3+LEFT*2)
        colin=dice_row([5,2,6,3,4,1],size=0.48,edge=colin_c,pip=colin_c).move_to(UP*0.3+RIGHT*2.2)
        self.P(FadeIn(peter),FadeIn(colin),rt=0.6)
        import random as _r; _r.seed(1)
        cnt=label("rolls: 1",18,gpt); cnt.move_to(DOWN*0.9)
        self.P(FadeIn(cnt),rt=0.4)
        for k,n in enumerate(["500,000","1,200,000","2,000,000"]):
            self.P(*[Transform(peter[i],die(_r.randint(1,4),0.4,panel,peter_c,peter_c).move_to(peter[i])) for i in range(9)],
                   *[Transform(colin[i],die(_r.randint(1,6),0.48,panel,colin_c,colin_c).move_to(colin[i])) for i in range(6)],
                   Transform(cnt,label(f"rolls: {n}",18,gpt).move_to(cnt)),rt=0.5)

        self.waitfor(4)  # Monte Carlo
        self.P(FadeOut(VGroup(peter,colin,cnt)),rt=0.4)
        mc=label("this is a Monte Carlo simulation",22,gpt); mc.move_to(UP*0.5)
        self.P(Write(mc),rt=1.2)

        self.waitfor(5)  # genuinely useful, fair
        fair=label("genuinely powerful --- used in finance, physics",18,dim); fair.next_to(mc,DOWN,buff=0.4)
        self.P(Write(fair),rt=1.3)

        self.waitfor(6)  # but this isn't too big, it's tiny
        self.P(FadeOut(VGroup(mc,fair)),rt=0.4)
        tiny=label("but this problem isn't too big --- it's tiny",22,bad); tiny.move_to(UP*0.6)
        self.P(Write(tiny),rt=1.3)
        other=label("three models counted it exactly in a split second",18,dim); other.next_to(tiny,DOWN,buff=0.4)
        self.P(FadeIn(other),rt=1.1)

        self.waitfor(7)  # approximation has a cost
        self.P(FadeOut(VGroup(tiny,other)),rt=0.4)
        cost=label("approximation has a cost",22,bad); cost.move_to(UP*1.2)
        self.P(Write(cost),rt=1.0)

        self.waitfor(8)  # reported 0.5728345 vs 0.5731441
        comp=VGroup(
            label("ChatGPT:  0.5728345  ✗",24,bad),
            label("exact:    0.5731441",22,good),
        ).arrange(DOWN,buff=0.35).next_to(cost,DOWN,buff=0.5)
        self.P(Write(comp[0]),rt=1.0)

        self.waitfor(9)  # off at 4th decimal
        self.P(Write(comp[1]),rt=0.9)
        off=label("off from the 4th decimal --- and drifts every run",18,dim)
        off.next_to(comp,DOWN,buff=0.4)

        self.waitfor(10)  # different seed different number
        self.P(Write(off),rt=1.3)

        self.waitfor(11)  # sledgehammer to a pencil problem
        self.P(FadeOut(VGroup(cost,comp,off)),rt=0.4)
        sledge=label("a sledgehammer for a problem that needed a pencil",20,bad)
        sledge.move_to(UP*0.2)
        self.P(Write(sledge),rt=1.4)

        self.waitfor(12)  # only one without the right answer
        only=label("the only model that missed the exact answer",18,dim)
        only.next_to(sledge,DOWN,buff=0.4)
        self.P(Write(only),rt=1.4)
        self.finish(77.95+1.3)


class Sec7_Eval(Base):
    times=[0.0,6.18,10.97,16.27,22.71,31.38]
    def construct(self):
        self.start()
        self.waitfor(0)
        title=label("Side by Side",30); title.to_edge(UP,buff=0.55)
        self.P(Write(title),rt=1.0)
        rows=[("Gemini",gem,"convolution","0.5731441 ✓",good),
              ("Grok",grok,"brute-force count","0.5731441 ✓",good),
              ("Claude",cld,"enumerate + count","0.5731441 ✓",good),
              ("ChatGPT",gpt,"Monte Carlo (2M)","0.5728345 ✗",bad)]
        cards=VGroup()
        for nm,col,meth,res,rc in rows:
            box=RoundedRectangle(corner_radius=0.1,width=10.6,height=0.92).set_fill(panel,1).set_stroke(col,1.6)
            name=label(nm,22,col).move_to(box.get_left()+RIGHT*1.2)
            m=label(meth,17,ink).move_to(box.get_center()+LEFT*0.3)
            r=label(res,18,rc).move_to(box.get_right()+LEFT*1.5)
            cards.add(VGroup(box,name,m,r))
        cards.arrange(DOWN,buff=0.3).move_to(DOWN*0.1)

        self.waitfor(1)  # Gemini
        self.P(FadeIn(cards[0],shift=RIGHT*0.25),rt=0.8)
        self.waitfor(2)  # Grok
        self.P(FadeIn(cards[1],shift=RIGHT*0.25),rt=0.8)
        self.waitfor(3)  # Claude
        self.P(FadeIn(cards[2],shift=RIGHT*0.25),rt=0.8)
        self.waitfor(4)  # ChatGPT
        self.P(FadeIn(cards[3],shift=RIGHT*0.25),rt=0.8)

        self.waitfor(5)  # 3 exact, one missed = the $100B one
        summ=label("three exact  \\cdot  one approximation  \\cdot  the \\$100B one missed",17,dim)
        summ.next_to(cards,DOWN,buff=0.5)
        self.P(Write(summ),rt=1.4)
        self.finish(37.55+1.3)


class Sec8_Verdict(Base):
    times=[0.0,11.4,19.18,25.29,32.34,41.27,44.43,48.27,52.27,63.81,71.65]
    def construct(self):
        self.start()
        head=label("The Verdict",32); head.to_edge(UP,buff=0.5)
        names=["Gemini","Grok","Claude","ChatGPT"]
        cols={"Gemini":gem,"Grok":grok,"Claude":cld,"ChatGPT":gpt}
        scs=VGroup()
        for nm in names:
            box=RoundedRectangle(corner_radius=0.08,width=4.4,height=0.78).set_fill(panel,1).set_stroke(gridc,1.2)
            lab=label(nm,20,cols[nm]).move_to(box.get_left()+RIGHT*0.95)
            scs.add(VGroup(box,lab))
        scs.arrange(DOWN,buff=0.22).to_edge(RIGHT,buff=0.6)
        focus=LEFT*3.2+UP*0.3
        def note(i,txt,col):
            nt=label(txt,15,col).move_to(scs[i][0].get_right()+LEFT*1.45)
            self.P(FadeIn(nt,shift=LEFT*0.15),rt=0.5)

        self.waitfor(0)  # winner Gemini
        self.P(Write(head),rt=0.8)
        self.P(*[FadeIn(r[0]) for r in scs],*[FadeIn(r[1]) for r in scs],rt=1.0)
        gf=pill("Gemini",gem,w=2.8,h=0.9,size=26).move_to(focus)
        crown=Polygon([-0.4,0,0],[-0.24,0.32,0],[0,0.06,0],[0.24,0.32,0],[0.4,0,0]).set_fill(gold,1).set_stroke(gold,1).scale(0.85)
        crown.next_to(gf,UP,buff=0.12)
        self.P(FadeIn(gf,shift=DOWN*0.2),rt=0.6); self.P(FadeIn(crown,shift=DOWN*0.3),rt=0.5)
        g1=label("cleanest solution --- convolution",17,gem); g1.next_to(gf,DOWN,buff=0.45)
        self.P(Write(g1),rt=1.0); note(0,"winner",gold)

        self.waitfor(1)  # Grok 2nd
        self.P(FadeOut(VGroup(gf,crown,g1)),rt=0.4)
        rf=pill("Grok",grok,w=2.8,h=0.9,size=26).move_to(focus)
        self.P(FadeIn(rf,shift=DOWN*0.2),rt=0.6)
        r1=label("same exact answer --- by brute force",17,ink); r1.next_to(rf,DOWN,buff=0.45)
        self.P(Write(r1),rt=1.0); note(1,"2nd, correct",grok)
        self.waitfor(2)  # nothing wrong, just less graceful
        r2=label("correct and honest --- just less graceful",17,dim); r2.next_to(r1,DOWN,buff=0.25)
        self.P(Write(r2),rt=1.0)

        self.waitfor(3)  # Claude 3rd, not failure
        self.P(FadeOut(VGroup(rf,r1,r2)),rt=0.4)
        cf=pill("Claude",cld,w=2.8,h=0.9,size=26).move_to(focus)
        self.P(FadeIn(cf,shift=DOWN*0.2),rt=0.6)
        c1=label("third is not failure --- it got it right",17,ink); c1.next_to(cf,DOWN,buff=0.45)
        self.P(Write(c1),rt=1.0); note(2,"correct, heavy",cld)
        self.waitfor(4)  # heaviest path, others cleaner
        c2=label("just the heaviest path to the same answer",17,dim); c2.next_to(c1,DOWN,buff=0.25)
        self.P(Write(c2),rt=1.0)

        self.waitfor(5)  # ChatGPT, $100B, only miss
        self.P(FadeOut(VGroup(cf,c1,c2)),rt=0.4)
        pf=pill("ChatGPT",gpt,w=2.8,h=0.9,size=26).move_to(focus)
        self.P(FadeIn(pf,shift=DOWN*0.2),rt=0.6)
        p1=label("the \\$100B model --- the only miss",17,bad); p1.next_to(pf,DOWN,buff=0.45)
        self.P(Write(p1),rt=1.0); note(3,"missed exact",bad)
        self.waitfor(6)  # reached for simulation on small problem
        p2=label("simulated a problem small enough to solve exactly",17,dim); p2.next_to(p1,DOWN,buff=0.25)
        self.P(Write(p2),rt=1.0)
        self.waitfor(7)  # lesson: money != judgment
        p3=label("more money doesn't mean better judgment of fit",17,bad); p3.next_to(p2,DOWN,buff=0.25)
        self.P(Write(p3),rt=1.0)
        self.waitfor(8)  # cheaper models saw it
        p4=label("the cheaper models saw it --- the expensive one overshot",17,gold); p4.next_to(p3,DOWN,buff=0.25)
        self.P(Write(p4),rt=1.1)

        self.waitfor(9)  # the answer
        self.P(FadeOut(VGroup(pf,p1,p2,p3,p4)),rt=0.4)
        fin1=label("Project Euler 205",22,dim); fin1.move_to(focus+UP*0.7)
        fin2=label("0.5731441",40,gold); fin2.next_to(fin1,DOWN,buff=0.35)
        b=bar(0.5731,width=5).next_to(fin2,DOWN,buff=0.4)
        self.P(FadeIn(fin1),rt=0.5); self.P(Write(fin2),rt=1.0)
        self.P(FadeIn(b[0]),GrowFromEdge(b[1],LEFT),rt=0.9)

        self.waitfor(10)  # $100B beaten by free, next time
        outro=label("the \\$100B model, beaten by free ones --- same four next time",17,dim)
        outro.to_edge(DOWN,buff=0.7)
        self.P(Write(outro),rt=1.5)
        self.finish(73.39+1.3)
