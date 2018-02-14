import sys
import gym
import universe


def run_agent(vnc_port, info_channel):
    game = 'flashgames.DuskDrive-v0'
    remote = 'vnc://localhost:' + str(vnc_port) + '+' + str(info_channel)
    env = gym.make(game)
    env.configure(remotes=remote)  # automatically creates a local docker container
    observation_n = env.reset()
    while True:
        action_n = [[('KeyEvent', 'ArrowUp', True)] for ob in observation_n]  # your agent here
        observation_n, reward_n, done_n, info = env.step(action_n)
        env.render()

if __name__ == '__main__':
    vnc_port = sys.argv[1]
    info_channel = sys.argv[2]
    run_agent(vnc_port, info_channel)
