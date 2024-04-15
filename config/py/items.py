import random
import pygame
import math
pygame.mixer.init()

sound_hp = pygame.mixer.Sound('./config/music/health-pickup.mp3')
sound_mana = pygame.mixer.Sound('./config/music/mana_pickup.mp3')
sound_coin = pygame.mixer.Sound('./config/music/coin.wav')
sound_arrow_box = pygame.mixer.Sound('./config/music/item-equip.mp3')
sound_bonus_01 = pygame.mixer.Sound('./config/music/bonus_01.wav')
sound_bonus_02 = pygame.mixer.Sound('./config/music/bonus_02.wav')


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, typ, image_list):
        pygame.sprite.Sprite.__init__(self)
        self.typ = typ  # 0 - coin,  1 - health potion
        self.item_time = pygame.time.get_ticks()
        self.bonus_score = 5
        self.bonus_mana = 400

        # images setting
        self.image_index = typ
        self.image_list = image_list
        if self.image_index == 0:
            self.image = self.image_list[0][self.image_index]
        else:
            self.image = self.image_list[self.image_index]

        self.rect = self.image.get_rect(center=(x, y))

    def update(self, screen_scroll, player, weapon):
        # reposition after camera moving
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # check collision
        if self.rect.colliderect(player.rect):
            # coin collected
            if self.typ == 0:
                player.score += self.bonus_score
                player.coin_amount += 1
                sound_coin.play()
                self.kill()
            # potion hp collected
            elif self.typ == 1:
                self.kill()
                sound_hp.play()
                player.health += random.randint(15, 20)
                player.health = player.max_hp if player.health > player.max_hp else player.health
                player.score += self.bonus_score
            # potion mana collected
            elif self.typ == 2:
                self.kill()
                sound_hp.play()
                player.boost_lvl += self.bonus_mana
                player.slowed = False
                player.score += self.bonus_score
            # arrow box collected
            elif self.typ == 3:
                self.kill()
                sound_arrow_box.play()
                weapon.storage += 1
                player.score += self.bonus_score
            # potion green
            elif self.typ == 4:
                self.kill()
                sound_mana.play()
                weapon.deceleration -= 0.85
                player.velocity_normal += 0.10
                player.score += self.bonus_score
            # potion orange
            elif self.typ == 5:
                self.kill()
                sound_mana.play()
                weapon.max_amount += weapon.max_amount // 10
                weapon.deceleration -= 0.25
                player.score += self.bonus_score
            # Empty slot to new free item option

            # SHOP BONUSES
            elif self.typ == 11:
                self.kill()
                sound_bonus_02.play()
                player.max_hp += random.randint(10, 15)
                player.health += 15
            elif self.typ == 12:
                self.kill()
                sound_bonus_02.play()
                player.velocity_normal += random.randint(15, 20) / 100
            elif self.typ == 13:
                self.kill()
                weapon.slow_chance += 3
                weapon.deceleration -= 0.45
                weapon.min_damage += 1
                sound_bonus_01.play()
            elif self.typ == 14:
                self.kill()
                sound_bonus_01.play()
                weapon.shot_cooldown -= weapon.shot_cooldown * 0.90
            elif self.typ == 15:
                self.kill()
                player.fire_resist += random.randint(10, 13)
                sound_bonus_02.play()
            elif self.typ == 16:
                self.kill()
                player.armor += random.randint(15, 20)
                player.max_hp += random.randint(3, 5)
                player.health += 5
                sound_bonus_02.play()
            elif self.typ == 17:
                self.kill()
                sound_bonus_01.play()
                weapon.max_damage += random.randint(2, 4)
                weapon.min_damage += random.randint(3, 5)
            elif self.typ == 18:
                self.kill()
                sound_bonus_01.play()
                weapon.critical_chance += random.randint(3, 5)
                add_dmg = max(1, math.ceil(weapon.min_damage * 1.042))
                weapon.min_damage += add_dmg
            elif self.typ == 19:
                self.kill()
                sound_bonus_01.play()
                weapon.armor_penetration += random.randint(3, 5)
                add_dmg_2 = max(1, math.ceil(weapon.max_damage * 1.044))
                weapon.max_damage += add_dmg_2

        # update coin image
        animation_cooldown = 130
        if self.typ == 0:
            self.image = self.image_list[0][self.image_index]
            if pygame.time.get_ticks() - self.item_time > animation_cooldown:
                self.image_index = (self.image_index + 1) % 5
                self.item_time = pygame.time.get_ticks()
