#!/ usr/bin/python -tt
# -*- coding: utf-8 -*-
# Ronny Conde at Monkey from the Future
import entorno
from random import randint


def valor_estado(estado, valores_q):
    """ Calculara y devolvera el valor asociado a estado teniendo en cuenta
    valores_q.
    """
    max = -10000000
    for accion in entorno.acciones_disponibles(estado):
        if valores_q[(estado, accion)] > max:
            max = valores_q[(estado, accion)]
    return max


def imprimir_valores_estados(estados, valores_q):
    """ imprime por pantalla los valores asociados a cada estado."""
    for estado in estados:
        print("{} : {}".format(estado, valor_estado(estado, valores_q)))


def qlearning():
    gamma = 0.9
    alpha = 0.01
    N = 20000  # Numero de episodios

    # Inicializamos estados como una lista que almacena cada posible posicion
    # del agente en el laberinto. Hay que tener en cuenta que (1, 1) no estara
    # en la lista al ser un obstaculo.
    # E.g. estados se inicializara como [(0, 0), (0, 1), ... ]
    filas = 3
    columnas = 4
    muros = [(1, 1)]
    estados = []
    for fil in xrange(filas):
        for col in xrange(columnas):
            if (fil, col) not in muros:
                estados.append((fil, col))

    # valores_q sera un diccionario:
    #   - Claves. Tuplas con la combinacion de cada estado y sus
    #     acciones disponibles
    #   - Valores: Suma de las recompensas que se esperan recibir hasta el final
    #   del episodio si se actua de manera optima partiendo del estado Q (la
    #   clave asociada) y teniendo en cuenta el factor de descuento gamma.
    # Inicializaremos todos los valores a 0.0
    # E.g. valores_q se inicializara como {((0, 0), 'W'): 0.0, ((0, 0), 'N'):
    # 0.0, ... }
    valores_q = {(estado, accion): 0.0 for estado in estados
                 for accion in entorno.acciones_disponibles(estado)}

    # Actualizar valores_q entrenando el agente con qlearning durante N
    # episodios.
    # E.g. A continuacion se muestra una posible estructura
    # for episode in range(N):
    #     s = entorno.reset()
    #     for _ in range(10000): # Numero limite de pasos por episodio
    #         ...
    #         ...
    #         if done: # Fin del Episodio
    #             ...
    #             break
    #     ...
    for _ in xrange(N):
        estado = entorno.reset()
        for _ in xrange(1000):
            # seleccionar accion random
            acciones = entorno.acciones_disponibles(estado)
            accion = acciones[randint(0, len(acciones) - 1)]
            # ejecutar un paso
            nuevo_estado, recompensa, episodio_terminado = \
                entorno.paso(estado, accion)
            # comprobacion de fin de episodio
            if episodio_terminado:
                assert(nuevo_estado is None)
                valores_q[(estado, accion)] = recompensa
                estado = entorno.reset()
                break
            else:
                # valor optimo a partir del siguiente estado
                sample = recompensa + gamma * valor_estado(nuevo_estado, valores_q)
                # actualizacion del valor_q asociado a (estado, accion)
                valores_q[(estado, accion)] = valores_q[(estado, accion)] + \
                    alpha * (sample - valores_q[(estado, accion)])
                estado = nuevo_estado

    # Llamada a imprimir_valores_estados(estados, valores_q).
    imprimir_valores_estados(estados, valores_q)

if __name__ == "__main__":
    qlearning()
