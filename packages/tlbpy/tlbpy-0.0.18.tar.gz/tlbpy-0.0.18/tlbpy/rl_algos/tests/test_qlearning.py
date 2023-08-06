import gym
from ..qlearning import Q_learning

ENV_NAME = "Pendulum-v0"
            
def test(args):
    n_epoch = int(args[0])
    env = gym.make(ENV_NAME)
    
    qlearner = Q_learning(env, discret_actions=False, discret_spaces=False, n_actions=6, n_spaces=12)

    qlearner.train(n_epoch, "q_table")
    
    qlearner.load_model("q_table.npy")
    
    for i in range(5):
        reward = qlearner.test_one()
        print(f'Reward : {reward}')
    env.close()
