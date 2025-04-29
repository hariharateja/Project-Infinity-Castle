import pygame
import sys 
from player import *
from declare import *
from interface import *
from set import *

class Play:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(8)
        self.effect_channel = pygame.mixer.Channel(1)
        self.effect_channel.set_volume(1.0)
        self.menu_music = "music/demonslayertheme.mp3"
        self.playing_music = "music/playing_ds.mp3" 
        self.game_over_music = "music/game_over_bgm.mp3"  
        self.current_game_state = None
        self.screen = pygame.display.set_mode((screen_width,screen_height))
        pygame.display.set_caption("Demon Slayer infinity")

        self.special_block = None
        self.special_block_timer = random.uniform(30, 40)  
        self.special_block_active = False
        self.special_block_duration = 12
        self.clock = pygame.time.Clock()
        self.dt = 0 
        self.running= True
        self.game_state = "menu" 
        self.character_screen_state = "player1_selecting"
        self.ui = ui()
        self.start_background = pygame.transform.scale(pygame.image.load("images/start.jpg"), (screen_width, screen_height))
        self.menu_background = pygame.transform.scale(pygame.image.load("images/main_menu.jpeg"), (screen_width, screen_height))
        self.playing_background = pygame.transform.scale(pygame.image.load("images/battlefield.jpeg"), (screen_width, screen_height))
        self.next_level_background = pygame.transform.scale(pygame.image.load("images/next_level.png"),(screen_width,screen_height))
        self.background = self.start_background
        self.current_player_a_blocks = player_a_blocks
        self.current_player_b_blocks = player_b_blocks
        self.player1_name = "player_1"
        self.player2_name = "player_2"
        self.active_input = 0 
        self.player_score = [2000,2000]
        self.players = []
        self.current_player_idx = 0

        self.player1_selected_characters = []
        self.player2_selected_characters = []
        self.current_selecting_player = 0  # 0 for player 1, 1 for player 2
        self.character_selection_complete = False

        self.reset_timer = 0 
        self.timer = 0 
        self.level = level

    def spawn_special_block(self):
        x = random.randint(screen_width // 4, 3 * screen_width // 4)
        y = random.randint(300, 500)
        from blocks import SpecialBlock
        self.special_block = SpecialBlock(pygame.Vector2(x, y))
        self.special_block_active = True 
    def update_special_block(self):
        if not self.special_block_active:
            self.special_block_timer -= self.dt
            if self.special_block_timer <= 0:
                self.spawn_special_block()
                self.special_block_timer = random.uniform(30,40)  
        else:
            if self.special_block:
                self.special_block.update(self.dt)
                self.special_block_duration -= self.dt
                
                if self.special_block_duration <= 0:
                    self.special_block = None
                    self.special_block_active = False
                    self.special_block_duration = 12         

    def check_special_block_collision(self, player_x):
        """Check if player hit the special block"""
        if self.special_block_active and self.special_block and not self.special_block.is_destroyed():
            if player_x.check_collision(self.special_block):
                self.player_score[self.current_player_idx] += 200 # bonus
                if self.special_block.damage_effect(25, player_x.character_type):
                    self.special_block_active = False
                    self.special_block = None
                    try:
                        effect = pygame.mixer.Sound("music/special_hit.mp3")
                        self.effect_channel.play(effect)
                    except:
                        pass
                    
                    return True
        return False

    def start_game(self):
        player1 = Set(self.player1_name,player_a_pos, True,self.player1_selected_characters)
        player2 = Set(self.player2_name,player_b_pos, False,self.player2_selected_characters)

        player1.initialize_blocks(self.current_player_b_blocks)
        player2.initialize_blocks(self.current_player_a_blocks)

        self.players = [player1 , player2]
        self.current_player_idx = 0
        if self.level == 0:
            self.background = self.playing_background
        else:
            self.background =self.next_level_background
        self.game_state = "playing"

    def play_background_music(self, music_file):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)      

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return 
            
            elif self.game_state == "menu":
                self.handle_menu_events(event)
            elif self.game_state == "player_input": 
                self.handle_player_input_events(event)
            elif self.game_state == "character_selection":
                self.handle_character_selection_events(event)
            elif self.game_state == "playing":
                self.handle_playing_events(event)
            elif self.game_state == "game_over":
                self.handle_game_over_events(event)

    def handle_menu_events(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                start_button =self.ui.draw_menu(self.screen)
                if start_button.collidepoint(event.pos):
                    self.background = self.menu_background
                    self.game_state = "player_input"
    
    def handle_character_selection_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                is_player1 = self.character_screen_state == "player1_selecting"
                if is_player1:
                    selected_chars = self.player1_selected_characters
                    player_name = self.player1_name
                else:
                    selected_chars = self.player2_selected_characters
                    player_name = self.player2_name
                    
                char_rects = self.ui.draw_character_selection(
                    self.screen, player_name, selected_chars, is_player1
                )
                
                for char_name, rect in char_rects.items():
                    if rect.collidepoint(event.pos):
                        # Toggle selection
                        if char_name in selected_chars:
                            selected_chars.remove(char_name)
                        elif len(selected_chars) < 3:  
                            selected_chars.append(char_name)
                
                # Check confirm button
                confirm_button = pygame.Rect(screen_width // 2 - 100, 700, 200, 50)
                if confirm_button.collidepoint(event.pos):
                    if len(selected_chars) == 3:
                        if self.character_screen_state == "player1_selecting":
                            self.character_screen_state = "player2_selecting"
                        else:
                            # Both players have selected, start the game
                            self.start_game()

    def handle_player_input_events(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                p1_rect , p2_rect , start_button = self.ui.take_input(
                    self.screen , self.player1_name,self.player2_name,self.active_input
                )

                if p1_rect.collidepoint(event.pos):
                    self.active_input = 1
                elif p2_rect.collidepoint(event.pos):
                    self.active_input = 2
                elif start_button.collidepoint(event.pos):
                    self.game_state = "character_selection" 
                    self.character_screen_state = "player1_selecting"
                    self.background = self.menu_background
                    self.player1_selected_characters = []
                    self.player2_selected_characters = []
                    
        elif event.type == pygame.KEYDOWN:
            if self.active_input == 1:
                if event.key == pygame.K_BACKSPACE:
                    self.player1_name = self.player1_name[:-1]
                elif event.key == pygame.K_RETURN:
                    self.active_input = 2
                elif len(self.player1_name) < 15:  
                    self.player1_name += event.unicode
            
            elif self.active_input == 2:
                if event.key == pygame.K_BACKSPACE:
                    self.player2_name = self.player2_name[:-1]
                elif len(self.player2_name) < 15:  
                    self.player2_name += event.unicode

        
    def handle_playing_events(self, event):
        """Handle events during gameplay"""
        current_player = self.players[self.current_player_idx]
        player_x = current_player.player_x
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not player_x.is_thrown:  
                mouse_pos = pygame.Vector2(event.pos)
                player_x.start_drag(mouse_pos)
                self.player_score[self.current_player_idx] -= 100
            if event.button == 1:
                exit_button = self.ui.draw_exit(self.screen)
                if exit_button.collidepoint(event.pos):
                    self.game_state = "menu"
                    self.background = self.menu_background
                    self.current_player_a_blocks = player_a_blocks
                    self.current_player_b_blocks = player_b_blocks
        
        elif event.type == pygame.MOUSEMOTION:
            if player_x.is_dragging:
                mouse_pos = pygame.Vector2(event.pos)
                player_x.update_drag(mouse_pos)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and player_x.is_dragging:
                mouse_pos = pygame.Vector2(event.pos)
                player_x.end_drag(mouse_pos)

    def handle_game_over_events(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button ==1 :
                winner_name = self.players[self.current_player_idx].name
                play_again_button,next_level_button = self.ui.draw_game_over(self.screen, winner_name,self.players)
                if play_again_button.collidepoint(event.pos):
                    self.game_state = "player_input"
                    self.player_score = [2000,2000]
                if next_level_button.collidepoint(event.pos):
                    self.current_player_a_blocks = player_a_blocks2
                    self.current_player_b_blocks = player_b_blocks2
                    self.game_state = "player_input"
                    self.level = 1
                    self.background = self.next_level_background
                    self.player_score = [2000,2000]

    def update(self):
        if self.game_state != "playing":
            return
        current_player = self.players[self.current_player_idx]
        opponent = self.players[1-self.current_player_idx]
        player_x = current_player.player_x

        self.update_special_block()

        for player in self.players:
            for block in player.blocks:
                block.update_effects(self.dt)

        for i, player in enumerate(self.players):
            if player.is_castle_destroyed():
                self.current_player_idx = 1 - i  
                self.game_state = "game_over"
                return       
        if self.reset_timer > 0:
            self.reset_timer-= self.dt
            if self.reset_timer <= 0:
                player_x.reset()
                current_player.change_character()
                self.current_player_idx = 1- self.current_player_idx
        
        elif player_x.is_thrown:
            should_resset = player_x.update(self.dt , screen_width , screen_height)
            special_hit = self.check_special_block_collision(player_x)
            collision_occured = opponent.check_projectile_collision(player_x)

            if opponent.is_castle_destroyed():
                self.player_score[self.current_player_idx] += 500
                self.game_state = "game_over"
                return
            if collision_occured or should_resset or special_hit:
                self.reset_timer = reset_delay
    def draw(self):
        self.screen.blit(self.background,(0,0))

        if self.game_state == "menu":
            self.ui.draw_menu(self.screen)
        elif self.game_state == "player_input":
            self.ui.take_input(self.screen , self.player1_name,self.player2_name,self.active_input)
        elif self.game_state == "character_selection":
            if self.character_screen_state == "player1_selecting":
                self.ui.draw_character_selection(self.screen, self.player1_name, self.player1_selected_characters,True)
            else:
                self.ui.draw_character_selection(self.screen, self.player2_name, self.player2_selected_characters,False)
        elif self.game_state == "playing":
                for player in self.players:
                    player.draw_slingshot(self.screen)
                    player.draw_blocks(self.screen)
                if self.special_block_active and self.special_block:
                    self.special_block.draw_block(self.screen)

                current_player = self.players[self.current_player_idx]
                current_player.player_x.draw(self.screen)

                if current_player.player_x.is_dragging and not current_player.player_x.is_thrown:
                    current_player.player_x.draw_trajectory(self.screen)

                self.ui.draw_player_info(self.screen , self.players[0],self.players[1],self.current_player_idx)
                exit_button = self.ui.draw_exit(self.screen)
        elif self.game_state == "game_over":
            for player in self.players:
                player.draw_slingshot(self.screen)
                player.draw_blocks(self.screen)
            
            winner_name = self.players[self.current_player_idx].name
            self.ui.draw_game_over(self.screen, winner_name,self.player_score)
        
        pygame.display.flip()

    def run(self):
        if self.game_state == "menu":
            self.play_background_music(self.menu_music)
        while self.running:
            if self.current_game_state != self.game_state:
                if self.game_state == "menu":
                    self.play_background_music(self.menu_music)
                elif self.game_state == "playing":
                    self.play_background_music(self.playing_music)
                    pygame.mixer.music.set_volume(0.2)
                    self.effect_channel.set_volume(1.0)
                elif self.game_state == "game_over":
                    self.play_background_music(self.game_over_music)
                self.current_game_state = self.game_state
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.timer/ 1000
            self.timer = self.clock.tick(60)
        pygame.quit()
        sys.exit()   
        
