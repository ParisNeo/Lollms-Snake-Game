import pygame
import random
import time
from pygame import mixer

# 🎭 Setting up our interdimensional circus! 🎭
pygame.init()
mixer.init()

# 🎨 Colors from parallel dimensions!
RAINBOW_COLORS = [(255,0,0), (255,165,0), (255,255,0), (0,255,0), (0,0,255), (75,0,130), (238,130,238)]
PINK = (255, 192, 203)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 🎪 Setting up our quantum playground!
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Quantum Snake's Interdimensional Adventure! 🌀")

class SnakeParty:
    def __init__(self):
        # 🎯 Basic quantum coordinates
        self.snake_pos = [[WIDTH//2, HEIGHT//2]]
        self.snake_dir = [BLOCK_SIZE, 0]
        self.score = 0
        self.lives = 3
        self.highscore = self.load_highscore()
        self.game_over = False
        self.clock = pygame.time.Clock()
        
        # 🎉 Fun quantum fluctuations!
        self.party_mode = False
        self.snake_speed = 10
        self.invincible = False
        self.invincible_timer = 0
        self.effect_timer = 0
        self.message_timer = 0
        self.current_message = ""
        
        # 🌀 Portal messages for dimensional travel!
        self.portal_messages = [
            "WHOOSH! Portal power!",
            "Through the wormhole!",
            "Quantum tunneling snake!",
            "Who needs walls anyway?",
            "Snake goes brrrrrrr!",
        ]
        
        # 🎨 Shape Menu of Interdimensional Delights!
        self.food_types = [
            {
                "name": "Pizza",
                "shape": "triangle",
                "color": (255, 140, 0),
                "points": 1,
                "effect": "normal",
                "message": "Triangle food! Geometry is tasty!"
            },
            {
                "name": "Burger",
                "shape": "circle",
                "color": (139, 69, 19),
                "points": 2,
                "effect": "speed",
                "message": "ZOOM ZOOM! Round food makes snake go FAST!"
            },
            {
                "name": "Star",
                "shape": "star",
                "color": (255, 215, 0),
                "points": 15,
                "effect": "star",
                "message": "STAR POWER! Temporary immortality acquired!"
            },
            {
                "name": "Ice Cream",
                "shape": "diamond",
                "color": (255, 192, 203),
                "points": -1,
                "effect": "freeze",
                "message": "Brrrr! Cold shapes are cold!"
            },
            {
                "name": "Magic Cookie",
                "shape": "square",
                "color": (210, 105, 30),
                "points": 5,
                "effect": "giant",
                "message": "Square snack make snake THICC!"
            }
        ]
        
        # 🎭 Special Effects!
        self.effects = {
            "normal": lambda: None,
            "speed": lambda: setattr(self, 'snake_speed', min(30, self.snake_speed + 2)),
            "party": lambda: setattr(self, 'party_mode', True),
            "freeze": lambda: setattr(self, 'snake_speed', max(5, self.snake_speed - 2)),
            "giant": lambda: self.snake_pos.extend([self.snake_pos[-1]] * 3),
            "star": self.activate_star_power
        }
        
        # 🍽️ First food spawn in this dimension
        self.food_pos = self.spawn_food()
        self.current_food = random.choice(self.food_types)

    def activate_star_power(self):
        self.invincible = True
        self.invincible_timer = 100  # 10 seconds of POWER!

    def load_highscore(self):
        try:
            with open('snake_highscore.txt', 'r') as f:
                return int(f.read())
        except:
            return 0

    def save_highscore(self):
        if self.score > self.highscore:
            with open('snake_highscore.txt', 'w') as f:
                f.write(str(self.score))
            return True
        return False

    def wrap_position(self, pos):
        x, y = pos
        wrapped = False
        if x < 0:
            x = WIDTH - BLOCK_SIZE
            wrapped = True
        elif x >= WIDTH:
            x = 0
            wrapped = True
        if y < 0:
            y = HEIGHT - BLOCK_SIZE
            wrapped = True
        elif y >= HEIGHT:
            y = 0
            wrapped = True
            
        if wrapped:
            self.current_message = random.choice(self.portal_messages)
            self.message_timer = 20
        return [x, y]

    def check_self_collision(self):
        head = self.snake_pos[0]
        return head in self.snake_pos[1:]

    def spawn_food(self):
        self.current_food = random.choice(self.food_types)
        return [random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE),
                random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)]

    def draw_snake(self):
        for i, pos in enumerate(self.snake_pos):
            color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
            pygame.draw.rect(screen, color, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            
            # 👀 Googly eyes for dimensional awareness
            if i == 0:
                pygame.draw.circle(screen, WHITE, (pos[0] + 5, pos[1] + 5), 3)
                pygame.draw.circle(screen, WHITE, (pos[0] + 15, pos[1] + 5), 3)
                pygame.draw.circle(screen, BLACK, (pos[0] + 5, pos[1] + 5), 1)
                pygame.draw.circle(screen, BLACK, (pos[0] + 15, pos[1] + 5), 1)

    def draw_food(self):
        x, y = self.food_pos[0], self.food_pos[1]
        
        if self.current_food["shape"] == "triangle":
            points = [(x + BLOCK_SIZE//2, y), 
                     (x, y + BLOCK_SIZE),
                     (x + BLOCK_SIZE, y + BLOCK_SIZE)]
            pygame.draw.polygon(screen, self.current_food["color"], points)
        
        elif self.current_food["shape"] == "circle":
            pygame.draw.circle(screen, self.current_food["color"],
                             (x + BLOCK_SIZE//2, y + BLOCK_SIZE//2),
                             BLOCK_SIZE//2)
        
        elif self.current_food["shape"] == "star":
            points = [(x + BLOCK_SIZE//2, y),
                     (x + BLOCK_SIZE, y + BLOCK_SIZE//2),
                     (x + BLOCK_SIZE//2, y + BLOCK_SIZE),
                     (x, y + BLOCK_SIZE//2)]
            pygame.draw.polygon(screen, self.current_food["color"], points)
            # Add sparkles because STARS SPARKLE!
            for _ in range(4):
                spark_x = x + random.randint(0, BLOCK_SIZE)
                spark_y = y + random.randint(0, BLOCK_SIZE)
                pygame.draw.circle(screen, WHITE, (spark_x, spark_y), 1)
        
        elif self.current_food["shape"] == "diamond":
            points = [(x + BLOCK_SIZE//2, y),
                     (x + BLOCK_SIZE, y + BLOCK_SIZE//2),
                     (x + BLOCK_SIZE//2, y + BLOCK_SIZE),
                     (x, y + BLOCK_SIZE//2)]
            pygame.draw.polygon(screen, self.current_food["color"], points)
        
        else:  # square and anything else
            pygame.draw.rect(screen, self.current_food["color"],
                           (x, y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Food wiggle effect
        if random.random() < 0.1:
            pygame.draw.circle(screen, WHITE,
                             (x + BLOCK_SIZE//2, y + BLOCK_SIZE//2), 2)

    def show_message(self, text, size, color, pos):
        font = pygame.font.Font(None, size)
        message = font.render(text, True, color)
        screen.blit(message, pos)

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake_dir != [0, BLOCK_SIZE]:
                        self.snake_dir = [0, -BLOCK_SIZE]
                    if event.key == pygame.K_DOWN and self.snake_dir != [0, -BLOCK_SIZE]:
                        self.snake_dir = [0, BLOCK_SIZE]
                    if event.key == pygame.K_LEFT and self.snake_dir != [BLOCK_SIZE, 0]:
                        self.snake_dir = [-BLOCK_SIZE, 0]
                    if event.key == pygame.K_RIGHT and self.snake_dir != [-BLOCK_SIZE, 0]:
                        self.snake_dir = [BLOCK_SIZE, 0]
                    if event.key == pygame.K_SPACE:
                        self.party_mode = not self.party_mode
                        self.snake_speed = 20 if self.party_mode else 10

            # Move through the quantum field!
            new_head = [self.snake_pos[0][0] + self.snake_dir[0],
                       self.snake_pos[0][1] + self.snake_dir[1]]
            new_head = self.wrap_position(new_head)
            self.snake_pos.insert(0, new_head)

            # Nom nom check
            if (abs(self.snake_pos[0][0] - self.food_pos[0]) < BLOCK_SIZE and 
                abs(self.snake_pos[0][1] - self.food_pos[1]) < BLOCK_SIZE):
                self.score += self.current_food["points"]
                self.current_message = self.current_food["message"]
                self.message_timer = 30
                self.effects[self.current_food["effect"]]()
                self.effect_timer = 100
                self.food_pos = self.spawn_food()
            else:
                self.snake_pos.pop()

            # Update star power timer
            if self.invincible:
                self.invincible_timer -= 1
                if self.invincible_timer <= 0:
                    self.invincible = False
                    self.current_message = "Star power fading... back to being mortal!"
                    self.message_timer = 30

            # Self-nom check (unless STAR POWER!)
            if not self.invincible and self.check_self_collision():
                self.lives -= 1
                if self.lives <= 0:
                    new_high = self.save_highscore()
                    message = "NEW HIGH SCORE! " if new_high else ""
                    self.show_message(f"{message}GAME OVER, YOU SILLY PRETZEL! 🥨", 
                                    74, PINK, (WIDTH//4, HEIGHT//2))
                    pygame.display.flip()
                    time.sleep(2)
                    self.game_over = True
                else:
                    self.snake_pos = [[WIDTH//2, HEIGHT//2]]
                    self.snake_dir = [BLOCK_SIZE, 0]
                    self.current_message = f"OOF! {self.lives} lives left! No self-eating!"
                    self.message_timer = 30

            # Draw everything in this dimension!
            screen.fill(BLACK)
            
            # Party mode quantum fluctuations!
            if self.party_mode:
                for i in range(10):
                    x = random.randrange(0, WIDTH)
                    y = random.randrange(0, HEIGHT)
                    pygame.draw.circle(screen, random.choice(RAINBOW_COLORS), (x, y), 2)

            self.draw_snake()
            self.draw_food()

            # Show messages and score
            if self.message_timer > 0:
                self.show_message(self.current_message, 36, PINK, (WIDTH//3, 50))
                self.message_timer -= 1

            # Show score, lives, and highscore
            self.show_message(f"Quantum Points: {self.score} ✨", 
                            36, GOLD, (10, 10))
            self.show_message(f"Lives: {'❤️ ' * self.lives}", 
                            36, PINK, (10, 40))
            self.show_message(f"High Score: {self.highscore} 👑", 
                            36, GOLD, (10, 70))
            
            # Party mode announcement
            if self.party_mode:
                self.show_message("QUANTUM PARTY TIME!", 
                                36, random.choice(RAINBOW_COLORS), (WIDTH//2 - 100, 10))

            # Star power timer and effects
            if self.invincible:
                timer_width = (self.invincible_timer / 100) * 200
                pygame.draw.rect(screen, GOLD, 
                               (WIDTH//2 - 100, HEIGHT - 20, timer_width, 10))
                self.show_message(f"STAR POWER: {self.invincible_timer//10}s", 
                                36, GOLD, (WIDTH//2 - 80, HEIGHT - 40))
                
                # Sparkles around invincible snake!
                head = self.snake_pos[0]
                for _ in range(4):
                    spark_x = head[0] + random.randint(-20, 20)
                    spark_y = head[1] + random.randint(-20, 20)
                    pygame.draw.circle(screen, GOLD, (spark_x, spark_y), 2)

            pygame.display.flip()
            self.clock.tick(self.snake_speed)

if __name__ == "__main__":
    print("🌀 Welcome to QUANTUM SNAKE'S INTERDIMENSIONAL ADVENTURE! 🌀")
    print("🎮 Arrow keys: Navigate through dimensions!")
    print("🎉 Space bar: Toggle QUANTUM PARTY MODE!")
    print("\n🎨 Interdimensional Menu:")
    print("  △ Triangle - Just a slice of spacetime!")
    print("  ○ Circle - Speed boost through dimensions!")
    print("  ⭐ Star - Temporary immortality (10s)!")
    print("  ◇ Diamond - Quantum cooling effect!")
    print("  □ Square - Grow big across parallel universes!")
    print("\n❤️ You have 3 lives - Don't create temporal paradoxes!")
    print("👑 Break the interdimensional high score!")
    print("🌀 Pro tip: Walls are actually portals!")
    
    game = SnakeParty()
    game.run()
    pygame.quit()
