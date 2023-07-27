import pygame.midi
import pygame
import numpy as np
import matplotlib.pyplot as plt

pygame.init()
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post
pygame.midi.init()
i = pygame.midi.Input(2)
pygame.display.set_mode((1, 1))

tp = []
going = True
try:
    while going:
        events = event_get()
        for e in events:
            if e.type in [pygame.QUIT]:
                going = False
            if e.type in [pygame.KEYDOWN]:
                going = False
            if e.type in [pygame.midi.MIDIIN]:
                if e.data1 != 0:
                    print(e)


        if i.poll():
            midi_events = i.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post(m_e)
            
except KeyboardInterrupt:
    pass
