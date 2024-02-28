import pygame
import time
import random
import pickle
import sys

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 20

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)
heart_image = pygame.image.load('heart.png')
heart_image = pygame.transform.scale(heart_image, (20, 20))

def our_snake(snake_block, snake_List, snake_color):
    for idx, x in enumerate(snake_List):
        pygame.draw.rect(dis, snake_color[idx], [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect()
    mesg_rect.center = (dis_width // 2, dis_height // 2)
    dis.blit(mesg, mesg_rect)

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    lives = 3
    score = 0

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    while food_color == (0, 0, 0):
        food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    snake_color = [white] * Length_of_snake

    obstacles = []
    obstacle_color = red

    while not game_over:

        while game_close == True:
            dis.fill(black)
            message("You Lost! Press Q-Quit or C-Play Again", white)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            lives -= 1
            if lives < 0:
                game_close = True
            else:
                x1 = dis_width / 2
                y1 = dis_height / 2

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        pygame.draw.rect(dis, food_color, [foodx, foody, snake_block, snake_block])

        for obs in obstacles:
            pygame.draw.rect(dis, obstacle_color, obs)

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            while food_color == (0, 0, 0):
                food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            Length_of_snake += 1
            score += 10
            snake_color.append(food_color)
        else:
            snake_color.append(snake_color[0])
            del snake_color[0]

        our_snake(snake_block, snake_List, snake_color)

        # Check if the current score is a multiple of 50 and generate only one obstacle
        if score % 50 == 0 and score > 0 and len(obstacles) < score // 50:
            obs_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            obs_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            obs_size = snake_block * random.randint(1, 5)
            obstacles.append(pygame.Rect(obs_x, obs_y, obs_size, obs_size))

        for obs in obstacles:
            if snake_Head[0] in range(obs.x, obs.x + obs.width) and snake_Head[1] in range(obs.y, obs.y + obs.height):
                lives -= 1
                if lives < 0:
                    game_close = True
                else:
                    x1 = dis_width / 2
                    y1 = dis_height / 2

        # Check if the snake's head collides with any part of its body
        for part in snake_List[:-1]:
            if snake_Head[0] == part[0] and snake_Head[1] == part[1]:
                lives -= 1
                if lives < 0:
                    game_close = True
                else:
                    x1 = dis_width / 2
                    y1 = dis_height / 2

        text = score_font.render("Score: " + str(score), True, white)
        dis.blit(text, [0, 0])

        heart_width = heart_image.get_width()
        heart_offset = 5

        for i in range(lives):
            dis.blit(heart_image, [dis_width - (heart_width + heart_offset) * (i + 1), 0])

        pygame.display.update()

        clock.tick(snake_speed)

    # Save the last 10 scores
    try:
        with open("scores.pkl", "rb") as f:
            scores = pickle.load(f)
    except FileNotFoundError:
        scores = []

    def text_input(font, color, surf, text='', max_length=20):
        input_box = pygame.Rect(dis_width // 2 - 100, dis_height // 2, 200, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        done = False
        text = ''

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        elif len(text) < max_length:
                            text += event.unicode

            surf.fill((0, 0, 0))
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            surf.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(surf, color, input_box, 2)
            pygame.display.flip()

        return text


    # Ask the user for their name
    message("Game Over! Enter your name:", white)
    pygame.display.update()
    name = text_input(score_font, white, dis)


    scores.append((name, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    scores = scores[:10]

    with open("scores.pkl", "wb") as f:
        pickle.dump(scores, f)

    # Display the leaderboard
    dis.fill(black)
    font = pygame.font.Font(None, 36)
    text = font.render("Leaderboard:", True, white)
    dis.blit(text, (dis_width // 2 - text.get_width() // 2, 50))

    for i, (name, score) in enumerate(scores):
        text = font.render(f"{i + 1}. {name}: {score}", True, white)
        dis.blit(text, (dis_width // 2 - text.get_width() // 2, 100 + i * 40))

    pygame.display.update()
    pygame.display.flip()
    pygame.time.wait(10000)  # Show the leaderboard for 10 seconds

    pygame.quit()
    sys.exit()

gameLoop()
