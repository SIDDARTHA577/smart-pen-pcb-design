# Smart Pen Revision F — Complete Mechanical & Electrical Assembly & Disassembly Instructions

**Project**: Smart Pen PCB and 3D Enclosure — RadixView Technologies  
**Date**: November 2, 2026  
**Revision Baseline**: Rev F Engineering Release  
**Authoritative Reference**: `Smart_Pen_PCB_Handoff(1).docx` (Revision 0.2, September 2026)  

---

## 1. Safety, ESD Precautions & Tools Required

### 1.1 Safety & Handling
- **LiPo Pouch Battery Caution**: The selected `LP401040` 300 mAh pouch cell contains high energy density. Do NOT bend, pierce, pinch, or apply direct soldering heat to the cell body. Verify integrated PCM circuit is intact before installation.
- **ESD Protection**: Use an ESD-safe workbench mat and grounded wrist strap when handling the Main PCB (`84.0 x 9.2 mm`), MicroSD Carrier Board (`11.4 x 16.0 mm`), and front MPU-6050 carrier.
- **Optics & Precision**: Clean optical lens / pen nose aperture with lint-free swabs and isopropyl alcohol (IPA 99%).

### 1.2 Tools & Materials Required
- #00 Phillips precision screwdriver
- ESD-safe angled tweezers
- Double-sided thermally conductive Kapton adhesive strip (0.1 mm thickness)
- Silicone grease / Krytox GPL 205 (micro-lubricant for bayonet collar and ratchet cam)
- Multi-meter with fine-pitch test probes

---

## 2. Component Inventory Checklist

Before starting assembly, confirm presence of all 16 digital sub-assemblies:
1. `01_Outer_Barrel.stl / .step` (Main enclosure tube, OD 15.5 mm)
2. `02_Front_Grip.stl / .step` (Contoured grip with MPU pocket and touch pad recess)
3. `03_Front_Cap_Tip.stl / .step` (Tapered nose cap with spring seat)
4. `04_Internal_Rail_Cartridge.stl / .step` (Central sliding chassis with push-rod tunnel)
5. `05_Battery_Cradle.stl / .step` (Snap-on / monolithic lower battery cradle)
6. `06_Front_IMU_Carrier.stl / .step` (Detachable MPU-6050 sensor carrier)
7. `07_Dual_Button_Actuator.stl / .step` (Rocker plunger for ERASE and MODE)
8. `08_Rear_Click_Mechanism_Cap.stl / .step` (Push button dome and sleeve)
9. `09_Pocket_Clip.stl / .step` (Spring clip)
10. `10_Vibration_Motor_Mount.stl / .step` (Haptic coin/ERM motor sleeve)
11. `11_LiPo_Battery_LP401040` (300 mAh cell with JST-SH 2-pin connector)
12. `12_D1_Ink_Refill_and_Spring` (Standard D1 refill 67 mm, helical return spring)
13. `13_Click_Ratchet_and_Pushrod` (Rotating ratchet cam + DIA 1.6 mm Delrin push-rod)
14. `14_Bayonet_Locking_Collar` (3 radial lugs with 30° rotational detents)
15. `SmartPen_RevF_PCB` (Main PCB populated with ESP32-C3, AP2112K, MCP73831, MCP23008)
16. `MicroSD_Carrier` (Off-board MicroSD carrier with 6-pin FPC ribbon)

---

## 3. Step-by-Step Assembly Procedure

### Stage A: Internal Electronics Rail Sub-Assembly
1. **Battery Installation**:
   - Clean the lower cradle pocket ($Y = -1.20$ to $-5.80\text{ mm}$) of the rail cartridge.
   - Apply a strip of double-sided Kapton tape to the battery bay floor.
   - Gently press the `LP401040` LiPo cell into the cradle pocket with lead wires facing rearward.
   - Route the 2-pin JST-SH wire pigtail upward through the lateral cable routing channel ($X = +5.5\text{ mm}$).
2. **Main PCB Mounting**:
   - Slide the $84.0 \times 9.2\text{ mm}$ Main PCB onto the upper stepped deck ($Y = +1.20\text{ mm}$) of the rail cartridge until the front edge seats firmly against the forward retention tabs.
   - Verify that the bottom copper layer of the PCB rests directly against the $2.40\text{ mm}$ solid composite barrier deck, isolated from the battery pouch below.
   - Connect the battery harness to `J_BAT` on the PCB.
3. **Haptic Motor Installation**:
   - Press the vibration motor into `10_Vibration_Motor_Mount.stl` with elastomeric damping shim.
   - Plug lead harness into `J_MOT` on the PCB.
4. **MicroSD Carrier Connection**:
   - Seat the $11.4 \times 16.0\text{ mm}$ MicroSD carrier board into the rear rail nest above the PCB.
   - Insert the 6-pin $0.5\text{ mm}$-pitch FPC flex cable between carrier connector `J1` and Main PCB header `J_SD`. Flip the ZIF actuator bars down to lock.

### Stage B: Kinematic Refill & Click Push-Rod Installation
1. **Push-Rod Insertion**:
   - Apply a microscopic film of silicone lubricant along the $\varnothing 1.60\text{ mm} \times 71.5\text{ mm}$ Delrin push-rod.
   - Insert the push-rod into the rear entry of the $\varnothing 3.20\text{ mm}$ central tunnel in the rail cartridge ($X=0, Y=0$) until its forward cup emerges at $Z = 68.50\text{ mm}$.
   - Verify frictionless axial slide along the full $4.50\text{ mm}$ stroke.
2. **Rear Click Mechanism Installation**:
   - Install the 12-tooth rotating cam ratchet into the rear guide sleeve of the rail cartridge.
   - Seat the push button actuator cap (`08_Rear_Click_Mechanism_Cap.stl`) over the ratchet plunger.
3. **Refill & Return Spring**:
   - Slide the standard D1 ballpoint refill ($\varnothing 2.35 \times 67.0\text{ mm}$) through the front bore of the rail until its brass tail cup seats firmly into the front pocket of the Delrin push-rod at $Z = 68.50\text{ mm}$.
   - Slide the helical conical return spring over the forward neck of the refill.

### Stage C: Front MPU-6050 & Touch Sensor Integration
1. **Front IMU Carrier**:
   - Place the MPU-6050 sensor module into the carrier pocket (`06_Front_IMU_Carrier.stl`).
   - Connect the 4-pin FPC cable between the MPU module and Main PCB header `J_IMU`.
   - Engage the strain relief clamp rib over the FPC cable.
2. **Capacitive Touch Electrode**:
   - Position the copper touch sensor foil into the grip pocket ($Z = 20.0$ to $35.0\text{ mm}$).
   - Plug the 3-pin touch lead into `J_TOUCH` on the Main PCB.
3. **Front Grip Sleeve**:
   - Slide the front grip sleeve (`02_Front_Grip.stl`) over the front nose sub-assembly.
   - Screw the front nose cap (`03_Front_Cap_Tip.stl`) onto the front threads, capturing the return spring in its counterbore.

### Stage D: Final Enclosure Insertion & Bayonet Twist-Lock Closure
1. **Rail Insertion**:
   - Align the longitudinal guide ribs on the internal rail cartridge with the internal guide keyways inside the main outer barrel (`01_Outer_Barrel.stl`).
   - Slide the fully populated rail cartridge smoothly into the barrel until the USB-C receptacle centers in the rear barrel bezel.
2. **Rocker Button Installation**:
   - Insert the dual rocker button actuator (`07_Dual_Button_Actuator.stl`) into the barrel slot, ensuring the plunger feet contact tactile switches `SW4` (ERASE) and `SW5` (MODE).
3. **Bayonet Twist-Lock**:
   - Align the 3 radial lugs on the front collar with the 3 entry slots on the barrel collar.
   - Press axially to engage the internal detent spring and **rotate $30.0^\circ$ clockwise** until the lugs click into the positive locking detents.
   - Press the pocket clip (`09_Pocket_Clip.stl`) into the rear barrel dovetail slot until flush.

---

## 4. Post-Assembly Verification & Bring-Up Test

1. **Mechanical Mechanism Verification**:
   - Depress the rear click button: Refill must smoothly extend $4.50\text{ mm}$, with the writing nib protruding $3.0\text{ mm}$ past the nose cap aperture.
   - Click again: Return spring must immediately and fully retract the refill nib inside the nose cap.
   - Shake the pen: Confirm zero internal component rattle or lateral battery play.
2. **Electrical Power Bring-Up**:
   - Slide power switch `SW3` to the ON position.
   - Verify green LED `D1` blinks once upon ESP32-C3 firmware boot.
3. **USB-C Interface Bring-Up**:
   - Connect a standard USB-C cable from a PC to the pen.
   - Verify red charge LED `D2` illuminates (MCP73831 active charging at $303\text{ mA}$).
   - Verify Device Manager detects `USB Serial/JTAG Device (COMx)`.
   - Open serial terminal at 115200 baud to observe live IMU raw packet streaming.
4. **Button & Touch Check**:
   - Press ERASE (`SW4`): Confirm tactile click and haptic pulse feedback.
   - Press MODE (`SW5`): Confirm mode toggle serial message.
   - Grasp front grip: Confirm touch interrupt fires on `GPIO3`.

---

## 5. Step-by-Step Disassembly Procedure (Service & Refill Replacement)

To service the electronics or replace the D1 ink refill:
1. **Power Off**: Slide `SW3` power switch to the OFF position.
2. **Bayonet Unlock**:
   - Grasp the outer barrel firmly in one hand and the front grip in the other hand.
   - **Rotate the front grip $30.0^\circ$ counter-clockwise**.
   - The bayonet locking lugs will disengage from the barrel J-slots.
3. **Rail Extraction**:
   - Gently pull the front grip and internal rail cartridge straight out of the outer barrel as a single unified sub-assembly.
   - Note: The rocker button actuator (`07`) will remain captured in the outer barrel slot.
4. **Refill Replacement**:
   - Pull the exhausted D1 refill tube forward out of the central push-rod socket.
   - Remove the return spring from the old refill and transfer to the new D1 refill.
   - Slide new refill into the central tunnel until seated in the push-rod cup.
5. **Re-insertion**:
   - Re-align rail guide ribs with barrel keyways, push straight in, and **rotate $30.0^\circ$ clockwise** to re-lock.

