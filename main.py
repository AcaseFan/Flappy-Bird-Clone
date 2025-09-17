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

BIRD_POS_X = 250
BIRD_RADIUS = 30
JUMP_VELOCITY = 750


HOLE_SIZE = 200

font = pygame.font.Font(None, 74)
text = font.render("COLLISION", True, (255, 255, 255))


class Bird:
    def __init__(self) -> None:
        self.pos_y = 300
        self.vel_y = 0

    def update(self, delta_time):
        self.pos_y += self.vel_y * delta_time
        self.vel_y += (GRAVITY*delta_time) * 2.5

        # Bird bounding box for collision detection
        self.bleft, self.btop = BIRD_POS_X - BIRD_RADIUS, self.pos_y - BIRD_RADIUS

        self.bird_rect = pygame.Rect(
            self.bleft,
            self.btop,
            BIRD_RADIUS * 2,
            BIRD_RADIUS * 2
        )

    def draw(self):

        pygame.draw.circle(window, pygame.Color('white'),
                           (BIRD_POS_X, self.pos_y), BIRD_RADIUS)

    def jump(self):
        self.vel_y = -JUMP_VELOCITY


class Pipes:
    VEL_X = 200
    WIDTH = 100

    def __init__(self) -> None:
        self.pos_x = SCREEN_WIDTH + self.WIDTH + 10
        self.hole_pos_y = random.randint(220, 420)
        self.scored = False

        # Rects:
        self.bottom_pipe_Rect = pygame.Rect(
            self.pos_x, self.hole_pos_y + HOLE_SIZE/2, Pipes.WIDTH, 400)

        self.top_pipe_Rect = pygame.Rect(
            self.pos_x, -10, Pipes.WIDTH, self.hole_pos_y - HOLE_SIZE/2)

    def update(self, delta_time):
        self.pos_x -= self.VEL_X * delta_time
        # update rects and their bounding boxes:
        #   TOP PIPE
        self.top_pipe_Rect = pygame.Rect(
            self.pos_x, -10, Pipes.WIDTH, self.hole_pos_y - HOLE_SIZE/2)
        # BOTTOM PIPE
        self.bottom_pipe_Rect = pygame.Rect(
            self.pos_x, self.hole_pos_y + HOLE_SIZE/2, Pipes.WIDTH, 400)

    def draw(self):
        pygame.draw.rect(window, pygame.Color('green'), self.top_pipe_Rect)
        # # debug circle
        # pygame.draw.circle(window, pygame.Color(
        #     'red'), (self.pos_x, self.hole_pos_y), 5)
        pygame.draw.rect(window, pygame.Color('green'), self.bottom_pipe_Rect)


class Game:
    PIPES_PER_SECOND = 1.5 * 1000

    def __init__(self) -> None:
        self.pipes = []  # shrani vec cevi
        self.time_since_last_pipe = pygame.time.get_ticks()
        self.bird = Bird()
        self.state = "START"
        self.score = 0

    def draw(self):
        for pipe in self.pipes:
            pipe.draw()

        # Draw ground
        pygame.draw.rect(window, pygame.Color('brown'), pygame.Rect(
            0, SCREEN_HEIGHT - SCREEN_HEIGHT/10, SCREEN_WIDTH, SCREEN_HEIGHT/10))

        # draw hole_Rect (debug)
        self.bird.draw()

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
                    continue

                if not pipe.scored and (pipe.pos_x + pipe.WIDTH/2) < BIRD_POS_X:
                    self.score += 1
                    pipe.scored = True
                    print(self.score)
                self.collision_with_pipe(pipe)
            # if bird_collision == True:
            self.collision_with_ground()

            # collision between the pipes and the bird_pos_y

    def collision_with_ground(self):
        if self.bird.pos_y > SCREEN_HEIGHT - SCREEN_HEIGHT/10 - BIRD_RADIUS:
            print("COLLISION WITH GROUND")

    def collision_with_pipe(self, pipe):
        if self.bird.pos_y < 0 and pipe.pos_x <= BIRD_POS_X <= pipe.pos_x + pipe.WIDTH:
            print("Bird is off-screen and over a pipe")

        # Bird collides with a pipe
        if self.bird.bird_rect.colliderect(pipe.top_pipe_Rect) or self.bird.bird_rect.colliderect(pipe.bottom_pipe_Rect):
            print("COLLISION WITH PIPE")

    def collision_with_holeRect(self, pipe):
        if self.bird.bird_rect.colliderect(pipe.hole_Rect):
            return True
        # game over state


window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

BIRD_UPDATE = pygame.USEREVENT
clock = pygame.time.Clock()


game = Game()

game.bird.pos_y = 300
game.bird.vel_y = 0

prev_time = pygame.time.get_ticks() / 1000
delta_time = 0


# Game loop
while True:
    # limit framerate
    # izracunaj delta time
    now = pygame.time.get_ticks() / 1000
    delta_time = now - prev_time
    prev_time = now
    # print(f"NOW: {now} | PREV_TIME: {prev_time}| DELTA_TIME {delta_time}")
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game.state != 'RUNNING':
                    game.state = 'RUNNING'
                game.bird.jump()
    # 2. Updating
    game.update()

    # 3. Drawing
    window.fill(SKY_BLUE)

    game.draw()

    pygame.display.update()
    clock.tick(FPS)
