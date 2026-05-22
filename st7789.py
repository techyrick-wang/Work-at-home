from machine import Pin
import time

BLACK = 0x0000
WHITE = 0xFFFF
RED = 0xF800
GREEN = 0x07E0
BLUE = 0x001F
YELLOW = 0xFFE0
CYAN = 0x07FF
MAGENTA = 0xF81F


class ST7789:
    def __init__(self, spi, width, height, reset, dc, cs, x_offset=0, y_offset=0):
        self.spi = spi
        self.width = width
        self.height = height
        self.reset = reset
        self.dc = dc
        self.cs = cs
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.reset.init(Pin.OUT, value=1)
        self.dc.init(Pin.OUT, value=0)
        self.cs.init(Pin.OUT, value=1)

        self.init_display()

    def write_cmd(self, cmd):
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)

    def write_data(self, data):
        self.cs.value(0)
        self.dc.value(1)
        self.spi.write(data)
        self.cs.value(1)

    def reset_display(self):
        self.reset.value(1)
        time.sleep_ms(50)
        self.reset.value(0)
        time.sleep_ms(50)
        self.reset.value(1)
        time.sleep_ms(150)

    def init_display(self):
        self.reset_display()

        self.write_cmd(0x01)  # Software reset
        time.sleep_ms(150)

        self.write_cmd(0x11)  # Sleep out
        time.sleep_ms(150)

        self.write_cmd(0x36)  # Memory access control
        self.write_data(bytearray([0x00]))

        self.write_cmd(0x3A)  # Color mode
        self.write_data(bytearray([0x55]))  # 16-bit RGB565

        self.write_cmd(0x21)  # Inversion on
        time.sleep_ms(10)

        self.write_cmd(0x13)  # Normal display mode
        time.sleep_ms(10)

        self.write_cmd(0x29)  # Display on
        time.sleep_ms(150)

    def set_window(self, x0, y0, x1, y1):
        x0 += self.x_offset
        x1 += self.x_offset
        y0 += self.y_offset
        y1 += self.y_offset

        self.write_cmd(0x2A)
        self.write_data(bytearray([
            (x0 >> 8) & 0xFF,
            x0 & 0xFF,
            (x1 >> 8) & 0xFF,
            x1 & 0xFF
        ]))

        self.write_cmd(0x2B)
        self.write_data(bytearray([
            (y0 >> 8) & 0xFF,
            y0 & 0xFF,
            (y1 >> 8) & 0xFF,
            y1 & 0xFF
        ]))

        self.write_cmd(0x2C)

    def fill(self, color):
        self.set_window(0, 0, self.width - 1, self.height - 1)

        high = (color >> 8) & 0xFF
        low = color & 0xFF

        row = bytearray(self.width * 2)
        for i in range(self.width):
            row[i * 2] = high
            row[i * 2 + 1] = low

        for _ in range(self.height):
            self.write_data(row)
