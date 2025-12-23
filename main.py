import serial
import struct

def crc16(data: bytes):
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return struct.pack("<H", crc)

# B: Unsigned char (1 byte, 0-255).
# H: Unsigned short (2 bytes, 0-65535).

def read_regs(ser, slave, func, addr, count):
    frame = struct.pack(">B B H H", slave, func, addr, count)
    frame += crc16(frame)
    print(f"Sending frame: {frame.hex()}")  # Debug: show hex of frame
    ser.write(frame)
    rx = ser.read(64)
    print(f"Received: {rx.hex() if rx else 'Nothing'}")  # Debug: show received bytes or nothing
    return rx

ser = serial.Serial(
    port="COM9",
    baudrate=9600,
    bytesize=8,
    parity="N",  
    stopbits=1,
    timeout=1  # Increase to 5 or 10 if needed for slower devices
)

print(f"Serial port open: {ser.is_open}")  # Debug: confirm port is open


def convert_voltage(value):
    return round(value / 10,1)

def convert_current(value):
    return round(value * 0.15,2)

def convert_a_power(value):
    return round(value * 15,1)


func_register = 0x03

regs = {
    "VTR":       (func_register, 4000, lambda x: x),  # No scaling function
    "CTR":       (func_register, 4001, lambda x: x),
    "V_L1":       (func_register, 4002, convert_voltage),
    "V_L2":       (func_register, 4003, convert_voltage),
    "V_L3":       (func_register, 4004, convert_voltage),
    "I_L1":       (func_register, 4026, convert_current),
    "I_L2":       (func_register, 4027, convert_current),
    "I_L3":       (func_register, 4028, convert_current),
    "AP_L1":      (func_register, 4072, convert_a_power),  # Apparent Power
    "AP_L2":      (func_register, 4073, convert_a_power),
    "AP_L3":      (func_register, 4074, convert_a_power),
    

}

results = {}
        

for name, (func, addr, converter) in regs.items():
    print(f"Reading {name} at addr {addr}")  # Debug: show which register
    rx = read_regs(ser, 1, func, addr, 10)
    if len(rx) >= 7:
        val = struct.unpack(">H", rx[3:5])[0]
        results[name] = converter(val)
        print(f"Parsed value: {val}")  # Debug: show parsed value
    else:
        results[name] = None
        print("No valid response")  # Debug: indicate failure

ser.close()

# === TABLE ===
print("\n--- TENSE EM-07 ---")
print(f"{'Parameter':<10} | Value")
print("-" * 22)
for k, v in results.items():
    print(f"{k:<10} | {v}")