import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 20, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 6

# Ball
BALL_RADIUS = 7
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)
ball_speed_x = 3 * random.choice((1, -1))
ball_speed_y = 3 * random.choice((1, -1))

# Bricks
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 20
bricks = [pygame.Rect(c * BRICK_WIDTH, r * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT) for r in range(BRICK_ROWS) for c in range(BRICK_COLS)]

# Score
score = 0

# Main game loop
running = True
clock = pygame.time.Clock()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = WIDTH // 2
    ball.y = HEIGHT // 2
    ball_speed_x = 3 * random.choice((1, -1))
    ball_speed_y = 3 * random.choice((1, -1))

lives = 3

while running and lives > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-paddle_speed, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(paddle_speed, 0)

    ball.move_ip(ball_speed_x, ball_speed_y)

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1

    if ball.colliderect(paddle):
        ball_speed_y *= -1

    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        hit_rect = bricks.pop(hit_index)
        if abs(ball.bottom - hit_rect.top) < 10 or abs(ball.top - hit_rect.bottom) < 10:
            ball_speed_y *= -1
        else:
            ball_speed_x *= -1
        score += 1

    if ball.bottom >= HEIGHT:
        lives -= 1
        reset_ball()

        if lives <= 0:
            break  # Exit the game loop if lives are exhausted

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)
    pygame.display.flip()
    clock.tick(60)

# Save the score to a file when the game ends
with open("score.txt", "w") as file:
    file.write(str(score))

pygame.quit()
sys.exit()


