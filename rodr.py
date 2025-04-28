import pygame
import math
pygame.init()

height = 800
width = 800
screen = pygame.display.set_mode((width, height))

running = True

class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=position)

    def follow_mouse(self, event):
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            char_angle = math.degrees(math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx))
            self.image = pygame.transform.rotate(self.image, char_angle)
            self.update

    

# Create a character instance and place it at the center of the screen
character = Character('New Piskel (2).png', (width // 2, height // 2))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                character.follow_mouse(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                character.rect.x += 10
            elif event.key == pygame.K_a:
                character.rect.x -= 10
            elif event.key == pygame.K_w:
                character.rect.y -= 10
            elif event.key == pygame.K_s:
                character.rect.y += 10
                

    # Fill the screen with a background color (e.g., black)
    screen.fill((0, 0, 0))

    # Draw the character
    screen.blit(character.image, character.rect)

    # Update the display
    pygame.display.update()

pygame.quit()
