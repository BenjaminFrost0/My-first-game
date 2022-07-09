import pygame

from random import randint
from Ball import Ball

pygame.mixer.pre_init(44100, -16, 1, 512)

pygame.init()
# звуки и фоновая музыка
pygame.mixer.music.load("music/chicken.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
s = pygame.mixer.Sound("music/chegg.ogg")
s.set_volume(100)

# время цикла
pygame.time.set_timer(pygame.USEREVENT, 2000)

# дисплей
W = 1000
H = 570
sc = pygame.display.set_mode((W, H), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("Падающие яйца")

# цвета
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
# основные переменные
FPS = 60
HP = 5
speed = 1
game_score = 0
# надписи и изображения(фон, корзина, сердечко)
g = pygame.font.SysFont('aril', 30)
heart = pygame.image.load("images/heart.png")
scorefon = pygame.image.load('images/scorefon.png')
korzina = pygame.image.load('images/korzina.png').convert_alpha()
bg = pygame.image.load('images/fon.png')
k_rect = korzina.get_rect(centerx=W // 2, bottom=H - 5)
bg_rect = bg.get_rect(center=(W // 2, H // 2))
# база яичек
balls_data = ({'path': 'egg.png', 'score': 100},
              {'path': 'egg1.png', 'score': 150},
              {'path': 'egg2.png', 'score': 200})
balls_surf = [pygame.image.load('images/' + data['path']).convert_alpha() for data in balls_data]

# создает яйца
def createBall(group):
    indx = randint(0, len(balls_surf) - 1)
    x1 = randint(20, 2000)
    speed = randint(1, 5)

    return Ball(x1, speed, balls_surf[indx], balls_data[indx]['score'], group, HP)

# собирает яйца и зачисляет очки
def collideBalls():
    global game_score
    for ball in balls:
        if k_rect.collidepoint(ball.rect.center):
            game_score += ball.score
            s.play()
            ball.kill()

# снимает HP
def minusHp():
    global HP
    for ball in balls:
        if ball.rect.y > H - 21:
            HP -= 1


speed = 10
balls = pygame.sprite.Group()
createBall(balls)
# главный цикл
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            createBall(balls)
            # движение корзинки
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        k_rect.x -= speed
        if k_rect.x < 0:
            k_rect.x = 0
    elif keys[pygame.K_d]:
        k_rect.x += speed
        if k_rect.x > W - k_rect.width:
            k_rect.x = W - k_rect.width

    collideBalls()
    minusHp()
    # создание всех надписей и изображений
    sc.fill(BLACK)
    sc.blit(bg, bg_rect)
    sc.blit(korzina, k_rect)
    sc.blit(scorefon, (0, 0))
    sc.blit(heart, (870, -90))
    sc_HP = g.render(str(HP), 1, BLACK)
    sc.blit(sc_HP, (959, 24))
    sc_text = g.render(str(game_score), 1, BLACK)
    sc.blit(sc_text, (20, 40))
     # условие Game Over
    if HP < 1:
        sc_over = g.render("GAME OVER", 1, BLACK)
        sc_space = g.render("Нажмите пробел, чтобы начать с начала", 1, BLACK)
        sc.blit(sc_over, (W - 550, H // 2))
        sc.blit(sc_space, (W - 650, H // 2 + 30))
        # нчать с начала
        if keys[pygame.K_SPACE]:
            HP = 5
            game_score = 0

    balls.draw(sc)
    pygame.display.update()

    clock.tick(FPS)

    balls.update(H)
