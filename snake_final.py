import pygame
import sys
import random
import time
from game_constants import CONSTANTS

window = pygame.display.set_mode((CONSTANTS.SCREEN_WIDTH, CONSTANTS.SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Stasiak The Snake')


def game_init():
    pygame.init()
    pygame.font.init()
    pygame.mixer.music.load(".\\media\\sounds\\SoWet.mp3")
    pygame.mixer.music.play(loops=100, start=0.0, fade_ms=0)
    pygame.mixer.music.set_volume(0)


def load_image(image_name):
    return pygame.image.load(image_name).convert_alpha()


# Define the Hero class
class Hero:
    background_image = CONSTANTS.IMAGE_PNG_PATH_BY_NAME['background_image']
    background = load_image(background_image)

    def __init__(self, x, y, name):
        self.image = load_image(name)
        self.x, self.y = x, y
        self.chosen_direction = pygame.K_RIGHT
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.body = [(x, y, self.rect)]  # list of body elements
        self.last_time_press_key = pygame.time.get_ticks()
        self.move_distance_in_pixels = 35

    def _choose_direction(self):
        keys_pressed = pygame.key.get_pressed()
        if self.chosen_direction == pygame.K_RIGHT:
            if keys_pressed[pygame.K_UP]:
                self.chosen_direction = pygame.K_UP
            elif keys_pressed[pygame.K_DOWN]:
                self.chosen_direction = pygame.K_DOWN
        elif self.chosen_direction == pygame.K_LEFT:
            if keys_pressed[pygame.K_UP]:
                self.chosen_direction = pygame.K_UP
            elif keys_pressed[pygame.K_DOWN]:
                self.chosen_direction = pygame.K_DOWN
        elif self.chosen_direction == pygame.K_UP:
            if keys_pressed[pygame.K_RIGHT]:
                self.chosen_direction = pygame.K_RIGHT
            elif keys_pressed[pygame.K_LEFT]:
                self.chosen_direction = pygame.K_LEFT
        elif self.chosen_direction == pygame.K_DOWN:
            if keys_pressed[pygame.K_RIGHT]:
                self.chosen_direction = pygame.K_RIGHT
            elif keys_pressed[pygame.K_LEFT]:
                self.chosen_direction = pygame.K_LEFT

    def add_body_when_eat(self, object_to_collide):
        # collision between food and snake
        if self.rect.colliderect(object_to_collide):
            # self.body.insert(0, (self.x, self.y))
            body_elem_rect = self.image.get_rect(topleft=(self.x, self.y))
            self.body.append((self.x, self.y, body_elem_rect))
        # collision between snake and itself
        else:
            self.head_body_collide()

    def head_body_collide(self):
        for body_elem in self.body[1:]:
            if self.rect.colliderect(body_elem[2]):
                enemies.reset_extra_enemy()  # reset bonus enemy
                time.sleep(3)
                self.reset_snake()

    def snake_last_element_delete(self):
        self.body.pop()

    def reset_snake(self):
        self.x = random.randint(0, CONSTANTS.SCREEN_WIDTH - 20)
        self.y = random.randint(0, CONSTANTS.SCREEN_HEIGHT - 20)
        self.body = [(self.x, self.y, self.rect)]
        main_menu.game_over()

    def _move_player(self):
        if self.chosen_direction == pygame.K_LEFT:
            self.x -= self.move_distance_in_pixels
        elif self.chosen_direction == pygame.K_RIGHT:
            self.x += self.move_distance_in_pixels
        elif self.chosen_direction == pygame.K_UP:
            self.y -= self.move_distance_in_pixels
        elif self.chosen_direction == pygame.K_DOWN:
            self.y += self.move_distance_in_pixels
        rect = self.image.get_rect(topleft=(self.x, self.y))
        self.body.insert(0, (self.x, self.y, rect))
        self.body.pop()

    def _handle_border_crossing(self):
        if self.x >= CONSTANTS.SCREEN_WIDTH:
            self.x = 1
        if self.x <= 0:
            self.x = CONSTANTS.SCREEN_WIDTH
        if self.y >= CONSTANTS.SCREEN_HEIGHT:
            self.y = 1
        if self.y <= 0:
            self.y = CONSTANTS.SCREEN_HEIGHT

    def moving(self):
        self._choose_direction()
        self._move_player()
        self._handle_border_crossing()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def render(self):
        window.blit(Hero.background, (0, 0))
        for pos in self.body:
            window.blit(self.image, (pos[0], pos[1]))

    def hero_execute_functions(self, object_to_interact):
        self.moving()
        self.render()
        self.add_body_when_eat(object_to_interact)


# Define the enemy class to create food for snake
class Enemy:
    points = 0

    def __init__(self, x, y, name, wall, text_font):
        self.name = name
        self.enemy = load_image(self.name)
        self.text_font = text_font
        self.random_enemy = random.choice(list(CONSTANTS.ENEMY_PNG_PATH_BY_ENEMY_NAME.values()))
        self.extra_enemy_1 = load_image(self.random_enemy)
        self.wall = pygame.image.load(wall)
        self.wall_rect = self.wall.get_rect(topleft=(0, 240))
        self.x, self.y = x, y
        # self.points = points
        self.chance_for_extra_enemy = 0
        self.x_extra, self.y_extra = random.randint(0, CONSTANTS.SCREEN_WIDTH - 20), random.randint(0,
                                                                                                    CONSTANTS.SCREEN_HEIGHT - 20)
        self.timer = 10
        self.dt = 0
        self.extra_enemy_1_rect = self.extra_enemy_1.get_rect(topleft=(self.x_extra, self.y_extra))
        self.rect = self.enemy.get_rect(topleft=(x, y))

    def render(self):
        window.blit(self.enemy, self.rect)
        self.render_extra_enemy()
        points_to_blit = self.text_font.render(str(Enemy.points), False, (0, 0, 0))
        window.blit(points_to_blit, (0, 0))

    def reset_extra_enemy(self):
        self.timer = 10
        self.chance_for_extra_enemy = 0
        print('did')

    def collision(self, object_to_collide):
        if self.rect.colliderect(object_to_collide):
            self.x, self.y = random.randint(0, CONSTANTS.SCREEN_WIDTH - 20), random.randint(0,
                                                                                            CONSTANTS.SCREEN_HEIGHT - 20)
            self.rect = self.enemy.get_rect(topleft=(self.x, self.y))
            window.blit(self.enemy, self.rect)
            self.chance_for_extra_enemy = random.randint(1, 3)
            Enemy.points += random.randint(1, 7)
            # reset timer
            self.timer = 10
            # enemy randomization
            self.random_enemy = random.choice(list(CONSTANTS.ENEMY_PNG_PATH_BY_ENEMY_NAME.values()))
            self.extra_enemy_1 = load_image(self.random_enemy)
            # back to standard background
            Hero.background_image = CONSTANTS.IMAGE_PNG_PATH_BY_NAME['background_image']
            Hero.background = load_image(Hero.background_image)
            # back to standard enemy photo
            self.enemy = load_image(self.name)

    def render_extra_enemy(self):
        clock = pygame.time.Clock()
        if self.chance_for_extra_enemy == 3:
            window.blit(self.extra_enemy_1, self.extra_enemy_1_rect)
            self.timer -= self.dt
            self.dt = clock.tick(CONSTANTS.FPS_AMOUNT) / 1000
            time_to_catch = self.text_font.render(str(round(self.timer, 2)), True, (252, 3, 44))
            window.blit(time_to_catch, (250, 0))
            pygame.display.update()
            if self.timer <= 0:
                self.timer = 10
                self.chance_for_extra_enemy = 0

    def extra_enemy_collision(self, object_to_collide):
        if self.extra_enemy_1_rect.colliderect(object_to_collide) and self.chance_for_extra_enemy == 3:
            self.random_enemy = random.choice(list(CONSTANTS.ENEMY_PNG_PATH_BY_ENEMY_NAME.values()))
            self.extra_enemy_1 = load_image(self.random_enemy)
            self.x_extra, self.y_extra = random.randint(0, CONSTANTS.SCREEN_WIDTH - 20), random.randint(0,
                                                                                                        CONSTANTS.SCREEN_HEIGHT - 20)
            self.extra_enemy_1_rect = self.extra_enemy_1.get_rect(topleft=(self.x_extra, self.y_extra))
            self.chance_for_extra_enemy = 0
            Enemy.points += random.randint(5, 20)

    def norbi_cougars(self, object_to_collide):
        grannies = [CONSTANTS.IMAGE_PNG_PATH_BY_NAME['babcia_1'],
                    CONSTANTS.IMAGE_PNG_PATH_BY_NAME['babcia_1'],
                    CONSTANTS.IMAGE_PNG_PATH_BY_NAME['babcia_1'],
                    CONSTANTS.IMAGE_PNG_PATH_BY_NAME['babcia_1']]
        random_granny = random.choice(list(grannies))
        if self.extra_enemy_1_rect.colliderect(
                object_to_collide) and self.random_enemy == CONSTANTS.ENEMY_PNG_PATH_BY_ENEMY_NAME[
            'norbi'] and self.chance_for_extra_enemy == 3:
            self.enemy = load_image(random_granny)


    def stefan_collision(self, object_to_collide):
        if self.extra_enemy_1_rect.colliderect(
                object_to_collide) and self.random_enemy == CONSTANTS.ENEMY_PNG_PATH_BY_ENEMY_NAME[
            'stefan'] and self.chance_for_extra_enemy == 3:
            my_hero.snake_last_element_delete()

    def enemy_with_minus_points(self, object_to_collide):
        if self.extra_enemy_1_rect.colliderect(
                object_to_collide) and self.random_enemy == CONSTANTS.ENEMY_PNG_PATH_BY_ENEMY_NAME[
            'pema'] and self.chance_for_extra_enemy == 3:
            Enemy.points -= 100

    def alan_screen(self, object_to_collide):
        if self.extra_enemy_1_rect.colliderect(
                object_to_collide) and self.random_enemy == CONSTANTS.ENEMY_PNG_PATH_BY_ENEMY_NAME[
            'alan'] and self.chance_for_extra_enemy == 3:
            Hero.background_image = CONSTANTS.IMAGE_PNG_PATH_BY_NAME['alan_background']
            Hero.background = load_image(Hero.background_image)

    def wall_colision(self, object_to_collide):
        wall_points = Enemy.points
        if 50 <= wall_points <= 100:
            window.blit(self.wall, self.wall_rect)
            if self.wall_rect.colliderect(object_to_collide):
                my_hero.reset_snake()
                main_menu.game_over()

    def execute_functions_enemy(self, my_object):
        self.render()
        self.collision(my_object)
        self.enemy_with_minus_points(my_object)
        self.alan_screen(my_object)
        self.norbi_cougars(my_object)
        self.stefan_collision(my_object)
        self.extra_enemy_collision(my_object)


class Main_menu:

    def __init__(self, text_font):
        self.button_colors = (255, 255, 255)
        self.button_colors_marked = (153, 145, 145)
        self.text_font = text_font

    def create_text(self, text, position, button_colors_tmp=(255, 255, 255)):
        text_to_create = self.text_font.render(text, False, button_colors_tmp)
        text_to_create_rect = text_to_create.get_rect(center=position)
        window.blit(text_to_create, text_to_create_rect)
        return text_to_create_rect

    def is_menu_button_clicked(self, text, position_a, position_b):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text_to_create_rect = self.create_text(text, (position_a, position_b))
        if text_to_create_rect.collidepoint((mouse_x, mouse_y)):
            shake_position_a, shake_position_b = random.randint(position_a - 1, position_a + 1), \
                                                 random.randint(position_b - 1, position_b + 1)
            shake_positions = (shake_position_a, shake_position_b)
            self.create_text(text, shake_positions, self.button_colors_marked)
            if pygame.mouse.get_pressed()[0]:
                return True

    def is_func_executed(self, text, position_a, position_b):
        is_func_clicked = self.is_menu_button_clicked(text, position_a, position_b)
        if is_func_clicked:
            return True

    def start_menu(self):
        while True:
            for event_menu in pygame.event.get():
                if event_menu.type == pygame.QUIT:
                    sys.exit()
            window.fill((0, 0, 0))
            window.blit(load_image(CONSTANTS.IMAGE_PNG_PATH_BY_NAME['snake_logo']), (0, 20))
            is_game_started = self.is_func_executed("new game", 230, 300)
            is_game_quit = self.is_func_executed("quit", 230, 350)
            if is_game_started:
                Enemy.points = 0
                return True
            if is_game_quit:
                sys.exit()
            pygame.display.update()

    def game_over(self):
        while True:
            for event_game_over in pygame.event.get():
                if event_game_over.type == pygame.QUIT:
                    sys.exit()
            window.fill((0, 0, 0))
            self.create_text("GAME OVER", (200, 20))
            score_display = self.text_font.render(f"You've scored {Enemy.points} points. Congratulations",
                                                  False,
                                                  (255, 255, 255))
            window.blit(score_display, (100, 300))
            is_game_restarted = self.is_func_executed("restart", 200, 120)
            if is_game_restarted:
                return self.start_menu()
            pygame.display.update()


class Boss_stage:

    def __init__(self):
        self.boss = load_image(CONSTANTS.IMAGE_PNG_PATH_BY_NAME['boss'])
        self.x, self.y = -10, -10
        self.boss_rect = self.boss.get_rect(topleft=(self.x, self.y))
        self.points_to_spawn = 70

    def render(self):
        if Enemy.points >= self.points_to_spawn:
            window.blit(self.boss, self.boss_rect)

    def boss_running(self):
        if Enemy.points >= self.points_to_spawn:
            self.x += 3
            self.y -= 3
        self.boss_rect = self.boss.get_rect(topleft=(self.x, self.y))

    def _handle_border_crossing(self):
        if Enemy.points >= self.points_to_spawn:
            if self.x >= CONSTANTS.SCREEN_WIDTH:
                self.x = 1
            if self.x <= 0:
                self.x = CONSTANTS.SCREEN_WIDTH
            if self.y >= CONSTANTS.SCREEN_HEIGHT:
                self.y = 1
            if self.y <= 0:
                self.y = CONSTANTS.SCREEN_HEIGHT

    def boss_collision(self, object_to_collide):
        if self.boss_rect.colliderect(object_to_collide) and Enemy.points >= self.points_to_spawn:
            enemies.reset_extra_enemy()  # reset bonus enemy
            time.sleep(2)
            my_hero.reset_snake()
            main_menu.game_over()

    def execute_boss_functions(self, object_to_collide):
        self.boss_running()
        self._handle_border_crossing()
        self.boss_collision(object_to_collide)
        self.render()


def main_game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        fps = pygame.time.Clock()
        my_hero.hero_execute_functions(enemies)
        enemies.execute_functions_enemy(my_hero)
        boss.execute_boss_functions(my_hero)
        pygame.display.update()
        fps.tick(CONSTANTS.FPS_AMOUNT)


if __name__ == '__main__':
    # random_enemy = random.choice(list(CONSTANTS.ENEMY_PNG_PATH_BY_ENEMY_NAME.values()))
    game_init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    boss = Boss_stage()
    my_hero = Hero(0, 0, CONSTANTS.IMAGE_PNG_PATH_BY_NAME['stasiak'])
    enemies = Enemy(random.randint(0, CONSTANTS.SCREEN_WIDTH - 20),
                    random.randint(0, CONSTANTS.SCREEN_HEIGHT - 20),
                    CONSTANTS.IMAGE_PNG_PATH_BY_NAME['chwaster'],
                    CONSTANTS.ENEMY_PNG_PATH_BY_ENEMY_NAME['alan'], font)
    main_menu = Main_menu(font)
    is_game_started = main_menu.start_menu()
    if is_game_started:
        print('fdfds')
        main_game_loop()


