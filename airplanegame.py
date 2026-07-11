import pygame, random, sys

pygame.init()
W, H = 600, 700
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40)); self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(centerx=W//2, bottom=H-10)
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= 8
        if keys[pygame.K_RIGHT] and self.rect.right < W: self.rect.x += 8

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 3
        self.image = pygame.Surface((30, 30)); self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(x=random.randint(0, W-30), y=random.randint(-100, -40))
        self.speed = random.randint(3, 6)
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > H: self.__init__()
    def hit(self):
        self.hp -= 1
        self.image.fill((180 if self.hp == 2 else 100, 0, 0))
        return self.hp <= 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 15)); self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(centerx=x, bottom=y)
    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0: self.kill()

def game_over(score):
    while True:
        screen.fill((0, 0, 0))
        t1 = font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
        t2 = font.render("Press 'R' to Restart or 'Esc' to Exit", True, (255, 255, 0))
        screen.blit(t1, (W//2 - t1.get_width()//2, H//3))
        screen.blit(t2, (W//2 - t2.get_width()//2, H//2))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

while True:
    all_sprites, obstacles, bullets = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
    player = Player(); all_sprites.add(player)
    for _ in range(6): o = Obstacle(); all_sprites.add(o); obstacles.add(o)
    score, running = 0, True
    while running:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                b = Bullet(player.rect.centerx, player.rect.top); all_sprites.add(b); bullets.add(b)
        all_sprites.update()
        hits = pygame.sprite.groupcollide(obstacles, bullets, False, True)
        for o in hits:
            if o.hit():
                o.kill(); score += 1
                new_o = Obstacle(); all_sprites.add(new_o); obstacles.add(new_o)
        if pygame.sprite.spritecollideany(player, obstacles): running = False
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
        pygame.display.flip()
    game_over(score)
