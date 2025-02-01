from machine import Pin, I2C

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
devices = i2c.scan()

if devices:
    print("✅ I2C devices found:", [hex(device) for device in devices])
else:
    print("❌ No I2C devices detected. Check wiring!")