import pygame
import random

COLOR_TUBE = (0, 217, 74)


class Tube:
    def __init__(self, screen_size, gap_pos=None, gap_height=200):
        self.screen_size = screen_size
        screen_w, screen_h = screen_size
        if gap_pos is None:
            gap_pos = random.randint(100, screen_h - 100 - gap_height)
        self.top_img = pygame.image.load('assets/top.png')
        self.bot_img = pygame.image.load('assets/bottom.png')
        scale_factor = screen_h / self.top_img.get_height()
        self.top_img = pygame.transform.scale(self.top_img, (
            int(self.top_img.get_width() * scale_factor), int(self.top_img.get_height() * scale_factor)))
        self.bot_img = pygame.transform.scale(self.bot_img, (
            int(self.bot_img.get_width() * scale_factor), int(self.bot_img.get_height() * scale_factor)))
        self.top_img.convert()
        self.bot_img.convert()
        self.top_rect = pygame.Rect(screen_w, gap_pos - self.top_img.get_height(), self.top_img.get_width(),
                                    self.top_img.get_height())
        self.bot_rect = pygame.Rect(screen_w, gap_pos + gap_height, self.bot_img.get_width(), self.bot_img.get_height())
        self.gap_point = self.bot_rect.x, self.bot_rect.y

    def update(self):
        self.top_rect.x -= 2
        self.bot_rect.x -= 2
        self.gap_point = self.bot_rect.x, self.bot_rect.y
        return self.top_rect.x + self.top_rect.w > 0

    def draw(self, surface, slow_mode=True):
        if slow_mode:
            surface.blit(self.top_img, self.top_rect)
            surface.blit(self.bot_img, self.bot_rect)
        else:
            pygame.draw.rect(surface, COLOR_TUBE, self.bot_rect)
            pygame.draw.rect(surface, COLOR_TUBE, self.top_rect)
