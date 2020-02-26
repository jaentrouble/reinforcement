import tensorflow as tf
import numpy as np
import grid_2d as grid
import random
from constants import *
import datetime
import os

class Player () :
    def __init__(self, game : grid.Grid) :
        self.game = game
        self.input_size = game.state_size()
        self.output_size = game.action_size()
        self.inputs = tf.keras.Input(shape = self.input_size)
        self.x = tf.keras.layers.Conv2D(32,3,padding='same')(self.inputs)
        self.x = tf.keras.activations.relu(self.x, max_value = 6)
        self.x = tf.keras.layers.Conv2D(32,2,strides=2)(self.x)
        self.x = tf.keras.activations.relu(self.x, max_value = 6)
        self.x = tf.keras.layers.Flatten()(self.x)
        self.x = tf.keras.layers.Dense(512)(self.x)
        self.x = tf.keras.activations.relu(self.x, max_value = 6)
        self.outputs = tf.keras.layers.Dense(self.output_size)(self.x)
        self.model = tf.keras.Model(inputs = self.inputs, outputs = self.outputs)
        self.model.compile(optimizer = tf.keras.optimizers.Adam(),
                           loss = tf.keras.losses.MeanSquaredError(),
                           metrics = [tf.keras.metrics.MeanSquaredError()])
        self.t_model = tf.keras.models.clone_model(self.model)
        self.t_model.build(self.input_size)
        self.t_model.compile(optimizer = tf.keras.optimizers.Adam(),
                           loss = tf.keras.losses.MeanSquaredError(),
                           metrics = [tf.keras.metrics.MeanSquaredError()])
        self.t_model.set_weights(self.model.get_weights())
        if not os.path.exists(DQ_log):
            os.makedirs(DQ_log)
        self.file_writer = tf.summary.create_file_writer(DQ_log)
        self.file_writer.set_as_default()
        self.input_buffer = np.zeros((DQ_buffer_size,*self.input_size),dtype=int)
        self.target_buffer = np.zeros((DQ_buffer_size,self.output_size))
        self.model.summary()
        self.count = 1
        self.rounds = 1
        self.initiated = False
        self.buffer_filled = False

    def get_count(self) :
        return self.count

    def e_decay(self) :
        if self.count > DQ_e_nstep :
            return DQ_e_min
        else :
            return DQ_e - (DQ_e-DQ_e_min)*(self.count/DQ_e_nstep)

    def choose_action (self, q : np.array) :
        """
        q: shape (1,1); [[*args]]
        """
        if random.random() < self.e_decay() :
            print('random')
            return random.randrange(0,len(q[0]))
        else :
            m = max(q[0])
            indices = [i for i, x in enumerate(q[0]) if x == m]
            return random.choice(indices)

    def normalize (self, n : np.array) :
        # n = tf.keras.utils.normalize(n)
        return n

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
                    state_vec.append(state)
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
            self.tick = 0
            self.total_tick = 0
            self.score = 0
            self.cumreward =0
            self.initiated = True
        bef_state = self.normalize(np.array([self.game.get_state()]))
        # print(bef_state)
        q = self.model.predict(bef_state)
        # print(q)
        action = self.choose_action(q)
        reward, done = self.game.reward(action)
        self.cumreward += reward
        self.tick += 1
        self.total_tick += 1
        if float(reward) == Reward_grow :
            self.score += 1
        if done :
            tf.summary.scalar('score', self.score, self.rounds)
            tf.summary.scalar('score_per_tick', self.score/self.tick, self.rounds)
            tf.summary.scalar('reward', self.cumreward, self.rounds)
            self.score = 0
            self.tick = 0
            self.cumreward = 0
            self.rounds += 1
        reward = DQ_reward_mul*float(reward)
        if not done :
            aft_state = self.normalize(np.array([self.game.get_state()]))
        # print(float(reward))
        if done :
            q[0, action] = reward
        else:
            q[0, action] = reward + DQ_discount * np.max(self.t_model.predict(aft_state))
            # a = q[0, action]
        self.input_buffer[self.total_tick%DQ_buffer_size] = bef_state[0]
        self.target_buffer[self.total_tick%DQ_buffer_size] = q[0]
        if not self.buffer_filled :
            print('filling buffer {0}/{1}'.format(self.total_tick, DQ_buffer_size))
            if self.total_tick > DQ_buffer_size:
                self.buffer_filled = True
        else :
            self.count += 1
            mini_idx = random.sample(range(len(self.input_buffer)),min(DQ_mini_buffer,len(self.input_buffer)))
            mini_input = np.zeros((DQ_mini_buffer,*self.input_size),dtype=int)
            mini_target = np.zeros((DQ_mini_buffer,self.output_size))
            for n,idx in enumerate(mini_idx) :
                mini_input[n] = self.input_buffer[idx]
                mini_target[n] = self.target_buffer[idx]
            self.model.fit(
                x = mini_input, 
                y = mini_target, 
                epochs = DQ_epoch,
                verbose = 0,
            )
            if not self.count % DQ_target_update :
                self.t_model.set_weights(self.model.get_weights())
        return done


if __name__ == '__main__' :
    p = Player(None)
