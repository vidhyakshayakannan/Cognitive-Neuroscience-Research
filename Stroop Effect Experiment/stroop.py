import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stroop Experiment")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Function to create a randomized list of stimuli
def create_stimuli_list(num_trials):
    colors = [RED, GREEN, BLUE, YELLOW]
    words = ['RED', 'GREEN', 'BLUE', 'YELLOW']

    stimuli_list = []

    for _ in range(num_trials // 4):
        for color, word in zip(colors, words):
            congruent_stimulus = (word, color)
            incongruent_color = random.choice([c for c in colors if c != color])
            incongruent_stimulus = (word, incongruent_color)

            stimuli_list.extend([congruent_stimulus, incongruent_stimulus])

    random.shuffle(stimuli_list)
    return stimuli_list

# Function to display instructions
def display_instructions():
    screen.fill(WHITE)
    instructions = [
        "Welcome to the Stroop Experiment!",
        "Press 'R' for RED, 'G' for GREEN, 'B' for BLUE, and 'Y' for YELLOW.",
        "Try to indicate the color of the word, not the written word itself.",
        "Press any key to start..."
    ]

    for i, line in enumerate(instructions):
        text = font.render(line, True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 2 + i * 30))
        screen.blit(text, text_rect)

    pygame.display.flip()
    pygame.time.wait(500)  # Wait for 500 milliseconds

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting_for_key = False

# Function to run the Stroop experiment
def run_stroop_experiment(num_trials=10):
    display_instructions()

    stimuli_list = create_stimuli_list(num_trials)

    inter_trial_interval = 1000  # Set the inter-trial interval in milliseconds

    for trial in stimuli_list:
        screen.fill(WHITE)

        text = font.render(trial[0], True, trial[1])
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

        waiting_for_response = True
        start_time = pygame.time.get_ticks()

      while waiting_for_response:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_r, pygame.K_g, pygame.K_b, pygame.K_y]:
                response_time = (pygame.time.get_ticks() - start_time) / 1000.0
                response_color = pygame.key.name(event.key)

                # Ensure response_color is treated as a string
                response_color_first_letter = response_color.lower()[0] if response_color != 'space' else ' '

                # Extract color name from trial
                trial_color_name = trial[0]

                accuracy = 1 if response_color_first_letter == trial_color_name[0].lower() else 0

                print(f"Stimulus: {trial[0]}, Color: {trial[1]}, Response: {response_color}, Accuracy: {accuracy}, RT: {response_time:.3f} seconds")

                waiting_for_response = False  # This should be indented to be part of the innermost if block


        pygame.time.delay(inter_trial_interval)  # Inter-trial interval in milliseconds

# Run the Stroop experiment 
run_stroop_experiment(num_trials=4)
