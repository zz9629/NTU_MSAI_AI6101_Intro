import collections

from matplotlib import pyplot as plt
from IPython.display import clear_output

from environment import CliffBoxPushingBase
from DrawMap import DrawMap
from collections import defaultdict
import numpy as np
import random
import time
import os

# SARSA or value iteration, policy iteration;
# Novel RL ideas are welcome and will receive bonus credit.
# Q-learning algorithm
class QAgent(object):
    def __init__(self):
        self.action_space = [1, 2, 3, 4]
        self.V = []
        self.Q = defaultdict(lambda: np.zeros(len(self.action_space)))
        self.discount_factor = 0.99
        self.alpha = 0.5
        self.epsilon = 0.01

    def take_action(self, state):
        if random.random() < self.epsilon:
            action = random.choice(self.action_space)
        else:
            action = self.action_space[np.argmax(self.Q[state])]
        return action

    # implement your train/update function to update self.V or self.Q
    # you should pass arguments to the train function
    def train(self, state, action, next_state, reward):
        # Update The Q-Value
        action -= 1
        self.Q[state][action] = self.Q[state][action] * (1 - self.alpha) + \
                self.alpha * (reward + self.discount_factor * np.max(self.Q[next_state]))
        # pass

# Show or plot the learning progress: episode rewards vs. episodes
def drawDiagram(path, x, y):
    if not os.path.isdir(path):
        os.mkdir(path)

    plt.figure()
    x = list(range(x))

    plt.plot(x, y)
    plt.xlabel("Episodes")
    plt.ylabel("Episode rewards")
    plt.title("Episode rewards change as episode goes on!")
    print("saving learning curve...")
    plt.show()
    plt.savefig(os.path.join(path, 'reward.png'))

'''
    Load the map of cliff
    return the collection of locations
'''
def generationCliff_loc():
    cliff_loc = []

    DEFAULT_DANGER_REGION = collections.OrderedDict({
        'A': [(2, 3), (5, 3)],
        'B': [(0, 6), (3, 6)],
        'C': [(0, 9), (2, 9)],
        'D': [(4, 9), (5, 9)],
        'E': [(2, 12), (5, 12)],
    })

    for _, region in DEFAULT_DANGER_REGION.items():
        A, B = region
        assert A[1] == B[1], "A[1] != B[1]"
        for i in range(A[0], B[0] + 1):
            cliff_loc.append((i, A[1]))
    return cliff_loc


'''
    3 episode for testing the Q values, and show the grid world simultaneously.
'''
def testNshow(env, agent):
    cliff_loc = generationCliff_loc()
    goal_pos = (4, 13)
    teminated = False
    rewards = []
    time_step = 0
    for episode in range(3):
        env.reset()
        print("*****EPISODE ", episode + 1, "*****\n\n\n\n")
        time.sleep(1)

        while not teminated:
            clear_output(wait=True)
            #         env.render()
            (agent_pos, box_pos) = env.get_state()
            DrawMap(agent.Q, agent_pos, box_pos, goal_pos, cliff_loc)
            time.sleep(0.3)

            state = env.get_state()
            action = agent.take_action(state)
            reward, teminated, _ = env.step([action])
            rewards.append(reward)
            time_step += 1

        clear_output(wait=True)
        #     env.render()
        (agent_pos, box_pos) = env.get_state()
        DrawMap(agent.Q, agent_pos, box_pos, goal_pos, cliff_loc)
        teminated = False

        time.sleep(3)
        clear_output(wait=True)


if __name__ == '__main__':
    env = CliffBoxPushingBase()
    # you can implement other algorithms
    agent = QAgent()
    print(agent.Q)
    agent.
    teminated = False
    rewards = []
    time_step = 0
    num_iterations = 10000
    rewards_all_episodes = []
    for i in range(num_iterations):
        env.reset()
        while not teminated:
            state = env.get_state()
            action = agent.take_action(state)
            # print(action)
            reward, teminated, _ = env.step([action])
            next_state = env.get_state()
            rewards.append(reward)
            time_step += 1
            agent.train(state, action, next_state, reward)
            if i % 100 == 0:
                print('i:', i)
                print(f'step: {time_step-1}, actions: {action}, reward: {reward}')
                print(f'rewards: {sum(rewards)}')
                print(f'print the historical actions: {env.episode_actions}')
        teminated = False
        rewards_current_episode = sum(rewards)
        rewards_all_episodes.append(rewards_current_episode)
        rewards = []

    path='diagrams/'
    # drawDiagram(path, num_iterations, rewards_all_episodes)
    env.print_world()
    time.sleep(0.5)

    # print(agent.Q)

    testNshow(env, agent)
    env.close()