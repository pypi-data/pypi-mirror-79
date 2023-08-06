from pyautogui import *
import mouse
import keyboard
from time import sleep

def launch():
	moveTo(100, 100)
	click(button='left')
	sleep(0.1)

def record(stop):
	record = keyboard.record(until=stop)
	print(record)
	keyboard.play(record, speed_factor=1)
	sleep(0.01)
	record = ''

def waveskip():
	moveTo(220, 65)
	click(button='left')

def launchmenuselect():
	moveTo(950, 550)
	click(button='left')

def launchmenuselectcancel():
	moveTo(750, 550)
	click(button='left')

def launchmenu(selection):
	if selection == 0:
		launchmenuselect()
	elif selection == 1:
		launchmenuselectcancel()

def deselect():
	sleep(0.01)
	moveTo(1000, 1000)
	mouse.double_click(button = 'right')

def moveforward(duration):
	sleep(0.3)
	for i in range(1, duration):
		keyboard.press('w')
		sleep(0.3)
		keyboard.release('w')

def moveback(duration):
	sleep(0.3)
	for i in range(1, duration):
		keyboard.press('s')
		sleep(0.3)
		keyboard.release('s')

def moveright(duration):
	sleep(0.3)
	for i in range(1, duration):
		keyboard.press('d')
		sleep(0.3)
		keyboard.release('d')

def moveleft(duration):
	sleep(0.3)
	for i in range(1, duration):
		keyboard.press('a')
		sleep(0.3)
		keyboard.release('a')

def schematicmenu():
	keyboard.press('t')
	sleep(0.3)
	keyboard.release('t')

def back():
	keyboard.press('esc')
	sleep(0.3)
	keyboard.release('esc')

def schematicimport():
	moveTo(950, 960)
	click(button='left')

def importfile():
	moveTo(830, 520)
	click(button='left')

def importclipboard():
	moveTo(830, 460)
	click(button='left')

def nextcategory(amount):
	sleep(0.3)
	for i in range(1, category):
		keyboard.press('.')
		sleep(0.3)
		keyboard.release('.')

def backcategory(amount):
	sleep(0.3)
	for i in range(1, category):
		keyboard.press(',')
		sleep(0.3)
		keyboard.release(',')

def selectblock(block):
	sleep(0.5)
#	for i in range(1, block):
	keyboard.press('right arrow')
	sleep(0.5)
	keyboard.release('right arrow')

def pause():
	keyboard.press('space')
	sleep(0.3)
	keyboard.release('space')

def highlight(wait):
	keyboard.press('f')
	sleep(wait)
	keyboard.release('f')

def highlightsafe():
	moveTo(800, 970)
	click(button='left')

def mindtext(text):
	textwrite = str(text)
	keyboard.write(textwrite)

def console():
	keyboard.press('f8')
	sleep(0.3)
	keyboard.release('f8')

def displaylaser():
	keyboard.press('f5')
	sleep(0.3)
	keyboard.release('f5')

def displayblockstatus():
	keyboard.press('f6')
	sleep(0.3)
	keyboard.release('f6')

def displayinvisiblegui():
	keyboard.press('c')
	sleep(0.3)
	keyboard.release('c')

def openchat():
	keyboard.press('enter')
	sleep(0.01)
	keyboard.release('enter')

def mindtap(duration):
	dur = duration / 2
	drag(0, 1, dur, button='left')
	drag(0, -1, dur, button='left')

def buildstop():
	keyboard.press('e')
	sleep(0.3)
	keyboard.release('e')