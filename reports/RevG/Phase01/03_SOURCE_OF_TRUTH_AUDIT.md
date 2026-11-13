# Smart Pen Rev G — Phase 1: Authoritative Design Source Audit

**Document ID**: `reports/RevG/Phase01/03_SOURCE_OF_TRUTH_AUDIT.md`  
**Execution Date**: November 13, 2026  
**Revision Baseline**: Revision F  
**Target Development Revision**: Revision G  
**Branch**: `engineering/revg-production`  

---

## 1. Executive Summary

A core objective of Phase 1 is resolving the historical ambiguity surrounding duplicate design files in the repository. The repository contains two competing versions of the Main PCB layout (`output/RevF_Working/` vs `output/RevF_Client_Delivery/`), identical daughterboards, and an outdated EasyEDA export.

Through byte-level hashing, structural entity parsing, and fresh KiCad 10.0 CLI rule checks, this audit conclusively establishes the true state of every file and determines the authoritative source baseline for Revision G.

---

## 2. Main PCB Comparison: Working vs. Client Delivery

| Parameter | Main PCB (Working) | Main PCB (Client Delivery) | Discrepancy & Root Cause Analysis |
| :--- | :--- | :--- | :--- |
| **File Path** | `output/RevF_Working/SmartPen.kicad_pcb` | `output/RevF_Client_Delivery/02_KiCad_Source/SmartPen.kicad_pcb` | Separate development trees |
| **File Size** | 71,622 bytes | 91,519 bytes | +19,897 bytes in delivery file |
| **SHA-256 Hash** | `e39c401f1ae25908337d3a3d6bd13e23f50412c336bec848bda14d4da942d4a2` | `37a2f4a69b317719de1fc8e265a421b9c21246e0e598d09eb6c7db66ff76e740` | **Distinct files** |
| **Track Segments** | **191** | **299** | +108 segments in delivery |
| **Via Count** | **78** | **205** | +127 vias in delivery |
| **Footprints** | 60 | 60 | Identical component count |
| **Copper Zones** | 2 (F.Cu GND, B.Cu GND) | 2 (F.Cu GND, B.Cu GND) | Identical zone definitions |
| **Net Naming** | Hierarchical prefix (`/3V3`, `/GND`, etc.) | Flat names (`3V3`, `GND`, etc.) | Delivery stripped leading slash |
| **Fresh DRC Errors**| **185 total** | **1,338 total** | Delivery has massive violations |
| **Shorting Items** | **33** | **199** | Delivery has catastrophic shorts |
| **Track Crossings** | **1** | **199** | Delivery routes directly across tracks |
| **Unconnected Nets**| **29** | **0** | Delivery forced 0 unconnected by shorting |
| **Schematic Parity**| 22 (J_USB pad shifts) | 199 parity errors | Delivery disconnected from schematic |

### Technical Analysis: What Happened in Client Delivery?
An automated script (e.g. `scripts/highway_astar_router.py` or `scripts/build_clean_routed_pcb.py`) was executed to eliminate unconnected ratlines. However, the router's clearance penalty function was disabled or bypassed, causing it to draw copper tracks straight across existing copper geometry, crossing tracks on the same layer 199 times and dead-shorting:
- **3V3 to GND**
- **USB_VBUS (5V) to VBAT (3.7V LiPo)**
- **VBAT to GND** (Direct LiPo dead-short)
- **USB_DM_CORE to USB_DP_CORE** (Differential pair short)
- **UART_TX to UART_RX**

The resulting file achieved a synthetic metric of "0 unconnected pads" but is **physically destructive, electrically lethal, and unmanufacturable**.

### Recommendation
- **`output/RevF_Client_Delivery/02_KiCad_Source/SmartPen.kicad_pcb` MUST BE CONDEMNED AND REJECTED.**
- **`output/RevF_Working/SmartPen.kicad_pcb` is selected as the authoritative layout baseline for Revision G.** It preserves genuine, uncorrupted component placements and routings, requiring targeted routing repair of its 33 via collisions and 29 unrouted connections.

---

## 3. Daughterboard Comparison: Working vs. Client Delivery

All three daughterboard layouts and schematics were audited for divergence between `RevF_Working` and `RevF_Client_Delivery`.

| Board | Working PCB SHA-256 | Delivery PCB SHA-256 | Identity Status | Working SCH SHA-256 | Delivery SCH SHA-256 | Identity Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Front MPU** | `ec59f0dcbee3e9dd...` | `ec59f0dcbee3e9dd...` | **100% BYTE IDENTICAL** | `a33fedfbbcd18857...` | `a33fedfbbcd18857...` | **100% BYTE IDENTICAL** |
| **MicroSD Carrier** | `96eb291ed0d287f9...` | `96eb291ed0d287f9...` | **100% BYTE IDENTICAL** | `6fe97adc5cd62d62...` | `6fe97adc5cd62d62...` | **100% BYTE IDENTICAL** |
| **Touch Sensor** | `cd5027f737b65b27...` | `cd5027f737b65b27...` | **100% BYTE IDENTICAL** | `867a01c8150585f3...` | `867a01c8150585f3...` | **100% BYTE IDENTICAL** |

### Findings
There is **zero discrepancy** between working and delivery versions of the three daughterboards. Both directories contain the exact same physical files.

---

## 4. EasyEDA Export Audit

**Inspected File**: `output/RevF_Client_Delivery/01_EasyEDA_Source/SmartPen_RevF_PCB.json`  
**File Size**: 28,118 bytes  
**JSON Metadata Header**:
```json
{
  "head": {
    "docType": "3",
    "editorVersion": "6.5.51",
    "newgId": true,
    "c_para": {
      "Title": "Smart Pen Rev E PCB",
      "Revision": "Rev E",
      "Company": "RadixView Technologies"
    }
  }
}
```
**Shape Analysis**:
- `TRACK`: 39 segments (Rev F has 191 to 299 segments).
- `VIA`: 20 vias (Rev F has 78 to 205 vias).
- `PAD`: 0 standalone pads.

### Conclusion
`SmartPen_RevF_PCB.json` is **not a Revision F file**. It is an outdated Revision E artifact with Rev E title, Rev E revision metadata, and an unfinished layout of only 39 tracks. It must not be used as an engineering reference for Revision G.

---

## 5. Authoritative Source of Truth Matrix for Revision G

Based on rigorous independent audit, the following files are formally designated as the **Authoritative Sources of Truth** for the Smart Pen project:

| Subsystem | Design Artifact | Authoritative Source File Path | SHA-256 Hash |
| :--- | :--- | :--- | :--- |
| **Main System** | Schematic | `output/RevF_Working/SmartPen.kicad_sch` | `ad190c9369258b47e635ed48262ef6af75193e1345b7fe32bd69d6986bf8ec2f` |
| **Main System** | PCB Layout | `output/RevF_Working/SmartPen.kicad_pcb` | `e39c401f1ae25908337d3a3d6bd13e23f50412c336bec848bda14d4da942d4a2` |
| **Main System** | Footprint Library | `output/RevF_Working/SmartPen.pretty/` | Directory containing 33 custom footprints |
| **Main System** | BOM Baseline | `output/RevF_Client_Delivery/05_BOM_CPL/SmartPen_RevF_BOM.csv` | `03e911296bf38b90c0ef1dbb528b81561f92e3a1f9a2b724581297e641ea5d28` |
| **Front MPU** | Schematic | `output/RevF_Working/Front_MPU/Front_MPU.kicad_sch` | `a33fedfbbcd188579f0e2b3f1e1e031dccaf3cd19d2044326b22d41b14e7f561` |
| **Front MPU** | PCB Layout | `output/RevF_Working/Front_MPU/Front_MPU.kicad_pcb` | `ec59f0dcbee3e9dd3231dc533178eb0d25fb1a9afd5e983fe39afc4b4a08ffcd` |
| **Front MPU** | Footprint Library | `output/RevF_Working/Front_MPU/Front_MPU.pretty/` | JST-SH-4P, MPU-6050, 0402 passes |
| **MicroSD Carrier** | Schematic | `output/RevF_Working/MicroSD_Carrier/MicroSD_Carrier.kicad_sch` | `6fe97adc5cd62d62372e8757ad534230bac0f194692fdb998fb87071effa975e` |
| **MicroSD Carrier** | PCB Layout | `output/RevF_Working/MicroSD_Carrier/MicroSD_Carrier.kicad_pcb` | `96eb291ed0d287f9330e7d8a10a91abe855cec65021ab33c689ba4fe58685768` |
| **Touch Sensor** | Schematic | `output/RevF_Working/Touch_Sensor/Touch_Sensor.kicad_sch` | `867a01c8150585f3b9f7008e9c49d04d2fa6176a0202874109bc16857bd940c7` |
| **Touch Sensor** | PCB Layout | `output/RevF_Working/Touch_Sensor/Touch_Sensor.kicad_pcb` | `cd5027f737b65b273b235a6602430dd1b041cd3997282bfb9377ae00613179c4` |
| **Mechanical Enclosure**| Parametric CAD | `output/RevF_Client_Delivery/07_3D_CAD_Source/SmartPen_Parametric_CAD_RevF.py` | Full 15-part parametric solid generator |
| **Mechanical Master**| Complete STEP | `output/RevF_Client_Delivery/07_3D_STEP/SmartPen_Complete_Assembly.step` | 742,970 bytes master 3D assembly |

---

## 6. Audit Sign-Off

- **Source Determination**: Complete and unambiguous.
- **Corrupted Files Isolated**: `output/RevF_Client_Delivery/02_KiCad_Source/SmartPen.kicad_pcb` and `SmartPen_RevF_PCB.json` quarantined.
- **Phase 1 Status**: **PASS**.
