from pathlib import Path
import pcbnew as p, math, json
ROOT=Path(__file__).resolve().parents[1];b=p.LoadBoard(str(ROOT/'NFCC.kicad_pcb'))
b.BuildConnectivity();c=b.GetConnectivity()
allitems=list(b.GetTracks())+[pad for f in b.GetFootprints() for pad in f.Pads()]
uid=lambda a:str(a.m_Uuid.AsString())
original={uid(a):a for a in allitems}
seen=set();groups=[]
for item in allitems:
 if item.GetNetname() not in ['GND','VDDA'] or uid(item) in seen:continue
 group=[];todo=[item]
 while todo:
  a=todo.pop();k=uid(a);a=original.get(k,a)
  if k in seen:continue
  seen.add(k);group.append(a)
  todo.extend(x for x in c.GetConnectedItems(a) if uid(x) not in seen and not isinstance(x,p.ZONE))
 if any(isinstance(x,p.PCB_VIA) or isinstance(x,p.PAD) and x.GetAttribute()==p.PAD_ATTRIB_PTH for x in group):continue
 groups.append(group)
print('Isolated plane connection groups',len(groups))
shapes=[]
for item in allitems:
 try:shape=item.GetEffectiveShape(p.F_Cu)
 except:continue
 shapes.append((item,shape))
clear=p.FromMM(.205)
def safe_via(pos,net):
 circle=p.SHAPE_CIRCLE(pos,p.FromMM(.3))
 x,y=p.ToMM(pos)
 if not(60.8<x<149.2 and 60.8<y<129.2):return False
 if 116.025<x<119.975 and 98.775<y<101.225:return False
 if any(isinstance(a,p.PCB_VIA) and math.hypot(p.ToMM(a.GetPosition().x-pos.x),p.ToMM(a.GetPosition().y-pos.y))<.56 for a in allitems):return False
 if (107.7<x<111.3 or 112.7<x<116.3) and 68.4<y<71.6:return False
 for item,shape in shapes:
  if item.GetNetCode()==net and not isinstance(item,p.PAD):continue
  if isinstance(item,p.PAD):
   bb=item.GetBoundingBox();dx=max(bb.GetLeft()-pos.x,0,pos.x-bb.GetRight());dy=max(bb.GetTop()-pos.y,0,pos.y-bb.GetBottom())
   if dx*dx+dy*dy < p.FromMM(.51)**2:return False
  elif shape.Collide(circle,clear):return False
 return True
def safe_track(a,z,net):
 ax,ay=p.ToMM(a);zx,zy=p.ToMM(z)
 if max(ax,zx)+.1>116.325 and min(ax,zx)-.1<119.675 and max(ay,zy)+.1>99.075 and min(ay,zy)-.1<100.925:return False
 if any(max(ax,zx)+.1>lo and min(ax,zx)-.1<hi and max(ay,zy)+.1>68.7 and min(ay,zy)-.1<71.3 for lo,hi in [(108,111),(113,116)]):return False
 tr=p.PCB_TRACK(b);tr.SetStart(a);tr.SetEnd(z);tr.SetWidth(p.FromMM(.2));tr.SetLayer(p.F_Cu)
 shape=tr.GetEffectiveShape()
 for item,other in shapes:
  if item.GetNetCode()==net or not item.IsOnLayer(p.F_Cu):continue
  if other.Collide(shape,clear):return False
 return True
added=0;failed=[]
for g in groups:
 net=g[0].GetNetCode();anchors=[]
 for a in g:
  if isinstance(a,p.PCB_TRACK):anchors += [a.GetStart(),a.GetEnd()]
  elif isinstance(a,p.PAD): anchors.append(a.GetPosition())
 found=None
 for a in anchors:
  if safe_via(a,net):found=(a,a);break
 if found is None:
  for rad in [.5,.6,.7,.8,.9,1.,1.1,1.2,1.4,1.6,1.8,2.,2.3,2.6,3,3.5,4]:
   for a in anchors:
    for j in range(32):
     pos=p.VECTOR2I(a.x+p.FromMM(rad*math.cos(j*math.pi/16)),a.y+p.FromMM(rad*math.sin(j*math.pi/16)))
     if safe_via(pos,net) and safe_track(a,pos,net):found=(a,pos);break
    if found:break
   if found:break
 if not found:failed.append([(x.GetNetname(),str(x.m_Uuid.AsString())) for x in g]);continue
 a,pos=found
 via=p.PCB_VIA(b);via.SetPosition(pos);via.SetWidth(p.FromMM(.6));via.SetDrill(p.FromMM(.3));via.SetViaType(p.VIATYPE_THROUGH);via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNetCode(net);b.Add(via);shapes.append((via,via.GetEffectiveShape()));added+=1
 if a!=pos:
  tr=p.PCB_TRACK(b);tr.SetStart(a);tr.SetEnd(pos);tr.SetWidth(p.FromMM(.2));tr.SetLayer(p.F_Cu);tr.SetNetCode(net);b.Add(tr);shapes.append((tr,tr.GetEffectiveShape()))
p.SaveBoard(str(ROOT/'NFCC.kicad_pcb'),b)
proj=json.loads((ROOT/'NFCC.kicad_pro').read_text());proj['board']['design_settings']['rules']['min_track_width']=.15;(ROOT/'NFCC.kicad_pro').write_text(json.dumps(proj,indent=2))
print('Added',added,'plane vias; failed groups',len(failed));(ROOT/'checks/plane-connections.json').write_text(json.dumps({'added':added,'failed':failed},indent=2))
