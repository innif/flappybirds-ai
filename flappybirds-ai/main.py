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
    slow_mode = False

    # sample_size Modelle generieren
    for i in range(sample_size):
        model = Model(size)
        model.mutate()
        models.append(model)

    iteration = 0

    while True:
        # Spiel aufsetzen
        my_game = Game(size=size, tube_period=150)
        for m in models:
            my_bird = Bird(m)
            my_game.add_bird(my_bird)
        my_game.start()

        # Spiel simulieren, bis beste Hälfte ermittelt wurde
        while my_game.birds_alive > sample_size / 2 - 1:
            my_game.update()
            my_game.render(slow_mode)
            if slow_mode:
                clock.tick(60)  # FPS auf 60 begrenzen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # wenn man auf das rote Kreuz drückt:
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # wenn man auf das rote Kreuz drückt:
                    slow_mode = not slow_mode
        my_game.update()

        # Vögel nach scores sortieren
        birds = my_game.bird_list
        birds.sort(reverse=True, key=lambda b: b.score)

        # Besten Vogel ausgeben
        print("\nIteration: {}, Score: {}".format(iteration, birds[0].score))
        birds[0].print()

        # Models aus der besten Hälfte der Vögel extrahieren
        models = [b.model for b in birds[0:int(sample_size / 2)]]

        # beste Vögel übernehmen und mutieren
        new_models = []
        for m in models:
            new = m.copy()
            new.mutate()
            new_models.append(new)
            new_models.append(m)
        models = new_models

        # Iteration hochzählen
        iteration += 1


if __name__ == '__main__':
    run()
