# Smart Pen Rev E Mechanical & Hardware Integration Guide

## 1. System Architecture & Components
- **Outer Shell**: 15.5 mm outer diameter (<= 16.0 mm customer limit), 88 mm length.
- **Internal Cartridge Rail**: Removable 86 mm cartridge holding the 84.0 x 9.2 mm PCB.
- **Battery Retention**: 46 mm cradle located strictly **BELOW** the electronics rail.
- **Tip IMU**: MPU6050-class sensor housed in the front tip carrier, connected via 4-wire keyed JST SH harness.
- **Writing Refill**: Standard ballpoint/rollerball refill traversing central 3.2 mm bore.

## 2. Assembly Sequence
1. **PCB Assembly**: Solder all 60 SMD components using JLCPCB PCBA standard SMT profile.
2. **Battery Installation**:
   - Insert 300mAh LiPo pouch cell into lower cradle below rail.
   - Route red (+) and black (-) leads through strain relief notch and plug into `J_BAT`.
3. **IMU Module Preparation**:
   - Install MPU6050 into front carrier pocket at tip.
   - Plug 4-pin JST SH harness into `J_IMU` on the front edge of the PCB.
4. **Rail Insertion & Twist-Lock**:
   - Align anti-rotation guide ribs of the rail cartridge with barrel internal tracks.
   - Slide rail forward into the barrel.
   - Engage bayonet lugs and twist front cap 30° clockwise until positive mechanical detent clicks.
5. **Rear Click Mechanism**:
   - Insert refill spring over tip refill neck.
   - Push refill into central bore from rear.
   - Install rear ratchet click cap into barrel rear aperture.
