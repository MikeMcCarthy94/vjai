import pygame.midi
import pygame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

pygame.init()
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post
pygame.midi.init()
i = pygame.midi.Input(3)
pygame.display.set_mode((1, 1))
plt.rcParams["figure.autolayout"] = True

tp = []
going = True
try:
    while going:
        events = event_get()

        if i.poll():
            midi_events = i.read(1)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for hit in midi_events:
                if hit[0][1] != 0:
                    xx = hit[1]
                    yy = hit[0][2]
                    
                else:
                    xx = 0
                    yy = 0
                    
            if xx != 0:
                tp.append( plt.scatter(xx, yy) )
                plt.pause(0.001)          
                
            if len(tp) > 100:
                tp[0].remove()
                tp.pop(0)
            for m_e in midi_evs:
                event_post(m_e)

except KeyboardInterrupt:
    pass
