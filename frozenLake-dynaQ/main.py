import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from environment import Environment
from agent_dynaQ import Agent


def train(agent, env, num_episodes=10000, steps_planning=50):
    agent.init_env(env)
    print("Starting agent training...")
    episode = 1
    steps_per_episode = []
    score=0
    BREAK = False
    T = 0
    last_T = -1
    last_written=-2
    
    for _ in range(num_episodes):
        agent.start(env)
        if episode==1 or episode%1000==0:
            print(f"\tEpisode {episode}/{num_episodes}... ")
        steps = 0
        
        while agent.last_state!=env.hash_state(*env.terminal_pos):
            action = agent.take_action(agent.last_state)
            s, r, scoreInc = gridWorld.get_next_state_and_reward(agent.last_state, action)
            T+=1
            score += scoreInc
            if T > 300:
                exit(0) #++ !!!!!
                BREAK = True
                break
            if agent.last_state!=env.hash_state(*env.terminal_pos) and T != last_written:
                print("World t="+str(T))
                print("score="+str(score)+",")
                last_written = T
            last_T = T
            agent.update_model(s, r)
            agent.update_Q(s, r)
            agent.planning_step(n_steps=steps_planning)
            steps+=1
        #T-=1 #as it takes 1 step less in the other simulation due to episode reset counting not <- has been equalized in the meanwhile
        steps_per_episode.append(steps)
        episode+=1
        if BREAK:
            break
    print("Training completed!")
    agent.define_policy()
    return steps_per_episode

def show_train_results(agent, env, steps_per_episode, labels_dict=None):
    V = agent.V*env.env
    if labels_dict is not None:
        policy = np.vectorize(labels_dict.get)(agent.policy)
    else:
        policy = agent.policy
    x, y = env.terminal_pos
    policy[x, y] = "GOAL"
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(13,5))
    ax1.set_title("Benefit of planning steps")
    ax1.set_xlabel("Episode")
    ax1.set_ylabel("Number of steps on each episode")
    ax1.plot([i+1 for i in range(len(steps_per_episode))], steps_per_episode, linewidth=1, color="navy")
    ax2.set_title("Policy learned by agent")
    sns.heatmap(gridWorld.env*V, cmap="RdYlGn", linewidths=1, annot=policy, fmt="", ax = ax2) #++ !!!!!
    #plt.show() #++ !!!!!


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Functionality that trains agent in a gridworld")
    parser.add_argument('-e', '--episodes', type=int, default=100)
    parser.add_argument('-s', '--planning_steps', type=int, default=50)
    args = parser.parse_args()

    gridWorld = Environment(width=4, height=4, 
                            start_pos=(0, 0), terminal_pos=(3, 3),
                            walls=[(1,1), (3,0), (1,3), (2,3)]
                            )
    agent = Agent()
    gridWorld.show()

    steps_per_episode = train(agent, gridWorld, num_episodes=args.episodes, steps_planning=args.planning_steps)
    show_train_results(agent,
                       gridWorld,
                       steps_per_episode,
                       labels_dict={"up": "↑", "left": "←", "right": "→", "down": "↓"})


