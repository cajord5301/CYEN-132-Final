#############################################################################
# Name: CJ Jordan, Makayla Price, Keiser Dallas
# Date: 18 May 2020
# Description: Final Pi Project - "Perfect Pitch"
#############################################################################
import RPi.GPIO as GPIO
from time import sleep
from random import choice
###########################
# set to True to enable debugging output
DEBUG = False

# create list of note names
notes = ["C", "C#", "D", "D#", "E", "F", \
         "F#", "G", "G#", "A", "A#", "B"]

# set the GPIO pin numbers
# the switches (from L to R)
switches = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 6, 5]

# the LEDs (from L to R)
leds = [17, 16, 13, 12]

# piezospeaker
speaker = 4

# map note names to Hz frequencies
notePitches = {"C":261.6, "C#":277.2, \
           "D":293.7, "D#":311.1, \
           "E":329.6, "F":349.2, \
           "F#":370.0, "G":392.0, \
           "G#":415.3, "A":440.0, \
           "A#":466.2, "B":493.9}

# map note names to switch pins
noteSwitches = {}
for i in range(12):
    noteSwitches[notes[i]] = switches[i]
if (DEBUG):
    print noteSwitches

# use the Broadcom pin mode
GPIO.setmode(GPIO.BCM)

# setup the input and output pins
GPIO.setup(switches, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(speaker, GPIO.OUT)
###########################
# this function flashes the LEDs
##def flash():
##    for i in range(len(leds)):
##        GPIO.output(leds[i], 1)  # write voltage to pin at i
##        sleep(0.125)             # wait 1/8 of a second
##        GPIO.output(leds[i], 0)  # stop writing voltage to pin at i
##
##    return
#############################
# plays pitch at given frequency
def play(freq):
    T = 1.0 / freq  # period of sound wave
    halfT = T / 2.0  # half of period
    
    for i in range(375):
        GPIO.output(speaker, 1)  # write voltage to piezospeaker
        sleep(halfT)             # wait for half a wavelength
        GPIO.output(speaker, 0)  # stop writing voltage to piezospeaker
        sleep(halfT)             # wait for half a wavelength
        
    return
#############################
# this functions flashes the LEDs a few times when the player loses
def lose(guessed, correct):
    print "\nUh-oh, you guessed wrong--game over!"
    print "You guessed {}, but the pitch was actually {}.".format(guessed, correct)
##    for i in range(0, 4):
##        flash()
##        sleep(0.125)
###########################
# the main part of the program

print "Welcome to Perfect Pitch!"
print "Try to guess the correct pitch by pressing the matching switch."
print "Press Ctrl+C to exit..."

# we'll discuss this later, but this allows us to detect
# when Ctrl+C is pressed so that we can reset the GPIO pins
try:
    # keep going until the user presses Ctrl+C
    while (True):
        note = choice(notes)
        pitch = notePitches[note]
        switch = noteSwitches[note]

        # in debug mode, print note name, pitch frequency, and pin #
        if (DEBUG):
            print "note = {}".format(note)
            print "pitch = {} Hz".format(pitch)
            print "switch # = {}".format(switch)

        # play note pitch using piezospeaker
        play(pitch)

        # wait for player input (via the switches)
        # initially no pitch has been guessed
        pitchGuessed = False
        # keep waiting for player to guess
        while (not pitchGuessed):
            # initially note that no switch is pressed
            # this will help with switch debouncing
            pressed = False
            # so long as no switch is currently pressed...
            while (not pressed):
                # ...we can check the status of each switch
                for i in range(len(switches)):
                    # if one switch is pressed
                    while (GPIO.input(switches[i]) == True):
                        # note its index
                        val = i
                        # note that a switch has now been pressed
                        # so that we don't detect any more switch presses
                        pressed = True
            guessNote = notes[val]  # store note name of user's guess
            guessPitch = notePitches[notes[val]]  # store Hz frequency of user's guess
            guessSwitch = noteSwitches[notes[val]]  # store pin number of user's guess
            pitchGuessed = True  # pitch has been guessed

            if (DEBUG):
                # display index and pin number of switch pressed
                print "val = {} = {}".format(val, notes[val]) 

            # play the corresponding sound
            play(guessPitch)

            # check to see if this pitch matches the random one
            if (guessPitch != pitch):
                # player is incorrect; invoke the lose function
                lose(guessNote, note)  # pass note guessed and actual note to function so game over message can be printed onscreen
                # reset the GPIO pins
                GPIO.cleanup()
                # exit the game
                exit(0)

# detect Ctrl+C
except KeyboardInterrupt:
    # reset the GPIO pins
    GPIO.cleanup()
