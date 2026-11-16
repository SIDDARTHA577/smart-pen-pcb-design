# Smart Pen Rev G — Phase 3C Client Decision Register
**Document ID:** RPT-REVG-P3C-DECISION-REGISTER  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant:** Four-Layer Evaluation Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Git Branch:** `engineering/revg-production`  
**Base Commit:** `f76aab08831da7bf26516d4a1a39215d754e0d73`  
**Date:** November 16, 2026  
**Status:** Client Architectural Sign-Off Matrix Ready for Review  

---

## 1. Executive Summary & Purpose

This document provides the formal Client Decision Register required before finalizing Phase 4 mechanical enclosure tooling and manufacturing preparations. For each of the six critical architectural items, the engineering team has formulated a technically substantiated recommendation, analyzed cost and geometry implications, established the current pending approval status, and identified exactly what digital work can proceed prior to client sign-off.

In strict adherence to independent engineering governance:
> **No item is labeled as approved without formal client evidence.**  
> **All six items currently remain in PENDING status awaiting client committee review.**

---

## 2. Decision Register Matrix

```
========================================================================================================================
#   DECISION ITEM                   RECOMMENDED OPTION              STATUS       PENDING ACTION
========================================================================================================================
1   PCB Layer Stackup               Four-Layer (or 6-Layer RF Opt)  PENDING      Client CTO approval of ECR-003
2   Battery Model & Charging Spec   EEMB LP401030 w/ PCM + 50mA Chg PENDING      Client sign-off on cell model & R9
3   External RF Antenna & Cable     Molex 146153-0050 (50mm U.FL)   PENDING      Client RF integration approval
4   Enclosure Material / RF Window  Plastic (or Metal w/ Window)    PENDING      Industrial Design material sign-off
5   USB-C Receptacle Side Access    Side Slot (9.5x3.8mm w/ Chamfer)PENDING      Client mechanical approval
6   MicroSD Service Architecture    Rear Bayonet Carrier w/ FFC     PENDING      Client UX/Serviceability sign-off
========================================================================================================================
```

---

## 3. Detailed Decision Briefings

### Item 1: Four-Layer PCB Architecture vs. Legacy Two-Layer Baseline
- **Recommended Candidate:** Formally adopt the **Four-Layer Stackup** (`F.Cu`, `In1.Cu`, `In2.Cu`, `B.Cu`, $1.60\text{ mm}$ thickness) for Revision G production. If total ground plane continuity under the RF front-end is mandated by the client, authorize an optional transition to a **Six-Layer Stackup** (Sig-GND-Sig-Sig-PWR-GND).
- **Cost Implications:** Prototype tooling delta for 4-layer vs 2-layer is minimal ($\approx \$15\text{--}\$25$ per prototype batch at volume fabricators like JLCPCB). In production quantities ($> 1,000\text{ units}$), the unit cost delta is $\approx \$0.30\text{--}\$0.50$.
- **Geometry Implications:** Enables 100% routing closure of all 46 nets within the contractual $84.00 \times 9.20\text{ mm}$ envelope, which was mathematically impossible on two layers without unrouted nets.
- **Approval Status:** **PENDING CLIENT APPROVAL**.
- **What Can Proceed Before Approval:** Phase 4 parametric 3D CAD modeling can proceed using the validated $84.00 \times 9.20 \times 1.60\text{ mm}$ board envelope.

---

### Item 2: Protected Rechargeable Battery Model & Charging Specifications
- **Recommended Candidate:**
  1. **Cell Model:** EEMB `LP401030` Lithium-Polymer pouch cell with built-in Protection Circuit Module (PCM) providing 4.28V overcharge, 2.75V overdischarge, and $\le 2.5\text{A}$ short-circuit cutoff. Nominal capacity: $90\text{--}100\text{ mAh}$.
  2. **Termination:** Pre-crimped 28 AWG wire leads terminating in JST `SHR-02V-S-B` housing (Pin 1: Red / VBAT, Pin 2: Black / GND).
  3. **Circuit Redesign:** Redesign charger programming resistor $R_9$ from $10.0\text{ k}\Omega$ ($100\text{ mA}$) to **$20.0\text{ k}\Omega$ ($50.0\text{ mA}$)** to operate at the manufacturer's recommended $0.5\text{C}$ safe charge rate.
- **Cost Implications:** Standard commercial LiPo pouch cell with integrated PCM is $\approx \$2.50\text{--}\$3.50$ in volume.
- **Geometry Implications:** Maximum dimensions ($4.0\text{ mm T} \times 10.0\text{ mm W} \times 32.0\text{ mm L}$) fit inside the below-rail cradle compartment ($35.0 \times 10.5 \times 4.5\text{ mm}$) with $3.0\text{ mm}$ wire egress clearance and $0.5\text{ mm}$ expansion allowance.
- **Approval Status:** **PENDING CLIENT APPROVAL**.
- **What Can Proceed Before Approval:** Internal removable chassis rail 3D modeling can proceed using the $35.0 \times 10.5 \times 4.5\text{ mm}$ cradle envelope.

---

### Item 3: External 2.4 GHz Antenna & Coaxial Cable Arrangement
- **Recommended Candidate:** Molex `146153-0050` balanced flexible dipole antenna ($34.90 \times 9.00 \times 0.10\text{ mm}$) with $50.0\text{ mm}$ of $\varnothing 1.13\text{ mm}$ micro-coaxial cable and I-PEX MHF1 / U.FL-compatible plug.
- **Cost Implications:** High-reliability COTS antenna assembly is $\approx \$1.20\text{--}\$1.80$ in production volume.
- **Geometry Implications:** Balanced dipole requires no PCB ground plane. Ultra-thin polyimide substrate curves naturally along the $13.5\text{ mm}$ ID cylindrical barrel wall with zero mechanical stress. $50\text{ mm}$ cable length eliminates excess coiled cable.
- **Approval Status:** **PENDING CLIENT APPROVAL**.
- **What Can Proceed Before Approval:** Cable routing relief channels and adhesive mounting pad geometry can be incorporated into the Phase 4 rail CAD model.

---

### Item 4: Pen-Barrel Enclosure Material & RF Windowing
- **Recommended Candidate:**
  - **Preferred (Option A):** High-grade engineering plastic (Polycarbonate, ABS, PEEK, or Delrin) for the complete outer barrel, providing $360^\circ$ RF transparency and zero wireless attenuation.
  - **Conditional (Option B - If Metallic Barrel Required):** If an aluminum alloy or brass barrel is mandated by industrial design, a **molded non-conductive plastic nose grip or a $40.0\text{ mm}$ circumferential RF-transparent dielectric window** is mandatory to prevent Faraday cage attenuation ($>30\text{ dB}$).
- **Cost Implications:** Plastic injection tooling is generally lower cost and lighter weight than precision multi-axis CNC machining of thin-walled aluminum pen barrels.
- **Geometry Implications:** Barrel wall thickness $1.00\text{ mm}$ (OD $15.50\text{ mm}$, ID $13.50\text{ mm}$).
- **Approval Status:** **PENDING CLIENT APPROVAL**.
- **What Can Proceed Before Approval:** Phase 4 parametric CAD models can be constructed with modular, split-body features supporting either an all-plastic shell or a multi-material metal-and-plastic assembly.

---

### Item 5: USB Type-C Receptacle Side-Access Arrangement
- **Recommended Candidate:** Direct lateral side-port aperture in the outer pen barrel:
  - Aperture dimensions: $9.50\text{ mm (L)} \times 3.80\text{ mm (H)}$.
  - Feature: $45^\circ$ lead-in chamfer ($0.75\text{ mm}$ depth) to accommodate standard commercial USB-C plug overmolds ($12.00 \times 6.50\text{ mm}$).
- **Cost Implications:** Standard CNC slotting or side-action core in injection molding tooling ($\approx \$500\text{--}\$1,000$ tooling delta).
- **Geometry Implications:** Receptacle `J_USB` sits $0.80\text{ mm}$ above the PCB midline at $X = 78.400\text{ mm}$. The chamfered slot provides ergonomic cable insertion while maintaining structural barrel rigidity.
- **Approval Status:** **PENDING CLIENT APPROVAL**.
- **What Can Proceed Before Approval:** Barrel cutout and cable overmold clearance envelopes can be fully modeled in Phase 4 3D CAD.

---

### Item 6: MicroSD Daughterboard Location & Serviceability Access
- **Recommended Candidate:** Preserve the separate dedicated carrier board (`MicroSD_Carrier.kicad_pcb`, $15.00 \times 9.20\text{ mm}$) connected via 6-conductor FFC ribbon cable to `J_SD` on the main PCB. Locate the carrier in the rear bayonet cartridge bay.
- **Cost Implications:** 2-board system + FFC cable represents $\approx \$0.80$ BOM delta compared to an onboard socket.
- **Geometry Implications:** Enables the user to remove and service the MicroSD card via the rear bayonet closure without removing the main electronics chassis or disconnecting fragile battery/IMU wiring.
- **Approval Status:** **PENDING CLIENT APPROVAL**.
- **What Can Proceed Before Approval:** Phase 4 CAD can model the rear bayonet card-slot cartridge and FFC service loop retention channel.
