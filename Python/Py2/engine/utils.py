import pygame
import math
import random

def clamp(v, a, b):
    return max(a, min(b, v))

def rand(n):
    return random.randint(0, n - 1)

def hex_to_rgb(hex_str):
    hex_str = hex_str.replace("#", "")
    return (
        int(hex_str[0:2], 16),
        int(hex_str[2:4], 16),
        int(hex_str[4:6], 16),
    )