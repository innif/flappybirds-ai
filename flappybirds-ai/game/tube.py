import pygame
import random

COLOR_TUBE = (0, 217, 74)  # Farbe der Röhre, wenn als Rechteck gezeichnet


class Tube:
    def __init__(self, screen_size, gap_pos=None, gap_height=200):
        """
        Konstruktor eines Röhrenpaars
        :param screen_size:     Größe des Screens, auf den die Röhren gezeichnet werden
        :param gap_pos:         Position der Lücke zwischen den Röhren
        :param gap_height:      Größe der Lücke zwischen den Röhren
        """
        self.screen_size = screen_w, screen_h = screen_size  # Größe des Screens, auf dem gemalt wird

        # Bilder
        self.top_img = pygame.image.load('assets/top.png')  # Bilder laden
        self.bot_img = pygame.image.load('assets/bottom.png')
        scale_factor = screen_h / self.top_img.get_height()  # Skalierungsfaktor berechnen
        self.top_img = pygame.transform.scale(self.top_img, (  # Bilder skalieren
            int(self.top_img.get_width() * scale_factor), int(self.top_img.get_height() * scale_factor)))
        self.bot_img = pygame.transform.scale(self.bot_img, (
            int(self.bot_img.get_width() * scale_factor), int(self.bot_img.get_height() * scale_factor)))
        self.top_img.convert()
        self.bot_img.convert()

        # Positionen
        if gap_pos is None:
            gap_pos = random.randint(100, screen_h - 100 - gap_height)  # legt die Position der Lücke zufällig fest
        self.top_rect = pygame.Rect(screen_w, gap_pos - self.top_img.get_height(), self.top_img.get_width(),
                                    self.top_img.get_height())
        self.bot_rect = pygame.Rect(screen_w, gap_pos + gap_height, self.bot_img.get_width(), self.bot_img.get_height())

    def update(self):
        """
        Diese Methode muss jeden Game-Cycle aufgerufen werden, um die Position der Röhre zu berechnen.
        :rtype: bool
        :return: True, wenn die Röhre das Bild nach links verlassen hat
        """
        # verschiebe beide Röhren um 2 nach links
        self.top_rect.x -= 2
        self.bot_rect.x -= 2
        # gib aus, ob die Röhre das Bild verlassen hat
        return self.top_rect.x + self.top_rect.w < 0

    def draw(self, surface, slow_mode=True):
        """
        Diese Methode rendert die Röhre auf dem Bildschirm
        :param surface:     Surface, auf dem die Röhre gezeichnet werden soll
        :param slow_mode:   wenn True werden die Bitmaps benutzt, sonst nur Rechtecke
        """
        if slow_mode:
            # zeichne im slow-mode die Bilder
            surface.blit(self.top_img, self.top_rect)
            surface.blit(self.bot_img, self.bot_rect)
        else:
            # andernfalls zeichne Rechtecke
            pygame.draw.rect(surface, COLOR_TUBE, self.bot_rect)
            pygame.draw.rect(surface, COLOR_TUBE, self.top_rect)
