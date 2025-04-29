import pygame
import numpy as np
from declare import *

def calculate_projectile_path(start_pos,force,time_step=0.1,total_time=2):
    path_points = []
    start_velocity = force

    for t in np.arange(0, total_time, time_step):
            x = start_pos.x + start_velocity.x * t + 0.5 * gravity.x * t**2
            y = start_pos.y + start_velocity.y * t + 0.5 * gravity.y * t**2
            path_points.append((x, y))
            
    return path_points

def apply_gravity(velocity,dt):
      return velocity + gravity*dt

def calculate_force(initial_pos,current_pos):
      return (initial_pos - current_pos) *force_multiplier

def check_collision_rect(rect1, rect2):
      return rect1.colliderect(rect2)

