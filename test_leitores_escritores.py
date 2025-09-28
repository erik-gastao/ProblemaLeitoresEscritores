import unittest
import threading
import time
from unittest.mock import patch, MagicMock
import sys
import os

# Adicionar o diretório atual ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class LeitoresEscritoresTest:
    """Classe para testes do problema Leitores-Escritores"""
    
    def __init__(self):
        self.dados = 0
        self.mutex = threading.Semaphore(1)
        self.wrt = threading.Semaphore(1)
        self.leitores_ativos = 0
        self.log = []
        self.log_lock = threading.Lock()
        
    def reset(self):
        """Resetar estado para novo teste"""
        self.dados = 0
        self.leitores_ativos = 0
        self.log = []
        self.mutex = threading.Semaphore(1)
        self.wrt = threading.Semaphore(1)
        
    def log_evento(self, evento):
        """Log thread-safe de eventos"""
        with self.log_lock:
            self.log.append({
                'timestamp': time.time(),
                'evento': evento,
                'thread_id': threading.current_thread().ident,
                'dados': self.dados,
                'leitores_ativos': self.leitores_ativos
            })
    
    def leitor(self, id, num_operacoes=1):
        """Leitor para testes"""
        for _ in range(num_operacoes):
            self.mutex.acquire()
            self.leitores_ativos += 1
            if self.leitores_ativos == 1:
                self.wrt.acquire()
            self.mutex.release()
            
            # Leitura
            valor = self.dados
            self.log_evento(f"LEITURA_INICIO_L{id}")
            time.sleep(0.1)  # Simular tempo de leitura
            self.log_evento(f"LEITURA_FIM_L{id}_VALOR_{valor}")
            
            self.mutex.acquire()
            self.leitores_ativos -= 1
            if self.leitores_ativos == 0:
                self.wrt.release()
            self.mutex.release()
            
            time.sleep(0.05)  # Pequena pausa entre operações
    
    def escritor(self, id, num_operacoes=1):
        """Escritor para testes"""
        for _ in range(num_operacoes):
            self.wrt.acquire()
            
            # Escrita
            self.log_evento(f"ESCRITA_INICIO_E{id}")
            old_value = self.dados
            time.sleep(0.1)  # Simular tempo de escrita
            self.dados += 1
            self.log_evento(f"ESCRITA_FIM_E{id}_DE_{old_value}_PARA_{self.dados}")
            
            self.wrt.release()
            
            time.sleep(0.05)  # Pequena pausa entre operações

class TestLeitoresEscritores(unittest.TestCase):
    """Testes unitários para o problema dos Leitores-Escritores"""
    
    def setUp(self):
        self.sistema = LeitoresEscritoresTest()
    
    def test_leitura_simples(self):
        """Teste básico de leitura"""
        self.sistema.reset()
        
        # Um leitor faz uma leitura
        thread = threading.Thread(target=self.sistema.leitor, args=(1, 1))
        thread.start()
        thread.join()
        
        # Verificar log
        eventos = [e['evento'] for e in self.sistema.log]
        self.assertIn('LEITURA_INICIO_L1', eventos)
        self.assertIn('LEITURA_FIM_L1_VALOR_0', eventos)
        
    def test_escrita_simples(self):
        """Teste básico de escrita"""
        self.sistema.reset()
        
        # Um escritor faz uma escrita
        thread = threading.Thread(target=self.sistema.escritor, args=(1, 1))
        thread.start()
        thread.join()
        
        # Verificar resultado
        self.assertEqual(self.sistema.dados, 1)
        
        # Verificar log
        eventos = [e['evento'] for e in self.sistema.log]
        self.assertIn('ESCRITA_INICIO_E1', eventos)
        self.assertIn('ESCRITA_FIM_E1_DE_0_PARA_1', eventos)
    
    def test_multiplos_leitores_simultaneos(self):
        """Teste de múltiplos leitores simultâneos"""
        self.sistema.reset()
        
        # Criar múltiplos leitores
        threads = []
        for i in range(3):
            t = threading.Thread(target=self.sistema.leitor, args=(i, 1))
            threads.append(t)
            t.start()
        
        # Aguardar conclusão
        for t in threads:
            t.join()
        
        # Verificar que todos leram
        eventos = [e['evento'] for e in self.sistema.log]
        for i in range(3):
            self.assertIn(f'LEITURA_INICIO_L{i}', eventos)
            self.assertIn(f'LEITURA_FIM_L{i}_VALOR_0', eventos)
    
    def test_exclusao_mutua_escritores(self):
        """Teste de exclusão mútua entre escritores"""
        self.sistema.reset()
        
        # Criar múltiplos escritores
        threads = []
        for i in range(3):
            t = threading.Thread(target=self.sistema.escritor, args=(i, 1))
            threads.append(t)
            t.start()
        
        # Aguardar conclusão
        for t in threads:
            t.join()
        
        # Verificar que o valor final está correto (3 escritas)
        self.assertEqual(self.sistema.dados, 3)
        
        # Verificar que não houve escritas simultâneas
        escritas_inicio = []
        escritas_fim = []
        
        for evento in self.sistema.log:
            if 'ESCRITA_INICIO' in evento['evento']:
                escritas_inicio.append(evento)
            elif 'ESCRITA_FIM' in evento['evento']:
                escritas_fim.append(evento)
        
        # Ordenar por timestamp
        escritas_inicio.sort(key=lambda x: x['timestamp'])
        escritas_fim.sort(key=lambda x: x['timestamp'])
        
        # Verificar que cada escrita termina antes da próxima começar
        for i in range(len(escritas_inicio) - 1):
            fim_atual = escritas_fim[i]['timestamp']
            inicio_proximo = escritas_inicio[i + 1]['timestamp']
            self.assertLessEqual(fim_atual, inicio_proximo, 
                               "Escritas simultâneas detectadas!")
    
    def test_leitores_bloqueiam_escritores(self):
        """Teste de que leitores bloqueiam escritores"""
        self.sistema.reset()
        
        # Modificar para ter tempos mais longos para garantir sobreposição
        def leitor_longo(id):
            self.sistema.mutex.acquire()
            self.sistema.leitores_ativos += 1
            if self.sistema.leitores_ativos == 1:
                self.sistema.wrt.acquire()
            self.sistema.mutex.release()
            
            self.sistema.log_evento(f"LEITURA_INICIO_L{id}")
            time.sleep(0.3)  # Leitura longa
            self.sistema.log_evento(f"LEITURA_FIM_L{id}")
            
            self.sistema.mutex.acquire()
            self.sistema.leitores_ativos -= 1
            if self.sistema.leitores_ativos == 0:
                self.sistema.wrt.release()
            self.sistema.mutex.release()
        
        # Iniciar leitor
        leitor_thread = threading.Thread(target=leitor_longo, args=(1,))
        leitor_thread.start()
        
        time.sleep(0.1)  # Garantir que leitor começou
        
        # Iniciar escritor (deve esperar)
        escritor_thread = threading.Thread(target=self.sistema.escritor, args=(1, 1))
        escritor_thread.start()
        
        # Aguardar conclusão
        leitor_thread.join()
        escritor_thread.join()
        
        # Verificar ordem dos eventos
        eventos = [(e['timestamp'], e['evento']) for e in self.sistema.log]
        eventos.sort(key=lambda x: x[0])
        
        # Leitor deve terminar antes do escritor começar
        leitura_fim_idx = next(i for i, (_, evt) in enumerate(eventos) if 'LEITURA_FIM_L1' in evt)
        escrita_inicio_idx = next(i for i, (_, evt) in enumerate(eventos) if 'ESCRITA_INICIO_E1' in evt)
        
        self.assertLess(leitura_fim_idx, escrita_inicio_idx,
                       "Escritor não esperou leitor terminar!")
    
    def test_escritores_bloqueiam_leitores(self):
        """Teste de que escritores bloqueiam leitores"""
        self.sistema.reset()
        
        # Modificar escritor para ser mais longo
        def escritor_longo(id):
            self.sistema.wrt.acquire()
            self.sistema.log_evento(f"ESCRITA_INICIO_E{id}")
            time.sleep(0.3)  # Escrita longa
            self.sistema.dados += 1
            self.sistema.log_evento(f"ESCRITA_FIM_E{id}")
            self.sistema.wrt.release()
        
        # Iniciar escritor
        escritor_thread = threading.Thread(target=escritor_longo, args=(1,))
        escritor_thread.start()
        
        time.sleep(0.1)  # Garantir que escritor começou
        
        # Iniciar leitor (deve esperar)
        leitor_thread = threading.Thread(target=self.sistema.leitor, args=(1, 1))
        leitor_thread.start()
        
        # Aguardar conclusão
        escritor_thread.join()
        leitor_thread.join()
        
        # Verificar ordem dos eventos
        eventos = [(e['timestamp'], e['evento']) for e in self.sistema.log]
        eventos.sort(key=lambda x: x[0])
        
        # Escritor deve terminar antes do leitor começar
        escrita_fim_idx = next(i for i, (_, evt) in enumerate(eventos) if 'ESCRITA_FIM_E1' in evt)
        leitura_inicio_idx = next(i for i, (_, evt) in enumerate(eventos) if 'LEITURA_INICIO_L1' in evt)
        
        self.assertLess(escrita_fim_idx, leitura_inicio_idx,
                       "Leitor não esperou escritor terminar!")
    
    def test_consistencia_dados(self):
        """Teste de consistência dos dados com múltiplas operações"""
        self.sistema.reset()
        num_escritores = 5
        num_escritas_por_escritor = 2
        
        # Criar escritores
        threads = []
        for i in range(num_escritores):
            t = threading.Thread(target=self.sistema.escritor, args=(i, num_escritas_por_escritor))
            threads.append(t)
            t.start()
        
        # Aguardar conclusão
        for t in threads:
            t.join()
        
        # Verificar valor final
        valor_esperado = num_escritores * num_escritas_por_escritor
        self.assertEqual(self.sistema.dados, valor_esperado,
                        f"Valor esperado: {valor_esperado}, obtido: {self.sistema.dados}")

def criar_suite_testes():
    """Cria suite de testes personalizados"""
    suite = unittest.TestSuite()
    
    # Adicionar todos os testes
    test_methods = [
        'test_leitura_simples',
        'test_escrita_simples',
        'test_multiplos_leitores_simultaneos',
        'test_exclusao_mutua_escritores',
        'test_leitores_bloqueiam_escritores',
        'test_escritores_bloqueiam_leitores',
        'test_consistencia_dados'
    ]
    
    for method in test_methods:
        suite.addTest(TestLeitoresEscritores(method))
    
    return suite

def executar_testes_detalhados():
    """Executa testes com output detalhado"""
    print("=" * 60)
    print("TESTES DO PROBLEMA DOS LEITORES-ESCRITORES")
    print("=" * 60)
    
    suite = criar_suite_testes()
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print(f"Testes executados: {resultado.testsRun}")
    print(f"Falhas: {len(resultado.failures)}")
    print(f"Erros: {len(resultado.errors)}")
    
    if resultado.failures:
        print("\nFALHAS:")
        for test, traceback in resultado.failures:
            print(f"- {test}: {traceback}")
    
    if resultado.errors:
        print("\nERROS:")
        for test, traceback in resultado.errors:
            print(f"- {test}: {traceback}")
    
    if resultado.wasSuccessful():
        print("\n✅ TODOS OS TESTES PASSARAM!")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
    
    return resultado.wasSuccessful()

if __name__ == "__main__":
    executar_testes_detalhados()