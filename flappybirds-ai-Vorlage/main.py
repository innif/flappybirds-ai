from game.game import Game
from game.bird import Bird
from ai.model import Model

import pygame
import sys


def run():
    size = (400, 600)
    sample_size = 10
    models = []
    clock = pygame.time.Clock()
    slow_mode = True

    # sample_size Modelle generieren
    for i in range(sample_size):
        model = Model(size)
        model.mutate()
        models.append(model)

    # Spiel aufsetzen
    my_game = Game(size=size, tube_period=150)
    for m in models:
        my_bird = Bird(m)
        my_game.add_bird(my_bird)
    my_game.start()

    # Spiel simulieren
    while my_game.birds_alive > 0:
        my_game.update()
        my_game.render(slow_mode)
        if slow_mode:
            clock.tick(60)  # FPS auf 60 begrenzen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # wenn man auf das rote Kreuz drückt:
                sys.exit()
            if event.type == pygame.KEYDOWN:  # wenn man auf eine Taste drückt:
                slow_mode = not slow_mode
    my_game.update()

    # Vögel nach scores sortieren
    birds = my_game.bird_list
    birds.sort(reverse=True, key=lambda b: b.score)

if __name__ == '__main__':
    run()
