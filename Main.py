import pygame
import random
import time

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)
size = [1000, 600]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Bird")
gap = size[1] / 4
bird_x = int(size[0] / 6)


class Bird:

    def __init__(self):
        self.weights = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        self.delta = 0
        self.y = int(size[1] / 2)
        self.radius = int(size[1] / 32)
        self.final_distance = 0

    def receive_touch(self, event):
        if event.key == 32:
            self.flap()

    def flap(self):
        self.delta = -size[1] / 55 / 2

    def update(self):
        self.delta += gravity
        self.y += self.delta
        if self.y + self.radius > size[1] or self.y - self.radius < 0:
            self.die()
        self.check_collision()

    def decide(self):
        first_col = [tubes[0].x + tubes[0].width / 2 - bird_x,
                     tubes[1].x + tubes[1].width / 2 - bird_x,
                     tubes[0].gap_top + gap / 2 - self.y,
                     tubes[0].gap_top + gap / 2 - self.y,
                     self.y]
        output_col = [0, 0]
        for x in range(len(self.weights)):
            for i in range(len(self.weights[x])):
                output_col[x] += first_col[i] * self.weights[x][i]
        if output_col[0] > output_col[1]:
            self.flap()

    def check_collision(self):
        rects = tubes[0].rects
        temp = tubes[1].rects
        rects.append(temp[0])
        rects.append(temp[1])
        for rect in rects:
            if intersects(rect, self.radius, [bird_x, self.y]):
                self.die()

    def die(self):
        self.final_distance = score
        try:
            birds.remove(self)
            dead_birds.append(self)
        except ValueError:
            pass

    def randomize_weights(self):
        for x in self.weights:
            for i in range(len(x)):
                x[i] = random.randint(0, 100) / 100.0

    def draw(self):
        pygame.draw.circle(screen, (219, 209, 30), [bird_x, int(self.y)], self.radius)


class Tube:

    def __init__(self, cords=size[0]):
        self.x = cords
        self.passed = False
        self.width = size[1] / 16
        self.gap_top = random.randint(int(size[1] / 6), int(size[1] / 6 * 5 - gap))
        top_rect = pygame.Rect(int(self.x), 0, self.width, self.gap_top)
        bottom_rect = pygame.Rect(int(self.x), self.gap_top + gap, self.width, size[1] - (gap + self.gap_top))
        self.rects = [top_rect, bottom_rect]

    def update(self):
        self.x -= int(size[0] / 45 / 2)  # 1067
        top_rect = pygame.Rect(int(self.x), 0, self.width, self.gap_top)
        bottom_rect = pygame.Rect(int(self.x), self.gap_top + gap, self.width, size[1] - (gap + self.gap_top))
        self.rects = [top_rect, bottom_rect]
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
    draw_text("FPS:" + str(int(clock.get_fps() * 10) / 10.0), (255, 75, 75), [size[0] / 10 * 9, size[1] / 10 * 9])


def create_tubes():
    global tubes
    tubes = [Tube(), Tube(cords=int(size[0] * 1.5))]


def reset():
    global birds, score, tubes, dead_birds
    score = 0
    create_tubes()
    birds = []
    dead_birds = []
    for f in range(75):
        birds.append(Bird())
    randomize_weights()


def randomize_weights():
    for bird in birds:
        bird.randomize_weights()


def intersects(rect, r, center):
    circle_distance_x = abs(center[0]-rect.centerx)
    circle_distance_y = abs(center[1]-rect.centery)
    if circle_distance_x > rect.w/2.0+r or circle_distance_y > rect.h/2.0+r:
        return False
    if circle_distance_x <= rect.w/2.0 or circle_distance_y <= rect.h/2.0:
        return True
    corner_x = circle_distance_x-rect.w/2.0
    corner_y = circle_distance_y-rect.h/2.0
    corner_distance_sq = corner_x**2.0 +corner_y**2.0
    return corner_distance_sq <= r**2.0


birds = []
dead_birds = []
for f in range(200):
    birds.append(Bird())
tubes = []
create_tubes()
score = 0
clock = pygame.time.Clock()
clock.tick(1)
gravity = size[1] / 55 / 45
randomize_weights()
last_time = time.time()


while True:
    screen.fill((30, 209, 219))
    if len(birds) == 0:
        reset()
    for bird in birds:
        if time.time() - last_time > 0.05:
            bird.decide()
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
            # bird.receive_touch(event)
            pass
    draw_gui()
    pygame.display.update()
    clock.tick(30)

