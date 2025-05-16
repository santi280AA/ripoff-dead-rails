import pygame 
import random
import math
import Button_dead as Button
import time as python
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
        self.original_speed = 8
        self.speed = 8
        self.last_hit_time = 0
        self.hit_cooldown = 1000
        self.max_health = 100
        self.bullet_damage = 5
        self.classes = 0
        self.class_type = ''
        global max_health
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
        self.velocity = 15
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
            if not self.explosion_start_time:
                self.explosion_start_time = pygame.time.get_ticks()
        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.explosion_start_time > self.explosion_time:
                self.kill()
    
    def check_explosion(self):
        hit_list = pygame.sprite.spritecollide(self, enemies, False)
        hit_list_boss = pygame.sprite.spritecollide(self, bosses, False)
        if hit_list or hit_list_boss or (pygame.time.get_ticks() - self.explosion_start_time > self.explosion_time):
            self.explode()
        
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

            # Apply damage to bosses within the explosion radius
            for boss in bosses:
                if self.rect.colliderect(boss.rect):
                    boss.health -= 50  # Adjust damage value as needed
                    print(f"Boss hit by molotov! Health: {boss.health}")
                    if boss.health <= 0:
                        boss.kill()
class MiniBoss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(center=(random.randint(9999, 10000), 500))
        self.speed = 2
        self.health = 250
        self.damage = 25
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

    def volley_shots(self, player):
        current_time = pygame.time.get_ticks()
        if not hasattr(self, 'last_shot_time'):
            self.last_shot_time = 0
        if current_time - self.last_shot_time > 1000:  # Delay of 1 second between volleys
            for angle_offset in range(-60, 61, 30):  # Shoot bullets in a cone pattern
                angle = math.atan2(player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)
                angle += math.radians(angle_offset)
                dir_x = self.rect.centerx + math.cos(angle) * 10
                dir_y = self.rect.centery + math.sin(angle) * 10
                bullet = Bullet(self.rect.centerx, self.rect.centery, dir_x, dir_y, RED)
                boss_bullets.add(bullet)
                all_sprites.add(bullet)
            self.last_shot_time = current_time

    def summon(self):
        current_time = pygame.time.get_ticks()
        if not hasattr(self, 'last_summon_time'):
            self.last_summon_time = 0
        if current_time - self.last_summon_time > 4000:
            new_enemy = Enemy()
            new_enemy.rect.x = self.rect.x + random.randint(-50, 50)
            new_enemy.rect.y = self.rect.y + random.randint(-50, 50)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
            self.last_summon_time = current_time

    def update(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            self.current_attack = random.choice(["dash", "volley_shots", "summon"])
            self.last_attack_time = current_time

        if self.current_attack == "summon":
            self.summon()
        elif self.current_attack == "volley_shots":
            self.volley_shots(player)
        elif self.current_attack == "dash":
            self.dash()
        if self.rect.x - player.rect.x < 1000:
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
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(1999999, 2000000), 500))
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
        current_time = pygame.time.get_ticks()
       
        if not hasattr(self, 'last_shot_time'):
            self.last_shot_time = 0
        if current_time - self.last_shot_time > 500:
            bullet = Bullet(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery, RED)
            boss_bullets.add(bullet)
            all_sprites.add(bullet)
            self.last_shot_time = current_time  
    def shot_gun(self, player):
        current_time = pygame.time.get_ticks()
        if not hasattr(self, 'last_shot_time'):
            self.last_shot_time = 0
        if current_time - self.last_shot_time > 500:  # Delay of 0.5 seconds between bullets
            for angle_offset in range(-30, 31, 15):
                angle = math.atan2(player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)
                angle += math.radians(angle_offset)
                dir_x = self.rect.centerx + math.cos(angle) * 10
                dir_y = self.rect.centery + math.sin(angle) * 10
                bullet = Bullet(self.rect.centerx, self.rect.centery, dir_x, dir_y, RED)
                boss_bullets.add(bullet)
                all_sprites.add(bullet)
            self.last_shot_time = current_time
   
    def update(self, player):
        health_bar_width = 100
        health_bar_height = 10
        health_ratio = max(0, self.health / 500)  # Assuming max health is 500
        health_bar_fill = int(health_bar_width * health_ratio)
        current_time = pygame.time.get_ticks()
        if self.rect.x - player.rect.x < 1000:
            pygame.draw.rect(screen, RED, (WIDTH // 2 - health_bar_width // 2, 10, health_bar_width, health_bar_height))
            pygame.draw.rect(screen, GREEN, (WIDTH // 2 - health_bar_width // 2, 10, health_bar_fill, health_bar_height))
            if current_time - self.last_attack_time > self.attack_cooldown:
                self.current_attack = random.choice(["dash", "shoot", "shot_gun"])
                self.last_attack_time = current_time
                
            if self.current_attack == "dash":
                self.dash()
            elif self.current_attack == "shoot":
                self.shoot(player)
            elif self.current_attack == "shot_gun":
                self.shot_gun(player)

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

        # Draw health bar
        
            
            
class lever(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('lever.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(center=(20000, 400))
        self.activated = False
        self.activation_time = None

    def update(self):
        if self.rect.colliderect(player.rect) and not self.activated:

            
            print("Lever activated!")
            self.activated = True
            self.activation_time = pygame.time.get_ticks()
            new_boss = Boss()
            new_boss.rect.x = self.rect.x + 200
            new_boss.rect.y = self.rect.y
            bosses.add(new_boss)
            all_sprites.add(new_boss)

        if self.activated:
            font = pygame.font.SysFont("Arial", 30)
            current_time = pygame.time.get_ticks()
            time_left = max(0, 60 - (current_time - self.activation_time) // 1000)
            timer_text = font.render(f"{time_left}s", True, WHITE)
            screen.blit(timer_text, (20000 - offset_x, 380))  # Adjusted for offset_x
            print(f"Time left: {time_left}s")
            if time_left == 0:
                font = pygame.font.SysFont(None, 80)
                text = font.render("YOU WIN", True, GREEN)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
                dist_text = font.render(f"FINAL Distance: {player.rect.x - 100}", True, BLACK)
                screen.blit(dist_text, (WIDTH // 2 - dist_text.get_width() // 2, HEIGHT // 2 + 100))
                pygame.display.flip()
                pygame.time.wait(2000)
                global running
                running = False
           
class GoldenArmor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('armor.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.collected = False

    def update(self, player):
        if not self.collected and self.rect.colliderect(player.rect):
            self.collected = True
            player.max_health = 150
            player.health = player.max_health
            print(f"Armor collected! Max health: {player.max_health}")
            
        elif self.collected:
            # Make the armor follow the player
            self.rect.center = player.rect.center

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(DARK_RED)
        self.rect = self.image.get_rect(center=(random.randint(2000, 19999), 500))
        self.speed = 5
        self.health = 50
        self.damage = 25

    def update(self, player):
        if self.rect.x - player.rect.x < 1000:
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

def draw_castle(offset_x):
    castle_x = 15000 - offset_x
    GRAY = (169, 169, 169)

    pygame.draw.rect(screen, GRAY, (castle_x, 200, 400, 400))
    pygame.draw.rect(screen, GRAY, (castle_x - 50, 150, 100, 450))
    pygame.draw.rect(screen, GRAY, (castle_x + 350, 150, 100, 450))

    pygame.draw.polygon(screen, DARK_RED, [(castle_x - 60, 150), (castle_x + 50, 80), (castle_x + 160, 150)])
    pygame.draw.polygon(screen, DARK_RED, [(castle_x + 340, 150), (castle_x + 450, 80), (castle_x + 560, 150)])

    pygame.draw.rect(screen, BROWN, (castle_x + 175, 450, 50, 150))
    pygame.draw.rect(screen, BLUE, (castle_x + 50, 300, 40, 60))
    pygame.draw.rect(screen, BLUE, (castle_x + 310, 300, 40, 60))

offset_y = -200
def draw_castle_interior():
    screen.fill((30, 30, 30))  # Dark stone walls
    pygame.draw.rect(screen, (60, 60, 60), (0, 500, WIDTH, 100))  # Floor

    for i in range(3):
        pygame.draw.rect(screen, BLUE, (150 + i * 200, 100, 50, 100))

    for i in range(2):
        pygame.draw.rect(screen, (139, 69, 19), (100 + i * 500, 300, 20, 60))  # Torch stand
        pygame.draw.circle(screen, (255, 140, 0), (110 + i * 500, 300), 15)    # Flame

    # vampfire
    pygame.draw.rect(screen, RED, (WIDTH//2 - 40, 400, 80, 100))
    pygame.draw.rect(screen, GOLD := (255, 215, 0), (WIDTH//2 - 30, 380, 60, 20))  # Throne head
   

def draw_bandage(max_health):
    cooldown_time = 10000
    current_time = pygame.time.get_ticks()
    bandage_image = pygame.image.load('bandage.png')
    bandage_image = pygame.transform.scale(bandage_image, (50, 50))
    screen.blit(bandage_image, (10, 215 + offset_y))
    bandage_button = Button.Button(10, 215 + offset_y, bandage_image, True)

    if current_time - draw_bandage.last_used_time > cooldown_time:
        if bandage_button.draw(screen):
            player.health += 25
            if player.health > player.max_health:
                player.health = player.max_health
            draw_bandage.last_used_time = current_time
class ClassesStand(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('classes.png')
        self.image = pygame.transform.scale(self.image, (256, 256))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        
        pass
    
def draw_runner(player):
    runner_image = pygame.image.load('runner_class.png')
    runner_image = pygame.transform.scale(runner_image, (50, 50))
    runner = pygame.sprite.Sprite()
    runner.image = runner_image
    runner.rect = runner_image.get_rect(center=(200, 325))
    screen.blit(runner.image, (runner.rect.x - offset_x, runner.rect.y))
    font = pygame.font.SysFont(None, 30)
    text = font.render("Runner: +2 speed", True, WHITE)
    screen.blit(text, (runner.rect.x - offset_x - 100, runner.rect.y - 30))
    if player.rect.colliderect(runner.rect) and player.classes == 0:
        player.original_speed = 30
        player.speed = 30
        player.classes += 1
        player.class_type = 'runner'

def draw_gunslinger(player):
    gunslinger_image = pygame.image.load('gunslinger class.png')
    gunslinger_image = pygame.transform.scale(gunslinger_image, (50, 50))
    gunslinger = pygame.sprite.Sprite()
    gunslinger.image = gunslinger_image
    gunslinger.rect = gunslinger_image.get_rect(center=(400, 325))
    screen.blit(gunslinger.image, (gunslinger.rect.x - offset_x, gunslinger.rect.y))
    font = pygame.font.SysFont(None, 30)
    text = font.render("gunslinger: +3 bullet damage", True, WHITE)
    screen.blit(text, (gunslinger.rect.x - offset_x + -100, gunslinger.rect.y - 30))
    if player.rect.colliderect(gunslinger.rect) and player.classes == 0:
        player.bullet_damage = 8
        player.classes += 1
        player.class_type = 'gunslinger'
    if player.rect.colliderect(gunslinger.rect) and player.classes == 0:
        player.bullet_damage = 8
        player.classes += 1
        player.class_type = 'gunslinger'
       
def draw_ironclad(player):
    ironclad_image = pygame.image.load('armor_class.png')
    ironclad_image = pygame.transform.scale(ironclad_image, (50, 50))
    ironclad = pygame.sprite.Sprite()
    ironclad.image = ironclad_image
    ironclad.rect = ironclad_image.get_rect(center=(600, 325))
    screen.blit(ironclad.image, (ironclad.rect.x - offset_x, ironclad.rect.y))
    font = pygame.font.SysFont(None, 30)
    text = font.render("Ironclad: +25 hp, -1 speed", True, WHITE)
    screen.blit(text, (ironclad.rect.x - offset_x + 10, ironclad.rect.y - 30))
    if not hasattr(player, 'armor_collected'):
        player.armor_collected = False
        player.armor = None

    if player.rect.colliderect(ironclad.rect) and not player.armor_collected and player.classes == 0:
        player.armor = pygame.sprite.Sprite()
        player.armor.image = pygame.image.load('gray_armor.png')  # Load the correct armor image
        player.armor.image = pygame.transform.scale(player.armor.image, (40, 40))  # Scale the image if needed
        player.armor.rect = player.armor.image.get_rect(center=player.rect.center)  # Set the rect to match the player's position
        player.speed = 7
        player.original_speed = 7
        player.max_health = 125
        player.health = player.max_health
        player.armor_collected = True
        player.classes += 1
        player.class_type = 'ironclad'
    if player.armor_collected and player.armor:
        # Ensure the armor stays with the player
        player.armor.rect.center = player.rect.center
        screen.blit(player.armor.image, (player.armor.rect.x - offset_x, player.armor.rect.y))
def draw_snake_oil():
    cooldown_time = 10000
    boost_duration = 5000
    current_time = pygame.time.get_ticks()
    snake_oil_image = pygame.image.load('Snake_Oil.png')
    snake_oil_image = pygame.transform.scale(snake_oil_image, (50, 50))
    screen.blit(snake_oil_image, (130, 215 + offset_y))
    snake_oil_button = Button.Button(130, 215 + offset_y, snake_oil_image, True)

    if not hasattr(draw_snake_oil, 'boost_active'):
        draw_snake_oil.boost_active = False

    if current_time - draw_snake_oil.last_used_time > cooldown_time:
        if snake_oil_button.draw(screen):
            player.speed += 5
            draw_snake_oil.last_used_time = current_time
            draw_snake_oil.boost_active = True

    if draw_snake_oil.boost_active and current_time - draw_snake_oil.last_used_time > boost_duration:
        player.speed = player.original_speed
        draw_snake_oil.boost_active = False
           

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
            if miniboss:
                closest_miniboss = min(miniboss, key=lambda e: math.hypot(player.rect.centerx - e.rect.centerx, player.rect.centery - e.rect.centery))
                new_molotov = molotov(player.rect.centerx, player.rect.centery, closest_miniboss.rect.centerx, closest_miniboss.rect.centery)
                molotovs.add(new_molotov)
                all_sprites.add(new_molotov)
                draw_molotov.last_used_time = current_time
def draw_castle(offset_x):
    castle_x = 15000 - offset_x
    GRAY = (169, 169, 169)

    pygame.draw.rect(screen, GRAY, (castle_x, 200, 400, 400))
    pygame.draw.rect(screen, GRAY, (castle_x - 50, 150, 100, 450))
    pygame.draw.rect(screen, GRAY, (castle_x + 350, 150, 100, 450))

    pygame.draw.polygon(screen, DARK_RED, [(castle_x - 60, 150), (castle_x + 50, 80), (castle_x + 160, 150)])
    pygame.draw.polygon(screen, DARK_RED, [(castle_x + 340, 150), (castle_x + 450, 80), (castle_x + 560, 150)])

    pygame.draw.rect(screen, BROWN, (castle_x + 175, 450, 50, 150))
    pygame.draw.rect(screen, BLUE, (castle_x + 50, 300, 40, 60))
    pygame.draw.rect(screen, BLUE, (castle_x + 310, 300, 40, 60))

offset_y = -200
def draw_castle_interior():
    screen.fill((30, 30, 30))  # Dark stone walls
    pygame.draw.rect(screen, (60, 60, 60), (0, 500, WIDTH, 100))  # Floor

    for i in range(3):
        pygame.draw.rect(screen, BLUE, (150 + i * 200, 100, 50, 100))

    for i in range(2):
        pygame.draw.rect(screen, (139, 69, 19), (100 + i * 500, 300, 20, 60))  # Torch stand
        pygame.draw.circle(screen, (255, 140, 0), (110 + i * 500, 300), 15)    # Flame

    # Throne
    pygame.draw.rect(screen, RED, (WIDTH//2 - 40, 400, 80, 100))
    pygame.draw.rect(screen, GOLD := (255, 215, 0), (WIDTH//2 - 30, 380, 60, 20))  # Throne head
   


# Initialize cooldowns
draw_bandage.last_used_time = 0
draw_molotov.last_used_time = 0
draw_snake_oil.last_used_time = 0

# Groups
golden_armor_group = pygame.sprite.Group()
player = Player()
enemies = pygame.sprite.Group([Enemy() for _ in range(5)])
bullets = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()
molotovs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player, *enemies)
bosses = pygame.sprite.Group([Boss() for _ in range(1)])
all_sprites.add(*bosses)
levers = pygame.sprite.Group([lever() for _ in range(1)])
all_sprites.add(*levers)
miniboss = pygame.sprite.Group([MiniBoss() for _ in range(1)])
all_sprites.add(*miniboss)
class_stand = ClassesStand(400, 150)
all_sprites.add(class_stand)
running = True
while running:
    dt = clock.tick(30)
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

    miniboss.update(player)
    golden_armor_group.update(player)
    miniboss.update(player)
    levers.update()
    # Player bullets hitting enemies
    for bullet in bullets:
        hit_list = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in hit_list:
            enemy.health -= player.bullet_damage
            bullet.kill()
            if enemy.health <= 0:
                enemy.kill()
    for bullet in bullets:
        hit_list = pygame.sprite.spritecollide(bullet, bosses, False)
        for boss in hit_list:
            boss.health -= player.bullet_damage
            print(f"Boss hit! Health: {boss.health}")
            bullet.kill()
            if boss.health <= 0:
                boss.kill()
    for bullet in bullets:
        hit_list = pygame.sprite.spritecollide(bullet, miniboss, False)
        for mini in hit_list:
            mini.health -= player.bullet_damage
            print(f"Miniboss hit! Health: {mini.health}")
            bullet.kill()
            if mini.health <= 0:
                mini.kill()
                golden_armor = GoldenArmor(mini.rect.centerx, mini.rect.centery)
                all_sprites.add(golden_armor)
                golden_armor_group.add(golden_armor)
                golden_armor = GoldenArmor(mini.rect.centerx, mini.rect.centery)
                all_sprites.add(golden_armor)
                    
                    

    # Boss bullets hit player
    for bullet in boss_bullets:
        if bullet.rect.colliderect(player.rect):
            player.take_damage(10)
            bullet.kill()

    # Molotov damage
    for m in molotovs:
        # Check if molotov leaves the screen
        if not pygame.Rect(offset_x, 0, WIDTH, HEIGHT).collidepoint(m.rect.center):
            m.kill()
            continue

        hit_list = pygame.sprite.spritecollide(m, enemies, False)
        for enemy in hit_list:
            enemy.health -= 0.5
            if enemy.health <= 0:
                enemy.kill()
        for boss in bosses:
            if m.rect.colliderect(boss.rect):  # Check if molotov is near the boss
                boss.health -= 0.05
                print(f"Boss hit! Health: {boss.health}")
            if boss.health <= 0:
                boss.kill()
        for mini in miniboss:
            if m.rect.colliderect(mini.rect):
                m.explode()  # Call the explode method to trigger the explosion
                mini.health -= 0.15
                print(f"Miniboss hit! Health: {mini.health}")
                if mini.health <= 0:
                    mini.kill()
                    golden_armor = GoldenArmor(mini.rect.centerx, mini.rect.centery)
                    all_sprites.add(golden_armor)
                    golden_armor_group.add(golden_armor)
    offset_x = max(0, player.rect.x - WIDTH // 2)
    
    
    screen.fill(BLACK)
    draw_train_background(offset_x)
    draw_house()
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - offset_x, sprite.rect.y))
    draw_runner(player)
    draw_bandage(max_health=100)
    draw_molotov()
    draw_snake_oil()
    draw_gunslinger(player)
    draw_castle(offset_x)
    draw_ironclad(player)
    for boss in bosses:
        if boss.rect.x - player.rect.x < 1000:
            text = pygame.font.SysFont(None, 40).render("Nikoli Tesla", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 25 - 20))
            health_bar_width = 400
            health_bar_height = 50
            health_ratio = max(0, boss.health / 500)  # Assuming max health is 500
            health_bar_fill = int(health_bar_width * health_ratio)
            pygame.draw.rect(screen, BLACK, (WIDTH // 2 - health_bar_width // 2, HEIGHT // 20, health_bar_width, health_bar_height))
            pygame.draw.rect(screen, GREEN, (WIDTH // 2 - health_bar_width // 2, HEIGHT // 20, health_bar_fill, health_bar_height))
    for mini in miniboss:
        if mini.rect.x - player.rect.x < 1000:
            text = pygame.font.SysFont(None, 40).render("The Summoner", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 25 - 20))
            health_bar_width = 400
            health_bar_height = 50
            health_ratio = max(0, mini.health / 250)
            health_bar_fill = int(health_bar_width * health_ratio)
            pygame.draw.rect(screen, BLACK, (WIDTH // 2 - health_bar_width // 2, HEIGHT // 20, health_bar_width, health_bar_height))
            pygame.draw.rect(screen, RED, (WIDTH // 2 - health_bar_width // 2, HEIGHT // 20, health_bar_fill, health_bar_height))

    pygame.draw.rect(screen, RED, (650, 10, 100, 10))
    pygame.draw.rect(screen, GREEN, (650, 10, max(player.health, 0), 10))
    pygame.draw.rect(screen, YELLOW, (650, 25, 100, 10))
    font = pygame.font.SysFont(None, 30)
    class_text = font.render(f"Class: {player.class_type}", True, WHITE)
    screen.blit(class_text, (600, 50))
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
