import gym
from ..pda import Dynamic_Programming

ENV_NAME = "FrozenLake8x8-v0"
            
def test(args):
    n_epoch = int(args[0])
    env = gym.make(ENV_NAME)
    
    dp = Dynamic_Programming(env, discret_actions=True, discret_spaces=True)

    # dp.train(n_epoch, "policy_table")
    
    dp.load_model("policy_table.npy")
    
    for i in range(5):
        reward = dp.test_one()
        print(f'Reward : {reward}')
    env.close()
