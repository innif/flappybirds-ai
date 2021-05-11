import pygame
from ai.model import Model
from game.tube import Tube

BIRD_COLOR = (250, 232, 0)


class Bird:
    def __init__(self, model, x=10, y=250, w=100, h=100):
        """
        Konstruktor für ein Vogel-Objekt
        :param model:   AI-Modell, nach dem der Vogel sich verhalten soll
        :param x:       x-Position des Vogels
        :param y:       y-Position des Vogels
        :param w:       Breite des Vogels
        :param h:       Höhe des Vogels
        """
        assert isinstance(model, Model)
        # Parameter setzen
        self.model = model
        self.score = 0
        self.is_alive = True
        self.rect = pygame.Rect(x, y, w, h)  # x, y, w, h
        self.angle = 0
        self.speed = 0
        self.next_tube = None

        # Bild laden
        self.img = pygame.image.load('assets/bird.gif')
        self.img = pygame.transform.scale(self.img, (w, h))
        self.img.convert()
        self.img_rotated = self.img

    def _calc_img_rotated(self):
        """
        berechnet das rotierte Bild des Vogels basierend auf self.angle und self.img
        """
        orig_rect = self.img.get_rect()
        rot_image = pygame.transform.rotate(self.img, self.angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        self.img_rotated = rot_image.subsurface(rot_rect)

    def _colliding(self, barrect, barsurface):
        """
        Berechnet, ob der Vogel mit einer Röhre Kollidiert
        :param barrect:     Rechteck, in das die Röhre gezeichnet wird
        :param barsurface:  Surface der Röhre
        :return:
        """
        # Prüfe zunächst auf Überschneidung der Rechtecke
        if not self.rect.colliderect(barrect):
            return False
        # Offset für die Überschneidungsmasken berechnen
        offset_x = barrect[0] - self.rect[0]
        offset_y = barrect[1] - self.rect[1]
        # Masken erstellen
        bird_mask = pygame.mask.from_surface(self.img, 50)
        tube_mask = pygame.mask.from_surface(barsurface, 50)
        # überschneidende Fläche berechnen
        a = bird_mask.overlap_area(tube_mask, (offset_x, offset_y))
        return a > 0

    def update(self, next_tube):
        """
        Diese Update-Methode muss jeden Game-Tick aufgerufen werden. Hier wird die Position des Vogels aktualisiert und
        auf Kollision getestet.
        :param next_tube: die nächste Röhre zur Kollisionsberechnung und für das AI-Model zur Flugberechnung
        """
        assert isinstance(next_tube, Tube)
        self.next_tube = next_tube
        if not self.is_alive:
            return
        # Positions-Updates
        self.speed -= 0.25
        if self.speed < 2.5 and self.model.calc(next_tube, self):
            self.speed = 5
        self.rect.y -= self.speed
        self.angle = self.speed * 4
        # Collision-Detection
        self._calc_img_rotated()
        if self._colliding(next_tube.top_rect, next_tube.top_img):
            self.is_alive = False
        if self._colliding(next_tube.bot_rect, next_tube.bot_img):
            self.is_alive = False

    def draw(self, surface, slow_mode=True, show_lines=True):
        """
        Rendert den Vogel auf einem gegebenen Surface
        :param surface:     Surface auf dem der Vogel gezeichnet wird
        :param slow_mode:   wenn True -> zeichne Bird des Vogels, sonst zeichne Kreis
        :param show_lines:  gibt an, ob die Linien zur nächsten Röhre gezeichnet werden sollen
        """
        if not self.is_alive:
            return
        if show_lines:
            pygame.draw.line(surface, (255, 0, 0), self.rect.center, self.next_tube.top_rect.bottomleft, 1)
            pygame.draw.line(surface, (255, 0, 0), self.rect.center, self.next_tube.bot_rect.topleft, 1)
        if slow_mode:
            surface.blit(self.img_rotated, self.rect)
        else:
            pygame.draw.circle(surface, BIRD_COLOR, self.rect.center, 30, 3)

    def print(self):
        """
        Gibt die trainierten Werte des AI-Modells aus
        """
        self.model.print()
