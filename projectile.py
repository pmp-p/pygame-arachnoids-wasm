import pygame
import math

SPRITE = "gfx/web_projectile.png"
SIZE = 25
SPEED = 0.025

class Projectile(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int, vx: int, vy: int, angle: float):
        super(Projectile, self).__init__()

        self.x, self.y = x, y
        self.vx, self.vy = vx, vy

        self.angle = angle

        self.rect = pygame.Rect(self.x, self.y, SIZE, SIZE)

        self.image = pygame.image.load(SPRITE).convert_alpha()
        self.image = pygame.transform.rotate(self.image, angle - 90)
        self.image = pygame.transform.scale(self.image, (SIZE, SIZE))

        self.time = 0

    def show (self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def update (self) -> None:
        self.x += self.vx * SPEED
        self.y += self.vy * SPEED

        self.rect.left, self.rect.top = self.x, self.y