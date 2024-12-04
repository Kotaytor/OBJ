import pygame
import random

pygame.init()

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Николюк: погоня за пивком')

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

#прыжок и кувырок
player_image = pygame.image.load('nikoluk_s_pivom_kastrirovaniy.png')
pos = [screen_width/2, screen_height/2]
speed = 10
initialPos = pos[1]
size = 150
rotateForce = 10
image = player_image
_image = image
jumpForce = 100
isKuvyrok = False
jumpPos = pos[1]
up = False
angle = rotateForce
isFlip = False
isRight = True
rotated_image = image
new_rect = rotated_image.get_rect(center = image.get_rect().center)
force = 10

# параметры стен и дверей
line_width = 10
line_gap = 150
line_offset = 20
door_width = 50
door_gap = 70
max_openings_per_line = 1

#стартовая позиция пивка
pivko = pygame.image.load('pivko.png').convert_alpha()
pivo_x = screen_width - 1895
pivo_y = screen_height - line_offset
pivo_rect = pivko.get_rect(center=(pivo_x, pivo_y))
screen.blit(pivko, pivo_rect)

# параметры и стартовая позиция николюка
player_radius = 23
player_speed = 10
player_x = screen_width - 20
player_y = screen_height - line_offset

# рисуем стены и двери
lines = []
for i in range(screen_width, 0, -line_gap):
    rect = pygame.Rect(i, 0, line_width, screen_height)
    num_openings = random.randint(1, max_openings_per_line)
    if num_openings == 1:
        # одна дверь посередине стены
        door_pos = random.randint(line_offset + door_width, screen_height - line_offset - door_width)
        lines.append(pygame.Rect(i, 0, line_width, door_pos - door_width))
        lines.append(pygame.Rect(i, door_pos + door_width, line_width, screen_height - door_pos - door_width))
    else:
        # несколько дверей
        opening_positions = [0] + sorted([random.randint(line_offset + door_width, screen_height - line_offset - door_width) for _ in range(num_openings-1)]) + [screen_height]
        for j in range(num_openings):
            lines.append(pygame.Rect(i, opening_positions[j], line_width, opening_positions[j+1]-opening_positions[j]-door_width))
pivo_y = door_pos
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # передвижение игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > player_radius:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < screen_width - player_radius:
        player_x += player_speed
    elif keys[pygame.K_UP] and player_y > player_radius:
        player_y -= player_speed
    elif keys[pygame.K_DOWN] and player_y < screen_height - player_radius:
        player_y += player_speed

    if isKuvyrok:
        rotated_image = pygame.transform.rotate(_image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = (pos[0] - size/2, pos[1] - size/2)).center)
        angle += rotateForce
        if angle >= 360:
            angle = 0
            isKuvyrok = False

    elif pos[1] != jumpPos and up:
        pos[1] -= speed
        if pos[1] == jumpPos:
            up = False
            isKuvyrok = True

    elif not up and pos[1] != initialPos:
        pos[1] += speed

    elif(pos[1] == initialPos and jumpPos != initialPos):
        jumpPos = initialPos

    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if(jumpPos == initialPos):
                        jumpPos = initialPos - jumpForce
                        up = True
                if event.key == pygame.K_DOWN:
                    isKuvyrok = True



    # проверка столкновений игрока со стенами
    player_rect = pygame.Rect(player_x - player_radius, player_y - player_radius, player_radius * 2, player_radius * 2)
    for line in lines:
        if line.colliderect(player_rect):
            # в случае столкновения возвращаем игрока назад
            if player_x > line.left and player_x < line.right:
                if player_y < line.top:
                    player_y = line.top - player_radius
                else:
                    player_y = line.bottom + player_radius
            elif player_y > line.top and player_y < line.bottom:
                if player_x < line.left:
                    player_x = line.left - player_radius
                else:
                    player_x = line.right + player_radius
    screen.fill(black)
    for line in lines:
        pygame.draw.rect(screen, green, line)
    player_rect = player_image.get_rect(center=(player_x, player_y))
    screen.blit(player_image, player_rect)

    pivko = pygame.image.load('pivko.png').convert_alpha()
    screen.blit(pivko, pivo_rect)
    if player_rect.colliderect(pivo_rect):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if(jumpPos == initialPos):
                        jumpPos = initialPos - jumpForce
                        up = True
                if event.key == pygame.K_DOWN:
                    isKuvyrok = True
    pygame.display.update()
    clock.tick(60)