
__all__ = ['Discretizer', 'Interpreter']

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
