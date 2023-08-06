from random import random
from .rl_algo import Rl_algo
from .utils import Discretizer, Interpreter, Epsilon
import numpy as np

__all__ = ['Q_learning']

class Q_learning(Rl_algo):
    def __init__(self, env, discret_actions, discret_spaces, dis=0.98, lr=0.01, 
                 n_action=None, 
                 n_state=None,
                 q_init = "zeros",
                 epsilon = 1,
                 seuil_epsilon = 0.1,
                 prct_epsilon = 0.5):
        """Q-learning algorithm

        Args:
            env ([type]): [description]
            discret_actions ([type]): [description]
            discret_spaces ([type]): [description]
            dis ([type]): [description]
            lr ([type]): [description]
            n_action ([type], optional): [description]. Defaults to None.
            n_state ([type], optional): [description]. Defaults to None.
            q_init (str, optional): [description]. Defaults to "zeros".
            epsilon (int, optional): [description]. Defaults to 1.
            seuil_epsilon (float, optional): [description]. Defaults to 0.1.
            prct_epsilon (float, optional): the pourcentage mult by the n_episode to know where epsilon should stop exploring. Defaults to 0.5.

        Raises:
            NotImplementedError: [description]
        """
        super(Q_learning, self).__init__(env, discret_actions, discret_spaces, dis, lr)
        
        self.discret_spaces = discret_spaces
        self.discret_actions = discret_actions
        
        if discret_actions == False:
            if n_action == None:
                raise Exception("We need n_action discret to interpret the continuous action")
            self.n_action = n_action
            self.interpreter = Interpreter(self.n_action, self.env.action_space.low, self.env.action_space.high)
        
        if discret_spaces == False:
            if n_state == None:
                raise Exception("We need n_state discret to discretize the continuous space")
            self.n_state = n_state
            self.discretizer = Discretizer(self.n_state, self.env.observation_space.low, self.env.observation_space.high)
            
        q_fct_shape = ([self.n_state]*self.obs_dim + [self.n_action]*self.act_dim)
        if q_init == "zeros":
            self.q_fct = np.zeros(q_fct_shape)
        elif q_init == "uniform":
            self.q_fct = np.random.uniform(low=-1, high=1, size=q_fct_shape)
        else:
            raise NotImplementedError
        
        self.e = epsilon
        self.e_seuil = seuil_epsilon
        self.e_prct = prct_epsilon
        
    def train_one_epoch(self):
        done = False
        
        state = self.discretizer(self.env.reset()) if not self.discret_spaces else self.env.reset()
        reward_epoch = 0
        while not done:
            self.render()
            
            policy = np.argmax(self.q_fct, axis=-1)
            
            if self.epsilon.explore():
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
        
        self.epsilon = Epsilon(self.e, self.e_seuil, self.e_prct, n_epochs)
        
        all_rewards = []
        reward_n_ep = []
        for epoch in range(n_epochs):
            reward = self.train_one_epoch()
            all_rewards.append(reward)
            reward_n_ep.append(reward)
            if epoch % (n_epochs // 100) == 0:
                print(f"{epoch}/{n_epochs} | (Max : {np.max(reward_n_ep)} | Moyenne  : {np.mean(reward_n_ep)} ) | Moyenne totale: {np.mean(all_rewards)}")
                reward_n_ep = []
            self.epsilon.update()
            
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
        print("Q-table saved !")