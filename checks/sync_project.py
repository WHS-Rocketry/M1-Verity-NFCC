from pathlib import Path
import pcbnew as p
from schlib import *
ROOT=Path(__file__).resolve().parents[1];b=p.LoadBoard(str(ROOT/'NFCC.kicad_pcb'));s=read(ROOT/'NFCC.kicad_sch');syms={prop(x,'Reference')[2]:x for x in items(s,'symbol')}
for f in b.GetFootprints():
 ref=f.GetReference()
 if ref not in syms:
  f.SetAttributes(f.GetAttributes()|p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_BOM);continue
 sym=syms[ref]
 for pp in items(sym,'property'):
  if pp[1] in ['Reference','Value','Footprint']:continue
  f.SetField(str(pp[1]),str(pp[2]));f.GetField(str(pp[1])).SetVisible(False)
 f.SetAttributes((f.GetAttributes() | p.FP_EXCLUDE_FROM_BOM) if str(get(sym,'in_bom')[1])=='no' else (f.GetAttributes() & ~p.FP_EXCLUDE_FROM_BOM))
 name=str(f.GetFPID().GetLibItemName()).split('__')[0]+'__'+ref
 f.SetFPID(p.LIB_ID('NFCC',name));prop(sym,'Footprint')[2]=Q('NFCC:'+name)
 p.FootprintSave(str(ROOT/'NFCC.pretty'),f)
save(s,ROOT/'NFCC.kicad_sch');p.SaveBoard(str(ROOT/'NFCC.kicad_pcb'),b)
# Match KiCad's escaped slash spelling in schematic-generated net names.
d=read(ROOT/'NFCC.kicad_pcb')
def walk(x):
 if not isinstance(x,list):return
 if x and x[0]=='net' and len(x)>1 and isinstance(x[1],str):x[1]=Q(x[1].replace('/','{slash}'))
 for v in x:walk(v)
walk(d);save(d,ROOT/'NFCC.kicad_pcb')
print('Synced local footprint library, schematic fields, board-only holes and net-name escaping')

# KiCad's footprint export retains board coordinates in embedded rule areas.
for f in b.GetFootprints():
 name=str(f.GetFPID().GetLibItemName());path=ROOT/'NFCC.pretty'/(name+'.kicad_mod')
 if not path.exists():continue
 d=read(path);zones=items(d,'zone')
 if not zones:continue
 assert abs(f.GetOrientationDegrees())<.001
 x,y=p.ToMM(f.GetPosition())
 for z in zones:
  for poly in items(z,'polygon'):
   for pt in items(get(poly,'pts'),'xy'):pt[1]=float(pt[1])-x;pt[2]=float(pt[2])-y
 save(d,path)
