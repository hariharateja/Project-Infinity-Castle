import pygame

screen_width = 1400
screen_height = 800
gravity = pygame.Vector2(0,250)

force_multiplier = 10
radius =40
damage_amount = 25
reset_delay = 1.5
block_size = (50,50)
level = 0 
block_types = {
    "stone": {"max_health":75,"image":"images/block1a.jpeg"},
    "wood": {"max_health":50,"image":"images/block2a.jpeg"},
    "ice":{"max_health":25,"image":"images/block3a.jpeg"},
    "special": {"max_health":25,"image":"images/special_block.png"}
}
characters_a = {
    "zenitsu": {
        "image": "images/zenitsu!.png",
        "damage_multiplier": {"wood": 1.0, "ice": 0.8, "stone": 0.8},
         "song" : "music/zenitsu_bgm.mp3"
    },
    "tanjiro": {
        "image": "images/tanjiro!.png",
        "damage_multiplier": {"wood": 0.8, "ice": 1.0, "stone": 0.8},
        "song" :"music/tanjiro_bgm.mp3"
    },
    "inosuke": {
        "image": "images/inosuke.png",
        "damage_multiplier": {"wood": 0.8, "ice": 0.8, "stone": 1.0},
        "song" :"music/inosuke_bgm.mp3"
    },
    "rengoku": {
        "image": "images/rengoku!.png",
        "damage_multiplier": {"wood": 1, "ice": 1, "stone": 1},
        "song" : "music/rengoku_bgm.mp3"
    }
}
characters_b = {
    "zenitsu": {
        "image": "images/zenitsu.png",
        "damage_multiplier": {"wood": 1.0, "ice": 0.8, "stone": 0.8},
        "song" : "music/zenitsu_bgm.mp3"
    },
    "tanjiro": {
        "image": "images/tanjiro.png",
        "damage_multiplier": {"wood": 0.8, "ice": 1.0, "stone": 0.8},
        "song" : "music/tanjiro_bgm.mp3"
    },
    "inosuke": {
        "image": "images/inosuke.png",
        "damage_multiplier": {"wood": 0.8, "ice": 0.8, "stone": 1.0},
        "song" : "music/inosuke_bgm.mp3"
    },
    "rengoku": {
        "image": "images/rengoku.png",
        "damage_multiplier": {"wood": 1, "ice": 1, "stone": 1},
        "song" : "music/rengoku_bgm.mp3"
    }
}
sling_shot_a_pos = (250,600)
sling_shot_b_pos = (1150,600)

player_a_pos =(250,500)
player_b_pos = (1150,500)

player_a_blocks = [ # need to be beaten
    {"type": "ice", "position": pygame.Vector2(1340, 730)},
    {"type": "stone", "position": pygame.Vector2(1270, 730)},
    {"type": "wood", "position": pygame.Vector2(1200, 730)},
    
    #2nd
    {"type": "stone", "position": pygame.Vector2(1340, 670)},
    {"type": "wood", "position": pygame.Vector2(1270, 670)},
    
    #3rd
    {"type": "ice", "position": pygame.Vector2(1340, 610)},
]

player_b_blocks = [ # need to be beaten
    {"type": "ice", "position": pygame.Vector2(20, 730)},
    {"type": "stone", "position": pygame.Vector2(90, 730)},
    {"type": "wood", "position": pygame.Vector2(160, 730)},
    #2nd
    {"type": "stone", "position": pygame.Vector2(20, 670)},
    {"type": "wood", "position": pygame.Vector2(90, 670)},
    #3rd
    {"type": "ice", "position": pygame.Vector2(20, 610)},
]

background = "battlefield.jpeg"
main_menu = "main_menu.jpeg"
slinshot = "sling_shot.png"
next_level = "next_levl.png"

player_a_blocks2 = [
    {"type": "stone", "position": pygame.Vector2(1340, 430)},
    {"type": "wood", "position": pygame.Vector2(1270, 430)},
    {"type": "stone", "position": pygame.Vector2(1200,430)},
    {"type": "wood", "position": pygame.Vector2(1130, 430)},
    #2
    {"type": "stone", "position": pygame.Vector2(1310, 370)},
    {"type": "wood", "position": pygame.Vector2(1240, 370)},
    {"type": "ice", "position": pygame.Vector2(1170, 370)},
    #3
    {"type": "ice", "position": pygame.Vector2(1280, 310)},
    {"type": "ice", "position": pygame.Vector2(1210, 310)},
    #4
    {"type": "ice", "position": pygame.Vector2(1250, 250)},
    #bottom
    {"type": "stone", "position": pygame.Vector2(1250, 490)},
    {"type": "wood", "position": pygame.Vector2(1250, 550)},
    {"type": "ice", "position": pygame.Vector2(1250, 610)},
    {"type": "stone", "position": pygame.Vector2(1250, 670)},
    {"type": "wood", "position": pygame.Vector2(1250, 730)},
]
player_b_blocks2 = [ # need to be beaten
    {"type": "stone", "position": pygame.Vector2(20, 430)},
    {"type": "wood", "position": pygame.Vector2(90, 430)},
    {"type": "ice", "position": pygame.Vector2(160, 430)},
    {"type": "ice", "position": pygame.Vector2(230, 430)},
    #2nd
    {"type": "stone", "position": pygame.Vector2(50, 370)},
    {"type": "wood", "position": pygame.Vector2(120, 370)},
    {"type": "ice", "position": pygame.Vector2(190, 370)},
    #3rd
    {"type": "ice", "position": pygame.Vector2(80, 310)},
    {"type": "ice", "position": pygame.Vector2(150, 310)},
    #4th
    {"type": "ice", "position": pygame.Vector2(110, 250)},
    {"type": "stone", "position": pygame.Vector2(100, 490)},
    {"type": "wood", "position": pygame.Vector2(100, 550)},
    {"type": "ice", "position": pygame.Vector2(100, 610)},
    {"type": "stone", "position": pygame.Vector2(100, 670)},
    {"type": "wood", "position": pygame.Vector2(100, 730)},
]
