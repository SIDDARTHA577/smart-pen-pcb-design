# Smart Pen Rev E GPIO & Hardware Pinout Map

| ESP32-C3 Pin | GPIO / Signal | Function | Electrical Topology |
| :---: | :---: | :--- | :--- |
| 1 | LNA_IN | RF 2.4 GHz BLE/Wi-Fi | 50-ohm pi-match (L2, C8, C9) -> U.FL (J_RF) |
| 4 | GPIO0 | I2C_SDA | 4.7k pullup (R10) -> Front IMU & MCP23008 |
| 5 | GPIO1 | I2C_SCL | 4.7k pullup (R11) -> Front IMU & MCP23008 |
| 6 | GPIO2 | STRAP2 | 10k pullup (R3) strapping pin |
| 7 | CHIP_EN | MCU_EN | 10k pullup (R1) + 1uF delay (C1) + RESET (SW1) |
| 8 | GPIO3 | TOUCH_OUT | External capacitive touch WRITE trigger (J_TOUCH) |
| 9 | GPIO4 | SD_MOSI | SPI Master Out Slave In -> MicroSD (J_SD) |
| 10 | GPIO5 | SD_MISO | SPI Master In Slave Out -> MicroSD (J_SD) |
| 12 | GPIO6 | SD_SCK | SPI Serial Clock -> MicroSD (J_SD) |
| 13 | GPIO7 | SD_CS | SPI Chip Select -> MicroSD (J_SD) with 10k PU (R18) |
| 15 | GPIO9 | BOOT9 | 10k pullup (R2) + BOOT switch (SW2) strapping |
| 18 | VDD_SPI | VDD_SPI | Internal Flash LDO out: 1uF bypass (C5) only |
| 25 | GPIO18 | USB_D- | Native USB Serial/JTAG D- via 22R (R7) + USBLC6 |
| 26 | GPIO19 | USB_D+ | Native USB Serial/JTAG D+ via 22R (R8) + USBLC6 |
| 27 | GPIO20 | UART_RX | Hardware UART0 RX test pad (J_UART Pin 2) |
| 28 | GPIO21 | UART_TX | Hardware UART0 TX test pad (J_UART Pin 1) |
| 29 | XTAL_N | XTAL_N | 40MHz Crystal Pin 1 + 15pF load cap (C6) |
| 30 | XTAL_P | XTAL_P | 24nH Inductor (L1) -> Crystal Pin 3 + 15pF (C7) |
| 33 | EP | GND | Center thermal ground pad (stitched to GND plane) |

### MCP23008 I2C GPIO Expander Allocation
- **GP0**: `BTN_ERASE` (Active Low tactile button SW4 with 10k pullup R12)
- **GP1**: `BTN_MODE` (Active Low tactile button SW5 with 10k pullup R13)
- **GP2**: `LED_GREEN_SINK` (Freehand drawing mode indicator D1 cathode via 1k R14)
- **GP3**: `LED_RED_SINK` (Paragraph writing mode indicator D2 cathode via 1k R15)
- **GP4**: `HAPTIC_GATE_DRIVE` (Drives Q1 AO3400A gate via 100R R16 + 100k R17)
- **GP5**: `CHG_STAT` (Monitors MCP73831 battery charge status output)
