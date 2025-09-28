import threading
import time
import random
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import queue

class LeitoresEscritoresGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Problema dos Leitores-Escritores")
        self.root.geometry("900x700")
        
        # Recurso compartilhado
        self.dados = 0
        
        # Controle de concorrência
        self.mutex = threading.Semaphore(1)
        self.wrt = threading.Semaphore(1)
        self.leitores_ativos = 0
        
        # Controle de threads
        self.threads = []
        self.running = False
        self.paused = False
        
        # Queue para comunicação thread-safe com a GUI
        self.message_queue = queue.Queue()
        
        # Estatísticas
        self.stats = {
            'total_leituras': 0,
            'total_escritas': 0,
            'leitores_simultaneos_max': 0,
            'tempo_inicio': None
        }
        
        self.setup_ui()
        self.process_messages()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuração de threads
        config_frame = ttk.LabelFrame(main_frame, text="Configuração", padding="10")
        config_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(config_frame, text="Número de Leitores:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.leitores_var = tk.StringVar(value="3")
        ttk.Spinbox(config_frame, from_=1, to=10, textvariable=self.leitores_var, width=5).grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(config_frame, text="Número de Escritores:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.escritores_var = tk.StringVar(value="2")
        ttk.Spinbox(config_frame, from_=1, to=10, textvariable=self.escritores_var, width=5).grid(row=0, column=3)
        
        # Controles
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.start_btn = ttk.Button(control_frame, text="Iniciar", command=self.start_simulation)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = ttk.Button(control_frame, text="Pausar", command=self.toggle_pause, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="Parar", command=self.stop_simulation, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(control_frame, text="Limpar Log", command=self.clear_log)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Status atual
        status_frame = ttk.LabelFrame(main_frame, text="Status Atual", padding="10")
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5), pady=5)
        
        ttk.Label(status_frame, text="Valor dos Dados:").grid(row=0, column=0, sticky=tk.W)
        self.dados_label = ttk.Label(status_frame, text="0", font=("Arial", 14, "bold"))
        self.dados_label.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(status_frame, text="Leitores Ativos:").grid(row=1, column=0, sticky=tk.W)
        self.leitores_label = ttk.Label(status_frame, text="0", font=("Arial", 12))
        self.leitores_label.grid(row=1, column=1, sticky=tk.W, padx=10)
        
        # Estatísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estatísticas", padding="10")
        stats_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=8, width=30, font=("Courier", 9))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Log de atividades
        log_frame = ttk.LabelFrame(main_frame, text="Log de Atividades", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80, font=("Courier", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
    
    def log_message(self, message):
        """Adiciona mensagem à queue para ser processada pela thread principal"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.message_queue.put(f"[{timestamp}] {message}")
    
    def process_messages(self):
        """Processa mensagens da queue e atualiza a GUI"""
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        
        # Atualizar labels
        self.dados_label.config(text=str(self.dados))
        self.leitores_label.config(text=str(self.leitores_ativos))
        
        # Atualizar estatísticas
        self.update_stats_display()
        
        # Reagendar para próxima verificação
        self.root.after(100, self.process_messages)
    
    def update_stats_display(self):
        """Atualiza a exibição das estatísticas"""
        if self.stats['tempo_inicio']:
            tempo_execucao = (datetime.now() - self.stats['tempo_inicio']).total_seconds()
        else:
            tempo_execucao = 0
            
        stats_text = f"""Tempo Execução: {tempo_execucao:.1f}s
Total Leituras: {self.stats['total_leituras']}
Total Escritas: {self.stats['total_escritas']}
Leitores Máx: {self.stats['leitores_simultaneos_max']}
Leitores Atual: {self.leitores_ativos}
Status: {'Executando' if self.running else 'Parado'}"""
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats_text)
    
    def leitor(self, id):
        """Função do leitor com interface"""
        while self.running:
            if not self.paused:
                time.sleep(random.uniform(0.5, 2))
                
                self.mutex.acquire()
                self.leitores_ativos += 1
                if self.leitores_ativos == 1:
                    self.wrt.acquire()  # primeiro leitor bloqueia escritores
                
                # Atualizar estatística de máximo
                if self.leitores_ativos > self.stats['leitores_simultaneos_max']:
                    self.stats['leitores_simultaneos_max'] = self.leitores_ativos
                
                self.mutex.release()
                
                # Leitura
                valor_lido = self.dados
                self.log_message(f"📘 Leitor {id} está lendo o valor: {valor_lido}")
                self.stats['total_leituras'] += 1
                time.sleep(random.uniform(0.5, 1.5))
                
                self.mutex.acquire()
                self.leitores_ativos -= 1
                if self.leitores_ativos == 0:
                    self.wrt.release()  # último leitor libera escritores
                self.mutex.release()
            else:
                time.sleep(0.1)  # Pequena pausa quando pausado
    
    def escritor(self, id):
        """Função do escritor com interface"""
        while self.running:
            if not self.paused:
                time.sleep(random.uniform(1, 3))
                self.wrt.acquire()
                
                # Escrita
                self.dados += 1
                self.log_message(f"✍️ Escritor {id} escreveu o valor: {self.dados}")
                self.stats['total_escritas'] += 1
                time.sleep(random.uniform(0.5, 1.5))
                
                self.wrt.release()
            else:
                time.sleep(0.1)  # Pequena pausa quando pausado
    
    def start_simulation(self):
        """Inicia a simulação"""
        if self.running:
            return
            
        self.running = True
        self.paused = False
        self.stats['tempo_inicio'] = datetime.now()
        
        # Resetar dados
        self.dados = 0
        self.leitores_ativos = 0
        self.stats['total_leituras'] = 0
        self.stats['total_escritas'] = 0
        self.stats['leitores_simultaneos_max'] = 0
        
        num_leitores = int(self.leitores_var.get())
        num_escritores = int(self.escritores_var.get())
        
        # Criar threads de leitores
        for i in range(num_leitores):
            t = threading.Thread(target=self.leitor, args=(i,), daemon=True)
            self.threads.append(t)
            t.start()
        
        # Criar threads de escritores
        for i in range(num_escritores):
            t = threading.Thread(target=self.escritor, args=(i,), daemon=True)
            self.threads.append(t)
            t.start()
        
        self.log_message(f"🚀 Simulação iniciada com {num_leitores} leitores e {num_escritores} escritores")
        
        # Atualizar botões
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)
    
    def toggle_pause(self):
        """Alterna entre pausar e continuar"""
        self.paused = not self.paused
        if self.paused:
            self.pause_btn.config(text="Continuar")
            self.log_message("⏸️ Simulação pausada")
        else:
            self.pause_btn.config(text="Pausar")
            self.log_message("▶️ Simulação continuada")
    
    def stop_simulation(self):
        """Para a simulação"""
        self.running = False
        self.paused = False
        
        self.log_message("🛑 Simulação parada")
        
        # Limpar threads
        self.threads.clear()
        
        # Resetar semáforos
        self.mutex = threading.Semaphore(1)
        self.wrt = threading.Semaphore(1)
        self.leitores_ativos = 0
        
        # Atualizar botões
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED, text="Pausar")
        self.stop_btn.config(state=tk.DISABLED)
    
    def clear_log(self):
        """Limpa o log de atividades"""
        self.log_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = LeitoresEscritoresGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()