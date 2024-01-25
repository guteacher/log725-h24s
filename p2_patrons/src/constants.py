import random
from math import ceil
import pygame
import time
from functools import wraps
import numpy as np

CURRENT_W, CURRENT_H = pygame.display.Info().current_w, pygame.display.Info().current_h
JUMP_SOUND = pygame.mixer.Sound('assets/audio/jump.ogg')

def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        _start = time.time()
        result = f(*args, **kwargs)
        print(f'@timing {f.__name__} ELAPSED TIME:', time.time() - _start)
        return result
    return wrapper



