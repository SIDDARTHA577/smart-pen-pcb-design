# SMART PEN REV G — ELECTRO-MECHANICAL ASSEMBLY & SERVICE MANUAL

**Document ID:** SRG-DOC-ASM-001  
**Revision:** 1.0 (Rev G Production Baseline)  
**Date:** November 17, 2026  

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
1. Mount the vibration motor into `13_Vibration_Motor_Mount.stl` and route wires to `J_MOT` on the Main PCB.
2. Place the battery pack (`Grepow GRP380830-HP-PCM` or `EEMB LP380830`) into `05_Battery_Cradle.stl`. Route the silicone leads through the rear wire conduit to `J_BAT`.
3. Slide `05_Battery_Cradle.stl` into the bottom retention rails of `04_Removable_Electronics_Rail.stl`.
4. Affix the Molex 146153 antenna onto `14_Antenna_Mount.stl` and connect the U.FL micro-coaxial cable to connector `J_RF` on the Main PCB.
5. Snap the Main PCB into the top deck of `04_Removable_Electronics_Rail.stl`. Connect all JST wire harnesses.

### Stage 3: Click Mechanism & Refill Insertion
1. Drop the helical return spring (`21_Helical_Return_Spring.stl`) into the front nose cone (`03_Front_Nose_Cone.stl`).
2. Insert standard D1 ink refill (`20_D1_Ink_Refill.stl`) into the nose cone.
3. Slide central pushrod (`22_Click_Pushrod.stl`) through the central tunnel of `04_Removable_Electronics_Rail.stl` until it contacts the refill tail.
4. Assemble the 3-piece click engine:
   - Insert stator sleeve (`10C_Click_Guide_Stator.stl`) into the rear barrel bore.
   - Insert cam rotor (`10B_Click_Rotor_Cam.stl`) into the stator sleeve.
   - Insert plunger button (`10A_Click_Plunger_Button.stl`) into the rotor.
5. Mate the rear bayonet collar (`11_Rear_Bayonet_Collar.stl`) by pressing axially and rotating $30^\circ$ clockwise until detent clicks.

### Stage 4: Enclosure Closure & Testing
1. Slide the outer barrel (`01_Outer_Barrel.stl`) over the assembled chassis.
2. Thread the front grip (`02_Front_Grip.stl`) and nose cone (`03_Front_Nose_Cone.stl`) onto the barrel.
3. Cycle the click mechanism 5 times to confirm positive tip extension and retraction.
4. Connect USB-C cable through port bezel (`08_USB_C_Access_Feature.stl`) to verify charging LED `D2` illumination and enumeration on host PC.
