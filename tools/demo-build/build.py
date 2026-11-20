import base64,sys
T,D=sys.argv[1],sys.argv[2]
R=T+'/sample/'
h=open(T+'/template.html',encoding='utf-8').read()
i='data:image/png;base64,'+base64.b64encode(open(T+'/icon-128.png','rb').read()).decode()
h=h.replace('__ICON__',i).replace('__CAMPERS__',open(R+'campers.csv',encoding='utf-8-sig').read().strip()).replace('__ACTIVITIES__',open(R+'activities.csv',encoding='utf-8-sig').read().strip())
import json
p=[x for x in json.load(open(T+'/oracle/activity-s1v1-missingcabin.json')) if x['group'] is not None]
h=h.replace('__PROGRAMS__',json.dumps(p,separators=(',',':')))
pick=lambda f:[y for y in json.load(open(T+'/oracle/'+f)) if y['name']=='Traditional Camp'][0]
h=h.replace('__PROGRAM_CASES__',json.dumps({'early':pick('activity-s1v1-missingcabin.json'),'later':pick('activity-s1v4-tuesdayswitches.json')},separators=(',',':')))
r=json.load(open(T+'/progdemo/roster.json',encoding='utf-8'))
g={y['name']:y['group'] for y in json.load(open(T+'/progdemo/groups.json',encoding='utf-8'))}
assert g=={'Counselor-In-Training':-1,'Traditional Camp':3,'Staff Kids':0}
K=['Preferred Name','Last Name','Program','Round 1','Round 2','Round 3','Rounds Assigned']
h=h.replace('__PROGRAM_CAMPERS__',json.dumps([{k:c[k] for k in K} for c in r['campers']],separators=(',',':')))
DC=json.load(open(T+'/demanddemo/roster.json',encoding='utf-8'))['campers']
h=h.replace('__DEMAND_CAMPERS__',json.dumps([{k:c[k] for k in ['Preferred Name','Last Name','Activity Preferences','Round 1','Round 2','Round 3']} for c in DC],separators=(',',':')))
open(D+'/index.html','w',encoding='utf-8').write(h)
