"""
Script de execução rápida para demonstrar funcionalidades
Execute este arquivo para ver uma demonstração automática
"""
import subprocess
import sys
import os

def executar_demo_rapida():
    """Executa uma demonstração rápida do sistema"""
    print("=" * 60)
    print("DEMONSTRAÇÃO RÁPIDA - LEITORES-ESCRITORES")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("leitores_escritores_gui.py"):
        print("❌ Erro: Execute este script no diretório do projeto")
        return
    
    print("\n1. Executando testes automáticos...")
    try:
        resultado = subprocess.run([sys.executable, "test_leitores_escritores.py"], 
                                 capture_output=True, text=True, timeout=30)
        if resultado.returncode == 0:
            print("✅ Todos os testes passaram!")
        else:
            print("❌ Alguns testes falharam:")
            print(resultado.stdout)
            print(resultado.stderr)
    except subprocess.TimeoutExpired:
        print("⚠️ Testes interrompidos por timeout")
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
    
    print("\n2. Arquivos disponíveis:")
    arquivos = [
        ("leitores_escritores_gui.py", "Interface gráfica interativa"),
        ("test_leitores_escritores.py", "Casos de teste unitários"),
        ("demonstracao_cenarios.py", "Demonstrações interativas"),
        ("LeitoresEscritores.py", "Versão original (linha de comando)"),
        ("README.md", "Documentação completa")
    ]
    
    for arquivo, descricao in arquivos:
        status = "✅" if os.path.exists(arquivo) else "❌"
        print(f"   {status} {arquivo:<30} - {descricao}")
    
    print("\n3. Como usar cada componente:")
    print("   • Interface Gráfica:")
    print("     python leitores_escritores_gui.py")
    print("     (Interface visual com controles em tempo real)")
    
    print("\n   • Testes Unitários:")
    print("     python test_leitores_escritores.py")
    print("     (Verificação automática de correção)")
    
    print("\n   • Demonstrações Interativas:")
    print("     python demonstracao_cenarios.py")
    print("     (Menu com cenários específicos)")
    
    print("\n   • Versão Original:")
    print("     python LeitoresEscritores.py")
    print("     (Execução simples em linha de comando)")
    
    print("\n4. Recursos implementados:")
    recursos = [
        "✅ Algoritmo correto dos Leitores-Escritores",
        "✅ Interface gráfica com tkinter",
        "✅ Controles de pausa/continuar/parar",
        "✅ Log detalhado em tempo real",
        "✅ Estatísticas de desempenho",
        "✅ 7 casos de teste unitários",
        "✅ 5 cenários de demonstração",
        "✅ Detecção de problemas (starvation)",
        "✅ Análise temporal precisa",
        "✅ Documentação completa"
    ]
    
    for recurso in recursos:
        print(f"   {recurso}")
    
    print("\n" + "=" * 60)
    print("RECOMENDAÇÃO: Execute a interface gráfica para melhor experiência!")
    print("Comando: python leitores_escritores_gui.py")
    print("=" * 60)

def menu_rapido():
    """Menu de acesso rápido"""
    while True:
        print("\n" + "=" * 50)
        print("MENU RÁPIDO - LEITORES-ESCRITORES")
        print("=" * 50)
        print("1. Interface Gráfica")
        print("2. Executar Testes")
        print("3. Demonstrações Interativas")
        print("4. Versão Original")
        print("5. Mostrar Informações")
        print("0. Sair")
        
        try:
            escolha = input("\nEscolha uma opção (0-5): ").strip()
            
            if escolha == '0':
                print("Encerrando...")
                break
            elif escolha == '1':
                print("Iniciando interface gráfica...")
                os.system("python leitores_escritores_gui.py")
            elif escolha == '2':
                print("Executando testes...")
                os.system("python test_leitores_escritores.py")
            elif escolha == '3':
                print("Iniciando demonstrações...")
                os.system("python demonstracao_cenarios.py")
            elif escolha == '4':
                print("Executando versão original...")
                os.system("python LeitoresEscritores.py")
            elif escolha == '5':
                executar_demo_rapida()
            else:
                print("Opção inválida!")
                
        except KeyboardInterrupt:
            print("\n\nInterrompido pelo usuário.")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--info":
        executar_demo_rapida()
    else:
        menu_rapido()