import tensorflow as tf
import numpy as np
import grid_2d as grid
from constants import *
import os
import random

class Player() :
    def __init__(self, game : grid.Grid) :
        self.game = game
        self.input_size = game.state_size()
        self.output_size = game.action_size()
        self.inputs = tf.keras.Input(shape = self.input_size)
        self.x = tf.keras.layers.Conv2D(64,4,strides = 2)(self.inputs)
        self.x = tf.keras.activations.relu(self.x, max_value = 6)
        self.x = tf.keras.layers.Conv2D(32,2)(self.x)
        self.x = tf.keras.activations.relu(self.x, max_value = 6)
        self.x = tf.keras.layers.Flatten()(self.x)
        self.x = tf.keras.layers.Dense(512)(self.x)
        self.x = tf.keras.activations.relu(self.x, max_value = 6)
        self.outputs = tf.keras.layers.Dense(self.output_size)(self.x)
        self.model = tf.keras.Model(inputs = self.inputs, outputs = self.outputs)
        self.load_weight()
        self.file_writer = tf.summary.create_file_writer(DQ_log)
        self.file_writer.set_as_default()
        self.score = 0
        self.cumreward = 0
        self.rounds = 1
        self.total_tick = 0

    def save_weight(self) :
        pass

    def load_weight(self, name = 'load.h5') :
        self.model.load_weights(os.path.join(DQ_save_directory, name))

    def normalize (self, n : np.array) :
        # n = tf.keras.utils.normalize(n)
        return n

    def update(self) :
        bef_state = self.normalize(np.array([self.game.get_state()]))
        q = self.model.predict(bef_state)
        m = max(q[0])
        indicies = [i for i, x in enumerate(q[0]) if x ==m]
        action = random.choice(indicies)
        reward, done = self.game.reward(action)
        self.cumreward += reward
        self.total_tick += 1
        if float(reward) == Reward_grow :
            self.score += 1
        if done :
            tf.summary.scalar('score', self.score, self.rounds)
            tf.summary.scalar('reward', self.cumreward, self.rounds)
            self.score = 0
            self.cumreward = 0
            self.rounds +=1
            
        return done