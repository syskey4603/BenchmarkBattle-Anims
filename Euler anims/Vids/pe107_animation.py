from manim import *
import numpy as np
import re
config.background_color = "#0A0A15"

mono="Consolas"
grok="#FF4500"; gpt="#10A37F"; gem="#4285F4"; cld="#E8925C"
gold="#FFD700"; bad="#FF5555"; good="#4ADE80"
ink="#F2F3F7"; dim="#FFB86C"; edgecol="#3A4A66"; panel="#10141F"

def fixtext(s):
    s=s.replace("\\"," ").replace("%",r"\%").replace("&",r"\&").replace("#",r"\#")
    s=s.replace("_",r"\_")
    s=re.sub(r'"([^"]*)"',r"``\1''",s)
    for a,b in [("→",r"$\rightarrow$"),("✓",r"$\checkmark$"),("✗",r"$\times$"),
                ("×",r"$\times$"),("≈",r"$\approx$"),("—","---"),("≠",r"$\neq$")]:
        s=s.replace(a,b)
    return s
def label(s,size=24,color=ink,font=None):
    t=Text(s,font_size=size,font=font) if font else Tex(fixtext(s),font_size=size)
    return t.set_color(color)
def pill(name,col,w=2.4,h=0.74,size=23):
    b=RoundedRectangle(corner_radius=0.12,width=w,height=h).set_fill(panel,1).set_stroke(col,2)
    return VGroup(b,label(name,size,col).move_to(b))

spots={
 "A":[-3.2,1.6],"B":[-0.6,2.4],"C":[-3.6,-1.2],"D":[-0.3,-0.2],
 "E":[2.4,1.7],"F":[-2.0,-2.6],"G":[2.8,-1.4]}
links=[("A","B",16),("A","C",12),("A","D",21),("B","D",17),("B","E",20),
 ("C","D",28),("C","F",31),("D","E",18),("D","F",19),("D","G",23),
 ("E","G",11),("F","G",27)]
tree_links=[("E","G",11),("A","C",12),("A","B",16),("B","D",17),("D","E",18),("D","F",19)]

def buildnodes(scale=1.0, shift=ORIGIN):
    nodes={}
    for k,(x,y) in spots.items():
        c=Circle(radius=0.28).set_fill(panel,1).set_stroke(ink,2)
        lbl=label(k,22,ink).move_to(c)
        g=VGroup(c,lbl).move_to(np.array([x,y,0])*scale+shift)
        nodes[k]=g
    return nodes

def buildedge(nodes,a,b,w,color=edgecol,width=2.5,show_w=True):
    p1=nodes[a].get_center(); p2=nodes[b].get_center()
    ln=Line(p1,p2).set_stroke(color,width)
    grp=VGroup(ln)
    if show_w:
        mid=(p1+p2)/2
        wl=label(str(w),16,dim).move_to(mid)
        bg=Circle(radius=0.2).set_fill("#0A0A15",1).set_stroke(width=0).move_to(mid)
        grp.add(bg,wl)
    return grp

class Base(Scene):
    times=[]
    def start(self):
        self.now=0.0
    def P(self,*a,rt=0.8,**k):
        self.play(*a,run_time=rt,**k); self.now+=rt
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
    times=[0.47,6.42,13.28,18.49,22.94,29.79,33.65]
    def construct(self):
        self.start()
        self.waitfor(0)
        title=label("Four models. One problem.",42); title.to_edge(UP,buff=1.1)
        ep=label("Episode 3",24,dim); ep.next_to(title,DOWN,buff=0.3)
        self.P(Write(title),rt=1.0); self.P(FadeIn(ep),rt=0.5)

        self.waitfor(1)
        chips=VGroup(pill("ChatGPT",gpt),pill("Gemini",gem),
                     pill("Grok",grok),pill("Claude",cld)).arrange(RIGHT,buff=0.34).shift(UP*0.2)
        for c in chips: self.P(FadeIn(c,shift=UP*0.25),rt=0.5)
        conds=label("same wording  ·  no hints",19,dim); conds.next_to(chips,DOWN,buff=0.6)
        self.P(FadeIn(conds),rt=0.6)

        self.waitfor(2)
        recap=label("last time",20,dim); recap.next_to(conds,DOWN,buff=0.7)
        self.P(FadeIn(recap),rt=0.5)
        cg=label("✓",24,good).next_to(chips[1],UP,buff=0.14)
        xg=label("✗",26,bad).next_to(chips[2],UP,buff=0.14)
        self.P(chips[1][0].animate.set_stroke(good,3),FadeIn(cg),rt=0.6)
        self.P(chips[2][0].animate.set_stroke(bad,2.5),FadeIn(xg),rt=0.6)

        self.waitfor(3)
        self.P(FadeOut(cg),FadeOut(xg),FadeOut(recap),
               chips[1][0].animate.set_stroke(gem,2),chips[2][0].animate.set_stroke(grok,2),rt=0.6)
        q=label("does the pattern flip again?",26,gold); q.next_to(conds,DOWN,buff=0.7)
        self.P(Write(q),rt=1.0)

        self.waitfor(4)
        self.P(FadeOut(q),rt=0.4)
        pe=label("from Project Euler --- problems that get harder as you go",20,dim)
        pe.next_to(conds,DOWN,buff=0.7)
        self.P(Write(pe),rt=1.2)

        self.waitfor(5)
        self.P(FadeOut(pe),rt=0.3)
        nj=label("not just who's right",22); nj.next_to(conds,DOWN,buff=0.7)
        self.P(Write(nj),rt=1.0)

        self.waitfor(6)
        tag=label("four models reach for completely different tools",20,dim)
        tag.next_to(nj,DOWN,buff=0.4)
        self.P(Write(tag),rt=1.3)
        self.finish(39.21+1.4)

class Sec2_Problem(Base):
    times=[0.0,7.81,12.53,18.7,26.53,32.38,39.02,45.21,49.84,53.5]
    def construct(self):
        self.start()
        self.waitfor(0)
        title=label("Problem 107 --- Minimal Network",30); title.to_edge(UP,buff=0.5)
        self.P(Write(title),rt=1.0)

        self.waitfor(1)
        nodes=buildnodes(scale=1.0)
        ng=VGroup(*nodes.values())
        self.P(LaggedStart(*[GrowFromCenter(n) for n in nodes.values()],lag_ratio=0.08),rt=1.4)
        edges=VGroup(*[buildedge(nodes,a,b,w) for a,b,w in links])
        self.P(LaggedStart(*[Create(e) for e in edges],lag_ratio=0.06),rt=1.6)
        cap=label("40 points  ·  every cable has a cost",18,dim); cap.to_edge(DOWN,buff=0.7)
        self.P(FadeIn(cap),rt=0.6)

        self.waitfor(2)
        self.P(FadeOut(cap),rt=0.3)
        tcap=label("(here's a small 7-point example)",17,dim); tcap.to_edge(DOWN,buff=0.7)
        self.P(FadeIn(tcap),rt=0.6)

        self.waitfor(3)
        self.P(FadeOut(tcap),rt=0.3)
        tot=label("full network cost: 261,832",24,gold); tot.to_edge(DOWN,buff=0.7)
        self.P(Write(tot),rt=1.0)

        self.waitfor(4)
        red=label("many of these are redundant",20,dim); red.move_to(tot)
        self.P(FadeOut(tot),rt=0.3); self.P(Write(red),rt=1.0)

        self.waitfor(5)
        cd=buildedge(nodes,"C","D",28)
        self.P(edges[5].animate.set_stroke(bad,4),rt=0.6)
        self.P(edges[5].animate.set_stroke(bad,0.5).set_opacity(0.15),rt=0.7)

        self.waitfor(6)
        self.P(FadeOut(red),rt=0.3)
        strip=label("strip away every redundant cable",20,dim); strip.to_edge(DOWN,buff=0.7)
        self.P(Write(strip),rt=1.0)
        mst_set={frozenset((a,b)) for a,b,_ in tree_links}
        anims=[]
        for e,(a,b,w) in zip(edges,links):
            if frozenset((a,b)) in mst_set:
                anims.append(e[0].animate.set_stroke(good,4))
            else:
                anims.append(e.animate.set_opacity(0.10))
        self.P(*anims,rt=1.4)

        self.waitfor(7)
        keep=label("but keep every point connected",20,good); keep.move_to(strip)
        self.P(FadeOut(strip),rt=0.3); self.P(Write(keep),rt=1.0)

        self.waitfor(8)
        self.P(FadeOut(keep),rt=0.3)
        sav=label("the answer = the maximum saving",22,gold); sav.to_edge(DOWN,buff=0.7)
        self.P(Write(sav),rt=1.0)

        self.waitfor(9)
        mst=label("this is a minimum spanning tree",22,ink); mst.next_to(sav,UP,buff=0.4)
        self.P(Write(mst),rt=1.2)
        self.finish(58.09+1.4)

class Sec3_Grok(Base):
    times=[0.0,8.54,13.66,18.03,22.6,32.87,35.46,44.87,47.55,53.27,57.87]
    def construct(self):
        self.start()
        self.waitfor(0)
        hdr=pill("Grok",grok).to_corner(UL,buff=0.45)
        sub=label("Kruskal's algorithm --- the classic fit",20,dim).next_to(hdr,RIGHT,buff=0.45)
        self.P(FadeIn(hdr,shift=DOWN*0.2),Write(sub),rt=1.0)

        self.waitfor(1)
        nodes=buildnodes(scale=0.85,shift=LEFT*2.2+DOWN*0.3)
        self.P(*[GrowFromCenter(n) for n in nodes.values()],rt=0.8)
        edges={}
        for a,b,w in links:
            edges[(a,b)]=buildedge(nodes,a,b,w,show_w=False)
        self.P(*[Create(e) for e in edges.values()],rt=1.0)

        self.waitfor(2)
        srt=VGroup(*[label(f"{a}-{b}  {w}",18,"#9FB6D4",font=mono)
                     for a,b,w in sorted(links,key=lambda e:e[2])])
        srt.arrange(DOWN,buff=0.13,aligned_edge=LEFT).to_edge(RIGHT,buff=1.0).shift(UP*0.2)
        slab=label("sorted by cost",16,grok); slab.next_to(srt,UP,buff=0.25)
        self.P(FadeIn(slab),LaggedStart(*[FadeIn(s,shift=RIGHT*0.1) for s in srt],lag_ratio=0.05),rt=1.4)

        self.waitfor(3)
        cursor=SurroundingRectangle(srt[0],buff=0.06).set_stroke(grok,2)
        self.P(Create(cursor),rt=0.5)

        self.waitfor(4)
        mst_set={frozenset((a,b)) for a,b,_ in tree_links}
        srt_edges=sorted(links,key=lambda e:e[2])
        for i in range(min(8,len(srt))):
            a,b,w=srt_edges[i]
            tgt=srt[i]
            self.P(cursor.animate.move_to(tgt),rt=0.22)
            ek=edges.get((a,b)) or edges.get((b,a))
            if frozenset((a,b)) in mst_set:
                self.P(tgt.animate.set_color(good),ek[0].animate.set_stroke(good,4),rt=0.25)
            else:
                self.P(tgt.animate.set_opacity(0.3),rt=0.18)

        self.waitfor(5)
        self.P(FadeOut(cursor),rt=0.3)

        self.waitfor(6)
        stop=label("stop the moment all points connect",18,dim); stop.to_edge(DOWN,buff=0.6)
        self.P(Write(stop),rt=1.0)

        self.waitfor(7)
        self.P(FadeOut(stop),rt=0.3)
        uf=label("union-find tracks which points share a group",18,grok); uf.to_edge(DOWN,buff=0.6)
        self.P(Write(uf),rt=1.2)

        self.waitfor(8)
        self.P(FadeOut(uf),rt=0.3)
        ee=label("early exit at 39 cables --- skip the rest",18,dim); ee.to_edge(DOWN,buff=0.6)
        self.P(Write(ee),rt=1.1)

        self.waitfor(9)
        self.P(FadeOut(ee),FadeOut(srt),FadeOut(slab),rt=0.4)
        ans=label("saving = 259,679  ✓",30,good); ans.move_to(RIGHT*2.5+UP*0.3)
        self.P(Write(ans),rt=1.0)

        self.waitfor(10)
        ms=label("~1 ms --- the most elegant of the four",18,dim); ms.next_to(ans,DOWN,buff=0.4)
        self.P(Write(ms),rt=1.2)
        self.finish(65.11+1.4)

class Sec4_ChatGPT(Base):
    times=[0.0,10.67,15.23,20.61,27.12,34.25,37.15,40.91,48.89,57.25]
    def construct(self):
        self.start()
        self.waitfor(0)
        hdr=pill("ChatGPT",gpt).to_corner(UL,buff=0.45)
        sub=label("Prim's algorithm --- grow outward",20,dim).next_to(hdr,RIGHT,buff=0.45)
        self.P(FadeIn(hdr,shift=DOWN*0.2),Write(sub),rt=1.0)
        nodes=buildnodes(scale=0.9)
        self.P(*[GrowFromCenter(n) for n in nodes.values()],rt=0.8)
        edges={}
        for a,b,w in links:
            edges[frozenset((a,b))]=buildedge(nodes,a,b,w,show_w=False)
        self.P(*[Create(e) for e in edges.values()],rt=0.9)

        self.waitfor(1)
        gl=label("grow the tree outward from one point",18,dim); gl.to_edge(DOWN,buff=0.6)
        self.P(FadeIn(gl),rt=0.7)

        self.waitfor(2)
        self.P(nodes["D"][0].animate.set_stroke(gpt,4).set_fill(gpt,0.25),rt=0.6)
        intree={"D"}

        self.waitfor(3)
        prim_seq=[("D","E"),("E","G"),("D","F"),("D","B") if False else ("B","D"),("A","B"),("A","C")]
        wmap={frozenset((a,b)):w for a,b,w in links}
        for a,b in prim_seq:
            newn = b if a in intree else a
            ek=edges[frozenset((a,b))]
            self.P(ek[0].animate.set_stroke(gpt,4),
                   nodes[newn][0].animate.set_stroke(gpt,4).set_fill(gpt,0.25),rt=0.45)
            intree.add(a); intree.add(b)

        self.waitfor(4)
        self.P(FadeOut(gl),rt=0.3)
        pq=label("a priority queue hands back the smallest instantly",18,gpt); pq.to_edge(DOWN,buff=0.6)
        self.P(Write(pq),rt=1.2)

        self.waitfor(5)
        self.P(FadeOut(pq),rt=0.3)
        gl2=VGroup(label("Grok: sorted the whole graph (global)",17,grok),
                   label("ChatGPT: grew one nearest point at a time (local)",17,gpt))
        gl2.arrange(DOWN,buff=0.25,aligned_edge=LEFT).to_edge(DOWN,buff=0.55)
        self.P(Write(gl2[0]),rt=0.9)

        self.waitfor(6)
        self.P(Write(gl2[1]),rt=0.9)

        self.waitfor(7)
        self.P(FadeOut(gl2),rt=0.3)
        ans=label("saving = 259,679  ✓",30,good); ans.to_edge(DOWN,buff=0.9)
        self.P(Write(ans),rt=1.0)

        self.waitfor(8)
        self.P(ans.animate.to_edge(DOWN,buff=1.3),rt=0.4)
        fast=label("a touch faster on the clock",18,dim); fast.next_to(ans,DOWN,buff=0.35)
        self.P(Write(fast),rt=1.0)

        self.waitfor(9)
        snd=label("second only because Kruskal is the cleaner fit here",17,dim); snd.next_to(fast,DOWN,buff=0.3)
        self.P(Write(snd),rt=1.2)
        self.finish(65.35+1.4)

class Sec5_Gemini(Base):
    times=[0.0,6.35,14.63,24.45,33.68,42.17,47.68,51.73,54.45,57.69,60.27,68.14,72.08]
    def construct(self):
        self.start()
        self.waitfor(0)
        hdr=pill("Gemini",gem).to_corner(UL,buff=0.45)
        sub=label("Right tool --- one wrong detail",20,dim).next_to(hdr,RIGHT,buff=0.45)
        self.P(FadeIn(hdr,shift=DOWN*0.2),Write(sub),rt=1.0)

        self.waitfor(1)
        rec=label("recognized it instantly as a spanning tree",20,gem); rec.move_to(UP*1.6)
        self.P(Write(rec),rt=1.2)

        self.waitfor(2)
        code=label("from scipy.sparse.csgraph import minimum_spanning_tree",20,gem,font=mono)
        code.scale(0.8).next_to(rec,DOWN,buff=0.5)
        box=SurroundingRectangle(code,buff=0.2).set_stroke(gem,2)
        self.P(Write(code),rt=1.0); self.P(Create(box),rt=0.6)

        self.waitfor(3)
        ok=label("and the tree it built was correct ✓",20,good); ok.next_to(box,DOWN,buff=0.5)
        self.P(Write(ok),rt=1.2)

        self.waitfor(4)
        self.P(FadeOut(rec),FadeOut(code),FadeOut(box),ok.animate.to_edge(UP,buff=1.2).scale(0.85),rt=0.6)
        bug=label("but the bug was in the saving",22,bad); bug.move_to(UP*0.9)
        self.P(Write(bug),rt=1.0)

        self.waitfor(5)
        self.P(FadeOut(bug),rt=0.3)
        rows=["-,16,12,...","16,-,-,...","12,-,-,..."]
        mat=VGroup(*[label(r,20,"#9FB6D4",font=mono) for r in rows]).arrange(DOWN,buff=0.18)
        mat.move_to(UP*0.3)
        mlab=label("the table is symmetric",18,dim); mlab.next_to(mat,UP,buff=0.3)
        self.P(FadeIn(mlab),FadeIn(mat),rt=1.0)

        self.waitfor(6)
        tw=label("every cable appears twice --- once each direction",18,dim); tw.next_to(mat,DOWN,buff=0.4)
        self.P(Write(tw),rt=1.2)

        self.waitfor(7)
        rule=label("so add it all, then divide by two",20,good); rule.next_to(tw,DOWN,buff=0.35)
        self.P(Write(rule),rt=1.0)

        self.waitfor(8)
        self.P(FadeOut(mat),FadeOut(mlab),FadeOut(tw),rule.animate.to_edge(UP,buff=1.6).scale(0.8),rt=0.5)
        forgot=label("Gemini forgot the ÷ 2",24,bad); forgot.move_to(UP*0.6)
        self.P(Write(forgot),rt=1.0)

        self.waitfor(9)
        dbl=label("261,832  ×  2  =  523,664 baseline",20,bad); dbl.next_to(forgot,DOWN,buff=0.4)
        self.P(Write(dbl),rt=1.2)

        self.waitfor(10)
        thr=label("a doubled total wrecks the final saving",18,dim); thr.next_to(dbl,DOWN,buff=0.35)
        self.P(Write(thr),rt=1.1)

        self.waitfor(11)
        self.P(FadeOut(forgot),FadeOut(dbl),FadeOut(thr),FadeOut(ok),rt=0.4)
        wrong=label("reported 521,511  ✗",30,bad); wrong.move_to(UP*0.2)
        right=label("correct was 259,679",20,dim); right.next_to(wrong,DOWN,buff=0.4)
        self.P(Write(wrong),rt=1.0); self.P(FadeIn(right),rt=0.6)

        self.waitfor(12)
        les=label("right tool, right tree --- one missing division sank it",18,dim)
        les.next_to(right,DOWN,buff=0.4)
        self.P(Write(les),rt=1.4)
        self.finish(74.09+1.4)

class Sec6_Claude(Base):
    times=[0.0,7.02,11.32,15.96,23.13,27.27,33.4,40.69,46.16,54.3,64.41,66.07]
    def construct(self):
        self.start()
        self.waitfor(0)
        hdr=pill("Claude",cld).to_corner(UL,buff=0.45)
        sub=label("Tried to prove the minimum",20,dim).next_to(hdr,RIGHT,buff=0.45)
        self.P(FadeIn(hdr,shift=DOWN*0.2),Write(sub),rt=1.0)

        self.waitfor(1)
        prove=label("not just find the tree --- prove it's the minimum",22,cld); prove.move_to(UP*1.7)
        self.P(Write(prove),rt=1.3)

        self.waitfor(2)
        expl=label("so explore the possible trees directly",19,dim); expl.next_to(prove,DOWN,buff=0.45)
        self.P(Write(expl),rt=1.0)

        self.waitfor(3)
        self.P(FadeOut(expl),rt=0.3)
        root=Dot(radius=0.10,color=cld).move_to(UP*1.0)
        self.P(GrowFromCenter(root),rt=0.4)
        layer=[root]
        all_dots=VGroup(root); all_lines=VGroup()
        for d in range(3):
            new=[]
            for nd in layer:
                for dx in (-1,1):
                    child=Dot(radius=0.08,color=cld).move_to(nd.get_center()+DOWN*0.8+RIGHT*dx*(1.6/(d+1)))
                    ln=Line(nd.get_center(),child.get_center()).set_stroke(edgecol,1.5)
                    all_dots.add(child); all_lines.add(ln); new.append(child)
            layer=new
            self.P(*[Create(l) for l in all_lines[-len(new):]],
                   *[GrowFromCenter(c) for c in new],rt=0.5)
        inc=label("include / exclude each edge",17,dim); inc.to_edge(DOWN,buff=0.7)
        self.P(FadeIn(inc),rt=0.5)

        self.waitfor(4)
        self.P(FadeOut(inc),rt=0.3)
        fine=label("for 7 points --- totally fine",18,good); fine.to_edge(DOWN,buff=0.7)
        self.P(Write(fine),rt=0.9)

        self.waitfor(5)
        self.P(FadeOut(fine),rt=0.3)
        layer2=layer
        for d in range(2):
            new=[]
            for nd in layer2:
                for dx in (-1,1):
                    child=Dot(radius=0.05,color=bad).move_to(nd.get_center()+DOWN*0.6+RIGHT*dx*0.25)
                    ln=Line(nd.get_center(),child.get_center()).set_stroke(bad,1)
                    all_dots.add(child); all_lines.add(ln); new.append(child)
            layer2=new
            self.P(*[Create(l) for l in all_lines[-len(new):]],
                   *[GrowFromCenter(c) for c in new],rt=0.4)
        n40=label("but with 40 points...",20,bad); n40.to_edge(DOWN,buff=0.7)
        self.P(Write(n40),rt=0.9)

        self.waitfor(6)
        self.P(FadeOut(n40),rt=0.3)
        big=label("possible trees: a number with dozens of digits",19,bad); big.to_edge(DOWN,buff=0.7)
        self.P(Write(big),rt=1.2)

        self.waitfor(7)
        self.P(FadeOut(big),rt=0.3)
        univ=label("more than there's time in the universe to check",19,bad); univ.to_edge(DOWN,buff=0.7)
        self.P(Write(univ),rt=1.2)

        self.waitfor(8)
        self.P(FadeOut(univ),rt=0.3)
        prune=label("light pruning --- nowhere near aggressive enough",18,dim); prune.to_edge(DOWN,buff=0.7)
        self.P(Write(prune),rt=1.2)

        self.waitfor(9)
        self.P(FadeOut(prune),FadeOut(all_dots),FadeOut(all_lines),FadeOut(root),
               FadeOut(prove),rt=0.5)
        run=label("it just kept running...",24,bad); run.move_to(UP*0.2)
        self.P(Write(run),rt=1.0)

        self.waitfor(10)
        stop=label("...and never finished",22,bad); stop.next_to(run,DOWN,buff=0.4)
        self.P(Write(stop),rt=1.0)

        self.waitfor(11)
        les=label("the smartest-sounding approach --- the one that never answers",18,dim)
        les.next_to(stop,DOWN,buff=0.4)
        self.P(Write(les),rt=1.4)
        self.finish(69.7+1.4)

class Sec7_Eval(Base):
    times=[0.0,7.14,16.99,29.56,36.49]
    def construct(self):
        self.start()
        self.waitfor(0)
        title=label("Side by Side",30); title.to_edge(UP,buff=0.55)
        self.P(Write(title),rt=1.0)
        rows=[("Grok",grok,"Kruskal + union-find","259,679 ✓",good),
              ("ChatGPT",gpt,"Prim + heap","259,679 ✓",good),
              ("Gemini",gem,"scipy, forgot ÷2","521,511 ✗",bad),
              ("Claude",cld,"enumerate all trees","never finished",bad)]
        cards=VGroup()
        for nm,col,meth,res,rc in rows:
            box=RoundedRectangle(corner_radius=0.1,width=10.4,height=0.92).set_fill(panel,1).set_stroke(col,1.6)
            name=label(nm,22,col).move_to(box.get_left()+RIGHT*1.25)
            m=label(meth,17,ink).move_to(box.get_center()+LEFT*0.3)
            r=label(res,18,rc).move_to(box.get_right()+LEFT*1.5)
            cards.add(VGroup(box,name,m,r))
        cards.arrange(DOWN,buff=0.3).move_to(DOWN*0.1)

        self.waitfor(1)
        self.P(FadeIn(cards[0],shift=RIGHT*0.25),rt=0.8)
        self.W(1.0)
        self.waitfor(2)
        self.P(FadeIn(cards[1],shift=RIGHT*0.25),rt=0.8)
        self.waitfor(3)
        self.P(FadeIn(cards[2],shift=RIGHT*0.25),rt=0.8)
        self.waitfor(4)
        self.P(FadeIn(cards[3],shift=RIGHT*0.25),rt=0.8)
        summ=label("two correct  ·  one wrong  ·  one never finished",18,dim)
        summ.next_to(cards,DOWN,buff=0.5)
        self.P(Write(summ),rt=1.2)
        self.finish(41.34+1.4)

class Sec8_Verdict(Base):
    times=[0.0,5.68,12.59,19.1,27.45,35.44,43.94,47.1,54.2,61.04,65.67,73.76,85.68,92.9]
    def construct(self):
        self.start()
        head=label("The Verdict",32); head.to_edge(UP,buff=0.5)
        names=["Grok","ChatGPT","Gemini","Claude"]
        cols={"Grok":grok,"ChatGPT":gpt,"Gemini":gem,"Claude":cld}
        scs=VGroup()
        for nm in names:
            box=RoundedRectangle(corner_radius=0.08,width=4.4,height=0.78).set_fill(panel,1).set_stroke("#2A3450",1.2)
            lab=label(nm,20,cols[nm]).move_to(box.get_left()+RIGHT*0.9)
            scs.add(VGroup(box,lab))
        scs.arrange(DOWN,buff=0.22).to_edge(RIGHT,buff=0.6)
        focus=LEFT*3.2+UP*0.3
        def note(i,txt,col):
            nt=label(txt,15,col).move_to(scs[i][0].get_right()+LEFT*1.45)
            self.P(FadeIn(nt,shift=LEFT*0.15),rt=0.5)

        self.waitfor(0)
        self.P(Write(head),rt=0.8)
        self.P(*[FadeIn(r[0]) for r in scs],*[FadeIn(r[1]) for r in scs],rt=1.0)
        gf=pill("Grok",grok,w=2.8,h=0.9,size=26).move_to(focus)
        crown=Polygon([-0.4,0,0],[-0.24,0.32,0],[0,0.06,0],[0.24,0.32,0],[0.4,0,0]).set_fill(gold,1).set_stroke(gold,1).scale(0.85)
        crown.next_to(gf,UP,buff=0.12)
        self.P(FadeIn(gf,shift=DOWN*0.2),rt=0.6)
        self.P(FadeIn(crown,shift=DOWN*0.3),rt=0.6); note(0,"winner",gold)

        self.waitfor(1)
        p1=label("the right classic --- Kruskal's",17,ink); p1.next_to(gf,DOWN,buff=0.45)
        self.P(Write(p1),rt=1.0)
        self.waitfor(2)
        p2=label("clean union-find + a smart early exit",17,dim); p2.next_to(p1,DOWN,buff=0.22)
        self.P(Write(p2),rt=1.0)
        self.waitfor(3)
        p3=label("no overthinking --- textbook tool, used right",17,grok); p3.next_to(p2,DOWN,buff=0.22)
        self.P(Write(p3),rt=1.0)
        self.waitfor(4)
        p4=label("a table of edges --- sort and build",17,dim); p4.next_to(p3,DOWN,buff=0.22)
        self.P(Write(p4),rt=1.0)

        self.waitfor(5)
        self.P(FadeOut(VGroup(gf,crown,p1,p2,p3,p4)),rt=0.4)
        cf=pill("ChatGPT",gpt,w=2.8,h=0.9,size=26).move_to(focus)
        self.P(FadeIn(cf,shift=DOWN*0.2),rt=0.6)
        q1=label("a very close second",17,ink); q1.next_to(cf,DOWN,buff=0.45)
        self.P(Write(q1),rt=1.0); note(1,"2nd, nearly tied",gpt)

        self.waitfor(6)
        q2=label("Prim's --- just as correct, a hair faster",17,dim); q2.next_to(q1,DOWN,buff=0.22)
        self.P(Write(q2),rt=1.0)
        self.waitfor(7)
        q3=label("Kruskal was just the more elegant fit here",17,gpt); q3.next_to(q2,DOWN,buff=0.22)
        self.P(Write(q3),rt=1.0)
        self.waitfor(8)
        q4=label("the closest top two of any episode",17,gold); q4.next_to(q3,DOWN,buff=0.22)
        self.P(Write(q4),rt=1.0)

        self.waitfor(9)
        self.P(FadeOut(VGroup(cf,q1,q2,q3,q4)),rt=0.4)
        mf=pill("Gemini",gem,w=2.8,h=0.9,size=26).move_to(focus)
        self.P(FadeIn(mf,shift=DOWN*0.2),rt=0.6)
        r1=label("so close --- and it stings",17,ink); r1.next_to(mf,DOWN,buff=0.45)
        self.P(Write(r1),rt=1.0); note(2,"wrong saving",bad)

        self.waitfor(10)
        r2=label("good instinct, correct tree --- but forgot ÷2",17,bad); r2.next_to(r1,DOWN,buff=0.22)
        self.P(Write(r2),rt=1.0)
        self.waitfor(11)
        r3=label("a right algorithm read wrong is still wrong",17,dim); r3.next_to(r2,DOWN,buff=0.22)
        self.P(Write(r3),rt=1.0)

        self.waitfor(12)
        self.P(FadeOut(VGroup(mf,r1,r2,r3)),rt=0.4)
        clf=pill("Claude",cld,w=2.8,h=0.9,size=26).move_to(focus)
        self.P(FadeIn(clf,shift=DOWN*0.2),rt=0.6)
        s1=label("deepest understanding --- never finished",17,ink); s1.next_to(clf,DOWN,buff=0.45)
        self.P(Write(s1),rt=1.0); note(3,"did not finish",bad)
        s2=label("rigor that runs forever isn't an answer",17,dim); s2.next_to(s1,DOWN,buff=0.22)
        self.P(Write(s2),rt=1.0)

        self.waitfor(13)
        self.P(FadeOut(VGroup(clf,s1,s2)),rt=0.4)
        fin1=label("Project Euler 107",22,dim); fin1.move_to(focus+UP*0.5)
        fin2=label("259,679",40,gold); fin2.next_to(fin1,DOWN,buff=0.35)
        fbox=SurroundingRectangle(fin2,buff=0.2).set_stroke(gold,2)
        self.P(FadeIn(fin1),rt=0.6); self.P(Write(fin2),rt=1.0); self.P(Create(fbox),rt=0.6)
        outro=label("Grok takes the crown --- same four, next time",18,dim); outro.to_edge(DOWN,buff=0.7)
        self.P(Write(outro),rt=1.4)
        self.finish(95.62+1.4)
