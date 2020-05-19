import tensorflow as tf
import numpy as np
import DQ_1d as dq
from constants import *
import os
import random

class Player() :
    def __init__(self, game) :
        self.game = game
        tmp = dq.Player(game)
        self.model = tf.keras.Model.from_config(tmp.model.get_config())
        self.normalize = tmp.normalize
        self.choose_action = tmp.choose_action
        self.load_weight()
        self.file_writer = tf.summary.create_file_writer(DQ_log)
        self.file_writer.set_as_default()
        self.score = 0
        self.cumreward = 0
        self.rounds = 1
        self.total_tick = 0
        del tmp

    def save_weight(self) :
        pass

    def e_decay(self) :
        return DQ_e_min

    def load_weight(self, name = 'load.h5') :
        self.model.load_weights(os.path.join(DQ_save_directory,'DQ_1D', name))

    def update(self) :
        bef_state = self.normalize(np.array([self.game.get_state()]))
        q = self.model.predict(bef_state)
        action = self.choose_action(q)
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