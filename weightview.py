import tensorflow as tf
import numpy as numpy
import DQ
import grid

game = grid.Grid(20,20,3, True, 0)

p1 = DQ.Player(game)
p1.load_weight('2.h5')
p2 = DQ.Player(game)
p2.load_weight('3.h5')
model1 = p1.model
model2 = p2.model
layers1 = model1.layers
layers2 = model2.layers
l_1_1 = layers1[1].get_weights()
l_2_1 = layers2[1].get_weights()
print(l_1_1[0]-l_2_1[0])
print(l_1_1[1]-l_2_1[1])