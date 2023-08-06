from random import random
from .rl_algo import Rl_algo
from .utils import Discretizer, Interpreter
import numpy as np

__all__ = ['Q_learning']

class Q_learning(Rl_algo):
    def __init__(self, env, discret_actions, discret_spaces, dis=0.98, lr=0.01, 
                 n_actions=None, 
                 n_spaces=None,
                 q_init = "zeros",
                 epsilon = 1,
                 seuil_epsilon = 0.1,
                 end_epsilon = 0.5):
        """Q-learning algorithm

        Args:
            env ([type]): [description]
            discret_actions ([type]): [description]
            discret_spaces ([type]): [description]
            dis ([type]): [description]
            lr ([type]): [description]
            n_actions ([type], optional): [description]. Defaults to None.
            n_spaces ([type], optional): [description]. Defaults to None.
            q_init (str, optional): [description]. Defaults to "zeros".
            epsilon (int, optional): [description]. Defaults to 1.
            seuil_epsilon (float, optional): [description]. Defaults to 0.1.
            end_epsilon (float, optional): the pourcentage mult by the n_episode to know where epsilon should stop exploring. Defaults to 0.5.

        Raises:
            NotImplementedError: [description]
        """
        super(Q_learning, self).__init__(env, discret_actions, discret_spaces, dis, lr)
        if discret_actions == False:
            if n_actions == None:
                raise Exception("We need n_actions discret to interpret the continuous action")
            self.n_action = n_actions
            self.interpreter = Interpreter(self.n_action, self.env.action_space.low, self.env.action_space.high)
        
        self.discret_spaces = discret_spaces
        self.discret_actions = discret_actions
        
        if discret_spaces == False:
            if n_spaces == None:
                raise Exception("We need n_spaces discret to discretize the continuous space")
            self.n_space = n_spaces
            self.discretizer = Discretizer(self.n_space, self.env.observation_space.low, self.env.observation_space.high)
            
        q_fct_shape = ([self.n_space]*self.obs_dim + [self.n_action]*self.act_dim)
        if q_init == "zeros":
            self.q_fct = np.zeros(q_fct_shape)
        elif q_init == "uniform":
            self.q_fct = np.random.uniform(low=-1, high=1, size=q_fct_shape)
        else:
            raise NotImplementedError
        
        self.epsilon = epsilon
        self.seuil_epsilon = seuil_epsilon
        self.end_epsilon = end_epsilon
        
    def train_one_epoch(self):
        done = False
        
        state = self.discretizer(self.env.reset()) if not self.discret_spaces else self.env.reset()
        reward_epoch = 0
        while not done:
            self.render()
            
            policy = np.argmax(self.q_fct, axis=-1)
            
            if random() <= self.epsilon:
                action = np.random.randint(self.n_action)
            else:
                action = policy[state]
            
            interpreted_action = self.interpreter(action) if not self.discret_actions else action
            new_state, reward, done, _ = self.env.step(interpreted_action)
            new_state = self.discretizer(new_state) if not self.discret_spaces else new_state
            reward_epoch += reward
            
            self.q_fct[state][action] += self.lr * (reward + np.max(self.dis * self.q_fct[new_state]) - self.q_fct[state][action])
            
            state = new_state
            
        return reward_epoch
            
    def _train(self, n_epochs):
        
        end_epsilon = int(n_epochs*self.end_epsilon)
        pas_epsilon = self.epsilon / (end_epsilon - 1)
        
        all_rewards = []
        reward_n_ep = []
        for epoch in range(n_epochs):
            reward = self.train_one_epoch()
            all_rewards.append(reward)
            reward_n_ep.append(reward)
            if epoch % (n_epochs // 100) == 0:
                print(f"{epoch}/{n_epochs} | (Max : {np.max(reward_n_ep)} | Moyenne  : {np.mean(reward_n_ep)} ) | Moyenne totale: {np.mean(all_rewards)}")
                reward_n_ep = []
            self.epsilon -= pas_epsilon if self.epsilon - pas_epsilon >= self.seuil_epsilon else 0
    
    def test_one(self):
        done = False
        tot_rewards = 0
        state = self.discretizer(self.env.reset()) if not self.discret_spaces else self.env.reset()
        
        while not done:
            self.render(True)
            policy = np.argmax(self.q_fct, axis=-1)
            action = policy[state]
            interpreted_action = self.interpreter(action) if not self.discret_actions else action
            new_state, reward, done, _ = self.env.step(interpreted_action)
            new_state = self.discretizer(new_state) if not self.discret_spaces else new_state
            tot_rewards += reward
            
            state = new_state
            
        return tot_rewards
    
    def load_model(self, path):
        self.q_fct = np.load(path)
    
    def save_model(self, path):
        np.save(path, self.q_fct)