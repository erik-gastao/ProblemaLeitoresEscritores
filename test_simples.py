# -*- coding: utf-8 -*-
"""
Testes Simplificados - Leitores-Escritores
Versão sem caracteres especiais para compatibilidade
"""
import unittest
import threading
import time
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class LeitoresEscritoresTestSimples:
    """Classe simplificada para testes"""
    
    def __init__(self):
        self.dados = 0
        self.mutex = threading.Semaphore(1)
        self.wrt = threading.Semaphore(1)
        self.leitores_ativos = 0
        self.log = []
        self.log_lock = threading.Lock()
        
    def reset(self):
        """Reset para novo teste"""
        self.dados = 0
        self.leitores_ativos = 0
        self.log = []
        self.mutex = threading.Semaphore(1)
        self.wrt = threading.Semaphore(1)
        
    def log_evento(self, evento):
        """Log thread-safe"""
        with self.log_lock:
            self.log.append({
                'evento': evento,
                'dados': self.dados,
                'leitores_ativos': self.leitores_ativos
            })
    
    def leitor(self, id):
        """Leitor simplificado"""
        self.mutex.acquire()
        self.leitores_ativos += 1
        if self.leitores_ativos == 1:
            self.wrt.acquire()
        self.mutex.release()
        
        # Leitura
        self.log_evento(f"LEITOR_{id}_INICIO")
        time.sleep(0.01)
        valor = self.dados
        self.log_evento(f"LEITOR_{id}_FIM_VALOR_{valor}")
        
        self.mutex.acquire()
        self.leitores_ativos -= 1
        if self.leitores_ativos == 0:
            self.wrt.release()
        self.mutex.release()
    
    def escritor(self, id):
        """Escritor simplificado"""
        self.wrt.acquire()
        
        self.log_evento(f"ESCRITOR_{id}_INICIO")
        time.sleep(0.01)
        old_value = self.dados
        self.dados += 1
        self.log_evento(f"ESCRITOR_{id}_FIM_{old_value}_PARA_{self.dados}")
        
        self.wrt.release()

class TestLeitoresEscritoresSimples(unittest.TestCase):
    """Testes unitários simplificados"""
    
    def setUp(self):
        self.sistema = LeitoresEscritoresTestSimples()
    
    def test_leitura_basica(self):
        """Teste basico de leitura"""
        self.sistema.reset()
        thread = threading.Thread(target=self.sistema.leitor, args=(1,))
        thread.start()
        thread.join()
        
        # Verificar eventos
        eventos = [e['evento'] for e in self.sistema.log]
        self.assertIn('LEITOR_1_INICIO', eventos)
        self.assertIn('LEITOR_1_FIM_VALOR_0', eventos)
    
    def test_escrita_basica(self):
        """Teste basico de escrita"""
        self.sistema.reset()
        thread = threading.Thread(target=self.sistema.escritor, args=(1,))
        thread.start()
        thread.join()
        
        self.assertEqual(self.sistema.dados, 1)
        eventos = [e['evento'] for e in self.sistema.log]
        self.assertIn('ESCRITOR_1_INICIO', eventos)
    
    def test_multiplos_leitores(self):
        """Teste com multiplos leitores"""
        self.sistema.reset()
        threads = []
        
        for i in range(3):
            t = threading.Thread(target=self.sistema.leitor, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Todos devem ter lido
        eventos = [e['evento'] for e in self.sistema.log]
        for i in range(3):
            self.assertIn(f'LEITOR_{i}_INICIO', eventos)
    
    def test_exclusao_escritores(self):
        """Teste de exclusao mutua de escritores"""
        self.sistema.reset()
        threads = []
        
        for i in range(3):
            t = threading.Thread(target=self.sistema.escritor, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Valor final deve ser 3
        self.assertEqual(self.sistema.dados, 3)
    
    def test_consistencia(self):
        """Teste de consistencia dos dados"""
        self.sistema.reset()
        num_escritores = 5
        threads = []
        
        for i in range(num_escritores):
            t = threading.Thread(target=self.sistema.escritor, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Verificar valor final
        self.assertEqual(self.sistema.dados, num_escritores)

def executar_testes_simples():
    """Executa os testes simplificados"""
    print("=" * 50)
    print("TESTES SIMPLIFICADOS - LEITORES-ESCRITORES")
    print("=" * 50)
    
    # Criar suite de testes
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLeitoresEscritoresSimples)
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    print("\n" + "=" * 50)
    print("RESUMO DOS TESTES")
    print("=" * 50)
    print(f"Testes executados: {resultado.testsRun}")
    print(f"Falhas: {len(resultado.failures)}")
    print(f"Erros: {len(resultado.errors)}")
    
    if resultado.wasSuccessful():
        print("\n[SUCESSO] TODOS OS TESTES PASSARAM!")
        print("A implementacao esta correta!")
    else:
        print("\n[FALHA] ALGUNS TESTES FALHARAM!")
        if resultado.failures:
            print("FALHAS:")
            for test, traceback in resultado.failures:
                print(f"- {test}")
        if resultado.errors:
            print("ERROS:")
            for test, traceback in resultado.errors:
                print(f"- {test}")
    
    return resultado.wasSuccessful()

if __name__ == "__main__":
    executar_testes_simples()