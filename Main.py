import pygame
import random

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)
size = [800, 800]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Bird")
gravity = size[1] / 200000
gap = 200
bird_x = int(size[0] / 6)


class Bird:

    def __init__(self):
        self.delta = 0
        self.y = int(size[1] / 2)
        self.radius = 25

    def receive_touch(self, event):
        if event.key == 32:
            self.flap()

    def flap(self):
        self.delta = -1

    def update(self):
        self.delta += gravity
        self.y += self.delta
        if self.y + self.radius > size[1] or self.y - self.radius < 0:
            self.die()

    def check_collision(self, rect):
        circle_distance_x = abs(bird_x - rect.centerx)
        circle_distance_y = abs(self.y - rect.centery)
        if circle_distance_x > rect.width / 2.0 + self.radius or circle_distance_y > rect.height / 2.0 + self.radius:
            return False
        if circle_distance_x <= rect.width / 2.0 or circle_distance_y <= rect.h / 2.0:
            return True
        corner_x = circle_distance_x - rect.width / 2.0
        corner_y = circle_distance_y - rect.height / 2.0
        corner_distance_sq = corner_x ** 2.0 + corner_y ** 2.0
        return corner_distance_sq <= self.radius ** 2.0

    def die(self):
        reset()

    def draw(self):
        pygame.draw.circle(screen, (219, 209, 30), [bird_x, int(self.y)], self.radius)


class Tube:

    def __init__(self, cords=size[0]):
        self.x = cords
        self.passed = False
        self.width = size[1] / 16
        self.gap_top = random.randint(100, size[1] - 100 - gap)

    def update(self):
        self.x -= size[0] / 1067
        top_rect = pygame.Rect(int(self.x), 0, self.width, self.gap_top)
        bottom_rect = pygame.Rect(int(self.x), self.gap_top + gap, self.width, size[1] - (gap + self.gap_top))
        if bird.check_collision(top_rect) or bird.check_collision(bottom_rect):
            bird.die()
        if self.x < -self.width:
            global tubes
            tubes[tubes.index(self)] = Tube()
        if not self.passed and self.x + self.width < bird_x + bird.radius:
            self.passed = True
            global score
            score += 1

    def draw(self):
        top_rect = pygame.Rect(int(self.x), 0, self.width, self.gap_top)
        bottom_rect = pygame.Rect(int(self.x), self.gap_top + gap, self.width, size[1] - (gap + self.gap_top))
        pygame.draw.rect(screen, (82, 216, 115), top_rect)
        pygame.draw.rect(screen, (82, 216, 115), bottom_rect)


def draw_text(msg, color=(255, 0, 0), cords=[0, 0], size=20):
    if size == 20:
        used_font = font
    else:
        used_font = pygame.font.Font('freesansbold.ttf', size)
    text = pygame.font.Font.render(used_font, msg, True, color)
    screen.blit(text, (cords[0] - used_font.size(msg)[0] / 2, cords[1] - used_font.size(msg)[1] / 2))


def draw_gui():
    draw_text("Score: " + str(score), (0, 0, 0), [int(size[0] / 2), int(size[1] / 15)], 30)


def create_tubes():
    global tubes
    tubes = [Tube(), Tube(cords=int(size[0] * 1.5))]


def reset():
    global bird, score, tubes
    bird = Bird()
    score = 0
    create_tubes()


bird = Bird()
tubes = []
create_tubes()
score = 0

while True:
    screen.fill((30, 209, 219))
    bird.update()
    bird.draw()
    for tube in tubes:
        tube.draw()
        tube.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
        if event.type == pygame.KEYDOWN:
            bird.receive_touch(event)
    draw_gui()
    pygame.display.update()
