import threading
import time
import random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import queue
import subprocess
import sys
import os

class LeitoresEscritoresUnificado:
    def __init__(self, root):
        self.root = root
        self.root.title("Problema dos Leitores-Escritores - Interface Unificada")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Recursos compartilhados
        self.dados = 0
        self.mutex = threading.Semaphore(1)
        self.wrt = threading.Semaphore(1)
        self.leitores_ativos = 0
        
        # Controle de threads
        self.threads = []
        self.running = False
        self.paused = False
        
        # Queue para comunicação thread-safe
        self.message_queue = queue.Queue()
        
        # Estatísticas
        self.stats = {
            'total_leituras': 0,
            'total_escritas': 0,
            'leitores_simultaneos_max': 0,
            'tempo_inicio': None
        }
        
        # Configurações
        self.configuracoes = self.carregar_configuracoes()
        self.config_atual = 'padrao'
        
        self.setup_ui()
        self.process_messages()
    
    def carregar_configuracoes(self):
        """Carrega as configurações disponíveis"""
        return {
            'padrao': {
                'num_leitores': 3,
                'num_escritores': 2,
                'delay_min': 0.5,
                'delay_max': 2.0,
                'descricao': 'Configuração padrão balanceada'
            },
            'muitos_leitores': {
                'num_leitores': 8,
                'num_escritores': 1,
                'delay_min': 0.1,
                'delay_max': 0.5,
                'descricao': 'Teste de starvation - muitos leitores'
            },
            'muitos_escritores': {
                'num_leitores': 1,
                'num_escritores': 6,
                'delay_min': 0.2,
                'delay_max': 0.8,
                'descricao': 'Muitos escritores competindo'
            },
            'balanceado': {
                'num_leitores': 4,
                'num_escritores': 4,
                'delay_min': 0.3,
                'delay_max': 1.0,
                'descricao': 'Cenário balanceado'
            },
            'alta_concorrencia': {
                'num_leitores': 10,
                'num_escritores': 5,
                'delay_min': 0.1,
                'delay_max': 0.3,
                'descricao': 'Alta concorrência'
            },
            'stress': {
                'num_leitores': 15,
                'num_escritores': 8,
                'delay_min': 0.05,
                'delay_max': 0.2,
                'descricao': 'Teste de stress máximo'
            }
        }
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Criar as abas
        self.setup_simulacao_tab()
        self.setup_exemplos_tab()
        self.setup_configuracoes_tab()
        self.setup_testes_tab()
        self.setup_ajuda_tab()
        
        # Barra de status
        self.setup_status_bar()
    
    def setup_simulacao_tab(self):
        """Aba principal de simulação"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎮 Simulação")
        
        # Frame principal dividido
        main_paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Lado esquerdo - Controles e Status
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Configuração rápida
        config_frame = ttk.LabelFrame(left_frame, text="⚙️ Configuração", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Seletor de configuração pré-definida
        ttk.Label(config_frame, text="Configuração:").grid(row=0, column=0, sticky=tk.W)
        self.config_var = tk.StringVar(value=self.config_atual)
        config_combo = ttk.Combobox(config_frame, textvariable=self.config_var, 
                                  values=list(self.configuracoes.keys()),
                                  state="readonly", width=15)
        config_combo.grid(row=0, column=1, padx=(5, 10))
        config_combo.bind('<<ComboboxSelected>>', self.on_config_changed)
        
        ttk.Button(config_frame, text="Aplicar", 
                  command=self.aplicar_configuracao).grid(row=0, column=2)
        
        # Configuração manual
        manual_frame = ttk.Frame(config_frame)
        manual_frame.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        ttk.Label(manual_frame, text="Leitores:").grid(row=0, column=0, sticky=tk.W)
        self.leitores_var = tk.StringVar(value="3")
        ttk.Spinbox(manual_frame, from_=1, to=20, textvariable=self.leitores_var, 
                   width=5).grid(row=0, column=1, padx=(5, 15))
        
        ttk.Label(manual_frame, text="Escritores:").grid(row=0, column=2, sticky=tk.W)
        self.escritores_var = tk.StringVar(value="2")
        ttk.Spinbox(manual_frame, from_=1, to=20, textvariable=self.escritores_var, 
                   width=5).grid(row=0, column=3, padx=(5, 0))
        
        # Controles
        control_frame = ttk.LabelFrame(left_frame, text="🎮 Controles", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        controls_grid = ttk.Frame(control_frame)
        controls_grid.pack()
        
        self.start_btn = ttk.Button(controls_grid, text="▶️ Iniciar", 
                                   command=self.start_simulation)
        self.start_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.pause_btn = ttk.Button(controls_grid, text="⏸️ Pausar", 
                                   command=self.toggle_pause, state=tk.DISABLED)
        self.pause_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.stop_btn = ttk.Button(controls_grid, text="⏹️ Parar", 
                                  command=self.stop_simulation, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.clear_btn = ttk.Button(controls_grid, text="🧹 Limpar", 
                                   command=self.clear_log)
        self.clear_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.reset_btn = ttk.Button(controls_grid, text="🔄 Reset", 
                                   command=self.reset_simulation)
        self.reset_btn.grid(row=1, column=1, padx=5, pady=5)
        
        # Status atual
        status_frame = ttk.LabelFrame(left_frame, text="📊 Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        status_grid = ttk.Frame(status_frame)
        status_grid.pack(fill=tk.X)
        
        ttk.Label(status_grid, text="Dados:").grid(row=0, column=0, sticky=tk.W)
        self.dados_label = ttk.Label(status_grid, text="0", 
                                    font=("Arial", 16, "bold"), foreground="blue")
        self.dados_label.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(status_grid, text="Leitores Ativos:").grid(row=1, column=0, sticky=tk.W)
        self.leitores_label = ttk.Label(status_grid, text="0", 
                                       font=("Arial", 12, "bold"), foreground="green")
        self.leitores_label.grid(row=1, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(status_grid, text="Estado:").grid(row=2, column=0, sticky=tk.W)
        self.estado_label = ttk.Label(status_grid, text="Parado", 
                                     font=("Arial", 10, "bold"))
        self.estado_label.grid(row=2, column=1, sticky=tk.W, padx=10)
        
        # Estatísticas
        stats_frame = ttk.LabelFrame(left_frame, text="📈 Estatísticas", padding="10")
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        self.stats_text = tk.Text(stats_frame, height=8, font=("Courier", 10))
        stats_scroll = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, 
                                    command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=stats_scroll.set)
        self.stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stats_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Lado direito - Log
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        log_frame = ttk.LabelFrame(right_frame, text="📝 Log de Atividades", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log com cores
        self.log_text = scrolledtext.ScrolledText(log_frame, height=25, 
                                                 font=("Courier", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags para cores
        self.log_text.tag_config("leitor", foreground="blue")
        self.log_text.tag_config("escritor", foreground="red")
        self.log_text.tag_config("sistema", foreground="purple")
        self.log_text.tag_config("timestamp", foreground="gray")
    
    def setup_exemplos_tab(self):
        """Aba de exemplos e demonstrações"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📚 Exemplos")
        
        # Frame principal
        main_frame = ttk.Frame(frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="📚 Exemplos e Demonstrações", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Frame para exemplos
        exemplos_frame = ttk.LabelFrame(main_frame, text="Exemplos Pré-configurados", 
                                       padding="15")
        exemplos_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lista de exemplos
        exemplos = [
            {
                'nome': '🔄 Múltiplos Leitores Simultâneos',
                'desc': 'Demonstra que vários leitores podem ler ao mesmo tempo',
                'config': {'num_leitores': 5, 'num_escritores': 1, 'duracao': 10}
            },
            {
                'nome': '⚡ Exclusão Mútua de Escritores',
                'desc': 'Mostra que escritores se excluem mutuamente',
                'config': {'num_leitores': 1, 'num_escritores': 4, 'duracao': 12}
            },
            {
                'nome': '⚖️ Cenário Balanceado',
                'desc': 'Interação equilibrada entre leitores e escritores',
                'config': {'num_leitores': 4, 'num_escritores': 3, 'duracao': 15}
            },
            {
                'nome': '🚨 Teste de Starvation',
                'desc': 'Analisa possível inanição com muitos leitores',
                'config': {'num_leitores': 8, 'num_escritores': 1, 'duracao': 20}
            },
            {
                'nome': '🚀 Alta Concorrência',
                'desc': 'Teste com máxima concorrência',
                'config': {'num_leitores': 10, 'num_escritores': 6, 'duracao': 8}
            },
            {
                'nome': '💥 Stress Test',
                'desc': 'Teste extremo do sistema',
                'config': {'num_leitores': 15, 'num_escritores': 10, 'duracao': 5}
            }
        ]
        
        # Canvas com scrollbar para exemplos
        canvas = tk.Canvas(exemplos_frame)
        scrollbar = ttk.Scrollbar(exemplos_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Criar botões para cada exemplo
        for i, exemplo in enumerate(exemplos):
            exemplo_frame = ttk.Frame(scrollable_frame, relief="raised", borderwidth=1)
            exemplo_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Nome do exemplo
            nome_label = ttk.Label(exemplo_frame, text=exemplo['nome'], 
                                  font=("Arial", 12, "bold"))
            nome_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
            
            # Descrição
            desc_label = ttk.Label(exemplo_frame, text=exemplo['desc'], 
                                  font=("Arial", 10))
            desc_label.pack(anchor=tk.W, padx=10, pady=(0, 5))
            
            # Configuração
            config_text = f"Leitores: {exemplo['config']['num_leitores']}, " \
                         f"Escritores: {exemplo['config']['num_escritores']}, " \
                         f"Duração: {exemplo['config']['duracao']}s"
            config_label = ttk.Label(exemplo_frame, text=config_text, 
                                   font=("Arial", 9), foreground="gray")
            config_label.pack(anchor=tk.W, padx=10, pady=(0, 10))
            
            # Botão para executar
            btn_frame = ttk.Frame(exemplo_frame)
            btn_frame.pack(anchor=tk.E, padx=10, pady=(0, 10))
            
            executar_btn = ttk.Button(btn_frame, text="▶️ Executar",
                                    command=lambda e=exemplo: self.executar_exemplo(e))
            executar_btn.pack(side=tk.RIGHT, padx=5)
            
            aplicar_btn = ttk.Button(btn_frame, text="📋 Aplicar Config",
                                   command=lambda e=exemplo: self.aplicar_exemplo(e))
            aplicar_btn.pack(side=tk.RIGHT)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_configuracoes_tab(self):
        """Aba de configurações avançadas"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚙️ Configurações")
        
        main_frame = ttk.Frame(frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="⚙️ Configurações Avançadas", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Notebook interno para configurações
        config_notebook = ttk.Notebook(main_frame)
        config_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba de configurações pré-definidas
        self.setup_presets_config(config_notebook)
        
        # Aba de configuração personalizada
        self.setup_custom_config(config_notebook)
        
        # Aba de configurações avançadas
        self.setup_advanced_config(config_notebook)
    
    def setup_presets_config(self, parent):
        """Configurações pré-definidas"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="📋 Pré-definidas")
        
        main_frame = ttk.Frame(frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lista de configurações
        for nome, config in self.configuracoes.items():
            config_frame = ttk.LabelFrame(main_frame, text=nome.replace('_', ' ').title(), 
                                        padding="10")
            config_frame.pack(fill=tk.X, pady=5)
            
            # Descrição
            desc_label = ttk.Label(config_frame, text=config['descricao'])
            desc_label.pack(anchor=tk.W)
            
            # Parâmetros
            params_frame = ttk.Frame(config_frame)
            params_frame.pack(fill=tk.X, pady=(5, 0))
            
            params_text = f"Leitores: {config['num_leitores']} | " \
                         f"Escritores: {config['num_escritores']} | " \
                         f"Delay: {config['delay_min']}-{config['delay_max']}s"
            ttk.Label(params_frame, text=params_text, font=("Courier", 9)).pack(side=tk.LEFT)
            
            ttk.Button(params_frame, text="Aplicar", 
                      command=lambda n=nome: self.aplicar_preset(n)).pack(side=tk.RIGHT)
    
    def setup_custom_config(self, parent):
        """Configuração personalizada"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="🎨 Personalizada")
        
        main_frame = ttk.Frame(frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Variáveis para configuração personalizada
        self.custom_leitores = tk.StringVar(value="3")
        self.custom_escritores = tk.StringVar(value="2")
        self.custom_delay_min = tk.StringVar(value="0.5")
        self.custom_delay_max = tk.StringVar(value="2.0")
        self.custom_tempo_leitura = tk.StringVar(value="1.0")
        self.custom_tempo_escrita = tk.StringVar(value="1.0")
        
        # Interface de configuração
        configs = [
            ("Número de Leitores:", self.custom_leitores, 1, 50),
            ("Número de Escritores:", self.custom_escritores, 1, 50),
            ("Delay Mínimo (s):", self.custom_delay_min, 0.1, 10.0),
            ("Delay Máximo (s):", self.custom_delay_max, 0.1, 10.0),
            ("Tempo de Leitura (s):", self.custom_tempo_leitura, 0.1, 5.0),
            ("Tempo de Escrita (s):", self.custom_tempo_escrita, 0.1, 5.0)
        ]
        
        for i, (label, var, min_val, max_val) in enumerate(configs):
            row_frame = ttk.Frame(main_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(row_frame, text=label, width=20).pack(side=tk.LEFT)
            ttk.Spinbox(row_frame, from_=min_val, to=max_val, increment=0.1,
                       textvariable=var, width=10).pack(side=tk.LEFT, padx=10)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Aplicar Configuração", 
                  command=self.aplicar_config_personalizada).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Salvar como Preset", 
                  command=self.salvar_preset).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Restaurar Padrão", 
                  command=self.restaurar_padrao).pack(side=tk.LEFT, padx=10)
    
    def setup_advanced_config(self, parent):
        """Configurações avançadas do sistema"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="🔧 Avançadas")
        
        main_frame = ttk.Frame(frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurações de log
        log_frame = ttk.LabelFrame(main_frame, text="Configurações de Log", padding="10")
        log_frame.pack(fill=tk.X, pady=5)
        
        self.log_timestamps = tk.BooleanVar(value=True)
        self.log_colors = tk.BooleanVar(value=True)
        self.log_detailed = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(log_frame, text="Mostrar timestamps", 
                       variable=self.log_timestamps).pack(anchor=tk.W)
        ttk.Checkbutton(log_frame, text="Usar cores no log", 
                       variable=self.log_colors).pack(anchor=tk.W)
        ttk.Checkbutton(log_frame, text="Log detalhado (debug)", 
                       variable=self.log_detailed).pack(anchor=tk.W)
        
        # Configurações de desempenho
        perf_frame = ttk.LabelFrame(main_frame, text="Performance", padding="10")
        perf_frame.pack(fill=tk.X, pady=5)
        
        self.auto_scroll = tk.BooleanVar(value=True)
        self.max_log_lines = tk.StringVar(value="1000")
        
        ttk.Checkbutton(perf_frame, text="Auto-scroll do log", 
                       variable=self.auto_scroll).pack(anchor=tk.W)
        
        lines_frame = ttk.Frame(perf_frame)
        lines_frame.pack(fill=tk.X, pady=5)
        ttk.Label(lines_frame, text="Máximo de linhas no log:").pack(side=tk.LEFT)
        ttk.Spinbox(lines_frame, from_=100, to=10000, increment=100,
                   textvariable=self.max_log_lines, width=8).pack(side=tk.LEFT, padx=10)
    
    def setup_testes_tab(self):
        """Aba de testes e validação"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🧪 Testes")
        
        main_frame = ttk.Frame(frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="🧪 Testes e Validação", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Seção de testes unitários
        tests_frame = ttk.LabelFrame(main_frame, text="Testes Unitários", padding="10")
        tests_frame.pack(fill=tk.X, pady=(0, 10))
        
        test_desc = """Execute os testes unitários para verificar a correção da implementação:
• Teste de leitura simples
• Teste de escrita simples  
• Teste de múltiplos leitores simultâneos
• Teste de exclusão mútua de escritores
• Teste de sincronização entre leitores e escritores
• Teste de consistência de dados"""
        
        ttk.Label(tests_frame, text=test_desc, justify=tk.LEFT).pack(anchor=tk.W)
        
        test_btn_frame = ttk.Frame(tests_frame)
        test_btn_frame.pack(pady=10)
        
        ttk.Button(test_btn_frame, text="▶️ Executar Todos os Testes", 
                  command=self.executar_testes).pack(side=tk.LEFT, padx=5)
        ttk.Button(test_btn_frame, text="📋 Ver Resultados", 
                  command=self.mostrar_resultados_testes).pack(side=tk.LEFT, padx=5)
        
        # Seção de validação em tempo real
        validation_frame = ttk.LabelFrame(main_frame, text="Validação em Tempo Real", 
                                        padding="10")
        validation_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.validation_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(validation_frame, text="Ativar validação automática durante simulação", 
                       variable=self.validation_enabled).pack(anchor=tk.W)
        
        # Área de resultados dos testes
        results_frame = ttk.LabelFrame(main_frame, text="Resultados dos Testes", 
                                     padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.test_results = scrolledtext.ScrolledText(results_frame, height=15, 
                                                     font=("Courier", 9))
        self.test_results.pack(fill=tk.BOTH, expand=True)
    
    def setup_ajuda_tab(self):
        """Aba de ajuda e documentação"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="❓ Ajuda")
        
        main_frame = ttk.Frame(frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook para diferentes seções de ajuda
        help_notebook = ttk.Notebook(main_frame)
        help_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Seção "Como Usar"
        self.setup_help_usage(help_notebook)
        
        # Seção "Sobre o Algoritmo"
        self.setup_help_algorithm(help_notebook)
        
        # Seção "FAQ"
        self.setup_help_faq(help_notebook)
    
    def setup_help_usage(self, parent):
        """Seção de ajuda sobre como usar"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="📖 Como Usar")
        
        text_frame = ttk.Frame(frame, padding="10")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text = scrolledtext.ScrolledText(text_frame, font=("Arial", 10), wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True)
        
        usage_content = """
🎮 COMO USAR A INTERFACE

1. ABA SIMULAÇÃO:
   • Escolha uma configuração pré-definida ou configure manualmente
   • Clique "Iniciar" para começar a simulação
   • Use "Pausar" para análise detalhada
   • "Parar" encerra a simulação
   • Observe o log em tempo real e as estatísticas

2. ABA EXEMPLOS:
   • Exemplos pré-configurados para diferentes cenários
   • Clique "Executar" para rodar automaticamente
   • Ou "Aplicar Config" para usar as configurações na simulação

3. ABA CONFIGURAÇÕES:
   • Pré-definidas: Configurações prontas para diferentes testes
   • Personalizada: Crie suas próprias configurações
   • Avançadas: Opções de log e performance

4. ABA TESTES:
   • Execute testes unitários para verificar correção
   • Validação em tempo real durante simulação

📊 INTERPRETANDO RESULTADOS:

COMPORTAMENTO CORRETO:
✅ Múltiplos leitores lendo simultaneamente
✅ Apenas um escritor por vez
✅ Dados incrementando consistentemente
✅ Alternância entre leituras e escritas

PROBLEMAS POTENCIAIS:
❌ Escritores simultâneos (bug grave!)
❌ Leitor e escritor simultâneos (condição de corrida!)
❌ Dados inconsistentes
❌ Starvation (escritor nunca executa)

🎯 DICAS:
• Use configurações diferentes para entender comportamentos
• Observe o máximo de leitores simultâneos
• Compare total de leituras vs escritas
• Teste cenários de stress para identificar limites
"""
        
        help_text.insert(tk.END, usage_content)
        help_text.config(state=tk.DISABLED)
    
    def setup_help_algorithm(self, parent):
        """Seção sobre o algoritmo"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="🔬 Algoritmo")
        
        text_frame = ttk.Frame(frame, padding="10")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text = scrolledtext.ScrolledText(text_frame, font=("Courier", 9), wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True)
        
        algorithm_content = """
🔬 PROBLEMA DOS LEITORES-ESCRITORES

DEFINIÇÃO:
O problema clássico de sincronização onde múltiplos processos
acessam um recurso compartilhado com duas operações distintas:

• LEITORES: Podem ler simultaneamente (operação não-destrutiva)
• ESCRITORES: Precisam de acesso exclusivo (operação destrutiva)

REGRAS:
1. Múltiplos leitores podem ler ao mesmo tempo
2. Apenas um escritor pode escrever por vez
3. Leitores e escritores são mutuamente exclusivos

IMPLEMENTAÇÃO:

Variáveis de controle:
• mutex: Semáforo binário (protege contador de leitores)
• wrt: Semáforo binário (garante exclusividade de escrita)
• leitores_ativos: Contador de leitores ativos

ALGORITMO DO LEITOR:
def leitor(id):
    mutex.acquire()                    # Proteger contador
    leitores_ativos += 1
    if leitores_ativos == 1:          # Primeiro leitor
        wrt.acquire()                  # Bloqueia escritores
    mutex.release()
    
    # === SEÇÃO CRÍTICA DE LEITURA ===
    ler_dados()
    # ===============================
    
    mutex.acquire()                    # Proteger contador
    leitores_ativos -= 1
    if leitores_ativos == 0:          # Último leitor
        wrt.release()                  # Libera escritores
    mutex.release()

ALGORITMO DO ESCRITOR:
def escritor(id):
    wrt.acquire()                      # Acesso exclusivo
    
    # === SEÇÃO CRÍTICA DE ESCRITA ===
    escrever_dados()
    # ===============================
    
    wrt.release()                      # Libera recurso

CARACTERÍSTICAS:
✅ Correção: Implementa as regras corretamente
✅ Concorrência: Múltiplos leitores simultâneos
✅ Exclusão: Escritores têm acesso exclusivo
⚠️ Starvation: Leitores podem impedir escritores indefinidamente

VARIANTES:
• Readers-preference (implementada aqui)
• Writers-preference
• Fair readers-writers
"""
        
        help_text.insert(tk.END, algorithm_content)
        help_text.config(state=tk.DISABLED)
    
    def setup_help_faq(self, parent):
        """Seção de FAQ"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="❓ FAQ")
        
        text_frame = ttk.Frame(frame, padding="10")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text = scrolledtext.ScrolledText(text_frame, font=("Arial", 10), wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True)
        
        faq_content = """
❓ PERGUNTAS FREQUENTES

Q: Por que alguns escritores não executam?
A: Isso pode indicar "starvation" - quando muitos leitores 
   impedem escritores de obter acesso. Teste com menos leitores.

Q: É normal ver vários leitores simultaneamente?
A: Sim! Múltiplos leitores podem ler ao mesmo tempo. 
   Isso é uma característica desejada do algoritmo.

Q: O que significa "condição de corrida"?
A: Ocorre quando leitores e escritores executam simultaneamente,
   violando a exclusão mútua. Isso NÃO deve acontecer.

Q: Como interpretar as estatísticas?
A: - Total leituras/escritas: Quantas operações foram feitas
   - Leitores máx: Máximo de leitores simultâneos observado
   - Tempo execução: Duração da simulação

Q: Por que usar semáforos?
A: Semáforos garantem sincronização entre threads, evitando
   condições de corrida e garantindo exclusão mútua.

Q: O algoritmo é justo?
A: Esta implementação favorece leitores (readers-preference).
   Pode causar starvation de escritores com muitos leitores.

Q: Como detectar problemas?
A: - Escritores simultâneos no log (BUG!)
   - Dados inconsistentes (pular números)
   - Escritor nunca executa (starvation)

Q: Qual a melhor configuração para aprender?
A: Comece com 3-5 leitores e 1-2 escritores. Depois teste
   cenários extremos como "muitos leitores" para ver starvation.

Q: Os testes sempre devem passar?
A: Sim! Se algum teste falhar, há bug na implementação.
   Todos os 7 testes devem passar sempre.
"""
        
        help_text.insert(tk.END, faq_content)
        help_text.config(state=tk.DISABLED)
    
    def setup_status_bar(self):
        """Barra de status na parte inferior"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)
        
        # Labels de status
        self.status_left = ttk.Label(self.status_frame, text="Pronto")
        self.status_left.pack(side=tk.LEFT)
        
        self.status_right = ttk.Label(self.status_frame, text="")
        self.status_right.pack(side=tk.RIGHT)
        
        # Separador
        ttk.Separator(self.status_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=2)
    
    # Métodos de funcionalidade
    def log_message(self, message, tipo="sistema"):
        """Adiciona mensagem ao log com timestamp e cor"""
        if self.log_timestamps.get():
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            formatted_message = f"[{timestamp}] {message}"
        else:
            formatted_message = message
        
        self.message_queue.put((formatted_message, tipo))
    
    def process_messages(self):
        """Processa mensagens da queue e atualiza a GUI"""
        try:
            while True:
                message, tipo = self.message_queue.get_nowait()
                
                # Inserir com cor
                if self.log_colors.get():
                    if "Leitor" in message:
                        tag = "leitor"
                    elif "Escritor" in message:
                        tag = "escritor"
                    else:
                        tag = "sistema"
                else:
                    tag = None
                
                self.log_text.insert(tk.END, message + "\n", tag)
                
                # Auto scroll
                if self.auto_scroll.get():
                    self.log_text.see(tk.END)
                
                # Limitar linhas do log
                try:
                    max_lines = int(self.max_log_lines.get())
                    current_lines = int(self.log_text.index(tk.END).split('.')[0])
                    if current_lines > max_lines:
                        self.log_text.delete(1.0, f"{current_lines - max_lines}.0")
                except:
                    pass
                    
        except queue.Empty:
            pass
        
        # Atualizar interface
        self.update_interface()
        
        # Reagendar
        self.root.after(100, self.process_messages)
    
    def update_interface(self):
        """Atualiza elementos da interface"""
        # Labels de status
        self.dados_label.config(text=str(self.dados))
        self.leitores_label.config(text=str(self.leitores_ativos))
        
        if self.running:
            if self.paused:
                self.estado_label.config(text="Pausado", foreground="orange")
            else:
                self.estado_label.config(text="Executando", foreground="green")
        else:
            self.estado_label.config(text="Parado", foreground="red")
        
        # Atualizar estatísticas
        self.update_stats_display()
        
        # Status bar
        if self.running:
            status_text = f"Executando - Dados: {self.dados}, Leitores: {self.leitores_ativos}"
        else:
            status_text = "Pronto"
        
        self.status_left.config(text=status_text)
        
        # Timestamp na status bar direita
        self.status_right.config(text=datetime.now().strftime("%H:%M:%S"))
    
    def update_stats_display(self):
        """Atualiza display de estatísticas"""
        if self.stats['tempo_inicio']:
            tempo_execucao = (datetime.now() - self.stats['tempo_inicio']).total_seconds()
        else:
            tempo_execucao = 0
        
        stats_text = f"""📊 ESTATÍSTICAS DE EXECUÇÃO

⏱️ Tempo de Execução: {tempo_execucao:.1f}s

📖 Total de Leituras: {self.stats['total_leituras']:,}
✍️ Total de Escritas: {self.stats['total_escritas']:,}

👥 Leitores Simultâneos:
   • Atual: {self.leitores_ativos}
   • Máximo: {self.stats['leitores_simultaneos_max']}

📈 Taxa de Operações:
   • Leituras/s: {self.stats['total_leituras']/max(tempo_execucao, 1):.1f}
   • Escritas/s: {self.stats['total_escritas']/max(tempo_execucao, 1):.1f}

⚖️ Proporção L/E: {self.stats['total_leituras']/(max(self.stats['total_escritas'], 1)):.1f}

🎯 Estado: {'🟢 Executando' if self.running else '🔴 Parado'}
{'⏸️ Pausado' if self.paused else ''}"""
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats_text)
    
    # Métodos dos algoritmos (leitor e escritor)
    def leitor(self, id):
        """Algoritmo do leitor"""
        while self.running:
            if not self.paused:
                # Delay antes de tentar ler
                time.sleep(random.uniform(0.3, 1.5))
                
                # Entrada na seção crítica
                self.mutex.acquire()
                self.leitores_ativos += 1
                if self.leitores_ativos == 1:
                    self.wrt.acquire()  # Primeiro leitor bloqueia escritores
                    self.log_message(f"🔒 Leitor {id} BLOQUEIA escritores (primeiro leitor)")
                else:
                    self.log_message(f"👥 Leitor {id} se JUNTA à leitura")
                
                # Atualizar máximo
                if self.leitores_ativos > self.stats['leitores_simultaneos_max']:
                    self.stats['leitores_simultaneos_max'] = self.leitores_ativos
                
                self.mutex.release()
                
                # Leitura (seção crítica)
                valor = self.dados
                self.log_message(f"📖 Leitor {id} está LENDO valor: {valor}", "leitor")
                self.stats['total_leituras'] += 1
                
                # Simular tempo de leitura
                time.sleep(random.uniform(0.2, 0.8))
                
                # Saída da seção crítica
                self.mutex.acquire()
                self.leitores_ativos -= 1
                if self.leitores_ativos == 0:
                    self.wrt.release()  # Último leitor libera escritores
                    self.log_message(f"🔓 Leitor {id} LIBERA escritores (último leitor)")
                else:
                    self.log_message(f"👤 Leitor {id} SAI da leitura")
                self.mutex.release()
                
            else:
                time.sleep(0.1)  # Pausa quando pausado
    
    def escritor(self, id):
        """Algoritmo do escritor"""
        while self.running:
            if not self.paused:
                # Delay antes de tentar escrever
                time.sleep(random.uniform(0.5, 2.0))
                
                self.log_message(f"⏳ Escritor {id} AGUARDANDO acesso exclusivo...")
                
                # Entrada na seção crítica
                self.wrt.acquire()
                self.log_message(f"🔒 Escritor {id} OBTEVE acesso exclusivo", "escritor")
                
                # Escrita (seção crítica)
                valor_antigo = self.dados
                time.sleep(random.uniform(0.2, 0.8))  # Simular tempo de escrita
                self.dados += 1
                
                self.log_message(f"✍️ Escritor {id} ESCREVEU: {valor_antigo} → {self.dados}", "escritor")
                self.stats['total_escritas'] += 1
                
                # Saída da seção crítica
                self.wrt.release()
                self.log_message(f"🔓 Escritor {id} LIBEROU acesso exclusivo")
                
            else:
                time.sleep(0.1)  # Pausa quando pausado
    
    # Métodos de controle da simulação
    def start_simulation(self):
        """Inicia a simulação"""
        if self.running:
            return
        
        self.running = True
        self.paused = False
        self.stats['tempo_inicio'] = datetime.now()
        
        # Reset
        self.dados = 0
        self.leitores_ativos = 0
        self.stats['total_leituras'] = 0
        self.stats['total_escritas'] = 0
        self.stats['leitores_simultaneos_max'] = 0
        
        # Obter configuração
        try:
            num_leitores = int(self.leitores_var.get())
            num_escritores = int(self.escritores_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Números de leitores e escritores devem ser inteiros válidos")
            return
        
        # Criar threads
        self.threads = []
        
        for i in range(num_leitores):
            t = threading.Thread(target=self.leitor, args=(i,), daemon=True, name=f"Leitor-{i}")
            self.threads.append(t)
            t.start()
        
        for i in range(num_escritores):
            t = threading.Thread(target=self.escritor, args=(i,), daemon=True, name=f"Escritor-{i}")
            self.threads.append(t)
            t.start()
        
        self.log_message(f"🚀 SIMULAÇÃO INICIADA: {num_leitores} leitores, {num_escritores} escritores")
        
        # Atualizar botões
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)
    
    def toggle_pause(self):
        """Alterna pausa"""
        self.paused = not self.paused
        if self.paused:
            self.pause_btn.config(text="▶️ Continuar")
            self.log_message("⏸️ Simulação PAUSADA")
        else:
            self.pause_btn.config(text="⏸️ Pausar")
            self.log_message("▶️ Simulação CONTINUADA")
    
    def stop_simulation(self):
        """Para a simulação"""
        if not self.running:
            return
            
        self.running = False
        self.paused = False
        
        tempo_total = (datetime.now() - self.stats['tempo_inicio']).total_seconds()
        
        self.log_message(f"🛑 SIMULAÇÃO PARADA - Duração: {tempo_total:.1f}s")
        self.log_message(f"📊 RESULTADO FINAL: {self.stats['total_leituras']} leituras, "
                        f"{self.stats['total_escritas']} escritas, dados = {self.dados}")
        
        # Reset semáforos
        self.mutex = threading.Semaphore(1)
        self.wrt = threading.Semaphore(1)
        self.leitores_ativos = 0
        
        # Atualizar botões
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED, text="⏸️ Pausar")
        self.stop_btn.config(state=tk.DISABLED)
    
    def reset_simulation(self):
        """Reset completo"""
        self.stop_simulation()
        time.sleep(0.1)
        
        # Reset dados
        self.dados = 0
        self.leitores_ativos = 0
        
        # Reset estatísticas
        for key in self.stats:
            if key != 'tempo_inicio':
                self.stats[key] = 0
        self.stats['tempo_inicio'] = None
        
        self.log_message("🔄 Sistema RESETADO")
    
    def clear_log(self):
        """Limpa o log"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("🧹 Log LIMPO")
    
    # Métodos de configuração e exemplos
    def on_config_changed(self, event=None):
        """Quando configuração é alterada"""
        config_nome = self.config_var.get()
        if config_nome in self.configuracoes:
            config = self.configuracoes[config_nome]
            self.leitores_var.set(str(config['num_leitores']))
            self.escritores_var.set(str(config['num_escritores']))
    
    def aplicar_configuracao(self):
        """Aplica configuração selecionada"""
        self.on_config_changed()
        self.log_message(f"⚙️ Configuração '{self.config_var.get()}' aplicada")
    
    def aplicar_preset(self, nome):
        """Aplica preset específico"""
        self.config_var.set(nome)
        self.aplicar_configuracao()
        
        # Mudar para aba de simulação
        self.notebook.select(0)
    
    def executar_exemplo(self, exemplo):
        """Executa exemplo automaticamente"""
        # Para simulação atual se estiver rodando
        if self.running:
            self.stop_simulation()
            time.sleep(0.5)
        
        # Aplicar configuração do exemplo
        config = exemplo['config']
        self.leitores_var.set(str(config['num_leitores']))
        self.escritores_var.set(str(config['num_escritores']))
        
        # Mudar para aba de simulação
        self.notebook.select(0)
        
        # Limpar log
        self.clear_log()
        
        # Iniciar simulação
        self.start_simulation()
        
        self.log_message(f"🎯 EXECUTANDO EXEMPLO: {exemplo['nome']}")
        
        # Parar automaticamente após duração especificada
        duracao = config.get('duracao', 10) * 1000  # Converter para ms
        self.root.after(duracao, self.stop_simulation)
    
    def aplicar_exemplo(self, exemplo):
        """Aplica configuração do exemplo sem executar"""
        config = exemplo['config']
        self.leitores_var.set(str(config['num_leitores']))
        self.escritores_var.set(str(config['num_escritores']))
        
        # Mudar para aba de simulação
        self.notebook.select(0)
        
        self.log_message(f"📋 Configuração do exemplo '{exemplo['nome']}' aplicada")
    
    def aplicar_config_personalizada(self):
        """Aplica configuração personalizada"""
        try:
            self.leitores_var.set(self.custom_leitores.get())
            self.escritores_var.set(self.custom_escritores.get())
            
            self.log_message("🎨 Configuração personalizada aplicada")
            
            # Mudar para aba de simulação
            self.notebook.select(0)
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Valores inválidos: {e}")
    
    def salvar_preset(self):
        """Salva configuração atual como preset"""
        # Implementação simplificada - apenas mostra mensagem
        messagebox.showinfo("Preset", "Funcionalidade de salvar preset será implementada em versão futura")
    
    def restaurar_padrao(self):
        """Restaura configurações padrão"""
        config = self.configuracoes['padrao']
        self.custom_leitores.set(str(config['num_leitores']))
        self.custom_escritores.set(str(config['num_escritores']))
        self.custom_delay_min.set("0.5")
        self.custom_delay_max.set("2.0")
        self.custom_tempo_leitura.set("1.0")
        self.custom_tempo_escrita.set("1.0")
        
        self.log_message("🔄 Configurações padrão restauradas")
    
    # Métodos de testes
    def executar_testes(self):
        """Executa os testes unitários"""
        self.test_results.delete(1.0, tk.END)
        self.test_results.insert(tk.END, "🧪 Executando testes unitários...\n\n")
        self.root.update()
        
        try:
            # Executar testes em subprocess
            result = subprocess.run([sys.executable, "test_leitores_escritores.py"], 
                                  capture_output=True, text=True, timeout=60,
                                  cwd=os.path.dirname(__file__))
            
            output = result.stdout + result.stderr
            self.test_results.insert(tk.END, output)
            
            if result.returncode == 0:
                self.test_results.insert(tk.END, "\n✅ TODOS OS TESTES PASSARAM!\n")
            else:
                self.test_results.insert(tk.END, "\n❌ ALGUNS TESTES FALHARAM!\n")
                
        except subprocess.TimeoutExpired:
            self.test_results.insert(tk.END, "\n⏰ TIMEOUT: Testes interrompidos\n")
        except FileNotFoundError:
            self.test_results.insert(tk.END, "\n❌ ERRO: Arquivo de testes não encontrado\n")
        except Exception as e:
            self.test_results.insert(tk.END, f"\n❌ ERRO: {str(e)}\n")
        
        self.test_results.see(tk.END)
    
    def mostrar_resultados_testes(self):
        """Mostra a aba de testes"""
        self.notebook.select(3)  # Seleciona aba de testes

def main():
    root = tk.Tk()
    app = LeitoresEscritoresUnificado(root)
    
    # Configurar ícone da janela (se disponível)
    try:
        root.iconbitmap(default="icon.ico")  # Se tiver um ícone
    except:
        pass
    
    # Configurar fechamento da janela
    def on_closing():
        if app.running:
            app.stop_simulation()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Iniciar aplicação
    root.mainloop()

if __name__ == "__main__":
    main()