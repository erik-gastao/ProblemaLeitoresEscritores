"""
Exemplos práticos de uso do sistema Leitores-Escritores
Este arquivo demonstra como usar todos os componentes do sistema
"""
import os
import subprocess
import sys
import time

def exemplo_interface_grafica():
    """Exemplo de uso da interface gráfica"""
    print("=" * 60)
    print("EXEMPLO: INTERFACE GRÁFICA")
    print("=" * 60)
    
    print("""
A interface gráfica oferece:

1. CONFIGURAÇÃO:
   - Ajuste quantos leitores (1-10)
   - Ajuste quantos escritores (1-10)
   
2. CONTROLES:
   - Iniciar: Começa a simulação
   - Pausar/Continuar: Para análise detalhada
   - Parar: Encerra completamente
   - Limpar Log: Remove histórico
   
3. VISUALIZAÇÃO:
   - Valor atual dos dados
   - Leitores ativos em tempo real
   - Log com timestamp preciso
   - Estatísticas de desempenho
   
Para executar:
   python leitores_escritores_gui.py
   
DICA: Use 5 leitores e 2 escritores para ver comportamento interessante!
""")

def exemplo_testes_unitarios():
    """Exemplo dos testes unitários"""
    print("=" * 60)
    print("EXEMPLO: TESTES UNITÁRIOS")
    print("=" * 60)
    
    print("""
Os testes verificam:

✅ FUNCIONAMENTO BÁSICO:
   - Leitura simples funciona
   - Escrita simples funciona
   
✅ CONCORRÊNCIA:
   - Múltiplos leitores simultâneos
   - Escritores se excluem mutuamente
   
✅ SINCRONIZAÇÃO:
   - Leitores bloqueiam escritores
   - Escritores bloqueiam leitores
   
✅ CONSISTÊNCIA:
   - Dados permanecem íntegros
   - Sem condições de corrida
   
Para executar:
   python test_leitores_escritores.py
   
Todos os 7 testes devem passar para implementação correta!
""")

def exemplo_demonstracoes():
    """Exemplo das demonstrações interativas"""
    print("=" * 60)
    print("EXEMPLO: DEMONSTRAÇÕES INTERATIVAS")
    print("=" * 60)
    
    print("""
5 cenários educacionais:

1. MÚLTIPLOS LEITORES:
   - 4 leitores lendo simultaneamente
   - Mostra que leitores não se bloqueiam
   
2. EXCLUSÃO DE ESCRITORES:
   - 3 escritores competindo
   - Prova que apenas 1 escreve por vez
   
3. LEITORES vs ESCRITORES:
   - Cenário misto realista
   - Demonstra coordenação completa
   
4. TESTE DE STARVATION:
   - 5 leitores vs 1 escritor
   - Identifica possível inanição
   
5. ANÁLISE TEMPORAL:
   - Controle preciso de tempos
   - Análise de esperas e execuções
   
Para executar:
   python demonstracao_cenarios.py
   
Escolha o cenário no menu interativo!
""")

def exemplo_analise_resultados():
    """Como analisar os resultados"""
    print("=" * 60)
    print("EXEMPLO: COMO ANALISAR RESULTADOS")
    print("=" * 60)
    
    print("""
🔍 O QUE OBSERVAR:

COMPORTAMENTO CORRETO:
✅ Múltiplos leitores ativos simultaneamente (ex: "Leitores: 3")
✅ Apenas 1 escritor por vez (nunca "Escritores simultâneos")
✅ Alternância fluida entre leituras e escritas
✅ Dados incrementando consistentemente (0→1→2→3...)

PROBLEMAS POTENCIAIS:
❌ Dois escritores executando juntos (BUG GRAVE!)
❌ Leitor e escritor simultâneos (CONDIÇÃO DE CORRIDA!)
❌ Dados inconsistentes (ex: pular números)
❌ Escritor nunca executa (STARVATION)

MÉTRICAS IMPORTANTES:
📊 Taxa de Leituras/Escritas
📊 Tempo médio de espera
📊 Máximo de leitores simultâneos
📊 Utilização do recurso compartilhado

EXEMPLO DE LOG CORRETO:
[10:30:15.123] 📘 Leitor 0 está lendo valor: 5
[10:30:15.125] 📘 Leitor 1 está lendo valor: 5  ← SIMULTÂNEO OK!
[10:30:15.127] 📘 Leitor 2 está lendo valor: 5  ← SIMULTÂNEO OK!
[10:30:16.200] ✍️ Escritor 0 escreveu valor: 6   ← APÓS LEITORES
[10:30:17.100] 📘 Leitor 3 está lendo valor: 6  ← APÓS ESCRITOR
""")

def exemplo_configuracao_personalizada():
    """Como criar configurações personalizadas"""
    print("=" * 60)
    print("EXEMPLO: CONFIGURAÇÕES PERSONALIZADAS")
    print("=" * 60)
    
    print("""
🔧 CONFIGURAÇÕES DISPONÍVEIS:

CENÁRIO PADRÃO:
- 3 leitores, 2 escritores
- Tempos moderados
- Boa para demonstração inicial

TESTE DE STARVATION:
- 8 leitores, 1 escritor
- Leitores rápidos, escritor lento
- Pode causar inanição do escritor

ALTA CONCORRÊNCIA:
- 10 leitores, 5 escritores
- Tempos muito rápidos
- Testa limites do sistema

STRESS TEST:
- 15 leitores, 8 escritores
- Máxima concorrência
- Identifica gargalos

Para usar configurações:
   from configuracoes import get_config
   
   config = get_config('stress')
   # Use config['num_leitores'], etc.
   
Para listar todas:
   python configuracoes.py
""")

def exemplo_casos_de_uso_reais():
    """Casos de uso do mundo real"""
    print("=" * 60)
    print("EXEMPLO: CASOS DE USO REAIS")
    print("=" * 60)
    
    print("""
🌍 APLICAÇÕES PRÁTICAS:

1. BANCO DE DADOS:
   Leitores: Consultas SELECT
   Escritores: INSERT/UPDATE/DELETE
   → Múltiplas consultas simultâneas OK
   → Modificações precisam exclusividade

2. CACHE DE SISTEMA:
   Leitores: Aplicações lendo cache
   Escritores: Sistema atualizando cache
   → Leituras rápidas e simultâneas
   → Atualizações atômicas

3. ARQUIVO DE CONFIGURAÇÃO:
   Leitores: Serviços lendo configuração
   Escritores: Admin alterando configuração
   → Serviços não se bloqueiam
   → Alterações são consistentes

4. SISTEMA DE INVENTÁRIO:
   Leitores: Consultas de estoque
   Escritores: Vendas/Compras
   → Consultas simultâneas
   → Transações exclusivas

5. ESTRUTURA DE DADOS COMPARTILHADA:
   Leitores: Threads lendo estrutura
   Escritores: Threads modificando
   → Múltiplas leituras seguras
   → Modificações atômicas

VANTAGENS DA IMPLEMENTAÇÃO:
✅ Performance: Leitores não se bloqueiam
✅ Correção: Escritas são atômicas
✅ Escalabilidade: Suporta muitos leitores
""")

def executar_exemplo_completo():
    """Executa um exemplo completo do sistema"""
    print("=" * 60)
    print("EXEMPLO COMPLETO - EXECUÇÃO GUIADA")
    print("=" * 60)
    
    print("Este exemplo vai mostrar todos os componentes em ação:")
    
    # 1. Executar testes
    print("\n1. Executando testes para verificar correção...")
    try:
        resultado = subprocess.run([sys.executable, "test_leitores_escritores.py"], 
                                 capture_output=True, text=True, timeout=30)
        if resultado.returncode == 0:
            print("✅ Testes OK - Implementação correta!")
        else:
            print("❌ Falha nos testes!")
            return
    except Exception as e:
        print(f"Erro: {e}")
        return
    
    # 2. Mostrar configurações
    print("\n2. Configurações disponíveis:")
    from configuracoes import CONFIGURACOES
    for nome, config in CONFIGURACOES.items():
        print(f"   {nome}: {config['num_leitores']}L/{config['num_escritores']}E")
    
    # 3. Instruções para interface
    print("\n3. Próximos passos recomendados:")
    print("   a) Execute a interface gráfica:")
    print("      python leitores_escritores_gui.py")
    print("   b) Configure: 5 leitores, 2 escritores")
    print("   c) Clique 'Iniciar' e observe o comportamento")
    print("   d) Teste 'Pausar' para análise detalhada")
    
    print("\n4. Para análise avançada:")
    print("   python demonstracao_cenarios.py")
    print("   → Escolha 'Teste de starvation' (opção 4)")
    
    print(f"\n{'='*60}")
    print("SISTEMA PRONTO PARA USO!")
    print("Escolha uma opção acima para começar.")
    print(f"{'='*60}")

def menu_exemplos():
    """Menu interativo dos exemplos"""
    exemplos = {
        '1': ("Interface Gráfica", exemplo_interface_grafica),
        '2': ("Testes Unitários", exemplo_testes_unitarios),
        '3': ("Demonstrações", exemplo_demonstracoes),
        '4': ("Análise de Resultados", exemplo_analise_resultados),
        '5': ("Configurações", exemplo_configuracao_personalizada),
        '6': ("Casos de Uso Reais", exemplo_casos_de_uso_reais),
        '7': ("Exemplo Completo", executar_exemplo_completo)
    }
    
    while True:
        print("\n" + "="*60)
        print("EXEMPLOS PRÁTICOS - LEITORES-ESCRITORES")
        print("="*60)
        print("Escolha um exemplo para ver:")
        
        for key, (titulo, _) in exemplos.items():
            print(f"{key}. {titulo}")
        
        print("0. Sair")
        
        try:
            escolha = input("\nEscolha (0-7): ").strip()
            
            if escolha == '0':
                print("Saindo dos exemplos...")
                break
            
            if escolha in exemplos:
                titulo, funcao = exemplos[escolha]
                print(f"\n📖 Carregando: {titulo}")
                funcao()
                input("\nPressione ENTER para continuar...")
            else:
                print("Opção inválida!")
                
        except KeyboardInterrupt:
            print("\n\nInterrompido pelo usuário.")
            break

if __name__ == "__main__":
    menu_exemplos()