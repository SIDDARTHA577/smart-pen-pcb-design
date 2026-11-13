# Smart Pen Rev E Power Tree & Battery Management

## 1. Power Topology Overview
```
[USB-C 5V VBUS] ----> [USBLC6-2SC6 TVS]
       |
       v
[MCP73831T Charger] ----> [3.7V LiPo Battery]
       |                         |
       |                   [SPDT Switch SW3]
       |                         |
       +-------> [VBAT_SW Rail] -+
                     |
                     +---> [AP2112K-3.3 LDO (600mA)] ----> [3.3V System Rail]
                     |                                           |
                     +---> [Haptic Motor J_MOT]                  +---> ESP32-C3 Core
                                                                 +---> Front Tip IMU
                                                                 +---> MicroSD FPC
                                                                 +---> Touch Controller
```

## 2. Power Specifications
- **Battery Cell**: Single-cell 3.7V LiPo pouch (300 mAh nominal, 40 x 10 x 4.2 mm).
- **Charging Current**: 500 mA programmed via R9 = 2.0k ($I_{reg} = 1000V / R_{prog}$).
- **System Voltage Regulator**: AP2112K-3.3TRG1 SOT-23-5:
  * Maximum Output Current: 600 mA continuous (800 mA peak, easily satisfying ESP32-C3 RF transmission bursts).
  * Dropout Voltage: 250 mV @ 600 mA.
  * Quiescent Current: 55 uA.
