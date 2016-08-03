#!/ usr/bin/python -tt
# -*- coding: utf-8 -*-
# Ronny Conde at Monkey from the Future

from __future__ import print_function
import gym

def episodio():
    """ Ejecutara un episodio del entorno FrozenLake-v0 siguiendo una politica
    aleatoria y devolvera una tupla con:
        - Lista con los estados visitados
        - Lista con las recompensas recibidas

    * Nota: Come seguimos el convenio de que las recompensas se reciben al salir
    de un estado no incorporaremos a la lista el estado devuelto por el entorno
    cuando la variable done es True.

    E.g. episodio() puede devolver ([0, 0, 0, 0, 4, 4], [0.0, 0.0, 0.0, 0.0,
    0.0, 0.0])
    """
    import gym
    env = gym.make('FrozenLake-v0')
    initial_state = env.reset()
    states = [initial_state]
    rewards = []
    for _ in range(1000):
        random_action = env.action_space.sample()
        state, reward, done, _ = env.step(random_action)
        if done:
            break
        states.append(state)
        rewards.append(reward)
    return (states, rewards)


if __name__ == '__main__':
    print(episodio())
