# SMART PEN REV G — PROTOTYPE VALIDATION & PHYSICAL TESTING GUIDE

**Document ID:** SRG-DOC-VAL-001  
**Revision:** 1.1 (Phase 6B Production Baseline)  
**Date:** November 18, 2026  
**Scope:** Engineering Recommendations for Physical Hardware Bring-Up & Explicit Digital Boundaries  

---

## 1. SCOPE NOTE & DIGITAL BOUNDARY DISCLOSURE

Per the contract mission statement:
> *"COMPLETE DIGITAL PCB DESIGN + 3D PRINTABLE MECHANICAL DESIGN + MANUFACTURING FILES + FINAL CLIENT HANDOFF. NO physical fabrication, hardware purchase, assembly, or bench testing is required."*

All calculations, 3D clearance audits, kinematic motion sweeps, and DRC/ERC checks in this delivery are based on validated CAD geometry, silicon datasheets, and native KiCad rule engines. Physical hardware testing must be executed by the client during initial prototype bench bring-up.

---

## 2. EXPLICIT OUTSTANDING HARDWARE & VENDOR QUALIFICATIONS

The following real-world engineering attributes cannot be certified within a digital-only delivery and remain subject to physical hardware and vendor qualification:

1. **Battery Supplier & Finished Pack Specification:**
   - The cell Model `LP300830-PCM` ($50\text{ mAh}$, nominal $3.7\text{ V}$, max finished $33.00 \times 8.20 \times 3.30\text{ mm}$) has been validated geometrically for cradle fit ($+0.437\text{ mm}$ bore clearance). However, the specific cell manufacturer, protection circuit module (PCM) overcurrent/undervoltage cutoff tolerances, and cell lot consistency are not qualified.
   - Final battery certification (UN 38.3 transport safety, IEC 62133-2 secondary lithium safety, UL 1642) and actual runtime require physical vendor evidence and prototype discharge testing.
2. **Wi-Fi High-Power Operation & Firmware Enforcement:**
   - Full-power Wi-Fi 802.11b transmission ($385\text{ mA}$ peak at $+19.5\text{ dBm}$) is designed and thermally allocated for **USB-connected operation only**, where power is drawn from USB $V_{\text{BUS}}$ via diode `D4`, with the battery isolated by P-FET `Q2`.
   - Firmware enforcement restricting high-power Wi-Fi transmission when operating on battery power is an external integration requirement; no firmware has been implemented or verified within this digital design deliverable.
3. **RF Antenna Over-The-Air Performance:**
   - The Molex 146153 wideband antenna layout, $50\ \Omega$ CPW-G line, and U.FL routing comply with design rules, but over-the-air (OTA) return loss ($S_{11}$), radiation efficiency, and user hand phantom detuning must be measured in an RF anechoic chamber.
4. **Physical Assembly Tolerances & Mechanical Wear:**
   - Kinematic click stroke ($4.50\text{ mm}$) and clearances ($0.0000\text{ mm}^3$ collision across 351 pairs) are proven in CAD. Physical snap-fit forces, friction, spring fatigue, and cyclic cam wear (Rotor Cam `10B` and Guide Stator `10C`) require physical prototype endurance testing.
5. **PCBA SMT Reflow & Solder Integrity:**
   - Footprints comply with IPC-7351B, but reflow thermal profiles across continuous internal copper planes and solder paste volumes for 0201/0402 passives must be validated by the assembly house.

---

## 3. RECOMMENDED PHYSICAL BRING-UP SEQUENCE

### Phase A: Bare PCB Inspection & Unpowered Testing
1. Visual inspection under stereo microscope for solder bridges, tombstoning, and component polarity (especially SOT-23 pin 1 dots and QFN pin 1 markings).
2. Measure unpowered resistance from `3V3`, `VBAT`, and `USB_VBUS` to `GND`. Confirm no direct shorts ($R > 100\text{ k}\Omega$).
3. Inspect ENIG plating uniformity and solder mask integrity across 0402 footprints.

### Phase B: Power & Charging Bench Testing
1. Connect external bench power supply with current limit set to $100\text{ mA}$ at $3.70\text{ V}$ to battery connector `J_BAT`.
2. Measure quiescent current draw with slide switch `SW3` OFF ($I < 1\ \mu\text{A}$) and ON ($I \approx 22\text{ mA}$).
3. Measure AP2112K LDO output on test pad: confirm $3.30\text{ V} \pm 1.5\%$.
4. Plug 5.0V USB-C power source into `J_USB`.
   - Verify charging LED `D2` (Red) turns ON.
   - Measure charge current with in-line ammeter: confirm $50.0\text{ mA} \pm 5\text{ mA}$ ($R_9 = 20.0\text{ k}\Omega$).
   - Monitor MCP73831 case temperature with thermocouple: worst-case power dissipation is $P_D = (5.0\text{ V} - 3.0\text{ V}) \times 50\text{ mA} = 100\text{ mW}$, yielding expected IC rise $\Delta T \le 23.0^\circ\text{C}$ ($T_{J,\text{IC}} \le 48.0^\circ\text{C}$).
   - Disconnect battery; confirm system continues operating seamlessly on USB power via power-path diode **`D4`** and P-FET **`Q2`**.
   - Verify inductive flyback diode **`D3`** clamps motor inductive spikes when haptic motor is pulsed.

### Phase C: ESP32-C3 Firmware Flash & RF Verification
1. Connect USB-C to PC; verify ESP32-C3 internal USB-JTAG/Serial enumerates.
2. Flash diagnostic firmware image (`esptool.py flash`).
3. Execute Wi-Fi scan and 802.11b TX burst at $+19.5\text{ dBm}$ (while USB connected) while probing `3V3` rail with oscilloscope (AC coupled). Confirm voltage dip is $\le 120\text{ mV}$ and rail stays safely above $3.00\text{ V}$ brownout threshold.
4. Verify BLE pairing and continuous IMU 6-axis stream from MPU-6050 over I2C bus at 400 kHz.

### Phase D: Mechanical Click & 3D Print Testing
1. 3D print mechanical enclosure parts in SLA / SLS engineering resin or PA12 nylon (Formlabs Tough 2000 or HP Multi Jet Fusion PA12 recommended).
2. Clean support material from internal bayonet lugs and stator teeth.
3. Test click mechanism through 500 retract-extend-retract cycles. Inspect rotor sawteeth for wear or jamming.
