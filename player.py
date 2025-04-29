import pygame
from declare import *
from calculations import *
import random

class Player:
    def __init__(self,character_type,initial_position,is_left_side = True):
        self.character_type = character_type
        self.initial_position = pygame.Vector2(initial_position)
        self.position = self.initial_position.copy()
        self.velocity = pygame.Vector2(0,0)
        self.force = pygame.Vector2(0,0)
        self.is_thrown = False
        self.is_dragging = False
        self.reset_timer = 0
        self.is_left_side = is_left_side 
        self.load_image()
        characters_ = characters_a if self.is_left_side else characters_b
        wind_arr = [-50, -100, -150, 0, -200, 0, 150, 80, 120]
        self.wind = np.random.choice(wind_arr)
        self.wind_particles = []
        self.wind_timer = 0
        self.wind_timer2 = 0
        sound_path = characters_[self.character_type]["song"]
        self.sound_effect = None
        if sound_path and sound_path != "":  
            try:
                self.sound_effect = pygame.mixer.Sound(sound_path)
            except:
                print(f"Couldn't load sound: {sound_path}")
    

    def load_image(self):
        characters_ = characters_a if self.is_left_side else characters_b
        image_path = characters_[self.character_type]["image"]
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image,(radius*2 , radius*2))
        self.width , self.height = self.image.get_size()    

        self.rect = pygame.Rect(self.position.x,self.position.y,self.width,self.height)

    def start_drag(self,mouse_pos):
        self.is_dragging =True
        if self.sound_effect:
                effect_channel = pygame.mixer.find_channel()  
                if effect_channel:
                    effect_channel.play(self.sound_effect)                       

    def update_drag(self,mouse_pos):
        if self.is_dragging and not self.is_thrown:
            self.position = mouse_pos - pygame.Vector2(self.width/2,self.height/2)
            self.update_rect()

    def end_drag(self, mouse_pos):
        if self.is_dragging:
            self.is_dragging = False
            # Calculate center position
            center_pos = self.position + pygame.Vector2(self.width/2, self.height/2)
            initial_center = self.initial_position + pygame.Vector2(self.width/2, self.height/2)
            # Calculate force based on centers
            self.force = calculate_force(initial_center, center_pos)
            self.velocity = self.force.copy()
            self.is_thrown = True
            
    

    def update(self, dt, screen_width, screen_height):
        if not self.is_thrown or self.is_dragging:
            return False
        should_reset =False
        self.velocity = apply_gravity(self.velocity, dt)
        self.wind_timer += dt
        self.wind_timer2 += dt
        if self.wind_timer > 0.2 and self.wind_timer2 < 7:  
            self.velocity.x += self.wind * dt
            self.create_wind_particles()
            self.wind_timer = 0
        self.update_wind_particles(dt)
        next_pos = self.position + self.velocity * dt
        if next_pos.x + self.width >= screen_width:
            next_pos.x = screen_width - self.width
            self.velocity.x *= -0.7  
        elif next_pos.x <= 0:
            next_pos.x = 0 
            self.velocity.x *= -0.7
        
        if next_pos.y + self.height >= screen_height:
            next_pos.y = screen_height - self.height
            self.velocity.y *= -0.7  
        elif next_pos.y <= 0:
            next_pos.y = 0
            self.velocity.y *= -0.7
        
        
        if abs(self.velocity.x) < 3 or abs(self.velocity.y) < 3 and self.position.y >= screen_height - self.height:
            should_reset = True
        
        self.position = next_pos
        self.update_rect()
        return should_reset
    def create_wind_particles(self):
        if abs(self.wind) > 10:  
            for _ in range(3):
                particle = {
                    'pos': pygame.Vector2(
                        random.randint(0, 1200),  
                        random.randint(0, 600)   
                    ),
                    'vel': pygame.Vector2(self.wind * 0.1, random.uniform(-5, 5)),
                    'size': random.randint(1,4),
                    'lifetime': random.uniform(0.5, 1.5)
                }
                self.wind_particles.append(particle)

    def update_wind_particles(self, dt):
        for particle in self.wind_particles[:]:
            particle['pos'] += particle['vel'] * dt
            particle['lifetime'] -= dt
            if particle['lifetime'] <= 0:
                self.wind_particles.remove(particle)             
    
    def reset(self):
        
        self.position = self.initial_position.copy()
        self.velocity = pygame.Vector2(0, 0)
        self.force = pygame.Vector2(0, 0)
        self.is_thrown = False
        self.is_dragging = False
        self.reset_timer = 0
        self.update_rect()

    def draw(self,screen):
        for particle in self.wind_particles:
            wind_color = (200, 200, 255) if self.wind > 0 else (255, 200, 200)
            pygame.draw.circle(
                screen,
                wind_color,
                (int(particle['pos'].x), int(particle['pos'].y)),
                int(particle['size'])
            )
        screen.blit(self.image,self.position)

    def draw_trajectory(self, screen):
    
        if not self.is_thrown and self.is_dragging:
            center_pos = pygame.Vector2(
                self.position.x + self.width/2,
                self.position.y + self.height/2
            )
            force = calculate_force(self.initial_position + pygame.Vector2(self.width/2, self.height/2), center_pos)
            path_points = calculate_projectile_path(center_pos, force)

            thunder_color = (30, 144, 255)  
            import random
            
            for i, point in enumerate(path_points):

                radius = random.randint(2, 5)
                
                pygame.draw.circle(screen, (150, 200, 255), (int(point[0]), int(point[1])), radius + 2)
                pygame.draw.circle(screen, thunder_color, (int(point[0]), int(point[1])), radius)
                
                if random.random() < 0.2:
                    branch_x = int(point[0] + random.randint(-10, 10))
                    branch_y = int(point[1] + random.randint(-10, 10))
                    pygame.draw.line(screen, thunder_color, (int(point[0]), int(point[1])), (branch_x, branch_y), 2)

    def check_collision(self,block):
        return check_collision_rect(self.rect,block.rect)
    
    def update_rect(self):
        self.rect.x = self.position.x
        self.rect.y = self.position.y