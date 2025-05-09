import pygame 
import random
import math
import Button_dead as Button

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DeadRails 2D")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
LIGHT_GREEN = (144, 238, 144)
BLACK = (0, 0, 0)
DARK_RED = (100, 0, 0)
BROWN = (139, 69, 19)
BLUE = (0, 191, 255)
YELLOW = (255, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(100, 500))
        self.health = 100
        self.speed = 20
        self.last_hit_time = 0
        self.hit_cooldown = 1000

    def update(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_q]:
            self.speed += 5
        if keys[pygame.K_e]:
            self.speed -= 5

    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.hit_cooldown:
            self.health -= amount
            self.last_hit_time = current_time
            print(f"Player hit! Health: {self.health}")

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, color=BLACK):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 10
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.velocity
        self.dy = math.sin(angle) * self.velocity

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if not pygame.Rect(offset_x, 0, WIDTH, HEIGHT).collidepoint(self.rect.center):
            self.kill()

class molotov(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, dir_y):
        super().__init__()
        self.image = pygame.image.load('molotov.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.exploded = False
        self.velocity = 10
        angle = math.atan2(dir_y - y, dir_x - x)
        self.dx = math.cos(angle) * self.velocity
        self.dy = math.sin(angle) * self.velocity
        self.explosion_time = 5000  
        self.explosion_start_time = None

    def update(self):
        if not self.exploded:
            self.rect.x += self.dx
            self.rect.y += self.dy
            self.check_explosion()
        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.explosion_start_time > self.explosion_time:
                self.kill()

    def check_explosion(self):
        hit_list = pygame.sprite.spritecollide(self, enemies, False)
        hit_list_boss = pygame.sprite.spritecollide(self, bosses, False)
        if hit_list or hit_list_boss:
            self.explode()

        if not self.explosion_start_time:
            self.explosion_start_time = pygame.time.get_ticks()

    def explode(self):
        if not self.exploded:
            self.exploded = True
            self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(self.image, RED, (50, 50), 50)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.explosion_start_time = pygame.time.get_ticks()

class boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(1999, 2000), 500))
        self.speed = 2
        self.health = 500
        self.damage = 50
        self.last_attack_time = 0
        self.attack_cooldown = 2000
        self.current_attack = None

    def dash(self):
        dash_duration = 1000
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time < dash_duration:
            self.rect.x += self.speed * 2 if self.rect.x < WIDTH else -self.speed * 2
            self.rect.y += self.speed * 2 if self.rect.y < HEIGHT else -self.speed * 2
        else:
            self.speed = 2

    def shoot(self, player):
        bullet = Bullet(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery, RED)
        boss_bullets.add(bullet)
        all_sprites.add(bullet)

    def shot_gun(self, player):
        for angle_offset in range(-30, 31, 15):
            angle = math.atan2(player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)
            angle += math.radians(angle_offset)
            dir_x = self.rect.centerx + math.cos(angle) * 10
            dir_y = self.rect.centery + math.sin(angle) * 10
            bullet = Bullet(self.rect.centerx, self.rect.centery, dir_x, dir_y, RED)
            boss_bullets.add(bullet)
            all_sprites.add(bullet)

    def update(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            self.current_attack = random.choice(["dash", "shoot", "shot_gun"])
            self.last_attack_time = current_time

        if self.current_attack == "dash":
            self.dash()
        elif self.current_attack == "shoot":
            self.shoot(player)
        elif self.current_attack == "shot_gun":
            self.shot_gun(player)

        if self.rect.x - player.rect.x < 5000:
            if self.rect.x > player.rect.x:
                self.rect.x -= self.speed
            elif self.rect.x < player.rect.x:
                self.rect.x += self.speed
            if self.rect.y > player.rect.y:
                self.rect.y -= self.speed
            elif self.rect.y < player.rect.y:
                self.rect.y += self.speed

        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(DARK_RED)
        self.rect = self.image.get_rect(center=(random.randint(400, 1400), 500))
        self.speed = 2
        self.health = 50
        self.damage = 25

    def update(self, player):
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        elif self.rect.x < player.rect.x:
            self.rect.x += self.speed
        if self.rect.y > player.rect.y:
            self.rect.y -= self.speed
        elif self.rect.y < player.rect.y:
            self.rect.y += self.speed

        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)

def draw_train_background(offset_x):
    train_surface = pygame.Surface((20000, HEIGHT))
    train_surface.fill((210, 180, 140))
    for i in range(0, 20000, 100):
        pygame.draw.rect(train_surface, (90, 90, 90), (i, 400, 80, 200))
    screen.blit(train_surface, (-offset_x, 0))

offset_y = -200

def draw_house():
    pygame.draw.rect(screen, LIGHT_GREEN, (300, 300 + offset_y, 200, 200))
    pygame.draw.polygon(screen, DARK_RED, [(280, 300 + offset_y), (520, 300 + offset_y), (400, 200 + offset_y)])
    pygame.draw.rect(screen, BLACK, (375, 400 + offset_y, 50, 100))
    pygame.draw.rect(screen, BLUE, (320, 330 + offset_y, 40, 40))
    pygame.draw.rect(screen, BLUE, (440, 330 + offset_y, 40, 40))

def draw_bandage():
    cooldown_time = 10000
    current_time = pygame.time.get_ticks()
    bandage_image = pygame.image.load('bandage.png')
    bandage_image = pygame.transform.scale(bandage_image, (50, 50))
    screen.blit(bandage_image, (10, 215 + offset_y))
    bandage_button = Button.Button(10, 215 + offset_y, bandage_image, True)

    if current_time - draw_bandage.last_used_time > cooldown_time:
        if bandage_button.draw(screen):
            player.health += 25
            if player.health > 100:
                player.health = 100
            draw_bandage.last_used_time = current_time
        else:
            player.speed = 5

def draw_snake_oil():
    cooldown_time = 10000
    current_time = pygame.time.get_ticks()
    snake_oil_image = pygame.image.load('Snake_Oil.png')
    snake_oil_image = pygame.transform.scale(snake_oil_image, (50, 50))
    screen.blit(snake_oil_image, (130, 215 + offset_y))
    snake_oil_button = Button.Button(130, 215 + offset_y, snake_oil_image, True)

    if current_time - draw_snake_oil.last_used_time > cooldown_time:
        if snake_oil_button.draw(screen):
            player.speed = 8
            draw_snake_oil.last_used_time = 0
    else:
        player.speed = 5

def draw_molotov():
    cooldown_time = 10000
    current_time = pygame.time.get_ticks()
    molotov_image = pygame.image.load('molotov_button.png')
    molotov_image = pygame.transform.scale(molotov_image, (50, 50))
    screen.blit(molotov_image, (70, 215 + offset_y))
    molotov_button = Button.Button(70, 215 + offset_y, molotov_image, True)

    if current_time - draw_molotov.last_used_time > cooldown_time:
        if molotov_button.draw(screen):
            if enemies:
                closest_enemy = min(enemies, key=lambda e: math.hypot(player.rect.centerx - e.rect.centerx, player.rect.centery - e.rect.centery))
                new_molotov = molotov(player.rect.centerx, player.rect.centery, closest_enemy.rect.centerx, closest_enemy.rect.centery)
                molotovs.add(new_molotov)
                all_sprites.add(new_molotov)
                draw_molotov.last_used_time = current_time
            if bosses:
                closest_boss = min(bosses, key=lambda e: math.hypot(player.rect.centerx - e.rect.centerx, player.rect.centery - e.rect.centery))
                new_molotov = molotov(player.rect.centerx, player.rect.centery, closest_boss.rect.centerx, closest_boss.rect.centery)
                molotovs.add(new_molotov)
                all_sprites.add(new_molotov)
                draw_molotov.last_used_time = current_time

# Initialize cooldowns
draw_bandage.last_used_time = 0
draw_molotov.last_used_time = 0
draw_snake_oil.last_used_time = 0

# Groups
player = Player()
enemies = pygame.sprite.Group([Enemy() for _ in range(5)])
bullets = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()
molotovs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player, *enemies)
bosses = pygame.sprite.Group([boss() for _ in range(1)])
all_sprites.add(*bosses)

# Main loop
running = True
while running:
    dt = clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            bullet = Bullet(player.rect.centerx, player.rect.centery, mx, my)
            bullets.add(bullet)
            all_sprites.add(bullet)

    player.update(keys)
    enemies.update(player)
    bullets.update()
    boss_bullets.update()
    molotovs.update()
    bosses.update(player)

    # Player bullets hitting enemies
    for bullet in bullets:
        hit_list = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in hit_list:
            enemy.health -= 5
            bullet.kill()
            if enemy.health <= 0:
                enemy.kill()
    for bullet in bullets:
        hit_list = pygame.sprite.spritecollide(bullet, bosses, False)
        for b in hit_list:
            b.health -= 5
            bullet.kill()
            if b.health <= 0:
                b.kill()

    # Boss bullets hit player
    for bullet in boss_bullets:
        if bullet.rect.colliderect(player.rect):
            player.take_damage(10)
            bullet.kill()

    # Molotov damage
    for m in molotovs:
        hit_list = pygame.sprite.spritecollide(m, enemies, False)
        for enemy in hit_list:
            enemy.health -= 0.5
            if enemy.health <= 0:
                enemy.kill()
        for boss in bosses:
            boss.health -= 0.5
            if boss.health <= 0:
                boss.kill()

    offset_x = max(0, player.rect.x - WIDTH // 2)

    screen.fill(BLACK)
    draw_train_background(offset_x)
    draw_house()
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - offset_x, sprite.rect.y))

    draw_bandage()
    draw_molotov()
    draw_snake_oil()
    pygame.draw.rect(screen, RED, (650, 10, 100, 10))
    pygame.draw.rect(screen, GREEN, (650, 10, max(player.health, 0), 10))
    pygame.draw.rect(screen, YELLOW, (650, 25, 100, 10))

    if player.health <= 0:
        font = pygame.font.SysFont(None, 80)
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        dist_text = font.render(f"FINAL Distance: {player.rect.x - 100}", True, BLACK)
        screen.blit(dist_text, (WIDTH // 2 - dist_text.get_width() // 2, HEIGHT // 2 + 100))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()

pygame.quit()
