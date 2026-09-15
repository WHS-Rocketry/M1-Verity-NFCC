import re, json, pathlib, copy, uuid, math
class Q(str): pass
def parse(t):
 toks=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',t); stack=[]; root=None
 for tok in toks:
  if tok=='(':
   a=[]
   if stack: stack[-1].append(a)
   else: root=a
   stack.append(a)
  elif tok==')': stack.pop()
  else: stack[-1].append(Q(json.loads(tok)) if tok.startswith('"') else tok)
 return root
def dump(x, n=0):
 if not isinstance(x,list): return json.dumps(str(x),ensure_ascii=False) if isinstance(x,Q) else str(x)
 if not any(isinstance(v,list) for v in x): return '('+' '.join(dump(v) for v in x)+')'
 return '('+' '.join(dump(v) for v in x if not isinstance(v,list))+''.join('\n'+'\t'*(n+1)+dump(v,n+1) for v in x if isinstance(v,list))+ '\n'+'\t'*n+')'
def items(x,k): return [v for v in x if isinstance(v,list) and v and v[0]==k]
def get(x,k,default=None): return next(iter(items(x,k)),default)
def prop(x,k): return next((v for v in items(x,'property') if v[1]==k),None)
def uid(): return Q(str(uuid.uuid4()))
def read(p): return parse(pathlib.Path(p).read_text())
def save(x,p): pathlib.Path(p).write_text(dump(x)+'\n')
def pins(lib): return [p for s in items(lib,'symbol') for p in items(s,'pin')]
def point(sym,p):
 at=get(sym,'at'); pa=get(p,'at'); x,y=float(pa[1]),-float(pa[2]); a=math.radians(float(at[3])); m=get(sym,'mirror')
 if m:
  if m[1]=='x': y=-y
  if m[1]=='y': x=-x
 return tuple(round(v,4) for v in (float(at[1])+x*math.cos(a)+y*math.sin(a),float(at[2])-x*math.sin(a)+y*math.cos(a)))
if __name__=='__main__':
 for f in ['NFCC','NFFCPeri']:
  d=read('design/original/'+f+'.kicad_sch'); libs={x[1]:x for x in items(get(d,'lib_symbols'),'symbol')}
  print('\n'+f)
  for s in items(d,'symbol'):
   ref=prop(s,'Reference')[2]
   if ref.startswith('#'): continue
   print(ref,prop(s,'Value')[2], get(s,'at')[1:], 'footprint',prop(s,'Footprint')[2])
   if ref in ['NFCC1','U7','U4']:
    for p in pins(libs[get(s,'lib_id')[1]]):
     pt=point(s,p); lbl=[x[1] for x in items(d,'global_label') if tuple(map(float,get(x,'at')[1:3]))==pt]; nc=any(tuple(map(float,get(x,'at')[1:3]))==pt for x in items(d,'no_connect'))
     print(' ',get(p,'number')[1],get(p,'name')[1],pt,lbl,'NC' if nc else '')
