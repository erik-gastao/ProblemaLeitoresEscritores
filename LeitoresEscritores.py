import threading
import time
import random

# Recurso compartilhado (ex: banco de dados)
dados = 0

# Controle de concorrência
mutex = threading.Semaphore(1)   # protege o contador de leitores
wrt = threading.Semaphore(1)     # garante exclusividade de escrita
leitores = 0                     # contador de leitores ativos

def leitor(id):
    global leitores
    while True:
        time.sleep(random.uniform(1, 3))

        mutex.acquire()
        leitores += 1
        if leitores == 1:
            wrt.acquire()  # primeiro leitor bloqueia escritores
        mutex.release()

        # leitura
        print(f"📘 Leitor {id} está lendo o valor: {dados}")
        time.sleep(random.uniform(1, 2))

        mutex.acquire()
        leitores -= 1
        if leitores == 0:
            wrt.release()  # último leitor libera escritores
        mutex.release()

def escritor(id):
    global dados
    while True:
        time.sleep(random.uniform(2, 5))
        wrt.acquire()

        # escrita
        dados += 1
        print(f"✍️ Escritor {id} escreveu o valor: {dados}")
        time.sleep(random.uniform(1, 2))

        wrt.release()

# Criando threads
threads = []
for i in range(3):  # 3 leitores
    t = threading.Thread(target=leitor, args=(i,))
    threads.append(t)
    t.start()

for i in range(2):  # 2 escritores
    t = threading.Thread(target=escritor, args=(i,))
    threads.append(t)
    t.start()