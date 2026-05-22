from machine import Pin, SPI
import time
import st7789

print("Starting screen test...")

spi = SPI(
    0,
    baudrate=1000000,
    polarity=0,
    phase=0,
    sck=Pin(18),
    mosi=Pin(19)
)

screen = st7789.ST7789(
    spi,
    240,
    240,
    reset=Pin(20, Pin.OUT),
    dc=Pin(21, Pin.OUT),
    cs=Pin(17, Pin.OUT),
    x_offset=0,
    y_offset=0
)

print("Screen initialized")

while True:
    print("RED")
    screen.fill(st7789.RED)
    time.sleep(2)

    print("GREEN")
    screen.fill(st7789.GREEN)
    time.sleep(2)

    print("BLUE")
    screen.fill(st7789.BLUE)
    time.sleep(2)

    print("WHITE")
    screen.fill(st7789.WHITE)
    time.sleep(2)

    print("BLACK")
    screen.fill(st7789.BLACK)
    time.sleep(2)
