import pygame
import os


class SpriteImage:
    # Sprite image in pygame
    def __init__(self, image):
        self.sheet = image
        self.width = self.sheet.get_width()
        self.height = self.sheet.get_height()

    def get_image(self, frame, width, height, scale, colour):
        g_image = pygame.Surface((width, height)).convert_alpha()
        g_image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        g_image = pygame.transform.scale(g_image, (width * scale, height * scale))
        g_image.set_colorkey(colour)  # make image transparent

        return g_image

    def get_image_one_sheet(self, amount, index=1, scale=1, x=0, y=0):
        width = self.width // amount
        height = self.height
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (x, y), ((index * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey('black')  # make image transparent
        # color_key = image.get_at((0, 0))
        # image = pygame.transform.scale(image, (width * scale, height * scale))
        # image.set_colorkey(color_key)
        return image


# Rename image
def rename_images(folder_path, first_index, last_index, typ='png', prefix='', suffix=''):
    for i in range(first_index, last_index + 1):
        old_name = os.path.join(folder_path, f'{prefix}{i}{suffix}.{typ}')
        new_name = os.path.join(folder_path, f'{i + 1}.png')
        os.rename(old_name, new_name)
    print('-------- END --------')
