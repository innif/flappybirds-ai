import pygame
from ai.model import Model
from game.tube import Tube

BIRD_COLOR = (250, 232, 0)


class Bird:
    def __init__(self, model, x=10, y=250, w=100, h=100):
        assert isinstance(model, Model)
        self.model = model
        self.score = 0
        self.is_alive = True
        self.rect = pygame.Rect(x, y, w, h)  # x, y, w, h
        self.img = pygame.image.load('assets/bird.gif')
        self.img = pygame.transform.scale(self.img, (w, h))
        self.img.convert()
        self.img_rotated = self.img
        self.angle = 0
        self.speed = 0
        self.next_tube = None
        pass

    def _calc_img_rotated(self):
        """rotate an image while keeping its center and size"""
        orig_rect = self.img.get_rect()
        rot_image = pygame.transform.rotate(self.img, self.angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        self.img_rotated = rot_image.subsurface(rot_rect)

    def _colliding(self, barrect, barsurface):
        if self.rect.colliderect(barrect):
            birdMask = pygame.mask.from_surface(self.img, 50)
            offset_x = barrect[0] - self.rect[0]
            offset_y = barrect[1] - self.rect[1]
            tubeMask = pygame.mask.from_surface(barsurface, 50)
            a = birdMask.overlap_area(tubeMask, (offset_x, offset_y))
            return a > 0
        else:
            return False

    def update(self, next_tube):
        self.next_tube = next_tube
        if not self.is_alive: return
        self.speed -= 0.25
        if self.speed < 2.5 and self.model.calc(next_tube, self):
            self.speed = 5
        self.rect.y -= self.speed
        self.angle = self.speed * 4
        self._calc_img_rotated()
        assert isinstance(next_tube, Tube)
        if self._colliding(next_tube.top_rect, next_tube.top_img):
            self.is_alive = False
        if self._colliding(next_tube.bot_rect, next_tube.bot_img):
            self.is_alive = False

    def draw(self, surface, slow_mode=True):
        if self.is_alive:
            pygame.draw.line(surface, (255, 0, 0), self.rect.center, self.next_tube.top_rect.bottomleft, 1)
            pygame.draw.line(surface, (255, 0, 0), self.rect.center, self.next_tube.bot_rect.topleft, 1)
            if slow_mode:
                surface.blit(self.img_rotated, self.rect)
            else:
                pygame.draw.circle(surface, BIRD_COLOR, self.rect.center, 30, 3)

    def print(self):
        self.model.print()
