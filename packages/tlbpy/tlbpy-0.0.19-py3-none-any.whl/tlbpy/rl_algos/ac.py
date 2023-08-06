from .rl_algo import Rl_algo
from .utils import Discretizer, Interpreter, Epsilon
import numpy as np


class Actor_Critic(Rl_algo):
    
    def __init__(self, env, discret_actions=True, discret_spaces=True,
                 lr = 0.01,
                 dis = 0.98,
                 n_action = None,
                 n_state = None,
                 epsilon = 1,
                 seuil_epsilon = 0.1,
                 prct_epsilon = 0.5):
        
        super(Actor_Critic, self).__init__(env, discret_actions, discret_spaces, dis, lr)
        
                
    def train_one_epoch(self):
        raise NotImplementedError
    
    def _train(self, n_epochs):
        raise NotImplementedError
    
    def test_one(self):
        raise NotImplementedError
    
    def load_model(self, path):
        raise NotImplementedError
    
    def save_model(self, path):
        raise NotImplementedError