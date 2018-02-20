#Quest for Kronol

import pygame
from pygame.locals import *
import math
import random
#import easygui

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 1024)
#pygame.joystick.init()

class Player(object):

    def __init__(self, soldier, health_bar, health = 8):
        '''This class creates a Player object, which groups together a Human and a Health bar'''
        self.human = soldier
        self.bar = health_bar
        self.hp = health

    def adjust(self, num = 1):
        '''P.adjust(int) --> None
        Adds health to bar and human if num > 1, subtracts from otherwise'''
        self.human.hp += num
        self.bar.hp += num
        self.bar.update()

class Human(pygame.sprite.Sprite):

    def __init__(self, coordinates = (0, 0), health = 8):
        '''A sprite modelling the player character, with a health, point, speed, and guns property. Also creates a Bar object with the same health value. The object is aligned to coordinates'''
        pygame.sprite.Sprite.__init__(self)

        self.hp = health
        self.bar = Health(self.hp)
        self.points = 0
        self.sp = 5

        #Since the player can rotate in any direction, this property is an angle between 0 - 360
        self.direction = 0

        self.image_list = []

        for pic in range (4):

            self.image_list.append(pygame.image.load(r'Graphics\Human\Pistol\{}.png'.format(pic)).convert_alpha())

        self.image_pos = 0
        self.image = self.image_list[self.image_pos]

        self.rect = self.image.get_rect()
        self.rect.centerx = coordinates[0]
        self.rect.centery = coordinates[1]

    def update(self, angle = ' '):
        '''H.update(str) --> None
        Rotates the player to point gun towards the point'''
        self.direction = math.degrees(math.atan2(-(self.rect.centery - mark.rect.center[1]), (self.rect.right - mark.rect.center[0])))

        if angle in 'UPDOWNLEFTRIGHT':

            if angle == 'UP':
                self.rect.centery -= self.sp

            elif angle == 'RIGHT':
                self.rect.centerx += self.sp

            elif angle == 'DOWN':
                self.rect.centery += self.sp

            elif angle == 'LEFT':
                self.rect.centerx -= self.sp

            if self.image_pos < 3:
                #Making it so that every five movements we animate, using integer flooring
                self.image_pos += 0.2

            else:
                self.image_pos = 0

        self.image = pygame.transform.rotate(self.image_list[int(self.image_pos)], self.direction + 180)

    def get_points(self):
        '''H.get_points() --> int
        Return the player's point value'''
        return self.points

    def add_points(self, num = 1):
        '''H.add_points(int) --> None
        Add points to the player's point value'''
        self.points += num

class Health(pygame.sprite.Sprite):

    def __init__(self, health):
        '''A class modelling a health bar that reflect's a player's health in real time'''
        pygame.sprite.Sprite.__init__(self)

        self.image_list = []
        self.hp = health

        for bar in range(9):
            self.image_list.append(pygame.image.load(r'Graphics\Health\{}.png'.format(bar)).convert_alpha())

        self.image = self.image_list[self.hp]
        self.rect = self.image.get_rect()
        self.rect.right = game_size[0]

    def update(self):
        '''H.update() --> None
        Refresh the health bar'''
        if self.hp >= 0 and self.hp <= 8:
            self.image = self.image_list[self.hp]

class Hitmarker(pygame.sprite.Sprite):

    def __init__(self):
        '''A class modelling a hitmarker that acts as the mouse'''
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Graphics\hitmarker.png').convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, direction):
        '''H.update(str) --> None
        Moves the hitmarker to where the mouse/joystick commands'''
        if direction == 'UP':
            self.rect.centery -= 15

        elif direction == 'DOWN':
            self.rect.centery += 15

        elif direction == 'LEFT':
            self.rect.centerx -= 15

        elif direction == 'RIGHT':
            self.rect.centerx += 15

class Zombie(pygame.sprite.Sprite):

    def __init__(self, player, health = 10, coordinates = (0, 0), speed = 2):
        '''A Zombie class modelling enemies that chase the player, with a target, health, and speed properties. Placed at coordinates.'''
        pygame.sprite.Sprite.__init__(self)

        self.hp = health
        self.sp = rounds / 5 + 1
        self.direction = 0
        self.enemy = player

        self.running = []
        self.death = []

        if random.randint(0, 1):
            variation = 'Green'

        else:
            variation = 'Red'

        for pic in range (4):
            self.running.append(pygame.image.load(r'Graphics\Zombie\{}\Running\{}.png'.format(variation, pic)).convert_alpha())
            self.death.append(pygame.image.load(r'Graphics\Zombie\{}\Death\{}.png'.format(variation, pic)).convert_alpha())

        self.image_pos = 0
        self.image_list = self.running
        self.image = self.running[self.image_pos]

        self.rect = self.image.get_rect()
        self.rect.centerx = coordinates[0]
        self.rect.centery = coordinates[1]

    def update(self):
        '''Z.update() --> None
        Moves zombie closer to player'''

        if self.image_list == self.running:

            if self.rect.centery > self.enemy.rect.centery:
                self.rect.centery -= min(self.rect.centery - self.enemy.rect.centery, self.sp) + random.randint(-1, 1)

            elif self.rect.centery < self.enemy.rect.centery:
                self.rect.centery += min(self.enemy.rect.centery - self.rect.centery, self.sp) + random.randint(-1, 1)

            if self.rect.centerx > self.enemy.rect.centerx:
                self.rect.centerx -= min(self.rect.centerx - self.enemy.rect.centerx, self.sp) + random.randint(-1, 1)

            elif self.rect.centerx < self.enemy.rect.centerx:
                self.rect.centerx += min(self.enemy.rect.centerx - self.rect.centerx, self.sp) + random.randint(-1, 1)

        if self.image_pos < 3:
            self.image_pos += 0.2

        else:

            if self.image_list == self.running:
                self.image_pos = 0

            else:

                self.kill()
                death_sound.play()
                spawn()

        self.direction = math.degrees(math.atan2(-(self.rect.centery - self.enemy.rect.centery), (self.rect.centerx - self.enemy.rect.centerx)))
        self.image = pygame.transform.rotate(self.image_list[int(self.image_pos)], self.direction + 180)

    def die(self):
        '''Z.die() --> None
        Shows Zombie's death animation, then kills the sprite'''
        if self.image_list != self.death:
            self.image_list = self.death
            self.image_pos = 0

            #self.image = pygame.transform.rotate(self.image_list[int(self.image_pos)], self.direction + 180)

            self.image_pos += 1

class Shot(pygame.sprite.Sprite):

    def __init__(self):
        '''A Shot class that models the bullet path of a gunshot, using a pygame.draw.line for reference'''
        pygame.sprite.Sprite.__init__(self)

        line = pygame.draw.line(background, (255, 215, 0), (user.rect.centerx, user.rect.centery), (mark.rect.centerx, mark.rect.centery), 5)
        self.image = line
        self.rect = line
        #self.image = bullet_sheet
        #sheet_rect = bullet_sheet.get_rect()


        #Bottom right
        #if (user.direction >= 90 and user.direction <= 180) or (user.direction < 0 and user.direction <= -90) and user.direction > 0:
            #self.rect = pygame.draw.line(sheet, (255, 215, 0), (0, 0), (sheet_rect.right, sheet_rect.bottom), 5)
            #sheet_rect.top, sheet_rect.left = user.rect.centerx, user.rect.centery

        #Top right
        #elif (user.direction >= 90 and user.direction <= 180) or (user.direction < 0 and user.direction <= -90):
            #self.rect = pygame.draw.line(sheet, (255, 215, 0), (0, sheet_rect.top), (sheet_rect.right, 0))
            #sheet_rect.bottom, sheet_rect.left = user.rect.centerx, user.rect.centery

        #Bottom left
        #elif not ((user.direction >= 90 and user.direction <= 180) or (user.direction < 0 and user.direction <= -90)) and user.direction > 0:
            #self.rect = pygame.draw.line(sheet, (255, 215, 0), (mark.rect.centerx, 0), (0, mark.rect.centery))

        #Top left
        #elif not ((user.direction >= 90 and user.direction <= 180) or (user.direction < 0 and user.direction <= -90)):
            #self.rect = pygame.draw.line(sheet, (255, 215, 0), (mark.rect.centerx, mark.rect.centery), (0, 0))


        #self.rect.left, self.rect.top = user.rect.centerx, user.rect.centery

    def update(self):
        '''S.update() --> None
        Recreate a bullet path of a gunshot'''

        if (user.direction >= 90 and user.direction <= 180) or (user.direction < 0 and user.direction <= -90):
            self.rect.left = self.line.left

        else:
            self.rect.right = self.line.right

        if user.direction <= 0:
            self.rect.top = self.line.top

        else:
            self.rect.top = self.line.top


class Button(pygame.sprite.Sprite):

    def __init__(self, text, coords):
        '''A Button class modelling pressable buttons'''
        pygame.sprite.Sprite.__init__(self)

        self.default = pygame.image.load('Graphics\Buttons\{}.png'.format(text)).convert()
        self.selected = pygame.image.load('Graphics\Buttons\{} H.png'.format(text)).convert()

        self.image = self.default

        self.rect = self.image.get_rect()

        self.rect.left, self.rect.top = coords[0], coords[1]

        self.sound = pygame.mixer.Sound('Graphics\Sounds\click.ogg')

    def highlight(self):
        '''B.highlight() --> None
        Changes the image of this sprite to a highlighted version'''
        self.image = self.selected

    def dehighlight(self):
        '''B.dehighlight() --> None
        Changes the image of this sprite to the original version'''
        self.image = self.default

    def press(self):
        '''B.press() --> None
        Plays a random zombie noise'''
        self.sound.play()

class Mouse(pygame.sprite.Sprite):

    def __init__(self, coords = (0, 0)):
        '''A Mouse class that models the computer cursor, with a modified image'''
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Graphics\mouse.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.left, self.rect.top = coords[0], coords[1]


def spawn(amount = 1, rounds = 1):
    '''spawn(int, int) --> None
    Spawn amount amount of zombies'''
    for times in range (amount):

        for ai in range (10):
            #First we determine if the zombie is coming from the top/bottom or left/right, randomly
            side = random.randint(0, 1)

        if side == 0:

            x = random.randint(0, 1000)
            y = random.randint(0, 1)
            #Preventing the zombie from spawning anywhere between the top and the bottom
            if y == 1:
                y = 700

        else:

            x = random.randint(0, 1)
            y = random.randint(0, 700)
            #Preventing the zombie from spawning anywhere between the left and right ends of the screen
            if x == 1:
                x = 1000

        zombies.add(Zombie(user, 8 + rounds * 2, (x, y)))

game_size = (1000, 700)
screen = pygame.display.set_mode(game_size)#, pygame.RESIZABLE)
pygame.display.set_caption('Quest for Kronol')

background = pygame.image.load('Graphics\map.png').convert()

screen.blit(background, (0, 0))

user = Human((500, 350))
users = pygame.sprite.Group(user)

font = pygame.font.Font(r'Graphics\Fonts\Dirty Play.ttf', 32)

player = Player(user, user.bar)

points_label = font.render('POINTS: {}'.format(user.get_points()), True, (255, 0, 0))

pygame.key.set_repeat(1, 50)
pygame.mouse.set_visible(0)

mark = Hitmarker()
marks = pygame.sprite.Group(mark)

bars = pygame.sprite.Group(user.bar)

#joystick = pygame.joystick.Joystick(0)
#joystick.init()

shooting = False

clock = pygame.time.Clock()
counter = 0
rounds = 1
time_left = 3600

zombies = pygame.sprite.Group()
spawn(10)

time_label = font.render('{}'.format(int(time_left / 60)), True, (255, 0, 0))

round_label = pygame.image.load('Graphics\Round\{}.png'.format(rounds)).convert_alpha()

resume = Button('Resume', (125, 50))

menu = False
mouse = Mouse()
mice = pygame.sprite.Group(mouse)

buttons = pygame.sprite.Group(resume)

shots = pygame.sprite.Group()

death_sound = pygame.mixer.Sound('Graphics\Sounds\zombie_death.ogg')
hit_sounds = [pygame.mixer.Sound('Graphics\Sounds\zombie_attack_1.ogg'), pygame.mixer.Sound('Graphics\Sounds\zombie_attack_2.ogg')]
ambient_sounds = [pygame.mixer.Sound('Graphics\Sounds\zombie_1.ogg'), pygame.mixer.Sound('Graphics\Sounds\zombie_2.ogg'), pygame.mixer.Sound('Graphics\Sounds\zombie_3.ogg')]
gunshot = pygame.mixer.Sound('Graphics\Sounds\gunshot.ogg')
music = pygame.mixer.music.load('Graphics\Sounds\music.mp3')
pygame.mixer.music.play(-1)

keep_going = True

while keep_going and user.hp > 0:

    clock.tick(60)

    if not menu:
        buttons.clear(screen, background)

        counter += 1
        time_left -= 1

        if time_left == 1:
            time_left = 3600 + (rounds * 1200)
            rounds += 1
            ambient_sounds[random.randint(0, 2)].play()
            spawn(5)

        if (pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]) and user.rect.right <= 1000:
            user.update('RIGHT')

        if (pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_a]) and user.rect.left >= 0:
            user.update('LEFT')

        if (pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_w]) and user.rect.top >= 0:
            user.update('UP')

        if (pygame.key.get_pressed()[K_DOWN] or pygame.key.get_pressed()[K_s] ) and user.rect.bottom <= 700:
            user.update('DOWN')


        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                keep_going = False

            elif ev.type == MOUSEMOTION:
                mark.rect.center = ev.pos
                user.update()
                #print(user.direction)

            elif ev.type == MOUSEBUTTONDOWN and not shooting:

                shooting = True
                #background.fill((0, 255, 0))

                if (user.direction >= 90 and user.direction <= 180) or (user.direction < 0 and user.direction <= -90):
                    x = mark.rect.centerx - user.rect.centerx

                else:
                    x = user.rect.centerx - mark.rect.centerx

                if user.direction <= 0:
                    y = user.rect.centery - mark.rect.centery

                else:
                    y = mark.rect.centery - user.rect.centery

                #bullet_sheet = pygame.Surface((x, y)).convert_alpha()
                #bullet_sheet.fill((0, 0, 0, 0))

               # print(x)
                #print(y)
                #bullet.update()

                bullet = Shot()
                shots = pygame.sprite.Group(bullet)
                gunshot.play()
                #bullet = Shot(pygame.draw.line(background, (255, 0, 0), (user.rect.centerx, user.rect.centery), (mark.rect.centerx, mark.rect.centery), 5))

                for collide in pygame.sprite.spritecollide(bullet, zombies, False):
                    collide.die()
                    user.add_points(1)

            elif ev.type == MOUSEBUTTONUP and shooting:
                shooting = False

                background = pygame.image.load('Graphics\map.png').convert()

            elif ev.type == KEYDOWN and ev.key == K_p:
                menu = True

        for collide in pygame.sprite.spritecollide(user, zombies, False):
            #Allowing the zombie to hit the player every 3/4 of a second
            if counter % 45 == 0 and pygame.sprite.collide_mask(user, collide):
                player.adjust(-1)
                hit_sounds[random.randint(0, 1)].play()

        for ai in zombies.sprites():
            ai.update()

        screen.blit(background, (0, 0))

        for group in [zombies, users, bars, marks]:
            group.clear(screen, background)

        for group in [zombies, users, bars, marks]:
            group.draw(screen)

        screen.blit(points_label, points_label.get_rect())
        screen.blit(time_label, (0, 670))
        screen.blit(round_label, (920, 660))

        points_label = font.render('POINTS: {}'.format(user.get_points()), True, (255, 0, 0))
        time_label = font.render('{:02d}:{:02d}'.format(int(time_left / 3600), int((time_left % 3600) / 60)), True, (255, 0, 0))
        round_label = pygame.image.load('Graphics\Round\{}.png'.format(rounds)).convert_alpha()

    else:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                keep_going = False

            elif ev.type == MOUSEMOTION:
                mouse.rect.center = ev.pos

                collides = []
                for collide in pygame.sprite.spritecollide(mouse, buttons, False):
                    collide.highlight()
                    collides.append(collide)

                for collide in collides:
                    collide.dehighlight()


            elif ev.type == MOUSEBUTTONDOWN:

                for collide in pygame.sprite.spritecollide(mouse, buttons, False):
                    collide.highlight()
                    collide.press()

                    if collide == resume:
                        menu = False

            #elif joystick.get_button(3):
                #menu = False

        buttons.clear(screen, background)
        mice.clear(screen, background)
        buttons.draw(screen)
        mice.draw(screen)


    pygame.display.flip()

#easygui.msgbox('Better luck next time!\nYou finished with {} points.'.format(user.points), 'Quest for Kronol')
