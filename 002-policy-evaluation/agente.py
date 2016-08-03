#!/ usr/bin/python -tt
# -*- coding: utf-8 -*-
# Ronny Conde at Monkey from the Future
from __future__ import print_function
import laberinto as lab

def posibles_estados():
    """
    Devuelve una lista con todos los posibles estados.
    E.g. posibles_estados() devolvera [(0, 0), (0, 1), ... ]
    """
    filas = 3
    columnas = 4
    muros = [(1,1)]
    estados = []
    for i in xrange(filas):
        for j in xrange(columnas):
            if (i, j) not in muros:
                estados.append((i, j))
    return estados

def actualizar_valor_estado(estado, politica, valores_estados, gamma):
    """ Devuelve el valor del estado tras aplicar un paso de Policy Evaluation.
    Se utilizara politica para saber la accion a seleccionar y valores_estados
    para saber el valor de los estados destino. El parametro gamma es el factor
    de descuento.
    E.g. actualizar_valor_estado((0, 0), politica, valores_estados, 0.9) puede
    devolver 0.06574
    """
    accion = politica[estado]
    accum = 0
    for nuevo_estado, probabilidad in lab.posibles_transiciones(estado, accion):
        if nuevo_estado is not None:
            accum += probabilidad * (lab.recompensa(estado, accion) + \
                                     gamma * valores_estados[nuevo_estado])
        else:
            accum += probabilidad * lab.recompensa(estado, accion)
    return accum


def paso(politica, valores_estados, gamma):
    """ Devuelve la version actualizada de valores_estados tras ejecutar un paso
    de Policy Evaluation. El parametro gamma es el factor de descuento.
    """
    nuevos_estados = {}
    for estado in valores_estados:
        nuevos_estados[estado] = actualizar_valor_estado(estado, politica, \
                                                         valores_estados, gamma)
    return nuevos_estados


def main():
    gamma = 0.9
    N = 100

    #print(posibles_estados())

    # Definimos politica. politica es el diccionario que va a almacenar la
    # politica a evaluar. Cada clave sera un posible estado y su valor la accion
    # a seleccionar. La politica a evaluar sera 'N' en todos los estados salvo
    # en los terminales, que sera 'EXIT'.
    # E.g. politica = {(0, 1): 'N', (1, 2): 'N', (0, 0): 'N', (2, 1): 'N', (2,
    # 0): 'N', (1, 3): 'EXIT', (2, 3): 'N', (2, 2): 'N', (1, 0): 'N', (0, 3):
    # 'EXIT', (0, 2): 'N'}
    politica = {estado : "N" for estado in posibles_estados()}
    estados_finales = [(0, 3), (1, 3)]
    for estado in estados_finales:
        politica[estado] = "EXIT"
    #print("Politica: \n{}".format(politica))

    # Inicializamos valores_estados. valores_estados es un diccionario que
    # almacena cada posible estado, como clave, asociado a su valor. Al estar
    # evaluando una politica, el valor de un estado se define como la suma de
    # las recompensas esperadas desde ese estado hasta el final del episodio si
    # el agente sigue la política a evaluar y teniendo en cuenta el factor de
    # descuento gamma.
    # E.g. valores_estados se inicializara como {(0, 0): 0.0, (0, 1): 0.0, ... }
    valores_estados = {estado : 0.0 for estado in posibles_estados()}
    #print("Valores estados: \n{}".format(valores_estados))

    # Bucle para ejecutar la funcion paso N veces E.g. Tras ejecutar 100 pasos
    # el resultado tiene que ser:
    # {(0, 1): 0.1387855814730856, (1, 2): 0.1907114099448302, (0, 0):
    # 0.06574007226947705, (2, 1): 0.038463394803138554, (2, 0):
    # 0.049474822146981734, (1, 3): -1.0, (2, 3): -0.7842669416236797, (2, 2):
    # 0.07018985904904827, (1, 0): 0.05772287949195069, (0, 3): 1.0, (0, 2):
    # 0.3660380817898193}
    for _ in xrange(N):
        valores_estados = paso(politica, valores_estados, gamma)
    print(valores_estados)
    #print("Politica: \n{}".format(politica))

if __name__ == "__main__":
    main()
