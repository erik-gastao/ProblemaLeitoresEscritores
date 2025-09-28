# Problema dos Leitores-Escritores

Uma implementação completa do clássico problema de concorrência dos Leitores-Escritores com **interface gráfica unificada** e casos de teste abrangentes.

## 📁 Estrutura do Projeto

```
LeitoresEscritores/
├── launcher.py                    # 🚀 PONTO DE ENTRADA PRINCIPAL
├── interface_unificada.py         # 🖥️ Interface completa unificada (RECOMENDADO)
├── leitores_escritores_gui.py     # Interface gráfica simples
├── test_leitores_escritores.py    # Casos de teste unitários
├── demonstracao_cenarios.py       # Demonstrações interativas
├── exemplos_praticos.py           # Guia de exemplos
├── configuracoes.py               # Configurações personalizáveis
├── executar.py                    # Menu de acesso rápido
├── LeitoresEscritores.py          # Implementação original (linha de comando)
└── README.md                      # Este arquivo
```

## � Como Começar (RECOMENDADO)

### 1. Launcher Principal

```bash
python launcher.py
```

O launcher oferece acesso fácil a todas as funcionalidades:
- �🖥️ **Interface Unificada** (RECOMENDADO)
- 🎮 Interface Simples
- 🧪 Testes Automáticos
- 📚 Demonstrações
- 📖 Exemplos Práticos
- 💻 Versão Terminal

### 2. Interface Unificada (MELHOR OPÇÃO)

```bash
python interface_unificada.py
```

## 🖥️ Interface Unificada - Funcionalidades Completas

A interface unificada combina **TUDO** em um único aplicativo com abas:

### 🎮 Aba Simulação
- **Configuração Flexível**: Pré-definidas ou personalizadas
- **Controles Completos**: Iniciar, pausar, parar, resetar
- **Visualização em Tempo Real**: Status, estatísticas e log detalhado
- **Interface Intuitiva**: Fácil de usar e entender

### 📚 Aba Exemplos
- **6 Exemplos Pré-configurados**:
  - 🔄 Múltiplos Leitores Simultâneos
  - ⚡ Exclusão Mútua de Escritores  
  - ⚖️ Cenário Balanceado
  - 🚨 Teste de Starvation
  - 🚀 Alta Concorrência
  - 💥 Stress Test
- **Execução Automática**: Clique e execute exemplo completo
- **Aplicar Configuração**: Use configurações sem executar

### ⚙️ Aba Configurações
- **Pré-definidas**: 6 configurações prontas
- **Personalizada**: Crie suas próprias configurações
- **Avançadas**: Opções de log e performance

### 🧪 Aba Testes
- **Execução de Testes**: Todos os 7 testes unitários
- **Validação em Tempo Real**: Durante simulação
- **Resultados Detalhados**: Output completo dos testes

### ❓ Aba Ajuda
- **Como Usar**: Guia completo da interface
- **Sobre o Algoritmo**: Explicação técnica detalhada
- **FAQ**: Respostas para dúvidas comuns

### Características da Interface

- **Configuração flexível**: Ajuste o número de leitores e escritores
- **Controles de simulação**: Iniciar, pausar/continuar, parar
- **Visualização em tempo real**: 
  - Status atual dos dados e leitores ativos
  - Log detalhado de todas as operações
  - Estatísticas de desempenho
- **Interface intuitiva**: Fácil de usar e entender

### Funcionalidades

1. **Painel de Configuração**
   - Define quantos leitores (1-10)
   - Define quantos escritores (1-10)

2. **Controles de Simulação**
   - **Iniciar**: Começa a simulação
   - **Pausar/Continuar**: Pausa temporariamente
   - **Parar**: Encerra a simulação
   - **Limpar Log**: Remove histórico de eventos

3. **Status em Tempo Real**
   - Valor atual dos dados compartilhados
   - Número de leitores ativos
   - Tempo de execução

4. **Estatísticas**
   - Total de leituras realizadas
   - Total de escritas realizadas
   - Máximo de leitores simultâneos
   - Status da simulação

5. **Log Detalhado**
   - Timestamp preciso de cada operação
   - Identificação clara de leitores e escritores
   - Scroll automático para acompanhar eventos

## 🧪 Casos de Teste

### Executando os Testes

```bash
python test_leitores_escritores.py
```

### Testes Implementados

1. **Teste de Leitura Simples**
   - Verifica funcionamento básico de um leitor

2. **Teste de Escrita Simples**
   - Verifica funcionamento básico de um escritor

3. **Múltiplos Leitores Simultâneos**
   - Confirma que vários leitores podem ler ao mesmo tempo

4. **Exclusão Mútua de Escritores**
   - Garante que escritores não escrevem simultaneamente

5. **Leitores Bloqueiam Escritores**
   - Verifica que escritores esperam leitores terminarem

6. **Escritores Bloqueiam Leitores**
   - Verifica que leitores esperam escritores terminarem

7. **Teste de Consistência**
   - Confirma integridade dos dados com múltiplas operações

### Saída dos Testes

```
============================================================
TESTES DO PROBLEMA DOS LEITORES-ESCRITORES
============================================================
test_consistencia_dados ... ok
test_escrita_simples ... ok
test_escritores_bloqueiam_leitores ... ok
test_exclusao_mutua_escritores ... ok
test_leitura_simples ... ok
test_leitores_bloqueiam_escritores ... ok
test_multiplos_leitores_simultaneos ... ok

============================================================
RESUMO DOS TESTES
============================================================
Testes executados: 7
Falhas: 0
Erros: 0

✅ TODOS OS TESTES PASSARAM!
```

## 🎯 Demonstrações Interativas

### Executando as Demonstrações

```bash
python demonstracao_cenarios.py
```

### Cenários Disponíveis

1. **Múltiplos Leitores Simultâneos**
   - Demonstra leitores concorrentes
   - Mostra que não há conflito entre leitores

2. **Exclusão Mútua entre Escritores**
   - Prova que escritores se excluem mutuamente
   - Verifica integridade dos dados

3. **Interação Leitores vs Escritores**
   - Cenário misto com leitores e escritores
   - Demonstra coordenação entre os tipos

4. **Teste de Starvation**
   - Analisa possível inanição com muitos leitores
   - Identifica quando escritores são bloqueados excessivamente

5. **Análise Temporizada**
   - Controle temporal preciso
   - Análise detalhada de tempos de espera

## 🔧 Conceitos Implementados

### Problema dos Leitores-Escritores

O problema clássico de sincronização onde:

- **Leitores**: Podem ler simultaneamente
- **Escritores**: Precisam de acesso exclusivo
- **Regras**:
  - Múltiplos leitores podem ler ao mesmo tempo
  - Apenas um escritor pode escrever por vez
  - Leitores e escritores são mutuamente exclusivos

### Solução Implementada

```python
# Controle de concorrência
mutex = threading.Semaphore(1)   # Protege contador de leitores
wrt = threading.Semaphore(1)     # Garante exclusividade de escrita
leitores_ativos = 0              # Contador de leitores ativos
```

### Algoritmo do Leitor

```python
def leitor(id):
    mutex.acquire()
    leitores_ativos += 1
    if leitores_ativos == 1:
        wrt.acquire()  # Primeiro leitor bloqueia escritores
    mutex.release()
    
    # LEITURA
    
    mutex.acquire()
    leitores_ativos -= 1
    if leitores_ativos == 0:
        wrt.release()  # Último leitor libera escritores
    mutex.release()
```

### Algoritmo do Escritor

```python
def escritor(id):
    wrt.acquire()  # Acesso exclusivo
    
    # ESCRITA
    
    wrt.release()
```

## 📊 Características da Implementação

### Vantagens

- ✅ **Correção**: Implementação correta do algoritmo
- ✅ **Concorrência**: Múltiplos leitores simultâneos
- ✅ **Exclusão Mútua**: Escritores com acesso exclusivo
- ✅ **Interface Visual**: Fácil visualização do comportamento
- ✅ **Testes Abrangentes**: Verificação de correção
- ✅ **Demonstrações**: Cenários práticos de uso

### Possíveis Problemas

- ⚠️ **Starvation de Escritores**: Muitos leitores podem impedir escritores
- ⚠️ **Preferência de Leitores**: Implementação favorece leitores

## 🚀 Como Usar

### 1. Interface Gráfica (Recomendado para Visualização)

```bash
python leitores_escritores_gui.py
```

1. Ajuste número de leitores e escritores
2. Clique "Iniciar"
3. Observe o comportamento em tempo real
4. Use "Pausar" para análise detalhada
5. "Parar" quando terminar

### 2. Testes Automáticos (Para Verificação)

```bash
python test_leitores_escritores.py
```

### 3. Demonstrações Interativas (Para Estudo)

```bash
python demonstracao_cenarios.py
```

Escolha cenários específicos para análise detalhada.

### 4. Versão Original (Linha de Comando)

```bash
python LeitoresEscritores.py
```

## 🎓 Objetivos Educacionais

Esta implementação é ideal para:

- **Estudo de Concorrência**: Entender sincronização de threads
- **Análise de Algoritmos**: Verificar correção e desempenho
- **Detecção de Problemas**: Identificar condições de corrida
- **Visualização**: Ver comportamento em tempo real
- **Testes**: Validar implementações

## 🔍 Análise de Resultados

### O que Observar na Interface

1. **Leitores Simultâneos**: Vários leitores lendo ao mesmo tempo
2. **Escritores Exclusivos**: Apenas um escritor por vez
3. **Alternância**: Como leitores e escritores se alternam
4. **Estatísticas**: Balanceamento entre leituras e escritas

### Indicadores de Funcionamento Correto

- ✅ Múltiplos leitores ativos simultaneamente
- ✅ Apenas um escritor ativo por vez
- ✅ Dados consistentes (incremento correto)
- ✅ Sem condições de corrida

### Possíveis Problemas a Observar

- ❌ Escritores executando simultaneamente
- ❌ Leitores e escritores simultâneos
- ❌ Inconsistência nos dados
- ❌ Starvation excessiva de escritores

## 📈 Extensões Possíveis

1. **Algoritmo com Prioridade de Escritores**
2. **Implementação com Readers-Writers Fair**
3. **Métricas avançadas de desempenho**
4. **Simulação de diferentes cargas de trabalho**
5. **Análise de throughput e latência**

---

**Desenvolvido para fins educacionais - Problema Clássico de Concorrência**