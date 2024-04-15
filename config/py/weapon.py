import random
import pygame
from . import functions as hf
from . import game_settings as gs
import math
import ctypes
from .sprite_image import SpriteImage

# region pygame init
pygame.init()
screen = pygame.display.set_mode((gs.WINDOW_WIDTH, gs.WINDOW_HEIGHT))
screen.fill(gs.WHITE)
pygame.display.set_caption("MYSZ.games")


def center_window():
    user32 = ctypes.windll.user32
    screen_center_x = user32.GetSystemMetrics(0) // 2
    screen_center_y = user32.GetSystemMetrics(1) // 2
    user32.SetWindowPos(pygame.display.get_wm_info()["window"], 0, screen_center_x - gs.WINDOW_WIDTH // 2,
                        screen_center_y - gs.WINDOW_HEIGHT // 2 - 50, 0, 0, 0x0001)


intro_img = pygame.image.load('./config/images/intro/mysz_games2.png')
intro_rect = intro_img.get_rect(topleft=(86, -50))
logo_image = pygame.image.load('./config/images/game/logo.png')
pygame.display.set_icon(logo_image)
pygame.mouse.set_visible(False)
screen.blit(intro_img, intro_rect)
pygame.display.flip()
center_window()
pygame.time.delay(2500)
# endregion

# region  Weapon setting
# images
weapon_bow_image = hf.scale_image(pygame.image.load('./config/images/weapons/bow01.png'), 0.90)
weapon_bow2_image = hf.scale_image(pygame.image.load('./config/images/weapons/bow02.png'), 1.00)
weapon_bow3_image = hf.scale_image(pygame.image.load('./config/images/weapons/bow03.png'), 1.10)
weapon_bow4_image = hf.scale_image(pygame.image.load('./config/images/weapons/bow04.png'), 0.90)
weapon_arrow_image = hf.scale_image(pygame.image.load('./config/images/weapons/arrow01.png'), 0.75)
weapon_arrow2_image = hf.scale_image(pygame.image.load('./config/images/weapons/arrow02.png'), 1.00)
weapon_arrow3_image = hf.scale_image(pygame.image.load('./config/images/weapons/arrow03.png'), 0.95)
weapon_arrow4_image = hf.scale_image(pygame.image.load('./config/images/weapons/arrow04.png'), 0.90)

# values
images_bow_list = [weapon_bow_image, weapon_bow2_image, weapon_bow3_image, weapon_bow4_image]
shot_cooldown_list = [380, 285, 195, 90]
reload_cooldown_list = [1250, 666, 1000, 2000]
amount_list = [10, 25, 30, 55]
max_amount_list = [10, 25, 30, 55]
storage_list = [2, 3, 4, 3]

images_arrow_list = [weapon_arrow_image, weapon_arrow2_image, weapon_arrow3_image, weapon_arrow4_image]
critical_chance_list = [30, 10, 5, 1]
slow_chance_list = [0, 5, 25, 1]
min_damage_distance_list = [250,  50, 350, 125]
max_damage_distance_list = [999, 750, 600, 425]
min_damage_list = [60, 25, 20, 9]
max_damage_list = [85, 60, 35, 14]
deceleration_list = [2.5, 0.5, -1.8, 1.0]
armor_penetration_list = [35, 15, 0, 20]  # 0-100%

# music
pygame.mixer.init()
sound_shoot = pygame.mixer.Sound('./config/music/arrow_shot.mp3')
sound_hit = pygame.mixer.Sound('./config/music/arrow_hit.wav')
sound_fireball = pygame.mixer.Sound('./config/music/hurt.mp3')
sound_floor = pygame.mixer.Sound('./config/music/knife.mp3')
sound_shop = pygame.mixer.Sound('./config/music/shop.mp3')
sound_auto_shooter = pygame.mixer.Sound('./config/music/auto_shooter.mp3')


# endregion


class Bow:
    def __init__(self, index):
        self.index = index
        self.image_original = images_bow_list[self.index]
        self.image_angle = 0

        # Bow values
        self.shot_cooldown = shot_cooldown_list[self.index]
        self.reload_cooldown = reload_cooldown_list[self.index]
        self.amount = amount_list[self.index]
        self.max_amount = max_amount_list[self.index]
        self.storage = storage_list[self.index]
        self.reloading = False
        self.auto_shooter = False
        self.shooter_counter = 0
        self.fired = False
        self.last_buy = pygame.time.get_ticks()
        self.auto_shooter_time = pygame.time.get_ticks()
        self.extra_time = 0

        self.image = pygame.transform.rotate(self.image_original, self.image_angle)
        self.rect = self.image.get_rect()

        # Restart Bow values
        self.start_deceleration = deceleration_list[self.index]
        self.start_max_amount = max_amount_list[self.index]
        self.start_shoot_cooldown = shot_cooldown_list[self.index]

        # Arrow values
        self.critical_chance = critical_chance_list[self.index]
        self.slow_chance = slow_chance_list[self.index]
        self.min_damage_distance = min_damage_distance_list[self.index]
        self.max_damage_distance = max_damage_distance_list[self.index]
        self.min_damage = min_damage_list[self.index]
        self.max_damage = max_damage_list[self.index]
        self.deceleration = deceleration_list[self.index]
        self.armor_penetration = armor_penetration_list[self.index]

        self.arrow_image = images_arrow_list[self.index]
        self.last_shot = pygame.time.get_ticks()  # shot cooldown

    def update(self, player, weapon):
        arrow = None
        self.rect.center = player.rect.center

        # arrow rotate when mouse moving
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -pos[1] + self.rect.centery
        self.image_angle = math.degrees(math.atan2(y_dist, x_dist))

        #
        self.shot_cooldown = max(self.shot_cooldown, 75)

        # SHOT = user clicked left mouse button
        if pygame.mouse.get_pressed()[0] and not self.fired and \
                (pygame.time.get_ticks() - self.last_shot > self.shot_cooldown) \
                and weapon.amount > 0 and not self.reloading:
            # create single arrow
            arrow = Arrow(self.rect.centerx, self.rect.centery, self.image_angle, self.index, self.critical_chance,
                          self.slow_chance, self.min_damage_distance, self.max_damage_distance, self.min_damage,
                          self.max_damage, self.deceleration, self.armor_penetration)
            self.last_shot = pygame.time.get_ticks()
            weapon.amount -= 1
            sound_shoot.play()
            # u can hold mouse pressed to shot ( while self.auto_shooter = True )
            self.fired = False if self.auto_shooter else True

        # reset mouseclick
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

        # reload time
        if weapon.amount == 0:
            self.reloading = True

        # Arrow buying
        keys = pygame.key.get_pressed()
        if keys[pygame.K_b] and pygame.time.get_ticks() - self.last_shot > 600 and player.coin_amount >= 5:
            player.coin_amount -= 5
            self.storage += 1
            self.last_shot = pygame.time.get_ticks()
            sound_shop.play()

        # Auto-shooter ON
        if keys[pygame.K_q] and pygame.time.get_ticks() - self.last_shot > 450 and player.coin_amount >= 1:
            if self.auto_shooter:
                self.extra_time += 1150
            player.coin_amount -= 1
            self.last_shot = pygame.time.get_ticks()
            self.auto_shooter_time = pygame.time.get_ticks()
            sound_auto_shooter.play()
            self.auto_shooter = True

        # Auto-shooter OFF
        if pygame.time.get_ticks() - self.auto_shooter_time > 1250 + self.extra_time:
            self.auto_shooter = False
            self.extra_time = 0

        # Automate Auto-shooter [weapon 4 - orange
        if self.index == 3:
            self.shooter_counter += 1
        if self.shooter_counter >= 82:
            self.auto_shooter = True
            self.auto_shooter_time = pygame.time.get_ticks()
            self.shooter_counter = 0

        # restart after die
        if player.dead:
            self.image_original = images_bow_list[self.index]
            self.arrow_image = images_arrow_list[self.index]

            self.deceleration = self.start_deceleration
            self.shot_cooldown = self.start_shoot_cooldown
            self.reload_cooldown = reload_cooldown_list[self.index]

            self.amount = amount_list[self.index]
            self.max_amount = max_amount_list[self.index]
            self.storage = storage_list[self.index]
            self.auto_shooter = False

        return arrow

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.image_original, self.image_angle)
        surface.blit(self.image, (self.rect.centerx - self.image.get_width() // 2,
                                  self.rect.centery - self.image.get_height() // 2))

    def restart(self):
        # Bow values
        self.shot_cooldown = shot_cooldown_list[self.index]
        self.reload_cooldown = reload_cooldown_list[self.index]
        self.amount = amount_list[self.index]
        self.max_amount = max_amount_list[self.index]
        self.storage = storage_list[self.index]
        # Arrow values
        self.critical_chance = critical_chance_list[self.index]
        self.slow_chance = slow_chance_list[self.index]
        self.min_damage_distance = min_damage_distance_list[self.index]
        self.max_damage_distance = max_damage_distance_list[self.index]
        self.min_damage = min_damage_list[self.index]
        self.max_damage = max_damage_list[self.index]
        self.deceleration = deceleration_list[self.index]
        self.armor_penetration = armor_penetration_list[self.index]


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, index=0, critical_chance=0, slow_chance=0, min_damage_distance=0,
                 max_damage_distance=0, min_damage=0, max_damage=0, deceleration=0, armor_penetration=0):
        pygame.sprite.Sprite.__init__(self)
        self.index = int(index)
        self.image_original = images_arrow_list[self.index]
        self.image_angle = angle
        self.image = pygame.transform.rotate(self.image_original, self.image_angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.start_x = x
        self.start_y = y
        self.counter = 0

        # extra values
        self.critical_chance = critical_chance
        self.slow_chance = slow_chance
        self.min_damage_distance = min_damage_distance
        self.max_damage_distance = max_damage_distance
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.deceleration = deceleration
        self.armor_penetration = armor_penetration

        # calculate the horizontal and vertical speed based on the angle
        self.rad_angel = math.radians(self.image_angle)
        self.dx = math.cos(self.rad_angel) * gs.ARROW_SPEED
        self.dy = -math.sin(self.rad_angel) * gs.ARROW_SPEED

    def update(self, enemy_list, obstacle_list=None, screen_scrool=None):
        # reset variables before return
        if screen_scrool is None:
            screen_scrool = []
        if obstacle_list is None:
            obstacle_list = []
        full_damage = 0
        damage_pos = None
        critical_strike = False
        slow = False
        self.counter += self.deceleration

        # arrow reposition
        self.rect.x += screen_scrool[0] + self.dx * (1000 - self.counter) / 1000
        self.rect.y += screen_scrool[1] + self.dy * (1000 - self.counter) / 1000

        # check if arrow has gone of screen
        if self.rect.right < -gs.ARROW_OFFSET or self.rect.left > gs.WINDOW_WIDTH + gs.ARROW_OFFSET \
                or self.rect.top < -gs.ARROW_OFFSET or self.rect.bottom > gs.WINDOW_HEIGHT + gs.ARROW_OFFSET:
            self.kill()

        # check if arrow over the maximum distance
        if hf.diagonal_distance(self.rect.x, self.start_x, self.rect.y, self.start_y) > self.max_damage_distance:
            self.kill()

        # check if arrow hit wall  (obstacle_collision)
        for obstacle in obstacle_list:
            if obstacle[1].colliderect(self.rect):
                self.kill()

        # check collision with enemy
        for enemy in enemy_list:
            if enemy.collision_rect.colliderect(self.rect) and enemy.alive:
                arrow_distance = hf.diagonal_distance(self.rect.x, self.start_x, self.rect.y, self.start_y)
                enemy_armor = 100 / (100 + enemy.armor * (100 - self.armor_penetration) / 100)
                enemy_crit_reduction = (100 - enemy.crit_reduction) / 100

                # basic arrow damage (more dmg while you are closer to enemy)
                # print(arrow_distance)
                if arrow_distance <= self.min_damage_distance:
                    basic_damage = self.max_damage - random.randint(0, 1)
                else:
                    damage_typ1 = self.max_damage - 2 - (
                                (self.max_damage - self.min_damage) * (arrow_distance / self.max_damage_distance))
                    damage_typ2 = hf.random_number(self.min_damage, self.max_damage)
                    typ_1_chance = (max(0, arrow_distance - self.min_damage_distance) /
                                    (self.max_damage_distance - self.min_damage_distance))
                    typ_2_chance = 1 - typ_1_chance
                    basic_damage = random.choices([damage_typ1, damage_typ2], [typ_1_chance, typ_2_chance])[0]

                # total damage
                damage = basic_damage * enemy_armor
                critical_dmg = damage * enemy_crit_reduction if random.randint(0, 99) < self.critical_chance else 0
                full_damage = math.ceil(damage + critical_dmg)
                damage_pos = enemy.rect
                enemy.health -= full_damage
                critical_strike = True if critical_dmg > 0 else False
                slow = True if random.randint(0, 99) < self.slow_chance else False
                self.kill()
                sound_hit.play()
                if slow:
                    if enemy.velocity > 3.65:
                        enemy.velocity -= 0.75
                    elif enemy.velocity > 2.75:
                        enemy.velocity -= 0.45
                    elif enemy.velocity > 1.85:
                        enemy.velocity -= 0.25
                    elif enemy.velocity > 1.05:
                        enemy.velocity -= 0.15
                    elif enemy.velocity > 0.55:
                        enemy.velocity -= 0.10
                    elif enemy.velocity <= 0.55:
                        enemy.velocity -= 0.03
                break
        return full_damage, damage_pos, critical_strike, slow

    def draw(self, surface):
        surface.blit(self.image, (self.rect.centerx - self.image.get_width() // 2,
                                  self.rect.centery - self.image.get_height() // 2))


# region Fireball setting
fireball_range_distance_list = [300, 380]
fireball_min_damage_list = [8, 13]
fireball_max_damage_list = [10, 20]
fireball_speed_list = [2.75, 3.75]

# Load Fireball explode images
fireball_images_list_01 = []
fireball_images_list_02 = []
fireball_sprites_img = SpriteImage(pygame.image.load(f'./config/images/weapons/fire_explode.png'))
for i in range(1, 7):
    image = fireball_sprites_img.get_image_one_sheet(amount=7, index=i, scale=0.25)
    fireball_images_list_01.append(image)
for i in range(1, 7):
    image = fireball_sprites_img.get_image_one_sheet(amount=7, index=i, scale=0.55)
    fireball_images_list_02.append(image)

fireball_images_list = [fireball_images_list_01, fireball_images_list_02]


# endregion


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, index=0, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale
        self.image_original = hf.scale_image(pygame.image.load('./config/images/weapons/fireball.png'), self.scale)
        distance_x = target_x - x
        distance_y = y - target_y
        self.index = index
        self.angel = math.degrees(math.atan2(distance_y, distance_x)) + random.randint(-5, 5)
        self.image = pygame.transform.rotate(self.image_original, self.angel)
        self.rect = self.image.get_rect(center=(x, y))

        self.start_x = x
        self.start_y = y
        self.range_distance = fireball_range_distance_list[self.index]
        self.min_damage = fireball_min_damage_list[self.index]
        self.max_damage = fireball_max_damage_list[self.index]
        self.speed = fireball_speed_list[self.index]

        # calculate the horizontal and vertical speed based on the angle
        self.rad_angel = math.radians(self.angel)
        self.dx = math.cos(self.rad_angel) * self.speed
        self.dy = -math.sin(self.rad_angel) * self.speed

        # animation settings
        self.update_time = pygame.time.get_ticks()
        self.make_animation = False
        self.animation_index = 0
        self.animation_list = fireball_images_list[self.index]
        self.animation_cooldown = 75

    def update(self, player, screen_scroll, obstacle_list=None):
        # fireball reposition
        if obstacle_list is None:
            obstacle_list = []

        # update position
        self.rect.x += screen_scroll[0] + (self.dx // 1) * (1 - int(self.make_animation))
        self.rect.y += screen_scroll[1] + (self.dy // 1) * (1 - int(self.make_animation))

        # check if fireball has gone of screen
        if self.rect.right < -gs.FIREBALL_OFFSET or self.rect.left > gs.WINDOW_WIDTH + gs.FIREBALL_OFFSET \
                or self.rect.top < -gs.FIREBALL_OFFSET or self.rect.bottom > gs.WINDOW_HEIGHT + gs.FIREBALL_OFFSET:
            self.kill()

        # check if fireball over the maximum distance
        if hf.diagonal_distance(self.rect.x, self.start_x, self.rect.y, self.start_y) > self.range_distance \
                and not self.make_animation:
            self.make_animation = True

        # check if fireball hit wall (obstacle_collision)
        for obstacle in obstacle_list:
            if obstacle[1].colliderect(self.rect):
                self.kill()

        # check collision with player
        if player.rect.colliderect(self.rect):
            player_resist = (100 - player.fire_resist) / 100
            damage = math.ceil(hf.random_number(self.min_damage, self.max_damage) * player_resist)
            # damage_pos = player.rect
            player.health -= damage
            self.kill()
            if not player.dead:
                sound_fireball.play()

        # make animation after max distance
        if self.make_animation:
            self.image = self.animation_list[self.animation_index]
            if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
                if self.animation_index == len(self.animation_list) - 1:
                    if pygame.time.get_ticks() - self.update_time > 2 * self.animation_cooldown:
                        self.kill()
                else:
                    self.animation_index += 1
                    self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        surface.blit(self.image, (self.rect.centerx - self.image.get_width() // 2,
                                  self.rect.centery - self.image.get_height() // 2))


# Floor settings
image_list = []
for i in range(4):
    image = pygame.image.load(f'./config/images/floor/floor_spikes_anim_f{i}.png')
    image_list.append(hf.scale_size_image(image, gs.TILE_SIZE, gs.TILE_SIZE))


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, index=0, animation_cooldown=650):
        pygame.sprite.Sprite.__init__(self)
        self.image_list = image_list
        self.index = index
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_cooldown = animation_cooldown
        self.image_time = pygame.time.get_ticks()
        self.hurt_time = pygame.time.get_ticks()

    def update(self, screen_scroll, player, weapon=None):
        # reposition after camera moving
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # check collision
        if self.rect.colliderect(player.rect):
            if self.index == 1:
                player.health -= 1
                self.image_time = pygame.time.get_ticks()
                sound_floor.set_volume(0.2)
                # play sound effect
                if pygame.time.get_ticks() - self.hurt_time > 1250 and not player.dead:
                    sound_floor.play()
                    self.hurt_time = pygame.time.get_ticks()
            if self.index == 2:
                player.health -= 5
                self.image_time = pygame.time.get_ticks()
                sound_floor.set_volume(0.4)
                # play sound effect
                if pygame.time.get_ticks() - self.hurt_time > 1250 and not player.dead:
                    sound_floor.play()
                    self.hurt_time = pygame.time.get_ticks()
            if self.index == 3:
                player.health -= 15
                self.image_time = pygame.time.get_ticks()
                sound_floor.set_volume(0.75)
                # play sound effect
                if pygame.time.get_ticks() - self.hurt_time > 1250 and not player.dead:
                    sound_floor.play()
                    self.hurt_time = pygame.time.get_ticks()
        # update image
        self.image = self.image_list[self.index]
        if pygame.time.get_ticks() - self.image_time > self.animation_cooldown:
            self.index = (self.index + 1) % 4
            self.image_time = pygame.time.get_ticks()

        player.update()
