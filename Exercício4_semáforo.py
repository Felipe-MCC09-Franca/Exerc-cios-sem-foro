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

def treinar(id, nome):
    global x
    global sem
    

    sem_p = sem[0]
    sem_e = sem[1]
    
    with sem_e[nome]:
        with sem_p:
            
            print(f"Carro {id} da equipe {nome} entrou na pista.")
            
            for volta in range(1, 4):
                tempo_volta = random.uniform(1.0, 2.0)
                time.sleep(tempo_volta)
                print(f"Carro {id} ({nome}) concluiu a {volta}ª volta. Tempo: {tempo_volta}s")
                
            print(f"Carro {id} da equipe {nome} saiu da pista e concluiu o treino.\n")

def main():
    equipes = ["Ferrari", "McLaren", "RedBull", "Mercedes", "AstonMartin", "Alpine", "Williams"]
    vetor = [(0, 0)] * 14
    id = 1

    for equipe in equipes:
        vetor[id - 1] = (id, equipe)
        id += 1
        vetor[id - 1] = (id, equipe)
        id += 1

    random.shuffle(vetor)

    with mp.Manager() as manager:
        semaforo = manager.Semaphore(5)
        
        semaforo_e = {equipe: manager.Semaphore(1) for equipe in equipes}
        
        controles = (semaforo, semaforo_e)
        
        valor = manager.Value(int, 0)

        with mp.Pool(processes = 14, initializer = init, initargs = (valor, controles)) as pool:
            pool.starmap(treinar, vetor)

if __name__ == "__main__":
    main()