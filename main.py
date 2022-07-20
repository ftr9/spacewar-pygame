import random
import sys
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./assets/spaceship.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(800 / 2, 350))

    def update_position(self):
        self.rect.center = pygame.mouse.get_pos()

    def game_over(self):
        global enemy_list,game_active
        if pygame.sprite.spritecollide(self, enemy_list, True):
           game_active = False

    def update(self):
        self.update_position()
        self.game_over()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, mouse_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./assets/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=mouse_position)

    def update_pos(self):
        self.rect.top -= 5
        if self.rect.top <= -10:
            self.kill()

    def update(self):
        self.update_pos()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./assets/enemy.png').convert_alpha()
        random_x = random.randint(50, 750)
        self.rect = self.image.get_rect(midbottom=(random_x, 0))
        self.dy = dy

    def update_pos(self):
        self.rect.bottom += self.dy

    def update(self):
        self.update_pos()


class ScoreText(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = pygame.font.Font('./assets/Lato-Bold.ttf', 15)
        self.score = 0
        self.image = self.text.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.rect = self.image.get_rect(midtop=(40, 4))

    def update_score(self):
        global bullets, enemy_list
        if pygame.sprite.groupcollide(bullets, enemy_list, True, True):
            self.score += 1
            self.image = self.text.render('Score: ' + str(self.score), True, (255, 255, 255))

    def update(self):
        self.update_score()


# initialization
pygame.init()
display = pygame.display.set_mode((800, 400))
pygame.display.set_caption("space war")

velocity_enemy_dy = 3
game_active = True
TICK = pygame.time.Clock()

# enemy spawn event
enemy_spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_spawn_timer, 600)
# enemy velocity increment
enemy_velocity_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_velocity_timer, 5000)

# class Score
score = pygame.sprite.GroupSingle(ScoreText())
# class player
player = pygame.sprite.GroupSingle(Player())
# class bullet
bullets = pygame.sprite.Group()
# class enemy
enemy_list = pygame.sprite.Group()

# background image
bg_image = pygame.image.load('./assets/lame.png')
bg_rect = bg_image.get_rect()

# game loop
while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if events.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                bullets.add(Bullet(pygame.mouse.get_pos()))
        if events.type == enemy_spawn_timer:
            enemy_list.add(Enemy(velocity_enemy_dy))
        if events.type == enemy_velocity_timer:
            velocity_enemy_dy += 1

    if game_active:
        # background image
        display.blit(bg_image, bg_rect)
        # player
        player.draw(display)
        player.update()

        # bullet
        bullets.draw(display)
        bullets.update()

        # enemy list
        enemy_list.draw(display)
        enemy_list.update()

        # score
        score.draw(display)
        score.update()

        pygame.display.update()
    else:
        bullets.empty()
        enemy_list.empty()
        display.fill('Red')

    TICK.tick(60)
