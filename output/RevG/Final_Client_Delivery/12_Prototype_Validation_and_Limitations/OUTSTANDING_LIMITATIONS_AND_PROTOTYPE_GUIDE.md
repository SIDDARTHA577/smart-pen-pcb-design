# SMART PEN REV G — PROTOTYPE VALIDATION & PHYSICAL TESTING GUIDE

**Document ID:** SRG-DOC-VAL-001  
**Revision:** 1.0  
**Date:** November 17, 2026  
**Scope:** Engineering Recommendations for Physical Hardware Bring-Up & Validation Testing  

---

## 1. SCOPE NOTE
Per the contract mission statement:
> *"COMPLETE DIGITAL PCB DESIGN + 3D PRINTABLE MECHANICAL DESIGN + MANUFACTURING FILES + FINAL CLIENT HANDOFF. NO physical fabrication, hardware purchase, assembly, or bench testing is required."*

All calculations, 3D clearance audits, kinematic motion sweeps, and DRC/ERC checks in this delivery are based on validated CAD geometry, silicon datasheets, and native KiCad rule engines. Physical hardware testing must be executed by the client during initial prototype bench bring-up.

---

## 2. RECOMMENDED PHYSICAL BRING-UP SEQUENCE

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
   - Monitor MCP73831 case temperature with thermocouple: confirm case temperature rise $\le 25^\circ\text{C}$.
   - Disconnect battery; confirm system continues operating seamlessly on USB power via diode `D3` and P-FET `Q2`.

### Phase C: ESP32-C3 Firmware Flash & RF Verification
1. Connect USB-C to PC; verify ESP32-C3 internal USB-JTAG/Serial enumerates.
2. Flash diagnostic firmware image (`esptool.py flash`).
3. Execute Wi-Fi scan and 802.11b TX burst at $+19.5\text{ dBm}$ while probing `3V3` rail with oscilloscope (AC coupled). Confirm voltage dip is $\le 120\text{ mV}$ and rail stays safely above $3.00\text{ V}$ brownout threshold.
4. Verify BLE pairing and continuous IMU 6-axis stream from MPU-6050 over I2C bus at 400 kHz.

### Phase D: Mechanical Click & 3D Print Testing
1. 3D print mechanical enclosure parts in SLA / SLS engineering resin or PA12 nylon (Formlabs Tough 2000 or HP Multi Jet Fusion PA12 recommended).
2. Clean support material from internal bayonet lugs and stator teeth.
3. Test click mechanism through 500 retract-extend-retract cycles. Inspect rotor sawteeth for wear or jamming.
