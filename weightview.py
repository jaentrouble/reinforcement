import tensorflow as tf
import numpy as numpy
import DQ
import grid

game = grid.Grid(20,20,3, True, 0)

p = DQ.Player(game)
p.load_weight()
model = p.model
layers = model.layers
for l in layers :
    print(l.get_weights())