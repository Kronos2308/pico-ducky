# License : GPLv2.0
# copyright (c) 2023
# Author: Kronos2308
# Pico waveshare_rp2040_zero board support

import time
import board
import neopixel
import asyncio

pixel = neopixel.NeoPixel(board.GP16, 1)
pixel.brightness = 0.1

# Private
async def Blink(color):
    pixel.fill(color)
    time.sleep(0.2)
    pixel.fill(0x000000)
    
# Async Pulse
def PulseA(color=0xffffff):
    pico_led_task = asyncio.create_task(Blink(color))
    asyncio.gather(pico_led_task)

# Sync Pulse
def PulseS(color=0xffffff):
    pixel.fill(color)
    time.sleep(0.2)
    pixel.fill(0x000000)

# Set brightness off led
def Candle(light=0.6):
    pixel.brightness = light

# Power the Led
def LON(color=0xffffff):
    pixel.fill(color)
    
def LOFF():
    pixel.fill(0x000000)
