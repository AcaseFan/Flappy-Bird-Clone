import sys
import pygame
import random

pygame.init()


# Game Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

GRAVITY = 9.8 * 100

SKY_BLUE = (87, 165, 229)


HOLE_SIZE = 200


class Bird:
    POS_X = 250
    BIRD_RADIUS = 30
    JUMP_VELOCITY = 700

    def __init__(self) -> None:
        self.pos_y = 300
        self.vel_y = 0
        self.reduce_hitbox = 2
        self.sprite = pygame.image.load("sprites/bird.png")

    def update(self, delta_time):
        self.pos_y += self.vel_y * delta_time
        self.vel_y += (GRAVITY * delta_time) * 2.5

        # Bird bounding box for collision detection
        self.bleft, self.btop = (
            self.POS_X - self.BIRD_RADIUS + self.reduce_hitbox,
            self.pos_y - self.BIRD_RADIUS + self.reduce_hitbox,
        )  # -5 to make the game easier

        self.bird_rect = pygame.Rect(
            self.bleft, self.btop, self.BIRD_RADIUS * 2, self.BIRD_RADIUS * 2
        )

    def draw(self):
        pygame.draw.circle(
            window,
            pygame.Color("white"),
            (self.POS_X, self.pos_y),
            self.BIRD_RADIUS,
        )
        window.blit(self.sprite, (self.POS_X - 41, self.pos_y - 30))

    def jump(self):
        self.vel_y = -self.JUMP_VELOCITY

    def reset(self):
        self.pos_y = 300
        self.vel_y = 0


class Pipes:
    VEL_X = 200
    WIDTH = 100

    def __init__(self) -> None:
        self.pos_x = SCREEN_WIDTH + self.WIDTH + 10
        self.hole_pos_y = random.randint(220, 420)
        self.scored = False
        self.sprite_top = pygame.image.load("sprites/top_pipe.png")
        self.sprite_bottom = pygame.image.load("sprites/bottom_pipe.png")

        # Rects:
        self.bottom_pipe_Rect = pygame.Rect(
            self.pos_x, self.hole_pos_y + HOLE_SIZE / 2, Pipes.WIDTH, 400
        )

        self.top_pipe_Rect = pygame.Rect(
            self.pos_x, -10, Pipes.WIDTH, self.hole_pos_y - HOLE_SIZE / 2
        )

    def update(self, delta_time):
        self.pos_x -= self.VEL_X * delta_time
        # update rects and their bounding boxes:
        #   TOP PIPE
        self.top_pipe_Rect = pygame.Rect(
            self.pos_x, -10, Pipes.WIDTH, self.hole_pos_y - HOLE_SIZE / 2
        )
        # BOTTOM PIPE
        self.bottom_pipe_Rect = pygame.Rect(
            self.pos_x, self.hole_pos_y + HOLE_SIZE / 2, Pipes.WIDTH, 400
        )

    def draw(self):
        # pygame.draw.rect(window, pygame.Color("green"), self.top_pipe_Rect)
        # # debug circle
        # pygame.draw.circle(window, pygame.Color(
        #     'red'), (self.pos_x, self.hole_pos_y), 5)
        # pygame.draw.rect(window, pygame.Color("green"), self.bottom_pipe_Rect)
        window.blit(self.sprite_bottom, (self.pos_x, self.hole_pos_y + HOLE_SIZE / 2))
        window.blit(
            self.sprite_top, (self.pos_x, (self.hole_pos_y - HOLE_SIZE / 2) - 330 - 10)
        )
        # 330 ker je to visina teksture


class Menu:
    def __init__(self) -> None:
        self.menu_x = (SCREEN_WIDTH * 0.2) / 2
        self.menu_y = SCREEN_HEIGHT / 4
        self.menu_width = SCREEN_WIDTH * 0.8
        self.menu_height = SCREEN_HEIGHT / 2
        self.menu_Rect = pygame.Rect(
            self.menu_x, self.menu_y, self.menu_width, self.menu_height
        )

    def draw(self):
        pygame.draw.rect(window, pygame.Color("BROWN"), self.menu_Rect, 0, 50)


class Text:
    def __init__(self, text, pos_x, pos_y, color):
        self.text = text
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.color = color

        self.font = pygame.font.Font(None, 72)
        self.text_render = self.font.render(str(self.text), True, self.color)

        self.rect = self.text_render.get_rect()
        self.rect.center = (self.pos_x, self.pos_y)

    def update(self, text_updated):
        self.text_render = self.font.render(str(text_updated), True, self.color)

        self.rect = self.text_render.get_rect()
        self.rect.center = (self.pos_x, self.pos_y)

    def draw(self):
        window.blit(self.text_render, self.rect)


class Game:
    PIPES_PER_SECOND = 1.5 * 1000

    def __init__(self) -> None:
        self.pipes = []  # shrani vec cevi
        self.time_since_last_pipe = pygame.time.get_ticks()
        self.bird = Bird()
        self.menu = Menu()
        self.state = "STARTED"
        self.score = 0
        self.game_over_time = 0

        self.score_text = Text(
            self.score, SCREEN_WIDTH // 2, 100, pygame.Color("Black")
        )

        self.game_over_text = Text(
            "FINAL SCORE:",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 125,
            pygame.Color("Black"),
        )
        self.quit_text = Text(
            "PRESS ESC TO QUIT",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 125,
            pygame.Color("Black"),
        )

    def draw(self):
        for pipe in self.pipes:
            pipe.draw()

        # Draw ground
        pygame.draw.rect(
            window,
            pygame.Color("brown"),
            pygame.Rect(
                0, SCREEN_HEIGHT - SCREEN_HEIGHT / 10, SCREEN_WIDTH, SCREEN_HEIGHT / 10
            ),
        )

        # draw hole_Rect (debug)
        self.bird.draw()

        if self.state == "STOPPED":
            self.menu.draw()
            self.game_over_text.draw()
            self.quit_text.draw()
        self.score_text.draw()

    def update(self):
        if self.state == "RUNNING":
            self.bird.update(delta_time)

            # Spawnaj Pipe vsake x sekunde
            now = pygame.time.get_ticks()
            if now - self.time_since_last_pipe > self.PIPES_PER_SECOND:
                self.pipes.append(Pipes())
                self.time_since_last_pipe = now

            # updataj and unici cevi in preveri ce se ptic dotika cevi
            for pipe in self.pipes[:]:
                pipe.update(delta_time)
                if pipe.pos_x + Pipes.WIDTH < 0:
                    self.pipes.remove(pipe)

                if not pipe.scored and (pipe.pos_x + pipe.WIDTH / 2) < self.bird.POS_X:
                    self.score += 1
                    pipe.scored = True

                    self.score_text.update(self.score)
                self.collision_with_pipe(pipe)
            # if bird_collision == True:
            self.collision_with_ground()

            self.score_text.text = self.score

    def collision_with_ground(self):
        if self.bird.pos_y > SCREEN_HEIGHT - SCREEN_HEIGHT / 10 - self.bird.BIRD_RADIUS:
            self.game_over()

    def collision_with_pipe(self, pipe):
        # bottom pipe
        if (
            self.bird.pos_y < 0
            and pipe.pos_x <= self.bird.POS_X <= pipe.pos_x + pipe.WIDTH
        ):
            self.game_over()
        # top pipe
        if self.bird.bird_rect.colliderect(
            pipe.top_pipe_Rect
        ) or self.bird.bird_rect.colliderect(pipe.bottom_pipe_Rect):
            self.game_over()

    def reset(self):
        self.pipes.clear()
        self.score = 0
        self.score_text.pos_y = 100
        self.bird.reset()
        self.state = "RUNNING"
        self.score_text.update(self.score)

    def game_over(self):
        self.state = "STOPPED"
        self.game_over_time = pygame.time.get_ticks()
        self.score_text.pos_y = SCREEN_HEIGHT // 2 - 50
        self.score_text.update(self.score)


window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

clock = pygame.time.Clock()


game = Game()

game.bird.pos_y = 300
game.bird.vel_y = 0

prev_time = pygame.time.get_ticks() / 1000
delta_time = 0

cooldown = 2


# Game loop
while True:
    BACKGROUND_IMG = pygame.image.load("sprites/background.png").convert()
    # limit framerate
    # izracunaj delta time
    now = pygame.time.get_ticks() / 1000
    delta_time = now - prev_time
    prev_time = now
    # print(f"NOW: {now} | PREV_TIME: {prev_time}| DELTA_TIME {delta_time}")
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.UIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game.state == "STARTED":
                    game.state = "RUNNING"
                    game.bird.jump()
                if game.state == "STOPPED":
                    if pygame.time.get_ticks() - game.game_over_time > 250:
                        game.reset()
                        game.bird.jump()
                else:
                    game.bird.jump()
            if game.state == "STOPPED":
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    game.bird.jump()

    game.update()
    # 3. Drawing
    # window.fill(SKY_BLUE)

    window.blit(BACKGROUND_IMG, (0, 0))
    game.draw()

    pygame.display.flip()
    clock.tick(FPS)
