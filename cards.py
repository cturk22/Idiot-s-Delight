import pygame
import sys
import os
import matplotlib.pyplot as plt
from io import BytesIO
import random

# Pygame Initialization
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Idiot's Delight")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont('Arial', 24)
button_font = pygame.font.SysFont('Arial', 20)

# Button Class
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, window):
        pygame.draw.rect(window, GREEN, self.rect)
        text_surface = button_font.render(self.text, True, BLACK)
        window.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()

# Game state
games_played = 0
score = None
best_score = None
score_history = []
deck = []

# Create deck
def make_deck():
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
    suits = ["clubs", "diamonds", "hearts", "spades"]
    return [(v, s) for v in values for s in suits]

def shuffle(deck):
    from random import shuffle
    shuffle(deck)
    return deck

# Idiot's Delight game logic
def idiots_delight(deck):
    in_game_deck = deck[:]
    active_card = 0
    while len(in_game_deck) >= 4 and active_card <= len(in_game_deck) - 4:
        if in_game_deck[active_card][0] == in_game_deck[active_card + 3][0]:
            del in_game_deck[active_card:active_card + 4]
            active_card = 0
        elif in_game_deck[active_card][1] == in_game_deck[active_card + 3][1]:
            del in_game_deck[active_card + 1:active_card + 3]
            active_card = 0
        else:
            active_card += 1
    return len(in_game_deck), in_game_deck

def play_game():
    global score, best_score, deck, score_history
    deck = shuffle(make_deck())
    score, deck = idiots_delight(deck)
    score_history.append(score)
    if best_score is None or score < best_score:
        best_score = score

def increase_games_played():
    global games_played
    games_played += 1
    play_game()

def load_card_images():
    card_images = {}
    image_folder = "images/"
    for value in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]:
        for suit in ["clubs", "diamonds", "hearts", "spades"]:
            card_name = f"{value}_of_{suit}.png"
            image_path = os.path.join(image_folder, card_name)
            if os.path.exists(image_path):
                image = pygame.image.load(image_path)
                card_images[(value, suit)] = pygame.transform.scale(image, (80, 120))
    return card_images

def load_card_back_image():
    image_path = os.path.join("images/", "card_back.png")
    if os.path.exists(image_path):
        return pygame.transform.scale(pygame.image.load(image_path), (80, 120))
    return None

def generate_histogram():
    if not score_history:
        return None
    plt.figure(figsize=(4, 2))  # Adjusting the figure size
    plt.hist(score_history, bins=10, color='blue', alpha=0.7)
    plt.xlabel('Remaining Cards')
    plt.ylabel('Frequency')
    plt.title('Score Distribution')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    return pygame.image.load(buf)

# Fireworks Animation Function
def fireworks_effect(origin_x, origin_y):
    particles = []
    for _ in range(50):  # Number of fireworks particles
        particles.append({
            'x': origin_x,
            'y': origin_y,
            'size': random.randint(3, 6),
            'color': random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]),
            'dx': random.uniform(-2, 2),
            'dy': random.uniform(-3, -1),
            'life': 255  # Particle's initial life (opacity)
        })
    return particles

def update_fireworks(particles):
    for particle in particles:
        particle['x'] += particle['dx']
        particle['y'] += particle['dy']
        particle['life'] -= 5  # Fade effect
        particle['dy'] += 0.05  # Gravity effect
        if particle['life'] <= 0:
            particles.remove(particle)
        else:
            pygame.draw.circle(window, particle['color'], (int(particle['x']), int(particle['y'])), particle['size'])

def main():
    global games_played, score, best_score, deck, WIDTH, HEIGHT, window, wins  # Ensure window is global
    play_button = Button(WIDTH - 180, HEIGHT - 80, 150, 50, "Play Game", increase_games_played)
    
    # Initialize the window once
    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    running = True
    card_images = load_card_images()
    card_back_image = load_card_back_image()
    
    fireworks_particles = []
    wins = 0  # Initialize wins counter to 0
    while running:
        window.fill(WHITE)  # Ensure window is always initialized here
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h  # Update WIDTH and HEIGHT
                window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Reinitialize window
            play_button.is_pressed(event)

        # Check if the score is 0 and trigger fireworks (only after game start)
        if score == 0:
            fireworks_particles = fireworks_effect(100, 100)  # Use win counter's position as origin
            congrats_surface = font.render("Congratulations! You Win!", True, BLACK)
            window.blit(congrats_surface, (WIDTH // 2 - congrats_surface.get_width() // 2, HEIGHT // 2 - 30))
            wins += 1  # Increment the wins counter

        # Top-left: Summary Stats
        best_score_display = "Win" if best_score == 0 else best_score
        wins_surface = font.render(f"Wins: {wins}", True, BLACK)
        summary_surface = font.render(f"Games: {games_played} | Best: {best_score_display}", True, BLACK)
        window.blit(summary_surface, (20, 20))
        window.blit(wins_surface, (20, 60))  # Display wins below summary

        # Histogram Top-right (adjusted to avoid overflow)
        hist_image = generate_histogram()
        if hist_image:
            hist_width = hist_image.get_width()
            hist_x = WIDTH - hist_width - 20  # Ensure margin from the right edge
            hist_y = 20  # Margin from the top
            window.blit(hist_image, (hist_x, hist_y))

        # Bottom-right: Play Button and Score
        score_surface = font.render(f"Score: {score}", True, BLACK)
        window.blit(score_surface, (WIDTH - 180, HEIGHT - 140))
        play_button.rect.topleft = (WIDTH - 180, HEIGHT - 80)
        play_button.draw(window)

        # Display last 4 cards
        x_offset, y_offset = 50, HEIGHT // 2
        for card_value, card_suit in deck[-4:]:
            if (card_value, card_suit) in card_images:
                window.blit(card_images[(card_value, card_suit)], (x_offset, y_offset))
                x_offset += 90
        if len(deck) > 4 and card_back_image:
            window.blit(card_back_image, (x_offset, y_offset))

        # Update fireworks if score is 0
        if fireworks_particles:
            update_fireworks(fireworks_particles)

        pygame.display.update()

    pygame.quit()
    sys.exit()

main()
