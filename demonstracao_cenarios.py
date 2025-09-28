"""
Demonstração de diferentes cenários do problema Leitores-Escritores
Este arquivo mostra como executar testes específicos e cenários de demonstração
"""
import threading
import time
import random
from datetime import datetime

class LeitoresEscritoresDemostracao:
    def __init__(self):
        self.dados = 0
        self.mutex = threading.Semaphore(1)
        self.wrt = threading.Semaphore(1)
        self.leitores_ativos = 0
        self.log_eventos = []
        self.log_lock = threading.Lock()
        self.executando = True
        
    def log_evento(self, evento):
        """Registra evento com timestamp"""
        with self.log_lock:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            thread_name = threading.current_thread().name
            self.log_eventos.append({
                'timestamp': timestamp,
                'evento': evento,
                'thread': thread_name,
                'dados': self.dados,
                'leitores_ativos': self.leitores_ativos
            })
            print(f"[{timestamp}] [{thread_name}] {evento} (Dados: {self.dados}, Leitores: {self.leitores_ativos})")
    
    def reset(self):
        """Reset para novo teste"""
        self.dados = 0
        self.leitores_ativos = 0
        self.log_eventos = []
        self.mutex = threading.Semaphore(1)
        self.wrt = threading.Semaphore(1)
        self.executando = True
    
    def parar(self):
        """Para a execução"""
        self.executando = False
    
    def leitor(self, id, operacoes=None, delay_min=0.5, delay_max=2.0):
        """Leitor configurável"""
        contador = 0
        while self.executando and (operacoes is None or contador < operacoes):
            time.sleep(random.uniform(delay_min, delay_max))
            
            self.mutex.acquire()
            self.leitores_ativos += 1
            if self.leitores_ativos == 1:
                self.wrt.acquire()  # Primeiro leitor bloqueia escritores
                self.log_evento(f"📘 Leitor {id} BLOQUEIA escritores (primeiro leitor)")
            else:
                self.log_evento(f"📘 Leitor {id} se junta à leitura")
            self.mutex.release()
            
            # Leitura
            valor = self.dados
            self.log_evento(f"📖 Leitor {id} LENDO valor: {valor}")
            time.sleep(random.uniform(0.3, 1.0))  # Tempo de leitura
            self.log_evento(f"📗 Leitor {id} TERMINOU leitura")
            
            self.mutex.acquire()
            self.leitores_ativos -= 1
            if self.leitores_ativos == 0:
                self.wrt.release()  # Último leitor libera escritores
                self.log_evento(f"📘 Leitor {id} LIBERA escritores (último leitor)")
            else:
                self.log_evento(f"📘 Leitor {id} sai da leitura")
            self.mutex.release()
            
            contador += 1
    
    def escritor(self, id, operacoes=None, delay_min=1.0, delay_max=3.0):
        """Escritor configurável"""
        contador = 0
        while self.executando and (operacoes is None or contador < operacoes):
            time.sleep(random.uniform(delay_min, delay_max))
            
            self.log_evento(f"✍️ Escritor {id} AGUARDANDO acesso exclusivo...")
            self.wrt.acquire()
            self.log_evento(f"✅ Escritor {id} OBTEVE acesso exclusivo")
            
            # Escrita
            valor_antigo = self.dados
            time.sleep(random.uniform(0.3, 1.0))  # Tempo de escrita
            self.dados += 1
            self.log_evento(f"✍️ Escritor {id} ESCREVEU: {valor_antigo} → {self.dados}")
            
            self.wrt.release()
            self.log_evento(f"✅ Escritor {id} LIBEROU acesso exclusivo")
            
            contador += 1

def cenario_1_leitores_simultaneos():
    """Cenário 1: Múltiplos leitores simultâneos"""
    print("\n" + "="*60)
    print("CENÁRIO 1: MÚLTIPLOS LEITORES SIMULTÂNEOS")
    print("="*60)
    print("Demonstra que múltiplos leitores podem ler simultaneamente")
    
    demo = LeitoresEscritoresDemostracao()
    threads = []
    
    # Criar 4 leitores
    for i in range(4):
        t = threading.Thread(target=demo.leitor, args=(i, 2), name=f"Leitor-{i}")
        threads.append(t)
        t.start()
    
    # Aguardar conclusão
    time.sleep(8)
    demo.parar()
    for t in threads:
        t.join()
    
    print(f"\nResultado: {len([e for e in demo.log_eventos if 'LENDO' in e['evento']])} leituras realizadas")

def cenario_2_exclusao_mutua_escritores():
    """Cenário 2: Exclusão mútua entre escritores"""
    print("\n" + "="*60)
    print("CENÁRIO 2: EXCLUSÃO MÚTUA ENTRE ESCRITORES")
    print("="*60)
    print("Demonstra que escritores não podem escrever simultaneamente")
    
    demo = LeitoresEscritoresDemostracao()
    threads = []
    
    # Criar 3 escritores
    for i in range(3):
        t = threading.Thread(target=demo.escritor, args=(i, 2), name=f"Escritor-{i}")
        threads.append(t)
        t.start()
    
    # Aguardar conclusão
    time.sleep(10)
    demo.parar()
    for t in threads:
        t.join()
    
    print(f"\nResultado final: dados = {demo.dados}")

def cenario_3_leitores_vs_escritores():
    """Cenário 3: Interação entre leitores e escritores"""
    print("\n" + "="*60)
    print("CENÁRIO 3: INTERAÇÃO LEITORES VS ESCRITORES")
    print("="*60)
    print("Demonstra como leitores e escritores se coordenam")
    
    demo = LeitoresEscritoresDemostracao()
    threads = []
    
    # Criar 2 leitores e 2 escritores
    for i in range(2):
        t_leitor = threading.Thread(target=demo.leitor, args=(i, 3), name=f"Leitor-{i}")
        t_escritor = threading.Thread(target=demo.escritor, args=(i, 2), name=f"Escritor-{i}")
        threads.extend([t_leitor, t_escritor])
        t_leitor.start()
        t_escritor.start()
    
    # Aguardar conclusão
    time.sleep(12)
    demo.parar()
    for t in threads:
        t.join()
    
    print(f"\nResultado final: dados = {demo.dados}")

def cenario_4_starvation_test():
    """Cenário 4: Teste de starvation (inanição)"""
    print("\n" + "="*60)
    print("CENÁRIO 4: TESTE DE STARVATION")
    print("="*60)
    print("Demonstra possível inanição de escritores com muitos leitores")
    
    demo = LeitoresEscritoresDemostracao()
    threads = []
    
    # Muitos leitores (podem causar starvation do escritor)
    for i in range(5):
        t = threading.Thread(target=demo.leitor, args=(i, None, 0.1, 0.3), name=f"Leitor-{i}")
        threads.append(t)
        t.start()
    
    # Um escritor
    t_escritor = threading.Thread(target=demo.escritor, args=(0, 3, 0.5, 1.0), name="Escritor-0")
    threads.append(t_escritor)
    t_escritor.start()
    
    # Executar por tempo limitado
    time.sleep(8)
    demo.parar()
    for t in threads:
        t.join()
    
    escritas = len([e for e in demo.log_eventos if 'ESCREVEU' in e['evento']])
    leituras = len([e for e in demo.log_eventos if 'LENDO' in e['evento']])
    
    print(f"\nEstatísticas:")
    print(f"- Escritas realizadas: {escritas}")
    print(f"- Leituras realizadas: {leituras}")
    print(f"- Dados final: {demo.dados}")
    
    if escritas < 2:
        print("⚠️  POSSÍVEL STARVATION DETECTADA: Escritor teve poucas oportunidades")
    else:
        print("✅ Sem starvation detectada")

def analise_temporizada():
    """Análise com controle temporal preciso"""
    print("\n" + "="*60)
    print("ANÁLISE TEMPORIZADA")
    print("="*60)
    print("Análise detalhada dos tempos de espera e execução")
    
    demo = LeitoresEscritoresDemostracao()
    
    # Cenário controlado
    def teste_temporizado():
        # Escritor longo
        def escritor_longo():
            demo.log_evento("🔒 Escritor iniciando operação LONGA")
            demo.wrt.acquire()
            demo.log_evento("✍️ Escritor obteve lock - INÍCIO escrita longa")
            time.sleep(2)  # Escrita muito longa
            demo.dados += 100
            demo.log_evento("✍️ Escritor TERMINOU escrita longa")
            demo.wrt.release()
            demo.log_evento("🔓 Escritor liberou lock")
        
        # Leitores esperando
        def leitor_esperando(id):
            time.sleep(0.5)  # Garantir que escritor começou primeiro
            demo.log_evento(f"📚 Leitor {id} TENTANDO ler (deve esperar)")
            demo.leitor(id, 1)
        
        # Iniciar escritor longo
        t_escritor = threading.Thread(target=escritor_longo, name="Escritor-Longo")
        t_escritor.start()
        
        # Iniciar leitores que vão esperar
        threads_leitores = []
        for i in range(3):
            t = threading.Thread(target=leitor_esperando, args=(i,), name=f"Leitor-Esperando-{i}")
            threads_leitores.append(t)
            t.start()
        
        # Aguardar conclusão
        t_escritor.join()
        for t in threads_leitores:
            t.join()
    
    teste_temporizado()
    
    # Analisar tempos
    eventos_escritor = [e for e in demo.log_eventos if 'Escritor' in e['thread']]
    eventos_leitores = [e for e in demo.log_eventos if 'Leitor' in e['thread']]
    
    print(f"\nAnálise temporal:")
    print(f"- Eventos do escritor: {len(eventos_escritor)}")
    print(f"- Eventos dos leitores: {len(eventos_leitores)}")
    print(f"- Valor final: {demo.dados}")

def menu_interativo():
    """Menu interativo para escolher cenários"""
    while True:
        print("\n" + "="*60)
        print("DEMONSTRAÇÃO - PROBLEMA DOS LEITORES-ESCRITORES")
        print("="*60)
        print("Escolha um cenário para executar:")
        print("1. Múltiplos leitores simultâneos")
        print("2. Exclusão mútua entre escritores")
        print("3. Interação leitores vs escritores")
        print("4. Teste de starvation")
        print("5. Análise temporizada")
        print("6. Executar todos os cenários")
        print("0. Sair")
        
        try:
            escolha = input("\nDigite sua escolha (0-6): ").strip()
            
            if escolha == '0':
                print("Encerrando demonstração...")
                break
            elif escolha == '1':
                cenario_1_leitores_simultaneos()
            elif escolha == '2':
                cenario_2_exclusao_mutua_escritores()
            elif escolha == '3':
                cenario_3_leitores_vs_escritores()
            elif escolha == '4':
                cenario_4_starvation_test()
            elif escolha == '5':
                analise_temporizada()
            elif escolha == '6':
                cenario_1_leitores_simultaneos()
                cenario_2_exclusao_mutua_escritores()
                cenario_3_leitores_vs_escritores()
                cenario_4_starvation_test()
                analise_temporizada()
            else:
                print("Escolha inválida! Tente novamente.")
                continue
                
            input("\nPressione ENTER para continuar...")
            
        except KeyboardInterrupt:
            print("\n\nInterrompido pelo usuário. Encerrando...")
            break
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    menu_interativo()