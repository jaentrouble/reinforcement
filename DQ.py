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
        self.x = tf.keras.layers.Dense(10, activation = 'linear')(self.inputs)
        self.x = tf.keras.layers.Dense(10, activation = 'sigmoid')(self.x)
        self.outputs = tf.keras.layers.Dense(self.output_size, activation = 'tanh', kernel_initializer = 'zeros')(self.x)
        self.model = tf.keras.Model(inputs = self.inputs, outputs = self.outputs)
        self.model.compile(optimizer = tf.keras.optimizers.Adam(),
                           loss = tf.keras.losses.MeanSquaredError(),
                           metrics = [tf.keras.metrics.MeanSquaredError()])
        self.t_model = tf.keras.models.clone_model(self.model)
        self.t_model.build((None, self.input_size))
        self.t_model.compile(optimizer = tf.keras.optimizers.Adam(),
                           loss = tf.keras.losses.MeanSquaredError(),
                           metrics = [tf.keras.metrics.MeanSquaredError()])
        self.t_model.set_weights(self.model.get_weights())
        self.input_buffer = np.empty((0,self.input_size))
        self.target_buffer = np.empty((0,self.output_size))
        self.count = 1
        self.acted = 0

    def choose_action (self, q : np.array) :
        """
        q: shape (1,1); [[*args]]
        """
        if random.random() < DQ_e/self.count :
            print('random')
            return random.randrange(0,len(q[0]))
        else :
            return np.argmax(q[0])

    def normalize (self, n : np.array) :
        return tf.keras.utils.normalize(n.astype('float64'))

    def update (self) :
        self.acted += 1
        bef_state = self.normalize(np.array([self.game.get_state()]))
        q = self.model.predict(bef_state)
        print(q)
        action = self.choose_action(q)
        reward, done = self.game.reward(action)
        reward = float(reward)
        aft_state = self.normalize(np.array([self.game.get_state()]))
        print(float(reward))
        if done :
            q[0, action] = reward
        else:
            q[0, action] = reward + DQ_discount * np.max(self.t_model.predict(aft_state))
            a = q[0, action]
        self.input_buffer = np.vstack((self.input_buffer, bef_state))
        self.target_buffer = np.vstack((self.target_buffer, q))
        if len(self.input_buffer) > DQ_buffer_size :
            self.input_buffer = np.delete(self.input_buffer,0,0)
        if not self.acted % 100 :
            self.count += 1
            mini_idx = random.sample(range(len(self.input_buffer)),min(DQ_mini_buffer,len(self.input_buffer)))
            mini_input = np.empty((0,self.input_size))
            mini_target = np.empty((0,self.output_size))
            for idx in mini_idx :
                mini_input = np.vstack((mini_input,self.input_buffer[idx]))
                mini_target = np.vstack((mini_target,self.target_buffer[idx]))
            self.model.fit(x = mini_input, y = mini_target, epochs = 10)
            if not self.count % 10 :
                self.t_model.set_weights(self.model.get_weights())
        return done


if __name__ == '__main__' :
    p = Player(None)
