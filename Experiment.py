import pygame
import time
import random
import numpy as np
import csv

# Initialize pygame mixer and display
pygame.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Audio Experiment")

# Define function to display instructions
def display_instructions():
    font = pygame.font.Font(None, 36)
    instructions = [
        "Press 'M' if the tone is in tune with the guitar sounds and 'Z' if it is not.",
        "Respond with 'M' or 'Z' as soon as you hear the tone.",
        "Press any key to start the experiment..."
    ]
    screen.fill((255, 255, 255))  # Fill the screen with white
    y_offset = 200
    for line in instructions:
        text = font.render(line, True, (0, 0, 0))
        rect = text.get_rect(center=(screen_width / 2, y_offset))
        screen.blit(text, rect)
        y_offset += 40
    pygame.display.flip()

    # Wait for any key press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# Define function to play a tone
def play_tone(frequency, duration):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    tone = 32767 * 0.5 * np.sin(2 * np.pi * frequency * t)
    buf = np.zeros((n_samples, 2), dtype=np.int16)
    buf[:, 0] = tone
    buf[:, 1] = tone
    sound = pygame.sndarray.make_sound(buf)
    sound.play()
    return sound, time.time()  # Return the sound object and the time when the tone starts playing

# Define function to play strong and weak guitar sounds with tone
def play_guitar_sound_with_tone(volume, tone_frequency, tone_duration):
    strong_sound = pygame.mixer.Sound('/Users/vidhyakshayakannan/Downloads/snare-808.wav')
    weak_sound = pygame.mixer.Sound('/Users/vidhyakshayakannan/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album/kick-classic.wav')
    strong_sound.set_volume(volume)
    weak_sound.set_volume(volume * 0.5)

    # Randomly decide when to play the tone within the sequence
    position = random.randint(1, 4)
    
    tone_start_time = None
    tone_sound = None

    for i in range(5):
        if i == position:
            tone_sound, tone_start_time = play_tone(tone_frequency, tone_duration)
        
        strong_sound.play()
        wait_for_response_or_timeout(tone_start_time, strong_sound, weak_sound, tone_sound)
        
        weak_sound.play()
        wait_for_response_or_timeout(tone_start_time, strong_sound, weak_sound, tone_sound)

    return tone_start_time

# Function to wait for a response or until sound ends
def wait_for_response_or_timeout(tone_start_time, strong_sound, weak_sound, tone_sound):
    global reaction_time, response, waiting_for_response
    start_time = time.time()
    
    while pygame.mixer.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m or event.key == pygame.K_z:
                    reaction_time = time.time() - tone_start_time
                    response = chr(event.key).upper()
                    waiting_for_response = False
                    strong_sound.stop()
                    weak_sound.stop()
                    if tone_sound:
                        tone_sound.stop()
                    return
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        time.sleep(0.01)  # Reduce this value to decrease the delay

# Function to run the experiment and store reaction times to a CSV file
def run_experiment(num_trials):
    # Set parameters
    sound_volume = 1.0
    tone_frequency = 440  # A4
    tone_duration = 0.5  # seconds

    # Open a CSV file to write reaction times
    with open('reaction_times.csv', 'w', newline='') as csvfile:
        fieldnames = ['trial', 'reaction_time', 'response']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Run the experiment for the specified number of trials
        for trial in range(1, num_trials + 1):
            # Display instructions
            display_instructions()

            # Switch to blank screen
            screen.fill((255, 255, 255))  # Fill the screen with white
            pygame.display.flip()

            # Initialize variables for reaction time measurement
            global reaction_time, response, waiting_for_response
            reaction_time = None
            response
            import pygame
import time
import random
import numpy as np
import csv

# Initialize pygame mixer and display
pygame.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Audio Experiment")

# Define function to display instructions
def display_instructions():
    font = pygame.font.Font(None, 36)
    instructions = [
        "Press 'M' if the tone is in tune with the guitar sounds and 'Z' if it is not.",
        "Respond with 'M' or 'Z' as soon as you hear the tone.",
        "Press any key to start the experiment..."
    ]
    screen.fill((255, 255, 255))  # Fill the screen with white
    y_offset = 200
    for line in instructions:
        text = font.render(line, True, (0, 0, 0))
        rect = text.get_rect(center=(screen_width / 2, y_offset))
        screen.blit(text, rect)
        y_offset += 40
    pygame.display.flip()

    # Wait for any key press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# Define function to play a tone
def play_tone(frequency, duration):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    tone = 32767 * 0.5 * np.sin(2 * np.pi * frequency * t)
    buf = np.zeros((n_samples, 2), dtype=np.int16)
    buf[:, 0] = tone
    buf[:, 1] = tone
    sound = pygame.sndarray.make_sound(buf)
    sound.play()
    return sound, time.time()  # Return the sound object and the time when the tone starts playing

# Define function to play strong and weak guitar sounds with tone
def play_guitar_sound_with_tone(volume, tone_frequency, tone_duration):
    """
    Plays a sequence of strong and weak guitar sounds with a randomly placed tone.

    Args:
        volume (float): Volume of the sounds (0.0 to 1.0).
        tone_frequency (float): Frequency of the tone in Hz.
        tone_duration (float): Duration of the tone in seconds.

    Returns:
        float: The time when the tone starts playing (or None if no tone is played).
    """
    strong_sound_channel = pygame.mixer.Channel(1)
    weak_sound_channel = pygame.mixer.Channel(2)
    
    strong_sound = pygame.mixer.Sound('/Users/vidhyakshayakannan/Downloads/snare-808.wav')
    weak_sound = pygame.mixer.Sound('/Users/vidhyakshayakannan/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album/kick-classic.wav')
    strong_sound.set_volume(volume)
    weak_sound.set_volume(volume * 0.5)

    # Randomly decide when to play the tone within the sequence
    position = random.randint(1, 4)
    tone_start_time = None
    tone_sound = None

    for i in range(5):
        if i == position:
            tone_sound, tone_start_time = play_tone(tone_frequency, tone_duration)

        # Play strong sound on its channel
        strong_sound_channel.play(strong_sound)
        wait_for_response_or_timeout(tone_start_time, strong_sound_channel, weak_sound_channel, tone_sound)

        # Play weak sound on its channel
        weak_sound_channel.play(weak_sound)
        wait_for_response_or_timeout(tone_start_time, strong_sound_channel, weak_sound_channel, tone_sound)

    return tone_start_time


# Function to wait for a response or until sound ends
def wait_for_response_or_timeout(tone_start_time, strong_sound, weak_sound, tone_sound):
    
    global reaction_time, response, waiting_for_response
    start_time = time.time()
    
    while pygame.mixer.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m or event.key == pygame.K_z:
                    reaction_time = time.time() - tone_start_time
                    response = chr(event.key).upper()
                    waiting_for_response = False
                    # Stop all sounds here
                    strong_sound.stop()
                    weak_sound.stop()
                    if tone_sound:
                        tone_sound.stop()
                    return
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        time.sleep(0.01)  # Reduce this value to decrease the delay


# Function to run the experiment and store reaction times to a CSV file
def run_experiment(num_trials):
    # Set parameters
    sound_volume = 1.0
    tone_frequency = 440  # A4
    tone_duration = 0.5  # seconds

    # Open a CSV file to write reaction times
    with open('reaction_times.csv', 'w', newline='') as csvfile:
        fieldnames = ['trial', 'reaction_time', 'response']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Run the experiment for the specified number of trials
        for trial in range(1, num_trials + 1):
            # Display instructions
            display_instructions()

            # Switch to blank screen
            screen.fill((255, 255, 255))  # Fill the screen with white
            pygame.display.flip()

            # Initialize variables for reaction time measurement
            global reaction_time, response, waiting_for_response
            reaction_time = None
            response = None
            waiting_for_response = True

            # Play guitar sounds with tone and get the tone start time
            tone_start_time = play_guitar_sound_with_tone(sound_volume, tone_frequency, tone_duration)

            # Display results after the sequence
            screen.fill((255, 255, 255))  # Fill the screen with white
            font = pygame.font.Font(None, 36)
            if reaction_time is not None:
                result_text = f"Trial {trial}: Reaction Time: {reaction_time:.3f} seconds. You responded '{response}'."
            else:
                result_text = f"Trial {trial}: No valid response recorded."

            text = font.render(result_text, True, (0, 0, 0))
            rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(text, rect)
            pygame.display.flip()

            # Write reaction time to CSV file
            writer.writerow({'trial': trial, 'reaction_time': reaction_time, 'response': response})

            # Wait for a few seconds before proceeding to the next trial
            time.sleep(2)

# Run the experiment with a specified number of trials
num_trials = int(input("Enter the number of trials: "))
run_experiment(num_trials)

# Close the pygame window
pygame.quit()


