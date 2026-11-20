import sys
T,D=sys.argv[1],sys.argv[2]
h=open(D+'/index.html',encoding='utf-8').read()
import json
pd=json.dumps(json.load(open(T+'/progdemo/roster.json',encoding='utf-8'))['campers'])
head='<script>window.__errs=[];addEventListener("error",function(e){__errs.push(e.message)});</script>'
exp=open(T+'/expected.js',encoding='utf-8').read().replace('</','<\\/')
t=h.replace('<head>','<head>'+head,1).replace('</body>','<script>window.__programDemo='+pd.replace('</','<\\/')+';'+exp+'</script><script>'+open(T+'/test.js',encoding='utf-8').read()+'</script></body>')
open(T+'/shots/test.html','w',encoding='utf-8').write(t)
S={'home':'','import':"document.getElementById('tImport').click();",'aq':"document.getElementById('filterTab3').click();",'prog':"document.getElementById('filterTab1').click();"}
for k,v in S.items():
    s='<script>addEventListener("load",function(){'+v+'var o=document.documentElement;var p=document.createElement("meta");p.name="ov";p.content=o.scrollWidth+"/"+innerWidth;document.head.appendChild(p);});</script>'
    open(T+'/shots/%s.html'%k,'w',encoding='utf-8').write(h.replace('</body>',s+'</body>'))
