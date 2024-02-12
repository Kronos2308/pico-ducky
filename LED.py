# License : GPLv2.0
# copyright (c) 2023
# Author: Kronos2308
# Pico waveshare_rp2040_zero board support

import time
import board
import neopixel
import asyncio
import struct

pixel = neopixel.NeoPixel(board.GP16, 1)
pixel.brightness = 0.06
# Power the Led
def LON(color=0xffffff):
    # RGB color=0x2f3603
    # RGB to GRB neopixel 
    var = hex(color)
    var = var[2:8]
    tot = len(var)
    print("0x"+var)
    print(tot)
    var = ("0" * (6-tot))+var
    print("0x"+var)
    var = "0x" + var[2:4] + var[0:2] + var[4:6]
    print(var)
    color = int(var,16)
    
    pixel.fill(color)

    
def LOFF():
    pixel.fill(0x000000)

# Private
async def Blink(color):
    LON(color)
    time.sleep(0.2)
    LOFF()
    
# Async Pulse
def PulseA(color=0xffffff):
    pico_led_task = asyncio.create_task(Blink(color))
    asyncio.gather(pico_led_task)

# Sync Pulse
def PulseS(color=0xffffff):
    LON(color)
    time.sleep(0.2)
    LOFF()
    time.sleep(0.2)

# Set brightness off led
def Candle(light=0.6):
    pixel.brightness = light



# Dictionary representing the morse code chart
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}
 
# Function to encrypt the string
# according to the morse code chart
def encrypt(message):
    cipher = ''
    for letter in message.upper():
        if letter != ' ':
 
            # Looks up the dictionary and adds the
            # corresponding morse code
            # along with a space to separate
            # morse codes for different characters
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            # 1 space indicates different characters
            # and 2 indicates different words
            cipher += ' '
 
    return cipher
def numpulse(num):
    num +=1
    code = '.'
    code = code * num
    return ' ' + code + ' '
# repeater
def LEDID(color=0xffffff,val=" "):
    # code = encrypt(str(val))
    code = numpulse(val)
    sort = 0.16
    long = sort * 3
    for letter in code:
        if letter == '.':
            LON(color)
            time.sleep(sort)
            LOFF()
            time.sleep(sort)
        if letter == '-':
            LON(color)
            time.sleep(long)
            LOFF()
            time.sleep(sort)
        if letter == ' ':
            LOFF()
            time.sleep(long)
    print(val)
    print(code)
