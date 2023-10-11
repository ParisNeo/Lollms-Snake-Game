import pygame
import random
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SNAKE_SIZE = 20
SNAKE_SPEED = 5
SNAKE_COLOR = (255, 0, 0)  # Red
FOOD_COLOR = (0, 255, 0)  # Green
WALL_COLOR = (255, 0, 0)  # Red
WALL_THICKNESS = 1
WALL_POSITIONS = [
    # Top wall
    (0, 0, WINDOW_WIDTH // SNAKE_SIZE, WALL_THICKNESS),
    # Bottom wall
    (0, WINDOW_HEIGHT // SNAKE_SIZE - WALL_THICKNESS, WINDOW_WIDTH // SNAKE_SIZE, WALL_THICKNESS),
    # Left wall
    (0, 0, WALL_THICKNESS, WINDOW_HEIGHT // SNAKE_SIZE),
    # Right wall
    (WINDOW_WIDTH // SNAKE_SIZE - WALL_THICKNESS, 0, WALL_THICKNESS, WINDOW_HEIGHT // SNAKE_SIZE)
]
class Snake:
    def __init__(self):
        self.body = [(WINDOW_WIDTH // 2 // SNAKE_SIZE, WINDOW_HEIGHT // 2 // SNAKE_SIZE)]
        self.direction = "right"
        self.lives = 3
    def move(self):
        x, y = self.body[0]
        if self.direction == "up":
            y -= 1
        elif self.direction == "down":
            y += 1
        elif self.direction == "left":
            x -= 1
        elif self.direction == "right":
            x += 1
        self.body.insert(0, (x, y))
        self.body.pop()
    def check_collision(self):
        x, y = self.body[0]
        if (
            x < WALL_THICKNESS
            or x >= WINDOW_WIDTH // SNAKE_SIZE - WALL_THICKNESS
            or y < WALL_THICKNESS
            or y >= WINDOW_HEIGHT // SNAKE_SIZE - WALL_THICKNESS
            or (x, y) in self.body[1:]
        ):
            return True
        return False
class Food:
    def __init__(self):
        self.position = self.generate_position()
    def generate_position(self):
        x = random.randint(WALL_THICKNESS, WINDOW_WIDTH // SNAKE_SIZE - WALL_THICKNESS - 1)
        y = random.randint(WALL_THICKNESS, WINDOW_HEIGHT // SNAKE_SIZE - WALL_THICKNESS - 1)
        return x, y
def draw_walls(window):
    for wall_position in WALL_POSITIONS:
        x, y, width, height = wall_position
        pygame.draw.rect(window, WALL_COLOR, (x * SNAKE_SIZE, y * SNAKE_SIZE, width * SNAKE_SIZE, height * SNAKE_SIZE))
def draw_score(window, score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score: {}".format(score), True, (255, 255, 255))
    text_rect = text.get_rect(bottomright=(WINDOW_WIDTH - 20, WINDOW_HEIGHT - 20))
    window.blit(text, text_rect)
def draw_lives(window, lives):
    font = pygame.font.Font(None, 36)
    text = font.render("Lives: {}".format("H" * lives), True, (255, 255, 255))
    text_rect = text.get_rect(bottomright=(WINDOW_WIDTH - 20, WINDOW_HEIGHT - 50))
    window.blit(text, text_rect)
def restart_game(snake, food):
    snake.body = [(WINDOW_WIDTH // 2 // SNAKE_SIZE, WINDOW_HEIGHT // 2 // SNAKE_SIZE)]
    snake.direction = "right"
    food.position = food.generate_position()
def game_over(window, score):
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over! Score: {}".format(score), True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)
def play_game():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != "down":
                    snake.direction = "up"
                elif event.key == pygame.K_DOWN and snake.direction != "up":
                    snake.direction = "down"
                elif event.key == pygame.K_LEFT and snake.direction != "right":
                    snake.direction = "left"
                elif event.key == pygame.K_RIGHT and snake.direction != "left":
                    snake.direction = "right"
        snake.move()
        if snake.check_collision():
            snake.lives -= 1
            if snake.lives == 0:
                game_over(window, score)
                running = False
            else:
                restart_game(snake, food)
        if snake.body[0] == food.position:
           snake.body.append((0, 0))  # Add a new body segment
           food.position = food.generate_position()
           score += 1
        window.fill((0, 0, 0))  # Clear the window
        draw_walls(window)  # Draw walls
        draw_score(window, score)  # Draw score
        draw_lives(window, snake.lives)  # Draw lives
        # Draw snake and food
        for segment in snake.body:
            x, y = segment
            pygame.draw.rect(window, SNAKE_COLOR, (x * SNAKE_SIZE, y * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE))
        pygame.draw.rect(window, FOOD_COLOR, (food.position[0] * SNAKE_SIZE, food.position[1] * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE))
        pygame.display.update()
        clock.tick(10)  # Limit the frame rate to 10 FPS
    pygame.quit()
play_game()
