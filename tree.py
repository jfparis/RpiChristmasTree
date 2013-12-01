#!/usr/bin/env python
# 
#   RpiChristmasTree - A virtual Christmas tree on your TV wit RPI
#   Copyright (C) 2013 Jean-Francois Paris
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
from pygame.locals import *
import random
import math

width = 1920 
height = 1080 
BROWN = (  102, 51,   0)
GREEN = (  0, 255,   0)
RED = (  255, 0,   0)
BLUE = (  0, 0,   255)
YELLOW = (255,255,0)
balls_collors = (RED,YELLOW,BLUE)


def draw_tree():
    """ Draw the christmas tree"""

    trunc_width = width/16
    
    surface = pygame.Surface([width, height])
    # draw the trunk
    pygame.draw.polygon(surface, BROWN, 
                        [[(width-trunc_width)/2,height],
                         [(width-trunc_width)/2,height-trunc_width],
                         [(width+trunc_width)/2,height-trunc_width],
                         [(width+trunc_width)/2,height]
                        ],0)
    
    # draw the tree
    tree_height = height - trunc_width*2
    
    leaf_width = width/2
    leaf_height = tree_height/3
    leaf_base_height = height-trunc_width
    leaf = pygame.Surface([leaf_width, leaf_height])
    pygame.draw.polygon(leaf,GREEN,
                        [[0, leaf_height],
                         [leaf_width, leaf_height],
                         [leaf_width/2,0]
                        ], 0)
    
    # place the first leaf
    surface.blit(leaf,((width-leaf_width)/2,leaf_base_height-leaf_height))
    
    # place the other leaves
    for i in range(1,4):
        # calculate the width of the scaled leafs
        scaled_leaf_width = leaf_width * (4-i)/4
        scaled_leaf_height = leaf_height
        # scale and place the second leaf
        scaled_leaf = pygame.transform.scale(leaf, (scaled_leaf_width, scaled_leaf_height))
        surface.blit(scaled_leaf,((width-scaled_leaf_width)/2,leaf_base_height-scaled_leaf_height-i*leaf_height*2/3))
    
    return surface


def list_lights(surface, nb_light = 20):
    """Build a list of the light on the tree"""
    list = []
    min_dist = width/16
    
    done = False
    count = 0 
    random.seed()
    
    # while loop with safety break
    while (not done) and (count < nb_light*10):
        candidate = (random.randint(0,width-1), random.randint(0,height-1))
        if not surface.get_at(candidate) == GREEN:#pygame.Color(GREEN[0],GREEN[1],GREEN[2]):
            continue
        
        good_candidate = True
        
        for each in list:
            # check the (euclidean) distance to the other points
            if math.sqrt((candidate[0]-each[0])**2+(candidate[1]-each[1])**2)<=min_dist:
                good_candidate = False
                break
        
        # only add the point if its not too close from the existing one
        if good_candidate:
            list.append(candidate)
    
        if len(list) == nb_light:
            done = True
            
        count=+1
            
    return list

# start pygame
pygame.init()

#check the highest possible resolution
modes = pygame.display.list_modes()
max_mode = modes[0]
width = max_mode[0]
height = max_mode[1]

# init the screen
size = [width, height]
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

# draw the tree on a reusable surface that we can blit easily
background = draw_tree()

# create the lights
lights = list_lights(background)

loop_count = 0

# main loop
while True:
    for event in pygame.event.get(): # User did something
        if event.type in (QUIT, KEYDOWN): # If user clicked close
            pygame.quit() # Flag that we are done so we exit this loop
    
    # only update very 5 seconds
    if loop_count == 0:
        # put the tree on screen
        screen.blit(background,(0,0))
        
        # draw the lights
        for light in lights:
            pygame.draw.circle(screen, random.choice(balls_collors), light, width/80, 0)
            
        # update display
        pygame.display.flip()

    # we have to use this trick to avoid freezing the main loop and 
    # delay the end of the program
    loop_count = (loop_count +1) % 50
            
    # sleep for 1/10 of a second
    pygame.time.wait(100)