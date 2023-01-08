import pygame

SPRITE = "gfx/web_node.png"

SIZE = 50
START_X = 150
START_Y = 50
class Node (pygame.sprite.Sprite):
    
    def __init__ (self, x: int, y: int):
        super(Node, self).__init__()

        self.visible = False

        self.image = pygame.image.load(SPRITE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE - 10, SIZE - 10))
        self.rect = pygame.Rect(START_X + (SIZE * x), 
        START_Y + (SIZE * y), SIZE, SIZE)

    def show (self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)