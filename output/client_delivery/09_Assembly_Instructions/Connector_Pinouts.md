# Smart Pen Rev E Connector Pinout Specification

### J_USB: USB-C 16-Pin Receptacle (Rear Facing)
- **A1, B12, B1, A12**: GND (Ground return)
- **A4, B9, B4, A9**: USB_VBUS (5.0V charging input)
- **A5**: USB_CC1 (5.1k pull-down R5 to GND)
- **B5**: USB_CC2 (5.1k pull-down R6 to GND)
- **A6, B6**: USB_DP_PORT (USB 2.0 Full-Speed D+)
- **A7, B7**: USB_DM_PORT (USB 2.0 Full-Speed D-)

### J_IMU: 4-Pin Front Tip IMU (JST SH 1.0mm Keyed)
- **Pin 1**: 3V3 (Regulated power with local 0.1uF C15)
- **Pin 2**: GND (Ground return)
- **Pin 3**: I2C_SDA (Serial Data with 4.7k pullup R10)
- **Pin 4**: I2C_SCL (Serial Clock with 4.7k pullup R11)

### J_BAT: 2-Pin Battery Header (JST SH 1.0mm Keyed)
- **Pin 1**: VBAT (Protected LiPo +3.7V)
- **Pin 2**: GND (Battery ground)

### J_SD: 6-Pin MicroSD FPC (0.5mm Pitch)
- **Pin 1**: 3V3
- **Pin 2**: GND
- **Pin 3**: SD_SCK (SPI Clock)
- **Pin 4**: SD_MOSI (Master Out Slave In)
- **Pin 5**: SD_MISO (Master In Slave Out)
- **Pin 6**: SD_CS (Chip Select with 10k pullup R18)

### J_TOUCH: 3-Pin Touch Interface (JST SH 1.0mm Keyed)
- **Pin 1**: 3V3
- **Pin 2**: GND
- **Pin 3**: TOUCH_OUT (Digital active-high touch detect)
