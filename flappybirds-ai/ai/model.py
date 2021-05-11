from game.tube import Tube

import random
import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class NeuralNetworkLayer:
    def __init__(self, input_dim, output_dim, weights=None, next_layer=None):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.weights = weights
        self.next_layer = next_layer
        if weights is None:
            self.weights = [[0.1 * (random.random() - 0.5)] * input_dim] * output_dim

    def forward(self, x):
        output = []
        assert isinstance(x, list)
        assert len(x) == self.input_dim
        for weight_list in self.weights:
            out_sum = 0
            for i in range(self.input_dim):
                out_sum += weight_list[i] * x[i]
            output.append(sigmoid(out_sum))
        if self.next_layer == None:
            return output
        else:
            return self.next_layer.forward(output)

    def mutate(self, amount):
        if self.next_layer != None:
            self.next_layer.mutate(amount)
        for i in range(self.output_dim):
            for j in range(self.input_dim):
                self.weights[i][j] += amount * (random.random() - 0.5)

    def copy(self):
        nl = None
        if self.next_layer != None:
            nl = self.next_layer.copy()
        new_weights = [w.copy() for w in self.weights]
        return NeuralNetworkLayer(self.input_dim, self.output_dim, new_weights, nl)

    def print(self):
        print(self.weights)


class Model():
    def __init__(self, screen_size, layer1=None):
        self.screen_size = screen_size
        self.layer1 = layer1
        if self.layer1 is None:
            self.layer1 = NeuralNetworkLayer(4, 1)

    def calc(self, next_tube, bird):
        w, h = self.screen_size
        assert isinstance(next_tube, Tube)

        x, y1 = next_tube.top_rect.bottomleft
        _, y2 = next_tube.bot_rect.topleft
        y3 = bird.rect.y

        x /= w
        y1 /= h
        y2 /= h
        y3 /= h

        out = self.layer1.forward([x, y1, y2, y3])
        return out[0] > 0.5

    def mutate(self):
        self.layer1.mutate(0.1)

    def copy(self):
        return Model(self.screen_size, self.layer1.copy())

    def print(self):
        self.layer1.print()
