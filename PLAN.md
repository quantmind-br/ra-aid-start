# RA.Aid Start - Plano de Desenvolvimento

## Visão Geral

O **ra-aid-start** é uma aplicação Python que funciona diretamente no terminal (instalação via pip) para criar e executar presets de forma assistida para inicialização do aplicativo Ra.Aid.

## Objetivos

- Simplificar o uso do RA.Aid através de presets configuráveis
- Oferecer interface assistida para configuração de todas as 47 flags disponíveis
- Gerenciar modelos de forma flexível para cada provider
- Executar presets diretamente no diretório atual do usuário
- Armazenar configurações de forma persistente

## Arquitetura do Sistema

### Estrutura de Diretórios

```
ra-aid-start/
├── ra_aid_start/
│   ├── __init__.py
│   ├── __main__.py              # Entry point principal
│   ├── core/
│   │   ├── __init__.py
│   │   ├── preset_manager.py    # Gerenciamento de presets
│   │   ├── model_manager.py     # Gerenciamento de modelos
│   │   ├── config_manager.py    # Configurações globais
│   │   └── command_builder.py   # Construção de comandos ra-aid
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── menu_system.py       # Sistema de menus
│   │   ├── wizards.py          # Assistentes de configuração
│   │   └── display.py          # Formatação e exibição
│   ├── models/
│   │   ├── __init__.py
│   │   ├── preset.py           # Modelo de dados para presets
│   │   ├── provider.py         # Modelo de dados para providers
│   │   └── validation.py       # Validação de dados
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_handler.py     # Manipulação de arquivos
│   │   ├── json_handler.py     # Manipulação de JSON
│   │   └── backup_manager.py   # Sistema de backup
│   └── data/
│       ├── __init__.py
│       ├── default_models.py   # Modelos padrão por provider
│       └── schemas.py          # Schemas de validação JSON
```
├── tests/
│   ├── __init__.py
│   ├── test_preset_manager.py
│   ├── test_model_manager.py
│   └── test_wizards.py
├── setup.py
├── requirements.txt
├── README.md
└── LICENSE
```

### Armazenamento de Dados

**Localização:** `~/.ra-aid-start/`

```
~/.ra-aid-start/
├── presets/
│   ├── preset1.json
│   ├── preset2.json
│   └── ...
├── models/
│   ├── openai_models.json
│   ├── anthropic_models.json
│   ├── gemini_models.json
│   ├── ollama_models.json
│   ├── openrouter_models.json
│   ├── deepseek_models.json
│   ├── fireworks_models.json
│   └── openai_compatible_models.json
├── config.json
└── backups/
    ├── 2025-01-15_presets_backup.json
    └── ...
```

## Funcionalidades Principais

### 1. Menu Principal

```
RA.Aid Preset Manager
===================
1. 🚀 Selecionar e Executar Preset
2. ⚙️  Configurar/Editar Preset
3. 🤖 Gerenciar Modelos
4. ❌ Sair
```

### 2. Execução de Presets

- Lista todos os presets salvos com nome e comando
- Permite seleção via número ou nome
- Executa o comando ra-aid no diretório atual
- Mostra preview do comando antes da execução

### 3. Configuração Assistida

Sistema de wizard condicional que guia o usuário através de:

├── tests/
│   ├── __init__.py
│   ├── test_preset_manager.py
│   ├── test_model_manager.py
│   └── test_wizards.py
├── setup.py
├── requirements.txt
├── README.md
└── LICENSE
```

### Armazenamento de Dados

**Localização:** `~/.ra-aid-start/`

```
~/.ra-aid-start/
├── presets/
│   ├── preset1.json
│   ├── preset2.json
│   └── ...
├── models/
│   ├── openai_models.json
│   ├── anthropic_models.json
│   ├── gemini_models.json
│   ├── ollama_models.json
│   ├── openrouter_models.json
│   ├── deepseek_models.json
│   ├── fireworks_models.json
│   └── openai_compatible_models.json
├── config.json
└── backups/
    ├── 2025-01-15_presets_backup.json
    └── ...
```

## Funcionalidades Principais

### 1. Menu Principal

```
RA.Aid Preset Manager
===================
1. 🚀 Selecionar e Executar Preset
2. ⚙️  Configurar/Editar Preset
3. 🤖 Gerenciar Modelos
4. ❌ Sair
```

### 2. Execução de Presets

- Lista todos os presets salvos com nome e comando
- Permite seleção via número ou nome
- Executa o comando ra-aid no diretório atual
- Mostra preview do comando antes da execução

├── tests/
│   ├── __init__.py
│   ├── test_preset_manager.py
│   ├── test_model_manager.py
│   └── test_wizards.py
├── setup.py
├── requirements.txt
├── README.md
└── LICENSE
```

### Armazenamento de Dados

**Localização:** `~/.ra-aid-start/`

```
~/.ra-aid-start/
├── presets/
│   ├── preset1.json
│   ├── preset2.json
│   └── ...
├── models/
│   ├── openai_models.json
│   ├── anthropic_models.json
│   ├── gemini_models.json
│   ├── ollama_models.json
│   ├── openrouter_models.json
│   ├── deepseek_models.json
│   ├── fireworks_models.json
│   └── openai_compatible_models.json
├── config.json
└── backups/
    ├── 2025-01-15_presets_backup.json
    └── ...
```

## Funcionalidades Principais

### 1. Menu Principal

```
RA.Aid Preset Manager
===================
1. 🚀 Selecionar e Executar Preset
2. ⚙️  Configurar/Editar Preset
3. 🤖 Gerenciar Modelos
4. ❌ Sair
```

### 2. Execução de Presets

- Lista todos os presets salvos com nome e comando
- Permite seleção via número ou nome
- Executa o comando ra-aid no diretório atual
- Mostra preview do comando antes da execução

### 3. Configuração Assistida

Sistema de wizard condicional que guia o usuário através de:

#### 3.1 Fluxo Principal de Configuração

1. **Informações Básicas**
   - Nome do preset
   - Descrição opcional

2. **Modo de Entrada** (Decisão principal que determina o fluxo)
   - Chat Interativo (--chat)
   - Mensagem/Tarefa (-m / --message)
   - Arquivo de Texto (--msg-file)
   - Servidor Web (--server)

3. **Configurações Condicionais por Modo**

   **Modo Chat:**
   - Human-in-the-loop automático
   - Cowboy mode opcional
   - Research-only não disponível

   **Modo Mensagem/Arquivo:**
   - Opção Research-only (--research-only)
   - Human-in-the-loop opcional
   - Cowboy mode opcional
   - Configuração de mensagem/arquivo

   **Modo Servidor:**
   - Configurações de host e porta
   - Cowboy mode com aviso de segurança

4. **Configuração de Modelos**
   - Modelo principal (obrigatório)
   - Modelo expert (opcional)
   - Modelos especializados (opcional)

5. **Ferramentas de Desenvolvimento**
   - Aider integration
   - Custom tools
   - Automated testing

6. **Configurações de Exibição**
   - Cost tracking
   - Model thoughts
   - Debug information

7. **Logging e Configurações Avançadas**

### 2. Execução de Presets

- Lista todos os presets salvos com nome e comando
- Permite seleção via número ou nome
- Executa o comando ra-aid no diretório atual
- Mostra preview do comando antes da execução

### 3. Configuração Assistida

Sistema de wizard condicional que guia o usuário através de:

#### 3.1 Fluxo Principal de Configuração

1. **Informações Básicas**
   - Nome do preset
   - Descrição opcional

2. **Modo de Entrada** (Decisão principal que determina o fluxo)
   - Chat Interativo (--chat)
   - Mensagem/Tarefa (-m / --message)
   - Arquivo de Texto (--msg-file)
   - Servidor Web (--server)

3. **Configurações Condicionais por Modo**

   **Modo Chat:**
   - Human-in-the-loop automático
   - Cowboy mode opcional
   - Research-only não disponível

   **Modo Mensagem/Arquivo:**
   - Opção Research-only (--research-only)
   - Human-in-the-loop opcional
   - Cowboy mode opcional
   - Configuração de mensagem/arquivo

   **Modo Servidor:**
   - Configurações de host e porta
   - Cowboy mode com aviso de segurança

4. **Configuração de Modelos**
   - Modelo principal (obrigatório)
   - Modelo expert (opcional)
   - Modelos especializados (opcional)

5. **Ferramentas de Desenvolvimento**
   - Aider integration
   - Custom tools
   - Automated testing

### 2. Execução de Presets

- Lista todos os presets salvos com nome e comando
- Permite seleção via número ou nome
- Executa o comando ra-aid no diretório atual
- Mostra preview do comando antes da execução

### 3. Configuração Assistida

Sistema de wizard condicional que guia o usuário através de:

#### 3.1 Fluxo Principal de Configuração

1. **Informações Básicas**
   - Nome do preset
   - Descrição opcional

2. **Modo de Entrada** (Decisão principal que determina o fluxo)
   - Chat Interativo (--chat)
   - Mensagem/Tarefa (-m / --message)
   - Arquivo de Texto (--msg-file)
   - Servidor Web (--server)

3. **Configurações Condicionais por Modo**

   **Modo Chat:**
   - Human-in-the-loop automático
   - Cowboy mode opcional
   - Research-only não disponível

   **Modo Mensagem/Arquivo:**
   - Opção Research-only (--research-only)
   - Human-in-the-loop opcional
   - Cowboy mode opcional
   - Configuração de mensagem/arquivo

   **Modo Servidor:**
   - Configurações de host e porta
   - Cowboy mode com aviso de segurança

4. **Configuração de Modelos**
   - Modelo principal (obrigatório)
   - Modelo expert (opcional)
   - Modelos especializados (opcional)


- **Visualizar Modelos:** Lista modelos por provider
- **Adicionar Modelo:** Interface para adicionar novos modelos
- **Editar Modelo:** Modificar informações de modelos existentes
- **Remover Modelo:** Excluir modelos personalizados
- **Importar/Exportar:** Backup e compartilhamento de listas
- **Restaurar Padrões:** Voltar aos modelos padrão

#### 4.2 Estrutura de Dados dos Modelos

```json
{
  "provider": "openai",
  "models": [
    {
      "name": "gpt-4o",
      "description": "GPT-4 Omni - recomendado para uso geral",
      "recommended_for": ["uso geral", "programação", "análise"],
      "is_default": true,
      "supports_temperature": true,
      "context_window": 128000,
      "created_by": "system",
      "created_at": "2025-01-15T10:00:00Z"
    }
  ],
  "last_updated": "2025-01-15T15:30:00Z"
}
```

### 5. Sistema de Backup

- Backup automático antes de mudanças importantes
- Versionamento de presets
- Restauração de configurações anteriores
- Export/import de configurações completas

## Mapeamento das 47 Flags do RA.Aid

### Flags de Mensagem/Tarefa (2)
- `-m, --message`: Mensagem/tarefa principal
- `--msg-file`: Arquivo contendo a mensagem

### Flags de Modo de Operação (4)
- `--chat`: Modo chat interativo
- `--research-only`: Apenas pesquisa, sem implementação
- `--hil, -H`: Human-in-the-loop
- `--cowboy-mode`: Execução sem confirmações

### Flags de Provedor e Modelo Principal (4)
- `--provider`: Provedor LLM principal
- `--model`: Nome do modelo principal
- `--num-ctx`: Tamanho do contexto (Ollama)
- `--temperature`: Controle de aleatoriedade


- **Visualizar Modelos:** Lista modelos por provider
- **Adicionar Modelo:** Interface para adicionar novos modelos
- **Editar Modelo:** Modificar informações de modelos existentes
- **Remover Modelo:** Excluir modelos personalizados
- **Importar/Exportar:** Backup e compartilhamento de listas
- **Restaurar Padrões:** Voltar aos modelos padrão

#### 4.2 Estrutura de Dados dos Modelos

```json
{
  "provider": "openai",
  "models": [
    {
      "name": "gpt-4o",
      "description": "GPT-4 Omni - recomendado para uso geral",
      "recommended_for": ["uso geral", "programação", "análise"],
      "is_default": true,
      "supports_temperature": true,
      "context_window": 128000,
      "created_by": "system",
      "created_at": "2025-01-15T10:00:00Z"
    }
  ],
  "last_updated": "2025-01-15T15:30:00Z"
}
```

### 5. Sistema de Backup

- Backup automático antes de mudanças importantes
- Versionamento de presets
- Restauração de configurações anteriores
- Export/import de configurações completas

## Mapeamento das 47 Flags do RA.Aid

### Flags de Mensagem/Tarefa (2)
- `-m, --message`: Mensagem/tarefa principal
- `--msg-file`: Arquivo contendo a mensagem

### Flags de Modo de Operação (4)
- `--chat`: Modo chat interativo
- `--research-only`: Apenas pesquisa, sem implementação
- `--hil, -H`: Human-in-the-loop
- `--cowboy-mode`: Execução sem confirmações

### Flags de Provedor e Modelo Principal (4)
- `--provider`: Provedor LLM principal
- `--model`: Nome do modelo principal
- `--num-ctx`: Tamanho do contexto (Ollama)
- `--temperature`: Controle de aleatoriedade


- **Visualizar Modelos:** Lista modelos por provider
- **Adicionar Modelo:** Interface para adicionar novos modelos
- **Editar Modelo:** Modificar informações de modelos existentes
- **Remover Modelo:** Excluir modelos personalizados
- **Importar/Exportar:** Backup e compartilhamento de listas
- **Restaurar Padrões:** Voltar aos modelos padrão

#### 4.2 Estrutura de Dados dos Modelos

```json
{
  "provider": "openai",
  "models": [
    {
      "name": "gpt-4o",
      "description": "GPT-4 Omni - recomendado para uso geral",
      "recommended_for": ["uso geral", "programação", "análise"],
      "is_default": true,
      "supports_temperature": true,
      "context_window": 128000,
      "created_by": "system",
      "created_at": "2025-01-15T10:00:00Z"
    }
  ],
  "last_updated": "2025-01-15T15:30:00Z"
}
```

### 5. Sistema de Backup

- Backup automático antes de mudanças importantes
- Versionamento de presets
- Restauração de configurações anteriores
- Export/import de configurações completas

## Mapeamento das 47 Flags do RA.Aid

### Flags de Mensagem/Tarefa (2)
- `-m, --message`: Mensagem/tarefa principal
- `--msg-file`: Arquivo contendo a mensagem

### Flags de Modo de Operação (4)
- `--chat`: Modo chat interativo
- `--research-only`: Apenas pesquisa, sem implementação
- `--hil, -H`: Human-in-the-loop
- `--cowboy-mode`: Execução sem confirmações


### Flags de Provedor e Modelo Principal (4)
- `--provider`: Provedor LLM principal
- `--model`: Nome do modelo principal
- `--num-ctx`: Tamanho do contexto (Ollama)
- `--temperature`: Controle de aleatoriedade

### Flags de Modelo Expert (3)
- `--expert-provider`: Provedor para modelo expert
- `--expert-model`: Nome do modelo expert
- `--expert-num-ctx`: Contexto para modelo expert (Ollama)

### Flags de Modelos Especializados (4)
- `--research-provider`: Provedor para pesquisa
- `--research-model`: Modelo para pesquisa
- `--planner-provider`: Provedor para planejamento
- `--planner-model`: Modelo para planejamento

### Flags de Logging (3)
- `--log-mode`: Modo de logging (file/console)
- `--log-level`: Nível de logging (debug/info/warning/error/critical)
- `--pretty-logger`: Formatação colorida dos logs

### Flags de Servidor Web (3)
- `--server`: Ativar modo servidor
- `--server-host`: Host do servidor
- `--server-port`: Porta do servidor

### Flags de Estado do Projeto (2)
- `--project-state-dir`: Diretório de estado customizado
- `--wipe-project-memory`: Limpar memória ao iniciar

### Flags de Exibição (4)
- `--show-cost`: Mostrar custos durante execução
- `--track-cost`: Rastrear custos sem mostrar
- `--no-track-cost`: Desabilitar rastreamento de custos
- `--show-thoughts`: Mostrar processo de raciocínio do modelo

### Flags de Assistência de Raciocínio (2)
- `--reasoning-assistance`: Forçar assistência de raciocínio
- `--no-reasoning-assistance`: Desabilitar assistência de raciocínio

### Flags de Ferramentas (3)
- `--use-aider`: Usar Aider para modificações de código
- `--aider-config`: Arquivo de configuração do Aider
- `--custom-tools`: Arquivo Python com ferramentas customizadas

### Flags de Teste (4)
- `--test-cmd`: Comando de teste a ser executado
- `--auto-test`: Executar testes automaticamente
- `--max-test-cmd-retries`: Máximo de tentativas para testes
- `--test-cmd-timeout`: Timeout para execução de testes

### Flags de Configuração Avançada (3)
- `--recursion-limit`: Limite máximo de recursão
- `--disable-limit-tokens`: Desabilitar limitação de tokens
- `--experimental-fallback-handler`: Handler experimental de fallback


### Flags de Provedor e Modelo Principal (4)
- `--provider`: Provedor LLM principal
- `--model`: Nome do modelo principal
- `--num-ctx`: Tamanho do contexto (Ollama)
- `--temperature`: Controle de aleatoriedade

### Flags de Modelo Expert (3)
- `--expert-provider`: Provedor para modelo expert
- `--expert-model`: Nome do modelo expert
- `--expert-num-ctx`: Contexto para modelo expert (Ollama)

### Flags de Modelos Especializados (4)
- `--research-provider`: Provedor para pesquisa
- `--research-model`: Modelo para pesquisa
- `--planner-provider`: Provedor para planejamento
- `--planner-model`: Modelo para planejamento

### Flags de Logging (3)
- `--log-mode`: Modo de logging (file/console)
- `--log-level`: Nível de logging (debug/info/warning/error/critical)
- `--pretty-logger`: Formatação colorida dos logs

### Flags de Servidor Web (3)
- `--server`: Ativar modo servidor
- `--server-host`: Host do servidor
- `--server-port`: Porta do servidor

### Flags de Estado do Projeto (2)
- `--project-state-dir`: Diretório de estado customizado
- `--wipe-project-memory`: Limpar memória ao iniciar

### Flags de Exibição (4)
- `--show-cost`: Mostrar custos durante execução
- `--track-cost`: Rastrear custos sem mostrar
- `--no-track-cost`: Desabilitar rastreamento de custos
- `--show-thoughts`: Mostrar processo de raciocínio do modelo

### Flags de Assistência de Raciocínio (2)
- `--reasoning-assistance`: Forçar assistência de raciocínio
- `--no-reasoning-assistance`: Desabilitar assistência de raciocínio


### Flags de Ferramentas (3)
- `--use-aider`: Usar Aider para modificações de código
- `--aider-config`: Arquivo de configuração do Aider
- `--custom-tools`: Arquivo Python com ferramentas customizadas

### Flags de Teste (4)
- `--test-cmd`: Comando de teste a ser executado
- `--auto-test`: Executar testes automaticamente
- `--max-test-cmd-retries`: Máximo de tentativas para testes
- `--test-cmd-timeout`: Timeout para execução de testes

### Flags de Configuração Avançada (3)
- `--recursion-limit`: Limite máximo de recursão
- `--disable-limit-tokens`: Desabilitar limitação de tokens
- `--experimental-fallback-handler`: Handler experimental de fallback

### Flags de Configuração Padrão (2)
- `--set-default-provider`: Definir provedor padrão do sistema
- `--set-default-model`: Definir modelo padrão do sistema

### Flag de Versão (1)
- `--version`: Mostrar versão e sair

## Implementação Técnica

### Dependências Principais

```python
# requirements.txt
rich>=13.0.0           # Interface colorida no terminal
click>=8.0.0           # CLI framework
pydantic>=2.0.0        # Validação de dados
jsonschema>=4.0.0      # Validação de schemas JSON
pathlib>=1.0.0         # Manipulação de paths
typing-extensions>=4.0.0  # Type hints avançados
```

### Classes Principais

#### PresetManager
```python
class PresetManager:
    def __init__(self, storage_path: Path)
    def create_preset(self, preset_data: dict) -> Preset
    def load_preset(self, name: str) -> Preset
    def list_presets(self) -> List[Preset]
    def update_preset(self, name: str, data: dict) -> Preset
    def delete_preset(self, name: str) -> bool
    def execute_preset(self, name: str, current_dir: Path) -> bool
```

#### ModelManager
```python
class ModelManager:
    def __init__(self, storage_path: Path)
    def get_models_for_provider(self, provider: str) -> List[Model]
    def add_model(self, provider: str, model_data: dict) -> Model
    def update_model(self, provider: str, model_name: str, data: dict) -> Model
    def remove_model(self, provider: str, model_name: str) -> bool
    def import_models(self, file_path: Path) -> bool
    def export_models(self, provider: str = None) -> dict
    def restore_defaults(self, provider: str = None) -> bool
```


### Flags de Ferramentas (3)
- `--use-aider`: Usar Aider para modificações de código
- `--aider-config`: Arquivo de configuração do Aider
- `--custom-tools`: Arquivo Python com ferramentas customizadas

### Flags de Teste (4)
- `--test-cmd`: Comando de teste a ser executado
- `--auto-test`: Executar testes automaticamente
- `--max-test-cmd-retries`: Máximo de tentativas para testes
- `--test-cmd-timeout`: Timeout para execução de testes

### Flags de Configuração Avançada (3)
- `--recursion-limit`: Limite máximo de recursão
- `--disable-limit-tokens`: Desabilitar limitação de tokens
- `--experimental-fallback-handler`: Handler experimental de fallback

### Flags de Configuração Padrão (2)
- `--set-default-provider`: Definir provedor padrão do sistema
- `--set-default-model`: Definir modelo padrão do sistema

### Flag de Versão (1)
- `--version`: Mostrar versão e sair

## Implementação Técnica

### Dependências Principais

```python
# requirements.txt
rich>=13.0.0           # Interface colorida no terminal
click>=8.0.0           # CLI framework
pydantic>=2.0.0        # Validação de dados
jsonschema>=4.0.0      # Validação de schemas JSON
pathlib>=1.0.0         # Manipulação de paths
typing-extensions>=4.0.0  # Type hints avançados
```

### Classes Principais

#### PresetManager
```python
class PresetManager:
    def __init__(self, storage_path: Path)
    def create_preset(self, preset_data: dict) -> Preset
    def load_preset(self, name: str) -> Preset
    def list_presets(self) -> List[Preset]
    def update_preset(self, name: str, data: dict) -> Preset
    def delete_preset(self, name: str) -> bool
    def execute_preset(self, name: str, current_dir: Path) -> bool
```


### Flags de Ferramentas (3)
- `--use-aider`: Usar Aider para modificações de código
- `--aider-config`: Arquivo de configuração do Aider
- `--custom-tools`: Arquivo Python com ferramentas customizadas

### Flags de Teste (4)
- `--test-cmd`: Comando de teste a ser executado
- `--auto-test`: Executar testes automaticamente
- `--max-test-cmd-retries`: Máximo de tentativas para testes
- `--test-cmd-timeout`: Timeout para execução de testes

### Flags de Configuração Avançada (3)
- `--recursion-limit`: Limite máximo de recursão
- `--disable-limit-tokens`: Desabilitar limitação de tokens
- `--experimental-fallback-handler`: Handler experimental de fallback

### Flags de Configuração Padrão (2)
- `--set-default-provider`: Definir provedor padrão do sistema
- `--set-default-model`: Definir modelo padrão do sistema

### Flag de Versão (1)
- `--version`: Mostrar versão e sair

## Implementação Técnica

### Dependências Principais

```python
# requirements.txt
rich>=13.0.0           # Interface colorida no terminal
click>=8.0.0           # CLI framework
pydantic>=2.0.0        # Validação de dados
jsonschema>=4.0.0      # Validação de schemas JSON
pathlib>=1.0.0         # Manipulação de paths
typing-extensions>=4.0.0  # Type hints avançados
```

### Classes Principais

#### PresetManager
```python
class PresetManager:
    def __init__(self, storage_path: Path)
    def create_preset(self, preset_data: dict) -> Preset
    def load_preset(self, name: str) -> Preset
    def list_presets(self) -> List[Preset]
    def update_preset(self, name: str, data: dict) -> Preset
    def delete_preset(self, name: str) -> bool
    def execute_preset(self, name: str, current_dir: Path) -> bool
```


### Flags de Ferramentas (3)
- `--use-aider`: Usar Aider para modificações de código
- `--aider-config`: Arquivo de configuração do Aider
- `--custom-tools`: Arquivo Python com ferramentas customizadas

### Flags de Teste (4)
- `--test-cmd`: Comando de teste a ser executado
- `--auto-test`: Executar testes automaticamente
- `--max-test-cmd-retries`: Máximo de tentativas para testes
- `--test-cmd-timeout`: Timeout para execução de testes

### Flags de Configuração Avançada (3)
- `--recursion-limit`: Limite máximo de recursão
- `--disable-limit-tokens`: Desabilitar limitação de tokens
- `--experimental-fallback-handler`: Handler experimental de fallback

### Flags de Configuração Padrão (2)
- `--set-default-provider`: Definir provedor padrão do sistema
- `--set-default-model`: Definir modelo padrão do sistema

### Flag de Versão (1)
- `--version`: Mostrar versão e sair

## Implementação Técnica

### Dependências Principais

```python
# requirements.txt
rich>=13.0.0           # Interface colorida no terminal
click>=8.0.0           # CLI framework
pydantic>=2.0.0        # Validação de dados
jsonschema>=4.0.0      # Validação de schemas JSON
pathlib>=1.0.0         # Manipulação de paths
typing-extensions>=4.0.0  # Type hints avançados
```

### Classes Principais

#### PresetManager
```python
class PresetManager:
    def __init__(self, storage_path: Path)
    def create_preset(self, preset_data: dict) -> Preset
    def load_preset(self, name: str) -> Preset
    def list_presets(self) -> List[Preset]
    def update_preset(self, name: str, data: dict) -> Preset
    def delete_preset(self, name: str) -> bool
    def execute_preset(self, name: str, current_dir: Path) -> bool
```


### Flags de Ferramentas (3)
- `--use-aider`: Usar Aider para modificações de código
- `--aider-config`: Arquivo de configuração do Aider
- `--custom-tools`: Arquivo Python com ferramentas customizadas

### Flags de Teste (4)
- `--test-cmd`: Comando de teste a ser executado
- `--auto-test`: Executar testes automaticamente
- `--max-test-cmd-retries`: Máximo de tentativas para testes
- `--test-cmd-timeout`: Timeout para execução de testes

### Flags de Configuração Avançada (3)
- `--recursion-limit`: Limite máximo de recursão
- `--disable-limit-tokens`: Desabilitar limitação de tokens
- `--experimental-fallback-handler`: Handler experimental de fallback

### Flags de Configuração Padrão (2)
- `--set-default-provider`: Definir provedor padrão do sistema
- `--set-default-model`: Definir modelo padrão do sistema

### Flag de Versão (1)
- `--version`: Mostrar versão e sair

## Implementação Técnica

### Dependências Principais

```python
# requirements.txt
rich>=13.0.0           # Interface colorida no terminal
click>=8.0.0           # CLI framework
pydantic>=2.0.0        # Validação de dados
jsonschema>=4.0.0      # Validação de schemas JSON
pathlib>=1.0.0         # Manipulação de paths
typing-extensions>=4.0.0  # Type hints avançados
```

### Classes Principais

#### PresetManager
```python
class PresetManager:
    def __init__(self, storage_path: Path)
    def create_preset(self, preset_data: dict) -> Preset
    def load_preset(self, name: str) -> Preset
    def list_presets(self) -> List[Preset]
    def update_preset(self, name: str, data: dict) -> Preset
```


### Flags de Ferramentas (3)
- `--use-aider`: Usar Aider para modificações de código
- `--aider-config`: Arquivo de configuração do Aider
- `--custom-tools`: Arquivo Python com ferramentas customizadas

### Flags de Teste (4)
- `--test-cmd`: Comando de teste a ser executado
- `--auto-test`: Executar testes automaticamente
- `--max-test-cmd-retries`: Máximo de tentativas para testes
- `--test-cmd-timeout`: Timeout para execução de testes

### Flags de Configuração Avançada (3)
- `--recursion-limit`: Limite máximo de recursão
- `--disable-limit-tokens`: Desabilitar limitação de tokens
- `--experimental-fallback-handler`: Handler experimental de fallback

### Flags de Configuração Padrão (2)
- `--set-default-provider`: Definir provedor padrão do sistema
- `--set-default-model`: Definir modelo padrão do sistema

## Implementação Técnica

### Dependências Principais

```python
# requirements.txt
rich>=13.0.0           # Interface colorida no terminal
click>=8.0.0           # CLI framework
pydantic>=2.0.0        # Validação de dados
jsonschema>=4.0.0      # Validação de schemas JSON
pathlib>=1.0.0         # Manipulação de paths
typing-extensions>=4.0.0  # Type hints avançados
```

### Classes Principais

#### PresetManager
```python
class PresetManager:
    def __init__(self, storage_path: Path)
    def create_preset(self, preset_data: dict) -> Preset
    def load_preset(self, name: str) -> Preset
    def list_presets(self) -> List[Preset]
    def update_preset(self, name: str, data: dict) -> Preset
    def delete_preset(self, name: str) -> bool
    def execute_preset(self, name: str, current_dir: Path) -> bool
```


#### ModelManager
```python
class ModelManager:
    def __init__(self, storage_path: Path)
    def get_models_for_provider(self, provider: str) -> List[Model]
    def add_model(self, provider: str, model_data: dict) -> Model
    def update_model(self, provider: str, model_name: str, data: dict) -> Model
    def remove_model(self, provider: str, model_name: str) -> bool
    def import_models(self, file_path: Path) -> bool
    def export_models(self, provider: str = None) -> dict
    def restore_defaults(self, provider: str = None) -> bool
```

#### ConfigurationWizard
```python
class ConfigurationWizard:
    def __init__(self, preset_manager: PresetManager, model_manager: ModelManager)
    def start_wizard(self) -> Optional[Preset]
    def collect_basic_info(self) -> dict
    def select_operation_mode(self) -> str
    def configure_conditional_settings(self, mode: str) -> dict
    def configure_models(self) -> dict
    def configure_tools(self) -> dict
    def configure_display(self) -> dict
    def configure_logging(self) -> dict
    def configure_advanced(self) -> dict
    def show_summary_and_confirm(self, preset_data: dict) -> bool
```

#### CommandBuilder
```python
class CommandBuilder:
    def __init__(self)
    def build_command(self, preset: Preset) -> str
    def validate_command(self, command: str) -> bool
    def add_flag(self, flag: str, value: Any = None) -> 'CommandBuilder'
    def remove_flag(self, flag: str) -> 'CommandBuilder'
    def get_command_string(self) -> str
```

### Modelos de Dados

#### Preset
```python
@dataclass
class Preset:
    name: str
    description: str
    operation_mode: str
    flags: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    command: str
    
    def to_dict(self) -> dict
    def from_dict(cls, data: dict) -> 'Preset'
    def validate(self) -> bool
```

#### Model
```python
@dataclass
class Model:
    name: str
    provider: str
    description: str
    recommended_for: List[str]
    is_default: bool
    supports_temperature: bool
    context_window: Optional[int]
    created_by: str
    created_at: datetime
```


#### ModelManager
```python
class ModelManager:
    def __init__(self, storage_path: Path)
    def get_models_for_provider(self, provider: str) -> List[Model]
    def add_model(self, provider: str, model_data: dict) -> Model
    def update_model(self, provider: str, model_name: str, data: dict) -> Model
    def remove_model(self, provider: str, model_name: str) -> bool
    def import_models(self, file_path: Path) -> bool
    def export_models(self, provider: str = None) -> dict
    def restore_defaults(self, provider: str = None) -> bool
```

#### ConfigurationWizard
```python
class ConfigurationWizard:
    def __init__(self, preset_manager: PresetManager, model_manager: ModelManager)
    def start_wizard(self) -> Optional[Preset]
    def collect_basic_info(self) -> dict
    def select_operation_mode(self) -> str
    def configure_conditional_settings(self, mode: str) -> dict
    def configure_models(self) -> dict
    def configure_tools(self) -> dict
    def configure_display(self) -> dict
    def configure_logging(self) -> dict
    def configure_advanced(self) -> dict
    def show_summary_and_confirm(self, preset_data: dict) -> bool
```

#### CommandBuilder
```python
class CommandBuilder:
    def __init__(self)
    def build_command(self, preset: Preset) -> str
    def validate_command(self, command: str) -> bool
    def add_flag(self, flag: str, value: Any = None) -> 'CommandBuilder'
    def remove_flag(self, flag: str) -> 'CommandBuilder'
    def get_command_string(self) -> str
```

### Modelos de Dados

#### Preset
```python
@dataclass
class Preset:
    name: str
    description: str
    operation_mode: str
    flags: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    command: str
    
    def to_dict(self) -> dict
    def from_dict(cls, data: dict) -> 'Preset'
    def validate(self) -> bool
```


#### ModelManager
```python
class ModelManager:
    def __init__(self, storage_path: Path)
    def get_models_for_provider(self, provider: str) -> List[Model]
    def add_model(self, provider: str, model_data: dict) -> Model
    def update_model(self, provider: str, model_name: str, data: dict) -> Model
    def remove_model(self, provider: str, model_name: str) -> bool
    def import_models(self, file_path: Path) -> bool
    def export_models(self, provider: str = None) -> dict
    def restore_defaults(self, provider: str = None) -> bool
```

#### ConfigurationWizard
```python
class ConfigurationWizard:
    def __init__(self, preset_manager: PresetManager, model_manager: ModelManager)
    def start_wizard(self) -> Optional[Preset]
    def collect_basic_info(self) -> dict
    def select_operation_mode(self) -> str
    def configure_conditional_settings(self, mode: str) -> dict
    def configure_models(self) -> dict
    def configure_tools(self) -> dict
    def configure_display(self) -> dict
    def configure_logging(self) -> dict
    def configure_advanced(self) -> dict
    def show_summary_and_confirm(self, preset_data: dict) -> bool
```

#### CommandBuilder
```python
class CommandBuilder:
    def __init__(self)
    def build_command(self, preset: Preset) -> str
    def validate_command(self, command: str) -> bool
    def add_flag(self, flag: str, value: Any = None) -> 'CommandBuilder'
    def remove_flag(self, flag: str) -> 'CommandBuilder'
    def get_command_string(self) -> str
```


### Modelos de Dados

#### Preset
```python
@dataclass
class Preset:
    name: str
    description: str
    operation_mode: str
    flags: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    command: str
    
    def to_dict(self) -> dict
    def from_dict(cls, data: dict) -> 'Preset'
    def validate(self) -> bool
```

#### Model
```python
@dataclass
class Model:
    name: str
    provider: str
    description: str
    recommended_for: List[str]
    is_default: bool
    supports_temperature: bool
    context_window: Optional[int]
    created_by: str
    created_at: datetime
```

### Sistema de Validação

#### ValidationRules
```python
class ValidationRules:
    @staticmethod
    def validate_provider_model_combination(provider: str, model: str) -> bool
    
    @staticmethod
    def validate_flag_dependencies(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_conflicting_flags(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_file_paths(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_numeric_ranges(flags: Dict[str, Any]) -> List[str]
```

## Fluxo de Desenvolvimento

### Fase 1: Setup e Estrutura Base (Semana 1)
- [ ] Configurar estrutura de diretórios
- [ ] Implementar setup.py e requirements.txt
- [ ] Criar modelos de dados básicos (Preset, Model)
- [ ] Implementar sistema de armazenamento JSON
- [ ] Configurar testes unitários básicos


### Modelos de Dados

#### Preset
```python
@dataclass
class Preset:
    name: str
    description: str
    operation_mode: str
    flags: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    command: str
    
    def to_dict(self) -> dict
    def from_dict(cls, data: dict) -> 'Preset'
    def validate(self) -> bool
```

#### Model
```python
@dataclass
class Model:
    name: str
    provider: str
    description: str
    recommended_for: List[str]
    is_default: bool
    supports_temperature: bool
    context_window: Optional[int]
    created_by: str
    created_at: datetime
```

### Sistema de Validação

#### ValidationRules
```python
class ValidationRules:
    @staticmethod
    def validate_provider_model_combination(provider: str, model: str) -> bool
    
    @staticmethod
    def validate_flag_dependencies(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_conflicting_flags(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_file_paths(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_numeric_ranges(flags: Dict[str, Any]) -> List[str]
```

## Fluxo de Desenvolvimento

### Fase 1: Setup e Estrutura Base (Semana 1)
- [ ] Configurar estrutura de diretórios
- [ ] Implementar setup.py e requirements.txt
- [ ] Criar modelos de dados básicos (Preset, Model)
- [ ] Implementar sistema de armazenamento JSON
- [ ] Configurar testes unitários básicos


### Modelos de Dados

#### Preset
```python
@dataclass
class Preset:
    name: str
    description: str
    operation_mode: str
    flags: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    command: str
    
    def to_dict(self) -> dict
    def from_dict(cls, data: dict) -> 'Preset'
    def validate(self) -> bool
```

#### Model
```python
@dataclass
class Model:
    name: str
    provider: str
    description: str
    recommended_for: List[str]
    is_default: bool
    supports_temperature: bool
    context_window: Optional[int]
    created_by: str
    created_at: datetime
```

### Sistema de Validação

#### ValidationRules
```python
class ValidationRules:
    @staticmethod
    def validate_provider_model_combination(provider: str, model: str) -> bool
    
    @staticmethod
    def validate_flag_dependencies(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_conflicting_flags(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_file_paths(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_numeric_ranges(flags: Dict[str, Any]) -> List[str]
```


### Modelos de Dados

#### Preset
```python
@dataclass
class Preset:
    name: str
    description: str
    operation_mode: str
    flags: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    command: str
    
    def to_dict(self) -> dict
    def from_dict(cls, data: dict) -> 'Preset'
    def validate(self) -> bool
```

#### Model
```python
@dataclass
class Model:
    name: str
    provider: str
    description: str
    recommended_for: List[str]
    is_default: bool
    supports_temperature: bool
    context_window: Optional[int]
    created_by: str
    created_at: datetime
```

### Sistema de Validação

#### ValidationRules
```python
class ValidationRules:
    @staticmethod
    def validate_provider_model_combination(provider: str, model: str) -> bool
    
    @staticmethod
    def validate_flag_dependencies(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_conflicting_flags(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_file_paths(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_numeric_ranges(flags: Dict[str, Any]) -> List[str]
```

## Fluxo de Desenvolvimento


### Sistema de Validação

#### ValidationRules
```python
class ValidationRules:
    @staticmethod
    def validate_provider_model_combination(provider: str, model: str) -> bool
    
    @staticmethod
    def validate_flag_dependencies(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_conflicting_flags(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_file_paths(flags: Dict[str, Any]) -> List[str]
    
    @staticmethod
    def validate_numeric_ranges(flags: Dict[str, Any]) -> List[str]
```

## Fluxo de Desenvolvimento

### Fase 1: Setup e Estrutura Base (Semana 1)
- [ ] Configurar estrutura de diretórios
- [ ] Implementar setup.py e requirements.txt
- [ ] Criar modelos de dados básicos (Preset, Model)
- [ ] Implementar sistema de armazenamento JSON
- [ ] Configurar testes unitários básicos

### Fase 2: Core Managers (Semana 2)
- [ ] Implementar PresetManager completo
- [ ] Implementar ModelManager completo
- [ ] Criar sistema de backup automático
- [ ] Implementar validação de dados
- [ ] Testes para managers

### Fase 3: Interface de Menu (Semana 3)
- [ ] Implementar sistema de menus principal
- [ ] Menu de seleção e execução de presets
- [ ] Menu de gerenciamento de modelos
- [ ] Sistema de navegação entre menus
- [ ] Formatação visual com Rich

### Fase 4: Configuration Wizard (Semana 4)
- [ ] Implementar wizard de configuração básico
- [ ] Sistema condicional de perguntas
- [ ] Validação em tempo real
- [ ] Preview de comandos
- [ ] Testes do wizard

### Fase 5: Command Builder (Semana 5)
- [ ] Implementar CommandBuilder
- [ ] Mapeamento completo das 47 flags
- [ ] Validação de comandos
- [ ] Geração de strings de comando
- [ ] Testes de geração de comandos


## Fluxo de Desenvolvimento

### Fase 1: Setup e Estrutura Base (Semana 1)
- [ ] Configurar estrutura de diretórios
- [ ] Implementar setup.py e requirements.txt
- [ ] Criar modelos de dados básicos (Preset, Model)
- [ ] Implementar sistema de armazenamento JSON
- [ ] Configurar testes unitários básicos

### Fase 2: Core Managers (Semana 2)
- [ ] Implementar PresetManager completo
- [ ] Implementar ModelManager completo
- [ ] Criar sistema de backup automático
- [ ] Implementar validação de dados
- [ ] Testes para managers

### Fase 3: Interface de Menu (Semana 3)
- [ ] Implementar sistema de menus principal
- [ ] Menu de seleção e execução de presets
- [ ] Menu de gerenciamento de modelos
- [ ] Sistema de navegação entre menus
- [ ] Formatação visual com Rich

### Fase 4: Configuration Wizard (Semana 4)
- [ ] Implementar wizard de configuração básico
- [ ] Sistema condicional de perguntas
- [ ] Validação em tempo real
- [ ] Preview de comandos
- [ ] Testes do wizard

### Fase 5: Command Builder (Semana 5)
- [ ] Implementar CommandBuilder
- [ ] Mapeamento completo das 47 flags
- [ ] Validação de comandos
- [ ] Geração de strings de comando
- [ ] Testes de geração de comandos

### Fase 6: Integração e Polimento (Semana 6)
- [ ] Integração completa de todos os componentes
- [ ] Testes de integração
- [ ] Polimento da interface do usuário
- [ ] Tratamento de erros robusto
- [ ] Documentação completa

### Fase 7: Distribuição (Semana 7)
- [ ] Preparar pacote para PyPI
- [ ] Testes em diferentes ambientes
- [ ] Criar documentação de usuário
- [ ] Configurar CI/CD
- [ ] Publicar primeira versão


## Fluxo de Desenvolvimento

### Fase 1: Setup e Estrutura Base (Semana 1)
- [ ] Configurar estrutura de diretórios
- [ ] Implementar setup.py e requirements.txt
- [ ] Criar modelos de dados básicos (Preset, Model)
- [ ] Implementar sistema de armazenamento JSON
- [ ] Configurar testes unitários básicos

### Fase 2: Core Managers (Semana 2)
- [ ] Implementar PresetManager completo
- [ ] Implementar ModelManager completo
- [ ] Criar sistema de backup automático
- [ ] Implementar validação de dados
- [ ] Testes para managers

### Fase 3: Interface de Menu (Semana 3)
- [ ] Implementar sistema de menus principal
- [ ] Menu de seleção e execução de presets
- [ ] Menu de gerenciamento de modelos
- [ ] Sistema de navegação entre menus
- [ ] Formatação visual com Rich

### Fase 4: Configuration Wizard (Semana 4)
- [ ] Implementar wizard de configuração básico
- [ ] Sistema condicional de perguntas
- [ ] Validação em tempo real
- [ ] Preview de comandos
- [ ] Testes do wizard

### Fase 5: Command Builder (Semana 5)
- [ ] Implementar CommandBuilder
- [ ] Mapeamento completo das 47 flags
- [ ] Validação de comandos
- [ ] Geração de strings de comando
- [ ] Testes de geração de comandos

### Fase 6: Integração e Polimento (Semana 6)
- [ ] Integração completa de todos os componentes
- [ ] Testes de integração
- [ ] Polimento da interface do usuário
- [ ] Tratamento de erros robusto
- [ ] Documentação completa

### Fase 7: Distribuição (Semana 7)
- [ ] Preparar pacote para PyPI
- [ ] Testes em diferentes ambientes
- [ ] Criar documentação de usuário
- [ ] Configurar CI/CD
- [ ] Publicar primeira versão


## Fluxo de Desenvolvimento

### Fase 1: Setup e Estrutura Base (Semana 1)
- [ ] Configurar estrutura de diretórios
- [ ] Implementar setup.py e requirements.txt
- [ ] Criar modelos de dados básicos (Preset, Model)
- [ ] Implementar sistema de armazenamento JSON
- [ ] Configurar testes unitários básicos

### Fase 2: Core Managers (Semana 2)
- [ ] Implementar PresetManager completo
- [ ] Implementar ModelManager completo
- [ ] Criar sistema de backup automático
- [ ] Implementar validação de dados
- [ ] Testes para managers

### Fase 3: Interface de Menu (Semana 3)
- [ ] Implementar sistema de menus principal
- [ ] Menu de seleção e execução de presets
- [ ] Menu de gerenciamento de modelos
- [ ] Sistema de navegação entre menus
- [ ] Formatação visual com Rich

### Fase 4: Configuration Wizard (Semana 4)
- [ ] Implementar wizard de configuração básico
- [ ] Sistema condicional de perguntas
- [ ] Validação em tempo real
- [ ] Preview de comandos
- [ ] Testes do wizard

### Fase 5: Command Builder (Semana 5)
- [ ] Implementar CommandBuilder
- [ ] Mapeamento completo das 47 flags
- [ ] Validação de comandos
- [ ] Geração de strings de comando
- [ ] Testes de geração de comandos


### Fase 6: Integração e Polimento (Semana 6)
- [ ] Integração completa de todos os componentes
- [ ] Testes de integração
- [ ] Polimento da interface do usuário
- [ ] Tratamento de erros robusto
- [ ] Documentação completa

### Fase 7: Distribuição (Semana 7)
- [ ] Preparar pacote para PyPI
- [ ] Testes em diferentes ambientes
- [ ] Criar documentação de usuário
- [ ] Configurar CI/CD
- [ ] Publicar primeira versão

## Considerações de Implementação

### Tratamento de Erros
- Validação robusta de entrada do usuário
- Mensagens de erro claras e informativas
- Recuperação graceful de falhas
- Logging detalhado para debugging

### Performance
- Carregamento lazy de dados quando possível
- Cache de modelos frequentemente acessados
- Validação eficiente de configurações
- Startup rápido da aplicação

### Usabilidade
- Interface intuitiva e consistente
- Help contextual em cada etapa
- Undo/redo para ações importantes
- Confirmações para ações destrutivas

### Manutenibilidade
- Código bem documentado
- Separação clara de responsabilidades
- Testes abrangentes
- Configuração flexível

### Extensibilidade
- Sistema de plugins para futuras extensões
- API interna bem definida
- Configuração via arquivos
- Suporte a novos providers facilmente

## Conclusão

Este plano detalha a implementação completa do ra-aid-start, um gerenciador de presets para o RA.Aid que simplifica significativamente o uso da ferramenta através de uma interface assistida e configurações pré-definidas. O sistema é projetado para ser flexível, extensível e fácil de usar, cobrindo todas as 47 flags disponíveis no RA.Aid de forma organizada e intuitiva.


### Fase 6: Integração e Polimento (Semana 6)
- [ ] Integração completa de todos os componentes
- [ ] Testes de integração
- [ ] Polimento da interface do usuário
- [ ] Tratamento de erros robusto
- [ ] Documentação completa

### Fase 7: Distribuição (Semana 7)
- [ ] Preparar pacote para PyPI
- [ ] Testes em diferentes ambientes
- [ ] Criar documentação de usuário
- [ ] Configurar CI/CD
- [ ] Publicar primeira versão

## Considerações de Implementação

### Tratamento de Erros
- Validação robusta de entrada do usuário
- Mensagens de erro claras e informativas
- Recuperação graceful de falhas
- Logging detalhado para debugging

### Performance
- Carregamento lazy de dados quando possível
- Cache de modelos frequentemente acessados
- Validação eficiente de configurações
- Startup rápido da aplicação

### Usabilidade
- Interface intuitiva e consistente
- Help contextual em cada etapa
- Undo/redo para ações importantes
- Confirmações para ações destrutivas

### Manutenibilidade
- Código bem documentado
- Separação clara de responsabilidades
- Testes abrangentes
- Configuração flexível

### Extensibilidade
- Sistema de plugins para futuras extensões
- API interna bem definida
- Configuração via arquivos
- Suporte a novos providers facilmente


## Conclusão

Este plano detalha a implementação completa do ra-aid-start, um gerenciador de presets para o RA.Aid que simplifica significativamente o uso da ferramenta através de uma interface assistida e configurações pré-definidas. O sistema é projetado para ser flexível, extensível e fácil de usar, cobrindo todas as 47 flags disponíveis no RA.Aid de forma organizada e intuitiva.

O aplicativo oferece:

- **Interface Assistida**: Wizard condicional que guia o usuário através de todas as configurações necessárias
- **Gerenciamento de Modelos**: Sistema flexível para adicionar, editar e organizar modelos por provider
- **Execução Simplificada**: Seleção e execução de presets com um comando
- **Validação Robusta**: Sistema de validação que previne configurações inválidas
- **Backup Automático**: Sistema de backup e versionamento de configurações
- **Extensibilidade**: Arquitetura preparada para futuras extensões

O desenvolvimento seguirá um cronograma de 7 semanas, com fases bem definidas que garantem um produto final robusto e confiável, pronto para distribuição via PyPI.


## Sistema Completo de Menus

### Menu Principal
```
╔═══════════════════════════════════════╗
║        RA.Aid Preset Manager          ║
╚═══════════════════════════════════════╝

1. 🚀 Selecionar e Executar Preset
2. ⚙️  Configurar/Editar Preset
3. 🤖 Gerenciar Modelos
4. ❌ Sair

Escolha [1-4]: ___
```

### 1. Menu "Selecionar e Executar Preset"
```
╔═══════════════════════════════════════╗
║       SELECIONAR E EXECUTAR           ║
╚═══════════════════════════════════════╝

Presets Disponíveis:
==================
1. Desenvolvimento Web - ra-aid --provider gemini --model gemini-2.0-flash --chat --use-aider
2. Pesquisa Técnica - ra-aid --provider openai --model gpt-4o --research-only --expert-provider anthropic
3. Debug com Expert - ra-aid --provider ollama --model codellama --expert-provider openai --show-thoughts
4. Servidor Local - ra-aid --server --server-host 127.0.0.1 --server-port 3000
5. Chat Rápido - ra-aid --chat --provider anthropic --model claude-3-7-sonnet-20250219

0. ← Voltar ao menu principal

Selecione um preset (ou 0 para voltar): ___

→ Ao selecionar um preset:
  ╔═══════════════════════════════════════╗
  ║          EXECUTAR PRESET              ║
  ╚═══════════════════════════════════════╝
  
  Preset: [Nome do Preset]
  Descrição: [Descrição do preset]
  
  Comando a ser executado:
  ra-aid [flags completas...]
  
  Diretório atual: [/caminho/atual]
  
  ✅ Executar comando? [S/N]: ___
  📋 Apenas mostrar comando? [S/N]: ___
  0. ← Voltar à lista de presets
```

### 2. Menu "Configurar/Editar Preset"
```
╔═══════════════════════════════════════╗
║        GERENCIAR PRESETS              ║
╚═══════════════════════════════════════╝

1. ➕ Criar Novo Preset
2. ✏️  Editar Preset Existente
3. 🗑️  Excluir Preset
4. 📋 Visualizar Preset
5. 📥 Importar Presets
6. 📤 Exportar Presets
0. ← Voltar ao menu principal

Escolha [0-6]: ___
```

#### 2.1 Submenu "Editar Preset Existente"
```
╔═══════════════════════════════════════╗
║         EDITAR PRESET                 ║
╚═══════════════════════════════════════╝

Presets Disponíveis:
1. Desenvolvimento Web
2. Pesquisa Técnica  
3. Debug com Expert
4. Servidor Local
5. Chat Rápido

Selecione preset para editar [1-5]: ___

→ Após seleção:
  ╔═══════════════════════════════════════╗
  ║    EDITANDO: [Nome do Preset]         ║
  ╚═══════════════════════════════════════╝
  
  1. ✏️  Editar Nome e Descrição
  2. 🔧 Reconfigurar Completamente (wizard)
  3. ⚙️  Editar Configurações Específicas
  4. 🧪 Testar Preset
  5. 💾 Salvar Alterações
  6. 🗑️  Excluir Este Preset
  0. ← Voltar sem salvar
  
  Escolha [0-6]: ___
```

#### 2.2 Submenu "Visualizar Preset"
```
╔═══════════════════════════════════════╗
║        VISUALIZAR PRESET              ║
╚═══════════════════════════════════════╝

Presets Disponíveis:
1. Desenvolvimento Web
2. Pesquisa Técnica  
3. Debug com Expert
4. Servidor Local
5. Chat Rápido

Selecione preset para visualizar [1-5]: ___

→ Após seleção:
  ╔═══════════════════════════════════════╗
  ║  DETALHES: [Nome do Preset]           ║
  ╚═══════════════════════════════════════╝
  
  📋 Informações Básicas:
  Nome: [Nome]
  Descrição: [Descrição]
  Criado em: [Data]
  Modificado em: [Data]
  
  🎯 Configurações:
  Modo: [Chat/Mensagem/Arquivo/Servidor]
  Modelo Principal: [provider/model]
  Expert: [provider/model] (se configurado)
  Ferramentas: [lista de ferramentas]
  
  🚀 Comando Completo:
  ra-aid [comando completo com todas as flags]
  
  Ações:
  1. ✏️  Editar este preset
  2. 🚀 Executar este preset
  3. 📋 Copiar comando para clipboard
  0. ← Voltar
```


## Sistema Completo de Menus

### Menu Principal
```
╔═══════════════════════════════════════╗
║        RA.Aid Preset Manager          ║
╚═══════════════════════════════════════╝

1. 🚀 Selecionar e Executar Preset
2. ⚙️  Configurar/Editar Preset
3. 🤖 Gerenciar Modelos
4. ❌ Sair

Escolha [1-4]: ___
```

### 1. Menu "Selecionar e Executar Preset"
```
╔═══════════════════════════════════════╗
║       SELECIONAR E EXECUTAR           ║
╚═══════════════════════════════════════╝

Presets Disponíveis:
==================
1. Desenvolvimento Web - ra-aid --provider gemini --model gemini-2.0-flash --chat --use-aider
2. Pesquisa Técnica - ra-aid --provider openai --model gpt-4o --research-only --expert-provider anthropic
3. Debug com Expert - ra-aid --provider ollama --model codellama --expert-provider openai --show-thoughts
4. Servidor Local - ra-aid --server --server-host 127.0.0.1 --server-port 3000
5. Chat Rápido - ra-aid --chat --provider anthropic --model claude-3-7-sonnet-20250219

0. ← Voltar ao menu principal

Selecione um preset (ou 0 para voltar): ___
```

#### 1.1 Tela de Confirmação de Execução
```
╔═══════════════════════════════════════╗
║          EXECUTAR PRESET              ║
╚═══════════════════════════════════════╝

Preset: [Nome do Preset]
Descrição: [Descrição do preset]

Comando a ser executado:
ra-aid [flags completas...]

Diretório atual: [/caminho/atual]

✅ Executar comando? [S/N]: ___
📋 Apenas mostrar comando? [S/N]: ___
0. ← Voltar à lista de presets
```


## Sistema Completo de Menus

### Menu Principal
```
╔═══════════════════════════════════════╗
║        RA.Aid Preset Manager          ║
╚═══════════════════════════════════════╝

1. 🚀 Selecionar e Executar Preset
2. ⚙️  Configurar/Editar Preset
3. 🤖 Gerenciar Modelos
4. ❌ Sair

Escolha [1-4]: ___
```

### 1. Menu "Selecionar e Executar Preset"
```
╔═══════════════════════════════════════╗
║       SELECIONAR E EXECUTAR           ║
╚═══════════════════════════════════════╝

Presets Disponíveis:
==================
1. Desenvolvimento Web - ra-aid --provider gemini --model gemini-2.0-flash --chat --use-aider
2. Pesquisa Técnica - ra-aid --provider openai --model gpt-4o --research-only --expert-provider anthropic
3. Debug com Expert - ra-aid --provider ollama --model codellama --expert-provider openai --show-thoughts
4. Servidor Local - ra-aid --server --server-host 127.0.0.1 --server-port 3000
5. Chat Rápido - ra-aid --chat --provider anthropic --model claude-3-7-sonnet-20250219

0. ← Voltar ao menu principal

Selecione um preset (ou 0 para voltar): ___
```

#### 1.1 Tela de Confirmação de Execução
```
╔═══════════════════════════════════════╗
║          EXECUTAR PRESET              ║
╚═══════════════════════════════════════╝

Preset: [Nome do Preset]
Descrição: [Descrição do preset]

Comando a ser executado:
ra-aid [flags completas...]

Diretório atual: [/caminho/atual]

✅ Executar comando? [S/N]: ___
📋 Apenas mostrar comando? [S/N]: ___
0. ← Voltar à lista de presets
```


## Sistema Completo de Menus

### Menu Principal
```
╔═══════════════════════════════════════╗
║        RA.Aid Preset Manager          ║
╚═══════════════════════════════════════╝

1. 🚀 Selecionar e Executar Preset
2. ⚙️  Configurar/Editar Preset
3. 🤖 Gerenciar Modelos
4. ❌ Sair

Escolha [1-4]: ___
```

### 1. Menu "Selecionar e Executar Preset"
```
╔═══════════════════════════════════════╗
║       SELECIONAR E EXECUTAR           ║
╚═══════════════════════════════════════╝

Presets Disponíveis:
==================
1. Desenvolvimento Web - ra-aid --provider gemini --model gemini-2.0-flash --chat --use-aider
2. Pesquisa Técnica - ra-aid --provider openai --model gpt-4o --research-only --expert-provider anthropic
3. Debug com Expert - ra-aid --provider ollama --model codellama --expert-provider openai --show-thoughts
4. Servidor Local - ra-aid --server --server-host 127.0.0.1 --server-port 3000
5. Chat Rápido - ra-aid --chat --provider anthropic --model claude-3-7-sonnet-20250219

0. ← Voltar ao menu principal

Selecione um preset (ou 0 para voltar): ___
```


#### 1.1 Tela de Confirmação de Execução
```
╔═══════════════════════════════════════╗
║          EXECUTAR PRESET              ║
╚═══════════════════════════════════════╝

Preset: [Nome do Preset]
Descrição: [Descrição do preset]

Comando a ser executado:
ra-aid [flags completas...]

Diretório atual: [/caminho/atual]

✅ Executar comando? [S/N]: ___
📋 Apenas mostrar comando? [S/N]: ___
0. ← Voltar à lista de presets
```

### 2. Menu "Configurar/Editar Preset"
```
╔═══════════════════════════════════════╗
║        GERENCIAR PRESETS              ║
╚═══════════════════════════════════════╝

1. ➕ Criar Novo Preset
2. ✏️  Editar Preset Existente
3. 🗑️  Excluir Preset
4. 📋 Visualizar Preset
5. 📥 Importar Presets
6. 📤 Exportar Presets
0. ← Voltar ao menu principal

Escolha [0-6]: ___
```

#### 2.1 Submenu "Editar Preset Existente"
```
╔═══════════════════════════════════════╗
║         EDITAR PRESET                 ║
╚═══════════════════════════════════════╝

Presets Disponíveis:
1. Desenvolvimento Web
2. Pesquisa Técnica  
3. Debug com Expert
4. Servidor Local
5. Chat Rápido

Selecione preset para editar [1-5]: ___
```


#### 1.1 Tela de Confirmação de Execução
```
╔═══════════════════════════════════════╗
║          EXECUTAR PRESET              ║
╚═══════════════════════════════════════╝

Preset: [Nome do Preset]
Descrição: [Descrição do preset]

Comando a ser executado:
ra-aid [flags completas...]

Diretório atual: [/caminho/atual]

✅ Executar comando? [S/N]: ___
📋 Apenas mostrar comando? [S/N]: ___
0. ← Voltar à lista de presets
```

### 2. Menu "Configurar/Editar Preset"
```
╔═══════════════════════════════════════╗
║        GERENCIAR PRESETS              ║
╚═══════════════════════════════════════╝

1. ➕ Criar Novo Preset
2. ✏️  Editar Preset Existente
3. 🗑️  Excluir Preset
4. 📋 Visualizar Preset
5. 📥 Importar Presets
6. 📤 Exportar Presets
0. ← Voltar ao menu principal

Escolha [0-6]: ___
```

#### 2.1 Submenu "Editar Preset Existente"
```
╔═══════════════════════════════════════╗
║         EDITAR PRESET                 ║
╚═══════════════════════════════════════╝

Presets Disponíveis:
1. Desenvolvimento Web
2. Pesquisa Técnica  
3. Debug com Expert
4. Servidor Local
5. Chat Rápido

Selecione preset para editar [1-5]: ___
```


#### 1.1 Tela de Confirmação de Execução
```
╔═══════════════════════════════════════╗
║          EXECUTAR PRESET              ║
╚═══════════════════════════════════════╝

Preset: [Nome do Preset]
Descrição: [Descrição do preset]

Comando a ser executado:
ra-aid [flags completas...]

Diretório atual: [/caminho/atual]

✅ Executar comando? [S/N]: ___
📋 Apenas mostrar comando? [S/N]: ___
0. ← Voltar à lista de presets
```

### 2. Menu "Configurar/Editar Preset"
```
╔═══════════════════════════════════════╗
║        GERENCIAR PRESETS              ║
╚═══════════════════════════════════════╝

1. ➕ Criar Novo Preset
2. ✏️  Editar Preset Existente
3. 🗑️  Excluir Preset
4. 📋 Visualizar Preset
5. 📥 Importar Presets
6. 📤 Exportar Presets
0. ← Voltar ao menu principal

Escolha [0-6]: ___
```


#### 2.1 Submenu "Editar Preset Existente"
```
╔═══════════════════════════════════════╗
║         EDITAR PRESET                 ║
╚═══════════════════════════════════════╝

Presets Disponíveis:
1. Desenvolvimento Web
2. Pesquisa Técnica  
3. Debug com Expert
4. Servidor Local
5. Chat Rápido

Selecione preset para editar [1-5]: ___

→ Após seleção:
  ╔═══════════════════════════════════════╗
  ║    EDITANDO: [Nome do Preset]         ║
  ╚═══════════════════════════════════════╝
  
  1. ✏️  Editar Nome e Descrição
  2. 🔧 Reconfigurar Completamente (wizard)
  3. ⚙️  Editar Configurações Específicas
  4. 🧪 Testar Preset
  5. 💾 Salvar Alterações
  6. 🗑️  Excluir Este Preset
  0. ← Voltar sem salvar
  
  Escolha [0-6]: ___
```

#### 2.2 Submenu "Visualizar Preset"
```
╔═══════════════════════════════════════╗
║        VISUALIZAR PRESET              ║
╚═══════════════════════════════════════╝

Presets Disponíveis:
1. Desenvolvimento Web
2. Pesquisa Técnica  
3. Debug com Expert
4. Servidor Local
5. Chat Rápido

Selecione preset para visualizar [1-5]: ___
```


#### 2.3 Tela de Detalhes do Preset
```
╔═══════════════════════════════════════╗
║  DETALHES: [Nome do Preset]           ║
╚═══════════════════════════════════════╝

📋 Informações Básicas:
Nome: [Nome]
Descrição: [Descrição]
Criado em: [Data]
Modificado em: [Data]

🎯 Configurações:
Modo: [Chat/Mensagem/Arquivo/Servidor]
Modelo Principal: [provider/model]
Expert: [provider/model] (se configurado)
Ferramentas: [lista de ferramentas]

🚀 Comando Completo:
ra-aid [comando completo com todas as flags]

Ações:
1. ✏️  Editar este preset
2. 🚀 Executar este preset
3. 📋 Copiar comando para clipboard
0. ← Voltar
```

#### 2.4 Submenu "Importar/Exportar Presets"
```
╔═══════════════════════════════════════╗
║       IMPORTAR/EXPORTAR PRESETS       ║
╚═══════════════════════════════════════╝

📥 IMPORTAR:
1. 📄 Importar de arquivo JSON
2. 📋 Importar de texto (lista simples)
3. 🔗 Importar de URL

📤 EXPORTAR:
4. 💾 Exportar todos os presets
5. 📋 Exportar preset específico
6. 📄 Exportar como texto simples

0. ← Voltar

→ SE IMPORTAR DE ARQUIVO JSON:
  Caminho do arquivo: _______________
  
  Ação em caso de conflito:
  1. 🔄 Substituir presets existentes
  2. ➕ Adicionar apenas novos
  3. ❓ Perguntar para cada conflito
```


#### 2.3 Tela de Detalhes do Preset
```
╔═══════════════════════════════════════╗
║  DETALHES: [Nome do Preset]           ║
╚═══════════════════════════════════════╝

📋 Informações Básicas:
Nome: [Nome]
Descrição: [Descrição]
Criado em: [Data]
Modificado em: [Data]

🎯 Configurações:
Modo: [Chat/Mensagem/Arquivo/Servidor]
Modelo Principal: [provider/model]
Expert: [provider/model] (se configurado)
Ferramentas: [lista de ferramentas]

🚀 Comando Completo:
ra-aid [comando completo com todas as flags]

Ações:
1. ✏️  Editar este preset
2. 🚀 Executar este preset
3. 📋 Copiar comando para clipboard
0. ← Voltar
```

#### 2.4 Submenu "Importar/Exportar Presets"
```
╔═══════════════════════════════════════╗
║       IMPORTAR/EXPORTAR PRESETS       ║
╚═══════════════════════════════════════╝

📥 IMPORTAR:
1. 📄 Importar de arquivo JSON
2. 📋 Importar de texto (lista simples)
3. 🔗 Importar de URL

📤 EXPORTAR:
4. 💾 Exportar todos os presets
5. 📋 Exportar preset específico
6. 📄 Exportar como texto simples

0. ← Voltar
```


### 3. Menu "Gerenciar Modelos"
```
╔═══════════════════════════════════════╗
║        GERENCIAR MODELOS              ║
╚═══════════════════════════════════════╝

1. 📋 Visualizar Modelos por Provider
2. ➕ Adicionar Novo Modelo
3. ✏️  Editar Modelo Existente
4. 🗑️  Remover Modelo
5. 📥 Importar Lista de Modelos
6. 📤 Exportar Lista de Modelos
7. 🔄 Restaurar Modelos Padrão
0. ← Voltar ao menu principal

Escolha [0-7]: ___
```

#### 3.1 Submenu "Visualizar Modelos por Provider"
```
╔═══════════════════════════════════════╗
║      VISUALIZAR MODELOS               ║
╚═══════════════════════════════════════╝

Escolha o provider para visualizar:
1. 🤖 OpenAI
2. 🧠 Anthropic Claude
3. ⚡ Google Gemini
4. 🏠 Ollama
5. 🔀 OpenRouter
6. 💎 DeepSeek
7. 🚀 Fireworks
8. 🔧 OpenAI-Compatible
9. 👁️  Ver todos os providers
0. ← Voltar

→ SE ESCOLHER UM PROVIDER (ex: OpenAI):
  
  ╔═══════════════════════════════════════╗
  ║         MODELOS - OPENAI              ║
  ╚═══════════════════════════════════════╝
  
  📋 Modelos cadastrados:
  1. gpt-4o (GPT-4 Omni - recomendado para uso geral)
  2. gpt-4o-mini (versão mais rápida e econômica)
  3. gpt-4 (GPT-4 clássico)
  4. o1 (raciocínio avançado - mais lento mas mais preciso)
  5. o1-mini (raciocínio rápido)
  6. gpt-3.5-turbo (modelo legado)
  
  Ações:
  A. ➕ Adicionar novo modelo
  E. ✏️  Editar modelo selecionado
  R. 🗑️  Remover modelo selecionado
  0. ← Voltar
```


### 3. Menu "Gerenciar Modelos"
```
╔═══════════════════════════════════════╗
║        GERENCIAR MODELOS              ║
╚═══════════════════════════════════════╝

1. 📋 Visualizar Modelos por Provider
2. ➕ Adicionar Novo Modelo
3. ✏️  Editar Modelo Existente
4. 🗑️  Remover Modelo
5. 📥 Importar Lista de Modelos
6. 📤 Exportar Lista de Modelos
7. 🔄 Restaurar Modelos Padrão
0. ← Voltar ao menu principal

Escolha [0-7]: ___
```

#### 3.1 Submenu "Visualizar Modelos por Provider"
```
╔═══════════════════════════════════════╗
║      VISUALIZAR MODELOS               ║
╚═══════════════════════════════════════╝

Escolha o provider para visualizar:
1. 🤖 OpenAI
2. 🧠 Anthropic Claude
3. ⚡ Google Gemini
4. 🏠 Ollama
5. 🔀 OpenRouter
6. 💎 DeepSeek
7. 🚀 Fireworks
8. 🔧 OpenAI-Compatible
9. 👁️  Ver todos os providers
0. ← Voltar
```


#### 3.2 Tela de Modelos Específicos por Provider
```
╔═══════════════════════════════════════╗
║         MODELOS - OPENAI              ║
╚═══════════════════════════════════════╝

📋 Modelos cadastrados:
1. gpt-4o (GPT-4 Omni - recomendado para uso geral)
2. gpt-4o-mini (versão mais rápida e econômica)
3. gpt-4 (GPT-4 clássico)
4. o1 (raciocínio avançado - mais lento mas mais preciso)
5. o1-mini (raciocínio rápido)
6. gpt-3.5-turbo (modelo legado)
7. custom-model-user (Modelo personalizado - criado pelo usuário)

Ações:
A. ➕ Adicionar novo modelo
E. ✏️  Editar modelo selecionado (digite número + E, ex: 3E)
R. 🗑️  Remover modelo selecionado (digite número + R, ex: 7R)
0. ← Voltar
```

#### 3.3 Submenu "Adicionar Novo Modelo"
```
╔═══════════════════════════════════════╗
║        ADICIONAR NOVO MODELO          ║
╚═══════════════════════════════════════╝

Escolha o provider:
1. 🤖 OpenAI
2. 🧠 Anthropic Claude
3. ⚡ Google Gemini
4. 🏠 Ollama
5. 🔀 OpenRouter
6. 💎 DeepSeek
7. 🚀 Fireworks
8. 🔧 OpenAI-Compatible

Provider escolhido: [X]

📝 Informações do Modelo:
Nome do modelo: _______________
Descrição (opcional): _______________
Recomendado para: _______________
  (ex: "uso geral", "programação", "raciocínio", "velocidade")

Configurações específicas:
→ SE Ollama:
  Suporte a contexto customizado (--num-ctx)? [S/N]: ___
  
→ SE OpenAI-Compatible:
  Requer endpoint customizado? [S/N]: ___

✅ Salvar modelo? [S/N]: ___
```

#### 3.4 Submenu "Editar Modelo Existente"
```
╔═══════════════════════════════════════╗
║         EDITAR MODELO                 ║
╚═══════════════════════════════════════╝

Provider: [OpenAI]
Modelo selecionado: [gpt-4o]

📝 Informações atuais:
Nome: gpt-4o
Descrição: GPT-4 Omni - recomendado para uso geral
Recomendado para: uso geral

Campos editáveis:
1. ✏️  Descrição: _______________
2. 🎯 Recomendado para: _______________
3. 🗑️  Remover este modelo
0. ← Cancelar edição

Escolha [0-3]: ___
```


#### 3.2 Tela de Modelos Específicos por Provider
```
╔═══════════════════════════════════════╗
║         MODELOS - OPENAI              ║
╚═══════════════════════════════════════╝

📋 Modelos cadastrados:
1. gpt-4o (GPT-4 Omni - recomendado para uso geral)
2. gpt-4o-mini (versão mais rápida e econômica)
3. gpt-4 (GPT-4 clássico)
4. o1 (raciocínio avançado - mais lento mas mais preciso)
5. o1-mini (raciocínio rápido)
6. gpt-3.5-turbo (modelo legado)
7. custom-model-user (Modelo personalizado - criado pelo usuário)

Ações:
A. ➕ Adicionar novo modelo
E. ✏️  Editar modelo selecionado (digite número + E, ex: 3E)
R. 🗑️  Remover modelo selecionado (digite número + R, ex: 7R)
0. ← Voltar
```

#### 3.3 Submenu "Adicionar Novo Modelo"
```
╔═══════════════════════════════════════╗
║        ADICIONAR NOVO MODELO          ║
╚═══════════════════════════════════════╝

Escolha o provider:
1. 🤖 OpenAI
2. 🧠 Anthropic Claude
3. ⚡ Google Gemini
4. 🏠 Ollama
5. 🔀 OpenRouter
6. 💎 DeepSeek
7. 🚀 Fireworks
8. 🔧 OpenAI-Compatible

Provider escolhido: [X]

📝 Informações do Modelo:
Nome do modelo: _______________
Descrição (opcional): _______________
Recomendado para: _______________
  (ex: "uso geral", "programação", "raciocínio", "velocidade")

Configurações específicas:
→ SE Ollama:
  Suporte a contexto customizado (--num-ctx)? [S/N]: ___
  
→ SE OpenAI-Compatible:
  Requer endpoint customizado? [S/N]: ___

✅ Salvar modelo? [S/N]: ___
```


#### 3.3 Submenu "Adicionar Novo Modelo"
```
╔═══════════════════════════════════════╗
║        ADICIONAR NOVO MODELO          ║
╚═══════════════════════════════════════╝

Escolha o provider:
1. 🤖 OpenAI
2. 🧠 Anthropic Claude
3. ⚡ Google Gemini
4. 🏠 Ollama
5. 🔀 OpenRouter
6. 💎 DeepSeek
7. 🚀 Fireworks
8. 🔧 OpenAI-Compatible

Provider escolhido: [X]

📝 Informações do Modelo:
Nome do modelo: _______________
Descrição (opcional): _______________
Recomendado para: _______________
  (ex: "uso geral", "programação", "raciocínio", "velocidade")

Configurações específicas:
→ SE Ollama:
  Suporte a contexto customizado (--num-ctx)? [S/N]: ___
  
→ SE OpenAI-Compatible:
  Requer endpoint customizado? [S/N]: ___

✅ Salvar modelo? [S/N]: ___
```

#### 3.4 Submenu "Editar Modelo Existente"
```
╔═══════════════════════════════════════╗
║         EDITAR MODELO                 ║
╚═══════════════════════════════════════╝

Provider: [OpenAI]
Modelo selecionado: [gpt-4o]

📝 Informações atuais:
Nome: gpt-4o
Descrição: GPT-4 Omni - recomendado para uso geral
Recomendado para: uso geral

Campos editáveis:
1. ✏️  Descrição: _______________
2. 🎯 Recomendado para: _______________
3. 🗑️  Remover este modelo
0. ← Cancelar edição

Escolha [0-3]: ___
```


#### 3.4 Submenu "Editar Modelo Existente"
```
╔═══════════════════════════════════════╗
║         EDITAR MODELO                 ║
╚═══════════════════════════════════════╝

Provider: [OpenAI]
Modelo selecionado: [gpt-4o]

📝 Informações atuais:
Nome: gpt-4o
Descrição: GPT-4 Omni - recomendado para uso geral
Recomendado para: uso geral

Campos editáveis:
1. ✏️  Descrição: _______________
2. 🎯 Recomendado para: _______________
3. 🗑️  Remover este modelo
0. ← Cancelar edição

Escolha [0-3]: ___
```

#### 3.5 Submenu "Importar/Exportar Modelos"
```
╔═══════════════════════════════════════╗
║       IMPORTAR/EXPORTAR MODELOS       ║
╚═══════════════════════════════════════╝

📥 IMPORTAR:
1. 📄 Importar de arquivo JSON
2. 🌐 Buscar modelos online (futuro)
3. 📋 Importar de texto (lista simples)

📤 EXPORTAR:
4. 💾 Exportar todos os modelos
5. 📋 Exportar provider específico
6. 📄 Exportar como texto simples

0. ← Voltar

→ SE IMPORTAR DE ARQUIVO JSON:
  Caminho do arquivo: _______________
  
  Ação em caso de conflito:
  1. 🔄 Substituir modelos existentes
  2. ➕ Adicionar apenas novos
  3. ❓ Perguntar para cada conflito
  
→ SE IMPORTAR DE TEXTO:
  Cole a lista de modelos (um por linha):
  _______________
  _______________
  _______________
  [Enter para terminar]
  
  Provider de destino:
  [Lista de providers 1-8]
```


#### 3.5 Submenu "Importar/Exportar Modelos"
```
╔═══════════════════════════════════════╗
║       IMPORTAR/EXPORTAR MODELOS       ║
╚═══════════════════════════════════════╝

📥 IMPORTAR:
1. 📄 Importar de arquivo JSON
2. 🌐 Buscar modelos online (futuro)
3. 📋 Importar de texto (lista simples)

📤 EXPORTAR:
4. 💾 Exportar todos os modelos
5. 📋 Exportar provider específico
6. 📄 Exportar como texto simples

0. ← Voltar
```

#### 3.6 Tela de Importação de Modelos
```
→ SE IMPORTAR DE ARQUIVO JSON:
  Caminho do arquivo: _______________
  
  Ação em caso de conflito:
  1. 🔄 Substituir modelos existentes
  2. ➕ Adicionar apenas novos
  3. ❓ Perguntar para cada conflito
  
→ SE IMPORTAR DE TEXTO:
  Cole a lista de modelos (um por linha):
  _______________
  _______________
  _______________
  [Enter para terminar]
  
  Provider de destino:
  [Lista de providers 1-8]
```

#### 3.7 Submenu "Restaurar Padrões"
```
╔═══════════════════════════════════════╗
║        RESTAURAR PADRÕES              ║
╚═══════════════════════════════════════╝

⚠️  ATENÇÃO: Esta ação irá:
- Restaurar a lista padrão de modelos para todos os providers
- Manter modelos personalizados adicionados pelo usuário
- Sobrescrever descrições modificadas dos modelos padrão

Escolha o escopo:
1. 🔄 Restaurar todos os providers
2. 🎯 Restaurar provider específico
3. ➕ Adicionar apenas modelos padrão faltantes
0. ← Cancelar

→ SE PROVIDER ESPECÍFICO:
  Escolha o provider para restaurar:
  [Lista de providers 1-8]

⚠️  Confirmar restauração? [S/N]: ___
```


#### 3.6 Submenu "Restaurar Padrões"
```
╔═══════════════════════════════════════╗
║        RESTAURAR PADRÕES              ║
╚═══════════════════════════════════════╝

⚠️  ATENÇÃO: Esta ação irá:
- Restaurar a lista padrão de modelos para todos os providers
- Manter modelos personalizados adicionados pelo usuário
- Sobrescrever descrições modificadas dos modelos padrão

Escolha o escopo:
1. 🔄 Restaurar todos os providers
2. 🎯 Restaurar provider específico
3. ➕ Adicionar apenas modelos padrão faltantes
0. ← Cancelar

→ SE PROVIDER ESPECÍFICO:
  Escolha o provider para restaurar:
  [Lista de providers 1-8]

⚠️  Confirmar restauração? [S/N]: ___
```

## Wizard de Configuração Assistida - Menus Condicionais

### Início do Wizard
```
╔═══════════════════════════════════════╗
║        NOVO PRESET RA.AID             ║
╚═══════════════════════════════════════╝

Nome do Preset: ___________
Descrição (opcional): ___________

Pressione ENTER para continuar...
```

### Tela 1: Modo de Entrada de Dados
```
╔═══════════════════════════════════════╗
║      MODO DE ENTRADA DE DADOS         ║
╚═══════════════════════════════════════╝

Como será fornecida a informação para o RA.Aid?

1. 💬 Chat Interativo (--chat)
2. 📝 Mensagem/Tarefa (-m / --message)  
3. 📄 Arquivo de Texto (--msg-file)
4. 🌐 Servidor Web (--server)

Escolha [1-4]: ___

ℹ️  Dica: Chat é ideal para interação contínua, Mensagem para tarefas únicas
```


## Wizard de Configuração Assistida - Menus Condicionais

### Início do Wizard
```
╔═══════════════════════════════════════╗
║        NOVO PRESET RA.AID             ║
╚═══════════════════════════════════════╝

Nome do Preset: ___________
Descrição (opcional): ___________

Pressione ENTER para continuar...
```

### Tela 1: Modo de Entrada de Dados
```
╔═══════════════════════════════════════╗
║      MODO DE ENTRADA DE DADOS         ║
╚═══════════════════════════════════════╝

Como será fornecida a informação para o RA.Aid?

1. 💬 Chat Interativo (--chat)
2. 📝 Mensagem/Tarefa (-m / --message)  
3. 📄 Arquivo de Texto (--msg-file)
4. 🌐 Servidor Web (--server)

Escolha [1-4]: ___

ℹ️  Dica: Chat é ideal para interação contínua, Mensagem para tarefas únicas
```

### Tela 2A: Configuração Chat (se escolheu --chat)
```
╔═══════════════════════════════════════╗
║           MODO CHAT                   ║
║              (--chat)                 ║
╚═══════════════════════════════════════╝

✅ Configurações automáticas:
- Human-in-the-loop será habilitado automaticamente (--hil)
- Mensagem será solicitada durante a execução
- Research-only NÃO está disponível neste modo

⚠️  AVISO: --research-only não é compatível com modo chat

Configurações de Chat:
- 🏇 Modo Cowboy - sem confirmações de comandos (--cowboy-mode)? [S/N]: ___

ℹ️  Cowboy Mode: Executa comandos sem pedir confirmação (use com cuidado!)

Pressione ENTER para continuar...
```


### Tela 2A: Configuração Chat (se escolheu --chat)
```
╔═══════════════════════════════════════╗
║           MODO CHAT                   ║
║              (--chat)                 ║
╚═══════════════════════════════════════╝

✅ Configurações automáticas:
- Human-in-the-loop será habilitado automaticamente (--hil)
- Mensagem será solicitada durante a execução
- Research-only NÃO está disponível neste modo

⚠️  AVISO: --research-only não é compatível com modo chat

Configurações de Chat:
- 🏇 Modo Cowboy - sem confirmações de comandos (--cowboy-mode)? [S/N]: ___

ℹ️  Cowboy Mode: Executa comandos sem pedir confirmação (use com cuidado!)

Pressione ENTER para continuar...
```

### Tela 2B: Configuração Mensagem (se escolheu -m)
```
╔═══════════════════════════════════════╗
║         MODO MENSAGEM/TAREFA          ║
║           (-m / --message)            ║
╚═══════════════════════════════════════╝

Tipo de Operação:
1. 🔍 Apenas Pesquisa (--research-only)
2. 🛠️  Pesquisa + Implementação (padrão)

Escolha [1-2]: ___

→ SE APENAS PESQUISA (--research-only):
  ✅ Modo research-only ativado
  - Não fará implementação de código
  - Focará apenas em análise e pesquisa

→ SE PESQUISA + IMPLEMENTAÇÃO:
  Configurações de Execução:
  - 🤝 Human-in-the-loop (--hil / -H)? [S/N]: ___
  - 🏇 Modo Cowboy - sem confirmações (--cowboy-mode)? [S/N]: ___

Como será fornecida a mensagem/tarefa?
1. 📝 Digitar sempre na execução (usuário fornece via -m)
2. ⚡ Incluir mensagem fixa no preset

→ SE INCLUIR MENSAGEM FIXA:
  Mensagem/Tarefa para (-m): ___________________________

Pressione ENTER para continuar...
```


### Tela 2B: Configuração Mensagem (se escolheu -m)
```
╔═══════════════════════════════════════╗
║         MODO MENSAGEM/TAREFA          ║
║           (-m / --message)            ║
╚═══════════════════════════════════════╝

Tipo de Operação:
1. 🔍 Apenas Pesquisa (--research-only)
2. 🛠️  Pesquisa + Implementação (padrão)

Escolha [1-2]: ___

→ SE APENAS PESQUISA (--research-only):
  ✅ Modo research-only ativado
  - Não fará implementação de código
  - Focará apenas em análise e pesquisa

→ SE PESQUISA + IMPLEMENTAÇÃO:
  Configurações de Execução:
  - 🤝 Human-in-the-loop (--hil / -H)? [S/N]: ___
  - 🏇 Modo Cowboy - sem confirmações (--cowboy-mode)? [S/N]: ___

Como será fornecida a mensagem/tarefa?
1. 📝 Digitar sempre na execução (usuário fornece via -m)
2. ⚡ Incluir mensagem fixa no preset

→ SE INCLUIR MENSAGEM FIXA:
  Mensagem/Tarefa para (-m): ___________________________

Pressione ENTER para continuar...
```

### Tela 2C: Configuração Arquivo (se escolheu --msg-file)
```
╔═══════════════════════════════════════╗
║         MODO ARQUIVO DE TEXTO         ║
║            (--msg-file)               ║
╚═══════════════════════════════════════╝

Tipo de Operação:
1. 🔍 Apenas Pesquisa (--research-only)
2. 🛠️  Pesquisa + Implementação (padrão)

Escolha [1-2]: ___

→ SE APENAS PESQUISA (--research-only):
  ✅ Modo research-only ativado

→ SE PESQUISA + IMPLEMENTAÇÃO:
  Configurações de Execução:
  - 🤝 Human-in-the-loop (--hil / -H)? [S/N]: ___
  - 🏇 Modo Cowboy - sem confirmações (--cowboy-mode)? [S/N]: ___

Configuração do Arquivo:
1. 📄 Solicitar caminho na execução (usuário fornece --msg-file)
2. 📁 Definir caminho fixo no preset

→ SE CAMINHO FIXO:
  Caminho do arquivo para (--msg-file): ___________________________

Pressione ENTER para continuar...
```


## Resumo dos Menus Implementados

### Estrutura Completa de Navegação

1. **Menu Principal**: Ponto de entrada com 4 opções principais
2. **Sistema de Execução**: Lista, preview e execução de presets
3. **Sistema de Gerenciamento**: CRUD completo de presets com import/export
4. **Sistema de Modelos**: Gerenciamento flexível de modelos por provider
5. **Wizard Condicional**: Configuração assistida com fluxos condicionais
6. **Validação em Tempo Real**: Sistema integrado de validação
7. **Sistema de Backup**: Controle de versões e restauração

### Características dos Menus

- **Interface Consistente**: Uso de Rich para formatação visual
- **Navegação Intuitiva**: Sistema de numeração e teclas de atalho
- **Feedback Visual**: Emojis e cores para melhor UX
- **Validação**: Verificação em tempo real das entradas
- **Help Contextual**: Dicas e explicações em cada etapa
- **Confirmações**: Proteção contra ações destrutivas
- **Flexibilidade**: Suporte a diferentes fluxos de trabalho

### Total de Telas/Menus Projetados

- **Menu Principal**: 1 tela
- **Sistema de Execução**: 2 telas
- **Sistema de Presets**: 6 telas
- **Sistema de Modelos**: 8 telas  
- **Wizard de Configuração**: 11+ telas condicionais
- **Telas de Confirmação**: 5+ telas
- **Telas de Erro/Help**: 3+ telas

**Total: 35+ interfaces diferentes** com navegação completa e fluxos condicionais implementados.

O sistema de menus está projetado para cobrir todos os casos de uso identificados, desde a execução simples de presets até a configuração avançada de todas as 47 flags do RA.Aid, mantendo sempre a usabilidade e clareza para o usuário final.
