import pygame
from pygame import mixer
import os
import random
import csv
import button

mixer.init()
pygame.init()
from pygame.locals import *

flags = FULLSCREEN | DOUBLEBUF

# Constants & Variables
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
GRAVITY = 0.28
FRACTION = 0.4
SCROLL_THRESH = 400  # the distance to the edge of screen to start scrolling
ROWS = 16
COLS = 700  # columns
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPE = 40  # the different numbers of tiles types
screen_scroll = 0  # the main one    (to move rectangles)
bg_scroll = 0  # particular to the background
level = 1
MAX_LEVELS = 3
start_game = False
start_intro = False
# Creating Events
PLAYER_HIT = pygame.USEREVENT + 1
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the WINDOW
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, 16)
pygame.display.set_caption("Game 2")  # Set the Name (title) of the game
# Define player Action Variables
moving_left = False
moving_right = False
shoot = False
throw = False
grenade_thrown = False
aim = False
is_aiming = False
shooot = False
aim_crouch = False
crouch = False
action = False
music_on = True
# Set FrameRate
clock = pygame.time.Clock()
FPS = 60
# Colors
BG = (144, 201, 120)  # background color
RED = (127, 23, 31)
WHITE = (255, 255, 255)
GREEN = (77, 150, 99)
GREEN2 = (50, 220, 50)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
BLUE2 = (21, 52, 80)
BLUE1 = (50, 80, 150)
YELLOW1 = (182, 119, 33)
YELLOW2 = (127, 84, 23)
GREY = (27, 27, 27)
# Fonts
font = pygame.font.Font('fonts/EightBitDragon-anqx.ttf', 20)  # Futura
font2 = pygame.font.Font('fonts/EightBitDragon-anqx.ttf', 40)
font3 = pygame.font.Font('fonts/EightBitDragon-anqx.ttf', 15)
# Musics
pygame.mixer.music.load('audio/music1.mp3')
pygame.mixer.music.set_volume(0.17)
if music_on:
    pygame.mixer.music.play(-1, 0.0, 30000)
# Sounds
jump_fx = pygame.mixer.Sound('audio/jump.mp3')
jump_fx.set_volume(0.7)
shot1_fx = pygame.mixer.Sound('audio/shot1.mp3')
shot1_fx.set_volume(0.1)
shot3_fx = pygame.mixer.Sound('audio/shot3.mp3')
shot3_fx.set_volume(0.07)
shot4_fx = pygame.mixer.Sound('audio/shot4.mp3')
shot4_fx.set_volume(0.07)
grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0.5)
aim_fx = pygame.mixer.Sound('audio/aim.mp3')
aim_fx.set_volume(0.35)
emptygun_fx = pygame.mixer.Sound('audio/emptygun.mp3')
emptygun_fx.set_volume(0.5)
run_fx = pygame.mixer.Sound('audio/run.mp3')
run_fx.set_volume(0.19)
dog1_fx = pygame.mixer.Sound('audio/dog1.mp3')
dog1_fx.set_volume(0.2)
dog2_fx = pygame.mixer.Sound('audio/dog2.mp3')
dog2_fx.set_volume(0.25)
dog3_fx = pygame.mixer.Sound('audio/dog3.mp3')
dog3_fx.set_volume(0.25)
zombie1_fx = pygame.mixer.Sound('audio/zombie1.mp3')
zombie1_fx.set_volume(0.25)
zombie2_fx = pygame.mixer.Sound('audio/zombie2.mp3')
zombie2_fx.set_volume(0.25)
zombie3_fx = pygame.mixer.Sound('audio/zombie3.mp3')
zombie3_fx.set_volume(0.25)
zombie4_fx = pygame.mixer.Sound('audio/zombie4.wav')
zombie4_fx.set_volume(0.25)
zombie5_fx = pygame.mixer.Sound('audio/zombie5.wav')
zombie5_fx.set_volume(0.25)
zombie6_fx = pygame.mixer.Sound('audio/zombie6.mp3')
zombie6_fx.set_volume(0.25)
gold_fx = pygame.mixer.Sound('audio/gold.wav')
gold_fx.set_volume(0.4)
health_kit_fx = pygame.mixer.Sound('audio/health_kit.mp3')
health_kit_fx.set_volume(0.9)
item_fx = pygame.mixer.Sound('audio/item.wav')
item_fx.set_volume(0.3)
menu_fx = pygame.mixer.Sound('audio/menu.wav')
wind_fx = pygame.mixer.Sound('audio/wind.mp3')
wind_fx.set_volume(0.3)
levelup = pygame.mixer.Sound('audio/levelup.wav')
# IMAGES
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
spider_bullet_img = pygame.image.load('img/icons/spider_bullet.png').convert_alpha()
spider_grenade_img = pygame.image.load('img/icons/spider_grenade.png').convert_alpha()
gold_img = pygame.image.load('img/icons/gold.png').convert_alpha()
gold_img = pygame.transform.scale(gold_img, (25, 25)).convert_alpha()
gold_img_icon = pygame.image.load('img/icons/gold.png').convert_alpha()
gold_img_icon = pygame.transform.scale(gold_img_icon, (28, 28)).convert_alpha()
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
health_box_img = pygame.transform.scale(health_box_img, (110, 110)).convert_alpha()
health_box_icon_img = pygame.image.load('img/icons/health_box_icon.png').convert_alpha()
health_box_icon_img = pygame.transform.scale(health_box_icon_img, (80, 80))
ammo_box_img = pygame.image.load('img/icons/gun_ammo_box.png').convert_alpha()
ammo_box_img = pygame.transform.scale(ammo_box_img, (40, 40)).convert_alpha()
submachine_ammo_box_img = pygame.image.load('img/icons/submachine_ammo_box.png').convert_alpha()
submachine_ammo_box_img = pygame.transform.scale(submachine_ammo_box_img, (40, 40))
health_frame_img = pygame.image.load('img/icons/health_frame.png').convert_alpha()
health_frame_img = pygame.transform.scale(health_frame_img, (215, 40)).convert_alpha()
action_img = pygame.image.load('img/tile/23.png').convert_alpha()
location_img = pygame.image.load('img/tile/26.png').convert_alpha()
bar2_img = pygame.image.load('img/icons/bar2.png').convert_alpha()
bar2_img = pygame.transform.scale(bar2_img, (140, 45)).convert_alpha()
bar3_img = pygame.image.load('img/icons/bar3.png').convert_alpha()
bar1_img = pygame.image.load('img/icons/bar1.png').convert_alpha()
bar1_img = pygame.transform.scale(bar1_img, (800, 650)).convert_alpha()
logo_img = pygame.image.load('img/icons/blaster_logo.png').convert_alpha()
logo_img = pygame.transform.scale(logo_img, (400, 400)).convert_alpha()
logo2_img = pygame.image.load('img/icons/blaster_logo.png').convert_alpha()
logo2_img = pygame.transform.scale(logo_img, (150, 150)).convert_alpha()
icon_img = pygame.image.load('img/icons/icon.png').convert_alpha()
icon_img = pygame.transform.scale(icon_img, (32, 32)).convert_alpha()

#game_icon
pygame.display.set_icon(icon_img)

grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
grenade_box_img = pygame.transform.scale(grenade_box_img, (35, 35)).convert_alpha()
pistole_box_img = pygame.image.load('img/icons/pistole_box.png').convert_alpha()
pistole_box_img = pygame.transform.scale(pistole_box_img, (70, 60)).convert_alpha()
pistole_box_icon_img = pygame.image.load('img/icons/pistole_box_icon.png').convert_alpha()
pistole_box_icon_img = pygame.transform.scale(pistole_box_icon_img, (70, 60))
submachine_box_img = pygame.image.load('img/icons/submachine_box.png').convert_alpha()
submachine_box_img = pygame.transform.scale(submachine_box_img, (75, 57)).convert_alpha()
submachine_box_icon_img = pygame.image.load('img/icons/submachine_box_icon.png').convert_alpha()
submachine_box_icon_img = pygame.transform.scale(submachine_box_icon_img, (75, 50)).convert_alpha()
key_img = pygame.image.load('img/icons/key.png').convert_alpha()
key_img = pygame.transform.scale(key_img, (50, 50)).convert_alpha()

pine1_img = pygame.image.load('img/background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/background/mountain.png').convert_alpha()
castle_img = pygame.image.load('img/background/castle.png').convert_alpha()
castle_img = pygame.transform.scale(castle_img, (1376, 768)).convert_alpha()
forest_img = pygame.image.load('img/background/forest.png').convert_alpha()
forest_img = pygame.transform.scale(forest_img, (1376, 768)).convert_alpha()
forest1_img = pygame.image.load('img/background/forest1.png').convert_alpha()
forest1_img = pygame.transform.scale(forest1_img, (1376, 768)).convert_alpha()
forest2_img = pygame.image.load('img/background/forest2.png').convert_alpha()
forest2_img = pygame.transform.scale(forest2_img, (1376, 768)).convert_alpha()
forest3_img = pygame.image.load('img/background/forest3.png').convert_alpha()
forest3_img = pygame.transform.scale(forest3_img, (1376, 768)).convert_alpha()
forest4_img = pygame.image.load('img/background/forest4.png').convert_alpha()
forest4_img = pygame.transform.scale(forest4_img, (1376, 768)).convert_alpha()
forest5_img = pygame.image.load('img/background/forest5.png').convert_alpha()
forest5_img = pygame.transform.scale(forest5_img, (1376, 768)).convert_alpha()
forest6_img = pygame.image.load('img/background/forest6.png').convert_alpha()
forest6_img = pygame.transform.scale(forest6_img, (1376, 768)).convert_alpha()
forest7_img = pygame.image.load('img/background/forest7.png').convert_alpha()
forest7_img = pygame.transform.scale(forest7_img, (1376, 768)).convert_alpha()
forest8_img = pygame.image.load('img/background/forest8.png').convert_alpha()
forest8_img = pygame.transform.scale(forest8_img, (1376, 768)).convert_alpha()
menu_img = pygame.image.load('img/background/menu.png').convert_alpha()
menu_img = pygame.transform.scale(menu_img, (1376, 768)).convert_alpha()
hallway_img = pygame.image.load('img/background/hallway.png').convert_alpha()
hallway_img = pygame.transform.scale(hallway_img, (1376, 768)).convert_alpha()
hallway1_img = pygame.image.load('img/background/hallway1.png').convert_alpha()
hallway1_img = pygame.transform.scale(hallway1_img, (1376, 768)).convert_alpha()
hallway2_img = pygame.image.load('img/background/hallway2.png').convert_alpha()
hallway2_img = pygame.transform.scale(hallway2_img, (1376, 768)).convert_alpha()

start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
option_img = pygame.image.load('img/option_btn.png').convert_alpha()
resolution1_img = pygame.image.load('img/resolution1_btn.png').convert_alpha()
resolution2_img = pygame.image.load('img/resolution2_btn.png').convert_alpha()
resolution3_img = pygame.image.load('img/resolution3_btn.png').convert_alpha()
resolution4_img = pygame.image.load('img/resolution4_btn.png').convert_alpha()
resolution5_img = pygame.image.load('img/resolution5_btn.png').convert_alpha()
back_img = pygame.image.load('img/back_btn.png').convert_alpha()
arcade_img = pygame.image.load('img/arcade_btn.png').convert_alpha()
music_img = pygame.image.load('img/music_btn.png').convert_alpha()
credits_img = pygame.image.load('img/credit_btn.png').convert_alpha()
credits_img = pygame.transform.scale(credits_img, (180, 50)).convert_alpha()
help_img = pygame.image.load('img/help_btn.png').convert_alpha()
help_img = pygame.transform.scale(help_img, (180, 50)).convert_alpha()
MANUAL_CURSOR = pygame.image.load('img/icons/cursor.png').convert_alpha()  # CURSOR
MANUAL_CURSOR = pygame.transform.scale(MANUAL_CURSOR, (40, 40)).convert_alpha()

# world tiles images list
img_list = []
for x in range(TILE_TYPE):
    img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)).convert_alpha()
    img_list.append(img)

item_boxes = {
    'Health': health_box_img,
    'Gun_Ammo': ammo_box_img,
    'Submachine_Ammo': submachine_ammo_box_img,
    'Grenade': grenade_box_img,
    'Gold': gold_img,
    'Action': action_img,
    'Location': location_img,
    'Submachine': submachine_box_img,
    'Gun': pistole_box_img,
    'Key': key_img
}


# Draw text   (Transform Text to Image & Display it)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)  # TRANSFORM TEXT TO IMAGE   #True or 1 (anti alliasing)
    screen.blit(img, (x, y))

    # Draw Background

def draw_bg():
    screen.fill(BLACK)
    width = forest_img.get_width()
    if level == 1:
        for x in range(1, 23):
            screen.blit(forest_img, ((x * width) - bg_scroll * 0.92, 0))
        screen.blit(forest1_img, (- bg_scroll * 0.92, 0))  # bg_scroll * 0.8
        screen.blit(forest4_img, ((6 * width) - bg_scroll * 0.92, 0))
        screen.blit(forest5_img, ((10 * width) - bg_scroll * 0.92, 0))
        screen.blit(forest2_img, ((15 * width) - bg_scroll, 0))
        screen.blit(forest3_img, ((16 * width) - bg_scroll, 0))
    elif level == 2:
        for x in range(0, 23):
            screen.blit(hallway2_img, ((x * width) - bg_scroll, 0))  # bg_scroll * 0.8
        if player.lost_item:
            screen.blit(hallway1_img, ((1 * width) - bg_scroll, 0))
    elif level == 0:
        for x in range(0, 23):
            screen.blit(castle_img, ((x * width) - bg_scroll, 0))
    if cin == 0:
        screen.blit(bar3_img, (50, 58))
        screen.blit(gold_img_icon, ((SCREEN_WIDTH - 150, 61.5)))
        screen.blit(health_box_icon_img, (40, 92))
        if player.weapon == 'gun' and player.have_gun:
            screen.blit(pistole_box_icon_img, (47, 58))
        elif player.weapon == 'submachine' and player.have_submachine:
            screen.blit(submachine_box_icon_img, (59, 60))
        screen.blit(grenade_box_img, (61, 157))
        screen.blit(bar2_img, (SCREEN_WIDTH - 190, 10))
        health_bar = HealthBar(100, 28, player.health, player.max_health, 'player', 'health')
        health_bar.draw(player.health, 100)
        stamina_bar = HealthBar(100, 45, player.stamina, player.max_stamina, 'player', 'stamina')
        stamina_bar.draw(player.stamina, 100)
        if arcade and level == 0:
            time_bar = HealthBar(500, 45, player.time, player.max_time, 'player', 'time')
            time_bar.draw(player.time, 100)
            draw_text('Time', font, WHITE, 585, 25)
        screen.blit(health_frame_img, (62, 17))
        if player.have_gun or player.have_submachine:
            draw_text(f'{player.ammo}', font, GREEN2, 140, 80)  # Ammo Ui
        draw_text(f'{player.health_kit}', font, GREEN2, 140, 119)
        draw_text(f'{player.grenades}', font, GREEN2, 140, 164)
        draw_text(f'{player.gold}', font, WHITE, SCREEN_WIDTH - 97, 67)
        draw_text(f"Level:  {player.level}", font, WHITE, SCREEN_WIDTH - 170, 20)
        if player.have_key:
            screen.blit(key_img, (400, 20))

# TEXT BOX FUNCTION
text_box_img = pygame.image.load('img/icons/text_box.png')
text_box_img = pygame.transform.scale(text_box_img, (650, 150))


def text_box(text1, text2, text3):
    screen.blit(text_box_img, (380, 50))
    draw_text(f'{text1}', font, WHITE, 420, 80)
    draw_text(f'{text2}', font, WHITE, 420, 110)
    draw_text(f'{text3}', font, WHITE, 420, 145)

# Reset Function :    delete all instances     (used in 2 CASES: Death & Clearing Level(so we won't reload level in this function)
def reset_level():
    enemy_group.empty()
    zombie1_group.empty()
    zombie2_group.empty()
    spider_group.empty()
    dog_group.empty()
    bullet_player_group.empty()
    bullet_enemy_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    box_group.empty()
    stairs_group.empty()

    data = []  # THE STAGE (grid)             16*150 tiles
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data

# ______________________CREATING THE SOLDIER CLASS (Used for PLAYER or ENEMIES) :_______________________________________

class Soldier(pygame.sprite.Sprite):  # Inherit functionalities from pygame...class          SPRTIE CLASS
    def __init__(self, char_type, x, y, scale, speed, gun_ammo, health, grenades, gold, dmg, defense, submachine_ammo):
        pygame.sprite.Sprite.__init__(self)
        # VARIABLES
        self.time = 100
        self.max_time = 100
        self.hit_counter = 18
        self.hit = False
        self.disappear_counter = 150  # after death
        self.can_shoot = True
        self.have_key = False
        self.have_gun = False
        self.have_submachine = False
        self.char_type = char_type
        self.weapon = 'gun'
        self.submachine_ammo = submachine_ammo
        self.gun_ammo = gun_ammo
        self.health_kit = 2
        self.speed = speed
        if self.weapon == 'submachine':
            self.ammo = self.submachine_ammo  # The Resting ammo
        elif self.weapon == 'gun':
            self.ammo = self.gun_ammo
        self.start_ammo = gun_ammo  # The soldier's starting ammo
        self.shoot_cooldown = 0  # 0 ms     so we can shoot
        self.throw_cooldown = 0
        self.audio_cooldown = 0
        self.grenades = grenades
        self.gold = gold
        self.health = health
        self.max_health = self.health  # Starting health      (for the health bar)
        self.stamina = 100
        self.max_stamina = 100
        self.points = 0
        self.level = 1
        self.level_up = 100  # Points to reach next level
        self.dmg = dmg
        self.defense = defense
        self.vel_y = 0  # Jump Velocity
        self.vel_x = 0  # Slide Velocity
        self.direction = 1  # 1:looking to right        -1: looking to left
        self.alive = True
        self.jump = False  # (Define Action player Variable)
        self.slide = False
        self.in_air = True  # used for the jumping animation
        self.is_sliding = True
        self.turbo = False
        self.climb = False
        self.flip = False  # False: right(won't flip original sprite)       True: Left(flip original sprite)
        self.animation_list = []  # LIST OF FlipBooks
        self.frame_index = 0
        self.action = 0
        self.collide_action = False
        self.msg_index = 0
        self.location_index = 0
        self.update_time = pygame.time.get_ticks()
        # ai variables
        self.move_counter = 0  # to flip the enemy direction
        self.idling = False  # The enemies stop running (RANDOMLY) a bit then continue
        self.idle_counter = 0
        self.attack_cooldown = 0  # for Zombie
        self.lost_item = False
        self.can_ai = True
        self.attacking = False  # for dog
        self.done = False
        self.saw_player = False

        # ANIMATIONS                  to get all animations in animations list
        # Load all images(frames)
        animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Shoot', 'Fall', 'Aim', 'Shooot', 'AimRun', 'AimCrouch',
                           'ShootCrouch', 'Crouch', 'Hit', 'AimJump', 'AimFall', 'Slide', 'Roll', 'AimHit', 'Shoot2',
                           'Shooot2', 'AimCrouch2', 'ShootCrouch2', 'AimRun2', 'Wake', 'Shoot1_air', 'Shoot2_air']
        for animation in animation_types:
            temp_list = []  # Temporary List = FlipBook = Internal List = Action List   # RESET temporary list of images
            num_of_frames = len(os.listdir(
                f'img/{self.char_type}/{animation}'))  # Number of frames of each animation (of each flipBook)
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img,
                                             (int(scale * img.get_width()), int(scale * img.get_height())))  # Resize
                temp_list.append(img)  # ADD Frame to FLipBOOK
            self.animation_list.append(temp_list)  # list inside list  (Append flipBook in the FlipBooks list)

        self.image = self.animation_list[self.action][
            self.frame_index]  # just to draw the rect   (index here = 0 , so 1st frame)

        # RECTANGLE
        self.rect = self.image.get_rect()  # Creating the Player's RECTANGLE Using the Image SIZE
        self.rect.center = (x, y)  # Rectangle Starting Coordinates (the same as the player)

        self.width = self.image.get_width() - 15
        self.height = self.image.get_height()

        # -------------- Movement Function---------------------
    def move(self, moving_left, moving_right):
        # soldier's position (reset player's movement)
        screen_scroll = 0
        dx = 0  # THE COORDINATES VARIATION (when moving)
        dy = 0

        if dy != 0 and (
                self.char_type == 'enemy' or self.char_type == 'zombie1' or self.char_type == 'zombie2' or self.char_type == 'spider'):
            self.can_ai = False
        else:
            self.can_ai = True
        #       assign movement if moving left or right
        # Player
        if self.char_type == 'player':
            if self.is_sliding == False:
                if aim_crouch == False and crouch == False:
                    if moving_left:  # Move Left
                        dx = -self.speed
                        self.direction = -1
                        self.flip = True  # Flip the original sprite

                    if moving_right:  # Move Right
                        dx = self.speed
                        self.direction = 1
                        self.flip = False  # Original sprite without flipping
                else:  # if crouch == true     (JUST FLIP PLAYER without moving)
                    if moving_left:
                        self.direction = -1
                        self.flip = True
                    if moving_right:
                        self.direction = 1
                        self.flip = False
                # Enemy
        elif (self.char_type == 'zombie1' or self.char_type == 'spider') and self.hit == False:
            if moving_left:  # Move Left
                dx = -self.speed
                self.flip = True  # Flip the original sprite
                self.direction = -1
            if moving_right:  # Move Right
                dx = self.speed
                self.flip = False  # Original sprite without flipping
                self.direction = 1

        elif self.char_type != 'zombie1':  # other enemies
            if moving_left:  # Move Left
                dx = -self.speed
                self.flip = True  # Flip the original sprite
                self.direction = -1
            if moving_right:  # Move Right
                dx = self.speed
                self.flip = False  # Original sprite without flipping
                self.direction = 1
        #               SLIDE
        if self.slide == True and self.is_sliding == False and self.in_air == False and self.char_type == 'player':
            self.vel_x = self.direction * self.speed * 2
            self.slide = False
            self.is_sliding = True
            if self.stamina <= 0:
                self.stamina = 0
            else:
                self.stamina -= 50
            # APPLY FRACTION
        self.vel_x -= self.direction * FRACTION
        if self.is_sliding:
            dx += self.vel_x
        if player.direction == 1:  # Right
            if self.vel_x < 0:
                self.vel_x = 0
                self.is_sliding = False
        else:  # Left
            if self.vel_x > 0:
                self.vel_x = 0
                self.is_sliding = False
        #                JUMP
        if self.jump == True and self.in_air == False and self.is_sliding == False:
            if self.char_type == 'player':
                self.vel_y = -8  # (up) negative Cz the 0 coordinate is on the top   THe jump_beginning Speed
                self.stamina -= 25
                run_fx.stop()
            elif self.char_type == 'dog':
                self.vel_y = -6.4
            self.jump = False
            self.in_air = True
        #           APPLY GRAVITY
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
            run_fx.stop()
        dy += self.vel_y
        # falling animation for player
        if self.char_type == 'player' and self.vel_y > 2:
            if shoot:
                if self.weapon == 'gun':
                    self.update_action(24)  # shooting
                else:
                    self.update_action(25)
            else:
                self.update_action(5)  # normal fall

        #            CHECK COLLISIONS
        for tile in world.obstacle_list:
            # x Collision     (hit a wall)
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width,self.height):
                dx = 0  # stop the player
                if (self.char_type == 'enemy') or (self.char_type == 'zombie1') or (self.char_type == 'zombie2') or (self.char_type == 'spider'):
                    self.direction *= -1
                    self.move_counter = 0

            # y Collision     (hit a floor/ground)
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:  # Check if below ground (jump)
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top  # the few difference
                elif self.vel_y >= 0:  # Check if above ground (falling)
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom  # the few difference

        for box in box_group:
            # x Collision     (hit a wall)
            if box.rect.colliderect(self.rect.x + dx, self.rect.y, self.width,self.height):
                dx = 0  # stop the player
                if (self.char_type == 'enemy') or (self.char_type == 'zombie1') or (self.char_type == 'zombie2') or (
                        self.char_type == 'spider'):  # the enemy turns around when he hits a wall
                    self.direction *= -1
                    self.move_counter = 0

            # y Collision     (hit a floor/ground)
            if box.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:  # Check if below ground (jump)
                    self.vel_y = 0
                    dy = box.rect.bottom - self.rect.top  # the few difference
                elif self.vel_y >= 0:  # Check if above ground (falling)
                    self.vel_y = 0
                    self.in_air = False
                    dy = box.rect.top - self.rect.bottom  # the few difference

        for stairs in stairs_group:
            # x Collision     (hit a wall)
            if stairs.rect.colliderect(self.rect.x + dx, self.rect.y, self.width,self.height):
                if abs(dx) > 0:
                    dx = 1.7
                    dy -= 10
                if (self.char_type == 'enemy') or (self.char_type == 'zombie1') or (self.char_type == 'zombie2') or (
                        self.char_type == 'spider'):  # the enemy turns around when he hits a wall
                    self.direction *= -1
                    self.move_counter = 0
            # y Collision     (hit a floor/ground)
            if stairs.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:  # Check if below ground (jump)
                    self.vel_y = 0
                    dy = stairs.rect.bottom - self.rect.top  # the few difference
                elif self.vel_y >= 0:  # Check if above ground (falling)
                    self.vel_y = 0
                    self.in_air = False
                    dy = stairs.rect.top - self.rect.bottom  # the few difference

        #      CHECK for Collision with Water
        if pygame.sprite.spritecollide(self, water_group, False) and self.slide == False and self.is_sliding == False:
            self.health -= 2.5
            blood = Blood(self.rect.centerx + self.direction * 20, self.rect.y, False, 'player')
            blood_group.add(blood)
        #      CHECK for Collision with Exit    (Clear Level)
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True
        #       CHECK if Fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0
        #      CHECK if going off the edge of screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:  # 1: start          2: ending
                dx = 0  # stop the player
        #     UPDATE RECTANGLE POSITION (MOVING THE PLAYER)
        self.rect.x += dx
        self.rect.y += dy
        #     UPDATE Scroll based on PLayer Position
        if self.char_type == "player":  # check the beginning of level
            if self.is_sliding:  # Sliding
                if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < world.level_length * TILE_SIZE - SCREEN_WIDTH) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                    if self.direction == -1:
                        dx = - self.speed * 2
                    else:
                        dx = self.speed * 1
                    self.rect.x -= dx
                    screen_scroll = -dx
                    # Running
            else:
                if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < world.level_length * TILE_SIZE - SCREEN_WIDTH) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                    self.rect.x -= dx
                    screen_scroll = -dx  # EQUAL TO PLAYER SPEED

        return screen_scroll, level_complete

        # ------------ SHOOTING FUNCTION -----------
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0 and self.is_sliding == False:
            if self.char_type == 'spider':
                self.shoot_cooldown = 70
            elif self.char_type == 'enemy':
                self.shoot_cooldown = 75
            else:
                self.ammo -= 1  # Reduce Ammo
                if self.weapon == 'gun':
                    self.shoot_cooldown = 34  # CONTROL THE SHOOTING SPEED
                elif self.weapon == 'submachine':
                    self.shoot_cooldown = 7  # CONTROL THE SHOOTING SPEED
            if self.char_type == 'player':
                if aim_crouch:
                    if self.weapon == 'gun':
                        self.update_action(10)
                        offset = 5
                    elif self.weapon == 'submachine':
                        self.update_action(21)
                        offset = -5
                else:
                    if self.weapon == 'gun':
                        if moving_left == False and moving_right == False:
                            self.update_action(4)
                        offset = 20
                    elif self.weapon == 'submachine':
                        if moving_left == False and moving_right == False:
                            self.update_action(18)
                        offset = 10
            else:
                offset = 0  # enemy

                # Spark from weapon
            flip = False
            if self.direction == 1:
                flip = True
            spark = Spark(self.rect.centerx + self.direction * 47, player.rect.centery - offset, flip, 1, 'shot',
                          self.char_type)
            spark_group.add(spark)
            # Bullet
            if self.char_type == 'spider':
                bullet = Bullet(self.rect.centerx + self.direction * (0.7 * self.rect.size[0]), self.rect.centery,
                                self.direction, 'spider_bullet', self.dmg)

            else:  # player or enemy
                bullet = Bullet(self.rect.centerx + self.direction * (0.1 * self.rect.size[0]),
                                self.rect.centery - offset, self.direction, f'{self.char_type}_bullet',
                                self.dmg)  # If shoot: create a Bullet instance     size[0] means the width (x)
                if self.weapon == 'gun':
                    shot1_fx.play()
                elif self.weapon == 'submachine' and self.audio_cooldown == 0:
                    shot3_fx.play()
                # self.audio_cooldown = 5
            if self.char_type == 'player':
                bullet_player_group.add(bullet)
            else:
                bullet_enemy_group.add(bullet)  # Append the bullet to sprite group

                # ------------ ZOMBIE ATTACK FUNCTION ---------------

    def zombie_attack(self):
        if self.attack_cooldown == 0 and player.is_sliding == False and self.hit == False and self.can_shoot:
            if self.char_type == 'zombie1':
                self.attack_cooldown = 100
            else:
                self.attack_cooldown = 100
            self.update_action(4)
            if abs(self.rect.centerx - player.rect.centerx) <= 200 and player.rect.bottom == self.rect.bottom:
                pygame.event.post(pygame.event.Event(PLAYER_HIT))
                player.health -= self.dmg - player.defense
                # Add Blood
                if player.direction == 1:
                    flip = True
                else:
                    flip = False
                blood = Blood(player.rect.centerx - (player.image.get_width() // 2 - 70) * self.direction,
                              self.rect.centery, flip, 'player')
                blood_group.add(blood)

                # ------------ AI FUNCTION -----------   (Enemies)
    def enemy_ai(self):
        if self.in_air == True:
            self.move(False, False)
        elif self.alive and player.alive and self.can_ai and self.in_air == False:
            distancex = player.rect.centerx - self.rect.centerx
            distancey = player.rect.centery - self.rect.centery
            if abs(distancex) <= 850 and abs(distancey) <= 50:
                if distancex <= -700:  # Right move
                    self.move(True, False)
                    self.update_action(1)
                elif distancex < 0:  # Right shoot
                    self.direction = -1
                    self.flip = True
                    self.shoot()
                    self.update_action(0)
                elif distancex < 700 and distancex > 0:  # Left shoot
                    self.flip = False
                    self.direction = 1
                    self.shoot()
                    self.update_action(0)
                elif distancex >= 500:  # Left move
                    self.move(False, True)
                    self.update_action(1)
            elif random.randint(1, 200) == 1 and self.idling == False:  # IDLE
                self.update_action(0)
                self.idling = True  # Enemy stops Randomly
                self.idle_counter = 50  # countdown until 0: continue running
            else:
                if self.idling == False:  # RUN
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1  # counter to flip the direction
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1  # instead of reset on 0
                else:
                    self.idle_counter -= 1
                    if self.idle_counter <= 0:
                        self.idling = False  # Continue Running
        self.rect.x += screen_scroll

        # ------------ ZOMBIE1 AI FUNCTION -----------
    def zombie1(self):
        if self.in_air == True:
            self.move(False, False)
        elif self.alive and player.alive and self.can_ai:
            distancex = player.rect.centerx - self.rect.centerx
            distancey = player.rect.centery - self.rect.centery
            if abs(distancex) <= 850 and abs(distancey) <= 70:
                if self.done == False:
                    if random.randint(1, 2) == 1:
                        zombie4_fx.play()
                    else:
                        zombie6_fx.play()
                    self.done = True
                if distancex <= -40:  # Left move
                    self.move(True, False)
                    self.update_action(1)
                elif distancex <= 0:  # Left shoot
                    self.direction = -1
                    self.zombie_attack()
                elif distancex < 40 and distancex > 0:  # Right shoot
                    self.direction = 1
                    self.zombie_attack()
                elif distancex >= 40:  # Right move
                    self.move(False, True)
                    self.update_action(1)
            elif random.randint(1, 100) == 1 and self.idling == False:  # IDLE
                self.update_action(0)
                self.idling = True  # Enemy stops Randomly
                self.idle_counter = 200  # countdown until 0: continue running
            else:
                if self.idling == False:  # RUN
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1  # counter to flip the direction
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1  # instead of reset on 0
                else:
                    self.idle_counter -= 1
                    if self.idle_counter <= 0:
                        self.idling = False  # Continue Running
        self.rect.x += screen_scroll

        # ------------ ZOMBIE2 AI FUNCTION -----------
    def zombie2(self):
        if self.in_air == True:
            self.move(False, False)
        elif self.alive and player.alive and self.can_ai:
            distancex = player.rect.centerx - self.rect.centerx
            distancey = player.rect.centery - self.rect.centery
            if abs(distancex) <= 850 and abs(distancey) <= 80:
                if self.done == False:
                    if random.randint(1, 2) == 1:
                        zombie5_fx.play()
                    else:
                        zombie6_fx.play()
                    self.done = True
                self.speed += 0.038
                if self.speed >= 6.35:
                    self.speed = 6.35
                if distancex <= -85:  # Left move
                    self.move(True, False)
                    self.update_action(1)
                elif distancex <= -70:  # attack while moving near
                    self.move(True, False)
                    self.zombie_attack()
                    self.speed = 2.5
                elif distancex < 0:  # Left shoot
                    self.direction = -1
                    self.zombie_attack()
                elif distancex < 70 and distancex > 0:  # Right shoot
                    self.direction = 1
                    self.zombie_attack()
                elif distancex >= 85:  # Right move
                    self.move(False, True)
                    self.update_action(1)
                elif distancex >= 70:  # attack while moving near
                    self.move(False, True)
                    self.zombie_attack()
                    self.speed = 2.5
            elif random.randint(1, 100) == 1 and self.idling == False:  # IDLE
                self.update_action(0)
                self.idling = True  # Enemy stops Randomly
                self.idle_counter = 200  # countdown until 0: continue running
            else:
                self.speed = 2
                if self.idling == False:  # RUN
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1  # counter to flip the direction
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1  # instead of reset on 0
                else:
                    self.idle_counter -= 1
                    if self.idle_counter <= 0:
                        self.idling = False  # Continue Running
        self.rect.x += screen_scroll

        # ------------SPIDER AI FUNCTION -------------
    def spider_ai(self):
        if self.in_air == True:
            self.move(False, False)
        elif self.alive and player.alive and (self.char_type == 'spider'):
            distancex = player.rect.centerx - self.rect.centerx
            distancey = player.rect.centery - self.rect.centery
            if abs(distancex) <= 1200 and abs(distancey) <= 300:
                if distancex <= -800:  # Left move
                    self.move(True, False)
                    self.update_action(1)
                    if self.throw_cooldown == 0:
                        grenade = Grenade(self.rect.centerx + self.direction * (0.2 * self.rect.size[0]),
                                          player.rect.top - 40, self.direction, 'spider_grenade', abs(distancex / 60))
                        grenade_group.add(grenade)
                        self.throw_cooldown = 100
                elif distancex <= -400 and self.throw_cooldown == 0:  # Left throw grenade
                    grenade = Grenade(self.rect.centerx + self.direction * (0.2 * self.rect.size[0]),
                                      player.rect.top - 40, self.direction, 'spider_grenade', abs(distancex / 60))
                    grenade_group.add(grenade)
                    self.update_action(4)
                    self.throw_cooldown = 100
                    if self.shoot_cooldown == 0:
                        self.shoot()
                        self.shoot_cooldown = 200
                elif distancex < 0 and distancex > -400:  # Left shoot
                    self.direction = -1
                    self.flip = True
                    self.shoot()
                    self.update_action(4)
                if distancex == 0:
                    player.health -= 10
                elif distancex < 400 and distancex > 0:  # Right shoot
                    self.flip = False
                    self.direction = 1
                    self.shoot()
                    self.update_action(4)
                elif distancex <= 800 and self.throw_cooldown == 0:  # Right throw grenade
                    grenade = Grenade(self.rect.centerx + self.direction * (0.2 * self.rect.size[0]),
                                      player.rect.top - 40, self.direction, 'spider_grenade', abs(distancex / 60))
                    grenade_group.add(grenade)
                    self.update_action(4)
                    self.throw_cooldown = 100
                    if self.shoot_cooldown == 0:
                        self.shoot()
                        self.shoot_cooldown = 200
                elif distancex > 800:  # Right move
                    self.move(False, True)
                    self.update_action(1)

            elif random.randint(1, 200) == 1 and self.idling == False:  # IDLE
                self.update_action(0)
                self.idling = True  # Enemy stops Randomly
                self.idle_counter = 50  # countdown until 0: continue running
            else:
                if self.idling == False:  # RUN
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1  # counter to flip the direction
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1  # instead of reset on 0
                else:  # idling = true        IDLE   COUNTDOWN
                    self.idle_counter -= 1
                    if self.idle_counter <= 0:
                        self.idling = False  # Continue Running
        self.rect.x += screen_scroll

        # ------------ DOG AI FUNCTION -----------
    def dog_ai(self):
        player_is_crouching = False
        if player.direction == 1:
            flip = True
        else:
            flip = False
        if self.in_air == True and self.attacking == False:
            self.move(False, False)
        elif self.alive and (self.char_type == 'dog'):
            distancex = player.rect.centerx - self.rect.centerx
            distancey = player.rect.centery - self.rect.centery
            if abs(distancex) <= 1500 and abs(distancey) <= 500:
                if self.done == False:
                    if random.randint(1, 2) == 1:
                        dog1_fx.play()
                    else:
                        dog3_fx.play()
                    self.done = True
                if distancex <= -300 and self.attacking == False and self.attack_cooldown == 0:  # Left move         [-700 , -300]
                    self.move(True, False)
                    self.update_action(1)
                    self.speed += 0.08
                elif distancex < 0 and self.attacking == False:  # Left jump       [-300, 0]
                    if random.randint(0, 1) == 0:
                        dog2_fx.play()
                    if not (crouch) and not (aim_crouch):
                        self.jump = True
                        player_is_crouching = False
                        self.update_action(2)
                    else:  # player is crouching
                        self.update_action(1)
                        player_is_crouching = True
                        if self.rect.colliderect(player.rect):  # Attack in ground
                            player.health -= self.dmg - player.defense
                            pygame.event.post(pygame.event.Event(PLAYER_HIT))
                            blood = Blood(player.rect.centerx - (player.image.get_width() // 2 - 70) * self.direction,
                                          self.rect.centery, flip, 'player')
                            blood_group.add(blood)
                    self.speed = 18
                    self.attacking = True
                    self.attack_cooldown = 150
                elif distancex <= 300 and self.attacking == False:  # right jump        [0, 300]
                    self.update_action(2)
                    if random.randint(0, 2) == 1:
                        dog2_fx.play()
                    if not (crouch) and not (aim_crouch):
                        self.jump = True
                        player_is_crouching = False
                    else:  # player is crouching
                        self.update_action(1)
                        player_is_crouching = True
                        if self.rect.colliderect(player.rect):  # Attack in ground
                            player.health -= self.dmg - player.defense
                            pygame.event.post(pygame.event.Event(PLAYER_HIT))
                            blood = Blood(player.rect.centerx - (player.image.get_width() // 2 - 70) * self.direction,
                                          self.rect.centery, flip, 'player')
                            blood_group.add(blood)
                        for box in box_group:
                            if self.rect.colliderect(box.rect):
                                box.destroyed = True
                    self.speed = 18
                    self.attacking = True
                    self.attack_cooldown = 150
                elif distancex > 300 and self.attacking == False and self.attack_cooldown == 0:  # right move       [300, 700]
                    self.move(False, True)
                    self.update_action(1)
                    self.speed += 0.08
                elif self.attacking:  # Attack in air
                    if self.rect.colliderect(
                            player.rect) and player_is_crouching == False and player.is_sliding == False:
                        player.health -= self.dmg - player.defense
                        pygame.event.post(pygame.event.Event(PLAYER_HIT))
                        blood = Blood(player.rect.centerx - (player.image.get_width() // 2 - 70) * self.direction,
                                      self.rect.centery, flip, 'player')
                        blood_group.add(blood)
                    self.speed -= 0.25
                    if self.direction == -1:
                        self.move(True, False)
                    else:
                        self.move(False, True)
                    if self.speed <= 0:
                        self.speed = 0
                        self.update_action(0)
                        self.attacking = False
                        if self.direction == -1:
                            self.move(False, True)
                        else:
                            self.move(True, False)

                    for box in box_group:
                        if self.rect.colliderect(box.rect):
                            box.destroyed = True
            elif random.randint(1, 150) == 1 and self.idling == False:  # IDLE
                self.update_action(0)
                self.idling = True  # Enemy stops Randomly
                self.idle_counter = 50  # countdown until 0: continue running
            else:
                self.speed = 3
                if self.idling == False:  # RUN
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(6)
                    self.move_counter += 1  # counter to flip the direction
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1  # instead of reset on 0
                else:  # idling = true        IDLE   COUNTDOWN
                    self.idle_counter -= 1
                    if self.idle_counter <= 0:
                        self.idling = False  # Continue Running
        self.rect.x += screen_scroll

        # THE ANIMATION FUNCTION      ---------[To change the frames of flipBook]-------IT DOESN'T DRAW IT JUST CHANGES the Image USED IN DRAW FUNCTION --------

    def update_animation(self):  # Timer    # to update the flipBook images (FRAMES)    [TO change the frames]
        ANIMATION_COOLDOWN = 95  # 100 ms to update the frame       CONTROL THE ANIMATION SPEED
        if self.char_type == 'player' and (
                self.action == 1 or self.action == 8 or self.action == 22):  # Run animation for player
            ANIMATION_COOLDOWN = 65
        elif self.char_type == 'player' and self.action == 0:
            ANIMATION_COOLDOWN = 110
        elif self.char_type == 'zombie1' and (self.action == 4 or self.action == 18):
            ANIMATION_COOLDOWN = 50
        elif self.char_type == 'zombie2':
            if (self.action == 4 or self.action == 18):
                ANIMATION_COOLDOWN = 50
            else:
                ANIMATION_COOLDOWN = 70
        elif self.char_type == 'dog':
            if self.action == 0:
                ANIMATION_COOLDOWN = 110
            if self.action == 1 or self.action == 2 or self.action == 12:
                ANIMATION_COOLDOWN = 55
            elif self.action == 6:
                ANIMATION_COOLDOWN = 90
        # Update Image depending on current frame (current index)
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed (to update frame) since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:  # time to pass to other frame
            self.update_time = pygame.time.get_ticks()  # Reset (update) the timer to recalculate the passed time again
            self.frame_index += 1
        # Looping & Unlooping   (when index > the number of frames(5) it LOOPS from 0)
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.char_type == 'player' and self.action == 4:
                self.update_action(7)
            elif self.char_type == 'player' and self.action == 10:
                self.update_action(9)
            elif (self.char_type == 'player' and (self.action == 12 or self.action == 17 or self.action == 23)):
                self.frame_index = len(self.animation_list[self.action]) - 1
            elif (self.char_type == 'zombie1' or self.char_type == 'zombie2' or self.char_type == "enemy") and self.action == 12:
                self.update_action(0)
            elif self.action == 3 or (self.action == 6 and (
                    self.char_type != 'dog')) or self.action == 16 or self.action == 12:  # Case of: Unlooping Animations (death & aim & Shoot)
                self.frame_index = len(self.animation_list[self.action]) - 1
            elif (self.char_type == 'zombie1' or self.char_type == 'zombie2') and (
                    self.action == 4 or self.action == 18):
                self.update_action(0)
            elif self.char_type == 'dog' and self.action == 2:
                self.update_action(1)

            else:  # Case of : Looping Animations
                self.frame_index = 0

                # THE ACTION (flipBook type) Function -----------[To change the flipBook type(idle, run, jump...)]--------------
    def update_action(self, new_action):
        # Check if the current action is different then the previous one
        if new_action != self.action:  # if the action has changed
            self.action = new_action
            # Reset(update) the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

            # Death Function
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0  # To stop the soldier when he dies
            self.alive = False
            self.update_action(3)
            if (self.char_type == 'enemy' or self.char_type == 'zombie1' or self.char_type == 'zombie2' or self.char_type == 'spider' or self.char_type == 'dog') and self.lost_item == False:
                gold = ItemBox('Gold', self.rect.centerx, self.rect.centery - 17, self.gold, -2)
                item_box_group.add(gold)
                self.lost_item = True  # Enemy lost his item
                player.points += 20
                if self.char_type == 'zombie1':
                    zombie1_fx.play()
                    zombie5_fx.play()
                elif self.char_type == 'zombie2':
                    zombie1_fx.play()
                    zombie6_fx.play()
                elif self.char_type == 'dog':
                    zombie1_fx.play()
                if player.points >= player.level_up:
                    levelup.play()
                    player.level += 1
                    player.level_up *= 2.5
                    player.dmg += 2
                    player.defense += 1.3
                if arcade:
                    player.time += self.gold / 4
                    if player.time >= player.max_time:
                        player.time = player.max_time
            if self.disappear_counter > 0:
                self.disappear_counter -= 1
            else:
                self.kill()

        elif self.health >= 100:
            self.health = 100

            # Update_animation + Update CoolDown + Check_Alive
    def update(self):
        self.update_animation()
        self.check_alive()
        # UPDATE COOLDOWN
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1
        if self.audio_cooldown > 0:
            self.audio_cooldown -= 1

            # Drawing Soldier Function
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),self.rect)  # flip: TO FLIP THE SPRITE WHEN WE CHANGE DIRECTION

# _________________________________________________________________________________________________________________________
healthbar_group = []

# WORLD CLASS
class World():
    def __init__(self):
        self.obstacle_list = []  # (not all tiles are obstacles)    (only earth tiles (0 to 8)
    def process_data(self,data):  # take the world data (tiles values) & turn it (convert) into something that the game can use (level)
        self.level_length = len(data[0])  # level length depends on the columns number  (0 or 1 or 2 or .. doesn't matter)        level length = columns number * TILE SIZE
        index = 0
        # lst = []
        for y, row in enumerate(
                data):  # iterate through each value in level data file (iterate in the Grid through tiles values )
            for x, tile in enumerate(row):  # iterate through rows
                # DRAW TILES (DEPENDING ON THE CONTAINED VALUE)
                if tile >= 0:  # to avoid empty tiles (-1)
                    img = img_list[tile].convert_alpha()
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if (tile >= 0 and tile <= 8) or tile == 30:  # Obstacles (earth)
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10 or tile == 33 or tile == 34:  # water
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile == 11 or tile == 13 or tile == 14 or tile == 37 or tile == 38:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE, '')
                        decoration_group.add(decoration)
                    elif tile == 35:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE, 'dead')
                        decoration_group.add(decoration)
                    elif tile == 12:
                        img = pygame.transform.scale(img, (70, 70)).convert_alpha()
                        box = Box(img, x * TILE_SIZE, y * TILE_SIZE)  # BOX & (obstacle)
                        box_group.add(box)
                    elif tile == 15:  # CREATE PLAYER & Health Bar
                        if level == 1 or level == 0:
                            player = Soldier("player", x * TILE_SIZE, y * TILE_SIZE, 3.5, 6, 20, 100, 2, 0, 27, 0, 100)
                        elif level == 2:
                            player = Soldier("player", x * TILE_SIZE, y * TILE_SIZE, 3.5, 6, 0, 50, 0, 0, 27, 0, 0)
                    elif tile == 16:  # CREATE Enemy
                        enemy = Soldier("enemy", x * TILE_SIZE, y * TILE_SIZE, 2.8, 5, 70, 100, 0, 50, 9, 11, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:  # CREATE AMMO Box
                        item_box = ItemBox('Gun_Ammo', x * TILE_SIZE, y * TILE_SIZE, 0, -2)
                        item_box_group.add(item_box)
                    elif tile == 18:  # CREATE Grenade Box
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE, 0, -2)
                        item_box_group.add(item_box)
                    elif tile == 19:  # CREATE Health Box
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE, 0, -2)
                        item_box_group.add(item_box)
                    elif tile == 20:  # EXIT
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 21:  # ZOMBIE 1
                        zombie1 = Soldier("zombie1", x * TILE_SIZE, y * TILE_SIZE, 3.8, 2.6, 0, 100, 0, 20, 18, 10, 0)
                        zombie1_group.add(zombie1)
                    elif tile == 22:  # ZOMBIE 2
                        zombie2 = Soldier("zombie2", x * TILE_SIZE, y * TILE_SIZE, 3.73, 2, 0, 100, 0, 35, 16, 8, 0)
                        zombie2_group.add(zombie2)
                    elif tile == 23:
                        action_box = ItemBox('Action', x * TILE_SIZE, y * TILE_SIZE, 0, index)
                        item_box_group.add(action_box)
                        index += 1
                    elif tile == 24:
                        spider = Soldier("spider", x * TILE_SIZE, y * TILE_SIZE, 1, 2, 70, 100, 0, 65, 10, 20, 0)
                        spider_group.add(spider)
                    elif tile == 25:
                        dog = Soldier("dog", x * TILE_SIZE, y * TILE_SIZE, 3, 7, 70, 100, 0, 35, 1.2, 15, 0)
                        dog_group.add(dog)
                    elif tile == 26:
                        location_box = ItemBox('Location', x * TILE_SIZE, y * TILE_SIZE, 0, 0)
                        item_box_group.add(location_box)
                    elif tile == 27:
                        gun_box = ItemBox('Gun', x * TILE_SIZE, y * TILE_SIZE, 0, 0)
                        item_box_group.add(gun_box)
                    elif tile == 28:
                        submachine_box = ItemBox('Submachine', x * TILE_SIZE, y * TILE_SIZE, 0, 0)
                        item_box_group.add(submachine_box)
                    elif tile == 29:
                        item_box = ItemBox('Gold', x * TILE_SIZE, y * TILE_SIZE, 40, -2)
                        item_box_group.add(item_box)
                    elif tile == 31:
                        item_box = ItemBox('Submachine_Ammo', x * TILE_SIZE, y * TILE_SIZE, 0, -2)
                        item_box_group.add(item_box)
                    elif tile == 32:
                        img = pygame.transform.scale(img, (50, 25))
                        stairs = Stairs(img, x * TILE_SIZE, y * TILE_SIZE)  # BOX & (obstacle)
                        stairs_group.add(stairs)
                    elif tile == 36:
                        item_box = ItemBox('Key', x * TILE_SIZE, y * TILE_SIZE, 0, -2)
                        item_box_group.add(item_box)
        return player  # cz it is local (it should be global)
    def draw(self):  # Draw obstacles
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll  # 1: rectangle       0: x coordinate    TO SCROLL OBSTACLES
            screen.blit(tile[0], tile[1])


            # DECORATION CLASS
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = img
        if self.type == 'dead':
            self.image = pygame.transform.scale(self.image,
                                                (self.image.get_width() * 3, round(self.image.get_height() * 2)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height())

    def update(self):
        self.rect.x += screen_scroll  # SCROLL


        # WATER CLASS
class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        # self.rect = self.image.get_rect()
        # self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height())
        self.rect = pygame.rect.Rect(x, y, self.image.get_width() - 10, self.image.get_height() + 15)
    def update(self):
        self.rect.x += screen_scroll  # SCROLL
        # pygame.draw.rect(screen, RED, self.rect)


        # EXIT CLASS
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height())
    def update(self):
        self.rect.x += screen_scroll  # SCROLL


        # ITEMS CLASS + ACTION
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, value, index):  # item_type: string
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.value = value
        self.index = index
        self.image = item_boxes[item_type]  # item_boxes: items list   (Dictionary)
        self.x = x
        self.y = y
        if self.item_type == 'Location':
            self.rect = pygame.rect.Rect(self.x, 0, 500, SCREEN_HEIGHT)
        else:
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.text_counter1 = 400
        self.text_counter2 = 200
        self.text_counter3 = 70
        self.text_counter4 = 500
        self.collided = False
    def update(self):
        # Check If Collided with the PLAYER (only)
        if pygame.sprite.collide_rect(self, player) or self.collided:
            # check the item type
            if self.item_type == 'Health':
                player.health_kit += 1  # health shouldn't pass max health
                item_fx.play()
                self.kill()  # delete the item box
            if self.item_type == 'Gun_Ammo':
                player.ammo += 20
                item_fx.play()
                self.kill()  # delete the item box
            if self.item_type == 'Submachine_Ammo':
                player.ammo += 40
                item_fx.play()
                self.kill()  # delete the item box
            if self.item_type == 'Grenade':
                player.grenades += 2
                item_fx.play()
                self.kill()  # delete the item box
            if self.item_type == 'Gold':
                gold_fx.play()
                player.gold += self.value
                self.kill()
            if self.item_type == 'Submachine':
                player.have_submachine = True
                player.weapon = 'submachine'
                player.ammo += 60
                aim_fx.play()
                self.kill()
            if self.item_type == 'Gun':
                player.have_gun = True
                player.weapon = 'gun'
                player.ammo += 15
                aim_fx.play()
                self.kill()
            if self.item_type == 'Key':
                if self.collided == False:
                    item_fx.play()
                    self.collided = True
                player.have_key = True
                self.image = pygame.image.load('img/icons/key2.png').convert_alpha()
                if self.text_counter1 > 0:
                    self.text_counter1 -= 1
                    text_box("Let's get out of this madness", "", '')
                else:
                    self.kill()
            if self.item_type == 'Action':
                draw_text('Press  F', font, WHITE, player.rect.x - player.direction * 11, player.rect.y - 20)
                player.collide_action = True
                if msg_counter == 200:  # we can't change action until previous one ends
                    player.msg_index = self.index
                else:
                    player.collide_action = False
            if self.item_type == 'Location':
                if player.location_index == 0:
                    self.collided = True
                    if level == 1:
                        if self.text_counter2 > 0:
                            self.text_counter2 -= 1
                            draw_text('Shoot the Box', font, WHITE, 630, 250)
                            draw_text("Switch weapons using the number buttons", font, WHITE, 500, 350)
                        else:
                            self.kill()
                            player.location_index += 1
                    elif level == 2:
                        if self.text_counter1 > 0:
                            self.text_counter1 -= 1
                            draw_text("Slide or Roll to avoid the obstacles", font, WHITE, 500, 250)
                        else:
                            self.kill()
                            player.location_index += 1
                    elif level == 0:
                        self.collided = True
                        zombie1 = Soldier("zombie1", player.rect.centerx + 600, player.rect.centery, 3.8, 2, 0, 100, 0,
                                          15, 8, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie1", player.rect.centerx + 900, player.rect.centery, 3.8, 2, 0, 100, 0,
                                          15, 8, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie2 = Soldier("zombie2", player.rect.centerx + 2000, 50, 3.73, 2, 0, 100, 0, 25, 10, 8, 0)
                        zombie2_group.add(zombie2)
                        zombie1 = Soldier("zombie1", player.rect.centerx + 2400, player.rect.centery, 3.8, 2, 0, 100, 0,
                                          15, 8, 5, 0)
                        zombie1_group.add(zombie1)
                        spider = Soldier("spider", player.rect.centerx + 3600, player.rect.centery, 1, 2, 70, 100, 0,
                                         60, 10, 20, 0)
                        spider_group.add(spider)
                        self.kill()
                        player.location_index += 1

                elif player.location_index == 1:
                    self.collided = True
                    if level == 1:
                        if self.text_counter1 > 0:
                            self.text_counter1 -= 1
                            draw_text('Collect Coins to buy items', font, WHITE, 550, 250)
                            draw_text("Open shop from Escape button", font, WHITE, 530, 350)
                        else:
                            self.kill()
                            player.location_index += 1
                    elif level == 2:
                        if self.text_counter2 > 0:
                            self.text_counter2 -= 1
                            text_box("A human corpse !? ", "Maybe I'll find a way out if I go forward", '')
                        else:
                            self.kill()
                            player.location_index += 1

                elif player.location_index == 2:
                    if level == 1:
                        if self.text_counter1 > 0:
                            self.text_counter1 -= 1
                            draw_text("Dodge the enemy's attack by rolling or sliding", font, WHITE, 430, 240)
                        else:
                            self.kill()
                            player.location_index += 1
                    elif level == 2:
                        if self.collided == False:
                            zombie6_fx.play()
                            self.collided = True
                        if self.text_counter2 > 0:
                            self.text_counter2 -= 1
                            text_box("What was that ?", "Strange Area", '')
                        else:
                            if music_on:
                                pygame.mixer.music.play(1000, 0, 40000)
                            player.location_index += 1
                            self.kill()

                elif player.location_index == 3:
                    if level == 1:
                        self.collided = True
                        if self.text_counter1 > 0:
                            self.text_counter1 -= 1
                            text_box("Captain, Our soldiers are falling", "We don't know what we are facing",
                                     'Our chances are decreasing')
                        else:
                            self.kill()
                            player.location_index += 1
                    elif level == 2:
                        player.done = True
                        self.collided = True
                        self.kill()
                        player.location_index += 1

                elif player.location_index == 4:
                    if level == 1:
                        self.collided = True
                        dog2 = Soldier("dog", player.rect.x - 1100, 500, 3, 7, 70, 100, 0, 25, 0.82, 15, 0)
                        dog_group.add(dog2)
                        player.location_index += 1
                        self.kill()
                    elif level == 2:
                        player.done = True
                        player.lost_item = True
                        self.collided = True
                        self.kill()
                        player.location_index += 1
                elif player.location_index == 5:
                    if level == 1:
                        self.collided = True
                        dog1 = Soldier("dog", player.rect.x + 1200, 500, 3, 7, 70, 100, 0, 25, 0.85, 15, 0)
                        dog_group.add(dog1)
                        dog2 = Soldier("dog", player.rect.x - 1100, 500, 3, 7, 70, 100, 0, 25, 0.85, 15, 0)
                        dog_group.add(dog2)
                        self.kill()
                        player.location_index += 1
                    elif level == 2:
                        self.collided = True
                        if self.text_counter1 > 0:
                            self.text_counter1 -= 1
                            text_box("Is this a man-made !", "I have to find a way to reach the top", '')
                        else:
                            self.kill()
                            player.location_index += 1

                elif player.location_index == 6:
                    if level == 1:
                        self.collided = True
                        self.kill()
                        dog2 = Soldier("dog", player.rect.x - 1100, 500, 3, 7, 70, 100, 0, 25, 1.2, 15, 0)
                        dog_group.add(dog2)
                        player.location_index += 1
                    elif level == 2:
                        self.collided = True
                        self.kill()
                        zombie1 = Soldier("zombie1", player.rect.centerx + 600, player.rect.centery, 3.8, 2, 0, 100, 0,
                                          15, 8, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie1", player.rect.centerx + 800, player.rect.centery, 3.8, 2, 0, 100, 0,
                                          15, 8, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie1", player.rect.centerx + 1000, player.rect.centery, 3.8, 2, 0, 100, 0,
                                          15, 8, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie1", player.rect.centerx + 1200, player.rect.centery, 3.8, 2, 0, 100, 0,
                                          15, 8, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie1", player.rect.centerx - 850, player.rect.centery, 3.8, 2, 0, 100, 0,
                                          15, 8, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie1", player.rect.centerx - 800, player.rect.centery, 3.8, 2, 0, 100, 0,
                                          15, 8, 5, 0)
                        zombie1_group.add(zombie1)
                        player.location_index += 1

                elif player.location_index == 7:
                    if level == 1:
                        if self.text_counter2 > 0:
                            self.text_counter2 -= 1
                            if self.collided == False:
                                shot4_fx.play()
                            text_box('Shit ', "I have to move", '')
                        else:
                            self.kill()
                            player.location_index += 1
                        self.collided = True
                    elif level == 2:
                        self.collided = True
                        self.kill()
                        zombie1 = Soldier("zombie1", player.rect.centerx - 8500, 50, 3.8, 2.5, 0, 100, 0, 15, 9, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie1", player.rect.centerx - 8800, 50, 3.8, 2.5, 0, 100, 0, 15, 9, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie1", player.rect.centerx - 6000, 50, 3.8, 2.5, 0, 100, 0, 15, 9, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie1", player.rect.centerx - 5700, 50, 3.8, 2.5, 0, 100, 0, 15, 9, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie1", player.rect.centerx - 8000, 50, 3.8, 2.5, 0, 100, 0, 15, 9, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie1", player.rect.centerx - 6700, 50, 3.8, 2.5, 0, 100, 0, 15, 9, 5, 0)
                        zombie1_group.add(zombie1)

                        zombie2 = Soldier("zombie2", player.rect.centerx - 8500, 50, 3.73, 2, 0, 100, 0, 25, 10, 8, 0)
                        zombie2_group.add(zombie2)
                        zombie2 = Soldier("zombie2", player.rect.centerx - 8800, 50, 3.73, 2, 0, 100, 0, 25, 10, 8, 0)
                        zombie2_group.add(zombie2)
                        zombie2 = Soldier("zombie2", player.rect.centerx - 6500, 50, 3.73, 2, 0, 100, 0, 25, 10, 8, 0)
                        zombie2_group.add(zombie2)
                        zombie2 = Soldier("zombie2", player.rect.centerx - 8000, 50, 3.73, 2, 0, 100, 0, 25, 10, 8, 0)
                        zombie2_group.add(zombie2)
                        zombie1 = Soldier("zombie2", player.rect.centerx - 6700, 50, 3.65, 2, 0, 100, 0, 10, 10, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie2 = Soldier("zombie2", player.rect.centerx - 9500, 50, 3.73, 2, 0, 100, 0, 25, 10, 8, 0)
                        zombie2_group.add(zombie2)
                        zombie2 = Soldier("zombie2", player.rect.centerx - 10400, 50, 3.73, 2, 0, 100, 0, 25, 10, 8, 0)
                        zombie2_group.add(zombie2)
                        zombie1 = Soldier("zombie2", player.rect.centerx - 9800, 50, 3.65, 2, 0, 100, 0, 10, 10, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie2", player.rect.centerx - 10000, 50, 3.65, 2, 0, 100, 0, 10, 10, 5, 0)
                        zombie1_group.add(zombie1)
                        zombie1 = Soldier("zombie2", player.rect.centerx - 9000, 50, 3.65, 2, 0, 100, 0, 10, 10, 5, 0)
                        zombie1_group.add(zombie1)
                        player.location_index += 1

                elif player.location_index == 8:
                    if level == 1:
                        self.collided = True
                        if self.text_counter1 > 0:
                            self.text_counter1 -= 1
                            text_box('Captain we have a hard situation here', 'Another one down, strange creatures a..',
                                     "Captain ?..damn")
                        elif self.text_counter4 > 0:
                            self.text_counter4 -= 1
                            text_box('What the hell is happening here', 'Is this a human ?',
                                     "I am sure it's one of the organization's crimes")
                        elif self.text_counter2 > 0:
                            self.text_counter2 -= 1
                            text_box('The Front Gates are not far away',
                                     "But we must prepare for the guard's attack again", "")
                        else:
                            self.kill()
                            player.location_index += 1

        self.rect.x += screen_scroll  # SCROLL


        # Health Bar CLass
class HealthBar():
    def __init__(self, x, y, health, max_health, char_type, type):  # Type: health, stamina
        self.char_type = char_type
        self.type = type
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health, x):  # DRAW & UPDATE health bar           (WE DRAW 3 RECTANGLES: red, green, Black(borders))
        self.health = health  # update with new health (increased or decreased)
        if self.type == 'health':
            # Size is different between player  h bar and enemy h bar
            if self.char_type == 'player':
                pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 174, 14))
                pygame.draw.rect(screen, RED, (self.x, self.y, 170, 10))
                pygame.draw.rect(screen, GREEN, (self.x, self.y, 170 * (self.health / self.max_health), 10))

            if self.char_type == 'enemy':
                self.x = x  # TO FOLLOW THE ENEMY
                pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 47, 7))
                pygame.draw.rect(screen, RED, (self.x, self.y, 43, 3))
                pygame.draw.rect(screen, GREEN, (self.x, self.y, 43 * (self.health / self.max_health), 3))

        elif self.type == 'stamina':  # stamina (only for player)
            pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 174, 14))
            pygame.draw.rect(screen, BLUE2, (self.x, self.y, 170, 10))
            pygame.draw.rect(screen, BLUE1, (self.x, self.y, 170 * (self.health / self.max_health), 10))

        elif self.type == 'time':
            pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 204, 24))
            pygame.draw.rect(screen, YELLOW1, (self.x, self.y, 200, 20))
            pygame.draw.rect(screen, YELLOW2, (self.x, self.y, 200 * (self.health / self.max_health), 20))


            # STAIRS CLASS
class Stairs(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height())
        # self.rect = pygame.rect.Rect(self.x, self.y , self.image.get_width() , self.image.get_height())
        self.index = 0

    def update(self):
        self.rect.x += screen_scroll  # SCROLL
        pygame.draw.rect(screen, RED, self.rect)


        # BULLET CLASS
class Bullet(pygame.sprite.Sprite):  # sprite class
    def __init__(self, x, y, direction, type, dmg):  # types:   player_bullet   enemy_bullet  spider_bullet
        pygame.sprite.Sprite.__init__(self)
        self.dmg = dmg
        self.type = type
        if self.type == 'spider_bullet':
            self.image = spider_bullet_img  # Sprite
            self.speed = 15
        else:
            self.image = bullet_img  # Sprite
            if self.type == 'player_bullet':
                self.speed = 70
            else:
                self.speed = 23  # enemy bullet

        self.rect = self.image.get_rect()  # Rectangle
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):  # __________Move Bullet______________
        self.rect.x += (self.direction * self.speed) + screen_scroll  # +SCROLL

        # check if bullet has gone off screen
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()  # Remove the bullet if it has gone off screen

        # check collision with obstacles
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect) or tile[1].colliderect(self.rect.x - self.direction * 15, self.rect.y,
                                                                     self.image.get_width(), self.image.get_height()):
                # Add Spark
                flip = False
                if self.direction == -1:
                    flip = True
                spark = Spark(self.rect.centerx - (tile[0].get_width() // 2 - 7) * self.direction, self.rect.centery,
                              flip, 1.6, 'collision', '')
                spark_group.add(spark)

                self.kill()  # Remove Bullet

        # check collision with stairs
        for stairs in stairs_group:
            if stairs.rect.colliderect(self.rect) or stairs.rect.colliderect(self.rect.x - self.direction * 15,
                                                                             self.rect.y, self.image.get_width(),
                                                                             self.image.get_height()):
                # Add Spark
                flip = False
                if self.direction == -1:
                    flip = True
                spark = Spark(self.rect.centerx - (stairs.image.get_width() // 2) * self.direction, self.rect.centery,
                              flip, 1.6, 'collision', '')
                spark_group.add(spark)

                self.kill()  # Remove Bullet

        # Check Collision With Player
        if pygame.sprite.spritecollide(player, bullet_enemy_group, False) and not player.is_sliding and not crouch and not aim_crouch:
            if player.alive:
                # Add Blood
                flip = True  # Don't Flip blood
                if self.direction == -1:
                    flip = False  # Flip blood
                blood = Blood(self.rect.centerx - (player.image.get_width() // 2 - 24) * self.direction,
                              self.rect.centery, flip, 'player')
                blood_group.add(blood)

                self.kill()  # Remove the bullet if it collided with a soldier
                player.health -= self.dmg - player.defense  # DAMAGE

        # Check Collision With Enemy
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_player_group, False):
                if enemy.alive:
                    # Add Blood
                    flip = False  # Don't Flip blood
                    if self.direction == -1:
                        flip = True  # Flip blood
                    blood = Blood(self.rect.centerx + (player.image.get_width() // 2 + 7) * self.direction,
                                  self.rect.centery, flip, 'enemy')
                    blood_group.add(blood)
                    self.kill()  # Remove the bullet
                    if player.weapon == 'gun':
                        enemy.health -= self.dmg - enemy.defense  # DAMAGE
                    elif player.weapon == 'submachine':
                        enemy.health -= self.dmg - enemy.defense - 10
                    enemy.hit = True

        # Check Collision With Zombie1
        for zombie1 in zombie1_group:
            if pygame.sprite.spritecollide(zombie1, bullet_player_group, False) or pygame.sprite.spritecollide(zombie1,
                                                                                                               bullet_enemy_group,
                                                                                                               False):
                if zombie1.alive:
                    # Add Blood
                    flip = False  # Don't Flip blood
                    if self.direction == -1:
                        flip = True  # Flip blood
                    blood = Blood(self.rect.centerx + (player.image.get_width() // 2 + 5) * self.direction,
                                  self.rect.centery, flip, 'enemy')
                    blood_group.add(blood)
                    self.kill()  # Remove the bullet
                    if player.weapon == 'gun':
                        zombie1.health -= self.dmg - zombie1.defense  # DAMAGE
                    elif player.weapon == 'submachine':
                        zombie1.health -= self.dmg - zombie1.defense - 10

                    zombie1.hit = True

        # Check Collision With Zombie2
        for zombie2 in zombie2_group:
            if pygame.sprite.spritecollide(zombie2, bullet_player_group, False) or pygame.sprite.spritecollide(zombie2,
                                                                                                               bullet_enemy_group,
                                                                                                               False):
                if zombie2.alive:

                    # Add Blood
                    flip = False  # Don't Flip blood
                    if self.direction == -1:
                        flip = True  # Flip blood
                    blood = Blood(self.rect.centerx + (zombie2.image.get_width() // 2 - 30) * self.direction,
                                  self.rect.centery, flip, 'enemy')
                    blood_group.add(blood)

                    self.kill()  # Remove the bullet
                    if player.weapon == 'gun':
                        zombie2.health -= self.dmg - zombie2.defense  # DAMAGE
                    elif player.weapon == 'submachine':
                        zombie2.health -= self.dmg - zombie2.defense - 10

                    zombie2.hit = True

        # Check Collision With Spider
        for spider in spider_group:
            if pygame.sprite.spritecollide(spider, bullet_player_group, False) or pygame.sprite.spritecollide(spider,
                                                                                                              bullet_enemy_group,
                                                                                                              False):
                if spider.alive:
                    # Add Blood
                    flip = True  # Don't Flip blood
                    if self.direction == -1:
                        flip = False  # Flip blood
                    blood = Blood(self.rect.centerx - (spider.image.get_width() // 2 - 110) * self.direction,
                                  self.rect.centery, flip, 'spider')
                    blood_group.add(blood)
                    self.kill()  # Remove the bullet
                    if player.weapon == 'gun':
                        spider.health -= self.dmg - spider.defense  # DAMAGE
                    elif player.weapon == 'submachine':
                        spider.health -= self.dmg - spider.defense - 4.5

                    spider.hit = True

        # Check Collision With Dog
        for dog in dog_group:
            if pygame.sprite.spritecollide(dog, bullet_player_group, False):
                if dog.alive:

                    # Add Blood
                    flip = False  # Don't Flip blood
                    if self.direction == -1:
                        flip = True  # Flip blood
                    blood = Blood(self.rect.centerx + (player.image.get_width() // 2 + 7) * self.direction,
                                  self.rect.centery, flip, 'enemy')
                    blood_group.add(blood)

                    self.kill()  # Remove the bullet
                    if player.weapon == 'gun':
                        dog.health -= self.dmg - dog.defense  # DAMAGE
                    elif player.weapon == 'submachine':
                        dog.health -= self.dmg - dog.defense - 8


                        # BOX CLASS
class Box(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height())
        # self.rect = pygame.rect.Rect(self.x - 10, self.y, self.image.get_width() +  30, self.image.get_height() + 15)
        self.index = 0
        self.counter = 300
        self.destroyed = False
    def update(self):
        self.rect.x += screen_scroll  # SCROLL
        # Check Collision With Box
        for bullet in bullet_player_group:
            # if pygame.sprite.spritecollide(box, bullet_player_group, False):
            if self.rect.colliderect(bullet.rect) or self.rect.colliderect(bullet.rect.x - bullet.direction * 15,
                                                                           bullet.rect.y, bullet.image.get_width(),
                                                                           bullet.image.get_height()):
                bullet.kill()
                self.destroyed = True
                # Add spark
                flip = False
                if bullet.direction == -1:
                    flip = True
                spark = Spark(self.rect.centerx - (self.image.get_width() // 2 - 7) * bullet.direction,
                              self.rect.centery, flip, 1.6, 'collision', '')
                spark_group.add(spark)
                # Box Spark
        if self.destroyed:  # when a bullet collide with box
            self.image = box_spark[3]
            if self.index < len(box_spark):
                screen.blit(box_spark[self.index], (self.rect.centerx, self.rect.centery))
                self.index += 1
            else:
                x = random.randint(0, 10)
                if x % 2 == 0 and x < 5:
                    Gun_Ammo = ItemBox('Gun_Ammo', self.rect.x, self.rect.y + 20, 0, -2)
                    item_box_group.add(Gun_Ammo)
                elif x % 2 == 0 and x > 5:
                    Health = ItemBox('Health', self.rect.x, self.rect.y + 20, 0, -2)
                    item_box_group.add(Health)
                elif x % 2 != 0 and x < 5:
                    Grenade = ItemBox('Grenade', self.rect.x, self.rect.y + 20, 0, -2)
                    item_box_group.add(Grenade)
                elif x % 2 != 0 and x >= 5:
                    Gun_Ammo = ItemBox('Gun_Ammo', self.rect.x, self.rect.y + 20, 0, -2)
                    item_box_group.add(Gun_Ammo)

                self.kill()


        # GRENADE CLASS
class Grenade(pygame.sprite.Sprite):  # sprite class
    def __init__(self, x, y, direction, type, speed):  # speed: x speed
        pygame.sprite.Sprite.__init__(self)
        self.time = 100  # Explosion timer
        self.speed = speed  # Horizontal speed
        self.type = type
        if self.type == 'player_grenade' or self.type == 'enemy_grenade':
            self.image = grenade_img
            self.image = pygame.transform.scale(self.image, (19, 19))
            self.vel_y = -8
        else:  # spider type
            self.image = spider_grenade_img
            self.vel_y = -7  # Vertical speed   (it starts moving up (vel_y decreases) until it reaches the Peak (vel_y=0), then it starts moving down (vel_y ++))
        self.rect = self.image.get_rect()  # Rectangle
        self.rect.center = (x, y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    def update(self):  # __________Move Grenade______________
        #             apply gravity
        self.vel_y += GRAVITY * 1.3
        dx = self.speed * self.direction
        dy = self.vel_y

        #        update Rectangle Position (MOVING THE GRENADE)
        self.rect.x += dx + screen_scroll  # + SCROLL
        self.rect.y += dy

        # Spider Grenade
        if self.type == 'spider_grenade':

            if self.rect.colliderect(player.rect):
                player.health -= 20
                self.kill()
                spider_grenade_explosion = Explosion(self.rect.x, self.rect.y, 0.5,
                                                     'spider_explosion')  # Create an Explosion Instance for grenade
                explosion_group.add(spider_grenade_explosion)  # Add the explosion created to sprite group
            else:
                #            Check Collision with OBSTACLES
                for tile in world.obstacle_list:
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        spider_grenade_explosion = Explosion(self.rect.x, self.rect.y, 0.5, 'spider_explosion')
                        explosion_group.add(spider_grenade_explosion)
                        self.kill()
                    if tile[1].colliderect(self.rect.x, self.rect.y - 50, self.width, self.height):
                        self.kill()  # remove the grenade after explosion
                        spider_grenade_explosion = Explosion(self.rect.x, self.rect.y, 0.5, 'spider_explosion')
                        explosion_group.add(spider_grenade_explosion)

                        # DAMAGE to NEARBY Soldiers      (Check the distance (radius) not the Collision)        #Player
                        if abs(self.rect.centerx - player.rect.centerx) < 100 and abs(
                                self.rect.centery - player.rect.centery) < 50:
                            player.health -= 25
                            # Enemy
                        for enemy in enemy_group:
                            if abs(self.rect.centerx - enemy.rect.centerx) < 100 and abs(
                                    self.rect.centery - enemy.rect.centery) < 50:
                                enemy.health -= 25

                                # Soldier Grenade
        else:
            # check collision with enemies
            for zombie1 in zombie1_group:
                if self.rect.colliderect(zombie1.rect):
                    zombie1.health -= 100
                    grenade_fx.play()
                    self.kill()
                    explosion = Explosion(self.rect.x, self.rect.y, 0.5,
                                          'explosion')  # Create an Explosion Instance for grenade
                    explosion_group.add(explosion)
            for zombie2 in zombie2_group:
                if self.rect.colliderect(zombie2.rect):
                    zombie2.health -= 100
                    grenade_fx.play()
                    self.kill()
                    explosion = Explosion(self.rect.x, self.rect.y, 0.5,
                                          'explosion')  # Create an Explosion Instance for grenade
                    explosion_group.add(explosion)
            for enemy in enemy_group:
                if self.rect.colliderect(enemy.rect):
                    enemy.health -= 100
                    grenade_fx.play()
                    self.kill()
                    explosion = Explosion(self.rect.x, self.rect.y, 0.5,
                                          'explosion')  # Create an Explosion Instance for grenade
                    explosion_group.add(explosion)
            for dog in dog_group:
                if self.rect.colliderect(dog.rect):
                    dog.health -= 100
                    grenade_fx.play()
                    self.kill()
                    explosion = Explosion(self.rect.x, self.rect.y, 0.5,
                                          'explosion')  # Create an Explosion Instance for grenade
                    explosion_group.add(explosion)
            for spider in spider_group:
                if self.rect.colliderect(spider.rect):
                    spider.health -= 70
                    grenade_fx.play()
                    self.kill()
                    explosion = Explosion(self.rect.x, self.rect.y, 0.5,
                                          'explosion')  # Create an Explosion Instance for grenade
                    explosion_group.add(explosion)

            #            check collision with walls (with screen)                    (it bounces)
            if self.rect.right + dx > SCREEN_WIDTH or self.rect.left + dx < 0:
                self.direction *= -1
                dx = self.speed * self.direction / 1.3
            #            Check Collision with OBSTACLES            (like we did with the player)
            for tile in world.obstacle_list:
                # x collision                    (it bounces)
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    self.direction *= -1
                    dx = self.speed * self.direction
                # y collision
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    self.speed = 0
                    if self.vel_y < 0:  # Check if below ground (thrown up)
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    elif self.vel_y >= 0:  # Check if above ground (falling)
                        self.vel_y = 0
                        dy = tile[1].top - self.rect.bottom
            self.time -= 1
            if self.time <= 0:  # time to explode
                self.kill()  # remove the grenade after explosion
                grenade_fx.play()
                explosion = Explosion(self.rect.x, self.rect.y, 0.5,
                                      'explosion')  # Create an Explosion Instance for grenade
                explosion_group.add(explosion)  # Add the explosion created to sprite group
                # DAMAGE to NEARBY Soldiers      (Check the distance (radius) not the Collision)        #Player
                if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                        abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                    player.health -= 50
                if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 3 and \
                        abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 3:
                    player.health -= 25
                    # Enemy
                for enemy in enemy_group:
                    if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2.3 and \
                            abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2.3:
                        enemy.health -= 100
                    if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 3 and \
                            abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 3:
                        enemy.health -= 50
                        # zombie1
                for zombie1 in zombie1_group:
                    if abs(self.rect.centerx - zombie1.rect.centerx) < TILE_SIZE * 2 and \
                            abs(self.rect.centery - zombie1.rect.centery) < TILE_SIZE * 2:
                        zombie1.health -= 100
                    if abs(self.rect.centerx - zombie1.rect.centerx) < TILE_SIZE * 3 and \
                            abs(self.rect.centery - zombie1.rect.centery) < TILE_SIZE * 3:
                        zombie1.health -= 50
                        # zombie2
                for zombie2 in zombie2_group:
                    if self.rect.colliderect(zombie2.rect):
                        zombie2.health -= 100
                        self.kill()
                        explosion = Explosion(self.rect.x, self.rect.y, 0.5,
                                              'explosion')  # Create an Explosion Instance for grenade
                        explosion_group.add(explosion)
                    if abs(self.rect.centerx - zombie2.rect.centerx) < TILE_SIZE * 2 and \
                            abs(self.rect.centery - zombie2.rect.centery) < TILE_SIZE * 2:
                        zombie2.health -= 100
                    if abs(self.rect.centerx - zombie2.rect.centerx) < TILE_SIZE * 3 and \
                            abs(self.rect.centery - zombie2.rect.centery) < TILE_SIZE * 3:
                        zombie2.health -= 50
                for spider in spider_group:  # spider
                    if self.rect.colliderect(spider.rect):
                        spider.health -= 70
                        self.kill()
                        explosion = Explosion(self.rect.x, self.rect.y, 0.5,
                                              'explosion')  # Create an Explosion Instance for grenade
                        explosion_group.add(explosion)
                    if abs(self.rect.centerx - spider.rect.centerx) < TILE_SIZE * 2 and \
                            abs(self.rect.centery - spider.rect.centery) < TILE_SIZE * 2:
                        spider.health -= 50
                    if abs(self.rect.centerx - spider.rect.centerx) < TILE_SIZE * 3 and \
                            abs(self.rect.centery - spider.rect.centery) < TILE_SIZE * 3:
                        spider.health -= 25

                for dog in dog_group:  # dog
                    if self.rect.colliderect(dog.rect):
                        dog.health -= 100
                        self.kill()
                        explosion = Explosion(self.rect.x, self.rect.y, 0.5,
                                              'explosion')  # Create an Explosion Instance for grenade
                        explosion_group.add(explosion)
                    if abs(self.rect.centerx - dog.rect.centerx) < TILE_SIZE * 2.3 and \
                            abs(self.rect.centery - dog.rect.centery) < TILE_SIZE * 2.3:
                        dog.health -= 70
                    if abs(self.rect.centerx - dog.rect.centerx) < TILE_SIZE * 3 and \
                            abs(self.rect.centery - dog.rect.centery) < TILE_SIZE * 3:
                        dog.health -= 35

                for box in box_group:
                    if abs(self.rect.centerx - box.rect.centerx) < TILE_SIZE * 3 and abs(
                            self.rect.centery - box.rect.centery) < TILE_SIZE * 3:
                        box.destroyed = True


                        # EXPLOSION CLASS
class Explosion(pygame.sprite.Sprite):  # sprite class
    def __init__(self, x, y, scale, type):
        pygame.sprite.Sprite.__init__(self)
        # Animation       (Load all frames in the FlipBook)
        self.animation_images = []  # FlipBOOK
        self.type = type
        for num in range(1, 6):
            img = pygame.image.load(f'img/{type}/exp{num}.png').convert_alpha()  # Loading Frames
            if self.type == 'explosion':
                img = pygame.transform.scale(img, (
                    int(img.get_width() * 3.3 * scale), int(img.get_height() * 3.3 * scale))).convert_alpha()  # Resize
            else:
                img = pygame.transform.scale(img, (
                    int(img.get_width() * 2 * scale), int(img.get_height() * 2 * scale))).convert_alpha()
            self.animation_images.append(img)  # Add Frame to FlipBOOK
        self.frame_index = 0
        self.image = self.animation_images[
            self.frame_index].convert_alpha()  # Sprite          just to create the Rectangle
        self.rect = self.image.get_rect()  # Rectangle
        if self.type == 'explosion':
            self.rect.center = (x, y - 30)
        else:
            self.rect.center = (x, y)
        self.counter = 0  # Just like CoolDown (to switch between frames)
    def update(self):  # __________Move Explosion(Animation)______________
        EXPLOSION_SPEED = 4  # CONTROL animation speed
        self.counter += 1
        if self.counter >= EXPLOSION_SPEED:
            self.frame_index += 1
            self.counter = 0
            # if animation is complete: Deleted the explosion    (not looping)
            if self.frame_index >= len(self.animation_images):
                self.kill()
            else:
                self.image = self.animation_images[self.frame_index]

        self.rect.x += screen_scroll  # SCROLL


        # BLOOD CLASS
class Blood(pygame.sprite.Sprite):  # sprite class
    def __init__(self, x, y, flip, char_type):
        pygame.sprite.Sprite.__init__(self)
        self.flip = flip
        self.char_type = char_type
        # Animation       (Load all frames in the FlipBook)
        self.animation_images = []  # FlipBook
        for num in range(1, 4):
            img = pygame.image.load(f'img/blood/blood{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * 4), int(img.get_height() * 4))).convert_alpha()
            img = pygame.transform.flip(img, self.flip, False).convert_alpha()
            self.animation_images.append(img)
        self.frame_index = 0
        self.image = self.animation_images[self.frame_index].convert_alpha()
        self.rect = self.image.get_rect()  # Rectangle
        self.rect.center = (x, y)
        self.counter = 0
    def update(self):  # Blood  ANIMATION
        ANIMATION_SPEED = 4
        self.counter += 1
        if self.counter >= ANIMATION_SPEED:
            self.frame_index += 1
            self.counter = 0
            # if animation is complete: Deleted the Blood
            if self.frame_index >= len(self.animation_images):
                self.kill()
            else:
                self.image = self.animation_images[self.frame_index]
        self.rect.x += screen_scroll


        # SPARK CLASS                   2 TYPES:   shot spark, spark from collision with obstc
class Spark(pygame.sprite.Sprite):  # sprite class
    def __init__(self, x, y, flip, speed, type, char_type):  # types     collision , shot
        pygame.sprite.Sprite.__init__(self)  # Char_type:  to know who to follow
        self.char_type = char_type
        self.type = type
        self.speed = speed
        self.flip = flip
        # Animation       (Load all frames in the FlipBook)
        self.animation_images = []  # FlipBook
        if self.type == 'shot':
            for num in range(1, 4):
                img = pygame.image.load(f'img/sparkshot/spark{num}.png').convert_alpha()  # Loading frames
                img = pygame.transform.scale(img, (
                    int(img.get_width() * 0.8), int(img.get_height() * 0.8))).convert_alpha()  # Resize
                img = pygame.transform.flip(img, self.flip, False).convert_alpha()  # Flip
                self.animation_images.append(img)  # Add Frame to FlipBOOK
        elif self.type == 'collision':
            for num in range(1, 7):
                img = pygame.image.load(f'img/sparkcollision/spark{num}.png').convert_alpha()  # Loading frames
                img = pygame.transform.scale(img, (
                    int(img.get_width() * 4), int(img.get_height() * 4))).convert_alpha()  # Resize
                img = pygame.transform.flip(img, self.flip, False).convert_alpha()  # Flip
                self.animation_images.append(img)  # Add Frame to FlipBOOK
        self.frame_index = 0
        self.image = self.animation_images[self.frame_index].convert_alpha()
        self.rect = self.image.get_rect()  # Rectangle
        self.rect.center = (x, y)
        self.counter = 0
    def update(self):  # Spark  ANIMATION
        self.counter += 1
        if self.counter >= self.speed:
            self.frame_index += 1
            self.counter = 0
            # if animation is complete: Deleted the Spark
            if self.frame_index >= len(self.animation_images):
                self.kill()
            else:
                self.image = self.animation_images[self.frame_index]
        # player
        if self.type == 'shot' and self.char_type == 'player' and aim_crouch:
            if player.weapon == 'gun':
                offset = 5
            elif player.weapon == 'submachine':
                offset = - 3
            self.rect.center = (player.rect.centerx + player.direction * 50,
                                player.rect.centery - offset)  # to keep following the Player shot
        elif self.type == 'shot' and self.char_type == 'player':  # aim_c = false
            if player.weapon == 'gun':
                offset = 20
            elif player.weapon == 'submachine':
                offset = 13
            if moving_right or moving_left:  # run
                self.rect.center = (player.rect.centerx + player.direction * 70, player.rect.centery - offset)
            else:  # idle
                self.rect.center = (player.rect.centerx + player.direction * 50, player.rect.centery - offset)
            # enemy
        elif self.type == 'shot' and self.char_type == 'enemy':
            self.rect.center = (
                enemy.rect.centerx + enemy.direction * 60, enemy.rect.centery)  # to keep following the Enemy shot
        self.rect.x += screen_scroll


        # SCREEN TRANSITION CLASS
class ScreenFade():
    def __init__(self, direction, colour, speed):  # direction: 1 Start level scene,  2: death scene
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        self.fade_complete = False
        self.fade_counter += self.speed

        if self.direction == 1:  # Start Level(intro):  whole screen fade
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))  # h
            pygame.draw.rect(screen, self.colour,
                             (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))  # h
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))  # v
            pygame.draw.rect(screen, self.colour,
                             (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))  # v

        if self.direction == 2:  # Death:  vertical screen fade down
            pygame.draw.rect(screen, self.colour, (
                0, 0, SCREEN_WIDTH,
                0 + self.fade_counter))  # Create a rectangle & scroll it down to fill all the screen

        if self.fade_counter >= SCREEN_WIDTH:
            self.fade_complete = True  # the rectangle is filling the whole screen => show restart button
        return self.fade_complete


# CREATE Screen Transitions (instances)
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)  # death scene

#         CREATE BUTTONS
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 120, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 200, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2, restart_img, 2)
option_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 100, option_img, 1)
resolution1_button = button.Button(SCREEN_WIDTH // 2 - 500, SCREEN_HEIGHT // 2 - 50, resolution1_img, 1)
resolution2_button = button.Button(SCREEN_WIDTH // 2 - 500, SCREEN_HEIGHT // 2 + 50, resolution2_img, 1)
resolution3_button = button.Button(SCREEN_WIDTH // 2 - 500, SCREEN_HEIGHT // 2 - 150, resolution3_img, 1)
resolution4_button = button.Button(SCREEN_WIDTH // 2 - 500, SCREEN_HEIGHT // 2 - 250, resolution4_img, 1)
resolution5_button = button.Button(SCREEN_WIDTH // 2 - 500, SCREEN_HEIGHT // 2 + 150, resolution5_img, 1)
music_button = button.Button(SCREEN_WIDTH // 2 + 300, SCREEN_HEIGHT // 2 - 200, music_img, 1)
back_button = button.Button(SCREEN_WIDTH // 2 + 300, SCREEN_HEIGHT // 2 + 200, back_img, 1)
arcade_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2, arcade_img, 1)
credits_button = button.Button(SCREEN_WIDTH // 2 - 450, SCREEN_HEIGHT // 2 + 240, credits_img, 1)
help_button = button.Button(SCREEN_WIDTH // 2 - 450, SCREEN_HEIGHT // 2 + 140, help_img, 1)

#         CREATE SPRITE GROUP          it contains the bullets that we gonna show on screen (the shot bullets)
enemy_group = pygame.sprite.Group()  # Bcz we have many enemies
zombie1_group = pygame.sprite.Group()
zombie2_group = pygame.sprite.Group()
spider_group = pygame.sprite.Group()
dog_group = pygame.sprite.Group()
bullet_player_group = pygame.sprite.Group()
bullet_enemy_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
blood_group = pygame.sprite.Group()
spark_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
stairs_group = pygame.sprite.Group()

# press button animation
press_button = []
for x in range(0, 11):
    img = pygame.image.load(f"img/button/{x}.png")
    img = pygame.transform.scale(img, (30, 30))
    press_button.append(img)

    # Box spark animation
box_spark = []
for x in range(0, 7):
    img = pygame.image.load(f"img/boxspark/{x}.png")
    box_spark.append(img)

# INITIALISE EMPTY STAGE  [Create empty tile list (tiles contain -1)]
world_data = []  # THE STAGE (grid)             16*150 tiles
for row in range(ROWS):
    r = [
            -1] * COLS  # initialise each row (list) by empty tiles (-1)      (each row will contain 150 empty tiles  (empty tile = contains -1))
    world_data.append(r)

# Load in level data and create world (paste the current stage in the world  (paste the current stage's tiles values in the empty stage tiles values (-1))
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')  # csv reader , delimiter: the separable between values
    for x, row in enumerate(reader):  # spread csv file into rows
        for y, tile in enumerate(row):  # extract each individual tile ------->  get individual values
            world_data[x][y] = int(
                tile)  # remplace empty tiles (-1 values in world_data) with those csv file tiles (with those individual values) to create the current level

world = World()
player = world.process_data(world_data)
aim_counter = 10
runfx_counter = 45  # TO play footsteps sound
play_runfx = True  # True: TO play footsteps sound
jump_counter = 45
can_jump = True
msg_counter = 200  # time to hide msgs & to be able o change action
rest_counter = 500
next = False  # pressing e to: next / skip
msg_list = ['', '', '']
index = 0
option = False
arcade = False
credits = False
help = False

cin_counter1 = 250
cin_counter2 = 365
cin_counter3 = 493
cin_counter4 = 200
cin_counter5 = 150
cin_counter6 = 200
cin_counter7 = 120
cin_counter8 = 110
cin_counter9 = 150
cin_counter10 = 100
done = False
done2 = False
done3 = False
done4 = False
msg = 1
cin_text1 = ["              Hey! don't worry, I'm new here too",
             "        Actually I don't know how long I've been here",
             ".. It only took a few hours and the mission was ruined",
             "                We were pretty close ... and unlucky", "                              A hellish night."]
cin_text_index = 0
cin = 0
part = 1
menu = True
start_game = False
arcade = False
y1 = 0
y2 = SCREEN_HEIGHT - 80

class Fade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.display.get_surface().get_rect()
        self.image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        self.alpha = 0
        self.direction = 1

    def update(self, events):
        self.image.fill((0, 0, 0, self.alpha))
        self.alpha += self.direction
        if self.alpha > 255 or self.alpha < 0:
            self.direction *= -1
            self.alpha += self.direction

            # PAUSE function
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c or event.key == pygame.K_ESCAPE:  # continue
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif player.gold > 0:
                    if event.key == pygame.K_1 and player.gold >= 150:
                        player.gold -= 150
                        player.health_kit += 1
                        gold_fx.play()
                    elif event.key == pygame.K_2 and player.gold >= 100:
                        player.gold -= 100
                        player.ammo += 15
                        gold_fx.play()
                    elif event.key == pygame.K_3 and player.gold >= 200:
                        player.gold -= 200
                        player.ammo += 40
                        gold_fx.play()
                    elif event.key == pygame.K_4 and player.gold >= 100:
                        player.gold -= 100
                        player.grenades += 1
                        gold_fx.play()

        screen.blit(bar1_img, (310, 70))
        draw_text('PAUSED', font2, WHITE, 600, 180)
        draw_text('Press C to continue or Q to quit game', font, WHITE, 500, 240)
        draw_text('Collect gold to purchase items (Use Numbers)', font, WHITE, 420, 350)
        screen.blit(health_box_img, (350, 400))
        screen.blit(ammo_box_img, (380, 550))
        screen.blit(submachine_ammo_box_img, (850, 450))
        screen.blit(grenade_box_img, (850, 550))
        screen.blit(gold_img, (1000, 350))
        draw_text(f'{player.gold}', font, WHITE, 1035, 353)
        draw_text('150 gold   (1)', font, WHITE, 450, 460)
        draw_text('100 gold   (2)', font, WHITE, 450, 560)
        draw_text('200 gold   (3)', font, WHITE, 920, 460)
        draw_text('100 gold   (4)', font, WHITE, 900, 560)

        pygame.display.update()
        clock.tick(5)

sprites = pygame.sprite.Group(Fade())
# ======================================================= MAIN ==========================================================================
run = True
while run:  # The Main game Loop

    clock.tick(FPS)
    if player.done:
        cin = 1
        start_game = False
    if menu and start_game == False:  # ............MAIN MENU................
        screen.fill(BLACK)
        if cin_counter3 > 0:
            screen.blit(logo_img, (490, 100))
            cin_counter3 -= 1
        if cin_counter1 > 0:
            cin_counter1 -= 1
        elif cin_counter2 > 0:
            events = pygame.event.get()
            sprites.update(events)
            sprites.draw(screen)
            pygame.display.update()
            cin_counter2 -= 1
        else:
            screen.blit(menu_img, (0, 0))
            if option_button.draw(screen) and option == False and credits == False and help == False:
                menu_fx.play()
                screen.blit(menu_img, (0, 0))
                option = True
            elif option:
                screen.blit(menu_img, (0, 0))
                if resolution1_button.draw(screen):
                    SCREEN_WIDTH = 1366
                    SCREEN_HEIGHT = 768
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.toggle_fullscreen()
                if resolution2_button.draw(screen):
                    SCREEN_WIDTH = 1280
                    SCREEN_HEIGHT = 768
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.toggle_fullscreen()
                if resolution3_button.draw(screen):
                    SCREEN_WIDTH = 1600
                    SCREEN_HEIGHT = 900
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.toggle_fullscreen()
                if resolution4_button.draw(screen):
                    SCREEN_WIDTH = 1920
                    SCREEN_HEIGHT = 1080
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.toggle_fullscreen()
                if resolution5_button.draw(screen):
                    SCREEN_WIDTH = 800
                    SCREEN_HEIGHT = 600
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.toggle_fullscreen()
                if music_button.draw(screen):
                    music_on = not (music_on)
                    pygame.mixer.music.stop()

                if back_button.draw(screen):
                    option = False
                    menu_fx.play()

            elif option == False:
                if start_button.draw(screen) and credits == False and help == False:
                    menu = False
                    start_intro = True
                    cin = 1
                    part = 1
                    level = 1
                    start_game = True
                    pygame.mouse.set_visible(False)
                    player.have_submachine = False
                    cin_counter1 = 100
                    cin_counter2 = 100
                    cin_counter3 = 150
                    cin_counter4 = 200
                    cin_counter5 = 150
                    cin_counter6 = 200
                    cin_counter7 = 120
                    cin_counter8 = 110
                    cin_counter9 = 150
                    cin_counter10 = 100
                    if level < MAX_LEVELS:
                        world_data = reset_level()
                        with open(f'level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player = world.process_data(world_data)

                elif arcade_button.draw(screen) and credits == False and help == False:
                    arcade = True
                    menu = False
                    menu_fx.play()
                    cin = 1
                    part = 9
                    start_game = True
                    pygame.mouse.set_visible(False)
                    player.have_submachine = False
                    player.have_gun = False
                    cin_counter1 = 50
                    cin_counter2 = 150
                    cin_counter3 = 100
                    cin_counter4 = 200
                    level = 0
                    pygame.mixer.music.fadeout(1000)
                    pygame.mixer.music.load('audio/music2.mp3')
                    if level < MAX_LEVELS:
                        world_data = reset_level()
                        with open(f'level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player = world.process_data(world_data)

                elif exit_button.draw(screen) and credits == False and help == False:  # draw exit button + if true(clicked): action = true (action = exit game)
                    run = False

                elif credits_button.draw(screen) or credits == True:
                    credits = True
                    screen.blit(menu_img, (0, 0))
                    if back_button.draw(screen):
                        menu_fx.play()
                        credits = False
                    screen.blit(logo2_img, (615, 230))
                    draw_text("Blaster Game Studio", font2, WHITE, 470, 170)
                    draw_text("Game Developer", font2, WHITE, 520, 400)
                    draw_text("Yusuf Belkhiri", font, WHITE, 610, 470)
                    draw_text("Music", font2, WHITE, 620, 540)
                    draw_text("Hisenburgg", font, WHITE, 615, 610)
                    draw_text("Thank you for playing. Contact / Support us on itch.io", font, WHITE, 420, 700)
                elif help_button.draw(screen) or help == True:
                    help = True
                    screen.blit(menu_img, (0, 0))
                    if back_button.draw(screen):
                        menu_fx.play()
                        help = False
                    draw_text("Dodge any attack or damage by Sliding (Lshift) or Rolling (LCTRL), but it consumes stamina", font, WHITE, 100, 200)
                    draw_text("Kill enemies to increase your Remainer's level ( Increase damage, defense and movement speed )",font, WHITE, 100, 300)
                    draw_text("Switch Weapons using num buttons. Heal your Remainer (press A button)",font, WHITE, 100, 400)
                    draw_text("Collect Coins to buy some useful items from the shop (open shop from ESC)",font, WHITE, 100, 500)
                    draw_text("Your Remainer is a good guy, just make sure you are friendly with him", font, WHITE, 100,600)
            pygame.mouse.set_visible(False)  # Cursor
            screen.blit(MANUAL_CURSOR, (pygame.mouse.get_pos()))

#............CINEMATIC...............
    elif cin == 1:

        start_game = False

        if part == 1:  # PART 1
            pygame.mixer.music.fadeout(5000)
            if cin_counter1 > 0:
                cin_counter1 -= 1
                events = pygame.event.get()
                sprites.update(events)
                sprites.draw(screen)
                pygame.display.update()
            else:
                screen.fill(BLACK)
                if cin_counter2 > 0:
                    cin_counter2 -= 1
                else:
                    if index < len(press_button):
                        screen.blit(press_button[index], (650, 350))
                        index += 1
                    if index == len(press_button):
                        index = 0
                    draw_text(cin_text1[cin_text_index], font, WHITE, 400, 300)
                    if next and cin_text_index <= 3:
                        cin_text_index += 1
                        next = False
                    elif next == True:
                        part = 2
                        cin_counter1 = 100
                        cin_counter2 = 150
                        cin_counter3 = 200
                        cin_text_index = 0
                        next = False
                        done = False
                        if music_on:
                            pygame.mixer.music.play(-1, 0.0, 40000)
                        player.have_gun = True

        if part == 2:  # PART 2
            if cin_counter1 > 0:
                cin_counter1 -= 1
                screen.fill(BLACK)
            else:
                draw_bg()
                world.draw()
                pygame.draw.rect(screen, BLACK, (0, y1, SCREEN_WIDTH, 100))
                pygame.draw.rect(screen, BLACK, (0, y2, SCREEN_WIDTH, 100))
                player.draw()
                player.update()
                draw_text("DemonWoods Forests -The Front Gates (2km)-", font, WHITE, 410, 700)
                draw_text("8 pm  (3 hours since the start of the mission),    24th September 2021", font, WHITE, 300,740)
                if cin_counter2 > 0:
                    cin_counter2 -= 1
                elif cin_text_index == 0:
                    text_box(" Captain, can you hear me !   ", "we have lost the front lines control",
                             "The alpha team disappeared in seconds ")
                    if index < len(press_button):
                        screen.blit(press_button[index], (900, 150))
                        index += 1
                    if index == len(press_button):
                        index = 0
                    if next:
                        cin_text_index += 1
                        next = False
                elif cin_text_index == 1:
                    text_box(" The guards of the Suspected Organization ", " are resisting ", " ")
                    if index < len(press_button):
                        screen.blit(press_button[index], (900, 150))
                        index += 1
                    if index == len(press_button):
                        index = 0
                    if next:
                        cin_text_index += 1
                        next = False
                elif cin_text_index == 2:
                    text_box(" We gonna keep moving forward ", "", "")
                    if index < len(press_button):
                        screen.blit(press_button[index], (900, 150))
                        index += 1
                    if index == len(press_button):
                        index = 0
                    if next:
                        cin_text_index += 1
                        next = False
                elif cin_counter3 > 0:
                    cin_counter3 -= 1
                    player.update_action(0)
                    y1 -= 1
                    y2 += 1
                    draw_text("Invade the front gates", font, WHITE, 570, 350)
                else:
                    cin = 0
                    part = 3
                    cin_counter1 = 45
                    cin_counter2 = 145
                    cin_counter3 = 200
                    cin_text_index = 0
                    next = False
                    done = False
                    done2 = False
                    start_game = True
                    start_intro = False
                    y1 = 0
                    y2 = SCREEN_HEIGHT - 80
                    player.have_submachine = False

        elif part == 3:  # Part 3
            player.health = 100
            pygame.mixer.music.fadeout(4000)
            wind_fx.play(100, 0, 3000)
            screen_scroll = 0
            bg_scroll = 0
            if cin_counter10 > 0:
                cin_counter10 -= 1
                screen.fill(BLACK)
            else:
                if done2 == False:
                    dog = Soldier("dog", 15, player.rect.centery + 5, 3, 7, 0, 100, 0, 25, 0, 5, 0)
                    dog_group.add(dog)
                    enemy = Soldier("enemy", player.rect.x + 600, player.rect.centery, 2.8, 5, 70, 100, 0, 50, 15, 0, 0)
                    enemy_group.add(enemy)
                    done2 = True
                SCROLL_THRESH = 100
                screen.blit(forest_img, (0, -35))
                world.draw()
                pygame.draw.rect(screen, BLACK, (0, y1, SCREEN_WIDTH, 100))
                pygame.draw.rect(screen, BLACK, (0, y2, SCREEN_WIDTH, 100))
                player.draw()
                player.update()
                draw_text("DemonWoods Forests -the Front Gates - (2km)", font, WHITE, 410, 700)
                draw_text("8 pm (3 hours since the start of the mission), 24th September 2021", font, WHITE, 325, 740)
                player.speed = 5
                player.move(False, True)
                dog.update()  # UPDATE ANIMATION + UPDATE COOLDOWN + Check_Alive
                enemy.update()
                enemy.draw()
                enemy.speed = 7.5
                enemy.move(False, True)
                enemy.update_action(1)
                if cin_counter1 > 0:
                    cin_counter1 -= 1
                    player.update_action(15)  # slide
                else:
                    if cin_counter2 > 0:
                        player.update_action(1)  # run
                        cin_counter2 -= 1
                    else:
                        player.update_action(16)  # roll
                if player.rect.x >= SCREEN_WIDTH - SCROLL_THRESH * 2:
                    player.move(False, False)
                    player.update_action(0)
                    dog.draw()
                    if cin_counter9 > 0:
                        cin_counter9 -= 1
                    else:
                        if cin_text_index == 0:
                            text_box("Death was kidnapping the team ", "causing everyone to flee in hope of survival ",
                                     "")
                            if index < len(press_button):
                                screen.blit(press_button[index], (900, 150))
                                index += 1
                            if index == len(press_button):
                                index = 0
                            if next:
                                cin_text_index += 1
                                next = False
                        elif cin_text_index == 1:
                            text_box("      \" Saving your life is your priority \"",
                                     "    It was the first instruction in the guild", "")
                            if index < len(press_button):
                                screen.blit(press_button[index], (900, 150))
                                index += 1
                            if index == len(press_button):
                                index = 0
                            if next:
                                cin_text_index += 1
                                next = False
                        elif cin_text_index == 2:
                            text_box("But I could barely hold my gun when i reached", ' my limit, I had no choice.', '')
                            if index < len(press_button):
                                screen.blit(press_button[index], (900, 150))
                                index += 1
                            if index == len(press_button):
                                index = 0
                            if next:
                                cin_text_index += 1
                                next = False
                        else:
                            dog.dog_ai()
                            player.direction *= -1
                            player.flip = True
                            player.update_action(4)  # aim
                            dog.draw()
                            blood_group.update()
                            if done == False:
                                blood_group.draw(screen)
                            if cin_counter8 > 0:
                                cin_counter8 -= 1
                            else:
                                player.image = player.animation_list[12][1]  # Hit
                            if cin_counter3 > 0:
                                cin_counter3 -= 1
                            else:  # 1/2 fall death
                                player.image = player.animation_list[3][3]
                                dog.move(False, True)
                                if cin_counter4 > 0:
                                    cin_counter4 -= 1
                                else:
                                    done = True
                                    if cin_text_index == 3:
                                        text_box("Advancing towards the Front Gates ", "costs me my last breath ", "")
                                        if index < len(press_button):
                                            screen.blit(press_button[index], (900, 150))
                                            index += 1
                                        if index == len(press_button):
                                            index = 0
                                        if next:
                                            cin_text_index += 1
                                            next = False
                                    elif cin_text_index == 4:
                                        text_box("\" One Down here \"", " ", " ")
                                        if index < len(press_button):
                                            screen.blit(press_button[index], (980, 150))
                                            index += 1
                                        if index == len(press_button):
                                            index = 0
                                        if next:
                                            cin_text_index += 1
                                            next = False
                                    elif cin_text_index == 5:
                                        text_box("    Is it time for me to rest ? ! ", "    I .. I can't move", "")
                                        if index < len(press_button):
                                            screen.blit(press_button[index], (980, 150))
                                            index += 1
                                        if index == len(press_button):
                                            index = 0
                                        if next:
                                            cin_text_index += 1
                                            next = False
                                    else:
                                        if cin_counter7 > 0:
                                            cin_counter7 -= 1
                                        else:
                                            player.image = player.animation_list[3][7]  # fall (death)
                                            if cin_counter5 > 0:
                                                cin_counter5 -= 1
                                            elif cin_counter6 > 0:  # Fade
                                                cin_counter6 -= 1
                                                events = pygame.event.get()
                                                sprites.update(events)
                                                sprites.draw(screen)
                                                pygame.display.update()
                                            else:
                                                dog.kill()
                                                enemy.kill()
                                                part = 4
                                                screen.fill(BLACK)
                                                cin_counter1 = 250
                                                cin_counter2 = 450
                                                cin_counter3 = 450
                                                cin_counter4 = 450
                                                cin_counter5 = 450
                                                cin_counter6 = 250
                                                cin_counter7 = 150
                                                SCROLL_THRESH = 400
                                                next = False
                                                done = False
                                                cin_text_index = 0
                                                player.have_submachine = False
                                                player.have_gun = False
                                                player.gun_ammo = 0
                                                player.submachine_ammo = 0
                                                player.ammo = 0
                                                player.grenades = 0
                                                player.health_kit = 0
                                                wind_fx.fadeout(1000)
                                                player.speed = 6


        elif part == 4:  # Part 3
            screen.fill(BLACK)
            if cin_counter1 > 0:
                cin_counter1 -= 1
            else:
                if index < len(press_button):
                    screen.blit(press_button[index], (910, 450))
                    index += 1
                if index == len(press_button):
                    index = 0
                if cin_text_index == 0:
                    draw_text("                  Falling down was not my option", font, WHITE, 400, 300)

                if cin_text_index == 1:
                    draw_text(" Did i fail !  Is it over ?", font, WHITE, 400, 300)
                    draw_text("What happened to the investigation's team ?", font, WHITE, 400, 370)
                    draw_text("What about the objective ! is it canceled ?", font, WHITE, 400, 440)
                if cin_text_index == 2:
                    draw_text("All i remember was the Guard Dog a..", font, WHITE, 400, 300)
                    draw_text("Was it even a guard dog?", font, WHITE, 400, 370)
                    draw_text("What kind of creatures are these!", font, WHITE, 400, 440)
                if cin_text_index == 3:
                    draw_text("                        ...", font, WHITE, 400, 300)
                if cin_text_index == 4:
                    draw_text("             Well, maybe I got some hope ...", font, WHITE, 400, 300)
                if next:
                    cin_text_index += 1
                    next = False
                if cin_text_index == 5:
                    part = 5
                    next = False
                    done = False
                    cin_counter1 = 130
                    cin_counter2 = 270
                    cin_counter3 = 100
                    cin_counter4 = 200
                    cin_counter5 = 200
                    cin_counter6 = 250
                    cin_text_index = 0
                    pygame.mixer.music.load('audio/music2.mp3')
                    pygame.mixer.music.set_volume(0.1)
                    player.health = 50
        elif part == 5:  # Part 5
            player.direction = 1
            player.flip = False
            player.update()
            player.rect.x = 600
            if done == False:
                player.update_action(3)
            if cin_counter1 > 0:
                cin_counter1 -= 1
                screen.fill(BLACK)
            else:
                draw_bg()
                world.draw()
                player.draw()
                pygame.draw.rect(screen, BLACK, (0, y1, SCREEN_WIDTH, 100))
                pygame.draw.rect(screen, BLACK, (0, y2, SCREEN_WIDTH, 100))
            if cin_counter2 > 0:  # fade
                cin_counter2 -= 1
                events = pygame.event.get()
                sprites.update(events)
                sprites.draw(screen)
                pygame.display.update()
            elif cin_counter3 > 0:  # wake
                cin_counter3 -= 1
            else:
                done = True
                player.update_action(23)
                if cin_counter4 > 0:
                    cin_counter4 -= 1
                elif cin_text_index == 0:
                    text_box("C..co", "It's cold here", '')
                    if next:
                        cin_text_index += 1
                        next = False
                    if index < len(press_button):
                        screen.blit(press_button[index], (980, 150))
                        index += 1
                    if index == len(press_button):
                        index = 0
                elif cin_text_index == 1:
                    text_box("Why am I thrown here !", "Sounds like a familiar place", 'Oh my head')
                    if next:
                        cin_text_index += 1
                        next = False
                    if index < len(press_button):
                        screen.blit(press_button[index], (980, 150))
                        index += 1
                    if index == len(press_button):
                        index = 0
                elif cin_text_index == 2:
                    text_box("It might be the night", "My stuffs ..damn ", '')
                    if next:
                        cin_text_index += 1
                        next = False
                    if index < len(press_button):
                        screen.blit(press_button[index], (980, 150))
                        index += 1
                    if index == len(press_button):
                        index = 0
                elif cin_text_index == 3:
                    text_box("I still feel some pain", "The injury will bleed more if I don't find a solution ", '')
                    if next:
                        cin_text_index += 1
                        next = False
                    if index < len(press_button):
                        screen.blit(press_button[index], (980, 150))
                        index += 1
                    if index == len(press_button):
                        index = 0
                elif cin_text_index == 4:
                    text_box("Let's focus on getting out alive ", '', '')
                    if next:
                        cin_text_index += 1
                        next = False
                    if index < len(press_button):
                        screen.blit(press_button[index], (980, 150))
                        index += 1
                    if index == len(press_button):
                        index = 0
                elif cin_counter6 > 0:
                    cin_counter6 -= 1
                    player.update_action(0)
                    y1 -= 1
                    y2 += 1
                    draw_text("Find a way out", font, WHITE, 600, 350)
                else:
                    cin = 0
                    start_game = True
                    start_intro = False
                    part = 6
                    done = False
                    done2 = False
                    y1 = 0
                    y2 = SCREEN_HEIGHT - 80
                    cin_counter1 = 17
                    cin_counter2 = 200
                    cin_counter3 = 165
                    cin_counter4 = 17
                    cin_counter5 = 110
                    cin_counter6 = 100
                    cin_counter7 = 320
                    player.health = 50
                    player.speed = 6
                    player.update_action(0)
                    is_aiming = False
                    aim = False
                    cin_text_index = 0

        elif part == 6:  # Part 6
            screen_scroll = 0
            bg_scroll = 0
            screen.fill(BLACK)
            if done2 == False:
                zombie1a = Soldier("zombie1", player.rect.x - 360, 570, 3.8, 2, 0, 100, 0, 15, 24, 5, 0)
                zombie1b = Soldier("zombie1", player.rect.x + 400, 570, 3.8, 1.3, 0, 100, 0, 15, 24, 5, 0)
                zombie1b.flip = True
                zombie1_group.add(zombie1a)
                zombie1_group.add(zombie1b)
                done2 = True
            world.draw()
            screen.blit(forest7_img, (0, -84))
            player.draw()
            player.update()
            player.update_action(0)
            player.move(False, False)
            for zombie1 in zombie1_group:
                zombie1.update()
                zombie1.draw()
            if done == False:
                if cin_counter1 > 0:
                    cin_counter1 -= 1
                    screen.fill(WHITE)
                else:
                    done = True
            if cin_counter2 > 0:
                cin_counter2 -= 1
            else:
                if cin_counter3 > 0:
                    cin_counter3 -= 1
                    for zombie1 in zombie1_group:
                        zombie1.zombie1()
                        if cin_counter7 > 0:
                            cin_counter7 -= 1
                        else:
                            player.image = player.animation_list[3][3]
                else:
                    zombie1a.kill()
                    zombie1b.kill()
                    if cin_counter4 > 0:
                        cin_counter4 -= 1
                        screen.fill(WHITE)
                    else:
                        draw_bg()
                        world.draw()
                        player.image = player.animation_list[3][3]
                        player.draw()
                        decoration_group.update()
                        decoration_group.draw(screen)
                        water_group.update()
                        water_group.draw(screen)
                        if cin_counter5 > 0:
                            cin_counter5 -= 1
                        else:
                            if next == False:
                                player.image = player.animation_list[3][3]
                                text_box('The forest', 'That was m..me', ' But why.. why am I seeing this !')
                                if index < len(press_button):
                                    screen.blit(press_button[index], (980, 150))
                                    index += 1
                                if index == len(press_button):
                                    index = 0
                            else:
                                if cin_counter6 > 0:
                                    cin_counter6 -= 1
                                    player.update_action(0)
                                else:
                                    cin_counter1 = 17
                                    cin_counter2 = 170
                                    cin_counter3 = 30
                                    cin_counter4 = 17
                                    cin_counter5 = 110
                                    cin_counter6 = 100
                                    cin_counter7 = 210
                                    next = False
                                    done = False
                                    player.have_submachine = False
                                    player.have_gun = False
                                    cin = 0
                                    player.done = False
                                    start_game = True
                                    part = 7
                                    done2 = False

        elif part == 7:  # Part 7
            screen_scroll = 0
            bg_scroll = 0
            if done2 == False:
                zombie1a = Soldier("zombie1", player.rect.x - 40, 570, 3.8, 2.6, 0, 100, 0, 15, 24, 5, 0)
                zombie1b = Soldier("zombie1", player.rect.x + 70, 570, 3.8, 2.6, 0, 100, 0, 15, 24, 5, 0)
                zombie1b.flip = True
                zombie1_group.add(zombie1a)
                zombie1_group.add(zombie1b)
                done2 = True
            screen.fill(BLACK)
            world.draw()
            screen.blit(forest8_img, (0, -84))
            player.draw()
            player.update()
            player.image = player.animation_list[3][3]
            player.move(False, False)
            for zombie1 in zombie1_group:
                zombie1.update()
                zombie1.draw()
            if done == False:
                if cin_counter1 > 0:
                    cin_counter1 -= 1
                    screen.fill(WHITE)
                else:
                    done = True
            if cin_counter2 > 0:
                cin_counter2 -= 1
            else:
                if cin_counter3 > 0:
                    for zombie1 in zombie1_group:
                        zombie1.update_action(4)
                    cin_counter3 -= 1
                    blood_group.update()
                    blood_group.draw(screen)
                else:
                    if cin_counter4 > 0:
                        cin_counter4 -= 1
                        screen.fill(WHITE)
                    else:
                        draw_bg()
                        world.draw()
                        player.image = player.animation_list[3][3]
                        player.draw()
                        decoration_group.update()
                        decoration_group.draw(screen)
                        water_group.update()
                        water_group.draw(screen)
                        zombie1b.rect.x = player.rect.x + 340
                        zombie1a.rect.x = player.rect.x - 340
                        for zombie1 in zombie1_group:
                            zombie1.update()
                            zombie1.draw()
                        if next == False:
                            player.image = player.animation_list[3][3]
                            for zombie1 in zombie1_group:
                                zombie1.update()
                                zombie1.draw()
                            text_box('This foolish organization ', 'will destroy humanity.', 'You gonna pay.')
                            if index < len(press_button):
                                screen.blit(press_button[index], (980, 150))
                                index += 1
                            if index == len(press_button):
                                index = 0
                        else:
                            if cin_counter6 > 0:
                                cin_counter6 -= 1
                                player.update_action(0)
                                for zombie1 in zombie1_group:
                                    zombie1.update()
                                    zombie1.draw()
                            else:
                                cin_counter1 = 160
                                cin_counter2 = 100
                                cin_counter3 = 450
                                cin_counter4 = 700
                                cin_counter5 = 160
                                cin_counter6 = 140
                                cin_counter7 = 250
                                next = False
                                done = False
                                done2 = False
                                player.have_submachine = False
                                player.have_gun = False
                                cin = 0
                                player.done = False
                                start_game = True
                                start_intro = False
                                part = 8

        if part == 8:  # PART 8         GAME OVER
            if cin_counter6 > 0:
                cin_counter6 -= 1
                screen.fill(BLACK)
            else:
                screen.fill(WHITE)
            if cin_counter1 > 0:
                cin_counter1 -= 1
                events = pygame.event.get()
                sprites.update(events)
                sprites.draw(screen)
                pygame.display.update()
            elif cin_counter2 > 0:
                cin_counter2 -= 1
            elif cin_counter3 > 0:
                cin_counter3 -= 1
                draw_text("Thank  You  For  Playing", font, BLACK, 560, 350)
                draw_text("To Be Continued..", font, BLACK, 600, 480)
            elif cin_counter4 > 0:
                cin_counter4 -= 1  # Credits
                screen.blit(logo2_img, (615, 230))
                draw_text("Blaster Game Studio", font2, BLACK, 470, 170)
                draw_text("Game Developer", font2, BLACK, 520, 400)
                draw_text("Yusuf Belkhiri", font, BLACK, 610, 470)
                draw_text("Music", font2, BLACK, 620, 540)
                draw_text("Hisenburgg", font, BLACK, 615, 610)
            elif cin_counter5 > 0:
                cin_counter5 -= 1
                sprites.update(events)
                sprites.draw(screen)
                pygame.display.update()
            else:
                menu = True
                start_game = False
                cin = 0
                part = 1
                var = True
                cin_text_index = 0
                cin_counter1 = 50
                cin_counter2 = 300
                cin_counter3 = 75
                cin_counter4 = 200
                cin_counter5 = 150
                cin_counter6 = 200
                cin_counter7 = 120
                cin_counter8 = 110
                cin_counter9 = 150
                cin_counter10 = 100
                done = False
                done2 = False
                done3 = False
                done4 = False

        if part == 9:  # PART 9 FOR ARCADE
            player.update()
            player.rect.x = 570
            water_group.update()
            water_group.draw(screen)
            decoration_group.update()
            decoration_group.draw(screen)
            if done == False:
                player.update_action(3)
            if cin_counter1 > 0:
                cin_counter1 -= 1
                screen.fill(BLACK)
            else:
                draw_bg()
                world.draw()
                player.draw()
                pygame.draw.rect(screen, BLACK, (0, y1, SCREEN_WIDTH, 100))
                pygame.draw.rect(screen, BLACK, (0, y2, SCREEN_WIDTH, 100))
                draw_text("One hour before dusk", font, WHITE, 580, 700)
            if cin_counter2 > 0:  # fade
                cin_counter2 -= 1
                events = pygame.event.get()
                sprites.update(events)
                sprites.draw(screen)
                pygame.display.update()
            elif cin_counter3 > 0:  # wake
                cin_counter3 -= 1
            else:
                done = True
                player.update_action(23)
                if cin_counter4 > 0:
                    cin_counter4 -= 1
                if cin_text_index == 0:
                    text_box("Let's start the party !", "", "")
                    draw_text("Kill Enemies To Level Up & Get more Time ", font, WHITE, 462, 350)
                    draw_text("Press Escape Button To Buy Items", font, WHITE, 470, 420)
                    if index < len(press_button):
                        screen.blit(press_button[index], (980, 150))
                        index += 1
                    if index == len(press_button):
                        index = 0
                    if next:
                        cin_text_index += 1
                        next = False
                elif cin_counter6 > 0:
                    cin_counter6 -= 1
                    player.update_action(0)
                    y1 -= 1
                    y2 += 1
                    draw_text("Find a weapon and blow up some heads ", font, WHITE, 470, 350)
                else:
                    player.grenades = 0
                    player.health_kit = 0
                    pygame.mixer.music.play(-1, 0, 4000)
                    cin = 0
                    start_game = True
                    start_intro = False
                    done = False
                    next = False
                    y1 = 0
                    y2 = SCREEN_HEIGHT - 80
                    cin_counter1 = 17
                    cin_counter2 = 200
                    cin_counter3 = 165
                    cin_counter4 = 17
                    cin_counter5 = 110
                    cin_counter6 = 100
                    cin_text_index = 0
                    player.update_action(0)
                    is_aiming = False
                    aim = False
                    player.time = 100
                    arcade = True


    else:  # .............START GAME...............
        if arcade:
            player.time -= 0.017
            if player.time <= 0:
                player.health = 0
                # UI
        draw_bg()  # Draw Background
        world.draw()  # Draw STAGE
        # enemies
        for enemy in enemy_group:
            enemy.enemy_ai()
            if enemy.health > 0:
                if enemy.hit:
                    draw_text(f'{player.dmg - enemy.defense}', font3, RED, enemy.rect.left, enemy.rect.top)
                    enemy.hit_counter -= 1
                    if enemy.hit_counter <= 0:
                        enemy.hit = False
                        enemy.hit_counter = 18
            enemy.update()  # UPDATE ANIMATION + UPDATE COOLDOWN + Check_Alive
            enemy.draw()  # screen.blit(enemy.image, enemy.rect)
            if enemy.health > 0 and enemy.health < 100:  # if enemy dies don't show health bar
                health_bar = HealthBar(enemy.rect.x, enemy.rect.y - 8, enemy.health, enemy.max_health, 'enemy',
                                       'health')
                health_bar.draw(enemy.health, enemy.rect.x + 15)
        # Zombie1
        for zombie1 in zombie1_group:
            zombie1.zombie1()  # zombie ai
            if zombie1.health > 0:
                if zombie1.hit:
                    draw_text(f'{player.dmg - zombie1.defense}', font3, RED, zombie1.rect.left, zombie1.rect.top)
                    if player.weapon == 'gun':
                        zombie1.update_action(12)
                    zombie1.hit_counter -= 1
                    if zombie1.hit_counter <= 0:
                        zombie1.hit = False
                        zombie1.hit_counter = 18
            zombie1.update()  # UPDATE ANIMATION + UPDATE COOLDOWN + Check_Alive
            zombie1.draw()  # screen.blit(enemy.image, enemy.rect)
            if zombie1.health > 0 and zombie1.health < 100:  # if enemy dies don't show health bar
                health_bar = HealthBar(zombie1.rect.x, zombie1.rect.y - 10, zombie1.health, zombie1.max_health, 'enemy',
                                       'health')
                health_bar.draw(zombie1.health, zombie1.rect.x)
        # Zombie2
        for zombie2 in zombie2_group:
            zombie2.zombie2()  # zombie ai
            if zombie2.health > 0:
                if zombie2.hit:
                    draw_text(f'{player.dmg - zombie2.defense}', font3, RED, zombie2.rect.left, zombie2.rect.top)
                    zombie2.hit_counter -= 1
                    if zombie2.hit_counter <= 0:
                        zombie2.hit = False
                        zombie2.hit_counter = 18
            zombie2.update()  # UPDATE ANIMATION + UPDATE COOLDOWN + Check_Alive
            zombie2.draw()  # screen.blit(enemy.image, enemy.rect)
            if zombie2.health > 0 and zombie2.health < 100:  # if enemy dies don't show health bar
                health_bar = HealthBar(zombie2.rect.x, zombie2.rect.y - 10, zombie2.health, zombie2.max_health, 'enemy',
                                       'health')
                health_bar.draw(zombie2.health, zombie2.rect.x)
        # Spider
        for spider in spider_group:
            spider.spider_ai()
            if spider.health > 0:
                if spider.hit:
                    draw_text(f'{player.dmg - spider.defense}', font3, RED, spider.rect.left, spider.rect.top)
                    spider.update_action(12)
                    spider.hit_counter -= 1
                    if spider.hit_counter <= 0:
                        spider.hit = False
                        spider.hit_counter = 18
            spider.update()  # UPDATE ANIMATION + UPDATE COOLDOWN + Check_Alive
            spider.draw()  # screen.blit(enemy.image, enemy.rect)
            if spider.health > 0 and spider.health < 100:  # if enemy dies don't show health bar
                health_bar = HealthBar(spider.rect.x, spider.rect.y - 8, spider.health, spider.max_health, 'enemy',
                                       'health')
                health_bar.draw(spider.health, spider.rect.x + 15)
        # player
        player.update()  # update the image before draw (UPDATE ANIMATION) + UPDATE COOLDOWN + Check_Alive
        player.draw()  # screen.blit(player.image, player.rect)
        # Dog
        for dog in dog_group:
            dog.dog_ai()
            if dog.health > 0:
                if dog.hit:
                    draw_text(f'{player.dmg - dog.defense}', font3, RED, dog.rect.left, dog.rect.top)
                    dog.hit_counter -= 1
                    if dog.hit_counter <= 0:
                        dog.hit = False
                        dog.hit_counter = 18
            dog.update()  # UPDATE ANIMATION + UPDATE COOLDOWN + Check_Alive
            dog.draw()  # screen.blit(enemy.image, enemy.rect)
            if dog.health > 0 and dog.health < 100:  # if enemy dies don't show health bar
                health_bar = HealthBar(dog.rect.x, dog.rect.y - 8, dog.health, dog.max_health, 'enemy', 'health')
                health_bar.draw(dog.health, dog.rect.x + 15)

        # Update & Draw Sprite Groups
        bullet_player_group.update()  # MOVE the Bullet
        bullet_enemy_group.update()
        grenade_group.update()  # MOVE the grenade
        explosion_group.update()  # MOVE the explosion (Animation)
        blood_group.update()  # MOVE the blood (Animation)
        spark_group.update()  # MOVE the spark (Animation)
        item_box_group.update()  # MOVE the item_box (update it)
        decoration_group.update()
        water_group.update()
        exit_group.update()
        box_group.update()
        stairs_group.update()
        bullet_player_group.draw(screen)  # DRAW THE BULLET
        bullet_enemy_group.draw(screen)
        grenade_group.draw(screen)  # DRAW the grenade
        explosion_group.draw(screen)  # DRAW the explosion
        blood_group.draw(screen)  # DRAW the blood
        spark_group.draw(screen)  # DRAW the spark
        item_box_group.draw(screen)  # DRAW the items
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)
        box_group.draw(screen)
        stairs_group.draw(screen)

        # Start Intro
        if start_intro:
            if intro_fade.fade():  # Intro screen + check if completed
                start_intro = False  # to avoid repeating
                intro_fade.fade_counter = 0  # reset

        # Footsteps sound counter
        if play_runfx == False:
            runfx_counter -= 1
            if runfx_counter == 0:
                play_runfx = True
                runfx_counter = 37

        # Jump Counter
        if can_jump == False:
            jump_counter -= 1
            if jump_counter == 0:
                can_jump = True
                jump_counter = 45

        # Rest_counter   (re-fill player energy)     (regenerate stamina)
        if player.stamina < player.max_stamina:
            player.stamina += 0.4

        #                    Update Action
        if player.alive:
            if shoot and player.ammo > 0:  # Shoot
                player.shoot()  # for both (player & enemies)  (so: made it in the Soldier class)
            elif throw and grenade_thrown == False and player.grenades > 0:  # for player only (not made in the Soldier class)   GRENADE THROWN: INSTEAD OF COOLDOWN
                grenade = Grenade(player.rect.centerx + player.direction * (0.5 * player.rect.size[0]), player.rect.top,
                                  player.direction, 'player_grenade',
                                  9)  # If (grenade): create a Grenade instance     size[0] means the width (x)
                grenade_group.add(grenade)  # add the created grenade to sprite group
                player.grenades -= 1
                grenade_thrown = True
            if player.in_air:  # JUMP & Fall     1)Aim       2)Normal
                run_fx.stop()
                if player.vel_y < 0:  # JUmp
                    if shoot:
                        if player.weapon == 'gun':
                            player.update_action(24)
                        else:
                            player.update_action(25)
                    elif aim:
                        player.update_action(13)
                    else:
                        player.update_action(2)
                if player.vel_y > 0:  # Fall
                    if shoot:
                        if player.weapon == 'gun':
                            player.update_action(24)
                        else:
                            player.update_action(25)
                    elif aim:
                        player.update_action(14)
                    else:
                        player.update_action(5)
            elif player.is_sliding:  # Slide   &    Roll
                if act == 1:
                    player.update_action(15)
                else:
                    player.update_action(16)
            elif player.hit:  # Player Hit
                if aim:
                    player.update_action(17)
                else:
                    player.update_action(12)
                player.hit_counter -= 1
                if player.hit_counter <= 0:
                    player.hit = False
                    player.hit_counter = 10
            elif crouch:  # Normal Crouch
                player.update_action(11)
                run_fx.stop()
            elif aim_crouch:  # (Aim Crouch)
                if shoot == False:
                    if player.weapon == 'gun':
                        player.update_action(9)
                    if player.weapon == 'submachine':
                        player.update_action(20)
                run_fx.stop()
            elif moving_left or moving_right:  # RUN           1) AimRun           2) Run
                if aim == True:
                    if player.weapon == 'gun':
                        player.update_action(8)
                    if player.weapon == 'submachine':
                        player.update_action(22)
                else:
                    player.update_action(1)
                if play_runfx == True:
                    run_fx.play(0, 0, 200)
                    play_runfx = False
            else:  # IDLE:               1)Aim Idle     2) Idle
                run_fx.stop()
                if aim == True and shooot == True:
                    if shoot == False:
                        if player.weapon == 'gun':
                            player.update_action(7)
                        elif player.weapon == 'submachine':
                            player.update_action(19)
                            # 1   Aim Idle (After shooting) shouldn't repeat aim animation after shooting a bullet
                elif aim == True and shooot == False and shoot == False:
                    if is_aiming == False:
                        player.update_action(6)  # Aim Idle (Before any shot) (Aim animation)   player didn't shoot  yet
                        aim_counter -= 1
                        if aim_counter <= 0:
                            is_aiming = True
                            aim_counter = 10
                    else:
                        if player.weapon == 'gun':
                            player.update_action(7)
                        elif player.weapon == 'submachine':
                            player.update_action(19)
                else:
                    player.update_action(0)  # 2
                # Movement Function + Screen Scroll
            screen_scroll, level_complete = player.move(moving_left,moving_right)  # to get the scroll value   (Scroll: EQUAL TO PLAYER SPEED)
            bg_scroll -= screen_scroll
            # Check if LEVEL COMPLETED
            if level_complete:
                # start_intro = True
                level += 1
                start_game = False
                if level == 1:
                    pygame.mixer.music.fadeout(1000)
                if level == 2:
                    cin = 1
                    part = 3
                player.location_index = 0
                player.msg_index = 0
                player.have_key = False

                if level < MAX_LEVELS:  # to avoid error
                    world_data = reset_level()  # reset level (-1 tiles)
                    # Load in Level data and recreate world (NEXT level)
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player = world.process_data(world_data)

                    # RESTART LEVEL    (Player Died)
        else:
            screen_scroll = 0  # stop scrolling (avoid bugs)
            player.location_index = 0
            player.msg_index = 0
            player.done = False
            is_aiming = False
            aim = False
            if level == 0:
                cin_counter1 = 160
                cin_counter2 = 100
                cin_counter3 = 450
                cin_counter4 = 700
                cin_counter5 = 100
                cin_counter6 = 140
                part = 8
            if death_fade.fade():  # draw death screen + check if completed
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0  # reset
                    start_intro = True  # start intro when restarting level
                    bg_scroll = 0
                    world_data = reset_level()  # reset level (-1 tiles)
                    # Load in Level data and recreate world (CURENT level)
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player = world.process_data(world_data)
                if exit_button.draw(screen):
                    run = False
            if level == 1:
                player.have_submachine = False
                player.have_gun = True
            elif level == 2:
                player.have_gun = False
                player.gun_ammo = 0
                player.submachine_ammo = 0
                player.grenades = 0
                player.health_kit = 0
                player.health = 50
                player.ammo = 0
                part = 6
                cin_counter1 = 17
                cin_counter2 = 200
                cin_counter3 = 165
                cin_counter4 = 17
                cin_counter5 = 110
                cin_counter6 = 100
                cin_counter7 = 210
            pygame.mouse.set_visible(False)  # Cursor
            screen.blit(MANUAL_CURSOR, (pygame.mouse.get_pos()))

    ############################## EVENTS
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            run = False
        # KEYBOARD INPUT  (button pressed) ______INPUT SYSTEM________
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and cin == 0:  # Move Left
                moving_left = True
            if event.key == pygame.K_d and cin == 0:  # Move Right
                moving_right = True
            if event.key == pygame.K_s and cin == 0:  # Crouch       1) Normal Crouch        2) Aim Crouch
                if not (aim):
                    crouch = True
                else:
                    aim_crouch = True
            if event.key == pygame.K_2 and (
                    aim == False or player.weapon == 'submachine') and crouch == False and player.have_gun and cin == 0:  # Aim (Pistol)
                aim = True
                aim_fx.play()
                player.weapon = 'gun'
                player.ammo = player.gun_ammo
            if event.key == pygame.K_3 and (aim == False or player.weapon == 'gun') and crouch == False and player.have_submachine and cin == 0:  # Aim2 (Submachine)
                aim = True
                aim_fx.play()
                player.weapon = 'submachine'
                player.ammo = player.submachine_ammo
            if event.key == pygame.K_SPACE and player.alive and can_jump and cin == 0:  # Jump
                if crouch or aim_crouch:  # s + jump: slide
                    player.slide = True
                    act = 1
                else:
                    player.jump = True
                    can_jump = False  # jump coolDown
                    if random.randint(1, 4) == 1:
                        jump_fx.play()
            if event.key == pygame.K_LSHIFT and player.alive and player.stamina > 30 and cin == 0:  # Slide
                player.slide = True
                act = 1
            if event.key == pygame.K_LCTRL and player.alive and player.stamina > 30 and cin == 0:  # Roll
                player.slide = True
                act = 2
            if event.key == pygame.K_q and player.alive and player.health < player.max_health and player.health_kit > 0 and cin == 0:  # heal
                player.health += 25
                health_kit_fx.play()
                draw_text('+ 25', font3, GREEN2, player.rect.right, player.rect.top)
                if player.health > player.max_health:
                    player.health = player.max_health
                player.health_kit -= 1
            if event.key == pygame.K_f and player.alive and player.collide_action and action == False:  # ACTION
                action = True
                if player.msg_index == 0:
                    if level == 1:
                        text = 'We heared a lot about the forest, Weired place'
                    elif level == 2:
                        text = 'Everything seems strange, what a corpse'
                    elif level == 0:
                        text = 'COMPLETED'
                        cin = 1
                        part = 8
                        cin_counter1 = 160
                        cin_counter2 = 100
                        cin_counter3 = 450
                        cin_counter4 = 700
                        cin_counter5 = 160
                        cin_counter6 = 140
                        cin_counter7 = 250
                elif player.msg_index == 1:
                    if level == 2:
                        if player.have_key == False:
                            text = "It requires a key "
                        else:
                            cin = 1
                    elif level == 0:
                        text = 'COMPLETED'
                        cin = 1
                        part = 8
                        cin_counter1 = 160
                        cin_counter2 = 100
                        cin_counter3 = 450
                        cin_counter4 = 700
                        cin_counter5 = 160
                        cin_counter6 = 140
                        cin_counter7 = 250
                elif player.msg_index == 2:
                    enemy = Soldier('enemy', SCREEN_WIDTH + 1000, player.rect.y - 150, 3, 5, 60, 100, 0, 50, 25, 0)
                    enemy_group.add(enemy)
                    text = "   :')                                                  ..press E "
            if event.key == pygame.K_e and (action == True or cin > 0):  # Next/ Skip
                next = True
            if event.key == pygame.K_ESCAPE and menu == False:  # Pause
                pause()
                menu_fx.play()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and aim == True:  # Shoot      and player.vel_y >= -2.5
                if player.ammo > 0 and player.shoot_cooldown == 0:
                    shoot = True
                    shooot = True  # shot after aim  (after shot a bullet : aim animation shouldn't repeat)   the one that keeps the aim animation unreplayable
                elif player.ammo <= 0:  # Empty Gun
                    emptygun_fx.play()
                    shot3_fx.stop()
            elif event.button == 3:  # Throw Grenade
                throw = True
                grenade_thrown = False  # instead of cooldown
        # keyboard button released         # the listed actions here: we can hold the button to keep the action realised
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_s:
                aim_crouch = False
                crouch = False
            if event.key == pygame.K_1:
                aim = False
                is_aiming = False
                shooot = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                shoot = False
                if player.weapon == 'submachine':
                    # shot3_fx.stop()
                    player.audio_cooldown = 0
            elif event.button == 3:
                throw = False

        if event.type == PLAYER_HIT:  # Custom Events
            player.hit = True

    if action and (msg_counter >= 0 or next == False):
        if not (player.have_key) and level != 0:
            text_box(text, '', '')
            if index < len(press_button):
                screen.blit(press_button[index], (900, 150))
                index += 1
            if index == len(press_button):
                index = 0
        moving_right = False
        moving_left = False
        player.can_shoot = False
        player.jump = False
        player.slide = False
        msg_counter -= 1
        draw_text(f'{msg_list[player.msg_index]}', font, WHITE, player.rect.x - player.direction * 10,
                  player.rect.top - 50)
        if msg_counter <= 0 or next:
            action = False
            msg_counter = 200
            next = False

    if player.in_air or player.is_sliding:
        run_fx.stop()

    if player.weapon == 'submachine':
        player.submachine_ammo = player.ammo  # The Resting ammo
    elif player.weapon == 'gun':
        player.gun_ammo = player.ammo

    pygame.display.update()
    print(player.location_index)

pygame.quit()
