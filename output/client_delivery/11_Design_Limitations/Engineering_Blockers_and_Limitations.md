# Engineering Limitations & Prototype Validation Blockers

## 1. Core Technical Risk: IMU Drift vs. Dead Reckoning
- **Fundamental Physics Constraint**: An inertial measurement unit (MPU-6050) measures linear acceleration ($a$) and angular rate ($\omega$), not absolute position ($x, y, z$).
- **Double Integration Drift**: Calculating displacement via $x(t) = \iint a(t) \, dt^2$ causes sensor bias errors to compound quadratically over time. Even high-precision industrial IMUs drift several centimeters within a few seconds of continuous integration without external absolute reference corrections.
- **Engineering Recommendation**:
  1. Preserve uncompressed raw 6-DOF sensor streams on MicroSD and BLE.
  2. Implement zero-velocity update (ZUPT) and pen-stroke segment boundaries triggered by the external capacitive WRITE touch sensor.
  3. Prepare for a future Revision F hardware revision incorporating an optical displacement sensor (e.g. PMW3360 / PAW3204) at the tip for ground-truth position tracking.

## 2. MicroSD Socket Physical Clearance Barrier
- A standard physical push-pull MicroSD card socket is 14.0 mm wide x 14.5 mm long.
- The Smart Pen outer diameter is strictly constrained to **<= 16.0 mm** (with 1.25 mm wall thickness, leaving an inner diameter of **13.0 mm**).
- A 14.0 mm rigid socket cannot sit horizontally across a 9.2 mm PCB without penetrating the cylindrical shell.
- **Implemented Resolution**: J_SD is implemented as a miniature 0.5mm pitch 6-pin FPC connector feeding an axially mounted rear MicroSD holder cartridge.

## 3. Physical Prototype Bring-Up Gate
Before authorizing production batch manufacturing:
1. 3D-print enclosure prototypes A & B in SLA/SLS resin to verify bayonet twist-lock feel and clicker stroke.
2. Fabricate a 5-unit PCB pilot batch to measure 2.4GHz RF impedance on 1.0mm FR-4 substrate.
3. Validate LiPo battery thermal rise during simultaneous 500mA USB-C charging and ESP32-C3 BLE transmission.
