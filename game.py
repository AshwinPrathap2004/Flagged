import pygame
import sys

pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flagged")

# Clock
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Global dark mode flag
dark_mode = False
# Global player speed
player_speed = 3
# Global current level
current_level = "FIRE"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
LIGHT_MODE_COLOR = (255, 237, 220)  # Warm light color
DARK_MODE_COLOR = (40, 0, 48)      # Deep purple dark color
LIGHT_MODE_TEXT = (105, 2, 2)      # Deep red text for light mode

# Level-specific colors
LEVEL_COLORS = {
    "FIRE": {
        "gradient_top": (255, 165, 0),  # Orange
        "gradient_bottom": (255, 0, 0),  # Red
        "p1_color": (255, 255, 0),  # Yellow
        "p2_color": (139, 0, 0)    # Dark Red
    },
    "WATER": {
        "gradient_top": (135, 206, 235),  # Sky Blue
        "gradient_bottom": (0, 0, 255),   # Blue
        "p1_color": (0, 191, 255),  # Deep Sky Blue
        "p2_color": (0, 0, 139)     # Dark Blue
    },
    "EARTH": {
        "gradient_top": (144, 238, 144),  # Light Green
        "gradient_bottom": (0, 100, 0),   # Dark Green
        "p1_color": (34, 139, 34),   # Forest Green
        "p2_color": (139, 69, 19)    # Brown (Saddle Brown)
    },
    "WIND": {
        "gradient_top": (220, 220, 220),  # Light Gray
        "gradient_bottom": (105, 105, 105),  # Dark Gray
        "p1_color": (169, 169, 169),  # Dark Gray
        "p2_color": (47, 79, 79)      # Dark Slate Gray
    }
}

# Level-specific obstacles
LEVEL_OBSTACLES = {
    "FIRE": [
        pygame.Rect(200, 100, 50, 400),  # Vertical barrier
        pygame.Rect(550, 100, 50, 400),  # Vertical barrier
        pygame.Rect(350, 250, 100, 100)  # Center obstacle
    ],
    "WATER": [
        pygame.Rect(350, 60, 100, 100),   # Top center - moved down by 10
        pygame.Rect(350, 440, 100, 100),  # Bottom center - moved up by 10
        pygame.Rect(200, 250, 100, 100),  # Left middle
        pygame.Rect(500, 250, 100, 100)   # Right middle
    ],
    "EARTH": [
        pygame.Rect(150, 150, 100, 100),  # Top left
        pygame.Rect(550, 150, 100, 100),  # Top right
        pygame.Rect(150, 350, 100, 100),  # Bottom left
        pygame.Rect(550, 350, 100, 100),  # Bottom right
        pygame.Rect(350, 250, 100, 100)   # Center
    ],
    "WIND": [
        pygame.Rect(250, 100, 300, 30),    # Top horizontal - thinner
        pygame.Rect(250, 470, 300, 30),    # Bottom horizontal - thinner and lower
        pygame.Rect(150, 200, 30, 200),    # Left vertical - thinner and more to left
        pygame.Rect(620, 200, 30, 200),    # Right vertical - thinner and more to right
        pygame.Rect(350, 250, 80, 80)      # Smaller center obstacle
    ]
}

def get_colors():
    return (DARK_MODE_COLOR, WHITE) if dark_mode else (LIGHT_MODE_COLOR, LIGHT_MODE_TEXT)

def draw_text_center(text, y, screen, color):
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(SCREEN_WIDTH//2, y))
    screen.blit(txt, rect)

def button(rect, text, screen, text_color, bg_color, action=None):
    # Ensure contrast: Use LIGHT_MODE_COLOR in light mode for visibility
    if not dark_mode:
        bg_color = LIGHT_MODE_COLOR  # Use the light mode color for buttons
    pygame.draw.rect(screen, bg_color, rect, border_radius=5)
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, text_color, rect, 2, border_radius=5)
        if click[0] and action:
            pygame.time.delay(150)
            action()

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode

def toggle_player_speed():
    global player_speed
    if player_speed == 3:
        player_speed = 5
    elif player_speed == 5:
        player_speed = 7
    else:
        player_speed = 3

def quit_game():
    pygame.quit()
    sys.exit()

def settings_menu():
    while True:
        bg_color, text_color = get_colors()
        screen.fill(bg_color)

        draw_text_center("Settings", 100, screen, text_color)

        # Back button
        button(pygame.Rect(300, 500, 200, 50), "BACK", screen, text_color, bg_color, main_menu)

        # Dark Mode button (top-right)
        mode_text = "Light Mode" if dark_mode else "Dark Mode"
        button(pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 40), mode_text, screen, text_color, bg_color, toggle_dark_mode)
        
        # Player Speed button
        speed_text = f"Speed: {player_speed}"
        button(pygame.Rect(300, 200, 200, 50), speed_text, screen, text_color, bg_color, toggle_player_speed)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        clock.tick(60)

def draw_gradient_background(top_color, bottom_color):
    height = SCREEN_HEIGHT
    for i in range(height):
        # Calculate color for this line
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * i / height)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * i / height)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * i / height)
        pygame.draw.line(screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))

def level_select():
    global current_level
    while True:
        bg_color, text_color = get_colors()
        screen.fill(bg_color)
        draw_text_center("Select Level", 80, screen, text_color)

        levels = ["FIRE", "WATER", "EARTH", "WIND"]
        level_colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (128, 128, 128)]
        
        level_rects = []
        for i, level in enumerate(levels):
            rect = pygame.Rect(275, 150 + i * 70, 250, 50)
            level_rects.append(rect)
            
            # Draw gradient button
            gradient_top = LEVEL_COLORS[level]["gradient_top"]
            gradient_bottom = LEVEL_COLORS[level]["gradient_bottom"]
            for y in range(rect.height):
                progress = y / rect.height
                current_color = (
                    int(gradient_top[0] + (gradient_bottom[0] - gradient_top[0]) * progress),
                    int(gradient_top[1] + (gradient_bottom[1] - gradient_top[1]) * progress),
                    int(gradient_top[2] + (gradient_bottom[2] - gradient_top[2]) * progress)
                )
                pygame.draw.line(screen, current_color, 
                               (rect.left, rect.top + y), 
                               (rect.right, rect.top + y))
            
            # Add level name in the button
            level_text = font.render(level, True, WHITE)
            level_rect = level_text.get_rect(center=rect.center)
            screen.blit(level_text, level_rect)
            
            # Check for hover
            mouse = pygame.mouse.get_pos()
            if rect.collidepoint(mouse):
                pygame.draw.rect(screen, WHITE, rect, 2, border_radius=5)

        # Back button
        button(pygame.Rect(300, 500, 200, 50), "BACK", screen, text_color, bg_color, main_menu)

        # Dark mode toggle (top-right)
        mode_text = "Light Mode" if dark_mode else "Dark Mode"
        button(pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 40), mode_text, screen, text_color, bg_color, toggle_dark_mode)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(level_rects):
                    if rect.collidepoint(mouse_pos):
                        current_level = levels[i]
                        pygame.time.delay(150)
                        start_game()
                        return
        clock.tick(60)

def pause_menu():
    while True:
        bg_color, text_color = get_colors()
        screen.fill(bg_color)
        
        draw_text_center("PAUSED", 150, screen, text_color)
        
        # Resume button
        button(pygame.Rect(300, 250, 200, 50), "RESUME", screen, text_color, bg_color, lambda: None)
        
        # Quit button
        button(pygame.Rect(300, 320, 200, 50), "QUIT", screen, text_color, bg_color, quit_game)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                resume_rect = pygame.Rect(300, 250, 200, 50)
                if resume_rect.collidepoint(mouse_pos):
                    return
        clock.tick(60)

def main_menu():
    while True:
        bg_color, text_color = get_colors()
        screen.fill(bg_color)

        draw_text_center("Flagged", 100, screen, text_color)
        button(pygame.Rect(300, 200, 200, 50), "PLAY", screen, text_color, bg_color, level_select)
        button(pygame.Rect(300, 270, 200, 50), "SETTINGS", screen, text_color, bg_color, settings_menu)
        button(pygame.Rect(300, 340, 200, 50), "QUIT", screen, text_color, bg_color, quit_game)

        # Dark mode toggle (top-right)
        mode_text = "Light Mode" if dark_mode else "Dark Mode"
        button(pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 40), mode_text, screen, text_color, bg_color, toggle_dark_mode)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        clock.tick(60)

def game_over(winner):
    while True:
        bg_color, text_color = get_colors()
        screen.fill(bg_color)

        draw_text_center(f"{winner} WINS!", 200, screen, text_color)
        button(pygame.Rect(300, 300, 200, 50), "PLAY AGAIN", screen, text_color, bg_color, level_select)
        button(pygame.Rect(300, 370, 200, 50), "QUIT", screen, text_color, bg_color, quit_game)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        clock.tick(60)

def draw_score(screen, score_p1, score_p2, text_color):
    # Score box dimensions
    box_width = 40
    box_height = 40
    box_spacing = 20
    total_width = 200  # Total width of the score display
    
    # Calculate positions
    center_x = SCREEN_WIDTH // 2
    center_y = 30
    
    # Draw player labels
    p1_label = font.render("P1", True, text_color)
    p2_label = font.render("P2", True, text_color)
    
    # Position labels
    p1_rect = p1_label.get_rect(right=center_x - box_spacing - box_width - 10, centery=center_y)
    p2_rect = p2_label.get_rect(left=center_x + box_spacing + box_width + 10, centery=center_y)
    
    # Draw score boxes
    p1_box = pygame.Rect(center_x - box_spacing - box_width, center_y - box_height//2, box_width, box_height)
    p2_box = pygame.Rect(center_x + box_spacing, center_y - box_height//2, box_width, box_height)
    
    # Draw boxes
    pygame.draw.rect(screen, text_color, p1_box, 3, border_radius=5)
    pygame.draw.rect(screen, text_color, p2_box, 3, border_radius=5)
    
    # Draw dash between scores
    dash = font.render("-", True, text_color)
    dash_rect = dash.get_rect(center=(center_x, center_y))
    
    # Draw scores
    score1 = font.render(str(score_p1), True, text_color)
    score2 = font.render(str(score_p2), True, text_color)
    
    # Position scores in center of boxes
    score1_rect = score1.get_rect(center=p1_box.center)
    score2_rect = score2.get_rect(center=p2_box.center)
    
    # Draw everything
    screen.blit(p1_label, p1_rect)
    screen.blit(p2_label, p2_rect)
    screen.blit(dash, dash_rect)
    screen.blit(score1, score1_rect)
    screen.blit(score2, score2_rect)

def start_game():
    # Game variables
    # Center the bases vertically (SCREEN_HEIGHT/2 - base_height/2)
    base_height = 120
    vertical_center = SCREEN_HEIGHT//2 - base_height//2  # This will be 240 (600/2 - 120/2)
    
    # Base positions
    base1_x = 20
    base2_x = 660
    
    player1 = pygame.Rect(base1_x + 30, SCREEN_HEIGHT//2 - 25, 50, 50)  # Center player1, offset from base
    player2 = pygame.Rect(base2_x + 40, SCREEN_HEIGHT//2 - 25, 50, 50)  # Center player2, offset from base
    base1 = pygame.Rect(base1_x, vertical_center, 120, base_height)  # Left base
    base2 = pygame.Rect(base2_x, vertical_center, 120, base_height)  # Right base
    flag1 = pygame.Rect(base1_x - 20, vertical_center + 5, 20, 50)  # Left flag, consistent offset from base
    flag2 = pygame.Rect(base2_x + 120, vertical_center + 5, 20, 50)  # Right flag, consistent offset from base
    
    flag1_captured = False
    flag2_captured = False
    holder_p1 = False
    holder_p2 = False
    score_p1 = 0
    score_p2 = 0
    WINNING_SCORE = 3

    # Get level-specific obstacles
    obstacles = LEVEL_OBSTACLES[current_level]
    level_colors = LEVEL_COLORS[current_level]

    # Get dominant color for obstacles based on level
    obstacle_colors = {
        "FIRE": (255, 0, 0),      # Red
        "WATER": (0, 0, 255),     # Blue
        "EARTH": (0, 128, 0),     # Green
        "WIND": (128, 128, 128)   # Gray
    }
    obstacle_color = obstacle_colors[current_level]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()

        keys = pygame.key.get_pressed()
        prev_p1 = player1.copy()
        prev_p2 = player2.copy()

        # Player 1
        if keys[pygame.K_w]: player1.y -= player_speed
        if keys[pygame.K_s]: player1.y += player_speed
        if keys[pygame.K_a]: player1.x -= player_speed
        if keys[pygame.K_d]: player1.x += player_speed

        # Player 2
        if keys[pygame.K_UP]: player2.y -= player_speed
        if keys[pygame.K_DOWN]: player2.y += player_speed
        if keys[pygame.K_LEFT]: player2.x -= player_speed
        if keys[pygame.K_RIGHT]: player2.x += player_speed

        # Screen bounds
        player1.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        player2.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Obstacles
        for obs in obstacles:
            if player1.colliderect(obs): player1 = prev_p1
            if player2.colliderect(obs): player2 = prev_p2

        # Flags
        if player1.colliderect(flag2) and not holder_p1:
            holder_p1 = True
            flag2_captured = True
        if player2.colliderect(flag1) and not holder_p2:
            holder_p2 = True
            flag1_captured = True

        if holder_p1 and base1.contains(player1):
            score_p1 += 1
            holder_p1 = False
            flag2_captured = False

        if holder_p2 and base2.contains(player2):
            score_p2 += 1
            holder_p2 = False
            flag1_captured = False

        if player1.colliderect(player2):
            holder_p1 = holder_p2 = False
            flag1_captured = flag2_captured = False

        # Draw gradient background
        draw_gradient_background(level_colors["gradient_top"], level_colors["gradient_bottom"])

        # Draw Bases with triple borders
        # Black outer border
        pygame.draw.rect(screen, BLACK, base1.inflate(4, 4), 7)
        pygame.draw.rect(screen, BLACK, base2.inflate(4, 4), 7)
        # Colored middle border
        pygame.draw.rect(screen, level_colors["p1_color"], base1, 5)
        pygame.draw.rect(screen, level_colors["p2_color"], base2, 5)
        # Black inner border
        pygame.draw.rect(screen, BLACK, base1.inflate(-4, -4), 3)
        pygame.draw.rect(screen, BLACK, base2.inflate(-4, -4), 3)

        # Draw Players
        pygame.draw.rect(screen, level_colors["p2_color"] if holder_p1 else BLACK, player1)
        pygame.draw.rect(screen, level_colors["p1_color"], player1, 3)
        pygame.draw.rect(screen, level_colors["p1_color"] if holder_p2 else BLACK, player2)
        pygame.draw.rect(screen, level_colors["p2_color"], player2, 3)

        # Draw Flags
        if not flag1_captured:
            pygame.draw.rect(screen, level_colors["p1_color"], flag1)
        if not flag2_captured:
            pygame.draw.rect(screen, level_colors["p2_color"], flag2)

        # Draw Obstacles with color and black border
        for obs in obstacles:
            # Fill with level color
            pygame.draw.rect(screen, obstacle_color, obs)
            # Add black border
            pygame.draw.rect(screen, BLACK, obs, 2)

        # Draw Score
        draw_score(screen, score_p1, score_p2, WHITE)

        if score_p1 >= WINNING_SCORE:
            game_over("Player 1")
        elif score_p2 >= WINNING_SCORE:
            game_over("Player 2")

        pygame.display.flip()
        clock.tick(60)

# Start the game
main_menu()