import multiprocessing as mp
import time
import random

x: int = 0
sem = None

def init(v, s):
    global x
    global sem
    x = v
    sem = s

def caminhar(id, v):
    global sem
    global x
    c: int = 200
    soma = 0

    while True:
        time.sleep(0.1)
        print(f"A {id}ª pessoa andou {v} metros")
        soma+= v
        with sem:
            if soma > c:
                time.sleep(1)
                print(f"A {id}ª pessoa cruzou a porta")
                time.sleep(1)
                break


def main():
    vetor: int = [(0, 0)] * 4
    valor: int = 0

    for i in range(0, 4, 1):
        velocidade = random.randint(4, 6)
        vetor[i] = (i, velocidade)

    with mp.Manager() as manager:
        semaforo = manager.Semaphore(1)
        valor = manager.Value(int, 0)

        with mp.Pool(processes = 4, initializer = init, initargs = (valor, semaforo)) as pool:
            pool.starmap(caminhar, vetor)

if __name__ == "__main__":
    main()