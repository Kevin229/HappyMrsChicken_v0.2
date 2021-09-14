import pygame
import sys
import random
import math
from gif_image import GIFImage
from pygame.locals import *
import config

egg_chicken_list = []
random_egg_chicken_list = []

pygame.init()
pygame.font.init()
pygame.mixer.init()
fps_clock = pygame.time.Clock()
current_screen = pygame.display.Info()
config.WINDOW_WIDTH = current_screen.current_w
config.WINDOW_HEIGHT = current_screen.current_h
display_surface = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption('Happy Mrs Chicken')
introduce_sound = pygame.mixer.Sound(config.INTRODUCE_SOUND)
lay_egg_sound = pygame.mixer.Sound(config.LAY_EGG_SOUND)
egg_crack_sound = pygame.mixer.Sound(config.EGG_CRACK_SOUND)
random_egg_sound = pygame.mixer.Sound(config.RANDOM_EGG_SOUND)
egg_img = GIFImage(config.EGG_IMG)
egg_crack_img = GIFImage(config.EGG_CRACK_IMG)
chicken_img = GIFImage(config.MRS_CHICKEN_IMG)


class Chicken:
    def __init__(self):
        self.width = config.BIRD_WIDTH
        self.height = config.BIRD_HEIGHT
        self.x_pos = (config.WINDOW_WIDTH - self.width) / 2
        self.y_pos = (config.WINDOW_HEIGHT - self.height) / 2
        self.x_pos_new = (config.WINDOW_WIDTH - self.width) / 2
        self.y_pos_new = (config.WINDOW_HEIGHT - self.height) / 2
        self.speed = 0
        self.gif_img_introduce = GIFImage(config.CHICKEN_IMG)
        self.gif_img_play = GIFImage(config.MRS_CHICKEN_IMG)
        self.is_play = False
        self.move_done = True
        self.length = 0.0
        self.theta = 0.0
        self.x_increase = True
        self.y_increase = True
        self.x_ok = False
        self.y_ok = False
        self.delta_x = 0
        self.delta_y = 0

    def draw(self):
        if self.is_play:
            self.gif_img_play.render(display_surface, (int(self.x_pos), int(self.y_pos)))
        else:
            self.gif_img_introduce.render(display_surface, (int(self.x_pos), int(self.y_pos)))

    def update(self, update_pos):
        if update_pos:
            self.move_done = False
            self.x_pos_new = random.randint(0, config.WINDOW_WIDTH - 50)
            self.y_pos_new = random.randint(0, config.WINDOW_HEIGHT - 120)
            self.length = math.sqrt(math.pow(self.x_pos_new - self.x_pos, 2) + math.pow(self.y_pos_new - self.y_pos, 2))
            self.theta = math.atan(abs(self.y_pos_new - self.y_pos) / abs(self.x_pos_new - self.x_pos))
            self.delta_x = self.length * math.cos(self.theta) / 50
            self.delta_y = self.length * math.sin(self.theta) / 50
            if int(self.x_pos_new - self.x_pos) > 0:
                self.x_increase = True
            else:
                self.x_increase = False
            if int(self.y_pos_new - self.y_pos) > 0:
                self.y_increase = True
            else:
                self.y_increase = False
        if self.x_increase and not self.move_done:
            if self.x_pos < self.x_pos_new:
                self.x_pos += self.delta_x
            else:
                self.x_ok = True
                pass
        elif not self.x_increase and not self.move_done:
            if self.x_pos > self.x_pos_new:
                self.x_pos -= self.delta_x
            else:
                self.x_ok = True
                pass
        if self.y_increase and not self.move_done:
            if self.y_pos < self.y_pos_new:
                self.y_pos += self.delta_y
            else:
                self.y_ok = True
                pass
        elif not self.y_increase and not self.move_done:
            if self.y_pos > self.y_pos_new:
                self.y_pos -= self.delta_y
            else:
                self.y_ok = True
                pass
        if self.x_ok and self.y_ok and not self.move_done:
            self.x_ok = False
            self.y_ok = False
            self.move_done = True
            new_pos = (self.x_pos, self.y_pos, egg_img, egg_crack_img, chicken_img)
            egg_chicken_list.append(new_pos)
            pygame.mixer.Channel(1).play(lay_egg_sound)
        pass

    def set_play(self, is_play):
        self.is_play = is_play
        pass


class Score:
    def __init__(self):
        self.num_egg = 0
        self.gif_img_egg = GIFImage(config.EGG_ICON_IMG)
        self.gif_img_chicken = GIFImage(config.CHICKEN_ICON_IMG)
        self.font_egg = pygame.font.SysFont('arial', 30, bold=True)
        self.egg_score_surface = self.font_egg.render('000', True, (255, 255, 255))
        self.egg_score_size = self.egg_score_surface.get_size()
        self.x_pos_egg = config.WINDOW_WIDTH - 90 - self.gif_img_egg.get_width() / 2
        self.y_pos_egg = 20
        self.is_egg = True

    def draw(self):
        if self.is_egg:
            self.gif_img_egg.render(display_surface, (self.x_pos_egg, self.y_pos_egg))
        else:
            self.gif_img_chicken.render(display_surface, (self.x_pos_egg, self.y_pos_egg))
        self.egg_score_surface = self.font_egg.render(str(len(egg_chicken_list) + len(random_egg_chicken_list)).zfill(3), True, (255, 255, 255), (51, 51, 255))
        display_surface.blit(self.egg_score_surface, (config.WINDOW_WIDTH - 70, self.y_pos_egg))

    def set_is_egg(self, is_egg):
        self.is_egg = is_egg
        pass


def egg_crack():
    pygame.mixer.Channel(2).play(egg_crack_sound)
    pass


def random_egg(chicken):
    if pygame.mixer.Channel(3).get_busy():
        xx_pos = random.randint(0, config.WINDOW_WIDTH - 50)
        yy_pos = random.randint(0, config.WINDOW_HEIGHT - 120)
        if xx_pos % 2 and yy_pos % 2 and len(random_egg_chicken_list) < config.MAX_RANDOM_EGG:
            new_pos = (xx_pos, yy_pos, egg_img)
            idx = random.randint(1, 2)
            if idx == 1:
                new_pos = (xx_pos, yy_pos, chicken_img)
            random_egg_chicken_list.append(new_pos)
            pygame.mixer.Channel(1).play(lay_egg_sound)
        return True
    else:
        random_egg_chicken_list.clear()
        return False


def game_start(chicken):
    chicken.__init__()
    font = pygame.font.SysFont('arial', 40, bold=True)
    heading_surface = font.render('HAPPY MRS CHICKEN', True, (255, 255, 255))
    heading_size = heading_surface.get_size()

    font_1 = pygame.font.SysFont('courier', 30, bold=True)
    font_2 = pygame.font.SysFont('courier', 22, bold=True)
    str_display_1 = 'PRESS A KEY TO PLAY'
    str_display_2 = '5: Crack Egg Mode 7: Lay Egg Mode 9: Reset game 0: Auto Egg Mode in Crack Egg Mode'
    comment_surface_1 = font_1.render(str_display_1, True, (255, 255, 255))
    comment_surface_2 = font_2.render(str_display_2, True, (255, 255, 255))
    comment_size_1 = comment_surface_1.get_size()
    comment_size_2 = comment_surface_2.get_size()

    if pygame.mixer.Channel(0).get_busy():
        pygame.mixer.Channel(0).stop()

    pygame.mixer.Channel(0).play(introduce_sound, -1)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                return

        display_surface.fill(config.BACK_GROUND_COLOR)
        chicken.draw()
        display_surface.blit(heading_surface, (int((config.WINDOW_WIDTH - heading_size[0]) / 2), int(config.WINDOW_HEIGHT / 8 + heading_size[1] / 2)))
        display_surface.blit(comment_surface_1, (int((config.WINDOW_WIDTH - comment_size_1[0]) / 2), int(config.WINDOW_HEIGHT * 5 / 8 + comment_size_1[1] / 2)))
        display_surface.blit(comment_surface_2, (int((config.WINDOW_WIDTH - comment_size_2[0]) / 2), int(config.WINDOW_HEIGHT * 6 / 8 + comment_size_2[1] / 2)))

        pygame.display.update()
        fps_clock.tick(config.FPS)


def game_play(chicken, score):
    chicken.__init__()
    score.__init__()
    update_pos = False
    egg_to_chicken = False
    egg_chicken_list.clear()
    random_egg_chicken_list.clear()
    chicken.set_play(True)
    dance_count = 0
    left_to_right = True
    random_egg_mode = False
    pygame.mixer.Channel(2).stop()
    pygame.mixer.Channel(3).stop()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if egg_to_chicken:
                    if event.key == K_0:
                        pygame.mixer.Channel(3).play(random_egg_sound)
                        random_egg_mode = True
                if event.key == K_5:
                    if len(egg_chicken_list):
                        egg_to_chicken = True
                        egg_crack()
                    else:
                        update_pos = True
                elif event.key == K_7:
                    if len(egg_chicken_list):
                        egg_to_chicken = False
                        score.set_is_egg(True)
                    else:
                        update_pos = True
                elif event.key == K_9:
                    return
                else:
                    update_pos = True

        display_surface.fill(config.BACK_GROUND_COLOR)

        if not egg_to_chicken:
            chicken.draw()
            chicken.update(update_pos)
        update_pos = False

        if random_egg_mode:
            if left_to_right:
                random_egg_mode = random_egg(chicken)

            for x, y, gif in random_egg_chicken_list:
                gif.render(display_surface, (x, y))

        for x, y, *gif in egg_chicken_list:
            if egg_to_chicken:
                if pygame.mixer.Channel(2).get_busy():
                    gif[1].render(display_surface, (x + 40, y + 110))
                else:
                    score.set_is_egg(False)
                    if dance_count <= 50 and left_to_right:
                        dance_count += 0.1
                    if dance_count > 50:
                        left_to_right = False
                    if not left_to_right and dance_count >= 0:
                        dance_count -= 0.1
                    if dance_count < 0:
                        left_to_right = True
                    x_dance = x + dance_count
                    gif[2].render(display_surface, (x_dance, y))
            else:
                gif[0].render(display_surface, (x + 40, y + 110))

        score.draw()
        pygame.display.update()
        fps_clock.tick(config.FPS)


def main():
    chicken = Chicken()
    score = Score()
    while True:
        game_start(chicken)
        game_play(chicken, score)
    pass


if __name__ == '__main__':
    main()