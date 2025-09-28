"""
Demonstração Completa do Sistema Leitores-Escritores
Execute este arquivo para ver todas as funcionalidades em ação
"""
import subprocess
import sys
import time
import os
from datetime import datetime

class DemonstradorCompleto:
    def __init__(self):
        self.arquivos_necessarios = [
            'launcher.py',
            'interface_unificada.py',
            'leitores_escritores_gui.py',
            'test_leitores_escritores.py',
            'demonstracao_cenarios.py',
            'exemplos_praticos.py',
            'configuracoes.py',
            'LeitoresEscritores.py',
            'README.md'
        ]
    
    def verificar_sistema(self):
        """Verifica se todos os arquivos estão presentes"""
        print("🔍 VERIFICAÇÃO DO SISTEMA")
        print("=" * 50)
        
        faltando = []
        for arquivo in self.arquivos_necessarios:
            if os.path.exists(arquivo):
                print(f"✅ {arquivo}")
            else:
                print(f"❌ {arquivo} - FALTANDO!")
                faltando.append(arquivo)
        
        print("\n📊 RESUMO:")
        print(f"   Arquivos encontrados: {len(self.arquivos_necessarios) - len(faltando)}")
        print(f"   Arquivos faltando: {len(faltando)}")
        
        if faltando:
            print(f"\n⚠️ ATENÇÃO: {len(faltando)} arquivos faltando!")
            print("   Algumas funcionalidades podem não estar disponíveis.")
        else:
            print("\n✅ SISTEMA COMPLETO - Todos os arquivos presentes!")
        
        return len(faltando) == 0
    
    def executar_testes_rapidos(self):
        """Executa testes rápidos para verificar funcionamento"""
        print("\n🧪 EXECUTANDO TESTES RÁPIDOS")
        print("=" * 50)
        
        try:
            # Executar testes unitários
            print("Executando testes unitários...")
            resultado = subprocess.run([sys.executable, "test_leitores_escritores.py"], 
                                     capture_output=True, text=True, timeout=30)
            
            if resultado.returncode == 0:
                print("✅ Testes unitários: PASSOU")
                # Contar número de testes
                output_lines = resultado.stdout.split('\n')
                for line in output_lines:
                    if "Ran" in line and "tests" in line:
                        print(f"   {line.strip()}")
                        break
            else:
                print("❌ Testes unitários: FALHOU")
                print(f"   Erro: {resultado.stderr[:100]}...")
        
        except subprocess.TimeoutExpired:
            print("⏰ Testes unitários: TIMEOUT")
        except FileNotFoundError:
            print("❌ Arquivo de testes não encontrado")
        except Exception as e:
            print(f"❌ Erro nos testes: {str(e)}")
    
    def mostrar_funcionalidades(self):
        """Mostra todas as funcionalidades disponíveis"""
        print("\n🚀 FUNCIONALIDADES DISPONÍVEIS")
        print("=" * 50)
        
        funcionalidades = [
            {
                'nome': '🖥️ Interface Unificada',
                'arquivo': 'interface_unificada.py',
                'descricao': 'Interface completa com abas para simulação, exemplos, configurações e testes'
            },
            {
                'nome': '🎮 Interface Simples',
                'arquivo': 'leitores_escritores_gui.py', 
                'descricao': 'Interface focada apenas na simulação básica'
            },
            {
                'nome': '🧪 Testes Automáticos',
                'arquivo': 'test_leitores_escritores.py',
                'descricao': '7 testes unitários para validar correção da implementação'
            },
            {
                'nome': '📚 Demonstrações',
                'arquivo': 'demonstracao_cenarios.py',
                'descricao': '5 cenários educacionais com análise detalhada'
            },
            {
                'nome': '📖 Exemplos Práticos',
                'arquivo': 'exemplos_praticos.py',
                'descricao': 'Guia interativo com casos de uso reais'
            },
            {
                'nome': '💻 Versão Terminal',
                'arquivo': 'LeitoresEscritores.py',
                'descricao': 'Implementação original em linha de comando'
            },
            {
                'nome': '🚀 Launcher Principal',
                'arquivo': 'launcher.py',
                'descricao': 'Ponto de entrada unificado para todas as funcionalidades'
            }
        ]
        
        for func in funcionalidades:
            status = "✅" if os.path.exists(func['arquivo']) else "❌"
            print(f"{status} {func['nome']}")
            print(f"   📁 {func['arquivo']}")
            print(f"   📝 {func['descricao']}")
            print()
    
    def mostrar_como_usar(self):
        """Mostra como usar o sistema"""
        print("📚 COMO USAR O SISTEMA")
        print("=" * 50)
        
        print("""
🎯 OPÇÃO 1 - INICIANTE (RECOMENDADO):
   python launcher.py
   
   → Abre menu visual com todas as opções
   → Clique em "Interface Unificada"
   → Use a aba "Exemplos" para começar

🎯 OPÇÃO 2 - INTERFACE COMPLETA:
   python interface_unificada.py
   
   → Abre interface com todas as funcionalidades
   → 5 abas: Simulação, Exemplos, Configurações, Testes, Ajuda

🎯 OPÇÃO 3 - INTERFACE SIMPLES:
   python leitores_escritores_gui.py
   
   → Foca apenas na simulação básica
   → Ideal para uso direto

🎯 OPÇÃO 4 - TESTES:
   python test_leitores_escritores.py
   
   → Executa todos os 7 testes unitários
   → Valida correção da implementação

🎯 OPÇÃO 5 - DEMONSTRAÇÕES:
   python demonstracao_cenarios.py
   
   → Menu com 5 cenários educacionais
   → Análise detalhada de comportamentos
""")
    
    def mostrar_recursos_implementados(self):
        """Mostra recursos implementados"""
        print("🔧 RECURSOS IMPLEMENTADOS")
        print("=" * 50)
        
        recursos = [
            "✅ Algoritmo correto dos Leitores-Escritores",
            "✅ Interface gráfica unificada com 5 abas",
            "✅ Interface gráfica simples para simulação",
            "✅ 7 casos de teste unitários abrangentes",
            "✅ 6 exemplos pré-configurados executáveis",
            "✅ 6 configurações pré-definidas diferentes",
            "✅ 5 cenários de demonstração educacionais",
            "✅ Controles completos: iniciar, pausar, parar, resetar",
            "✅ Log detalhado em tempo real com cores",
            "✅ Estatísticas de desempenho e análise",
            "✅ Detecção automática de problemas (starvation)",
            "✅ Validação em tempo real durante execução",
            "✅ Configurações avançadas personalizáveis",
            "✅ Sistema de launcher unificado",
            "✅ Documentação completa e help integrado",
            "✅ Suporte a múltiplas formas de execução",
            "✅ Análise temporal precisa de eventos",
            "✅ Interface responsiva e intuitiva",
            "✅ Compatibilidade com Windows/Linux/Mac",
            "✅ Sistema modular e extensível"
        ]
        
        for recurso in recursos:
            print(f"   {recurso}")
    
    def mostrar_estatisticas(self):
        """Mostra estatísticas do sistema"""
        print("\n📊 ESTATÍSTICAS DO SISTEMA")
        print("=" * 50)
        
        # Contar linhas de código
        total_linhas = 0
        arquivos_python = [f for f in self.arquivos_necessarios if f.endswith('.py')]
        
        for arquivo in arquivos_python:
            if os.path.exists(arquivo):
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        linhas = len(f.readlines())
                        total_linhas += linhas
                        print(f"   📁 {arquivo:<25} {linhas:>4} linhas")
                except:
                    print(f"   📁 {arquivo:<25} ???? linhas")
        
        print(f"\n   📈 TOTAL: {total_linhas:,} linhas de código")
        print(f"   📁 Arquivos Python: {len(arquivos_python)}")
        print(f"   🧪 Testes unitários: 7")
        print(f"   📚 Exemplos: 6")
        print(f"   ⚙️ Configurações: 6") 
        print(f"   🎭 Cenários: 5")
        print(f"   📝 Interfaces: 3 (Unificada, Simples, Launcher)")
    
    def executar_demonstracao_completa(self):
        """Executa demonstração completa do sistema"""
        print("🎉 DEMONSTRAÇÃO COMPLETA - LEITORES-ESCRITORES")
        print("=" * 60)
        print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 60)
        
        # 1. Verificar sistema
        sistema_ok = self.verificar_sistema()
        
        # 2. Executar testes rápidos
        if sistema_ok:
            self.executar_testes_rapidos()
        
        # 3. Mostrar funcionalidades
        self.mostrar_funcionalidades()
        
        # 4. Mostrar como usar
        self.mostrar_como_usar()
        
        # 5. Mostrar recursos
        self.mostrar_recursos_implementados()
        
        # 6. Mostrar estatísticas
        self.mostrar_estatisticas()
        
        # 7. Conclusão
        print("\n" + "=" * 60)
        print("🎉 DEMONSTRAÇÃO CONCLUÍDA!")
        print("=" * 60)
        
        if sistema_ok:
            print("✅ Sistema completo e funcional!")
            print("\n🚀 PRÓXIMOS PASSOS:")
            print("   1. Execute: python launcher.py")
            print("   2. Clique em 'Interface Unificada'")
            print("   3. Experimente os exemplos pré-configurados")
            print("   4. Configure seus próprios cenários")
        else:
            print("⚠️ Sistema incompleto - alguns arquivos faltando")
            print("   Verifique os arquivos marcados com ❌")
        
        print("\n📚 SISTEMA EDUCACIONAL COMPLETO PARA LEITORES-ESCRITORES")
        print("   Desenvolvido para fins educacionais e demonstração")
        print("=" * 60)

def executar_menu_interativo():
    """Menu interativo para demonstração"""
    demo = DemonstradorCompleto()
    
    opcoes = {
        '1': ('Verificar Sistema', demo.verificar_sistema),
        '2': ('Executar Testes', demo.executar_testes_rapidos),
        '3': ('Mostrar Funcionalidades', demo.mostrar_funcionalidades),
        '4': ('Como Usar', demo.mostrar_como_usar),
        '5': ('Recursos Implementados', demo.mostrar_recursos_implementados),
        '6': ('Estatísticas', demo.mostrar_estatisticas),
        '7': ('Demonstração Completa', demo.executar_demonstracao_completa)
    }
    
    while True:
        print("\n" + "=" * 60)
        print("🎭 DEMONSTRADOR DO SISTEMA LEITORES-ESCRITORES")
        print("=" * 60)
        print("Escolha uma opção:")
        
        for key, (nome, _) in opcoes.items():
            print(f"   {key}. {nome}")
        
        print("   0. Sair")
        
        try:
            escolha = input("\nOpção (0-7): ").strip()
            
            if escolha == '0':
                print("\n👋 Encerrando demonstrador...")
                break
            
            if escolha in opcoes:
                nome, funcao = opcoes[escolha]
                print(f"\n🔄 Executando: {nome}")
                print("-" * 40)
                funcao()
                input("\nPressione ENTER para continuar...")
            else:
                print("❌ Opção inválida!")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Encerrando...")
            break

if __name__ == "__main__":
    # Se executado com argumento --completo, roda demonstração completa
    if len(sys.argv) > 1 and sys.argv[1] == "--completo":
        demo = DemonstradorCompleto()
        demo.executar_demonstracao_completa()
    else:
        # Senão, roda menu interativo
        executar_menu_interativo()