import numpy as np
import os
import datetime
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3
RU = 0
LU = 1
LD = 2
RD = 3

G_TRAP = 0
G_EMPTY = 1
G_SNAKE = 2
G_APPLE = 3

DIRECTION_LIST = [[1,0],[0,-1],[-1,0],[0,1]]

MOVE_RIGHT = 0
MOVE_FORWARD = 1
MOVE_LEFT = 2
MOVE_BACKWARD = 3

DIRECTION_CONVERT = [[DOWN,RIGHT,UP,LEFT],[RIGHT,UP,LEFT,DOWN],[UP,LEFT,DOWN,RIGHT],[LEFT,DOWN,RIGHT,UP]]
ROTATION_ARRAY = [
    np.array([[0,-1],[1,0]]),
    np.array([[1,0],[0,1]]),
    np.array([[0, 1],[-1,0]]),
    np.array([[-1,0],[0,-1]])
    ]

DEAD = -1
MOVED = 1
GROW = 2

B_size = 10
Init_health = 1000
Apple_health = 200
Consume_health = 1

Q_e = 0.3
Q_gamma = 0.7
Q_alpha = 0.1

DQ_discount = 0.99
DQ_e = 0.1
DQ_e_min = 0.01
DQ_e_nstep = 500000
DQ_buffer_size = 100000
DQ_learn_start = 10000
DQ_mini_buffer = 32
DQ_reward_mul = 1
DQ_epoch = 1
DQ_random_epoch = 1
DQ_generate_random = 500
DQ_generate_level = 5
DQ_target_update = 20000
DQ_save_directory = 'savefiles'
DQ_save_rate = 100000
now = datetime.datetime.now()
DQ_log = os.path.join(
    'records',
    '{0}_{1}_{2}_{3}_{4}'.format(now.month, now.day, now.hour, now.minute, now.second),
)

Reward_grow = 0.7
Reward_dead = -1
# Reward_apple_distance = True
Reward_movement_close = 0.1
Reward_movement_far = -0.2