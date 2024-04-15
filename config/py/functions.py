import pygame
from . import game_settings as gs
import math
import random
import os
import openpyxl


def diagonal_distance(x1, x2, y1, y2):
    dx = (x2 - x1)**2
    dy = (y2 - y1)**2
    return math.sqrt(dx + dy)


def sin_or_cos(x, y, sin=True):
    a = math.sqrt(x ** 2 + y ** 2)
    try:
        b = x / a if sin is True else y / a
    except ZeroDivisionError:
        return 1
    return b


def scale_image(image, scale):
    x = image.get_width()
    y = image.get_height()
    return pygame.transform.scale(image, (x*scale, y*scale))


def scale_size_image(image, x_size, y_size):
    return pygame.transform.scale(image, (x_size, y_size))


def draw_text(surface, text, x, y, font=gs.font_hud, color=gs.WHITE):
    image_text = font.render(text, True, color)
    surface.blit(image_text, (x, y))


def draw_image(surface, image, x, y, transparent=False):
    image.set_colorkey('black') if transparent else None
    surface.blit(image, (x, y))


def create_text(surface: pygame.surface, text: str, x: int, y: int, size: int, font: str = 'Chiller',
                random_color: bool = False, color: tuple = (255, 255, 255), standard: bool = True):
    if random_color:
        text_color = (random.randint(15, 255), random.randint(25, 255), random.randint(15, 255))
    else:
        text_color = color
    text_font = pygame.font.SysFont(font, size) if standard else pygame.font.Font(font, size)
    text_image = text_font.render(text, True, text_color)
    return surface.blit(text_image, (x, y))


def rename_file(old_name, new_name, file_typ='xlsx', file_path='./config/settings/'):
    number = 1
    old_file = f'{file_path}{old_name}.{file_typ}'
    if os.path.exists(old_file):
        while os.path.exists(f'{file_path}{new_name}_{number:02d}.{file_typ}'):
            number += 1
        new_file = f'{file_path}{new_name}_{number:02d}.{file_typ}'
        try:
            os.rename(old_file, new_file)
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["Score", "Date", "Weapon"])
            wb.save(f'{file_path}score.xlsx')
        except FileNotFoundError:
            print(f'File "{old_file}" not exist')


def random_number(num_1, num_2):
    a = math.ceil(num_1)
    b = math.ceil(num_2)
    if a > b:
        return random.randint(b, a)
    elif a == b:
        return a
    else:
        return random.randint(a, b)


def draw_number_with_probability(numbers: list, probabilities: list):
    selected_value = random.choices(numbers, probabilities)[0]
    return selected_value
