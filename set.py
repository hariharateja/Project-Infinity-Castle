import pygame
import random
from player import *
from blocks import *
from declare import *

class Set:
    def __init__(self,name,position,is_left_side = True,selected_characters = None):
        self.name = name 
        self.position =position
        self.is_left_side = is_left_side
        self.blocks = []
        if selected_characters and len(selected_characters) > 0:
            self.available_characters = selected_characters.copy()
        else:
            characters_ = characters_a if is_left_side else characters_b
            self.available_characters = list(characters_.keys())

        self.current_character = random.choice(self.available_characters)
        initial_pos = player_a_pos if is_left_side else player_b_pos
        self.player_x = Player(self.current_character ,initial_pos,self.is_left_side)

        self.slingshot_image = pygame.image.load("images/sling_shot.png")
        self.slingshot_image = pygame.transform.scale(self.slingshot_image, (100, 150))

    def add_block(self, block):
        self.blocks.append(block)

    def initialize_blocks(self,block_data_list):
        self.blocks =[]
        for block_data in block_data_list:
            block = Block(block_data["type"],block_data["position"])
            self.blocks.append(block)

    def change_character(self):
        if len(self.available_characters) <= 1:
            return  
        
        remaining = [c for c in self.available_characters if c != self.current_character]
        self.current_character = random.choice(remaining)
        
        
        initial_pos = player_a_pos if self.is_left_side else player_b_pos
        self.player_x = Player(self.current_character, initial_pos,self.is_left_side)

    def is_castle_destroyed(self):
        return all(block.is_destroyed() for block in self.blocks)
    
    def blocks_remaining(self):
        return sum(1 for block in self.blocks if not block.is_destroyed())
    
    
    def draw_blocks(self, screen):
        for block in self.blocks:
            block.draw_block(screen)
    
    def draw_slingshot(self, screen):
        screen.blit(self.slingshot_image, self.position)

    def check_projectile_collision(self, opponent_projectile):
        
        collision_occurred = False
        for block in self.blocks:
            if not block.is_destroyed() and opponent_projectile.check_collision(block):
                block.damage_effect(25, opponent_projectile.character_type)
                collision_occurred = True

        return collision_occurred