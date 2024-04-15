""" Mobs settings """
import random
import pygame
from . import weapon
from . import game_settings as gs
import math
from .items import Item
from . import functions as hf
from .sprite_image import SpriteImage

# region Settings
# Boss drop images setting
pygame.init()
screen = pygame.display.set_mode((1111, 1111))
path = './config/images/items/'

potion_hp_image = hf.scale_size_image(pygame.image.load(f'{path}potion_hp.png').convert_alpha(), 25, 25)
potion_mana_image = hf.scale_size_image(pygame.image.load(f'{path}potion_mana.png').convert_alpha(), 25, 25)
potion_green_image = hf.scale_size_image(pygame.image.load(f'{path}potion_green.png').convert_alpha(), 25, 25)
potion_orange_image = hf.scale_size_image(pygame.image.load(f'{path}potion_orange.png').convert_alpha(), 25, 25)
box_image = hf.scale_image(pygame.image.load(f'{path}bow_box.png').convert_alpha(), 1.2)
coin_images = []
coin_img = pygame.image.load(f'./config/images/items/coin-blog.png')
coin_image = SpriteImage(coin_img)

for i in range(1, 7):
    image = coin_image.get_image_one_sheet(6, i, 0.25)
    coin_images.append(image)

# Create images list to import map.py
item_list = [coin_images, potion_hp_image, potion_mana_image, box_image, potion_green_image, potion_orange_image,
             potion_hp_image, potion_mana_image, box_image, potion_green_image, potion_orange_image]

for i in range(9):
    image = hf.scale_size_image(pygame.image.load(f'./config/images/items/potion_{i}.png').convert_alpha(), 35, 35)
    item_list.append(image)

# 0 = 'imp', 'skeleton', 'goblin', 3 = 'muddy', 'tiny_zombie', 5 = 'big_demon', 6 = 'big_ogre', 'big_zombie', 'slug'
# Mob static definition
health_list = [40, 60, 120, 350, 10, 850, 1111, 2500, 225]
armor_list = [25, 110, 50, 0, 150, 40, 60, 0, 0]
drop_chance_list = [5, 0, 10, 25, 5, 0, 0, 0, 10]
velocity_list = [0.75, 2.95, 2.40, 1.65, 4.55, 2.15, 1.45, 1.05, 1.25]
min_damage_list = [8, 9, 11, 12, 5, 13, 24, 16, 1]
max_damage_list = [10, 12, 14, 20, 7, 20, 33, 21, 3]
attack_range_list = [800, 570, 390, 275, 1350, 666, 1111, 555, 2500]
attack_cooldown_list = [900, 100, 1050, 1450, 100, 650, 650, 1100, 420]
range_attack_able = [1, 0, 0, 0, 0, 1, 0, 0, 0]
die_after_hit_list = [1, 0, 1, 1, 0, 1, 1, 1, 1]
crit_reduction_list = [10, 90, 0, 45, 0, 25, 0, 60, 0]
score_list = [13, 12, 18, 25, 10, 110, 175, 225, 20]

# image size changer & image displacement x and y
ISC_list = [0.65, 0.75, 0.65, 0.88, 0.65, 0.7, 0.65, 0.60, 0.70]
IDispX_list = [6, 5, 7,  2, 7, 11, 14, 16, 4]
IDispY_list = [4, 0, 6, -7, 7, 15, 23, 25, 9]

# sound
pygame.mixer.init()
sound_enemy = pygame.mixer.Sound('./config/music/punch.mp3')
sound_slug = pygame.mixer.Sound('./config/music/slug.wav')

# endregion


class EnemyMob(pygame.sprite.Sprite):
    def __init__(self, x, y, index, image_list, boss=False, typ=None):
        pygame.sprite.Sprite.__init__(self)
        self.update_time = pygame.time.get_ticks()
        self.alive = True
        self.add_drop = False
        self.add_drop = False
        self.add_score = False
        self.remove_from_group = False
        self.index = index
        self.fireball = range_attack_able[self.index]  # enemy can shoot or not (True / False)
        self.boss = boss
        self.typ = typ

        self.health = health_list[self.index] - random.randint(0, 3)
        self.max_health = health_list[self.index]
        self.velocity = velocity_list[self.index] * gs.ENEMY_AI_SPEED
        self.armor = armor_list[self.index]
        self.crit_reduction = crit_reduction_list[self.index]
        self.min_damage = min_damage_list[self.index]
        self.max_damage = max_damage_list[self.index]
        self.attack_range = attack_range_list[self.index]
        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = attack_cooldown_list[self.index]
        self.die_after_hit = die_after_hit_list[self.index]
        self.drop_chance = drop_chance_list[self.index]

        self.score = score_list[self.index] + random.randint(-2, 2)

        # images setting
        self.flip_x = False
        self.flip_y = False
        self.image_index = 0
        self.image_type = 0  # 0 = mob idle, 1 = mob running
        self.image_list = image_list[self.index + 1]
        self.image = self.image_list[self.image_type][self.image_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image_width, self.image_height = self.image.get_size()

        self.ISC = ISC_list[self.index]
        self.image_offset_x = IDispX_list[self.index]
        self.image_offset_y = IDispY_list[self.index]
        self.collision_rect = pygame.Rect(x + self.image_offset_x, y + self.image_offset_y,
                                          math.ceil(self.ISC * self.image_width),
                                          math.ceil(self.ISC * self.image_height))

        # # AI move system
        self.counter_ai = 0
        self.counter_rect = 0
        self.rect_number = random.randint(0, 1)
        self.ratio_ai_dx = random.randint(0, 4)
        self.ratio_ai_dy = random.randint(0, 4)
        self.collision_x = False
        self.collision_y = False

    def update(self):
        # check if enemy has died
        if self.health <= 0:
            self.health = 0
            self.alive = False

        # enemy animation running
        animation_cooldown = 70
        self.image = self.image_list[self.image_type][self.image_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.image_index = (self.image_index + 1) % 4
            self.update_time = pygame.time.get_ticks()

        # zombie hp regen
        if self.index == 7 and self.alive and self.health <= self.max_health - 1:
            self.health += 1

        # AI system update
        self.counter_ai += 1
        if self.counter_ai >= 20:
            self.ratio_ai_dx = random.randint(0, 4)
            self.ratio_ai_dy = random.randint(0, 4)
            self.counter_ai = 0

        self.counter_rect += 1
        if self.counter_rect >= 30:
            self.rect_number = random.randint(0, 1)
            self.counter_rect = 0

        # drop after die
        drop = None
        if not self.alive and not self.add_drop:
            if self.boss:
                if self.typ == 'Zombie Boss':
                    drop_index = random.randint(11, 19)
                elif self.typ == 'slow':
                    drop_index = random.choice([1, 2, 4, 4, 5, 5])
                else:
                    drop_index = random.randint(0, 5)
                drop = Item(x=self.rect.centerx, y=self.rect.centery, typ=drop_index, image_list=item_list)
            else:
                if random.randint(0, 100) < self.drop_chance:
                    drop = Item(x=self.rect.centerx, y=self.rect.centery,
                                typ=random.randint(0, 3), image_list=item_list)
                    if drop is not None:
                        print('drop item')
            self.add_drop = True
            self.kill()
            # add score after die in function move()
            self.rect.center = (-5000, -5000)
            self.collision_rect.center = (-5000, -5000)
        return drop

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip_x, self.flip_y)
        surface.blit(flipped_image, (self.rect.x, self.rect.y - gs.ENEMY_OFFSET * gs.SCALE))

        # draw hp bar
        if self.boss and self.alive:
            ratio = self.health / self.max_health
            pygame.draw.rect(surface, gs.RED_dark, (self.rect.centerx - 32,
                                                    self.rect.centery - 55 + 3 * self.index, 60, 5), 1)
            pygame.draw.rect(surface, gs.RED, (self.rect.centerx - 32,
                                               self.rect.centery - 55 + 3 * self.index, 60 * ratio, 5))

    def move(self, screen_scroll, player, obstacle_list):
        fireball_obj = None
        if self.alive:
            clipped_line = ()
            ai_dx = 0
            ai_dy = 0
            if not self.fireball:
                target = player.rect if self.rect_number == 0 else player.rect2
            else:
                target = player.rect3

            # create a line of sight from the enemy to the player
            enemy_sight_line = ((self.rect.centerx, self.rect.centery), (target.centerx, target.centery))

            # check if sights line passes through wall
            for obstacle in obstacle_list:
                if obstacle[1].clipline(enemy_sight_line):
                    clipped_line = obstacle[1].clipline(enemy_sight_line)

            # check distance to player
            dist = math.sqrt(
                ((self.rect.centerx - player.rect.centerx) ** 2) + ((self.rect.centery - player.rect.centery) ** 2))

            # change direction
            if (self.index in [0, 5, 8] or not clipped_line) and 50 < dist < self.attack_range:
                if self.rect.centerx > target.centerx:
                    ai_dx = -self.velocity
                    self.flip_x = True
                if self.rect.centerx < target.centerx:
                    ai_dx = self.velocity
                    self.flip_x = False
                if self.rect.centery > target.centery:
                    ai_dy = -self.velocity
                if self.rect.centery < target.centery:
                    ai_dy = self.velocity

            # calculate speed value
            if ai_dx != 0 and ai_dy != 0:
                ai_dx = ai_dx * hf.sin_or_cos(self.ratio_ai_dx, self.ratio_ai_dy, sin=True)
                ai_dy = ai_dy * hf.sin_or_cos(self.ratio_ai_dx, self.ratio_ai_dy, sin=False)

            # Check for collision in X direction
            temp_rect = self.collision_rect.copy()
            temp_rect_x = self.collision_rect.x + screen_scroll[0] + ai_dx
            temp_rect.x = temp_rect_x

            for obstacle in obstacle_list:
                if obstacle[1].colliderect(temp_rect):
                    self.collision_x = True
                    ai_dx = 0

            # Check for collision in Y direction
            temp_rect_y = self.collision_rect.y + screen_scroll[1] + ai_dy
            temp_rect.y = temp_rect_y

            for obstacle in obstacle_list:
                if obstacle[1].colliderect(temp_rect):
                    self.collision_y = True
                    ai_dy = 0

            # move enemy (change enemy.rect position)
            self.rect.x += screen_scroll[0] + ai_dx
            self.rect.y += screen_scroll[1] + ai_dy
            self.collision_rect.x += screen_scroll[0] + ai_dx
            self.collision_rect.y += screen_scroll[1] + ai_dy

            # Restart collision_rect
            if self.collision_x or self.collision_y:
                self.collision_rect = pygame.Rect(self.rect.x + self.image_offset_x,
                                                  self.rect.y + self.image_offset_y,
                                                  math.ceil(self.ISC * self.image_width),
                                                  math.ceil(self.ISC * self.image_height))

            ''' fireball DMG in Fireball class - weapon.py '''
            # enemy fireball hit the player
            if self.fireball and dist < self.attack_range and \
                    pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                self.last_attack = pygame.time.get_ticks()
                fireball_scale = 0.85 if self.boss else 0.5
                fireball_index = 1 if self.boss else 0
                fireball_obj = weapon.Fireball(self.collision_rect.centerx, self.collision_rect.centery,
                                               player.rect.centerx, player.rect.centery,
                                               index=fireball_index, scale=fireball_scale)

            # enemy bite the player
            if dist < 52 and pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                # enemy DMG
                player_armor = 100 / (100 + player.armor)
                damage = math.ceil(random.randint(self.min_damage, self.max_damage) * player_armor)

                player.health -= damage
                self.last_attack = pygame.time.get_ticks()

                if self.typ == 'armor':
                    player.armor -= random.randint(0, 4)
                if self.typ == 'boost':
                    if player.boost_lvl > 0:
                        player.boost_lvl -= 350
                if self.typ == 'Zombie Boss':
                    player.coin_amount -= 1
                    player.score -= 1
                if self.die_after_hit == 0:
                    player.score -= 1
                    self.rect.center = (-5000, -5000)  # kill() not working, i m just change x,y away map
                    self.collision_rect.center = (-5000, -5000)
                if player.health > 0:
                    if self.typ == 'slow':
                        player.slowed = True
                        if player.velocity_normal > 3.35:
                            player.velocity_normal -= random.randint(16, 20) / 100
                        elif player.velocity_normal > 2.15:
                            player.velocity_normal -= random.randint(11, 15) / 100
                        elif player.velocity_normal > 1.45:
                            player.velocity_normal -= 0.08
                        else:
                            player.velocity_normal -= 1.25
                        sound_slug.play()
                    else:
                        sound_enemy.play()

        # Add score if player kill enemy
        if not self.alive and not self.add_score:
            player.score += math.ceil(random.randint(70, 100) * self.score / 100)
            self.add_score = True

        # return fireball object
        return fireball_obj


class DamageText(pygame.sprite.Sprite):
    def __init__(self, text, coordinates, critical_strike=False, slow=False):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.W, self.H = coordinates
        font = gs.font_crit if critical_strike else gs.font_dmg
        color = gs.BLUE if slow else gs.RED
        self.image = font.render(str(text), True, color)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.counter = 0

    def update(self, screen_scroll):
        # reposition after camera moving
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # MoveUp damage text
        self.rect.y -= gs.DAMAGE_TEXT_SPEED

        # Delete damage text after 35/60 sek
        self.counter += 1
        if self.counter > 35:
            self.kill()
