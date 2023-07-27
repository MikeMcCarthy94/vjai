
#https://github.com/letmaik/pyvirtualcam
import pygame.midi
import pygame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pyvirtualcam
import argparse
import pyvirtualcam
from pyvirtualcam import PixelFormat
import cv2



parser = argparse.ArgumentParser()
#parser.add_argument("video_path", help="path to input video file")
parser.add_argument("--fps", action="store_true", help="output fps every second")
parser.add_argument("--device", help="virtual camera device, e.g. /dev/video0 (optional)")
args = parser.parse_args()
video_paths = [r"C:\Users\Mike\Videos\Tapi.mp4", r"C:\Users\Mike\Videos\No Man's Sky\No Man's Sky 2022.03.13 - 20.56.01.02.mp4", r"C:\Users\Mike\Videos\Grand Theft Auto V\Grand Theft Auto V 2022.08.07 - 16.19.00.04.DVR.mp4"]
vi = 0
video = cv2.VideoCapture(video_paths[vi])
if not video.isOpened():
    raise ValueError("error opening video")
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)


pygame.init()
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post
pygame.midi.init()
i = pygame.midi.Input(1)
#i2 = pygame.midi.Input(3)
pygame.display.set_mode((1, 1))

going = True
with pyvirtualcam.Camera(width, height, fps, fmt=PixelFormat.BGR,
                         device=args.device, print_fps=args.fps) as cam:
    print(f'Virtual cam started: {cam.device} ({cam.width}x{cam.height} @ {cam.fps}fps)')
    count = 0
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

                if midi_events[0][0][1] == 36 and midi_events[0][0][2] != 0:
                    if vi < (len(video_paths) - 1):
                        vi += 1
                    else:
                        vi = 0
                    video = cv2.VideoCapture(video_paths[vi])
                        
                if xx != 0:
                    # Restart video on last frame.
                    if count == length:
                        count = 0
                        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    
                    # Read video frame.
                    ret, frame = video.read()
                    if not ret:
                        raise RuntimeError('Error fetching frame')
                    
                    # Send to virtual cam.
                    cam.send(frame)

                    # Wait until it's time for the next frame
                    cam.sleep_until_next_frame()
                    
                    count += 1      
                    
                for m_e in midi_evs:
                    event_post(m_e)
#            if i2.poll():
#                midi_events = i2.read(1)
                # convert them into pygame events.
#                midi_evs = pygame.midi.midis2events(midi_events, i2.device_id)

#                for hit in midi_events:
#                    if hit[0][1] != 0:
#                        xx = hit[1]
#                        yy = hit[0][2]
                        
#                    else:
#                        xx = 0
#                        yy = 0
                        
#                if xx != 0:
                    # Restart video on last frame.
#                    if count == length:
#                        count = 0
#                        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    
                    # Read video frame.
#                    ret, frame = video.read()
#                    if not ret:
#                        raise RuntimeError('Error fetching frame')
                    
                    # Send to virtual cam.
#                    cam.send(frame)

                    # Wait until it's time for the next frame
#                    cam.sleep_until_next_frame()
                    
#                    count += 1

#                for m_e in midi_evs:
#                    event_post(m_e)



    except KeyboardInterrupt:
        pass
