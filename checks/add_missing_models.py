from pathlib import Path
import copy,json,hashlib,shutil
from schlib import *
root=Path(__file__).resolve().parents[1];p=root/'NFCC.kicad_pcb';b=read(p)
models={
 'U3':('DFN-6-1EP_3x3mm_P0.95mm_EP1.7x2.6mm.step',0,1,0),
 'U7':('BMP581.step',0,1,0.001),
 'U8':('W25N01GVZEIG.step',0,1,0),
 'U10':('LGA-12_2x2mm_P0.5mm.step',0,0.6829268293,0),
 'U11':('24CW1280T-I_OT.step',90,1,0.75),
}
backup=root/'checks/before-models';backup.mkdir(exist_ok=True)
if (backup/p.name).exists():raise SystemExit('Backup already exists; do not rerun blindly')
shutil.copy2(p,backup/p.name)
for f in items(b,'footprint'):
 ref=prop(f,'Reference')[2]
 if ref not in models:continue
 name,rot,sz,z=models[ref];assert not items(f,'model')
 m=['model',Q('${KIPRJMOD}/NFCC.3dshapes/'+name),['offset',['xyz','0','0',str(z)]],['scale',['xyz','1','1',str(sz)]],['rotate',['xyz','0','0',str(rot)]]]
 f.append(m)
 lp=root/'NFCC.pretty'/(f[1].split(':')[1]+'.kicad_mod');shutil.copy2(lp,backup/lp.name);lib=read(lp);assert not items(lib,'model');lib.append(copy.deepcopy(m));save(lib,lp)
save(b,p)
# Prove model additions are the only semantic board change.
a=read(backup/p.name);n=copy.deepcopy(b)
for f in items(n,'footprint'):
 if prop(f,'Reference')[2] in models:f[:]=[v for v in f if not (isinstance(v,list) and v and v[0]=='model')]
assert a==n
print('Added five models; all non-model board data unchanged.')
# Create a model inspection board, using copies of the real footprints.
import pcbnew
src=pcbnew.LoadBoard(str(p));test=pcbnew.BOARD()
for i,ref in enumerate(models):
 fp=pcbnew.FOOTPRINT(src.FindFootprintByReference(ref));fp.SetOrientationDegrees(0);fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(10+15*i),pcbnew.FromMM(10)));test.Add(fp)
for a,c in [((3,3),(78,3)),((78,3),(78,18)),((78,18),(3,18)),((3,18),(3,3))]:
 s=pcbnew.PCB_SHAPE();s.SetShape(pcbnew.SHAPE_T_SEGMENT);s.SetLayer(pcbnew.Edge_Cuts);s.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(a[0]),pcbnew.FromMM(a[1])));s.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(c[0]),pcbnew.FromMM(c[1])));s.SetWidth(pcbnew.FromMM(.05));test.Add(s)
# Absolute paths for temporary inspection file outside project root.
for f in test.GetFootprints():
 for m in f.Models():m.m_Filename=m.m_Filename.replace('${KIPRJMOD}',str(root))
pcbnew.SaveBoard(str(root/'checks/models-inspection.kicad_pcb'),test)

inspection=root/"checks/models-inspection.kicad_pcb"
inspection.write_text(inspection.read_text().replace("${KIPRJMOD}",str(root)))
