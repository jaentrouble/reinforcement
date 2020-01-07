import tensorflow as tf
import numpy as np
import grid
import random
from constants import *

class Player () :
    def __init__(self, game : grid.Grid) :
        self.game = game
        self.input_size = game.state_size()
        self.output_size = game.action_size()
        self.inputs = tf.keras.Input(shape = (self.input_size,))
        self.x = tf.keras.layers.Dense(8, activation = 'sigmoid')(self.inputs)
        self.x = tf.keras.layers.Dense(8, activation = 'sigmoid')(self.x)
        self.outputs = tf.keras.layers.Dense(self.output_size, activation = 'sigmoid')(self.x)
        self.model = tf.keras.Model(inputs = self.inputs, outputs = self.outputs)
        self.model.compile(optimizer = tf.keras.optimizers.Adam(),
                           loss = tf.keras.losses.MeanSquaredError(),
                           metrics = [tf.keras.metrics.MeanSquaredError()])

        self.input_buffer = np.empty((0,self.input_size))
        self.target_buffer = np.empty((0,self.output_size))

    def choose_action (self, q : np.array) :
        """
        q: shape (1,1); [[*args]]
        """
        if random.random() < DQ_e :
            return random.randrange(0,len(q[0]))
        else :
            return np.argmax(q[0])

    def update (self) :
        bef_state = np.array([self.game.get_state()])
        q = self.model.predict(bef_state)
        action = self.choose_action(q)
        reward, done = self.game.reward(action)
        aft_state = np.array([self.game.get_state()])
        
        if done :
            q[0, action] = reward
        else:
            q[0, action] = reward + DQ_discount * np.max(self.model.predict(aft_state))
        self.input_buffer = np.vstack((self.input_buffer, bef_state))
        self.target_buffer = np.vstack((self.target_buffer, q))

        if len(self.input_buffer) >= DQ_buffer_size :
            self.model.fit(x = self.input_buffer, y = self.target_buffer)
            self.input_buffer = np.empty((0,self.input_size))
            self.target_buffer = np.empty((0,self.output_size))
        return done


if __name__ == '__main__' :
    p = Player(None)
