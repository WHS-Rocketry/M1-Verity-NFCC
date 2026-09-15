from pathlib import Path
from schlib import *
import pcbnew as p,json
R=Path(__file__).resolve().parents[1];d=read(R.parent/'revision-b/NFCC.kicad_pcb');d[:]=[a for a in d if not(isinstance(a,list) and a[0] in ['segment','arc','via','zone','gr_text'])]
for a in items(d,'gr_line'):
 if get(a,'layer')[1]=='Edge.Cuts':
  for tag in ['start','end']:
   at=get(a,tag)
   if float(at[1])==50:at[1]=60
   if float(at[2])==50:at[2]=60
# Preserve the user's logo as silkscreen artwork, resized to fit the smaller board.
f=next(a for a in items(d,'footprint') if prop(a,'Reference')[2]=='G***')
pts=[pt for poly in items(f,'fp_poly') for pt in items(get(poly,'pts'),'xy')]
xs=[float(pt[1]) for pt in pts];ys=[float(pt[2]) for pt in pts];cx=(min(xs)+max(xs))/2;cy=(min(ys)+max(ys))/2;scale=12/max(max(xs)-min(xs),max(ys)-min(ys))
for pt in pts:pt[1]=(float(pt[1])-cx)*scale;pt[2]=(float(pt[2])-cy)*scale
for poly in items(f,'fp_poly'):get(poly,'layer')[1]=Q('F.SilkS')
save(d,R/'NFCC.kicad_pcb');b=p.LoadBoard(str(R/'NFCC.kicad_pcb'))
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
pos={'J1':(147.33,88,90),'J2':(147.33,101,90),'J3':(66,80,90),'TELEM2':(63.5,96,270),'I2C5':(146.5,74,90),'U1':(140,109,180),'C57':(146,112,90),'C58':(146,108,90),'D3':(141,115,90),'R54':(141,118,0),'R47':(144,115,90),'R48':(144,118,90),'SWD2':(90,64,90),'SW6':(118,63,0),'R38':(125,62.5,0),'U11':(127,91.5,0),'C19':(124,94,90),'G***':(79,74,0),'H1':(64,64,0),'H2':(146,64,0),'H3':(146,126,0),'H4':(64,126,0)}
for ref,(x,y,a) in pos.items():
 f=b.FindFootprintByReference(ref);f.SetPosition(xy(x,y));f.SetOrientationDegrees(a)
for f in b.GetFootprints():
 f.Reference().SetPosition(f.GetPosition());f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
for net,layer in [('GND',p.In1_Cu),('VDDA',p.In2_Cu)]:
 z=p.ZONE(b);z.SetLayer(layer);z.SetNet(b.FindNet(net));z.SetLocalClearance(p.FromMM(.25));z.SetThermalReliefGap(p.FromMM(.25));z.SetThermalReliefSpokeWidth(p.FromMM(.3));z.SetMinThickness(p.FromMM(.2));z.SetIslandRemovalMode(0);po=z.Outline();po.NewOutline()
 for x,y in [(60.5,60.5),(149.5,60.5),(149.5,129.5),(60.5,129.5)]:po.Append(p.FromMM(x),p.FromMM(y))
 b.Add(z)
def route(net,w,pts):
 for a,z in zip(pts,pts[1:]):
  t=p.PCB_TRACK(b);t.SetStart(xy(*a));t.SetEnd(xy(*z));t.SetWidth(p.FromMM(w));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet(net));b.Add(t)
route('USB_DP',.2,[(108.675,87),(111.175,87)])
route('USB_DM',.2,[(108.675,87.5),(110.075,87.5),(111.175,88.6)])
route('Net-(J1-D+)',.2,[(112.825,87),(114,87),(114.85,87.85),(145,87.85),(145.15,88),(145.87,88)])
route('Net-(J1-D-)',.2,[(112.825,88.6),(114,88.6),(114.25,88.35),(144.5,88.35),(144.8,88.65),(145.87,88.65)])
# Preserve the compact regulator switching/boot connections from revision B.
old=p.LoadBoard(str(R.parent/'revision-b/NFCC.kicad_pcb'))
for t in old.GetTracks():
 if t.GetNetname() in ['Net-(U2-SW)','Net-(U2-BOOT)'] and not isinstance(t,p.PCB_VIA):
  route(t.GetNetname(),p.ToMM(t.GetWidth()),[p.ToMM(t.GetStart()),p.ToMM(t.GetEnd())])
p.SaveBoard(str(R/'NFCC.kicad_pcb'),b);(R/'checks/positions.json').write_text(json.dumps(pos,indent=2));print('90 x 70 mm outline and adjacent USB ports placed')
