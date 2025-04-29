import pygame
from declare import *
import numpy as np
from player import *

class ui:
    def __init__(self):
        self.font = pygame.font.Font("start.otf", 24)
        self.title_font = pygame.font.Font("start.otf", 96)
        self.button_font = pygame.font.Font("start.otf", 36)

    def draw_player_info(self,screen,player1,player2,current_player_idx):
        p1_text = f"{player1.name}: {player1.blocks_remaining()}/{len(player1.blocks)} blocks"
        p2_text = f"{player2.name}: {player2.blocks_remaining()}/{len(player2.blocks)} blocks"

        p1_surface = self.font.render(p1_text, True, (255,128,0))
        p2_surface = self.font.render(p2_text, True, (180,0,255))

        screen.blit(p1_surface, (10, 10))
        screen.blit(p2_surface, (screen_width - p2_surface.get_width() - 10, 10))

        current_player = player1 if current_player_idx == 0 else player2
        turn_text = f"Current turn: {current_player.name} ({current_player.current_character})"
        turn_surface = self.font.render(turn_text, True, (255,215,0))
        screen.blit(turn_surface, (screen_width // 2 - turn_surface.get_width() // 2, 10))
        

    def draw_menu(self,screen):
        #draw title
        title_text = "Infinity Castle"
        title_surface = self.title_font.render(title_text,True,(255,69,0))    
        screen.blit(title_surface, (screen_width// 2 - title_surface.get_width() // 2, 100))
        start_button = pygame.Rect(screen_width // 2 - 100, 500, 200, 50) 
        pygame.draw.rect(screen, (0, 0, 128), start_button)
        pygame.draw.rect(screen,(255,215,0),start_button,4)
        start_text = self.button_font.render("START", True,(255,255,255))
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, 
                                 start_button.centery - start_text.get_height() // 2))
        
        return start_button

    def take_input(self,screen,player1_name,player2_name,active_input):
        intf_text = "Enter player Names:"
        intf_surface = self.font.render(intf_text,True,(255,255,255)) #idk why true is used antialias for smoothness

        p1_label = self.font.render("Player 1:", True, (255,255,255))
        screen.blit(p1_label, (screen_width // 2 - 150, 200))

        p1_rect = pygame.Rect(screen_width // 2 - 50, 200, 200, 30)
        p1_color = (100, 100, 255) if active_input == 1 else (70, 70, 70)
        pygame.draw.rect(screen, p1_color, p1_rect)

        p1_text = self.font.render(player1_name, True, (255,255,255))
        screen.blit(p1_text, (p1_rect.x + 5, p1_rect.centery - p1_text.get_height() // 2))

        p2_label = self.font.render("Player 2:", True, (255,255,255))
        screen.blit(p2_label, (screen_width // 2 - 150, 250))

        p2_rect = pygame.Rect(screen_width // 2 - 50, 250, 200, 30)
        p2_color = (100, 100, 255) if active_input == 2 else (70, 70, 70)
        pygame.draw.rect(screen, p2_color, p2_rect)

        p2_text = self.font.render(player2_name, True, (255,255,255))
        screen.blit(p2_text, (p2_rect.x + 5, p2_rect.centery - p2_text.get_height() // 2))

        start_button = pygame.Rect(screen_width// 2 - 50, 300, 100, 40)
        pygame.draw.rect(screen, (0, 200, 0), start_button)
        start_text = self.font.render("START", True, (255,255,255))
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, 
                                 start_button.centery - start_text.get_height() // 2))
        
        return p1_rect, p2_rect, start_button
    
    def draw_game_over(self, screen, winner_name, player_score):
        """Draw game over screen"""
        game_over = pygame.transform.scale(pygame.image.load("images/game_over.jpeg"), (screen_width, screen_height))
        
        screen.blit(game_over, (0, 0))
        
        game_over_text = "Game Over!"
        game_over_surface = self.title_font.render(game_over_text, True, (255,255,255))
        screen.blit(game_over_surface, (screen_width // 2 - game_over_surface.get_width() // 2, 200))
        
        winner_text = f"{winner_name} wins!"
        winner_surface = self.button_font.render(winner_text, True, (255,255,255))
        screen.blit(winner_surface, (screen_width // 2 - winner_surface.get_width() // 2, 300))

        player1_score = player_score[0]
        player2_score = player_score[1]
        score1_text = f"Player 1 score: {player1_score}"
        score2_text = f"Player 2 score: {player2_score}"
        player1_surface = self.button_font.render(score1_text, True, (255,165,0))    
        player2_surface = self.button_font.render(score2_text, True, (128,0,128))
        screen.blit(player1_surface, (screen_width // 2 - player1_surface.get_width() // 2, 350))
        screen.blit(player2_surface, (screen_width // 2 - player2_surface.get_width() // 2, 400))

        play_again_button = pygame.Rect(screen_width // 2 - 100, 520, 200, 50)
        pygame.draw.rect(screen, (100, 100, 255), play_again_button)
        play_again_text = self.button_font.render("Play Again", True, (255,255,255))
        screen.blit(play_again_text, (play_again_button.centerx - play_again_text.get_width() // 2, 
                                    play_again_button.centery - play_again_text.get_height() // 2))
        
        play_next_level_button = pygame.Rect(screen_width // 2 - 100, 590, 200, 50)
        pygame.draw.rect(screen, (100,100,255), play_next_level_button)
        play_next_level_text = self.button_font.render("Next Level", True, (255,255,255))
        screen.blit(play_next_level_text, (play_next_level_button.centerx - play_next_level_text.get_width() // 2,
                    play_next_level_button.centery - play_next_level_text.get_height() // 2))
        
        return play_again_button, play_next_level_button
    
    def draw_character_selection(self, screen, player_name, selected_characters,is_player1 = True):
        """Draw the character selection screen and return clickable areas"""
        
        # Draw title
        title_text = f"{player_name}, select 3 characters"
        title_surface = self.title_font.render(title_text, True, (255,255,255))
        screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, 100))
        
        if is_player1:
            characters_= characters_a
        else:
            characters_= characters_b
        char_rects = {}
        char_positions = {
            "zenitsu": (screen_width // 4 - 100, 250),
            "tanjiro": (screen_width // 4 * 2 - 100, 250),
            "inosuke": (screen_width // 4 * 3 - 100, 250),
            "rengoku": (screen_width // 2 - 100, 500)
        }
        
        for char_name, position in char_positions.items():
            char_rect = pygame.Rect(position[0]-5, position[1]-5, 160, 160)
            char_rects[char_name] = char_rect
            
            if char_name in selected_characters:
                pygame.draw.rect(screen, (100, 255, 100), char_rect, 4)
            else:
                pygame.draw.rect(screen, (100, 100, 100), char_rect, 2)
            try:
                image_path = characters_[char_name]["image"]
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (150,150))
                screen.blit(image, (position[0] , position[1] ))
            except:
                pygame.draw.rect(screen, (150, 150, 150), 
                                (position[0] + 10, position[1] + 10, 180, 180))
            
            name_surface = self.font.render(char_name.capitalize(), True, (255,255,255))
            screen.blit(name_surface, (position[0] + 70 - name_surface.get_width() // 2, 
                                    position[1] + 170))
        
        count_text = f"Selected: {len(selected_characters)}/3"
        count_surface = self.button_font.render(count_text, True, (255,255,255))
        screen.blit(count_surface, (50,50))
        
        confirm_button = pygame.Rect(screen_width // 2 - 100, 700, 200, 50)
        button_color = (0, 200, 0) if len(selected_characters) == 3 else (100, 100, 100)
        pygame.draw.rect(screen, button_color, confirm_button)
        
        confirm_text = self.button_font.render("Confirm", True, (255,255,255))
        screen.blit(confirm_text, (confirm_button.centerx - confirm_text.get_width() // 2, 
                                    confirm_button.centery - confirm_text.get_height() // 2))
        
        return char_rects
    def draw_exit(self, screen):
        exit_button_image = pygame.image.load("images/exit.png")  
        exit_button_image = pygame.transform.scale(exit_button_image, (150, 150))
        exit_button_rect = exit_button_image.get_rect()
        exit_button_rect.topleft = (screen_width - 150 ,30)
        screen.blit(exit_button_image, exit_button_rect)
        return exit_button_rect
    
    

        
                                   

