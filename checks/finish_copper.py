from pathlib import Path
import pcbnew as p,json,math
R=Path(__file__).resolve().parents[1];b=p.LoadBoard(str(R/'NFCC.kicad_pcb'))
# Outer ground copper complements the uninterrupted internal ground plane.
for layer in [p.F_Cu,p.B_Cu]:
 z=p.ZONE(b);z.SetLayer(layer);z.SetNet(b.FindNet('GND'));z.SetLocalClearance(p.FromMM(.25));z.SetThermalReliefGap(p.FromMM(.25));z.SetThermalReliefSpokeWidth(p.FromMM(.35));z.SetMinThickness(p.FromMM(.2));z.SetIslandRemovalMode(0);poly=z.Outline();poly.NewOutline()
 for x,y in [(60.5,60.5),(149.5,60.5),(149.5,129.5),(60.5,129.5)]:poly.Append(p.FromMM(x),p.FromMM(y))
 b.Add(z)
# Sparse perimeter and connector stitching; avoid all pads and foreign copper on every layer.
obs=list(b.GetTracks())+[a for f in b.GetFootprints() for a in f.Pads()];ground=b.FindNet('GND');added=[]
for x,y in [(x,y) for x in range(71,145,8) for y in [62,128]]+[(x,y) for x in [62,148] for y in range(72,122,8)]+[(x,y) for x in range(116,144,8) for y in [84.7,87.6]]+[(71,116),(75,118.5),(69,120),(85,124),(89,124)]:
 pos=p.VECTOR2I(p.FromMM(x),p.FromMM(y));circle=p.SHAPE_CIRCLE(pos,p.FromMM(.3));safe=True
 if 116.025<x<119.975 and 98.775<y<101.225:continue
 for a in obs:
  if isinstance(a,p.PAD):
   bb=a.GetBoundingBox();dx=max(bb.GetLeft()-pos.x,0,pos.x-bb.GetRight());dy=max(bb.GetTop()-pos.y,0,pos.y-bb.GetBottom())
   if dx*dx+dy*dy<p.FromMM(.5)**2:safe=False;break
  elif a.GetNetname()!='GND' and a.GetEffectiveShape().Collide(circle,p.FromMM(.2)):safe=False;break
  elif isinstance(a,p.PCB_VIA) and math.hypot(p.ToMM(a.GetPosition().x-pos.x),p.ToMM(a.GetPosition().y-pos.y))<.8:safe=False;break
 if not safe:continue
 v=p.PCB_VIA(b);v.SetPosition(pos);v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(ground);b.Add(v);obs.append(v);added.append((x,y))
for text,x,y,size in [('NFCC REV C',106,76,1.1),('2S LiPo',68,88,1),('BAT +',66,67.6,0.8),('GND -',68,85.6,0.8),('PWM 0-7',138,119,1),('TELEM',69,91,0.8),('I2C',145,68,0.8),('USB MCU',144,82,0.8),('USB DEBUG',144,95,0.8)]:
 t=p.PCB_TEXT(b);t.SetText(text);t.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));t.SetTextSize(p.VECTOR2I(p.FromMM(size),p.FromMM(size)));t.SetTextThickness(p.FromMM(.12));t.SetLayer(p.F_SilkS);b.Add(t)
p.SaveBoard(str(R/'NFCC.kicad_pcb'),b);(R/'checks/stitching.json').write_text(json.dumps(added,indent=2));print('Added',len(added),'ground stitching vias and both outer ground pours')
