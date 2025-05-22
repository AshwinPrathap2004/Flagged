import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Capture The Flag")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Load clock
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# Player speed
PLAYER_SPEED = 3

# Function to restrict movement within boundaries
def keep_inside_window(player):
    player.x = max(0, min(player.x, SCREEN_WIDTH - player.width))
    player.y = max(0, min(player.y, SCREEN_HEIGHT - player.height))

# Button Class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, self.hover_color if self.rect.collidepoint(mouse_pos) else self.color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()

# Function to show victory screen
def victory_screen(winner):
    play_again_button = Button("PLAY AGAIN", 300, 300, 200, 50, GRAY, RED, start_game)
    quit_button = Button("QUIT", 300, 400, 200, 50, GRAY, RED, quit_game)

    while True:
        screen.fill(WHITE)
        victory_text = font.render(f"{winner} Wins!", True, BLACK)
        screen.blit(victory_text, (SCREEN_WIDTH // 2 - 80, 150))

        play_again_button.draw()
        quit_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            play_again_button.check_click(event)
            quit_button.check_click(event)

        pygame.display.flip()
        clock.tick(60)

# Function to start the game
def start_game():
    global player1, player2, flag1, flag2, base1, base2
    global score_p1, score_p2, holder_p1, holder_p2, flag1_captured, flag2_captured
    global obstacles

    # Reset game variables
    player1 = pygame.Rect(100, 300, 50, 50)
    player2 = pygame.Rect(650, 300, 50, 50)
    flag1 = pygame.Rect(50, 275, 20, 50)   # Red flag (Player 2's flag)
    flag2 = pygame.Rect(730, 275, 20, 50)  # Blue flag (Player 1's flag)
    base1 = pygame.Rect(70, 270, 120, 120)  # Player 1's base (Red border)
    base2 = pygame.Rect(610, 270, 120, 120)  # Player 2's base (Blue border)

    obstacles = [
        pygame.Rect(300, 150, 50, 100),
        pygame.Rect(450, 150, 50, 100),
        pygame.Rect(300, 350, 50, 100),
        pygame.Rect(450, 350, 50, 100)
    ]

    score_p1 = 0
    score_p2 = 0
    WINNING_SCORE = 3
    holder_p1 = False
    holder_p2 = False
    flag1_captured = False
    flag2_captured = False

    running = True
    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get key states
        keys = pygame.key.get_pressed()

        # Store previous positions (before moving)
        prev_p1_x, prev_p1_y = player1.x, player1.y
        prev_p2_x, prev_p2_y = player2.x, player2.y

        # Player 1 Controls (WASD)
        if keys[pygame.K_w]: player1.y -= PLAYER_SPEED
        if keys[pygame.K_s]: player1.y += PLAYER_SPEED
        if keys[pygame.K_a]: player1.x -= PLAYER_SPEED
        if keys[pygame.K_d]: player1.x += PLAYER_SPEED

        # Player 2 Controls (Arrow Keys)
        if keys[pygame.K_UP]: player2.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]: player2.y += PLAYER_SPEED
        if keys[pygame.K_LEFT]: player2.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]: player2.x += PLAYER_SPEED

        # Restrict movement within the game window
        keep_inside_window(player1)
        keep_inside_window(player2)

        # Collision with obstacles (reset to previous position if collision occurs)
        for obs in obstacles:
            if player1.colliderect(obs):
                player1.x, player1.y = prev_p1_x, prev_p1_y  # Reset Player 1 to previous position
            if player2.colliderect(obs):
                player2.x, player2.y = prev_p2_x, prev_p2_y  # Reset Player 2 to previous position

        # Flag Capture Mechanics (players take the opposite flag)
        if player1.colliderect(flag2) and not holder_p1:
            holder_p1 = True
            flag2_captured = True  # Player 1 captures Blue flag

        if player2.colliderect(flag1) and not holder_p2:
            holder_p2 = True
            flag1_captured = True  # Player 2 captures Red flag

        # Returning Flags to Base (Check if fully inside base)
        if holder_p1 and base1.contains(player1):
            score_p1 += 1
            holder_p1 = False
            flag2_captured = False  # Blue flag resets

        if holder_p2 and base2.contains(player2):
            score_p2 += 1
            holder_p2 = False
            flag1_captured = False  # Red flag resets

        # Tagging Mechanic (If players collide, drop the flag)
        if player1.colliderect(player2):
            if holder_p1:
                holder_p1 = False
                flag2_captured = False
            if holder_p2:
                holder_p2 = False
                flag1_captured = False

        # Draw Bases (with Borders)
        pygame.draw.rect(screen, RED, base1, 5)  # Red border for Player 1's base
        pygame.draw.rect(screen, BLUE, base2, 5)  # Blue border for Player 2's base

        # Draw Players
        pygame.draw.rect(screen, BLUE if holder_p1 else WHITE, player1)
        pygame.draw.rect(screen, RED if holder_p2 else WHITE, player2)
        pygame.draw.rect(screen, RED, player1, 3)  # Border for Player 1
        pygame.draw.rect(screen, BLUE, player2, 3)  # Border for Player 2

        # Draw Flags (Only if not captured)
        if not flag1_captured:
            pygame.draw.rect(screen, RED, flag1)  # Red flag for Player 2
        if not flag2_captured:
            pygame.draw.rect(screen, BLUE, flag2)  # Blue flag for Player 1

        # Draw Obstacles
        for obs in obstacles:
            pygame.draw.rect(screen, BLACK, obs)

        # Display Scores
        score_text = font.render(f"P1 Score: {score_p1}   P2 Score: {score_p2}", True, BLACK)
        screen.blit(score_text, (300, 20))

        # Check for Win Condition
        if score_p1 >= WINNING_SCORE:
            victory_screen("Player 1")
            return
        if score_p2 >= WINNING_SCORE:
            victory_screen("Player 2")
            return

        pygame.display.flip()
        clock.tick(60)

# Quit function
def quit_game():
    pygame.quit()
    sys.exit()

# Start the game
start_game()
