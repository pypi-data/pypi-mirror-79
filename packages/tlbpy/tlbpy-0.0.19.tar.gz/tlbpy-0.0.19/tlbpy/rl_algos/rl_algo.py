
__all__ = ['Rl_algo']

class Rl_algo:
    
    def __init__(self, env, 
                 discret_actions=True, 
                 discret_spaces=True,
                 dis = 0.98,
                 lr = 0.01):
        self.env = env
        self.act_dim = 1
        if discret_actions:
            self.n_action = env.action_space.n
        if discret_spaces:
            self.n_state = env.observation_space.n
            self.obs_dim = 1
        else:
            self.obs_dim = env.observation_space.shape[0]
        self.lr = lr
        self.dis = dis
        
    def render(self, aff=False):
        if aff:
            self.env.render()
            
    def train(self, n_epochs=1, path = None):
        self._train(n_epochs)
        if path:
            self.save_model(path)
            
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