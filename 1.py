import pygame
import sys
import random
import math

pygame.init()

width = 500
height = 500

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pacman")
clock = pygame.time.Clock()

pygame.init()


class Agrogame:
    def __init__(self):
        self.pacman_color = (255, 255, 0)
        self.pacman_size = 10
        self.pacman_x = 250
        self.pacman_y = 250
        self.pacman_speed = 2
        self.score = 0
        self.game_over = False
        self.win = False

        self.food_color = (255, 0, 0)
        self.food_size = 10
        self.food_radius = self.food_size / 2
        self.foods = []
        self._create_food()

        self.bush_color = (0, 128, 0)
        self.bush_radius = 15
        self.bush_positions = [
            (50, 50), (450, 50),
            (50, 450), (450, 450),
            (150, 150), (350, 150),
            (150, 350), (350, 350)
        ]

        self.enemy_color = (0, 0, 0)
        self.enemy_size = random.randint(5, 30)
        self.enemy_radious = self.enemy_size / 2
        self.enemies = []
        self._create_enemies()

    def _create_food(self):
        for _ in range(50):
            food_x = random.randint(0, width - self.food_size)
            food_y = random.randint(0, height - self.food_size)
            self.foods.append(pygame.Rect(food_x, food_y, self.food_size, self.food_size))

    def _create_enemies(self):
        for _ in range(3):
            enemy_x = random.randint(0, width - self.enemy_size)
            enemy_y = random.randint(0, height - self.enemy_size)
            self.enemies.append(pygame.Rect(enemy_x, enemy_y, self.enemy_size, self.enemy_size))

    def run_game(self):
        while True:
            if not self.game_over and not self.win:
                window.fill((100, 202, 0))
                self._check_events()
                self._update_pacman()
                self._update_enemies()
                self._check_food_collision()
                self._check_enemy_collision()
                self._update_window()
            clock.tick(30)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _update_pacman(self):
        keys = pygame.key.get_pressed()
        next_x = self.pacman_x
        next_y = self.pacman_y
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if next_x > mouse_x:
            next_x -= self.pacman_speed
        if next_x < mouse_x:
            next_x += self.pacman_speed
        if next_y > mouse_y:
            next_y -= self.pacman_speed
        if next_y < mouse_y:
            next_y += self.pacman_speed

        self.pacman_x = next_x
        self.pacman_y = next_y

        if self.score >= 30:
            self.win = True

    def _update_enemies(self):
            if self.pacman_size <= self.enemy_size:
                for enemy in self.enemies:
                    if self.pacman_x < enemy.x:
                        enemy.x -= 1
                    elif self.pacman_x > enemy.x:
                        enemy.x += 1
                    if self.pacman_y < enemy.y:
                        enemy.y -= 1
                    elif self.pacman_y > enemy.y:
                        enemy.y += 1

    def _check_food_collision(self):
        pacman_rect = pygame.Rect(self.pacman_x - self.pacman_size / 2, self.pacman_y - self.pacman_size / 2,
                                   self.pacman_size, self.pacman_size)
        for food in self.foods[:]:
            if pacman_rect.colliderect(food):
                self.score += 1
                self.foods.remove(food)
                self._add_food()
                self.pacman_size += 1

    def _check_enemy_collision(self):
        pacman_rect = pygame.Rect(self.pacman_x - self.pacman_size / 2, self.pacman_y - self.pacman_size / 2,
                                   self.pacman_size, self.pacman_size)
        for enemy in self.enemies:
            if pacman_rect.colliderect(enemy):
                if self.pacman_size > self.enemy_size:
                    self.enemies.remove(enemy)
                    self._add_enemy()
                    self.pacman_size += 10
                    self.score += 2
                else:
                    self.game_over = True

    def _add_food(self):
        food_x = random.randint(0, width - self.food_size)
        food_y = random.randint(0, height - self.food_size)
        self.foods.append(pygame.Rect(food_x, food_y, self.food_size, self.food_size))

    def _add_enemy(self):
        self.enemy_size = random.randint(20, 100)
        self.enemy_radious = self.enemy_size / 2
        enemy_x = random.randint(0, width - self.enemy_size)
        enemy_y = random.randint(0, height - self.enemy_size)
        self.enemies.append(pygame.Rect(enemy_x, enemy_y, self.enemy_size, self.enemy_size))

    def _update_window(self):
        pygame.draw.circle(window, self.pacman_color, (self.pacman_x, self.pacman_y), self.pacman_size // 2)
        for food in self.foods:
            pygame.draw.circle(window, self.food_color, (food.x, food.y), self.food_radius)
        for pos in self.bush_positions:
            pygame.draw.circle(window, self.bush_color, pos, self.bush_radius)
        for enemy in self.enemies:
            pygame.draw.circle(window, self.enemy_color, (enemy.x, enemy.y), self.enemy_radious)
        font = pygame.font.SysFont(None, 50)
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        window.blit(score_text, (10, 10))
        if self.game_over:
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            window.blit(game_over_text, (200, 200))
        if self.win:
            win_text = font.render("WIN!!!", True, (80, 80, 255))
            window.blit(win_text, (200, 200))

        pygame.display.flip()

game = Agrogame()
game.run_game()