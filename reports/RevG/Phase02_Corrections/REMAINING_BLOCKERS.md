# SMART PEN REVISION G — REMAINING BLOCKERS & PHASE 3 ENTRY GATES
## Actionable Hold Ledger and Prerequisites for PCB Layout Authorization

- **Project:** Smart Pen Hardware System
- **Document ID:** `REVG-DOC-BLOCKERS-002`
- **Revision:** Rev G Phase 2.1
- **Status:** FORMAL HOLD ON PHASE 3 (LAYOUT AUTHORIZATION PENDING)
- **Author:** Senior Multidisciplinary Engineering Team

---

## 1. Statement of Milestone Status

With the execution of Phase 2.1:
- The P-MOSFET body-diode uncontrolled charging hazard (`Q2`) has been resolved.
- The USB-C connector physical footprint (`J_USB`) has been upgraded with authentic through-hole shield slots and NPTH locating holes.
- The ESP32-C3FH4X strapping pin (`GPIO8`) and internal flash pinout (`Pins 19–24`) have been corrected to restore ROM Download Boot and protect the internal Quad SPI flash die.
- The automated test suite has been repaired and expanded with physics-based constraints and negative fault detection fixtures (59/59 passing).

**Phase 2.1 is complete. However, Phase 3 (PCB Layout & Rerouting) is NOT authorized and has NOT been started.**

---

## 2. Actionable Blocker Ledger & Phase 3 Entry Criteria

The following items are retained as active engineering holds that require formal client sign-off or physical hardware validation prior to authorizing Phase 3 PCB layout freeze and fabrication:

### BLOCKER 1: Physical Battery Sample Procurement & Mechanical Cradle Signoff
- **Constraint:** R3 (Battery beneath internal removable rail, cradle pocket $46.0\text{ mm} \times 10.0\text{ mm} \times 4.5\text{ mm}$).
- **Status:** **BLOCKED (Customer Signoff Required)**.
- **Engineering Recommendation:** Adopt **Candidate A (LP401035, $140\text{ mAh}$)**. With bare dimensions of $4.0 \times 10.0 \times 35.0\text{ mm}$ and pack length of $37.0\text{ mm}$ (including PCM), it provides $9.0\text{ mm}$ of longitudinal clearance for the 28 AWG wire loop and JST SH connector.
- **Disqualified Option:** Candidate B (LP401040, $300\text{ mAh}$) leaves only $2.0\text{ mm}$ of clearance, introducing severe wire pinch and shearing risks during pen assembly.
- **Required Action:** Client must review the comparative battery analysis (`BATTERY_AND_CHARGING_SAFETY_REVIEW.md`) and grant formal written approval of the $140\text{ mAh}$ cell capacity and cradle dimensions.

### BLOCKER 2: Front MPU Cable Harness Strain Relief & Tip Clearance Verification
- **Constraint:** R2 (Detachable front MPU on dedicated mechanical carrier, keyed 4-pin connector, no mechanical weight on connector).
- **Status:** **BLOCKED (Physical Prototype Fit Check Required)**.
- **Design Status:** Schematic and netlist pinout for the 4-pin interface are frozen:
  - Pin 1: `/3V3`
  - Pin 2: `/GND`
  - Pin 3: `/I2C_SDA`
  - Pin 4: `/I2C_SCL`
- **Required Action:** Fabricate 3D prototype nosecone and assemble sample silicone wire harness ($25\text{ mm}$, 30 AWG stranded, JST SH 1.0mm) to verify that the refill movement during click/retract does not rub against the sensor harness.

### BLOCKER 3: Capacitive Nib Touch Electrode Dielectric Calibration
- **Constraint:** R4 (Capacitive WRITE grip detection).
- **Status:** **HOLD (Pending Enclosure Material Confirmation)**.
- **Design Status:** Touch Sensor PCB outline and copper electrode geometry are verified.
- **Required Action:** Client must confirm the final production material of the grip section (anodized aluminum with insulating sleeve vs molded polycarbonate). Tuning of sensitivity threshold resistor $R_s$ / sensor integration parameters will be finalized during initial plastic casing trial.

### BLOCKER 4: Hot-Plug Oscilloscope Bench Validation
- **Constraint:** Load-sharing glitch depth and inrush current validation.
- **Status:** **HOLD (Bench Prototype Prerequisite)**.
- **Design Status:** The P-MOSFET source/drain reversal guarantees reverse-bias during USB powering ($V_{bias} = -0.45\text{ V}$).
- **Required Action:** Upon board bring-up in Phase 4, perform oscilloscope measurement of the $3.3\text{ V}$ rail transient during hot USB unplug at maximum write activity to verify that voltage sag remains $\le 5\%$ ($> 3.135\text{ V}$).

---

## 3. Explicit Phase Commitment

In strict accordance with the Master Engineering Instructions:
- PCB rerouting on the Main PCB has not been initiated.
- No manufacturing files (Gerbers, drills, IPC-D-356) have been generated for Rev G.
- Branch `engineering/revg-production` remains at the schematic correction stage.

**PHASE 2.1 EXECUTED — PHASE 3 NOT STARTED.**
