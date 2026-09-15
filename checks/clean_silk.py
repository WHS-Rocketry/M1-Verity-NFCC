from pathlib import Path
import pcbnew as p, math, json
ROOT=Path(__file__).resolve().parents[1];b=p.LoadBoard(str(ROOT/'NFCC.kicad_pcb'))
def rect(item,pad=0):
 bb=item.GetBoundingBox();return (p.ToMM(bb.GetLeft())-pad,p.ToMM(bb.GetTop())-pad,p.ToMM(bb.GetRight())+pad,p.ToMM(bb.GetBottom())+pad)
def intersects(a,c):return a[0]<c[2] and a[2]>c[0] and a[1]<c[3] and a[3]>c[1]
# Move literal import placeholders off the printing layer.
for f in b.GetFootprints():
 for g in f.GraphicalItems():
  if hasattr(g,'GetText') and g.GetText() in ['*','**','***','REF**','%R']:g.SetLayer(p.F_Fab)
pads=[rect(pad,.13) for f in b.GetFootprints() for pad in f.Pads()]
for f in b.GetFootprints():
 for g in f.GraphicalItems():
  if g.GetLayer()==p.F_SilkS and any(intersects(rect(g),q) for q in pads):g.SetLayer(p.F_Fab)
obstacles=pads+[rect(g,.08) for f in b.GetFootprints() for g in f.GraphicalItems() if g.GetLayer()==p.F_SilkS]
texts=[g for g in b.GetDrawings() if isinstance(g,p.PCB_TEXT) and g.GetLayer()==p.F_SilkS]
for t in texts:
 if t.GetText()=='PWM 0-7':t.SetPosition(p.VECTOR2I(p.FromMM(138),p.FromMM(119)))
 if t.GetText().startswith('NFCC  |'):t.SetText('NFCC / ROUTING DRAFT');t.SetPosition(p.VECTOR2I(p.FromMM(106),p.FromMM(76)))
 obstacles.append(rect(t,.08))
for f in sorted(b.GetFootprints(),key=lambda x:(not x.GetReference().startswith(('U','NFCC','J','PWM','SW','TELEM','I2C')),x.GetReference())):
 t=f.Reference()
 if not t.IsVisible():continue
 x,y=p.ToMM(f.GetPosition()); bb=f.GetBoundingBox(False,False)
 cand=[p.ToMM(t.GetPosition()),(x,y),(x,p.ToMM(bb.GetBottom())+.9),(p.ToMM(bb.GetLeft())-len(t.GetText())*.3-.3,y),(p.ToMM(bb.GetRight())+len(t.GetText())*.3+.3,y)]
 for rad in [2,3,4,5,6]:
  cand.extend((x+rad*math.cos(a*math.pi/8),y+rad*math.sin(a*math.pi/8)) for a in range(16))
 for xx,yy in cand:
  t.SetPosition(p.VECTOR2I(p.FromMM(xx),p.FromMM(yy)));r=rect(t,.1)
  if r[0]<60.4 or r[2]>149.6 or r[1]<60.4 or r[3]>129.6:continue
  if not any(intersects(r,q) for q in obstacles):obstacles.append(r);break
 else:t.SetLayer(p.F_Fab)
p.SaveBoard(str(ROOT/'NFCC.kicad_pcb'),b)
p.ExportSpecctraDSN(b,str(ROOT/'checks/placement.dsn'))
