import multiprocessing as mp
import time
import random

x = None
sem = None

def init(v, s):
    global x
    global sem
    x = v
    sem = s

def cs(id, pulo):
    global x
    global sem
    d: int = 100
    soma: int = 0

    while True:
        time.sleep(0.2)
        
        with sem:
            p = random.randint(0, pulo)
            soma += p
            
            print(f"O {id}º sapo percorreu {p} centímetros e já percorreu {soma} centímetros")
            
            if soma >= d:
                x.value += 1
                print(f"O {id}º sapo terminou a corrida em {x.value}º lugar")
                time.sleep(0.5)
                break

def main():
    vetor = [(0, 0)] * 5

    for i in range(0, 5, 1):
        vetor[i] = (i, 5)

    with mp.Manager() as manager:
        semaforo = manager.Semaphore(1)
        valor = manager.Value(int, 0)

        with mp.Pool(processes = 5, initializer = init, initargs = (valor, semaforo)) as pool:
            pool.starmap(cs, vetor)

if __name__ == "__main__":
    main()