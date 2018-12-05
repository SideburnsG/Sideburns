"""The Pygame section of this example is a snippet from the "Kids Can Code Youtube Channel"
https://www.youtube.com/watch?v=pA7OABYHNDY

The MapGenerator() class was written by Gerald Leese and inspired from the example in the link below
https://gamedevelopment.tutsplus.com/tutorials/generate-random-cave-levels-using-cellular-automata--gamedev-9664

-------THINGS TO DO-------

What the heck is going on in my for loops that i cant have a rectange shaped map because index is out of
range?

Looking for a way to do customize the map to spawn loot and mobs


Im still not entirely sure if my version of this is doing what it does in the article. It's close
but there are some things in the maps that could be improved....

* The caves don't always connect making some areas inaccesible.

* Seems like there are some random little islands in the caves sometimes only 1 cell in size would be
  nice to be able to get rid of these/smooth them out perhaps not drawing the map until all the steps
  are .


"""

import pygame, math, sys, datetime, os
from os import path
from settings import *
from ui import *
from sprites import *
import random

class MapGenerator():

    """Our map Generator is for Generating cave-like maps """
    
    def __init__(self, game, width, height, tile_size):

        self.tile_size = tile_size
        self.game = game
        self.width = width //self.tile_size
        self.height = height // self.tile_size
        
        self.tile_map = [['0' for r in range(self.width)] for c in range(self.height)]

    def generate_noise(self):

        #Setting this to 30 on a 2/3 death/birthLimit works fairly well
        #Setting this between 38-42 on a 3/4 death/birthLimit also works fairly well
        chanceToStartAlive = 40
        
        """The next part of the function iterates through the 2D tileMap array and on each iteration sets a
           random number between 0 and 100 to the randomSeed vriable it also does a quick check to see if the
           randomSeed number is less than chanceToStartAlive if it is then it changes the index of the inner
           array to a '1' """
        for r in range(self.width):
            for c in range(self.height):

                randomSeed = random.randint(1,100)

                if randomSeed < chanceToStartAlive:
                    self.tile_map[r][c] = '1'
                    
        
                    
    def count_alive_neighbours(self, map_array, x, y):
        neighbours = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbour_x = x+i
                neighbour_y = y+j

                 
                #If we're looking at the middle point

                if i == 0 and j == 0:
                    
                    
                    continue
                    
                #In case the index we're looking at is off the edge of the map
                elif neighbour_x < 0 or neighbour_y < 0 or neighbour_x >= len(map_array) or neighbour_y >= len(map_array[0]):
                    neighbours += 1
                    
                #Otherwise, a normal check of the neighbour
                elif map_array[neighbour_x][neighbour_y] == '1':
                    neighbours += 1
                    #This here is where I was having trouble getting the neighbour checks to work before I had
                    # map_array[x][y] which did not work until i changed it to what it is now. 
                    
                
                   
        return neighbours
        
        
    def do_simulation_step(self, oldMap):

        """Conway's game of life rules!
 1 If a living cell has less than two living neighbours, it dies.
 2 If a living cell has two or three living neighbours, it stays alive.
 3 If a living cell has more than three living neighbours, it dies.
 4 If a dead cell has exactly three living neighbours, it becomes alive"""

#we can play with the death/birthLimit to get different outcome 2/3 or 3/4 work pretty good so far
#at 2/3 with 30 chanceToStartAlive 3-5 iterations of the simulation work pretty well. 
                
                    
        deathLimit = 3
        birthLimit = 4

        # Here we have it create a new 2D array to store the new values of the map after a simultion_step
        newMap = [['0' for r in range(self.width)] for c in range(self.height)]
        
        #Here we iterate through the tiles of our oldMap and set nbs to the returned value of our
        #neighbour check method which takes a tile-map and the coordinates of the current cell being
        #checked as an argument
        for r in range(self.width):
            for c in range(self.height):
                
                nbs = self.count_alive_neighbours(self.tile_map, r, c)
        #During our iterations we are checking for which rules apply based on our death/birthLimits 
                if oldMap[r][c] == '1':
                    if nbs < deathLimit:
                        newMap[r][c] = '0'
                    else:
                        newMap[r][c] = '1'
                else:
                    if nbs > birthLimit:
                        newMap[r][c] = '1'
                    else:
                        newMap[r][c] = '0'

        self.tile_map = newMap

        #This last little bit places a wall sprite wherever there is a '1' in the tilemap 
        for r in range(self.width):
            for c in range(self.height):
                

                if self.tile_map[r][c] == '1':
                    
                    Wall(self.game, r, c)

        
        return newMap                    

class Game():

    #The main game class 

    def __init__(self):

        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.fpsClock = pygame.time.Clock()
        self.running = True
        
    def load_map(self):
        '''This will be where our map gets loaded into our game from
           either a new game or saved game will be looking into how to
           do unlimited world's'''
        pass

    def new(self):

        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        self.m = MapGenerator(self,WINDOWHEIGHT,WINDOWWIDTH ,TILESIZE)
        self.m.generate_noise()
           
    def run(self):

        #Run method for the Game

        self.playing = True
        self.new()

        while self.playing:
            self.dt = self.fpsClock.tick(FPS) / 1000
            self.fpsClock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        
    def events(self):
        
        #Variables for storing our mouse coordinates 
        mousex = 0
        mousey = 0
        mouseClicked = False

        # The event loop for the
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #if the event is mouse motion set the variables to its current coords 
            elif event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
               
            #if the event is a mouse button being released set the mouse coords
            #to its current position and set the mouse clicked variable to True 
            elif event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                #this method will run any time the mouse is clicked 
                self.m.do_simulation_step(self.m.tile_map)
            
    def update(self):

        #The update section for the Game

        self.all_sprites.update()

        

    def draw_grid(self):

        #This method will handle the drawing of the grid 

        for x in range(0, WINDOWWIDTH, TILESIZE):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, WINDOWHEIGHT))
            
            
        for y in range(0, WINDOWHEIGHT, TILESIZE):
            pygame.draw.line(self.screen, BLACK, (0, y), (WINDOWWIDTH, y))
        
        
    def draw(self):

        #This is where everything will get drawn to the screen
        
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        
        pygame.display.update()
        
g = Game()
g.run()  

