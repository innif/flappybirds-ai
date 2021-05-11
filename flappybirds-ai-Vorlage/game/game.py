from game.bird import Bird
from game.tube import Tube

import pygame


class Game:
    def __init__(self, size=(400, 600), tube_period=150, color=(120, 120, 120)):
        """
        Konstruktor der Game-Klasse
        :param size:        Größe des Fensters in Pixeln
        :param tube_period: Abstand zwischen zwei Röhrenpaaren in Pixeln
        :param color:       Hintergrundfarbe
        """
        pygame.init()
        self.color = color
        self.tube_period = tube_period
        self.bird_list = []
        self.tube_list = []
        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        self.running = False
        self.pos = 0
        self.birds_alive = 0

    def start(self):
        """
        Startet das Spiel bzw. die Simulation
        """
        self.running = True

    def add_bird(self, bird):
        """
        fügt dem Spiel einen Vogel hinzu
        :param bird:
        """
        assert isinstance(bird, Bird)
        self.bird_list.append(bird)
        self.birds_alive += 1

    def update(self):
        """
        Update-Methode, muss jeden Game-Tick aufgerufen werden
        """
        if not self.running:  # Abbruch, wenn Spiel nicht läuft
            return
        self.pos += 1
        # Röhren aktualisieren
        for tube in self.tube_list:
            assert isinstance(tube, Tube)
            if tube.update():
                self.tube_list.remove(tube)
        # neue Röhre hinzufügen
        if len(self.tube_list) == 0 or self.pos % self.tube_period == 0:
            self.tube_list.append(Tube(self.size))
        # Vögel aktualisieren
        for bird in self.bird_list:
            assert isinstance(bird, Bird)
            if not bird.is_alive:  # wenn Vogel nicht mehr lebt -> abbruch
                continue
            bird.score += 1  # Jeden Gametick den Vögeln einen Punkt geben
            bird.update(self.tube_list[0])  # Jeden Vogel aktualisieren und nächste Röhre übergeben
            if bird.rect.top < 0 or bird.rect.bottom > self.size[1]:  # Wenn ein Vogel das Bild verlässt -> stirbt
                bird.is_alive = False
            if not bird.is_alive:  # alive-counter updaten
                self.birds_alive -= 1

    def render(self, slow_mode=True):
        """
        Rendert das ganze Spiel
        :param slow_mode: wenn True, werden Bilder gezeichnet, sonst nur einfache Formen
        """
        self.screen.fill(self.color)  # Hintergrund
        # Vögel zeichnen
        for bird in self.bird_list:
            assert isinstance(bird, Bird)
            bird.draw(self.screen, slow_mode)
        # Röhren zeichnen
        for tube in self.tube_list:
            assert isinstance(tube, Tube)
            tube.draw(self.screen, slow_mode)
        # alive-Counter zeichnen
        font = pygame.font.SysFont("", 30)
        img = font.render("Birds alive: {}".format(self.birds_alive), True, (0, 0, 0))
        self.screen.blit(img, (10, 10))
        # den Bildschirm aktualisieren
        pygame.display.flip()
