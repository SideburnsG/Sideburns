import pygame
from pygame.sprite import Sprite
from settings import *


class Wall(Sprite):

    def __init__(self, game, x, y):

        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game 
        self.x = x
        self.y = y
        
        

        self.image = pygame.Surface((TILESIZE,TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        self.rect.x = x  * TILESIZE	
        self.rect.y = y  * TILESIZE
