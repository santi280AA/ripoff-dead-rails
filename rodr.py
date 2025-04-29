import pygame
import math
pygame.init()
move_counter = 0
move_delay = 5
pygame.display.set_caption("rip off dead rails lolw")

height = 800
width = 800
screen = pygame.display.set_mode((width, height))
player_speed = 1
real_speed = player_speed 
running = True

class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.original_image = self.image  # Keep the original image for rotation
        self.rect = self.image.get_rect(center=position)

    def follow_mouse(self, event):
        # Move the character to the mouse position
        self.rect.center = event.pos

    def rotate_towards_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        char_angle = math.degrees(math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx))
        self.image = pygame.transform.rotate(self.original_image, -char_angle)
        self.rect = self.image.get_rect(center=self.rect.center)


# Create a character instance and place it at the center of the screen
character = Character('New Piskel (2).png', (width // 2, height // 2))

while running:
    keys = pygame.key.get_pressed()  # Get the state of all keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    move_counter += 1
    if move_counter >= move_delay:
        move_counter = 0
 
        if keys[pygame.K_d]:
            character.rect.x += player_speed 
        if keys[pygame.K_a]:
            character.rect.x -= player_speed
        if keys[pygame.K_w]:
            character.rect.y -= player_speed
        if keys[pygame.K_s]:
            character.rect.y += player_speed

    # Rotate the character towards the mouse
    character.rotate_towards_mouse()

    # Fill the screen with a background color (e.g., black)
    screen.fill((0, 0, 0))

    # Draw the character
    screen.blit(character.image, character.rect)

    # Update the display
    pygame.display.update()

pygame.quit()
