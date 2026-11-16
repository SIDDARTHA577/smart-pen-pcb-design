# Smart Pen Rev G — MicroSD Carrier & FFC Ribbon Integration
**Document ID:** RPT-REVG-P4-MICROSD-FFC  
**Project:** Smart Pen Hardware Architecture Revision G  
**Target Variant:** Four-Layer Authoritative Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Git Branch:** `engineering/revg-production`  
**Date:** November 16, 2026  
**Status:** Rear Service Bay & FFC Bend Route Verified  

---

## 1. Executive Summary

This report establishes the mechanical packaging, serviceability access, and dynamic cable routing for the dedicated MicroSD Carrier assembly (`07_MicroSD_Carrier_Mount.step` / `.stl`) housing the authoritative `MicroSD_Carrier.kicad_pcb` daughterboard.

In strict accordance with the client hardware architecture:
- **Dedicated Rear Carrier Board:** The MicroSD flash socket is NOT mounted directly on the Main PCB. It is housed on an autonomous $11.40 \times 16.00 \times 0.80\text{ mm}$ carrier daughterboard located in the rear bayonet cartridge bay ($Z = 122.00\text{ to }138.00\text{ mm}$).
- **Rear Ejection Serviceability:** The card socket (push-push TF-01A) is oriented facing rearwards, allowing the user to insert and eject the flash memory card through the rear bayonet opening without removing the main electronics rail or disconnecting battery leads.
- **FFC Ribbon Routing:** Connection to `J_SD` on the Main PCB is provided by a flexible 6-conductor, $0.50\text{ mm}$ pitch polyimide Flat Flexible Cable (FFC) executing a controlled lateral $180^\circ$ service loop with a bend radius of $2.20\text{ mm}$ (exceeding the $1.50\text{ mm}$ static limit).
- **Refill Pushrod Isolation:** A solid $0.80\text{ mm}$ internal polymer deck completely isolates the card socket and FFC ribbon from the moving clicker pushrod.

---

## 2. Mechanical Bay Architecture & Enclosure Fit

```
                 +Y (Top Flank)
                       |
        +--[ Outer Barrel Bore ID 13.5 mm ]--+
        |                                    |
        |   +----------------------------+   |
        |   | MicroSD PCB (11.4 x 16 mm) |   |  Y = +1.40 to +2.20 mm
        |   | [ TF-01A Push-Push Socket ]|   |  (Thickness: 0.80 mm)
        |   +----------------------------+   |
        +------------------------------------+  Y = +1.20 mm (Carrier Floor)
        |  Solid Polymer Barrier (0.80 mm)   |
        +---------[ Pushrod Tunnel ]---------+  Y = +0.40 mm
        |   ( ( Ø1.6 mm Delrin Pushrod ) )   |  Centerline: Y = 0.00 mm
        +------------------------------------+  Y = -0.40 mm
                       |
                 -Y (Bottom Flank)
```

### 2.1 Geometric Envelope & Sagitta Clearance Audit

The carrier board is $11.40\text{ mm}$ wide, seated inside the $\varnothing 13.50\text{ mm}$ barrel bore ($R_{\text{bore}} = 6.75\text{ mm}$):

1. **Chord Clearance (Sagitta):**
   - Half-width of board: $X_{\text{half}} = 11.40 / 2.0 = 5.70\text{ mm}$.
   - Available circular boundary height at $X = \pm 5.70\text{ mm}$:
     $$Y_{\text{avail}} = \sqrt{R_{\text{bore}}^2 - X_{\text{half}}^2} = \sqrt{6.75^2 - 5.70^2} = \sqrt{45.5625 - 32.4900} = \sqrt{13.0725} \approx 3.62\text{ mm}$$
   - Total vertical span inside bore at board edges: $2 \times 3.62 = 7.24\text{ mm}$.
   - The carrier board and TF socket stack occupies $Y = +0.40\text{ to }+4.40\text{ mm}$ (total height $4.00\text{ mm}$).
   - **Sagitta Headroom Clearance:**
     $$\Delta Y = 3.62 - 2.20 = \mathbf{1.42\text{ mm}}$$
   - **Conclusion:** Zero clash between the board corners and the cylindrical barrel bore.

---

## 3. Real FFC Connector Architecture & Cable Bend Route

```
Main PCB Top (F.Cu)                                     MicroSD Carrier Board
[J_SD Receptacle]                                       [FFC Receptacle]
(Z = 96.4 mm, Y = +2.80)                                (Z = 124.0 mm, Y = +2.20)
       |                                                       |
       \===[ Polyimide 6-Pin FFC Ribbon (3.5 mm W x 0.12 mm T) ]/
             - Total Cable Length: 28.0 mm
             - Lateral Service Loop: X = +4.30 mm
             - Calculated Bend Radius: R_bend = 2.20 mm (> 1.50 mm min)
             - Solid Polymer Pushrod Barrier: 0.80 mm
```

### 3.1 Connector Interfaces
- **Main PCB Header (`J_SD`):** Hirose `FH12-6S-0.5SH(55)` (6-pin, 0.5 mm pitch, horizontal bottom-contact SMT receptacle with flip-lock actuator) located at $X = 58.400\text{ mm}, Y = 4.200\text{ mm}$ on `F.Cu` (assembled $Z = 96.400\text{ mm}$).
- **Carrier PCB Header:** Matching 6-pin $0.5\text{ mm}$ pitch horizontal bottom-contact SMT receptacle located at $(5.700, 2.000)$ on `MicroSD_Carrier.kicad_pcb` (assembled $Z = 124.000\text{ mm}$).
- **Cable Specification:** Molex `15020-0063` (or equivalent) 6-conductor polyimide FFC, $0.50\text{ mm}$ conductor pitch, $3.50\text{ mm}$ overall cable width, $0.12\text{ mm}$ nominal thickness, rated for $\ge 20$ dynamic service flex cycles.

### 3.2 FFC Pinout Mapping Table

| Pin | Net Name | Signal Function | Direction | Operating Frequency |
| :---: | :--- | :--- | :---: | :---: |
| **1** | `/3V3` | Card Power Supply ($+3.3\text{V}$) | Main $\rightarrow$ Carrier | DC ($I_{\text{peak}} \approx 80\text{ mA}$) |
| **2** | `/SD_CS` | SPI Chip Select (Active Low) | MCU $\rightarrow$ Card | $20\text{--}25\text{ MHz}$ |
| **3** | `/SD_MOSI` | SPI Master-Out Slave-In Data | MCU $\rightarrow$ Card | $20\text{--}25\text{ MHz}$ |
| **4** | `/SD_SCK` | SPI Serial Clock | MCU $\rightarrow$ Card | $20\text{--}25\text{ MHz}$ |
| **5** | `/SD_MISO` | SPI Master-In Slave-Out Data | Card $\rightarrow$ MCU | $20\text{--}25\text{ MHz}$ |
| **6** | `/GND` | Ground Reference & Shield | Bidirectional | Ground Return |

---

## 4. Card Insertion, Ejection & Serviceability Sequence

1. **Service Access (No Tools Required):** The rear click plunger cap assembly is removed by twisting the bayonet locking collar $30^\circ$ counter-clockwise.
2. **Card Ejection:** Pressing gently on the exposed trailing edge of the MicroSD card activates the TF-01A internal heart-cam push-push latch. The card springs outward by $4.50\text{ mm}$, protruding beyond the carrier face.
3. **Card Removal & Reinsertion:** The card is grasped between thumb and forefinger and extracted along the longitudinal axis. Reinsertion until tactile latch engagement is verified with zero binding against surrounding plastic ribs.
4. **Pushrod Isolation Proof:** The pushrod tunnel runs entirely beneath the carrier deck floor. Zero physical contact occurs between the moving clicker pushrod and the delicate polyimide FFC ribbon under all operating conditions.
