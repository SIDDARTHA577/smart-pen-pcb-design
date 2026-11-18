# REMAINING ENGINEERING LIMITATIONS & PROTOTYPE BOUNDARY REPORT

**Document ID:** SRG-P6A-LIM-010  
**Revision:** 1.1 (Phase 6B Final Release)  
**Date:** November 18, 2026  
**Status:** **TECHNICAL AUDIT COMPLETE — HONEST DISCLOSURE OF DIGITAL BOUNDARIES**

---

## 1. DIGITAL DESIGN VS PHYSICAL HARDWARE BOUNDARIES

This engineering release is strictly a **Digital Design Package**. In accordance with contractual mission instructions, no physical PCB fabrication, SMT assembly, component procurement, or lab bench testing was authorized or performed. Consequently, digital simulation and rule verification are complete, but real-world physical behaviors cannot be certified until physical prototypes are produced and tested.

---

## 2. EXPLICIT OUTSTANDING HARDWARE & VENDOR QUALIFICATIONS

### 2.1 Battery Supplier, Protected-Pack Specification & Certification
- **Limitation:** The exact battery cell supplier and finished protected-pack specification (`LP300830-PCM`, $50\text{ mAh}$, nominal $3.7\text{ V}$, maximum finished dimensions $33.00 \times 8.20 \times 3.30\text{ mm}$) have been verified geometrically in 3D CAD to fit the below-rail cradle with $+0.437\text{ mm}$ radial clearance to the barrel bore. However, physical supplier qualification, protection circuit module (PCM) overcharge/overdischarge threshold tolerances, and cell lot consistency have not been established.
- **Physical Certification Required:** Final battery certification under international safety standards (UN 38.3 transport safety, IEC 62133-2 secondary lithium safety, UL 1642 / UL 2054) requires formal vendor-provided documentation and physical sample testing.
- **Runtime Qualification:** The calculated continuous handwriting runtime of $1.89\text{ hours}$ ($113\text{ minutes}$) is an analytical projection based on nominal capacity ($50\text{ mAh}$ cell with $85\%$ usable capacity to $3.3\text{ V}$ cutoff). Actual runtime under temperature variations, aging, and dynamic load transients must be qualified on physical hardware prototypes.

### 2.2 Wi-Fi High-Power Operation & Firmware Enforcement Requirement
- **Limitation:** Full-power Wi-Fi 802.11b transmission draws peak currents up to $385\text{ mA}$ at $+19.5\text{ dBm}$. A small $50\text{ mAh}$ pouch cell cannot sustainably provide $385\text{ mA}$ bursts without severe voltage sag and premature brownout. Therefore, high-power Wi-Fi operation is architectural intended and thermally budgeted for **USB-connected operation only**, where system current is drawn from USB $V_{\text{BUS}}$ through diode $D_4$, while the battery is safely isolated by P-FET $Q_2$.
- **Firmware Enforcement Requirement:** Firmware enforcement of this operational boundary—disabling high-power Wi-Fi transmission when disconnected from USB power and permitting only low-power Bluetooth LE ($130\text{ mA}$ peak, $1\text{ ms}$ bursts) or local MicroSD logging—is an external software/firmware integration requirement. Firmware has not been implemented or verified within this digital hardware design deliverable.

### 2.3 RF Over-The-Air (OTA) Performance
- **Limitation:** The Molex 146153 wideband flexible PCB antenna is integrated conformally along the inner barrel wall ($R=6.60\text{ mm}$), driven via a $50\ \Omega$ coplanar waveguide with ground (CPW-G) and a U.FL micro-coax cable. While 3D clearances and ground plane boundaries are verified, real-world RF return loss ($S_{11}$), radiation efficiency, and user hand detuning (hand phantom effect) remain untested.
- **Prototype Testing Required:** Verification requires physical RF chamber testing with a vector network analyzer (VNA) and calibrated dummy hand fixture.

### 2.4 Physical Mechanical Assembly, Tooling & Durability
- **Limitation:** The 16 STL components are designed for high-resolution additive manufacturing (SLA/SLS with layer thickness $\le 50\ \mu\text{m}$) or micro-injection molding. While CAD clearances ($0.0000\text{ mm}^3$ interference across all 351 pairs) and kinematics ($4.50\text{ mm}$ refill stroke, $1.50\text{ mm}$ overtravel) are mathematically proven, physical assembly friction, snap-fit retention forces, spring fatigue, and cyclic cam wear (Rotor Cam `10B` and Guide Stator `10C`) remain untested.
- **Prototype Testing Required:** First-article 3D printing in engineering resin (e.g., Formlabs Tough 2000) or SLS Nylon PA12, followed by a minimum 500-cycle life-cycle endurance test of the click mechanism.

### 2.5 PCBA Manufacturing & SMT Solder Reflow
- **Limitation:** Gerber files (RS-274X), Excellon drill files, and IPC-compliant footprint land patterns are validated with 0 DRC/ERC violations. However, physical solder paste volume, tombstoning risks on 0201/0402 passives, and thermal profiles across inner ground planes during convection reflow must be validated by the contract manufacturer during first-article PCBA fabrication.

---

## 3. LOCAL WORKSTATION CAD TOOLING ENVIRONMENT (WDAC)

- **Context:** On the local Windows development workstation, Windows Defender Application Control (WDAC) restricts the loading of unsigned native C++ Python binaries (`OCP.pyd`).
- **Resolution:** Native FreeCAD 0.19 BRep kernel validation was executed on the remote GitHub Actions Ubuntu 22.04 runner ([Run 44128253975](https://github.com/SIDDARTHA577/smart-pen-pcb-design/actions/runs/44128253975)), where all 29 STEP files passed complete geometric validation. Local Windows execution remains restricted by workstation policy.
