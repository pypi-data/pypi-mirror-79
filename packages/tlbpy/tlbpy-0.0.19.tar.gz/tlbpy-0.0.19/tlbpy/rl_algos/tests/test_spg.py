import gym
from ..spg import SimplestPolicyGradient

ENV_NAME = "CartPole-v1"
            
def test(args):
    n_epoch = int(args[0])
    env = gym.make(ENV_NAME)
    
    spg = SimplestPolicyGradient(env, [32], discret_spaces=False)

    spg.train(n_epoch, "model.pt")
    spg.load_model("model.pt")
    for i in range(5):
        spg.test_one()
    
    env.close()
