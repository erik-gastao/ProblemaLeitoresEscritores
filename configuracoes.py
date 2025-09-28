"""
Configurações para diferentes cenários de teste
Permite personalizar comportamento dos leitores e escritores
"""

# Configurações padrão
CONFIG_PADRAO = {
    'num_leitores': 3,
    'num_escritores': 2,
    'delay_leitor_min': 0.5,
    'delay_leitor_max': 2.0,
    'delay_escritor_min': 1.0,
    'delay_escritor_max': 3.0,
    'tempo_leitura_min': 0.3,
    'tempo_leitura_max': 1.0,
    'tempo_escrita_min': 0.3,
    'tempo_escrita_max': 1.0,
    'duracao_teste': 10
}

# Cenário com muitos leitores (teste de starvation)
CONFIG_MUITOS_LEITORES = {
    'num_leitores': 8,
    'num_escritores': 1,
    'delay_leitor_min': 0.1,
    'delay_leitor_max': 0.3,
    'delay_escritor_min': 0.5,
    'delay_escritor_max': 1.0,
    'tempo_leitura_min': 0.1,
    'tempo_leitura_max': 0.2,
    'tempo_escrita_min': 0.5,
    'tempo_escrita_max': 1.0,
    'duracao_teste': 15
}

# Cenário com muitos escritores
CONFIG_MUITOS_ESCRITORES = {
    'num_leitores': 1,
    'num_escritores': 6,
    'delay_leitor_min': 1.0,
    'delay_leitor_max': 2.0,
    'delay_escritor_min': 0.2,
    'delay_escritor_max': 0.5,
    'tempo_leitura_min': 0.2,
    'tempo_leitura_max': 0.4,
    'tempo_escrita_min': 0.1,
    'tempo_escrita_max': 0.3,
    'duracao_teste': 12
}

# Cenário balanceado
CONFIG_BALANCEADO = {
    'num_leitores': 4,
    'num_escritores': 4,
    'delay_leitor_min': 0.5,
    'delay_leitor_max': 1.0,
    'delay_escritor_min': 0.5,
    'delay_escritor_max': 1.0,
    'tempo_leitura_min': 0.3,
    'tempo_leitura_max': 0.6,
    'tempo_escrita_min': 0.3,
    'tempo_escrita_max': 0.6,
    'duracao_teste': 10
}

# Cenário de alta concorrência
CONFIG_ALTA_CONCORRENCIA = {
    'num_leitores': 10,
    'num_escritores': 5,
    'delay_leitor_min': 0.1,
    'delay_leitor_max': 0.2,
    'delay_escritor_min': 0.1,
    'delay_escritor_max': 0.3,
    'tempo_leitura_min': 0.05,
    'tempo_leitura_max': 0.1,
    'tempo_escrita_min': 0.05,
    'tempo_escrita_max': 0.15,
    'duracao_teste': 8
}

# Cenário de teste de stress
CONFIG_STRESS = {
    'num_leitores': 15,
    'num_escritores': 8,
    'delay_leitor_min': 0.01,
    'delay_leitor_max': 0.05,
    'delay_escritor_min': 0.01,
    'delay_escritor_max': 0.1,
    'tempo_leitura_min': 0.01,
    'tempo_leitura_max': 0.05,
    'tempo_escrita_min': 0.02,
    'tempo_escrita_max': 0.08,
    'duracao_teste': 5
}

# Configurações disponíveis
CONFIGURACOES = {
    'padrao': CONFIG_PADRAO,
    'muitos_leitores': CONFIG_MUITOS_LEITORES,
    'muitos_escritores': CONFIG_MUITOS_ESCRITORES,
    'balanceado': CONFIG_BALANCEADO,
    'alta_concorrencia': CONFIG_ALTA_CONCORRENCIA,
    'stress': CONFIG_STRESS
}

def get_config(nome='padrao'):
    """Retorna configuração por nome"""
    return CONFIGURACOES.get(nome, CONFIG_PADRAO).copy()

def listar_configuracoes():
    """Lista todas as configurações disponíveis"""
    print("Configurações disponíveis:")
    for nome, config in CONFIGURACOES.items():
        print(f"\n{nome.upper()}:")
        print(f"  Leitores: {config['num_leitores']}")
        print(f"  Escritores: {config['num_escritores']}")
        print(f"  Duração: {config['duracao_teste']}s")

if __name__ == "__main__":
    listar_configuracoes()