# License : GPLv2.0
# copyright (c) 2023  Dave Bailey
# Author: Dave Bailey (dbisu, @daveisu)
# Pico and Pico W board support

import time
import digitalio
from board import *
import board
import neopixel
import asyncio


pixel = neopixel.NeoPixel(board.GP16, 1)

async def PulseL(color):
    pixel.fill(color)
    time.sleep(0.2)
    pixel.fill(0x000000)

def PulseW(color):
    pixel.fill(color)
    time.sleep(0.2)
    pixel.fill(0x000000)

def Blink(color):
    pico_led_task = asyncio.create_task(PulseL(color))
    asyncio.gather(pico_led_task)



def LON(G,R,B):
    pixel.fill((G, R, B))
    
def FON(color):
    pixel.fill(color)
    
def LOFF():
    pixel.fill((0, 0, 0))
