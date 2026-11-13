"""Smart Pen Rev A envelope STUDY, editable in Python/CadQuery.
NON-MANUFACTURING CAD: exact PCB, cell, click mechanism, lugs, fasteners are not selected.
World axes: z=pen axis, z=0 tip, z=153 rear. x,y=cross-section.
Battery below rail means lower (negative-y), not a validated clearance solution.
"""
from pathlib import Path
import cadquery as cq
O=Path(__file__).resolve().parent
OUT_STL=O/'3D_STL'; OUT_STEP=O/'3D_STEP'
OUT_STL.mkdir(exist_ok=True); OUT_STEP.mkdir(exist_ok=True)
# Must never exceed max OD 16 mm; these are provisional CAD envelope values.
LENGTH=153.0
OD=16.0
SHELL_WALL=1.2
R_OUT=OD/2
R_IN=R_OUT-SHELL_WALL

def annulus(rout,rin,h,z):
    return cq.Workplane('XY').circle(rout).circle(rin).extrude(h).translate((0,0,z))

def savepart(label, solid):
    cq.exporters.export(solid,str(OUT_STL/f'{label}.stl'),tolerance=0.10,angularTolerance=0.17)
    cq.exporters.export(solid,str(OUT_STEP/f'{label}.step'))
    return solid

# Body region z=62..143, simple wall with provisional ports / buttons.
body=annulus(R_OUT,R_IN,81,62)
# side access holes are rough clearances, not USB or button manufacturer's dimensions.
for zz,h,w in [(114,9,6.4),(94,5.2,4.2),(105,5.2,4.2)]:
    cut=cq.Workplane('XY').box(5,w,h).translate((7.25,0,zz))
    body=body.cut(cut)
body=savepart('01_Outer_Barrel_Concept',body)

# Grip from 20 to 62 (continuous axial refill path, natural fingers require testing).
grip=annulus(7.75,6.4,42,20)
grip=savepart('02_Front_Grip_Concept',grip)

# Tip from z=0..20, tapered shell with axial refill passage.
tip=cq.Workplane('XY').circle(1.8).workplane(offset=20).circle(7.75).loft(combine=True)
tip=tip.cut(cq.Workplane('XY').circle(1.05).extrude(21))
tip=savepart('03_Tapered_Tip_Concept',tip)

# Structural rail deck + battery support ribs, oriented so battery is BELOW the deck.
# z range 39..133; battery envelope 42 mm long underneath.
rail=cq.Workplane('XY').box(8.0,1.2,94).translate((0,1.45,86))
for x in [-4.35,4.35]:
    rail=rail.union(cq.Workplane('XY').box(1.0,4.5,70).translate((x,-2.2,86)))
for zz in [53,116]:
    rail=rail.union(cq.Workplane('XY').box(9.5,1.0,2.0).translate((0,-4.7,zz)))
# stabilizing tabs near ends
for zz in [41,130]:
    rail=rail.union(cq.Workplane('XY').box(9,2.0,3.0).translate((0,0.8,zz)))
rail=savepart('04_Internal_Rail_Battery_Below_Concept',rail)

# Separate MPU pocket near the tip; positive y, center hole retained for pen refill.
mpu=cq.Workplane('XY').box(7.8,5.4,10).translate((0,3.75,30.0))
mpu=mpu.cut(cq.Workplane('XY').circle(1.2).extrude(12).translate((0,0,24)))
mpu=mpu.cut(cq.Workplane('XY').box(6.0,3.3,6.5).translate((0,4.15,32.5)))
mpu=savepart('05_Detachable_Front_IMU_Pocket_Concept',mpu)

# Bayonet collar ring as a geometry PLACEHOLDER (NO tested lock lugs/slots).
collar=annulus(7.95,6.55,11,51.0)
# Indicate 3 provisional indexing marks as notches, not functioning locking system
for angle in [0,120,240]:
    cutter=cq.Workplane('XY').box(2.0,2.0,3.5).translate((7.8,0,54.0)).rotate((0,0,0),(0,0,1),angle)
    collar=collar.cut(cutter)
collar=savepart('06_Bayonet_Collar_PLACEHOLDER',collar)

# Rear click cap is only a dimensional stand-in, not a working click mechanism.
rear=cq.Workplane('XY').circle(6.7).extrude(10).translate((0,0,143))
rear=rear.cut(cq.Workplane('XY').circle(1.5).extrude(12).translate((0,0,142)))
rear=savepart('07_Rear_Click_Cap_PLACEHOLDER',rear)

# PCB and battery are REFERENCE ENVELOPES, not approved part dimensions.
pcb=cq.Workplane('XY').box(7.4,0.8,77).translate((0,2.55,85))
cell=cq.Workplane('XY').box(7.0,3.8,42).translate((0,-2.65,88))
# Barrel extends to z=143, cap to 153; both represent nominal 153 mm total length.
assembly=cq.Assembly(name='SmartPen_Envelope_Study_RevA')
for name,obj,color in [
 ('barrel',body,cq.Color(0.14,0.28,0.25)),('grip',grip,cq.Color(0.32,0.49,0.41)),
 ('tip',tip,cq.Color(0.24,0.32,0.30)),('rail',rail,cq.Color(0.82,0.67,0.35)),
 ('front_IMU_pocket',mpu,cq.Color(0.70,0.54,0.26)),('bayonet_placeholder',collar,cq.Color(0.34,0.39,0.48)),
 ('rear_click_placeholder',rear,cq.Color(0.33,0.42,0.39)),
 ('PCB_dummy_77x7p4',pcb,cq.Color(0.08,0.5,0.29)),('Battery_dummy_42x7x3p8',cell,cq.Color(0.25,0.35,0.68))]:
    assembly.add(obj,name=name,color=color)
assembly.save(str(O/'SmartPen_Assembly_Concept.step'))
print('Saved geometry, 153mm x 16mm maximum envelope; unverified mechanics')
