"""
Lançador Principal - Problema dos Leitores-Escritores
Este é o ponto de entrada principal para todas as funcionalidades
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import threading
import webbrowser

class LancadorPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Leitores-Escritores - Launcher Principal")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Centralizar janela
        self.center_window()
        
        # Configurar estilo
        self.setup_styles()
        
        # Criar interface
        self.setup_ui()
        
        # Verificar arquivos necessários
        self.check_files()
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Configura estilos da interface"""
        style = ttk.Style()
        
        # Configurar tema
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Estilos customizados
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 12))
        style.configure('Big.TButton', font=('Arial', 11, 'bold'), padding=10)
        style.configure('Description.TLabel', font=('Arial', 10), foreground='gray')
    
    def setup_ui(self):
        """Configura a interface principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Título principal
        title_label = ttk.Label(header_frame, 
                               text="🔄 Problema dos Leitores-Escritores", 
                               style='Title.TLabel')
        title_label.pack()
        
        # Subtítulo
        subtitle_label = ttk.Label(header_frame, 
                                  text="Sistema Educacional Completo com Interface Gráfica", 
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # Descrição
        desc_text = """Um sistema completo para estudar o problema clássico de concorrência
com interface visual, testes automatizados e exemplos práticos"""
        desc_label = ttk.Label(header_frame, text=desc_text, 
                              style='Description.TLabel', justify=tk.CENTER)
        desc_label.pack(pady=(10, 0))
        
        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        
        # Opções principais
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.BOTH, expand=True)
        
        # Grid de opções
        self.create_option_grid(options_frame)
        
        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        
        # Rodapé
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X)
        
        # Botões do rodapé
        self.create_footer(footer_frame)
        
        # Status
        self.status_var = tk.StringVar(value="Pronto - Escolha uma opção acima")
        status_label = ttk.Label(footer_frame, textvariable=self.status_var, 
                               style='Description.TLabel')
        status_label.pack(pady=(10, 0))
    
    def create_option_grid(self, parent):
        """Cria o grid de opções principais"""
        # Configurar grid
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        
        # Opções
        opcoes = [
            {
                'titulo': '🖥️ Interface Unificada',
                'desc': 'Interface completa com simulação,\nexemplos, testes e configurações',
                'arquivo': 'interface_unificada.py',
                'comando': self.abrir_interface_unificada,
                'destaque': True
            },
            {
                'titulo': '🎮 Interface Simples',
                'desc': 'Interface básica focada apenas\nna simulação',
                'arquivo': 'leitores_escritores_gui.py',
                'comando': self.abrir_interface_simples,
                'destaque': False
            },
            {
                'titulo': '🧪 Executar Testes',
                'desc': 'Executa todos os testes unitários\npara validar a implementação',
                'arquivo': 'test_leitores_escritores.py',
                'comando': self.executar_testes,
                'destaque': False
            },
            {
                'titulo': '📚 Demonstrações',
                'desc': 'Cenários educacionais específicos\ncom análise detalhada',
                'arquivo': 'demonstracao_cenarios.py',
                'comando': self.abrir_demonstracoes,
                'destaque': False
            },
            {
                'titulo': '💻 Versão Terminal',
                'desc': 'Execução simples em linha\nde comando (original)',
                'arquivo': 'LeitoresEscritores.py',
                'comando': self.executar_terminal,
                'destaque': False
            },
            {
                'titulo': '📖 Exemplos Práticos',
                'desc': 'Guia interativo com exemplos\ne casos de uso reais',
                'arquivo': 'exemplos_praticos.py',
                'comando': self.abrir_exemplos,
                'destaque': False
            }
        ]
        
        # Criar botões
        row, col = 0, 0
        for opcao in opcoes:
            self.create_option_button(parent, opcao, row, col)
            
            col += 1
            if col >= 2:
                col = 0
                row += 1
    
    def create_option_button(self, parent, opcao, row, col):
        """Cria um botão de opção"""
        # Frame do botão
        btn_frame = ttk.Frame(parent, relief="raised", borderwidth=1)
        btn_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew", ipady=10)
        
        # Verificar se arquivo existe
        arquivo_existe = os.path.exists(opcao['arquivo'])
        
        # Título
        titulo_color = 'black' if arquivo_existe else 'gray'
        titulo_label = ttk.Label(btn_frame, text=opcao['titulo'], 
                               font=('Arial', 12, 'bold'),
                               foreground=titulo_color)
        titulo_label.pack(pady=(10, 5))
        
        # Descrição
        desc_color = 'gray' if arquivo_existe else 'lightgray'
        desc_label = ttk.Label(btn_frame, text=opcao['desc'], 
                             justify=tk.CENTER, foreground=desc_color)
        desc_label.pack(pady=(0, 10))
        
        # Status do arquivo
        if not arquivo_existe:
            status_label = ttk.Label(btn_frame, text="❌ Arquivo não encontrado", 
                                   foreground='red', font=('Arial', 8))
            status_label.pack()
        
        # Botão
        btn_style = 'Big.TButton' if opcao.get('destaque') else 'TButton'
        btn_state = tk.NORMAL if arquivo_existe else tk.DISABLED
        
        btn = ttk.Button(btn_frame, text="Abrir" if arquivo_existe else "Indisponível", 
                        style=btn_style, state=btn_state,
                        command=opcao['comando'] if arquivo_existe else None)
        btn.pack(pady=10)
        
        # Destaque para opção recomendada
        if opcao.get('destaque') and arquivo_existe:
            btn_frame.configure(relief="solid", borderwidth=2)
            recomendado_label = ttk.Label(btn_frame, text="⭐ RECOMENDADO", 
                                        foreground='blue', font=('Arial', 8, 'bold'))
            recomendado_label.pack()
    
    def create_footer(self, parent):
        """Cria o rodapé com opções adicionais"""
        # Frame de botões
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=(0, 10))
        
        # Botões adicionais
        ttk.Button(btn_frame, text="📁 Abrir Pasta", 
                  command=self.abrir_pasta).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="📋 Sobre", 
                  command=self.mostrar_sobre).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="❓ Ajuda", 
                  command=self.mostrar_ajuda).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="🔄 Atualizar", 
                  command=self.atualizar_status).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="❌ Sair", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
    
    def check_files(self):
        """Verifica arquivos necessários"""
        arquivos_necessarios = [
            'interface_unificada.py',
            'leitores_escritores_gui.py', 
            'test_leitores_escritores.py',
            'demonstracao_cenarios.py',
            'LeitoresEscritores.py',
            'exemplos_praticos.py'
        ]
        
        faltando = []
        for arquivo in arquivos_necessarios:
            if not os.path.exists(arquivo):
                faltando.append(arquivo)
        
        if faltando:
            self.status_var.set(f"⚠️ Arquivos faltando: {len(faltando)}")
        else:
            self.status_var.set("✅ Todos os arquivos disponíveis")
    
    # Métodos para abrir cada opção
    def abrir_interface_unificada(self):
        """Abre a interface unificada"""
        self.executar_programa('interface_unificada.py', '🖥️ Interface Unificada')
    
    def abrir_interface_simples(self):
        """Abre a interface simples"""
        self.executar_programa('leitores_escritores_gui.py', '🎮 Interface Simples')
    
    def executar_testes(self):
        """Executa os testes"""
        self.executar_programa('test_leitores_escritores.py', '🧪 Testes', mostrar_output=True)
    
    def abrir_demonstracoes(self):
        """Abre as demonstrações"""
        self.executar_programa('demonstracao_cenarios.py', '📚 Demonstrações')
    
    def executar_terminal(self):
        """Executa versão terminal"""
        self.executar_programa('LeitoresEscritores.py', '💻 Versão Terminal')
    
    def abrir_exemplos(self):
        """Abre exemplos práticos"""
        self.executar_programa('exemplos_praticos.py', '📖 Exemplos Práticos')
    
    def executar_programa(self, arquivo, nome, mostrar_output=False):
        """Executa um programa Python"""
        if not os.path.exists(arquivo):
            messagebox.showerror("Erro", f"Arquivo {arquivo} não encontrado!")
            return
        
        self.status_var.set(f"Executando {nome}...")
        self.root.update()
        
        try:
            if mostrar_output:
                # Para testes, mostrar output em janela
                self.executar_com_output(arquivo, nome)
            else:
                # Para interfaces, executar em background
                subprocess.Popen([sys.executable, arquivo])
                self.status_var.set(f"{nome} iniciado com sucesso!")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar {nome}:\n{str(e)}")
            self.status_var.set("Erro ao executar programa")
    
    def executar_com_output(self, arquivo, nome):
        """Executa programa e mostra output em janela"""
        def executar():
            try:
                result = subprocess.run([sys.executable, arquivo], 
                                      capture_output=True, text=True, timeout=60)
                
                # Criar janela para mostrar resultado
                self.mostrar_resultado_teste(nome, result.stdout, result.stderr, result.returncode)
                
            except subprocess.TimeoutExpired:
                messagebox.showerror("Timeout", f"{nome} demorou muito para executar")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao executar {nome}:\n{str(e)}")
            
            self.status_var.set("Pronto")
        
        # Executar em thread separada
        thread = threading.Thread(target=executar, daemon=True)
        thread.start()
    
    def mostrar_resultado_teste(self, nome, stdout, stderr, returncode):
        """Mostra resultado dos testes em janela separada"""
        # Criar janela de resultado
        resultado_window = tk.Toplevel(self.root)
        resultado_window.title(f"Resultado: {nome}")
        resultado_window.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(resultado_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = f"📊 {nome} - "
        titulo += "✅ Sucesso" if returncode == 0 else "❌ Falha"
        ttk.Label(main_frame, text=titulo, font=('Arial', 14, 'bold')).pack(pady=(0, 10))
        
        # Área de texto com scroll
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(text_frame, font=('Courier', 10), wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Inserir conteúdo
        if stdout:
            text_widget.insert(tk.END, "SAÍDA:\n" + "="*50 + "\n")
            text_widget.insert(tk.END, stdout)
        
        if stderr:
            text_widget.insert(tk.END, "\n\nERROS:\n" + "="*50 + "\n")
            text_widget.insert(tk.END, stderr)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botão fechar
        ttk.Button(main_frame, text="Fechar", 
                  command=resultado_window.destroy).pack(pady=(10, 0))
        
        # Focar na janela
        resultado_window.focus()
    
    def abrir_pasta(self):
        """Abre a pasta do projeto no explorador"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile('.')
            elif os.name == 'posix':  # Linux/Mac
                subprocess.run(['xdg-open', '.'])
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a pasta:\n{str(e)}")
    
    def mostrar_sobre(self):
        """Mostra informações sobre o projeto"""
        sobre_text = """🔄 Problema dos Leitores-Escritores

VERSÃO: 2.0 - Interface Unificada
AUTOR: Sistema Educacional IA
DATA: Setembro 2025

DESCRIÇÃO:
Sistema completo para estudo do problema clássico de concorrência
dos Leitores-Escritores com interface gráfica, testes automatizados
e exemplos práticos.

COMPONENTES:
• Interface Gráfica Unificada (RECOMENDADO)
• Interface Simples de Simulação  
• Testes Unitários Automatizados
• Demonstrações Interativas
• Exemplos Práticos Educacionais
• Versão Original em Terminal

RECURSOS:
✅ Algoritmo correto implementado
✅ Interface visual intuitiva
✅ Controle completo da simulação
✅ Análise de problemas (starvation)
✅ Validação automática
✅ Configurações personalizáveis
✅ Documentação completa

OBJETIVO EDUCACIONAL:
Proporcionar compreensão prática e visual do problema de
sincronização de threads com leitores e escritores.
"""
        
        messagebox.showinfo("Sobre o Projeto", sobre_text)
    
    def mostrar_ajuda(self):
        """Mostra ajuda rápida"""
        ajuda_text = """❓ AJUDA RÁPIDA

COMEÇAR:
1. Clique em "🖥️ Interface Unificada" (RECOMENDADO)
2. Na aba "Simulação", configure leitores e escritores
3. Clique "Iniciar" e observe o comportamento

APRENDER:
• Use exemplos pré-configurados na aba "Exemplos"
• Execute testes para validar correção
• Experimente diferentes configurações

ENTENDER PROBLEMAS:
• Starvation: Muitos leitores impedem escritores
• Condição de Corrida: Leitores e escritores simultâneos
• Inconsistência: Dados corrompidos

O QUE OBSERVAR:
✅ Múltiplos leitores simultâneos (normal)
✅ Apenas 1 escritor por vez (obrigatório)  
❌ Escritores simultâneos (BUG!)
❌ Leitor + escritor simultâneos (BUG!)

DICA: Comece com 3-5 leitores e 1-2 escritores
"""
        
        messagebox.showinfo("Ajuda", ajuda_text)
    
    def atualizar_status(self):
        """Atualiza status dos arquivos"""
        self.check_files()
        self.root.update()

def main():
    root = tk.Tk()
    
    # Configurar ícone se disponível
    try:
        root.iconbitmap("icon.ico")
    except:
        pass
    
    # Criar launcher
    launcher = LancadorPrincipal(root)
    
    # Executar
    root.mainloop()

if __name__ == "__main__":
    main()