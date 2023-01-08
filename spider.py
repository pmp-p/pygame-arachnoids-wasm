import pygame
from node import Node

SPRITE = "gfx/spider.png"

SIZE = 50
SPEED = 5
class Spider (pygame.sprite.Sprite):
    
    def __init__ (self):
        super(Spider, self).__init__()

        self.x, self.y = 250, 250

        self.lives = 3
        self.score = 0

        self.living = True
        self.respawn_count = 0

        self.direction = "down"

        self.sprite = pygame.image.load(SPRITE).convert_alpha()
        self.image = pygame.transform.scale(self.sprite, (SIZE, SIZE))
        self.rect = pygame.Rect(self.x, self.y, SIZE, SIZE)

    def show (self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def update (self, directions: list, nodes: pygame.sprite.Group):

        new_x, new_y = self.x, self.y

        if "up" in directions and self.y > 50:
            new_y = self.y - SPEED

        elif "down" in directions and self.y < 500:
            new_y = self.y + SPEED

        if "left" in directions and self.x > 150:
            new_x = self.x - SPEED

        elif "right" in directions and self.x < 600:
            new_x = self.x + SPEED
        
        node: Node
        for node in nodes:
            if node.rect.collidepoint(new_x + SIZE // 2, new_y + SIZE // 2) and node.visible:
                self.x, self.y = new_x, new_y
                break
        
        self.rect.left, self.rect.top = self.x, self.y

    def rotate(self, angle: float) -> None:
        self.image = pygame.image.load(SPRITE).convert_alpha()
        self.image = pygame.transform.rotate(self.sprite, angle - 90)
        self.image = pygame.transform.scale(self.image, (SIZE, SIZE))