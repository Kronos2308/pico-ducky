# License : GPLv2.0
# copyright (c) 2023  Dave Bailey
# Author: Dave Bailey (dbisu, @daveisu)

from LED import *

import time
import digitalio
from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Debouncer
import board
from board import *
import pwmio
import asyncio
import usb_hid
from adafruit_hid.keyboard import Keyboard
import os

# comment out these lines for non_US keyboards
#from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
#from adafruit_hid.keycode import Keycode

# uncomment these lines for non_US keyboards
# replace LANG with appropriate language
from keyboard_layout_win_es import KeyboardLayout
from keycode_win_es import Keycode

#Global Vars
color = 0xffffff
payload = "payload.txt"
DEFA = "default.txt"
letstat = False
colorar = [0x006600,0x660000,0x006666,0x666600,0x82084b] 
paylist = []

def obget(obj,val):
    total = len(obj)
    str = ""
    if val < total:
        str = obj[val]
    else:
        str = obj[0]
    return str

def File_check(file):
    try:
        if not os.stat(file) == {0}:
            return True
    except OSError as e:
        print("Unable to open file ", file)

    return False

duckyCommands = {
    'WINDOWS': Keycode.WINDOWS,
    'GUI': Keycode.GUI,
    'APP': Keycode.APPLICATION,
    'MENU': Keycode.APPLICATION,
    'SHIFT': Keycode.SHIFT,
    'ALT': Keycode.ALT,
    'CONTROL': Keycode.CONTROL,
    'CTRL': Keycode.CONTROL,
    'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,
    'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,
    'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,
    'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,
    'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,
    'INSERT': Keycode.INSERT, 'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'PAGEUP': Keycode.PAGE_UP,
    'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,
    'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB,
    'BACKSPACE': Keycode.BACKSPACE,
    'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
    'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
    'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
    'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
    'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
    'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
    'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,
    'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,
    'F12': Keycode.F12,

}
def convertLine(line):
    newline = []
    # print(line)
    # loop on each key - the filter removes empty values
    for key in filter(None, line.split(" ")):
        key = key.upper()
        # find the keycode for the command in the list
        command_keycode = duckyCommands.get(key, None)
        if command_keycode is not None:
            # if it exists in the list, use it
            newline.append(command_keycode)
        elif hasattr(Keycode, key):
            # if it's in the Keycode module, use it (allows any valid keycode)
            newline.append(getattr(Keycode, key))
        else:
            # if it's not a known key name, show the error for diagnosis
            print(f"Unknown key: <{key}>")
    # print(newline)
    return newline

def runScriptLine(line):
    global kbd
    for k in line:
        kbd.press(k)
    kbd.release_all()

def sendString(line):
    global layout
    layout.write(line)

def parseLine(line):
    global defaultDelay, letstat
    if(line[0:3] == "REM"):
        # ignore ducky script comments
        pass
    elif(line[0:5] == "DELAY"):
        time.sleep(float(line[6:])/1000)
    elif(line[0:6] == "STRING"):
        sendString(line[7:])
    elif(line[0:5] == "PRINT"):
        print("[SCRIPT]: " + line[6:])
    elif(line[0:6] == "IMPORT"):
        runScript(line[7:])
    elif(line[0:13] == "DEFAULT_DELAY"):
        defaultDelay = int(line[14:]) * 10
    elif(line[0:12] == "DEFAULTDELAY"):
        defaultDelay = int(line[13:]) * 10
    elif(line[0:3] == "LED"):
        if(board.board_id == 'waveshare_rp2040_zero'):
            if len(line[4:]) == 0:
                if not letstat:
                    LON()
                    letstat = True
                else:
                    LOFF()
                    letstat = False
            else:
                LON(int(line[4:],16))
                if line[4:] == "0x000000":
                    letstat = False
                else:
                    letstat = True
        else:
            if(led.value == True):
                led.value = False
            else:
                led.value = True
    else:
        newScriptLine = convertLine(line)
        runScriptLine(newScriptLine)



#init button
button1_pin = DigitalInOut(GP12) # defaults to input
button1_pin.pull = Pull.UP      # turn on internal pull-up resistor
button1 =  Debouncer(button1_pin)

#init payload selection switch
payload0Pin = digitalio.DigitalInOut(GP0)
payload0Pin.switch_to_output(True)
# set input switches
payload1Pin = digitalio.DigitalInOut(GP1)
payload1Pin.switch_to_input(pull=digitalio.Pull.DOWN)
payload2Pin = digitalio.DigitalInOut(GP2)
payload2Pin.switch_to_input(pull=digitalio.Pull.DOWN)
payload3Pin = digitalio.DigitalInOut(GP3)
payload3Pin.switch_to_input(pull=digitalio.Pull.DOWN)
payload4Pin = digitalio.DigitalInOut(GP4)
payload4Pin.switch_to_input(pull=digitalio.Pull.DOWN)
print("pin g1 is : " + str(payload1Pin.value))

def getProgrammingStatus():
    # check GP0 for setup mode
    # see setup mode for instructions
    return not button1_pin.value

defaultDelay = 0

def runScript(file):
    global defaultDelay

    duckyScriptPath = file
    try:
        f = open(duckyScriptPath,"r",encoding='utf-8')
        previousLine = ""
        for line in f:
            line = line.rstrip()
            if(line[0:6] == "REPEAT"):
                for i in range(int(line[7:])):
                    #repeat the last command
                    parseLine(previousLine)
                    time.sleep(float(defaultDelay)/1000)
            else:
                parseLine(line)
                previousLine = line
            time.sleep(float(defaultDelay)/1000)
    except OSError as e:
        print("Unable to open file ", file)

def listpayloads():
    global paylist
    paylist = sorted(os.listdir("Payloads"))

def selectPayload():
    global payload1Pin, payload2Pin, payload3Pin, payload4Pin, payload, color, DEFA, paylist, colorar
    # check switch status
    # pin 0 conected whith 1,2,3,4 
    # will temporaly overwrite the saved payload
    sel = 0
    if(payload1Pin.value == True):
        sel = 0

    elif(payload2Pin.value == True):
        sel = 1

    elif(payload3Pin.value == True):
        sel = 2

    elif(payload4Pin.value == True):
        sel = 3
    
    # load The saved File Config
    elif File_check(DEFA):# Check if exist
        if not os.stat(DEFA)[6] == 0:# check if empty
            f = open(DEFA,"r",encoding='utf-8')
            payload = f.readline().strip()
            f.close()
        if not File_check("Payloads/"+payload):
            SwitchPayload()
        try:
            index = paylist.index(payload)
            color = obget(colorar,index)
            LEDID(0x222222,index)
        except OSError as e:
            print(payload not in list)
        return payload
        # if all pins are high, then no switch is present
        # default to payload1
    payload = obget(paylist,sel)
    color = obget(colorar,sel)

    return payload

def LaunchPayload():
    global color, kbd, layout
    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayout(kbd)

    # Run selected payload
    payload = selectPayload()
    LON(color)
    runScript("Payloads/"+payload)
    print("Done")
    LOFF()


def LightPayload():
    global color
    payload = selectPayload()
    PulseA(color)

def SwitchPayload():
    global color, payload, DEFA, paylist, colorar

    #List payloads
    sel = 0
    print(paylist)
    if payload in paylist:
        total = len(paylist)
        for x in range(total):
            print(paylist[x]+" "+str(x)+" "+payload+" "+str(paylist[x] == payload))
            if paylist[x] == payload:
                if x == (total -1):
                    sel = 0
                else:
                    sel = x+1
                payload = paylist[sel]
                break
    else:
        sel = 0
        payload = paylist[sel]


                
            
    print("----> "+payload)
    color = obget(colorar,sel)


    if File_check("Payloads/"+payload):
        LON(color)
        f = open(DEFA,"w+")
        f.write(payload)
        f.close()
        LOFF()
    LEDID(0x222222,sel)

    return


async def blink_led(led):
    print("Blink")
    if(board.board_id == 'raspberry_pi_pico'):
        blink_pico_led(led)
    elif(board.board_id == 'raspberry_pi_pico_w'):
        blink_pico_w_led(led)

async def blink_pico_led(led):
    print("starting blink_pico_led")
    led_state = False
    while True:
        if led_state:
            #led_pwm_up(led)
            #print("led up")
            for i in range(100):
                # PWM LED up and down
                if i < 50:
                    led.duty_cycle = int(i * 2 * 65535 / 100)  # Up
                await asyncio.sleep(0.01)
            led_state = False
        else:
            #led_pwm_down(led)
            #print("led down")
            for i in range(100):
                # PWM LED up and down
                if i >= 50:
                    led.duty_cycle = 65535 - int((i - 50) * 2 * 65535 / 100)  # Down
                await asyncio.sleep(0.01)
            led_state = True
        await asyncio.sleep(0)

async def blink_pico_w_led(led):
    print("starting blink_pico_w_led")
    led_state = False
    while True:
        if led_state:
            #print("led on")
            led.value = 1
            await asyncio.sleep(0.5)
            led_state = False
        else:
            #print("led off")
            led.value = 0
            await asyncio.sleep(0.5)
            led_state = True
        await asyncio.sleep(0.5)

async def monitor_buttons(button1):
    global inBlinkeyMode, inMenu, enableRandomBeep, enableSirenMode,pixel,color
    print("starting monitor_buttons")
    button1Down = False
    while True:
        button1.update()

        button1Pushed = button1.fell
        button1Released = button1.rose
        button1Held = not button1.value

        if(button1Pushed):
            print("Button 1 pushed")
            button1Down = True

        if(button1Released):
            if(button1Down):
                SwitchPayload()
            button1Down = False

        await asyncio.sleep(0.1)

