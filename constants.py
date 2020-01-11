RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3

DEAD = -1
MOVED = 1
GROW = 2

B_size = 10
Init_health = 100
Apple_health = 100
Consume_health = 1
Q_e = 0.3
Q_gamma = 0.7
Q_alpha = 0.1

DQ_discount = 0.9
DQ_e = 1
DQ_buffer_size = 100
DQ_mini_buffer = 20

Reward_grow = 1
Reward_dead = -1
# Reward_apple_distance = True
Reward_movement = 1