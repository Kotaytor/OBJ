import pygame
import random
import sys

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

#прыжок и кувырок
player = pygame.image.load('nikoluk_s_pivom_kastrirovaniy.png')
image_rect = player.get_rect(center=(screen_width - 20, screen_height - line_offset))
angle = 0
moving_up = False
moving_down = False
move_speed = 2

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
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                moving_up = True

    # передвижение игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and image_rect.x > player_radius:
        image_rect.x -= player_speed
    elif keys[pygame.K_RIGHT] and image_rect.x < screen_width - player_radius:
        image_rect.x += player_speed
    elif keys[pygame.K_UP] and image_rect.y > player_radius:
        image_rect.y -= player_speed
    elif keys[pygame.K_DOWN] and image_rect.y < screen_height - player_radius:
        image_rect.y += player_speed
        
    if moving_up:
        angle += 10
        if angle >= 360:
            angle = 0
            moving_up = False
        image_rect.y -= move_speed
        if image_rect.y < 50:
            moving_up = False
    if not moving_up and image_rect.y < 300:
        image_rect.y += move_speed

    # проверка столкновений игрока со стенами
    player_rect = pygame.Rect(image_rect.x - player_radius, image_rect.y - player_radius, player_radius * 2, player_radius * 2)
    for line in lines:
        if line.colliderect(player_rect):
            # в случае столкновения возвращаем игрока назад
            if image_rect.x > line.left and image_rect.x < line.right:
                if image_rect.y < line.top:
                    image_rect.y = line.top - player_radius
                else:
                    image_rect.y = line.bottom + player_radius
            elif image_rect.y > line.top and image_rect.y < line.bottom:
                if image_rect.x < line.left:
                    image_rect.x = line.left - player_radius
                else:
                    image_rect.x = line.right + player_radius
    screen.fill(black)
    for line in lines:
        pygame.draw.rect(screen, green, line)

    screen.blit(player, image_rect.topleft)
    screen.blit(pivko, pivo_rect)

    rotated_image = pygame.transform.rotate(player, angle)
    new_rect = rotated_image.get_rect(center=image_rect.center)
    screen.blit(rotated_image, new_rect.topleft)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)