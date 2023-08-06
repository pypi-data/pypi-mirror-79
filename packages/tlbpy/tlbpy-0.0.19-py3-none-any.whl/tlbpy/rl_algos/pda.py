from .rl_algo import Rl_algo
from .utils import Discretizer, Interpreter, Epsilon
import numpy as np
from matplotlib import pyplot as plt


class Dynamic_Programming(Rl_algo):
    
    def __init__(self, env, discret_actions=True, discret_spaces=True,
                 lr = 0.01,
                 dis = 0.98,
                 n_action = None,
                 n_state = None,
                 epsilon = 1,
                 seuil_epsilon = 0.1,
                 prct_epsilon = 0.5):
        
        super(Dynamic_Programming, self).__init__(env, discret_actions, discret_spaces, dis, lr)
        
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
        self.freq_s_a = np.zeros(([self.n_state]*self.obs_dim + [self.n_action]*self.act_dim))
        self.freq_out_s_a = np.zeros(([self.n_state]*self.obs_dim + [self.n_state]*self.obs_dim + [self.n_action]*self.act_dim))
        self.states_seen = []
        self.r_fct = np.zeros(([self.n_state]*self.obs_dim))
        self.v_fct = np.zeros(([self.n_state]*self.obs_dim))
        self.model = np.zeros(([self.n_state]*self.obs_dim + [self.n_state]*self.obs_dim + [self.n_action]*self.act_dim))
           
    def train_one_epoch(self):
        done = False
        state = self.discretizer(self.env.reset()) if not self.discret_spaces else self.env.reset()
        reward_epoch = 0
        
        while not done:
            self.render()
            
            if self.epsilon.explore():
                action = np.random.randint(self.n_action)
            else :
                action = self.policy[state]
            interpreted_action = self.interpreter(action) if not self.discret_actions else action 
            
            new_state, reward, done, _ = self.env.step(interpreted_action)
            new_state = self.discretizer(new_state) if not self.discret_spaces else new_state
            
            self.active_dp_algorithm(state, interpreted_action, new_state, reward)
            
            reward_epoch += reward
            
            state = new_state
            
        return reward_epoch
        
    def _train(self, n_epochs):
        self.epsilon = Epsilon(self.e, self.e_seuil, self.e_prct, n_epochs)
        all_rewards = []
        reward_n_ep = []
        show = int(n_epochs // 100) if n_epochs > 100 else 1
        for epoch in range(n_epochs):
            reward = self.train_one_epoch()
            all_rewards.append(reward)
            reward_n_ep.append(reward)
            if epoch % show == 0:
                self.plot()
                print(f"{epoch}/{n_epochs} |{(self.epsilon.e*100):.2f} %| (Max : {np.max(reward_n_ep)} | Moyenne  : {np.mean(reward_n_ep)} ) | Moyenne totale: {np.mean(all_rewards)}")
                reward_n_ep = []
            self.epsilon.update()
            
    def test_one(self):
        done = False
        state = self.discretizer(self.env.reset()) if not self.discret_spaces else self.env.reset()
        reward_epoch = 0
        
        while not done:
            self.render()
            self.plot(state)
            action = self.policy[state]
            interpreted_action = self.interpreter(action) if not self.discret_actions else action 
            
            new_state, reward, done, _ = self.env.step(interpreted_action)
            new_state = self.discretizer(new_state) if not self.discret_spaces else new_state
        
            reward_epoch += reward
            
            state = new_state
            
        return reward_epoch
    
    def load_model(self, path):
        self.policy = np.load(path)
    
    def save_model(self, path):
        np.save(path, self.policy)
        print("Policy table saved !")
    
    def active_dp_algorithm(self, state, action, new_state, reward):
        if not new_state in self.states_seen: # si nous sommes jamais passé par cet état
            self.states_seen.append(new_state)
            self.v_fct[new_state] = reward
            self.r_fct[new_state] = reward
        
        self.freq_s_a[state][action] += 1
        self.freq_out_s_a[new_state][state][action] += 1
        
        for s_prime in range(len(self.freq_out_s_a)):
            if self.freq_out_s_a[s_prime][state][action] != 0:
                self.model[s_prime][state][action] = self.freq_out_s_a[s_prime][state][action] / self.freq_s_a[state][action]
        
        self.value_iteration()
        self.optimal_policy(new_state)
        
    def value_iteration(self, theta = 0.01):
        tol = np.asarray([theta]*len(self.v_fct))
        v_fct = np.copy(self.v_fct)
        new_v_fct = np.zeros(np.shape(self.v_fct))
        while True:
            for state in range(len(self.v_fct)):
                # prob = np.zeros(self.n_action)
                # for s_prime in range(len(self.v_fct)):
                #     prob += self.model[s_prime][state][:]*v_fct[s_prime]
                prob = np.sum(np.multiply(self.model[:, state, :], v_fct.reshape(-1,1)), axis=0)

                new_v_fct[state] = self.r_fct[state] + self.dis * np.max(prob)
            if np.all(np.abs(v_fct - new_v_fct) <= tol):          
                break
            v_fct = np.copy(new_v_fct)
        self.v_fct = np.copy(v_fct)

    def optimal_policy(self, s):
        self.policy[s] = np.argmax(np.sum(self.model[:, s, :] * self.v_fct.reshape(-1,1), axis = 0))

    def plot(self, state=None):
        fig = plt.figure(1, clear=True)
        fig.add_subplot(1, 1, 1)
        plt.imshow(self.v_fct.reshape((8, 8)), cmap='hot')
        tab = self.policy.reshape((8,8))
        text = ["<-", "v", "->", "^"]
        for i in range(len(tab)):
            for j in range(len(tab[0])):
                c = text[tab[j][i]]
                plt.text(i, j, str(c), color="green", va='center', ha='center')
        if state:
            plt.text(state%8, state//8, str("O"), color="green", weight="bold", va="center", ha="center")
        plt.pause(0.001)
        