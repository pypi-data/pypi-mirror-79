from math import e
import numpy as np
import random

__all__ = ['Epsilon', 'Discretizer', 'Interpreter', 'value_iteration', 'active_dp_algorithm', 'optimal_policy']

class Epsilon:
    def __init__(self, e, seuil, prct, n_epochs):
        self.e = e
        self.seuil = seuil
        self.pas = self.e / (int(n_epochs*prct) - 1)
    
    def explore(self):
        return random.random() <= self.e
    
    def exploit(self):
        return random.random() > self.e
    
    def update(self):
        self.e -= self.pas if self.e - self.pas >= self.seuil else 0
    
class Discretizer:
    def __init__(self, n, low, high):
        self.step = (high - low) / n
        self.low = low
        self.high = high

    def __call__(self, x):
        new_x = (x - self.low) / self.step
        return tuple(new_x.astype(int))
    
class Interpreter:
    def __init__(self, n, low, high):
        self.high = high 
        self.low = low
        self.n = n
        
    def __call__(self, x):
        return (( x / self.n ) * (self.high - self.low)) + self.low

