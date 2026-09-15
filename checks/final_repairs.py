from pathlib import Path
from schlib import *
import pcbnew as p
R=Path(__file__).resolve().parents[1];d=read(R/'NFCC.kicad_pcb');d[:]=[a for a in d if not(isinstance(a,list) and get(a,'uuid') and get(a,'uuid')[1]=='9d31d16c-6ba8-4c49-a38a-45395ecc9a7b')];save(d,R/'NFCC.kicad_pcb');b=p.LoadBoard(str(R/'NFCC.kicad_pcb'))
def xy(a):return p.VECTOR2I(p.FromMM(a[0]),p.FromMM(a[1]))
def route(net,pts,w=.15):
 for a,z in zip(pts,pts[1:]):
  t=p.PCB_TRACK(b);t.SetStart(xy(a));t.SetEnd(xy(z));t.SetWidth(p.FromMM(w));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet(net));b.Add(t)
for t in b.GetTracks():
 u=str(t.m_Uuid.AsString())
 if u=='4689126e-c6c7-4e31-a6ea-9471ba2f973b':t.SetPosition(xy((117.5,96.9)))
 if u=='be56d8fc-11c9-4a43-bef1-343eeea1786c':t.SetEnd(xy((117.5,96.9)))
route('GND',[(118,98.7375),(118,98.05),(118.1952,97.8548),(118.824,97.8548)])
route('VDDA',[(118.676,102.145),(119.176,102.145)])
for a in b.FindFootprintByReference('U10').Pads():
 if a.GetNumber()=='6':a.SetLocalZoneConnection(p.ZONE_CONNECTION_NONE)
# Remove isolated outer-layer copper beneath header thermal spokes; the internal ground connection remains.
for z in b.Zones():
 if z.GetLayer()!=p.B_Cu:continue
 po=z.Outline()
 for x1,y1,x2,y2 in [(93.58,62.5,96.58,65.5),(126.12,120.26,134.2,123.26)]:
  h=po.NewHole(0)
  for x,y in [(x1,y1),(x1,y2),(x2,y2),(x2,y1)]:po.Append(p.FromMM(x),p.FromMM(y),0,h)
for t in b.GetDrawings():
 if isinstance(t,p.PCB_TEXT) and t.GetText()=='PWM 0-7':t.SetPosition(xy((137,119.5)))
p.SaveBoard(str(R/'NFCC.kicad_pcb'),b)
