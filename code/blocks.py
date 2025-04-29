import pygame
import random
import math
from declare import *


class Block:
    def __init__(self,block_type,position):
        self.type = block_type
        self.position = position
        self.max_health = block_types[block_type]["max_health"]
        self.health = self.max_health

        image_path = block_types[block_type]["image"]
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image,block_size)

        self.rect = pygame.Rect(position.x,position.y,block_size[0],block_size[1])
        self.particles = []
        
        
        self.burning = False
        self.burn_damage = 0
        self.burn_timer = 0
        self.burn_particles = []
        
        
        self.water_effect = False
        self.water_damage = 0
        self.water_timer = 0
        self.water_particles = []
        
        self.thunder_effect = False
        self.thunder_damage = 0
        self.thunder_timer = 0
        self.thunder_particles = []
        
        self.beast_effect = False
        self.beast_damage = 0
        self.beast_timer = 0
        self.beast_particles = []


    def damage_effect(self,amount,character_type = None,is_player_left = True):
        multiplier = 1.0
        if is_player_left:
            characters_ = characters_a
        else:
            characters_ = characters_b    
        if character_type and character_type in characters_:
            multiplier = characters_[character_type]["damage_multiplier"][self.type]

        actual_damage = amount * multiplier
        
        
        if character_type == "rengoku":
            immediate_damage = actual_damage * 0.4
            self.health = max(0, self.health - immediate_damage)
            self.burning = True
            self.burn_damage += actual_damage * 0.6
            self.burn_timer = 1  
            self.create_burn_particles()
        elif character_type == "tanjiro":
            immediate_damage = actual_damage * 0.5
            self.health = max(0, self.health - immediate_damage)
            self.water_effect = True
            self.water_damage += actual_damage * 0.5
            self.water_timer = 1  
            self.create_water_particles()
        elif character_type == "zenitsu":
            immediate_damage = actual_damage * 0.8  
            self.health = max(0, self.health - immediate_damage)
            self.thunder_effect = True
            self.thunder_damage += actual_damage * 0.2
            self.thunder_timer = 1.0  
            self.create_thunder_particles(10)  
        elif character_type == "inosuke":
            immediate_damage = actual_damage * 0.9 
            self.health = max(0, self.health - immediate_damage)
            self.beast_effect = True
            self.beast_damage += actual_damage * 0.1
            self.beast_timer = 1
            self.create_beast_particles()
        else:
            self.health = max(0, self.health - actual_damage)
            
        if self.health <= 0 and not self.particles:
            self.create_destruction_particles()
        return self.health <= 0
    
    def create_destruction_particles(self):
        colors = {
            "stone": [(150, 150, 150), (120, 120, 120), (100, 100, 100)],
            "wood": [(139, 69, 19), (160, 82, 45), (205, 133, 63)],
            "ice": [(200, 235, 255), (180, 215, 255), (160, 195, 255)]
        }
        
        block_colors = colors.get(self.type, [(255, 255, 255)])
        
        for _ in range(15):  
            particle = {
                'pos': pygame.Vector2(
                    self.position.x + random.randint(0, block_size[0]),
                    self.position.y + random.randint(0, block_size[1])
                ),
                'vel': pygame.Vector2(
                    random.uniform(-50, 50),
                    random.uniform(-100, -20)
                ),
                'radius': random.randint(2, 5),
                'color': random.choice(block_colors),
                'lifetime': random.uniform(0.5, 1.5)  
            }
            self.particles.append(particle)

    def create_burn_particles(self, count=5):
        fire_colors = [(255, 0, 0), (255, 69, 0), (255, 140, 0), (255, 165, 0), (255, 215, 0)]
        
        for _ in range(count):
            particle = {
                'pos': pygame.Vector2(
                    self.position.x + random.randint(0, block_size[0]),
                    self.position.y + random.randint(0, block_size[1])
                ),
                'vel': pygame.Vector2(
                    random.uniform(-10, 10),
                    random.uniform(-60, -30)
                ),
                'radius': random.randint(1, 3),
                'color': random.choice(fire_colors),
                'lifetime': random.uniform(0.2, 0.8)  
            }
            self.burn_particles.append(particle)
    
   
    def create_water_particles(self, count=8):
        
        crimson_colors = [(220, 20, 60), (178, 34, 34), (165, 42, 42), 
                        (139, 0, 0), (128, 0, 0)]  
        
        for _ in range(count):
            particle = {
                'pos': pygame.Vector2(
                    self.position.x + random.randint(0, block_size[0]),
                    self.position.y + random.randint(0, block_size[1])
                ),
                'vel': pygame.Vector2(
                    random.uniform(-15, 15),
                    random.uniform(-40, -10)
                ),
                'radius': random.randint(2, 4),
                'color': random.choice(crimson_colors),
                'lifetime': random.uniform(0.5, 1.2),
                'wave_offset': random.uniform(0, 6.28)  
            }
            self.water_particles.append(particle)
    
    def create_thunder_particles(self, count=10):
        thunder_colors = [(255, 255, 255), (200, 220, 255), (150, 190, 255), (100, 160, 255), (70, 130, 230), (40, 100, 220)]
        
        for _ in range(count):
            particle = {
                'pos': pygame.Vector2(
                    self.position.x + random.randint(0, block_size[0]),
                    self.position.y + random.randint(0, block_size[1])
                ),
                'vel': pygame.Vector2(
                    random.uniform(-30, 30),  
                    random.uniform(-80, -40)
                ),
                'radius': random.randint(1, 3),
                'color': random.choice(thunder_colors),
                'lifetime': random.uniform(0.1, 0.4), 
                'branch': random.random() < 0.3  
            }
            self.thunder_particles.append(particle)
    
    
    def create_beast_particles(self, count=6):
        
        beast_colors = [(139, 69, 19), (160, 82, 45), (101, 67, 33), (85, 65, 45), (110, 80, 50)]
        
        for _ in range(count):
            particle = {
                'pos': pygame.Vector2(
                    self.position.x + random.randint(0, block_size[0]),
                    self.position.y + random.randint(0, block_size[1])
                ),
                'vel': pygame.Vector2(
                    random.uniform(-25, 25),
                    random.uniform(-50, -10)
                ),
                'radius': random.randint(2, 6),  
                'color': random.choice(beast_colors),
                'lifetime': random.uniform(0.3, 0.6),
                'rotation': random.uniform(0, 360)  
            }
            self.beast_particles.append(particle)
    
    def update_effects(self, dt):
        
        for particle in self.particles[:]:
            particle['pos'] += particle['vel'] * dt
            particle['vel'].y += 150 * dt
            particle['lifetime'] -= dt
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
        
        if self.burning:
            damage_this_frame = min(self.burn_damage, self.burn_damage * (dt / self.burn_timer) if self.burn_timer > 0 else self.burn_damage)
            self.health = max(0, self.health - damage_this_frame)
            self.burn_damage -= damage_this_frame
            self.burn_timer -= dt
            
            for particle in self.burn_particles[:]:
                particle['pos'] += particle['vel'] * dt
                particle['vel'].y -= 10 * dt  
                particle['lifetime'] -= dt
                
                if particle['lifetime'] <= 0:
                    self.burn_particles.remove(particle)
            
            if self.burn_timer > 0 and random.random() < dt * 10:  
                self.create_burn_particles(2)  
                
            if self.burn_timer <= 0 or self.burn_damage <= 0:
                self.burning = False
        
        if self.water_effect:
            damage_this_frame = min(self.water_damage, self.water_damage * (dt / self.water_timer) if self.water_timer > 0 else self.water_damage)
            self.health = max(0, self.health - damage_this_frame)
            self.water_damage -= damage_this_frame
            self.water_timer -= dt
            
            for particle in self.water_particles[:]:
                
                wave_x = math.sin(particle['lifetime'] * 5 + particle['wave_offset']) * 2
                particle['pos'].x += wave_x
                particle['pos'] += particle['vel'] * dt
                particle['vel'].y += 20 * dt  
                particle['lifetime'] -= dt
                
                if 'color' in particle:
                    r, g, b = particle['color']
                    b = min(255, b + 1)
                    g = min(255, g + 1)
                    particle['color'] = (r, g, b)
                
                if particle['lifetime'] <= 0:
                    self.water_particles.remove(particle)
            
            if self.water_timer > 0 and random.random() < dt * 8:
                self.create_water_particles(3)
                
            if self.water_timer <= 0 or self.water_damage <= 0:
                self.water_effect = False
        
        if self.thunder_effect:
            damage_this_frame = min(self.thunder_damage, self.thunder_damage * (dt / (self.thunder_timer * 0.5)) if self.thunder_timer > 0 else self.thunder_damage)
            self.health = max(0, self.health - damage_this_frame)
            self.thunder_damage -= damage_this_frame
            self.thunder_timer -= dt
            
            for particle in self.thunder_particles[:]:
                particle['vel'].x += random.uniform(-30, 30) * dt
                particle['pos'] += particle['vel'] * dt
                particle['lifetime'] -= dt
                
                if 'color' in particle:
                    r, g, b = particle['color']
                    intensity = 255 * (particle['lifetime'] / 0.4)  
                    particle['color'] = (min(255, intensity), min(255, intensity), 255)  
                
                if particle['lifetime'] <= 0:
                    self.thunder_particles.remove(particle)
            
            if self.thunder_timer > 0 and random.random() < dt * 15:
                self.create_thunder_particles(4)
                
            if self.thunder_timer <= 0 or self.thunder_damage <= 0:
                self.thunder_effect = False
        
        
        if self.beast_effect:
            damage_this_frame = min(self.beast_damage, self.beast_damage * (dt / self.beast_timer) if self.beast_timer > 0 else self.beast_damage)
            self.health = max(0, self.health - damage_this_frame)
            self.beast_damage -= damage_this_frame
            self.beast_timer -= dt
            
            for particle in self.beast_particles[:]:
                particle['pos'] += particle['vel'] * dt
                particle['vel'].y += 200 * dt  
                particle['rotation'] += 180 * dt  
                particle['lifetime'] -= dt
                
                if particle['lifetime'] <= 0:
                    self.beast_particles.remove(particle)
            
            if self.beast_timer > 0 and random.random() < dt * 5:
                self.create_beast_particles(2)
                
            if self.beast_timer <= 0 or self.beast_damage <= 0:
                self.beast_effect = False
    
    def is_destroyed(self):
        return self.health <= 0
    
    def draw_block(self,screen):
        if not self.is_destroyed():
            screen.blit(self.image,self.position)
            self.draw_health_bar(screen)
            if self.burning:
                self.draw_burn_particles(screen)
            if self.water_effect:
                self.draw_water_particles(screen)
            if self.thunder_effect:
                self.draw_thunder_particles(screen)
            if self.beast_effect:
                self.draw_beast_particles(screen)
            elif self.particles:
                self.draw_particles(screen)

    def draw_health_bar(self,screen):
        bar_length = block_size[0]
        bar_height = 5

        fill = (self.health/self.max_health)*bar_length

        pygame.draw.rect(screen,(255,0,0),
                         (self.position.x , self.position.y,bar_length,bar_height))
        pygame.draw.rect(screen,(0,255,0),(self.position.x, self.position.y, fill , bar_height))

    def draw_particles(self, screen):
        for particle in self.particles:
            pygame.draw.circle(
                screen, 
                particle['color'],
                (int(particle['pos'].x), int(particle['pos'].y)),
                int(particle['radius'])
            )
    
    def draw_burn_particles(self, screen):
        for particle in self.burn_particles:
            pygame.draw.circle(
                screen,
                particle['color'],
                (int(particle['pos'].x), int(particle['pos'].y)),
                int(particle['radius'])
            )
    def draw_water_particles(self, screen):
        import math
        
        for particle in self.water_particles:
            pygame.draw.circle(
                screen,
                particle['color'],
                (int(particle['pos'].x), int(particle['pos'].y)),
                int(particle['radius'] + math.sin(particle['lifetime'] * 10) * 1.5)
            )
            
            if particle['radius'] > 2:
                lighter_color = tuple(min(255, c + 40) for c in particle['color'])
                pygame.draw.circle(
                    screen,
                    lighter_color,
                    (int(particle['pos'].x), int(particle['pos'].y)),
                    int(particle['radius'] * 0.6)
                )
    
    def draw_thunder_particles(self, screen):
        for particle in self.thunder_particles:
            pygame.draw.circle(
                screen,
                particle['color'],
                (int(particle['pos'].x), int(particle['pos'].y)),
                int(particle['radius'])
            )
            
            if particle.get('branch', False):
                end_x = particle['pos'].x + random.uniform(-20, 20)
                end_y = particle['pos'].y + random.uniform(-20, 20)
                pygame.draw.line(
                    screen,
                    particle['color'],
                    (int(particle['pos'].x), int(particle['pos'].y)),
                    (int(end_x), int(end_y)),
                    1
                )
                
                if random.random() < 0.5:
                    end2_x = end_x + random.uniform(-10, 10)
                    end2_y = end_y + random.uniform(-10, 10)
                    pygame.draw.line(
                        screen,
                        particle['color'],
                        (int(end_x), int(end_y)),
                        (int(end2_x), int(end2_y)),
                        1
                    )
    
    def draw_beast_particles(self, screen):
        for particle in self.beast_particles:
            pygame.draw.circle(
                screen,
                particle['color'],
                (int(particle['pos'].x), int(particle['pos'].y)),
                int(particle['radius'])
            )
            
            if particle['radius'] > 3 and random.random() < 0.5:
                import math
                
                angle = particle['rotation']
                points = []
                for i in range(5):  
                    radius = particle['radius'] * (1.5 if i % 2 == 0 else 0.8)
                    x = particle['pos'].x + math.cos(angle) * radius
                    y = particle['pos'].y + math.sin(angle) * radius
                    points.append((int(x), int(y)))
                    angle += 2 * math.pi / 5
                
                if len(points) >= 3: 
                    pygame.draw.polygon(screen, particle['color'], points)

class SpecialBlock(Block):
    def __init__(self, position):
        # Call the parent constructor with "special" type  from chatgpt
        super().__init__("special", position)
        self.max_health = 25
        self.health = self.max_health
        self.active = True
        self.movement_speed = 2
        self.direction = 1  # 1 for right, -1 for left
        self.movement_range = 600
        self.start_position = position.copy()
        self.hit_effect = None
        self.block_size = (60, 60)
        
        try:
            self.hit_effect = pygame.mixer.Sound("music/special_block_hit.mp3")
        except:
            print("Couldn't load special block sound effect")
        
        try:
            self.image = pygame.image.load("images/special_block.png")
            self.image = pygame.transform.scale(self.image, self.block_size)
        except:
            self.image = pygame.Surface(self.block_size)
            self.image.fill((255, 215, 0))  
    
    def update(self, dt):
        if not self.active:
            return
        if not hasattr(self, 'velocity'):
            angle = random.uniform(0, 2 * math.pi)
            speed = self.movement_speed * random.uniform(1,3)  # Faster
            self.velocity = pygame.Vector2(
                math.cos(angle) * speed * 60,
                math.sin(angle) * speed * 60
            )
            self.rotation = 0  
        self.position += self.velocity * dt
        
        self.rotation = (self.rotation + 180 * dt) % 360  
        try:
            img = pygame.image.load("images/special_block.png")
            self.image = pygame.transform.rotate(img, self.rotation)
            self.image = pygame.transform.scale(self.image, self.block_size)
        except:
            self.image = pygame.Surface(self.block_size)
            self.image.fill((255, 215, 0))
        screen_width = 1400
        screen_height = 800
        if self.position.x <= 0 or self.position.x >= screen_width - self.block_size[0]:
            self.velocity.x *= -1
            self.position.x = max(0, min(self.position.x, screen_width - self.block_size[0]))
        if self.position.y <= 0 or self.position.y >= screen_height - self.block_size[1]:
            self.velocity.y *= -1
            self.position.y = max(0, min(self.position.y, screen_height - self.block_size[1]))
        
        self.update_rect()
    
    def damage_effect(self, damage_amount, character_type):
        if not self.active:
            return False
            
        self.health -= damage_amount
        if self.hit_effect:
            effect_channel = pygame.mixer.find_channel()
            if effect_channel:
                effect_channel.play(self.hit_effect)
        
        if self.active and self.health <= 0:
            self.active = False
            return True
        
        return False
    def is_destroyed(self):
        return not self.active
    def draw_block(self, screen):
        if not self.active:
            return   
        # Draw the block with a pulsing effect
        alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() / 300))
        glow_surface = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (255, 215, 0, alpha), (5, 5, self.rect.width, self.rect.height), 5)
        screen.blit(glow_surface, (self.rect.x - 5, self.rect.y - 5))
        # Draw the main block
        screen.blit(self.image, self.position)                
    
    def update_rect(self):
        self.rect.x = self.position.x
        self.rect.y = self.position.y