from machine import Pin
import machine
import time
import math

# Configure the button pin
button = Pin(3, Pin.IN, Pin.PULL_UP)  # Replace with your GPIO pin

# Morse code dictionary
MORSE_CODE_DICT = {
    
    '...': 'S', '---': 'O',
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '.---.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S',
    '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9'
}


# Timing constants (in seconds)
DOT_TIME = 0.2  # Duration for a dot
DASH_TIME = 0.3  # Minimum duration for a dash
LETTER_GAP = 0.5  # Gap between letters
WORD_GAP = 1.0  # Gap between words



class LCD():
    def __init__(self, addr=0x27, blen=1):
        sda = machine.Pin(0)
        scl = machine.Pin(1)
        self.bus = machine.I2C(0, sda=sda, scl=scl, freq=400000)
        self.addr = addr
        self.blen = blen
        self.send_command(0x33)  # Initialize to 8-bit mode first
        time.sleep(0.005)
        self.send_command(0x32)  # Then switch to 4-bit mode
        time.sleep(0.005)
        self.send_command(0x28)  # 2 lines, 5x7 matrix
        time.sleep(0.005)
        self.send_command(0x0C)  # Display ON, cursor OFF
        time.sleep(0.005)
        self.clear()

    def write_word(self, data):
        temp = data
        if self.blen == 1:
            temp |= 0x08  # Backlight ON
        else:
            temp &= 0xF7  # Backlight OFF
        self.bus.writeto(self.addr, bytearray([temp]))

    def send_command(self, cmd):
        # Send high nibble
        buf = cmd & 0xF0
        buf |= 0x04  # RS = 0, RW = 0, EN = 1
        self.write_word(buf)
        time.sleep(0.002)
        buf &= 0xFB  # EN = 0
        self.write_word(buf)

        # Send low nibble
        buf = (cmd & 0x0F) << 4
        buf |= 0x04  # RS = 0, RW = 0, EN = 1
        self.write_word(buf)
        time.sleep(0.002)
        buf &= 0xFB  # EN = 0
        self.write_word(buf)

    def send_data(self, data):
        # Send high nibble
        buf = data & 0xF0
        buf |= 0x05  # RS = 1, RW = 0, EN = 1
        self.write_word(buf)
        time.sleep(0.002)
        buf &= 0xFB  # EN = 0
        self.write_word(buf)

        # Send low nibble
        buf = (data & 0x0F) << 4
        buf |= 0x05  # RS = 1, RW = 0, EN = 1
        self.write_word(buf)
        time.sleep(0.002)
        buf &= 0xFB  # EN = 0
        self.write_word(buf)

    def clear(self):
        self.send_command(0x01)  # Clear display

    def write(self, x, y, text):
        if x < 0:
            x = 0
        if x > 15:
            x = 15
        if y < 0:
            y = 0
        if y > 1:
            y = 1

        # Move cursor
        addr = 0x80 + 0x40 * y + x
        self.send_command(addr)

        # Write text
        for char in text:
            self.send_data(ord(char))

    def message(self, text):
        for char in text:
            if char == '\n':
                self.send_command(0xC0)  # Move to second line
            else:
                self.send_data(ord(char))


class MORSE():
    def read_morse(self):
        """Read button presses and interpret Morse code."""
        morse_sequence = ""
        print("Starting the read loop")

        while True:
            # Wait for button press
            while button.value():
                time.sleep(0.01)

    # Measure press duration
            press_start = time.ticks_ms()
            while not button.value():
                time.sleep(0.01)

            press_duration = (time.ticks_ms() - press_start) / 1000  # Convert to seconds
            print(f"print duration: {press_duration}")

            # Determine dot or dash
            if press_duration < DASH_TIME:
                morse_sequence += '.'
            else:
                morse_sequence += '-'

            # Wait for button release gap
            gap_start = time.ticks_ms()
            while button.value() and (time.ticks_ms() - gap_start) / 1000 < WORD_GAP:
                time.sleep(0.01)

            # Check if it's the end of a letter or word
            gap_duration = (time.ticks_ms() - gap_start) / 1000
            if gap_duration >= WORD_GAP:
                # End of word
                yield morse_sequence.strip()
                yield " "  # Indicate a space between words
                morse_sequence = ""
            elif gap_duration >= LETTER_GAP:
                # End of letter
                yield morse_sequence.strip()
                morse_sequence = ""

    def decode_morse(self):
        """Decode Morse code into ASCII."""
        print("Press the button to send Morse code!")
        current_letter = ""
        for morse in read_morse():
            if morse == " ":
                # End of letter
                print(f"Decoded letter: {current_letter}")
                current_letter = ""
            elif morse in MORSE_CODE_DICT:
                current_letter += MORSE_CODE_DICT[morse]
                print(f"Got a letter")
            else:
                print(f"Unknown sequence: {morse}")



# Initialize components

lcd = LCD()
morsec = MORSE()

while True:
    lcd.clear()
    """Decode Morse code into ASCII."""
    print("Press the button to send Morse code!")
    current_letter = ""
    for morse in morsec.read_morse():
        if morse == " ":
            # End of letter
            lcd.message(f"{current_letter}")
            current_letter = ""
        elif morse in MORSE_CODE_DICT:
            current_letter += MORSE_CODE_DICT[morse]
            print(f"Got a letter")
        else:
            print(f"Unknown sequence: {morse}")

    lcd.message("Morse Code Recd  \n")
    time.sleep(2)
