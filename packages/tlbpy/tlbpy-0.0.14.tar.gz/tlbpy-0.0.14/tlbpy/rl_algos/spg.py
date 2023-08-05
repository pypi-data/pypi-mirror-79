from torch import nn
import torch
from torch.optim.adam import Adam
from torch.distributions.categorical import Categorical
import numpy as np
from tlbpy.rl_algos.rl_algo import Rl_algo

__all__ = ['SimplestPolicyGradient']

class SimplestPolicyGradient(Rl_algo):
    
    def __init__(self, env, hidden_layers, discret_actions=True, discret_spaces=True,
                 activation=nn.Tanh,
                 out_activation=nn.Identity,
                 lr = 0.01,
                 dis = 0.98,
                 batchsize = 5000):
        
        super(SimplestPolicyGradient).__init__(env, discret_actions, discret_spaces, dis, lr)
        self.hidden_layers = hidden_layers
        self.model = self._mlp(self.obs_dim, self.hidden_layers, self.act_dim, activation, out_activation)
        self.optimizer = Adam(self.model.parameters(), lr=lr)
        self.batchsize = batchsize
        
    def _mlp(self, inputs, hidden_layers, outputs, activation=nn.Tanh, out_activation=nn.Identity):
        sizes = [inputs]+hidden_layers+[outputs]
        layers = []
        for j in range(len(sizes)-1):
            layers += [nn.Linear(sizes[j], sizes[j+1]), activation() if j < len(sizes)-2 else out_activation()]
        return nn.Sequential(*layers)
    
    def _policy(self, obs):
        output = self.model(obs)
        return Categorical(logits=output)
    
    def action(self, obs):
        return self._policy(obs).sample().item()

    def loss(self, obs, act, weights):
        logp = self._policy(obs).log_prob(act)
        return (-(logp * weights)).mean()
    
    def render(self, aff=False):
        if aff:
            self.env.render()
    
    def train_one_epoch(self):
        obs = self.env.reset()
        
        batch_obs = []
        batch_act = []
        batch_weights = []
        ep_rewards = []
        batch_returns = []
        batch_lengths = []
            
        # Forward
        while True:
            
            # Rendu 
            self.render()
            
            # Choisir l'action
            action = self.action(torch.as_tensor(obs, dtype=torch.float32))
            
            # Recevoir la nouvelle observation et le résultat
            new_obs, reward, done, _ = self.env.step(action)
            
            # Remplir les batch
            batch_obs.append(obs.copy())
            batch_act.append(action)
            ep_rewards.append(reward)
            obs = new_obs
            
            # end episode
            if done:
                ret = sum(ep_rewards)
                length = len(ep_rewards)
                
                batch_returns.append(ret)
                batch_lengths.append(length)
                batch_weights += [ret] * length
                
                # reset
                obs = self.env.reset()
                done = False
                ep_rewards = []
                
                if len(batch_obs) > self.batchsize:
                    break
          
        # Backward
        self.optimizer.zero_grad()
        loss = self.loss(   torch.as_tensor(batch_obs, dtype=torch.float32),
                            torch.as_tensor(batch_act, dtype=torch.float32),
                            torch.as_tensor(batch_weights, dtype=torch.float32))
        loss.backward()
        self.optimizer.step()
        
        return loss, batch_returns, batch_lengths
    
    def _train(self, n_epochs):
        ok = 0
        for i in range(n_epochs):
            loss, ret, lens = self.train_one_epoch()
            print(f"{i}/{n_epochs} | Loss:{loss}, returns:{np.mean(ret)}, lengths:{np.mean(lens)}")
            if np.mean(ret) == 500.0:
                ok += 1
            else:
                ok = 0
            if ok == 5:
                break
            
    def test_one(self):
        done = False
        obs = self.env.reset()
        while not done:
            self.env.render()
            action = self.action(torch.as_tensor(obs, dtype=torch.float32))
            # Recevoir la nouvelle observation et le résultat
            obs, reward, done, _ = self.env.step(action)
            
    def load_model(self, file_path):
        self.model.load_state_dict(torch.load(file_path))
        
    def save_model(self, file_path):
        torch.save(self.model.state_dict(), file_path)
        print("Modele sauvegardé :", file_path)