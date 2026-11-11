from pathlib import Path
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE,MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN,MSO_ANCHOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.xmlchemy import OxmlElement
import json,hashlib,shutil
r=Path(__file__).parent;prs=Presentation();prs.slide_width=Inches(13.333333);prs.slide_height=Inches(7.5)
navy='18344D';amber='B67816';gray='64748B';teal='147D79';white='FFFFFF';records=[]
def text(s,x,y,w,h,value,size=20,color=navy,bold=False):
 a=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=a.text_frame;tf.word_wrap=True;tf.margin_left=Inches(.03);tf.margin_right=Inches(.03);tf.margin_top=Inches(.02);tf.margin_bottom=Inches(.02)
 for i,line in enumerate(value.split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.alignment=PP_ALIGN.CENTER;p.font.name='Arial';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=RGBColor.from_string(color)
 records.append({'kind':'text','bounds':[x,y,w,h],'text':value});return a
def node(s,x,y,w,h,value,size=20):
 a=s.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h));a.fill.solid();a.fill.fore_color.rgb=RGBColor.from_string(navy);a.line.color.rgb=RGBColor.from_string(navy);tf=a.text_frame;tf.clear();tf.vertical_anchor=MSO_ANCHOR.MIDDLE;tf.word_wrap=True;tf.margin_left=Inches(.09);tf.margin_right=Inches(.09)
 for i,line in enumerate(value.split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.alignment=PP_ALIGN.CENTER;p.font.name='Arial';p.font.size=Pt(size);p.font.color.rgb=RGBColor.from_string(white)
 records.append({'kind':'node','bounds':[x,y,w,h],'text':value});return a
def arrow(s,x1,y1,x2,y2):
 a=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2));a.line.color.rgb=RGBColor.from_string(amber);a.line.width=Pt(2.5);a.line.dash_style=MSO_LINE_DASH_STYLE.DASH;ln=a._element.spPr.get_or_add_ln();end=OxmlElement('a:headEnd');end.set('type','none');ln.append(end);end=OxmlElement('a:tailEnd');end.set('type','triangle');ln.append(end);records.append({'kind':'conditionalArrow','from':[x1,y1],'to':[x2,y2]})
def blank():
 s=prs.slides.add_slide(prs.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=RGBColor.from_string(white);return s
s=blank();text(s,1.1,.65,11.1,.6,'Case A: one specified ticket route',28,bold=True);text(s,1.1,1.35,11.1,.45,'Synthetic placement assumption — no task or reply observed',18,color=gray)
node(s,1.2,2.35,2.9,1.45,'T-17 snippet\n“Receipts always\narrive instantly.”',19);node(s,5.25,2.55,2.15,1.05,'T-17 task',23);node(s,9.0,2.55,3.05,1.05,'Possible T-17 reply',22);arrow(s,4.12,3.08,5.22,3.08);arrow(s,7.43,3.08,8.97,3.08);text(s,4.2,2.2,.98,.5,'potential',14,color=amber);text(s,7.5,2.2,1.4,.5,'potential',14,color=amber)
node(s,4.2,4.65,2.1,.8,'Unrelated T-18',19);node(s,7.0,4.65,2.1,.8,'Later unrelated T-19',17);text(s,3.8,5.6,5.75,.5,'No route to these tickets is assumed or established.',17,color=gray)
s=blank();text(s,1.1,.65,11.1,.55,'Possible reach: bounded ticket vs shared article',27,bold=True);text(s,1.1,1.3,11.1,.45,'Synthetic diagrams — amber paths are conditional; observed paths: none supplied',17,color=gray)
text(s,1.1,1.95,3.15,.45,'Case A: ticket-specific',21,bold=True);node(s,1.35,2.65,2.6,.7,'T-17 snippet',20);node(s,1.35,3.9,2.6,.7,'T-17 task',20);node(s,1.35,5.15,2.6,.7,'Possible T-17 reply',19);arrow(s,2.65,3.38,2.65,3.87);arrow(s,2.65,4.63,2.65,5.12)
text(s,5.1,1.95,7.05,.45,'Case B: shared help article',21,bold=True);node(s,7.25,2.55,2.65,.75,'Shared source article',20)
copies=[(5.2,'Copy A\nEarlier / stale wording','Later task A\ntime t1'),(7.65,'Copy B\nRevised wording','Later task B\ntime t2'),(10.1,'Copy C\nUnknown version','Later task C\ntime t3')]
for x,label,task in copies:
 arrow(s,8.575,3.32,x+1.0,3.78);node(s,x,3.8,2.0,.95,label,17);arrow(s,x+1,4.78,x+1,5.18);node(s,x,5.2,2.0,.85,task,17)
# All teaching shapes and arrow endpoints remain inside the exact inner 84%.
for z in records:
 if 'bounds'in z:
  x,y,w,h=z['bounds'];assert x>=13.333333*.08-.01 and y>=7.5*.08-.01 and x+w<=13.333333*.92+.01 and y+h<=7.5*.92+.01,z
 else:
  for x,y in [z['from'],z['to']]:assert 1.06<=x<=12.28 and .6<=y<=6.9,z
path=r/'HarborDesk-Conditional-Reach-v2.pptx';prs.save(path);check=Presentation(path);assert len(check.slides)==2
for slide in check.slides:
 for shape in slide.shapes:
  if shape.shape_type==9:  # actual native connector
   assert shape._element.spPr.ln.find('{http://schemas.openxmlformats.org/drawingml/2006/main}headEnd').get('type')=='none'
   assert shape._element.spPr.ln.find('{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd').get('type')=='triangle'
alltext='\n'.join(shape.text for slide in check.slides for shape in slide.shapes if shape.has_text_frame);assert 'T-17 snippet'in alltext and 'Earlier / stale wording'in alltext and 'Revised wording'in alltext
assert 'Wider possible reach is not proof' not in alltext and 'One specified ticket route; possible reply influence' not in alltext
(r/'authoring-proof.json').write_text(json.dumps({'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'slides':2,'pythonPptxVersion':'1.0.2','editableNativeShapes':True,'observedHarborDeskPaths':0,'allArrowsConditional':True,'allTeachingContentInsideInner84Percent':True,'records':records},indent=2));print(json.dumps({'file':str(path),'slides':2,'shapeRecords':len(records),'awaitingGenuinePowerPointCapture':True}))
