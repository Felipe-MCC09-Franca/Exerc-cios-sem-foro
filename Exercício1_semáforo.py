import multiprocessing as mp
import time
import random

x = None
sem = None

def init(val, s):
    global x
    global sem
    x = val
    sem = s

def carro(id, sen):
    global x
    global sem
        
    with sem:
        x.value = sen

        print(f"Carro {id} está passando no sentido: {x.value}")
        time.sleep(0.5)
        
        print(f"Carro {id} saiu do cruzamento.\n")

def main():
    sentido: str = ["Norte", "Sul", "Leste", "Oeste"]
    
    random.shuffle(sentido)

    vetor = [(i + 1, sentido[i]) for i in range(4)]

    with mp.Manager() as manager:
        semaforo = manager.Semaphore(1)
        valor = manager.Value(str, "") 

        with mp.Pool(processes = 4, initializer = init, initargs = (valor, semaforo)) as pool:
            pool.starmap(carro, vetor)

if __name__ == "__main__":
    main()