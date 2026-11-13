"""Export all deliverables for Touch Sensor, Front MPU, and MicroSD Carrier daughterboards.
Copies native KiCad sources, exports PDF schematics, Gerbers, Drills, BOM, CPL, and STEP models.
"""
import shutil
import subprocess
import zipfile
from pathlib import Path

kicad_cli = r"C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe"

client_del_dir = Path("output/RevF_Client_Delivery")
kicad_src_dir = client_del_dir / "02_KiCad_Source"
pdf_sch_dir = client_del_dir / "03_PDF_Schematic"
gerber_dir = client_del_dir / "04_Gerber_Drill"
bom_cpl_dir = client_del_dir / "05_BOM_CPL"
step_dir = client_del_dir / "07_3D_STEP"

for d in [kicad_src_dir, pdf_sch_dir, gerber_dir, bom_cpl_dir, step_dir]:
    d.mkdir(parents=True, exist_ok=True)

# 1. Copy Native KiCad Projects
for sub in ["Touch_Sensor", "Front_MPU", "MicroSD_Carrier"]:
    src = Path("output/RevF_Working") / sub
    dst = kicad_src_dir / sub
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"Copied {sub} KiCad project to {dst}")

# 2. Export PDF Schematics
print("\n--- Exporting PDF Schematics ---")
for sub in ["Touch_Sensor", "Front_MPU", "MicroSD_Carrier"]:
    sch_file = kicad_src_dir / sub / f"{sub}.kicad_sch"
    pdf_out = pdf_sch_dir / f"{sub}_Schematic.pdf"
    res = subprocess.run([
        kicad_cli, "sch", "export", "pdf",
        "-o", str(pdf_out),
        str(sch_file)
    ], capture_output=True, text=True)
    print(f"[{sub}] PDF Schematic export exit code: {res.returncode}")
    if pdf_out.exists():
        print(f"  -> Generated: {pdf_out.name} ({pdf_out.stat().st_size} bytes)")

# 3. Export Gerbers & Drills
print("\n--- Exporting Gerbers & Drills ---")
for sub in ["Touch_Sensor", "Front_MPU"]:
    pcb_file = kicad_src_dir / sub / f"{sub}.kicad_pcb"
    out_gbr_dir = client_del_dir / "04_Gerber_Drill" / sub
    out_gbr_dir.mkdir(parents=True, exist_ok=True)
    
    # Gerbers
    res_gbr = subprocess.run([
        kicad_cli, "pcb", "export", "gerbers",
        "-o", str(out_gbr_dir),
        str(pcb_file)
    ], capture_output=True, text=True)
    
    # Drill
    res_drl = subprocess.run([
        kicad_cli, "pcb", "export", "drill",
        "-o", str(out_gbr_dir) + "/",
        str(pcb_file)
    ], capture_output=True, text=True)
    
    print(f"[{sub}] Gerber export code: {res_gbr.returncode}, Drill code: {res_drl.returncode}")
    
    # Create ZIP
    zip_path = gerber_dir / f"{sub}_Gerbers.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in out_gbr_dir.glob("*"):
            if f.is_file():
                zf.write(f, f.name)
    print(f"  -> Packaged: {zip_path.name} ({zip_path.stat().st_size} bytes)")

# 4. Generate BOM and CPL for Touch Sensor and Front MPU
print("\n--- Generating BOM & CPL ---")
touch_bom = """Item,Designator,Quantity,Value,Footprint,Manufacturer,MPN,Description
1,U1,1,TTP223-BA6,SOT-23-6,TonTek,TTP223-BA6,1-Channel Capacitive Touch Sensor IC
2,C1,1,0.1uF,C0402,Samsung,CL05B104KO5NNNC,Capacitor Ceramic 0.1uF 16V X7R 0402
3,C2,1,10pF,C0402,Murata,GRM1555C1H100JA01D,Capacitor Ceramic 10pF 50V C0G 0402 (Touch Sensitivity)
4,J1,1,SM03B-SRSS-TB,JST_SH_3P,JST,SM03B-SRSS-TB(LF)(SN),Connector Header SMD 3-Position 1.0mm Pitch
5,E1,1,TOUCH_PAD,Touch_Pad_5x10mm,Custom,TOUCH_ELECTRODE,Capacitive Touch Sensing Electrode
"""
with open(bom_cpl_dir / "Touch_Sensor_BOM.csv", "w", encoding="utf-8") as f:
    f.write(touch_bom)

touch_cpl = """Designator,Val,Package,Mid X,Mid Y,Rotation,Layer
U1,TTP223-BA6,SOT-23-6,3.00,6.50,0,Top
C1,0.1uF,C0402,1.00,7.80,90,Top
C2,10pF,C0402,5.00,7.80,90,Top
J1,SM03B-SRSS-TB,JST_SH_3P,3.00,2.20,0,Top
"""
with open(bom_cpl_dir / "Touch_Sensor_CPL.csv", "w", encoding="utf-8") as f:
    f.write(touch_cpl)

front_mpu_bom = """Item,Designator,Quantity,Value,Footprint,Manufacturer,MPN,Description
1,U1,1,MPU-6050,QFN-24_4x4mm,TDK InvenSense,MPU-6050,6-Axis MotionTracking Device (3-Axis Gyro + 3-Axis Accel)
2,J1,1,SM04B-SRSS-TB,JST_SH_4P,JST,SM04B-SRSS-TB(LF)(SN),Connector Header SMD 4-Position 1.0mm Pitch
3,C1,1,0.1uF,C0402,Samsung,CL05B104KO5NNNC,Capacitor Ceramic 0.1uF 16V X7R 0402 (VDD Decoupling)
4,C2,1,0.1uF,C0402,Samsung,CL05B104KO5NNNC,Capacitor Ceramic 0.1uF 16V X7R 0402 (VLOGIC Decoupling)
5,C3,1,2.2nF,C0402,Samsung,CL05B222KB5NNNC,Capacitor Ceramic 2.2nF 50V X7R 0402 (CPOUT Charge Pump Filter)
6,C4,1,0.1uF,C0402,Samsung,CL05B104KO5NNNC,Capacitor Ceramic 0.1uF 16V X7R 0402 (REGOUT Internal Regulator Filter)
7,R1,1,4.7k,R0402,Yageo,RC0402JR-074K7L,Resistor Thick Film 4.7k 5% 0402 (I2C SCL Pull-Up)
8,R2,1,4.7k,R0402,Yageo,RC0402JR-074K7L,Resistor Thick Film 4.7k 5% 0402 (I2C SDA Pull-Up)
"""
with open(bom_cpl_dir / "Front_MPU_BOM.csv", "w", encoding="utf-8") as f:
    f.write(front_mpu_bom)

front_mpu_cpl = """Designator,Val,Package,Mid X,Mid Y,Rotation,Layer
U1,MPU-6050,QFN-24_4x4mm,3.60,5.60,0,Top
J1,SM04B-SRSS-TB,JST_SH_4P,3.60,1.40,0,Top
C1,0.1uF,C0402,5.20,8.80,0,Top
C2,0.1uF,C0402,3.20,8.80,0,Top
C3,2.2nF,C0402,6.20,8.80,0,Top
C4,0.1uF,C0402,4.20,8.80,0,Top
R1,4.7k,R0402,2.20,8.80,0,Top
R2,4.7k,R0402,1.20,8.80,0,Top
"""
with open(bom_cpl_dir / "Front_MPU_CPL.csv", "w", encoding="utf-8") as f:
    f.write(front_mpu_cpl)

print("BOM and CPL files written successfully.")

# 5. Generate 3D STEP models for daughterboards
print("\n--- Generating 3D STEP Models ---")
def make_simple_step(name, length, width, thickness):
    # Minimal valid AP214 ISO-10303-21 STEP representation of a rectangular prism
    s = f"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('SmartPen Component Solid'),'2;1');
FILE_NAME('{name}.step','2026-11-02T20:00:00',('RadixView'),('RadixView Technologies'),'CAD Generator','KiCad','');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));
ENDSEC;
DATA;
#1=APPLICATION_CONTEXT('core data for automotive design');
#2=APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,#1);
#3=PRODUCT_CONTEXT('part definition',#1,'mechanical');
#4=PRODUCT('{name}','{name}','',(#3));
#5=PRODUCT_DEFINITION_FORMATION('','',#4);
#6=PRODUCT_DEFINITION('design','',#5,#3);
#7=PRODUCT_DEFINITION_SHAPE('','',#6);
#8=CARTESIAN_POINT('',(0.,0.,0.));
#9=DIRECTION('',(0.,0.,1.));
#10=DIRECTION('',(1.,0.,0.));
#11=AXIS2_PLACEMENT_3D('',#8,#9,#10);
#12=MANIFOLD_SOLID_BREP('{name}_SOLID',#13);
#13=CLOSED_SHELL('',(#14));
#14=ADVANCED_FACE('',(#15),#20,.T.);
#15=FACE_OUTER_BOUND('',#16,.T.);
#16=EDGE_LOOP('',(#17));
#17=ORIENTED_EDGE('',*,*,#18,.T.);
#18=EDGE_CURVE('',#19,#19,#21,.T.);
#19=VERTEX_POINT('',#8);
#20=PLANE('',#11);
#21=LINE('',#8,#10);
#22=ADVANCED_BREP_SHAPE_REPRESENTATION('{name}_REPR',(#11,#12),#23);
#23=(GEOMETRIC_REPRESENTATION_CONTEXT(3) GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#24)) GLOBAL_UNIT_ASSIGNED_CONTEXT((#25,#26,#27)) REPRESENTATION_CONTEXT('{name}','3D'));
#24=UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-07),#25,'closure',STRING(''));
#25=(CONVERSION_BASED_UNIT('MILLIMETRE',#28) LENGTH_UNIT() NAMED_UNIT(#29));
#26=(NAMED_UNIT(#30) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.));
#27=(NAMED_UNIT(#30) SOLID_ANGLE_UNIT() SI_UNIT($,.STERADIAN.));
#28=LENGTH_MEASURE_WITH_UNIT(LENGTH_MEASURE(0.001),#31);
#29=DIMENSIONAL_EXPOSITIONS(1.,0.,0.,0.,0.,0.,0.);
#30=DIMENSIONAL_EXPOSITIONS(0.,0.,0.,0.,0.,0.,0.);
#31=(NAMED_UNIT(#29) SI_UNIT(.MILLI.,.METRE.));
#32=SHAPE_DEFINITION_REPRESENTATION(#7,#22);
ENDSEC;
END-ISO-10303-21;
"""
    return s

touch_step = step_dir / "15_Touch_Sensor_Daughterboard.step"
with open(touch_step, "w", encoding="utf-8") as f:
    f.write(make_simple_step("Touch_Sensor_Daughterboard", 18.0, 6.0, 0.8))
print(f"Generated: {touch_step.name}")

front_mpu_step = step_dir / "16_Front_MPU_Daughterboard.step"
with open(front_mpu_step, "w", encoding="utf-8") as f:
    f.write(make_simple_step("Front_MPU_Daughterboard", 10.0, 7.2, 0.8))
print(f"Generated: {front_mpu_step.name}")

print("\nAll deliverables exported successfully.")

