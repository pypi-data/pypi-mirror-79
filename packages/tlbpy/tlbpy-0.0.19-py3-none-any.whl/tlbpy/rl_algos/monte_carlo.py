from .rl_algo import Rl_algo
from .utils import Discretizer, Interpreter, Epsilon
import numpy as np

class Monte_Carlo(Rl_algo):
    
    def __init__(self, env, discret_actions=True, discret_spaces=True,
                 lr = 0.01,
                 dis = 0.98,
                 n_action = None,
                 n_state = None,
                 epsilon = 1,
                 seuil_epsilon = 0.1,
                 prct_epsilon = 0.5):
        
        super(Monte_Carlo, self).__init__(env, discret_actions, discret_spaces, dis, lr)
        raise NotImplementedError
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

        self.e = epsilon
        self.e_seuil = seuil_epsilon
        self.e_prct = prct_epsilon
        
        self.policy = np.random.randint(self.n_action, size=([self.n_state]*self.obs_dim))
        self.g_table = []
        
    def train_one_epoch(self):
        done = False
        state = self.discretizer(self.env.reset()) if not self.discret_spaces else self.env.reset()
        reward_epoch = 0
        trial = []
        while not done:
            self.render()
            
            if self.epsilon.explore():
                action = np.random.randint(self.n_action)
            else :
                action = self.policy[state]
            interpreted_action = self.interpreter(action) if not self.discret_actions else action 
            
            new_state, reward, done, _ = self.env.step(interpreted_action)
            new_state = self.discretizer(new_state) if not self.discret_spaces else new_state
            
            trial.append(reward)
            reward_epoch += reward
            
            state = new_state
            
        return reward_epoch, trial
    
    def _train(self, n_epochs):
        self.epsilon = Epsilon(self.e, self.e_seuil, self.e_prct, n_epochs)
        
        for k in range(n_epochs):
            reward, trial = self.train_one_epoch()
                
            self.epsilon.update()
    
    
    def test_one(self):
        raise NotImplementedError
    
    def load_model(self, path):
        raise NotImplementedError
    
    def save_model(self, path):
        raise NotImplementedError