
__all__ = ['Rl_algo']

class Rl_algo:
    
    def __init__(self, env, 
                 discret_actions=True, 
                 discret_spaces=True,
                 dis = 0.98,
                 lr = 0.01):
        self.env = env
        self.act_dim = env.action_space.n if discret_actions else env.action_space.shape[0]
        self.obs_dim = env.observation_space.n if discret_spaces else env.observation_space.shape[0]
        self.lr = lr
        self.dis = dis
        
    def render(self, aff=False):
        if aff:
            self.env.render()
            
    def train_one_epoch(self):
        raise NotImplementedError
    
    def _train(self, n_epochs):
        raise NotImplementedError
    
    def train(self, n_epochs=1, path = None):
        self._train(n_epochs)
        if path:
            self.save_model(path)
    
    def test_one(self):
        raise NotImplementedError
    
    def load_model(self, path):
        raise NotImplementedError
    
    def save_model(self, path):
        raise NotImplementedError