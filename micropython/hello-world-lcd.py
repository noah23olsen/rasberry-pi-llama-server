import machine
import time

class LCD():
    def __init__(self, addr=0x27):
        print('init')
        sda = machine.Pin(4)
        scl = machine.Pin(5)
        self.bus = machine.I2C(0, sda=sda, scl=scl, freq=400000)
        self.addr = addr
        time.sleep(0.1)  # Allow LCD to stabilize

        self.send_command(0x33)  # Initialize in 8-bit mode
        time.sleep(0.01)
        self.send_command(0x32)  # Switch to 4-bit mode
        time.sleep(0.01)
        self.send_command(0x28)  # 2 Lines, 5x7 font
        time.sleep(0.01)
        self.send_command(0x0C)  # Display ON, Cursor OFF
        time.sleep(0.01)
        self.send_command(0x01)  # Clear display
        time.sleep(0.01)

    def write_word(self, data):
        print('in write word');
        time.sleep(0.001)  # Delay to prevent I2C errors
        self.bus.writeto(self.addr, bytearray([data]))

    def send_command(self, cmd):
        print('in send command');
        self.write_word(cmd & 0xF0 | 0x04)  # RS=0, RW=0, EN=1
        time.sleep(0.002)
        self.write_word(cmd & 0xF0)
        self.write_word((cmd << 4) & 0xF0 | 0x04)  # Lower nibble
        time.sleep(0.002)
        self.write_word((cmd << 4) & 0xF0)

    def send_data(self, data):
        print('in send data');
        self.write_word(data & 0xF0 | 0x05)  # RS=1, RW=0, EN=1
        time.sleep(0.002)
        self.write_word(data & 0xF0)
        self.write_word((data << 4) & 0xF0 | 0x05)  # Lower nibble
        time.sleep(0.002)
        self.write_word((data << 4) & 0xF0)

    def message(self, text):
        for char in text:
            self.send_data(ord(char))

# ✅ Initialize LCD
lcd = LCD()
print('after lcd init');

# ✅ Display message
lcd.message("Hello, World!")
print('after hello world');
