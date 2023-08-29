import pygame
import sys
import random


def game_floor():
    screen.blit(floor_base, (floor_x_pos, 900))  # Setting the floor position
    # Repeating the floor image
    screen.blit(floor_base, (floor_x_pos + 576, 900))


def background_moving():
    screen.blit(background, (background_x_pos, 0))
    screen.blit(background, (background_x_pos + 576, 0))


def check_collision(pipes):
    # Collision with pipes
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:  # Check floor is not hit
        die_sound.play()
        return False
    return True


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5

    return pipes


def draw_pipes(pipes):
    for pipes in pipes:
        if pipes.bottom >= 1024:
            screen.blit(pipe_surface, pipes)

        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipes)


pygame.init()
clock = pygame.time.Clock()  # Creating a clock to limit the frame rate

# variables
gravity = 0.25

floor_x_pos = 0
background_x_pos = 0

game_active = True

bird_movement = 0
screen = pygame.display.set_mode((576, 1024))  # Setting up the window size

# Loading the background image
background = pygame.image.load('assets/background-day.png').convert()
# Scaling the image to fit the screen
background = pygame.transform.scale2x(background)

# Loading the bird image
bird = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird = pygame.transform.scale2x(bird)

# Getting the rectangle of the bird image to use for collision detection.
bird_rect = bird.get_rect(center=(100, 512))

floor_base = pygame.image.load(
    'assets/base.png').convert()  # Loading the floor image
floor_base = pygame.transform.scale2x(floor_base)  # Scaling the floor image

message = pygame.image.load('assets/message.png').convert_alpha()
message = pygame.transform.scale2x(message)
game_over_rect = message.get_rect(center=(288, 512))

# Building pipes
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [400, 600, 800]

SPAWNPIPE = pygame.USEREVENT  # Creating a custom event

# Loading the sound effects
flap_sound = pygame.mixer.Sound('sound/wing.wav')
die_sound = pygame.mixer.Sound('sound/hit.wav')

# Setting the event to occur every 1.2 seconds
pygame.time.set_timer(SPAWNPIPE, 1200)

while True:

    for event in pygame.event.get():  # Getting a list of all the different events
        if event.type == pygame.QUIT:  # If the event is the quit event
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:  # If the event is a key press
            if event.key == pygame.K_SPACE and game_active:  # If the key pressed is the space bar
                bird_movement = 0  # Resetting the bird movement
                bird_movement -= 12  # Moving the bird up
                flap_sound.play()  # Playing the flap sound

            if event.key == pygame.K_SPACE and game_active == False:
                bird_rect.center = (100, 512)
                bird_movement = 0
                pipe_list.clear()  # Clearing the pipe list to reset the game
                game_active = True

        if event.type == SPAWNPIPE and game_active:
            # Adding a new pipe to the pipe list
            pipe_list.extend(create_pipe())

    # Drawing the background image to the screen
    screen.blit(background, (0, 0))

    # Moving the background
    background_x_pos -= 1
    background_moving()

    if background_x_pos <= -576:
        background_x_pos = 0

    if game_active:
        bird_movement += gravity  # Adding gravity to the bird
        bird_rect.centery += bird_movement

        screen.blit(bird, bird_rect)

        # Draw pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Check for collision
        game_active = check_collision(pipe_list)

    else:
        # Displaying the game over message
        screen.blit(message, game_over_rect)

    # Create floor
    floor_x_pos -= 1
    game_floor()

    if floor_x_pos <= -576:
        floor_x_pos = 0  # Resetting the floor position to use for repeating the floor image

    pygame.display.update()  # Updating the display
    clock.tick(120)  # Limiting the frame rate to 120
