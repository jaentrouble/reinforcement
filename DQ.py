import tensorflow as tf
import numpy as np
import grid
import random
from constants import *
import datetime
import os

class Player () :
    def __init__(self, game : grid.Grid) :
        self.game = game
        self.input_size = game.state_size()
        self.output_size = game.action_size()
        self.inputs = tf.keras.Input(shape = (self.input_size,))
        self.x = tf.keras.layers.Dense(20)(self.inputs)
        self.x = tf.keras.activations.relu(self.x, max_value = 6)
        self.x = tf.keras.layers.Dense(8)(self.x)
        self.x = tf.keras.activations.relu(self.x, max_value = 6)
        self.x = tf.keras.layers.Dense(8)(self.x)
        self.x = tf.keras.activations.relu(self.x, max_value = 6)
        self.outputs = tf.keras.layers.Dense(self.output_size, kernel_initializer = 'zeros')(self.x)
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
        self.model.summary()
        self.count = 1
        self.acted = 0
        self.initiated = False
        self.buffer_filled = False

    def get_count(self) :
        return self.count

    def choose_action (self, q : np.array) :
        """
        q: shape (1,1); [[*args]]
        """
        if random.random() < min(DQ_e, DQ_e/(0.1*self.count)) :
            print('random')
            return random.randrange(0,len(q[0]))
        else :
            m = max(q[0])
            indices = [i for i, x in enumerate(q[0]) if x == m]
            return random.choice(indices)

    def normalize (self, n : np.array) :
        n = tf.keras.utils.normalize(n)
        return n.astype('float64')

    def rand_generator(self, n : int, level : int) :
        state_vec = []
        q_vec = []
        original_length = self.game.get_snake_length()
        for l in range(level) :
            self.game.set_snake_length(original_length+l)
            for i in range(n) :
                done = False
                while not done :
                    state = self.normalize(self.game.get_state())
                    action = random.randrange(0,self.output_size)
                    reward, done = self.game.reward(action)
                    q = []
                    for _ in range(self.output_size):
                        q.append(0)
                    q[action] = reward
                    state_vec.append(state[0])
                    q_vec.append(q)
                self.game.reset()
                if not i % 100 :
                    print('Snake length : {}'.format(original_length+l))
                    print('Generating Random vectors : {0} / {1}'.format(i,n))
                    print('Vector size : {0}'.format(len(q_vec)))
        self.game.set_snake_length(original_length)
        return np.array(state_vec), np.array(q_vec)

    def save_weight(self) :
        now = datetime.datetime.now()
        filename = '{0}_{1}_{2}_{3}_{4}.h5'.format(now.month, now.day, now.hour, now.minute, now.second)
        self.model.save_weights(os.path.join(DQ_save_directory, filename))

    def load_weight(self, name = 'load.h5') :
        self.model.load_weights(os.path.join(DQ_save_directory, name))
        self.initiated = True

    def update (self) :
        if not self.initiated :
            r_states, r_qs = self.rand_generator(DQ_generate_random, DQ_generate_level)
            self.model.fit(x = r_states, y = r_qs, epochs = DQ_random_epoch)
            self.initiated = True
        self.acted += 1
        bef_state = self.normalize(np.array([self.game.get_state()]))
        # print(bef_state)
        q = self.model.predict(bef_state)
        print(q)
        action = self.choose_action(q)
        reward, done = self.game.reward(action)
        reward = DQ_reward_mul*float(reward)
        if not done :
            aft_state = self.normalize(np.array([self.game.get_state()]))
        print(float(reward))
        if done :
            q[0, action] = reward
        else:
            q[0, action] = reward + DQ_discount * np.max(self.t_model.predict(aft_state))
            # a = q[0, action]
        self.input_buffer = np.vstack((self.input_buffer, bef_state))
        self.target_buffer = np.vstack((self.target_buffer, q))
        if len(self.input_buffer) > DQ_buffer_size :
            self.buffer_filled = True
            self.input_buffer = np.delete(self.input_buffer,0,0)
            self.target_buffer = np.delete(self.target_buffer,0,0)
        if not self.acted % 100 and self.buffer_filled:
            self.count += 1
            mini_idx = random.sample(range(len(self.input_buffer)),min(DQ_mini_buffer,len(self.input_buffer)))
            mini_input = np.empty((0,self.input_size))
            mini_target = np.empty((0,self.output_size))
            for idx in mini_idx :
                mini_input = np.vstack((mini_input,self.input_buffer[idx]))
                mini_target = np.vstack((mini_target,self.target_buffer[idx]))
            self.model.fit(x = mini_input, y = mini_target, epochs = DQ_epoch)
            if not self.count % 10 :
                self.t_model.set_weights(self.model.get_weights())
        return done


if __name__ == '__main__' :
    p = Player(None)
