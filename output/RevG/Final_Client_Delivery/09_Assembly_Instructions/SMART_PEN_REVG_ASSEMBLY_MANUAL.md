# SMART PEN REV G — ELECTRO-MECHANICAL ASSEMBLY & SERVICE MANUAL

**Document ID:** SRG-DOC-ASM-001  
**Revision:** 1.1 (Rev G Phase 6B Production Baseline)  
**Date:** November 18, 2026  

---

## 1. TOOLS & CONSUMABLES REQUIRED
- Clean ESD-safe assembly mat and grounded wrist strap.
- Precision tweezers (curved and straight point).
- Miniature Phillips / slotted screwdriver set.
- 0.5mm pitch FFC insertion tool.
- Thermal-cure cyanoacrylate or UV-curable structural adhesive (Loctite 401 or equivalent).
- High-tack Kapton polyimide tape ($5.0\text{ mm}$ width).
- Industrial isopropyl alcohol ($> 99.5\%$) and lint-free swabs.

---

## 2. ASSEMBLY PROCEDURE

### Stage 1: Daughterboard Harnessing
1. **Front MPU Carrier:**
   - Connect the 4-pin JST-SH wire harness (`SHR-04V-S-B`) to receptacle `J1` on `Front_MPU.kicad_pcb`.
   - Slide `Front_MPU.kicad_pcb` into `06_Front_MPU_Carrier.stl` until the rear retention clips snap into place.
2. **MicroSD Carrier:**
   - Insert the 6-pin 0.5mm pitch FFC ribbon into connector `J1` on `MicroSD_Carrier.kicad_pcb` with stiffener facing upward. Flip the actuator bar down to lock.
   - Seat the carrier into `07_MicroSD_Carrier_Mount.stl`.
3. **Touch Sensor:**
   - Connect the 3-pin JST-SH wire harness to `Touch_Sensor.kicad_pcb`. Slide into the internal grip recess.

### Stage 2: Electronics Rail Integration
1. **Haptic Vibration Motor:**
   - Mount the vibration motor into `13_Vibration_Motor_Mount.stl` and route leads to receptacle `J_MOT` on the Main PCB.
   - Note: The motor drive circuit on the Main PCB incorporates inductive flyback clamp diode **`D3`** (`1N5819HW-7-F`) across the motor terminals to suppress inductive turn-off voltage transients.
2. **Battery Cradle & Cell Installation:**
   - Place the LiPo battery pack (Model **`LP300830-PCM`**, $50\text{ mAh}$, max finished dimensions $33.00 \times 8.20 \times 3.30\text{ mm}$) into `05_Battery_Cradle.stl`.
   - Route the 28 AWG silicone leads through the integrated rear wire conduit to connector `J_BAT` on the Main PCB.
3. **Rail Mating:**
   - Slide `05_Battery_Cradle.stl` into the bottom retention rails of `04_Removable_Electronics_Rail.stl`.
4. **Antenna & RF Cabling:**
   - Affix the Molex 146153 wideband antenna onto `14_Antenna_Mount.stl` and connect the U.FL micro-coaxial cable to receptacle `J_RF` on the Main PCB.
5. **Main Board Snap-In:**
   - Snap the Main PCB into the top deck of `04_Removable_Electronics_Rail.stl`. Connect all daughterboard harnesses.

### Stage 3: Click Mechanism & Refill Insertion
1. Drop the helical return spring (`21_Helical_Return_Spring.stl`) into the front nose cone (`03_Front_Nose_Cone.stl`).
2. Insert standard D1 ink refill (`20_D1_Ink_Refill.stl`) into the nose cone.
3. Slide central pushrod (`22_Click_Pushrod.stl`) through the central tunnel of `04_Removable_Electronics_Rail.stl` until it contacts the refill tail.
4. Assemble the 3-piece click engine:
   - Insert stator sleeve (`10C_Click_Guide_Stator.stl`) into the rear barrel bore.
   - Insert cam rotor (`10B_Click_Rotor_Cam.stl`) into the stator sleeve.
   - Insert plunger button (`10A_Click_Plunger_Button.stl`) into the rotor.
5. Mate the rear bayonet collar (`11_Rear_Bayonet_Collar.stl`) by pressing axially and rotating $30^\circ$ clockwise until detent clicks.

### Stage 4: Enclosure Closure & Operational Testing
1. Slide the outer barrel (`01_Outer_Barrel.stl`) over the assembled chassis.
2. Thread the front grip (`02_Front_Grip.stl`) and nose cone (`03_Front_Nose_Cone.stl`) onto the barrel.
3. Cycle the click mechanism 5 times to confirm positive tip extension ($4.50\text{ mm}$ travel) and retraction.
4. Connect USB-C cable through port bezel (`08_USB_C_Access_Feature.stl`) to verify:
   - Charging LED `D2` illuminates.
   - Power-path diode **`D4`** (`1N5819HW-7-F` / `MBR0520L`) and P-FET `Q2` (`DMG2305UX`) seamlessly route USB $V_{\text{BUS}}$ power to `VSYS_RAW`, isolating the battery during charging.
   - ESP32-C3 enumerates on host PC via USB-JTAG/Serial interface.

---

## 3. PHYSICAL ASSEMBLY & PROTOTYPE BOUNDARIES

This manual describes assembly sequences based on validated 3D CAD geometry. Physical validation requires prototype execution:
- Exact mold/print tolerances, snap-fit retention forces, and thermal convection profiles are unverified on physical hardware.
- Solder reflow profiles across the 4-layer FR4 PCB must be established by the assembly house.
- Exact battery supplier qualification and PCM trip thresholds must be verified with physical battery samples.
