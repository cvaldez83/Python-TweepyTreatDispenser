import pygame
import time

def run():
    print('running playSound.py')
    pygame.init()

    # # VARIABLES # #
    sound_filename = 'CharlieComeHere.ogg'

    # Load sound file
    a = pygame.mixer.Sound(sound_filename)
    t_call_length = a.get_length() #length of sound file
    a.play()
    print('playing sound for: ' + str(t_call_length) + ' seconds')
    time.sleep(t_call_length)