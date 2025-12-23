# Tense EM-07 Modbus Reader

This Python script communicates with a Tense EM-07 electrical monitoring device via Modbus RTU protocol over a serial connection. It reads various electrical parameters such as voltages, currents, and apparent powers from the device's registers and displays them in a formatted table.

## Features

- Reads voltage levels for L1, L2, L3 phases
- Reads current levels for L1, L2, L3 phases
- Reads apparent power for L1, L2, L3 phases
- Implements CRC16 checksum for Modbus RTU communication
- Applies appropriate scaling and conversion to raw register values

## Prerequisites

- Python 3.x
- `pyserial` library (already installed in the virtual environment)
- A serial connection to the Tense EM-07 device (e.g., RS-485 adapter)

## Installation

1. Ensure you have Python installed.
2. Activate the virtual environment:
   ```
   env\Scripts\activate
   ```
3. The required packages (`pyserial`) are already installed in the `env` directory.

## Usage

1. Connect your Tense EM-07 device to your computer via a serial port (e.g., COM9 on Windows).
2. Ensure the device is configured for Modbus RTU communication at 9600 baud, 8 data bits, no parity, 1 stop bit.
3. Run the script:
   ```
   python main.py
   ```
4. The script will read the specified registers and output the results in a table format.

## Configuration

- **Serial Port**: Currently set to `COM9`. Modify the `port` parameter in `main.py` if your device is on a different port.
- **Baudrate**: Set to 9600. Change if your device uses a different baudrate.
- **Slave ID**: Set to 1. Adjust the slave address in the `read_regs` call if necessary.
- **Registers**: The script reads from predefined register addresses. Refer to the Tense EM-07 manual for register mappings.

## Output Example

```
--- TENSE EM-07 ---
Parameter | Value
----------------------
VTR       | 230.0
CTR       | 5.0
V_L1      | 230.1
V_L2      | 229.8
V_L3      | 230.3
I_L1      | 2.45
I_L2      | 1.98
I_L3      | 3.12
AP_L1     | 564.5
AP_L2     | 455.4
AP_L3     | 718.8
```

## Notes

- The script uses a timeout of 1 second for serial reads. Increase if needed for slower devices.
- Debug prints are included to show sent/received frames and parsed values.
- Ensure the serial port is not in use by other applications.
- This script implements basic Modbus RTU reading. For more advanced features, consider using the `pymodbus` library (already installed).

## License

MIT