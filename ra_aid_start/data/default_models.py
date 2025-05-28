# ra_aid_start/data/default_models.py
"""
Este arquivo contém as definições de modelos LLM padrão para diferentes provedores.
A estrutura é um dicionário onde cada chave é o nome de um provedor e o valor
é uma lista de dicionários, cada um representando os dados de um modelo.
"""

DEFAULT_MODELS_DATA = {
    "OpenAI": [
        {
            "name": "gpt-4o",
            "provider": "OpenAI",
            "description": "O modelo mais recente e avançado da OpenAI, multimodal.",
            "recommended_for": ["geral", "chat", "análise", "geração de código"],
            "is_default": True,
            "supports_temperature": True,
            "context_window": 128000,
            "created_by": "system-default"
        },
        {
            "name": "gpt-4-turbo",
            "provider": "OpenAI",
            "description": "Modelo GPT-4 Turbo com janela de contexto de 128k e conhecimento até Abr 2023.",
            "recommended_for": ["geral", "chat", "análise complexa"],
            "is_default": False,
            "supports_temperature": True,
            "context_window": 128000,
            "created_by": "system-default"
        },
        {
            "name": "gpt-3.5-turbo",
            "provider": "OpenAI",
            "description": "Modelo rápido e econômico para tarefas gerais.",
            "recommended_for": ["chat rápido", "resumo", "tradução"],
            "is_default": False,
            "supports_temperature": True,
            "context_window": 16385,
            "created_by": "system-default"
        }
    ],
    "Anthropic": [
        {
            "name": "claude-3-opus-20240229",
            "provider": "Anthropic",
            "description": "O modelo mais poderoso da Anthropic para tarefas complexas.",
            "recommended_for": ["pesquisa", "desenvolvimento", "análise de alto nível"],
            "is_default": True,
            "supports_temperature": True,
            "context_window": 200000,
            "created_by": "system-default"
        },
        {
            "name": "claude-3-sonnet-20240229",
            "provider": "Anthropic",
            "description": "Equilíbrio ideal entre inteligência e velocidade para cargas de trabalho empresariais.",
            "recommended_for": ["processamento de dados", "recomendações", "geração de código"],
            "is_default": False,
            "supports_temperature": True,
            "context_window": 200000,
            "created_by": "system-default"
        },
        {
            "name": "claude-3-haiku-20240307",
            "provider": "Anthropic",
            "description": "O modelo mais rápido e compacto para capacidade de resposta quase instantânea.",
            "recommended_for": ["interação com cliente", "moderação de conteúdo", "tarefas de economia de custos"],
            "is_default": False,
            "supports_temperature": True,
            "context_window": 200000,
            "created_by": "system-default"
        }
    ],
    "Google": [
        {
            "name": "gemini-1.5-pro-latest",
            "provider": "Google",
            "description": "Modelo multimodal de médio porte da próxima geração, otimizado para uma ampla gama de tarefas.",
            "recommended_for": ["geral", "chat", "multimodal"],
            "is_default": True,
            "supports_temperature": True,
            "context_window": 1048576, # 1M tokens
            "created_by": "system-default"
        },
        {
            "name": "gemini-1.0-pro",
            "provider": "Google",
            "description": "Modelo de primeira geração otimizado para tarefas de linguagem natural.",
            "recommended_for": ["chat", "texto"],
            "is_default": False,
            "supports_temperature": True,
            "context_window": 32768,
            "created_by": "system-default"
        }
    ],
    "openrouter": [
        {
            "name": "openrouter-default",
            "provider": "openrouter",
            "description": "Modelo genérico via OpenRouter (substitua ou adicione específicos).",
            "recommended_for": ["geral", "experimental"],
            "is_default": True,
            "supports_temperature": True,
            "context_window": 32000, # Exemplo
            "created_by": "system-default"
        }
    ],
    "ollama": [
        {
            "name": "ollama-default", # Usuário precisará configurar o nome real do modelo Ollama
            "provider": "ollama",
            "description": "Modelo genérico via Ollama (configure o nome do modelo real).",
            "recommended_for": ["local", "experimental"],
            "is_default": True,
            "supports_temperature": True,
            "context_window": 8000, # Exemplo
            "created_by": "system-default"
        }
    ],
    "deepseek": [
        {
            "name": "deepseek-coder", # Exemplo popular
            "provider": "deepseek",
            "description": "Modelo DeepSeek especializado em codificação.",
            "recommended_for": ["geração de código", "assistência de código"],
            "is_default": True,
            "supports_temperature": True,
            "context_window": 16000, # Exemplo
            "created_by": "system-default"
        }
    ],
    "openai-compatible": [ # Para endpoints compatíveis com API OpenAI
        {
            "name": "openai-compatible-default",
            "provider": "openai-compatible",
            "description": "Modelo genérico para endpoints compatíveis com API OpenAI.",
            "recommended_for": ["geral", "custom llm"],
            "is_default": True,
            "supports_temperature": True,
            "context_window": 8000, # Exemplo
            "created_by": "system-default"
        }
    ],
    "fireworks": [
        {
            "name": "fireworks-default", # Exemplo, Fireworks oferece muitos modelos
            "provider": "fireworks",
            "description": "Modelo genérico via Fireworks AI.",
            "recommended_for": ["experimental", "inferência rápida"],
            "is_default": True,
            "supports_temperature": True,
            "context_window": 32000, # Exemplo
            "created_by": "system-default"
        }
    ]
    # Adicione outros provedores e seus modelos padrão aqui
}

if __name__ == '__main__':
    # Exemplo de como acessar os dados
    print("Modelos padrão da OpenAI:")
    for model in DEFAULT_MODELS_DATA.get("OpenAI", []):
        print(f"  - {model['name']} (Default: {model.get('is_default', False)})")

    print("\nModelos padrão da Anthropic:")
    for model in DEFAULT_MODELS_DATA.get("Anthropic", []):
        print(f"  - {model['name']} (Default: {model.get('is_default', False)})")

    print("\nModelos padrão da Google:")
    for model in DEFAULT_MODELS_DATA.get("Google", []):
        print(f"  - {model['name']} (Default: {model.get('is_default', False)})")

    print(f"\nTotal de provedores com modelos padrão: {len(DEFAULT_MODELS_DATA)}")