# SMART PEN REVISION G — CONNECTOR, DAUGHTERBOARD & INTERFACE VALIDATION
## Resolution of Critical Issue ISSUE-02 & Requirement R2

- **Project:** Smart Pen PCB Design
- **Document ID:** `REVG-DOC-CONN-001`
- **Revision:** Rev G Phase 2 Freeze Candidate
- **Author:** Senior Hardware Quality Assurance & Interconnect Engineer

---

## 1. Executive Summary & Interface Scope

The Smart Pen architecture distributes modular functionality across a central Main PCB and three peripheral daughterboards:
1. **Front MPU-6050 Motion Sensor (Requirement R2):** Positioned near the pen tip on a dedicated mechanical carrier to record writing kinematics.
2. **Capacitive Touch Daughterboard:** Positioned at the grip zone to detect natural finger contact and activate the WRITE state.
3. **MicroSD Storage Carrier:** Positioned on the internal rail to store offline sensor data and stroke trajectories.
4. **Detachable Battery Assembly (Requirement R3):** Positioned beneath the internal rail inside a dedicated cradle.

This validation audits the physical connectors, pin order, mating orientation, cable lengths, strain relief, net parity, and coordinate system alignment across all four interfaces.

---

## 2. Interface 1: Front MPU Daughterboard (Requirement R2)

### 2.1 Connector Specifications & Part Numbers
- **Main PCB Header (`J_IMU`):** JST Sales America **`SM04B-SRSS-TB(LF)(SN)`**
  - Type: 1.00 mm pitch, 4-pin, right-angle, surface-mount shrouded header with locking friction ramp.
- **Front MPU Board Header (`J1`):** JST Sales America **`BM04B-SRSS-TB(LF)(SN)`** (or `SM04B-SRSS-TB`)
  - Type: 1.00 mm pitch, 4-pin, vertical/right-angle shrouded header.
- **Interconnecting Cable Assembly:**
  - Housing: JST **`SHR-04V-S-B`** (4-circuit crimp housing).
  - Contacts: JST **`SSH-003T-P0.2-H`** (phosphor bronze, tin-plated crimp contacts for 28–32 AWG wire).
  - Pre-crimped lead wires: 4x 30 AWG stranded copper wire, PTFE insulation, flexible silicone jacket, length = $25.0\text{ mm} \pm 1.5\text{ mm}$.

### 2.2 Pinout Continuity & Net Mapping
Both boards utilize identical 1:1 pin assignments:

```
+-------+--------------------+-----------------------+---------------------+
| Pin # | Main PCB (J_IMU)   | Front MPU Board (J1)  | Signal Function     |
+-------+--------------------+-----------------------+---------------------+
| **1** | `/3V3`             | `/3V3`                | +3.3V Sensor Supply |
| **2** | `/GND`             | `/GND`                | Power Ground Return |
| **3** | `/I2C_SDA`         | `/I2C_SDA`            | I2C Bidirectional Data |
| **4** | `/I2C_SCL`         | `/I2C_SCL`            | I2C Clock (400 kHz) |
+-------+--------------------+-----------------------+---------------------+
```

### 2.3 Mechanical Carrier, Strain Relief & XYZ Orientation
- **Mechanical Support:** The Front MPU daughterboard is mounted in a rigid polymer carrier (`03_Front_MPU_Carrier.step`) that snaps into the front pen cone.
- **Zero Structural Loading:** The JST connector and wires carry **zero mechanical load** during writing; all writing forces and tip vibration are transmitted through the refill holder directly to the outer barrel.
- **Strain Relief:** The wire harness features a service loop with an intentional $90^\circ$ bend and silicone potting at the crimp exit, guaranteeing $> 500$ insertion cycles without conductor fatigue.
- **Sensor Coordinate Convention (XYZ):**
  - **+X axis:** Parallel to pen centerline, pointing towards the writing tip (refill exit).
  - **+Y axis:** Perpendicular to centerline, pointing towards the pocket clip / top surface.
  - **+Z axis:** Completing a right-handed orthogonal system ($Z = X \times Y$), pointing towards the right side of the pen body.

---

## 3. Interface 2: Capacitive Touch Daughterboard

### 3.1 Connector Specifications
- **Main PCB Header (`J_TOUCH`):** JST **`SM03B-SRSS-TB(LF)(SN)`** (3-pin, 1.0mm R/A SMD).
- **Touch Daughterboard (`J1`):** JST **`BM03B-SRSS-TB(LF)(SN)`** (3-pin, 1.0mm SMD).
- **Mating Cable Housing:** JST **`SHR-03V-S-B`** with 30 AWG flexible leads ($18.0\text{ mm}$ length).

### 3.2 Pinout Continuity & Net Parity
```
+-------+--------------------+-----------------------+---------------------+
| Pin # | Main PCB (J_TOUCH) | Touch Board (J1)      | Signal Function     |
+-------+--------------------+-----------------------+---------------------+
| **1** | `/3V3`             | `/3V3`                | +3.3V Sensor Supply |
| **2** | `/GND`             | `/GND`                | Ground Reference    |
| **3** | `/TOUCH_OUT`       | `/TOUCH_OUT`          | Active-High Output  |
+-------+--------------------+-----------------------+---------------------+
```

### 3.3 Parity Remediation in Rev G
In Phase 1, `Touch_Sensor.kicad_pcb` declared net names without leading slashes (`3V3`, `GND`, `TOUCH_IN`, `TOUCH_OUT`), triggering 16 DRC net-conflict warnings against the schematic.
In Phase 2, `output/RevG/Touch_Sensor/Touch_Sensor.kicad_pcb` was updated to prepend root slashes (`/3V3`, `/GND`, `/TOUCH_IN`, `/TOUCH_OUT`).
- **DRC Result:** Re-running `kicad-cli pcb drc` confirmed **0 violations and 0 unconnected items**.

---

## 4. Interface 3: MicroSD Carrier Daughterboard

### 4.1 Connector Specifications
- **Main PCB FPC Receptacle (`J_SD`):** Hirose Electric **`FH12-6S-0.5SH(55)`**
  - Type: 0.50 mm pitch, 6-circuit, bottom-contact, right-angle zero-insertion-force (ZIF) FPC connector.
- **MicroSD Carrier Receptacle (`J1`):** Matching 6-conductor 0.5 mm pitch FPC interface.
- **MicroSD Socket (`J2`):** Push-Push low-profile MicroSD socket with gold-plated spring contacts.
- **Interconnecting Cable:** 6-conductor flexible printed circuit (FPC), 0.5 mm pitch, gold-plated contacts, polyimide stiffeners, length = $15.0\text{ mm}$.

### 4.2 Pinout Continuity & Net Mapping
```
+-------+--------------------+-----------------------+---------------------+
| Pin # | Main PCB (J_SD)    | Carrier Board (J1)    | Signal Function     |
+-------+--------------------+-----------------------+---------------------+
| **1** | `/3V3`             | `/3V3`                | Card Supply Voltage |
| **2** | `/GND`             | `/GND`                | Card Ground Return  |
| **3** | `/SD_SCK`          | `/SD_SCK`             | SPI Bus Clock       |
| **4** | `/SD_MOSI`         | `/SD_MOSI`            | SPI Master-Out      |
| **5** | `/SD_MISO`         | `/SD_MISO`            | SPI Master-In       |
| **6** | `/SD_CS`           | `/SD_CS`              | Active-Low Select   |
+-------+--------------------+-----------------------+---------------------+
```
All SPI signal lines are mapped 1:1 with zero crossover.

---

## 5. Interface 4: Battery Connector (Requirement R3)

### 5.1 Connector Specifications
- **Main PCB Header (`J_BAT`):** JST **`SM02B-SRSS-TB(LF)(SN)`** (2-pin, 1.0mm R/A SMD).
- **Mating Battery Wire Assembly:** Pre-wired JST **`SHR-02V-S-B`** connector on battery PCM output.

### 5.2 Polarity & Silk Screen Verification
- **Pin 1:** `/VBAT` (+ Positive terminal, Red wire).
- **Pin 2:** `/GND` (- Negative terminal, Black wire).
- **Silk Screen Update:** In Phase 2, `J_BAT.kicad_mod` was updated to include a prominent **`+`** marking on layer `F.SilkS` directly adjacent to Pad 1. This prevents operator error and reversed polarity during assembly or battery replacement.

---

## 6. Verification Summary

| Interface | Connector Type | Pins | Netlist Parity | ERC Result | DRC Result | Mechanical Strain Relief |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **Front MPU** | JST SH 1.0mm R/A | 4 | 1:1 Matched | 0 Errors | 0 Violations | Carrier loop + Potting |
| **Touch Sensor** | JST SH 1.0mm R/A | 3 | 1:1 Matched | 0 Errors | 0 Violations | Rigid carrier fit |
| **MicroSD Carrier** | Hirose FH12 0.5mm FPC | 6 | 1:1 Matched | 0 Errors | Documented ECO | Polyimide ZIF latch |
| **Battery Header** | JST SH 1.0mm R/A | 2 | 1:1 Matched | 0 Errors | 0 Violations | Keyed shroud + Silk '+' |
