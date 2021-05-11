from game.tube import Tube

import random


class Model:
    def __init__(self, screen_size, params=None):
        """
        Konstruktor für ein Modell
        :param screen_size: Größe des Spielbildschirms
        :param params: Parameter des Modells
        """
        if params is None:  # setze Parameter auf einen Standardwert
            params = [0, 0, 0, 0]
        self.screen_size = screen_size
        self.params = params

    def calc(self, next_tube, bird):
        """
        Berechnet Angand der Inputs, ob der Vogel springen soll
        :param next_tube:   nächste Röhre
        :param bird:        Vogel, für den berechnet wird
        :return:            True, wenn Vogel springen soll
        """
        assert isinstance(next_tube, Tube)
        # Inputs extrahieren
        x, y1 = next_tube.top_rect.bottomleft
        _, y2 = next_tube.bot_rect.topleft
        y3 = bird.rect.y
        # Inputs normalisieren
        w, h = self.screen_size
        x /= w
        y1 /= h
        y2 /= h
        y3 /= h
        # Inputs in Liste schreiben
        inputs = [x, y1, y2, y3]
        # aus Inputs und Parametern output berechnen
        out = 0
        for i, value in enumerate(inputs):
            out += value * self.params[i]
        # Ausgeben, ob der Vogel springen soll
        return out > 0

    def mutate(self, amount=0.3):
        """
        lässt das Modell mutieren
        :param amount: die Stärke der Mutation
        """
        for i in range(len(self.params)):
            self.params[i] += amount * (random.random() - 0.5)

    def copy(self):
        """
        Erstellt eine Kopie dieses Modells
        :return: Kopie dieses Modells
        """
        return Model(self.screen_size, self.params.copy())

    def print(self):
        """
        Gibt die Parameter dieses Modells aus
        """
        print(self.params)
