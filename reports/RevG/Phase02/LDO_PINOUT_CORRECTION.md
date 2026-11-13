# SMART PEN REVISION G — LDO PINOUT CORRECTION & VOLTAGE REGULATION ARCHITECTURE
## Resolution of Critical Issue ISSUE-01

- **Project:** Smart Pen PCB Design
- **Document ID:** `REVG-DOC-LDO-001`
- **Revision:** Rev G Phase 2 Freeze Candidate
- **Author:** Senior Embedded Electronics & Power Engineer
- **Component Under Review:** Diodes Inc. `AP2112K-3.3TRG1` (Reference `U4`, formerly `J_PWR`)

---

## 1. Problem Statement & Root Cause Analysis

In Revision F, the primary 3.3V system LDO was assigned reference designator `J_PWR` and represented by a 3-pin schematic symbol. Inspection of the schematic and PCB revealed a catastrophic hardware failure mode:

### 1.1 Pin Mapping Discrepancy
- The physical device specified in the BOM is the Diodes Incorporated **AP2112K-3.3TRG1**, packaged in an industry-standard **SOT-23-5** package.
- The authoritative manufacturer datasheet specifies the SOT-23-5 pinout as follows:
  - **Pin 1:** `VIN` — Input Voltage Supply (2.5V to 6.0V)
  - **Pin 2:** `GND` — Ground Return
  - **Pin 3:** `EN` — Active-High Enable Control ($V_{IH} \ge 1.5\text{ V}$, $V_{IL} \le 0.4\text{ V}$)
  - **Pin 4:** `NC` — No Connection (internally floating)
  - **Pin 5:** `VOUT` — Regulated Output Voltage (+3.3V, 600mA rated)

### 1.2 The Rev F Flaw
- The schematic symbol `J_PWR` defined only 3 pins:
  - Symbol Pin 1 labeled "VIN"
  - Symbol Pin 2 labeled "GND"
  - Symbol Pin 3 labeled "VOUT"
- Because KiCad matches schematic pins to footprint pads by **pin number**, symbol Pin 3 mapped to **Pad 3** of the SOT-23-5 footprint.
- Consequently, Net `/3V3` was routed to Pad 3 (`EN`), while Pad 5 (`VOUT`) had no schematic pin and was left completely unrouted/floating on the PCB!
- When power was applied via `/VBAT_SW`, input voltage entered Pin 1 (`VIN`), but the regulator output Pin 5 (`VOUT`) remained disconnected. The entire 3.3V system rail received **0.00 V**, resulting in an unbootable, non-functional hardware assembly.

```
       Rev F Schematic (Defective):                 Rev F PCB Net Mapping (Dead-on-Arrival):
       +-----------------------+                    +------------------------------------+
       |         J_PWR         |                    | SOT-23-5 Footprint                 |
VIN ---| 1 (VIN)      3 (VOUT) |--- /3V3            | Pad 1: VIN   <--- Net /VBAT_SW     |
GND ---| 2 (GND)               |                    | Pad 2: GND   <--- Net /GND         |
       +-----------------------+                    | Pad 3: EN    <--- Net /3V3 (ERROR!)|
                                                    | Pad 4: NC    <--- Unconnected      |
                                                    | Pad 5: VOUT  <--- NO NET / 0V!     |
                                                    +------------------------------------+
```

---

## 2. Rev G Engineering Correction

In Revision G Phase 2, the symbol, library definition, reference designator, and schematic connections were systematically rebuilt:

### 2.1 Component & Library Updates
1. **Reference Designator:** Changed from `J_PWR` (which improperly used a connector prefix 'J') to `U4`, adhering to standard IEEE 315 / ANSI reference designators for active integrated circuits.
2. **Symbol Definition:** Created a dedicated 5-pin symbol in `SmartPen_Lib.kicad_sym` and `SmartPen.kicad_sch` `(lib_symbols)`:
   - `Pin 1` (passive/power_in): Name `VIN`, Number `"1"`
   - `Pin 2` (passive/power_in): Name `GND`, Number `"2"`
   - `Pin 3` (passive/input): Name `EN`, Number `"3"`
   - `Pin 4` (no_connect): Name `NC`, Number `"4"`
   - `Pin 5` (passive/power_out): Name `VOUT`, Number `"5"`
3. **Footprint Assignment:** Footprint remains `SmartPen:J_PWR`, which was already verified as a true 5-pad SOT-23-5 footprint with pads 1 through 5 matching standard JEDEC TO-236AB geometry.

### 2.2 Schematic Wiring Architecture
- **Pin 1 (VIN):** Wired to switched system supply net `/VBAT_SW`.
- **Pin 2 (GND):** Wired directly to system ground net `/GND`.
- **Pin 3 (EN):** Wired to switched supply net `/VBAT_SW`. When physical power switch `SW3` is closed (ON), Pin 3 rises to $V_{BAT}$ (3.2V–4.2V) or $V_{BUS}-V_D$ (4.65V), which exceeds the $1.5\text{ V}$ enable threshold ($V_{IH}$) and activates the LDO. When `SW3` is open (OFF), `VBAT_SW` collapses to 0V, disabling the regulator and ensuring zero quiescent current leakage.
- **Pin 4 (NC):** Explicitly marked with an official KiCad `(no_connect)` symbol at coordinate `(144.78, 190.50)` to ensure 100% clean ERC without floating-pin warnings.
- **Pin 5 (VOUT):** Wired directly to primary system supply net `/3V3`.

```
       Rev G Corrected Schematic Wiring:
       +---------------------------------------------+
       |                     U4                      |
       |               AP2112K-3.3TRG1               |
       |                  (SOT-23-5)                 |
       |                                             |
VBAT_SW --------| 1 (VIN)                             |
                |                                     |
GND ------------| 2 (GND)                    5 (VOUT) |-------- /3V3 (System Rail)
                |                                     |
VBAT_SW --------| 3 (EN)                              |
                |                                     |
NC   --(X)------| 4 (NC)                              |
       +---------------------------------------------+
```

---

## 3. Electrical Characteristics & Thermal Performance

### 3.1 Key Specifications of AP2112K-3.3TRG1
- **Regulated Output Voltage ($V_{OUT}$):** 3.3V ±1.5% accuracy over temperature.
- **Maximum Continuous Output Current ($I_{OUT(max)}$):** 600 mA (easily handles ESP32-C3 peak Wi-Fi/BLE transmission bursts of ~240–310 mA + sensors ~25 mA).
- **Ultra-Low Dropout Voltage ($V_{DROP}$):**
  - Typical $250\text{ mV}$ at $I_{OUT} = 300\text{ mA}$
  - Typical $120\text{ mV}$ at $I_{OUT} = 100\text{ mA}$
  - Minimum operating battery voltage: $V_{BAT(min)} = V_{OUT} + V_{DROP} = 3.3\text{ V} + 0.12\text{ V} = 3.42\text{ V}$.
  - Over 90% of the usable LiPo discharge curve (3.45V to 4.2V) is within full 3.3V regulation!
- **Quiescent Current ($I_Q$):** Typical $55\,\mu\text{A}$ active; $< 1.0\,\mu\text{A}$ in shutdown.
- **Power Supply Rejection Ratio (PSRR):** $65\text{ dB}$ at 1 kHz, providing excellent noise immunity against USB input ripple.

### 3.2 Thermal Dissipation & Temperature Rise
During normal continuous operation (ESP32-C3 BLE connected + MPU-6050 reading, average current $I_{SYS} \approx 65\text{ mA}$):
- Input voltage from battery: $V_{IN(nom)} = 3.8\text{ V}$
- Dropout across regulator: $\Delta V = 3.8\text{ V} - 3.3\text{ V} = 0.5\text{ V}$
- Power dissipation: $P_D = 0.5\text{ V} \times 0.065\text{ A} = 0.0325\text{ W} = 32.5\text{ mW}$
- SOT-23-5 Thermal Resistance ($\theta_{JA}$): $\approx 230^\circ\text{C/W}$
- Temperature rise: $\Delta T = 0.0325 \times 230 \approx 7.5^\circ\text{C}$ (negligible).

During worst-case operating mode (Wi-Fi data transfer active while operating from USB power, $V_{IN} \approx 4.65\text{ V}$, $I_{SYS} = 180\text{ mA}$ average):
- $\Delta V = 4.65\text{ V} - 3.3\text{ V} = 1.35\text{ V}$
- $P_D = 1.35\text{ V} \times 0.180\text{ A} = 0.243\text{ W} = 243\text{ mW}$
- Temperature rise: $\Delta T = 0.243 \times 230 \approx 55.9^\circ\text{C}$
- Junction temperature at $25^\circ\text{C}$ ambient: $T_J = 25 + 55.9 = 80.9^\circ\text{C}$
- Safe margin below maximum rated junction temperature ($T_{J(max)} = 125^\circ\text{C}$): **44.1°C margin**.

---

## 4. Verification Evidence

1. **ERC Validation:** Ran `kicad-cli sch erc` on `SmartPen.kicad_sch`. Reported **0 Errors, 0 Warnings**.
2. **Netlist Verification:** In `Main_SmartPen_netlist.net`:
   - Pin 1: `/VBAT_SW`
   - Pin 2: `/GND`
   - Pin 3: `/VBAT_SW`
   - Pin 4: `unconnected-(U4-NC-Pad4)`
   - Pin 5: `/3V3`
3. **Automated Unit Test:** `tests/test_revg_electrical.py::TestRevGElectrical::test_ap2112k_ldo_pinout_and_connections` executed and **PASSED**.
4. **Negative Test Fixture:** `tests/test_revg_electrical.py::TestRevGElectricalNegativeFixtures::test_negative_floating_ldo_output_fails` executed and proved that any omitted Pin 5 connection triggers immediate build failure.
