from game.bird import Bird
from game.tube import Tube

import pygame


class Game:
    def __init__(self, size=(400, 600), tube_period=150, color=(120, 120, 120)):
        pygame.init()
        self.color = color
        self.tube_period = tube_period
        self.birdlist = []
        self.tubelist = []
        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        self.running = False
        self.pos = 0
        self.birds_alive = 0

    def start(self):
        self.running = True

    def add_bird(self, bird):
        assert isinstance(bird, Bird)
        self.birdlist.append(bird)
        self.birds_alive += 1

    def update(self):
        if not self.running:
            return
        self.pos += 1
        for tube in self.tubelist:
            assert isinstance(tube, Tube)
            if not tube.update():
                self.tubelist.remove(tube)
        if len(self.tubelist) == 0 or self.pos % self.tube_period == 0:
            self.tubelist.append(Tube(self.size))
        for bird in self.birdlist:
            assert isinstance(bird, Bird)
            if bird.is_alive:
                bird.score += 1
                bird.update(self.tubelist[0])
                if bird.rect.top < 0 or bird.rect.bottom > self.size[1]:
                    bird.is_alive = False
                if not bird.is_alive:
                    self.birds_alive -= 1

    def render(self, slow_mode=True):
        self.screen.fill(self.color)
        for bird in self.birdlist:
            assert isinstance(bird, Bird)
            bird.draw(self.screen, slow_mode)
        for tube in self.tubelist:
            assert isinstance(tube, Tube)
            tube.draw(self.screen, slow_mode)
        font = pygame.font.SysFont("Consolas", 15)
        img = font.render("Birds alive: {}".format(self.birds_alive), True, (0, 0, 0))
        self.screen.blit(img, (10, 10))
        pygame.display.flip()  # den Bildschirm aktualisieren
