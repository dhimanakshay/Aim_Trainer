import math
import random
import time
import pygame

# Initialize the game
pygame.init()

# Set up the display window dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

# Timing and event constants
TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30

# Basic game settings
BG_COLOR = (0, 25, 40)
LIVES = 3
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

# Available colors and shapes for the targets
TARGET_COLORS = ["red", "green", "blue", "yellow", "purple"]
TARGET_SHAPES = ["circle", "square", "triangle", "star"]

# Target class with different shapes and colors
class Target:
    MAX_SIZE = 30  # Maximum size the target can grow
    GROWTH_RATE = 0.2  # Rate at which the target grows

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0  # Initial size of the target
        self.grow = True  # Indicates if the target is growing
        self.color = random.choice(TARGET_COLORS)  # Random color for each target
        self.shape = random.choice(TARGET_SHAPES)  # Random shape for each target

    # Update the size of the target as it grows and shrinks
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False  # Stop growing when it reaches max size

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    # Draw the target with its assigned shape and color
    def draw(self, win):
        if self.shape == "circle":
            pygame.draw.circle(win, self.color, (self.x, self.y), self.size)
        elif self.shape == "square":
            pygame.draw.rect(win, self.color, (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2))
        elif self.shape == "triangle":
            pygame.draw.polygon(win, self.color, [
                (self.x, self.y - self.size),
                (self.x - self.size, self.y + self.size),
                (self.x + self.size, self.y + self.size)
            ])
        elif self.shape == "star":
            self.draw_star(win)

    # Method to draw a star shape
    def draw_star(self, win):
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            r = self.size if i % 2 == 0 else self.size / 2
            x = self.x + r * math.cos(angle)
            y = self.y + r * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(win, self.color, points)

    # Check if the target is clicked
    def collide(self, x, y):
        if self.shape == "circle":
            distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
            return distance <= self.size
        elif self.shape == "square":
            return self.x - self.size <= x <= self.x + self.size and self.y - self.size <= y <= self.y + self.size
        elif self.shape == "triangle" or self.shape == "star":
            distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
            return distance <= self.size  # Basic collision for now

# Helper function to draw all targets on the screen
def draw(win, targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)

# Format time for display
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}.{milli}"

# Draw the top bar to show the player's stats
def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "black")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))

# Show the end screen when the game is over and offer a choice to play again or quit
def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")
    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")
    play_again_label = LABEL_FONT.render(
        "Press R to Play Again or Q to Quit", 1, "white")

    # Display game stats
    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))
    win.blit(play_again_label, (get_middle(play_again_label), 500))

    pygame.display.update()

    run = True
    # Wait for the user to either restart the game or quit
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart the game
                elif event.key == pygame.K_q:
                    return False  # Quit the game

# Function to get the center position of the text on the screen
def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2

# The main game function
def main():
    while True:
        # Game variables reset for each session
        run = True
        targets = []
        clock = pygame.time.Clock()
        targets_pressed = 0
        clicks = 0
        misses = 0
        start_time = time.time()

        # Create new targets every 400ms
        pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

        while run:
            clock.tick(60)  # Run the game at 60 frames per second
            click = False
            mouse_pos = pygame.mouse.get_pos()
            elapsed_time = time.time() - start_time

            # Process events (mouse clicks, target spawning, etc.)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if event.type == TARGET_EVENT:
                    x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                    y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                    target = Target(x, y)
                    targets.append(target)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                    clicks += 1

            # Update and remove targets
            for target in targets:
                target.update()
                if target.size <= 0:
                    targets.remove(target)
                    misses += 1
                if click and target.collide(*mouse_pos):
                    targets.remove(target)
                    targets_pressed += 1

            # If the player misses too many targets, show the end screen
            if misses >= LIVES:
                play_again = end_screen(WIN, elapsed_time, targets_pressed, clicks)
                if play_again:
                    main()  # Restart the game
                else:
                    pygame.quit()
                    quit()

            # Update the screen with the current game state
            draw(WIN, targets)
            draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    main()
