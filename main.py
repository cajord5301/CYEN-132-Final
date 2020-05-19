#############################################################################
# Name: CJ Jordan (DROPPED), Makayla Price, Keiser Dallas
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

### set the GPIO pin numbers ###
# the switches (from L to R)
#           C   C#  D   D#  E   F   F#  G   G#  A  A#  B
switches = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 6, 5]

# the LEDs (from L to R)
#       WHT BLU WHT BLU
leds = [17, 16, 13, 12]

# piezospeaker - from ENGR 121 class
speaker = 4

# map note names to Hz frequencies
notePitches = {"C":261.6, "C#":277.2, \
           "D":293.7, "D#":311.1, \
           "E":329.6, "F":349.2, \
           "F#":370.0, "G":392.0, \
           "G#":415.3, "A":440.0, \
           "A#":466.2, "B":493.9}

# map note names to switch pins
noteSwitches = {}  # create empty dictionary
for i in range(12):  # do for each note
    noteSwitches[notes[i]] = switches[i]  # add switch pin number as value w/ note name as key
if (DEBUG):
    print noteSwitches

# use the Broadcom pin mode
GPIO.setmode(GPIO.BCM)

# setup the input and output pins
GPIO.setup(switches, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(speaker, GPIO.OUT)

# plays pitch at given frequency
def play(freq, soundTime):
    soundTime *= 1000 # multiplies the soundTime by 1000
    soundTime = int(soundTime) # sets soundTime as an int  
    T = 1.0 / freq  # period of sound wave
    halfT = T / 2.0  # half of period
    
    for i in range(375):  # (assume 1000 = 1 sec) do for 3/8 of a second
        GPIO.output(speaker, 1)  # write voltage to piezospeaker
        sleep(halfT)             # wait for half a wavelength
        GPIO.output(speaker, 0)  # stop writing voltage to piezospeaker
        sleep(halfT)             # wait for half a wavelength
        
    return
    
###########################
# plays notes for intro (different note length)
def playIntro(freq):
    T = 1.0 / freq
    halfT = T / 2.0

    for i in range(125):  # (assume 1000 = 1 sec) do for 1/8 of a second
        GPIO.output(speaker, 1)  # write voltage to piezospeaker
        sleep(halfT)             # wait for half a wavelength
        GPIO.output(speaker, 0)  # stop writing voltage to piezospeaker
        sleep(halfT)             # wait for half a wavelength

    return
    
#############################
# this functions tells the player what note they got wrong at the end
def lose(guessed, correct):
    print "\nUh-oh, you guessed wrong--game over!"
    print "You guessed {}, but the pitch was actually {}.".format(guessed, correct)


###########################
# intro tune
def intro():
    introNotes = [261.6, "rest", 261.6, 293.7, 261.6, "rest", \
              261.6, 293.7, 261.6, 293.7, 261.6, 523.3, 392.0, \
              329.6, 261.6, "rest"]
    
    for i in range(len(introNotes)):
        if (i % 2 ==0):
            GPIO.output(leds, 1)  # turn LEDs on
        else:
            GPIO.output(leds, 0)  # turn LEDs off
        
        if (introNotes[i] != "rest"):
            playIntro(introNotes[i])  # play note
        else:
            sleep(0.125)  # wait 1/8 of a second
            
    return
    
###########################
# prints text in shell explaining how to play;
# pauses b/w different blocks of text to make
# it easier for the user to read instead of
# spitting out one big wall of text
def tutorial():
    # display header text to shell
    print "        HOW TO PLAY        "
    print "###########################"
    sleep(0.875)  # wait 7/8 of a second
    
    # display first sentence text to shell
    print "Perfect Pitch uses a piezospeaker to produce a tone at a given"
    print "pitch randomly chosen by the computer."
    sleep(1.0)  # wait 1 second
    
    # display second sentence text to shell
    print "The object of the game is for the player to correctly guess which"
    print "musical note corresponds to that pitch by pressing the matching"
    print "button on the circuit board."
    sleep(1.0)  # wait 1 second
    
    # display third sentence text to shell
    print "The 12 buttons on the circuit board are arranged to resemble a set"
    print "of piano keys; in case you're not familiar with what the layout of"
    print "a piano looks like, here's an ASCII art visual representation that"
    print "has all of the keys labeled with their corresponding note names:\n"
    sleep(0.90625)  # wait 29/32 of a second
    
    # display piano diagram text to shell
    print "  C# D#    F# G# A#  "
    print "| [] [] |  [] [] [] |"
    print "[_][_][_][_][_][_][_]"
    print " C  D  E  F  G  A  B "
    sleep(1.09375)  # wait 1 3/32 seconds
    
    # display prompt text to shell
    print "\n(Press any of the buttons on the circuit board to close this"
    print "tutorial and start playing the game.)\n"
    
    pressed = False  # no switch initially pressed
    while (not pressed):  # as long as no switch is pressed...
        for i in range(len(switches)):  # ...check status of each switch
            while (GPIO.input(switches[i]) == True):  # if a switch is pressed...
                pressed = True  # ...note switch has been pressed

    for i in range(3, 0, -1):
        print "{}...".format(i)
        sleep(1.0)

    print "START!\n"

    return  # go back to function call location
    
###########################
# the main part of the program

# each item in the sequence represents a switch, indexed at 0 through 3
seq = []
# randomly add the first two items to the sequence
seq.append(notePitches[choice(notes)])
seq.append(notePitches[choice(notes)])

print "Welcome to Perfect Pitch!"
intro()
print "Try to guess the correct pitch by pressing the matching switch.\n"
tutorial()
print "Press Ctrl+C to exit..."

# we'll discuss this later, but this allows us to detect
# when Ctrl+C is pressed so that we can reset the GPIO pins
try:
    # keep going until the user presses Ctrl+C
    while (True):       
        note = choice(notes)
        pitch = notePitches[note]
        switch = noteSwitches[note]
        # randomly add one more item to the sequence
        seq.append(pitch)

        # in debug mode, print note name, pitch frequency, and pin #
        if (DEBUG):
            print "note = {}".format(note)
            print "pitch = {} Hz".format(pitch)
            print "switch # = {}".format(switch)
                  
                
        if (len(seq) < 5):
        # standard play and delay times
        soundTime = 0.9
        delayTime = 0.5

        elif (len(seq) >= 5) and (len(seq) < 7):
        # first decrease of play and delay times
        soundTime = 0.8
        delayTime = 0.4

        elif (len(seq) >= 7)and (len(seq) < 10):
        # second decrease of play and delay times
        soundTime = 0.7
        delayTime = 0.3

        elif (len(seq) >= 10 and (len(seq) < 13):
        # third decrease of play and delay times
        soundTime = 0.6
        delayTime = 0.25

        elif (len(seq) >= 13):
        # fourth decrease of play and delay times
        soundTime = 0.5
        delayTime = 0.15
                    
        # display the sequence using the LEDs
        for s in seq:
            #if sequence is less than 15
            if (len(seq) < 15):
                # play its corresponding sound
                play(s, soundTime)
                sleep(soundTime)
                sleep(delayTime)
                
        # wait for player input (via the switches)
        # initially no pitch has been guessed
        # initialize the count of switches pressed to 0
        switch_count = 0
        # keep waiting for player to guess
        while (switch_count < len(seq)):
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
               

            # play the corresponding sound
            play(guessPitch, 0.375)
            sleep(0.25)
            
            if (DEBUG):
            # display index and pin number of switch pressed
            print "val = {} = {}".format(val, notes[val])

            # check to see if the guess is correct in the sequence
            if (guessPitch != seq[switch_count]):
                # player is incorrect; invoke the lose function
                lose(guessNote, note)  # pass note guessed and actual note to function so game over message can be printed onscreen
                # reset the GPIO pins
                GPIO.cleanup()
                # exit the game
                exit(0)
                
            switch_count += 1
            
# detect Ctrl+C
except KeyboardInterrupt:
    # reset the GPIO pins
    GPIO.cleanup()
