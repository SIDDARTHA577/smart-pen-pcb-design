# Smart Pen Rev G — Phase 1: Automated Test Suite Reliability Audit

**Document ID**: `reports/RevG/Phase01/10_TEST_SUITE_RELIABILITY_AUDIT.md`  
**Execution Date**: November 13, 2026  
**Test Runner**: `pytest-9.1.1` (Python 3.11.9)  
**Branch**: `engineering/revg-production`  

---

## 1. Executive Summary

A comprehensive reliability audit of the existing 13 test modules in `tests/` was conducted. When executed under standard pytest, the regression suite returned:

```
============================= 46 passed in 0.52s ==============================
```

Despite achieving a **100% pass rate in 0.52 seconds**, independent engineering audit proves that the physical design contains **1,338 DRC violations, 199 dead shorts, a floating LDO regulator output, an unsafe 303 mA battery charge rate, and missing firmware and browser software**.

In accordance with **Engineering Integrity Rule 2: "Do not treat successful Python unit tests as proof of a functional physical PCB,"** this audit dissects the failure modes of the automated test suite and specifies the necessary test harness refactoring.

---

## 2. Test Module Inventory & Diagnostic Breakdown

| Test Module File | Test Count | Reported Status | True Engineering Quality | Root Cause of Failure / False Pass |
| :--- | :---: | :---: | :---: | :--- |
| `tests/test_power_path.py` | 4 | **PASSED** | **CRITICAL FALSE PASS** | Hardcodes theoretical numbers; tests components (`DMG2305UX`) that do not exist |
| `tests/test_pcb.py` | 4 | **PASSED** | **CRITICAL FALSE PASS** | Evaluates legacy Rev E file (`output/RevE_work/SmartPen_RevE_PCB.json`), not Rev F |
| `tests/test_gerbers.py` | 2 | **PASSED** | **CRITICAL FALSE PASS** | Tests legacy Rev E delivery folder (`output/client_delivery/04_Gerber_Drill`) |
| `tests/test_microsd_carrier.py`| 4 | **PASSED** | **FALSE PASS** | Reads static `.rpt` file committed on disk; does not run live KiCad CLI DRC |
| `tests/test_touch_sensor.py` | 5 | **PASSED** | **COSMETIC ONLY** | Asserts text substring `(end 6.0 18.0)` exists; calls it "DRC clean" |
| `tests/test_front_mpu.py` | 5 | **PASSED** | **COSMETIC ONLY** | Checks file existence and static text; skips live KiCad CLI verification |
| `tests/test_delivery_integrity.py`| 5 | **PASSED** | **SHALLOW PASS** | Asserts directory and file existence (`size > 1000`); passes on corrupted files |
| `tests/test_assembly_cad.py` | 5 | **PASSED** | **COSMETIC ONLY** | Verifies STEP file size > 5000 bytes; does not test solid BRep clashes |
| `tests/test_assembly_clearance.py`| 1 | **PASSED** | **SHALLOW PASS** | Runs nominal 1D mathematical bounding-box subtraction; ignores CAD solid |
| `tests/test_mechanical.py` | 3 | **PASSED** | **COSMETIC ONLY** | Checks STL facet normal headers; watertight mesh does not prove fit |
| `tests/test_gpio_architecture.py` | 2 | **PASSED** | **DOCUMENTATION ONLY**| Checks text file exists on disk; does not verify live schematic nets |
| `tests/test_netlist.py` | 2 | **PASSED** | **SHALLOW PASS** | Compares component count (60 == 60); ignores pin-level shorts and pad mismatches |
| `tests/test_schematic.py` | 4 | **PASSED** | **SHALLOW PASS** | Asserts symbol count == 60; misses that LDO Pin 5 is floating and Pin 3 is misrouted |
| **TOTAL** | **46** | **100% PASS** | **UNRELIABLE** | **Fails to detect any P0 or P1 hardware defects** |

---

## 3. Detailed Case Studies in Test Failure

### Case Study 1: Fabricated Component Assertions (`test_power_path.py`)
In `tests/test_power_path.py`:
```python
def test_power_path_load_switch_parameters(self):
  # P-FET DMG2305UX-7: R_ds(on) max = 52 mOhm
  r_ds_on = 0.052
  i_system_peak = 0.150  # 150 mA typical system draw on battery
  v_drop = i_system_peak * r_ds_on  # 7.8 mV drop
  power_loss_mw = (i_system_peak**2) * r_ds_on * 1000.0  # 1.17 mW
  self.assertLess(v_drop, 0.015, "Battery path voltage drop must be < 15 mV")
  self.assertLess(power_loss_mw, 5.0, "Battery path power loss must be < 5 mW")
```
- **Analysis**: The test does not open `SmartPen.kicad_sch`. It does not parse `SmartPen_RevF_BOM.csv`. It multiplies two floating-point numbers in memory ($0.150 \times 0.052 = 0.0078$) and asserts that $0.0078 < 0.015$.
- **Reality**: `DMG2305UX` **does not exist** anywhere in the schematic, layout, or BOM. The test passes 100% while verifying a completely non-existent circuit.

### Case Study 2: Testing Outdated Revision Assets (`test_pcb.py`)
In `tests/test_pcb.py`:
```python
def setUp(self):
  self.pcb_path = Path('output/RevE_work/SmartPen_RevE_PCB.json')
  self.assertTrue(self.pcb_path.exists())
  with open(self.pcb_path, 'r', encoding='utf-8') as f:
    self.pcb = json.load(f)
```
- **Analysis**: The test explicitly loads `output/RevE_work/SmartPen_RevE_PCB.json`.
- **Reality**: The test suite has been testing **Revision E** legacy JSON files. It never opened `output/RevF_Working/SmartPen.kicad_pcb` or `output/RevF_Client_Delivery/.../SmartPen.kicad_pcb`. As a result, the 1,338 DRC violations and 199 dead shorts in Rev F were invisible to pytest.

### Case Study 3: Checking Static Text Reports on Disk (`test_microsd_carrier.py`)
In `tests/test_microsd_carrier.py`:
```python
def test_carrier_drc_clean(self):
  drc_rpt = self.carrier_dir / 'drc_carrier.rpt'
  self.assertTrue(drc_rpt.exists())
  with open(drc_rpt, 'r', encoding='utf-8') as f:
    content = f.read()
  self.assertIn('Found 0 DRC violations', content)
```
- **Analysis**: The test asserts that a text file `drc_carrier.rpt` exists on disk and contains the string `"Found 0 DRC violations"`.
- **Reality**: If an engineer modifies `MicroSD_Carrier.kicad_pcb` and introduces 500 shorts, the test continues to pass because it reads a historical text file that was committed to Git weeks earlier.

### Case Study 4: Substring Presence as "DRC Verification" (`test_touch_sensor.py`)
In `tests/test_touch_sensor.py`:
```python
def test_touch_pcb_drc_clean(self):
  pcb_text = (self.touch_dir / 'Touch_Sensor.kicad_pcb').read_text(
      encoding='utf-8'
  )
  self.assertIn('(end 6.0 18.0)', pcb_text)
  self.assertIn('"TOUCH_OUT"', pcb_text)
```
- **Analysis**: The test searches for the raw string `'(end 6.0 18.0)'` in the PCB file. If found, it declares the board "DRC clean".
- **Reality**: Finding a line of text in an S-expression file provides zero information regarding electrical shorts, clearance violations, or manufacturability.

---

## 4. Required Phase 2 Test Harness Overhaul

To eliminate false passes and establish hardware quality assurance, the test suite must be completely refactored in Phase 2:

1. **Subprocess Invocation of Official CLI**:
   - Every board test must invoke `kicad-cli pcb drc --format json` and `kicad-cli sch erc --format json`.
   - The test must parse the output JSON and assert `len(data['violations']) == 0` and `len(data['unconnected_items']) == 0`.
2. **Schematic-to-BOM Parity Validation**:
   - Parse `kicad-cli sch export netlist` and match 1:1 against `SmartPen_RevF_BOM.csv`.
   - Flag any component with pin count, package, or reference mismatch (e.g. `J_PWR` 3 pins vs 5 pins).
3. **Dynamic Netlist Verification**:
   - Programmatically trace power nets (`/3V3`, `/VBAT`, `/USB_VBUS`, `/GND`) from the netlist to assert that:
     - LDO Pin 5 connects to `/3V3`.
     - LDO Pin 3 (EN) connects to `/VBAT_SW`.
     - `USB_VBUS` does not short to `VBAT`.
4. **Targeted Revision Path Binding**:
   - Bind all tests dynamically to the active revision directory (`output/RevG/` or `output/RevF_Working/`), eliminating all references to `RevE_work` and `client_delivery`.

---

## 5. Audit Sign-Off

- **Root Cause of 100% Pass Rate Documented**: Hardcoded assertions, legacy file paths, and static text matching.
- **Phase 1 Status**: **FAIL (Current Test Suite Declared Untrustworthy)**.
