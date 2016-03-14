#!/usr/bin/env python
# coding: Latin-1
 
# Load library functions we want
import socket
import time
import pygame
 
# Settings for the RemoteKeyBorg client
broadcastIP = '192.168.1.105'           # IP address to send to, 255 in one or more positions is a broadcast / wild-card
broadcastPort = 9038                    # What message number to send with (LEDB on an LCD)
interval = 0.1                          # Time between keyboard updates in seconds, smaller responds faster but uses more processor time
regularUpdate = True                    # If True we send a command at a regular interval, if False we only send commands when keys are pressed or released
 
# Setup the connection for sending on
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)       # Create the socket
sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)                        # Enable broadcasting (sending to many IPs based on wild-cards)
sender.bind(('0.0.0.0', 0))                                                         # Set the IP and port number to use locally, IP 0.0.0.0 means all connections and port 0 means assign a number for us (do not care)
 
# Setup pygame and key states
global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRighte
global moveQuit
hadEvent = True
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveQuit = False
pygame.init()
screen = pygame.display.set_mode([300,300])
pygame.display.set_caption("RemoteKeyBorg - Press [ESC] to quit")
 
# Function to handle pygame events
def PygameHandler(events):
    # Variables accessible outside this function
    global hadEvent
    global moveUp
    global moveDown
    global moveLeft
    global moveRight
    global moveQuit
    # Handle each event individually
    for event in events:
        if event.type == pygame.QUIT:
            # User exit
            hadEvent = True
            moveQuit = True
        elif event.type == pygame.KEYDOWN:
            # A key has been pressed, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_UP:
                moveUp = True
            elif event.key == pygame.K_DOWN:
                moveDown = True
            elif event.key == pygame.K_LEFT:
                moveLeft = True
            elif event.key == pygame.K_RIGHT:
                moveRight = True
            elif event.key == pygame.K_ESCAPE:
                moveQuit = True
        elif event.type == pygame.KEYUP:
            # A key has been released, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_UP:
                moveUp = False
            elif event.key == pygame.K_DOWN:
                moveDown = False
            elif event.key == pygame.K_LEFT:
                moveLeft = False
            elif event.key == pygame.K_RIGHT:
                moveRight = False
            elif event.key == pygame.K_ESCAPE:
                moveQuit = False
 
try:
    print('Press [ESC] to quit')
    # Loop indefinitely
    while True:
        # Get the currently pressed keys on the keyboard
        PygameHandler(pygame.event.get())
        if hadEvent or regularUpdate:
            # Keys have changed, generate the command list based on keys
            hadEvent = False
            driveCommands = ['X']                    # Default to do not change
            if moveQuit:
                break
            elif moveLeft:
                driveCommands = 'left'
                
            elif moveRight:
                driveCommands = 'right'
                
            elif moveUp:
                driveCommands = 'forward'
            elif moveDown:
                driveCommands = 'backward'
                
            else:
                # None of our expected keys, stop
                driveCommands = 'OFF'
                
            # Send the drive commands
            
            sender.sendto(driveCommands, (broadcastIP, broadcastPort))
            print driveCommands
        # Wait for the interval period
        time.sleep(interval)
    # Inform the server to stop
    sender.sendto('ALLOFF', (broadcastIP, broadcastPort))
except KeyboardInterrupt:
    # CTRL+C exit, inform the server to stop
    sender.sendto('ALLOFF', (broadcastIP, broadcastPort))
