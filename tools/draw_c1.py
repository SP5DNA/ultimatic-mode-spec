"""Recreate the native C.1 timing plot; no input bitmap is edited."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import argparse
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'docs/annex-c1-timing-diagram.png');a=p.parse_args()
S=2
im=Image.new('RGB',(1043*S,2048*S),'#132c41');d=ImageDraw.Draw(im)
fonts={'regular':'/System/Library/Fonts/Supplemental/Arial.ttf','bold':'/System/Library/Fonts/Supplemental/Arial Bold.ttf','mono':'/System/Library/Fonts/Menlo.ttc'}
def txt(x,y,t,n=16,c='#abcce4',k='regular',anchor=None):d.text((x*S,y*S),t,font=ImageFont.truetype(fonts[k],n*S),fill=c,anchor=anchor)
def line(x,y,x2,y2,c='#2a4b65',w=1):d.line((round(x*S),round(y*S),round(x2*S),round(y2*S)),fill=c,width=w*S)
def box(x,y,x2,y2,c,edge=None,r=0):d.rounded_rectangle((round(x*S),round(y*S),round(x2*S),round(y2*S)),r*S,fill=c,outline=edge,width=S)
def dot(x,y,closed,c):d.ellipse(((x-3)*S,(y-3)*S,(x+3)*S,(y+3)*S),fill=c if closed else '#153148',outline=c,width=2*S)
for x in range(20,1043,96):line(x,0,x,2048,'#1b374d')
for y in range(18,2048,96):line(0,y,1043,y,'#1b374d')
txt(35,72,'ULTIMATIC KEYER · NORMATIVE SPEC §12',14,'#28a99f','mono')
txt(35,94,'TIMING DIAGRAM',50,'#edf4ff','bold')
txt(35,153,'Annex C.1 — letter N (− ·). Five conformant paddle timelines,',21)
txt(35,180,'tests T3 / T7, one identical output.',21)
box(706,35,1008,197,'#10283d','#2a4b65')
for i,(left,right) in enumerate([('SHEET','C.1 / N'),('SCALE','1 unit = 80 ms (15 WPM)'),('REF','§8, §9, T3, T7'),('SOURCE','QST May 1955, pt. 3'),('BY','SP5DNA')]):
 y=35+i*32;line(706,y,1008,y);line(797,y,797,y+32)
 txt(717,y+7,left,13,'#739bb9','mono');txt(807,y+7,right,13,'#edf4ff','mono')
line(35,222,1008,222)
box(35,249,1008,341,'#153148','#2a4b65')
for x,c,label,filled in [(56,'#ca811b','DAH paddle closed',False),(264,'#28a99f','DIT paddle closed',False),(464,'#ca811b','DAH sent (output)',True),(666,'#28a99f','DIT sent (output)',True)]:
 box(x,270,x+22,280,c if filled else '#153148',c,1);txt(x+32,266,label,16)
dot(60,315,True,'#abcce4');txt(76,305,'rising edge (press)',16)
dot(254,315,False,'#abcce4');txt(270,305,'release',16)
for x in range(358,384,8):line(x,315,x+5,315,'#abcce4',2)
txt(391,305,'IDLE decision, 320 ms',16)
box(35,368,1008,446,'#1b3b54');box(35,368,38,446,'#dda13e')
txt(55,380,'Why five panels:',16,'#edf4ff','bold')
txt(196,380,'each DIT press arrives before the decision at 320 ms.',16)
txt(55,400,'Scenario 2 is during DAH; scenario 3 is during SPACING (T7).',16)
txt(55,420,'The output is the same in all five panels.',16)
scenarios=[(160,10,80,'Plain squeeze during DAH'),(160,200,210,'Brief DIT during DAH'),(340,250,260,'DIT during SPACE (T7); DAH held into the space'),(420,300,410,'DAH held through the whole character'),(430,300,470,'DAH held through character + partial trailing space')]
for i,(end,ds,de,title) in enumerate(scenarios):
 top=478+i*261;box(35,top,1008,top+252,'#153148','#2a4b65')
 txt(55,top+17,str(i+1),27,'#dda13e','bold');txt(93,top+25,title,17,'#edf4ff')
 txt(987,top+30,f'DAH 0–{end} ms · DIT {ds}–{de} ms',13,'#739bb9','mono',anchor='ra')
 X=lambda t:167+t*1.79
 for t in range(0,401,80):
  line(X(t),top+64,X(t),top+223,'#304d62');txt(X(t),top+224,str(t),11,'#739bb9','mono',anchor='ma')
 for y in range(top+64,top+220,8):line(X(320),y,X(320),y+5,'#abcce4',2)
 txt(X(320)+8,top+65,'IDLE decision · 320 ms',11,'#abcce4','mono')
 txt(55,top+71,'DAH',14,'#ca811b','mono');txt(55,top+126,'DIT',14,'#28a99f','mono');txt(55,top+179,'OUT',14,'#abcce4','mono')
 box(X(0),top+75,X(end),top+97,'#303f45','#ca811b',5);dot(X(0),top+86,True,'#ca811b');dot(X(end),top+86,False,'#ca811b')
 txt(X(0),top+59,'0ms',11,'#abcce4','mono')
 box(X(ds),top+120,X(de),top+142,'#194353','#28a99f',5);dot(X(ds),top+131,True,'#28a99f');dot(X(de),top+131,False,'#28a99f');txt(X(ds),top+104,f'{ds}ms',11,'#abcce4','mono')
 box(X(0),top+165,X(240),top+192,'#ca811b',r=4);box(X(320),top+165,X(400),top+192,'#28a99f',r=4);txt(X(280),top+172,'SP',11,'#739bb9','mono',anchor='ma')
box(35,1803,1008,1973,'#153148','#2a4b65');box(35,1803,1008,1806,'#28a99f')
txt(57,1828,'TAKEAWAY — §12 T3 / T7',13,'#28a99f','mono')
for y,t in [(1855,'The DAH press at 0 ms starts the first element. A DIT press before 320 ms'),(1880,'is remembered during either the DAH mark or its following space.'),(1905,'DIT starts at 320 ms in every case. Both paddles are released before the'),(1930,'next decision at 480 ms, so the output ends after N.')]:txt(57,y,t,17)
txt(35,1994,'Ultimatic Mode Specification · Annex C, worked example C.1',12,'#739bb9','mono')
txt(1008,1994,'2026-10-19',12,'#739bb9','mono',anchor='ra')
a.output.parent.mkdir(parents=True,exist_ok=True)
im.resize((1744,3424),Image.Resampling.LANCZOS).save(a.output)
