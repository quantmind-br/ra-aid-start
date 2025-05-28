# Diretrizes de Desenvolvimento para IA - Projeto ra-aid-start

## 1. Visão Geral do Projeto

-   **Propósito:** `ra-aid-start` é uma CLI Python para criar e executar presets assistidos para a aplicação Ra.Aid.
-   **Pilha Tecnológica:** Python, Click, Rich, Pydantic, jsonschema, pathlib, typing-extensions.
-   **Funcionalidades Centrais:**
    -   Gerenciamento de presets (criar, editar, listar, excluir, executar).
    -   Interface de usuário assistida (wizard) para configuração de 47 flags.
    -   Gerenciamento de modelos LLM por provedor.
    -   Armazenamento persistente de configurações em `~/.ra-aid-start/`.

## 2. Arquitetura do Projeto

-   **Estrutura de Diretórios Principal:**
    -   `ra-aid-start/`: Raiz do projeto.
        -   `ra_aid_start/`: Código fonte principal da aplicação.
            -   `__init__.py`
            -   `__main__.py`: Ponto de entrada principal.
            -   `core/`: Lógica central da aplicação.
                -   `preset_manager.py`: Gerenciamento de presets.
                -   `model_manager.py`: Gerenciamento de modelos LLM.
                -   `config_manager.py`: Configurações globais.
                -   `command_builder.py`: Construção de comandos `ra-aid`.
            -   `ui/`: Interface com o usuário.
                -   `menu_system.py`: Sistema de menus interativos.
                -   `wizards.py`: Assistentes de configuração (wizard).
                -   `display.py`: Formatação e exibição de informações.
            -   `models/`: Modelos de dados da aplicação.
                -   `preset.py`: Modelo de dados para presets.
                -   `provider.py`: Modelo de dados para provedores LLM.
                -   `validation.py`: Lógica de validação de dados.
            -   `utils/`: Utilitários diversos.
                -   `file_handler.py`: Manipulação de arquivos.
                -   `json_handler.py`: Manipulação de JSON.
                -   `backup_manager.py`: Sistema de backup.
            -   `data/`: Dados padrão e schemas.
                -   `default_models.py`: Modelos LLM padrão por provedor.
                -   `schemas.py`: Schemas de validação JSON.
        -   `tests/`: Testes unitários.
            -   `test_preset_manager.py`
            -   `test_model_manager.py`
            -   `test_wizards.py`
        -   `setup.py`: Script de instalação.
        -   `requirements.txt`: Dependências do projeto.
        -   `README.md`: Documentação principal.
        -   `LICENSE`: Licença do projeto.
        -   `PLAN.MD`: Plano de desenvolvimento (este arquivo).
-   **Armazenamento de Dados do Usuário:** `~/.ra-aid-start/`
    -   `presets/`: Arquivos JSON de presets.
    -   `models/`: Arquivos JSON de modelos LLM por provedor.
    -   `config.json`: Configurações globais do `ra-aid-start`.
    -   `backups/`: Backups de presets e modelos.

## 3. Padrões de Código

-   **Nomenclatura:**
    -   Classes: `CamelCase` (ex: `PresetManager`).
    -   Funções/Métodos: `snake_case` (ex: `load_preset`).
    -   Arquivos/Módulos: `snake_case` (ex: `preset_manager.py`).
    -   Constantes: `UPPER_SNAKE_CASE` (ex: `DEFAULT_PROVIDER`).
-   **Comentários:**
    -   **OBRIGATÓRIO:** Usar docstrings (Google Style) para todas as classes, métodos e funções públicas.
    -   **OBRIGATÓRIO:** Comentar blocos de lógica complexa ou não óbvia.
-   **Formatação:**
    -   **OBRIGATÓRIO:** Seguir rigorosamente o PEP 8. Usar um formatador como Black ou Ruff.
    -   Limite de linha: 88 caracteres (padrão Black).
-   **Tipagem:**
    -   **OBRIGATÓRIO:** Usar type hints (PEP 484) em todas as definições de função, método e variáveis onde aplicável.
    -   **OBRIGATÓRIO:** Utilizar `typing-extensions` para type hints avançados se necessário.
    -   Referenciar [`PLAN.MD:658`](PLAN.MD:658).
-   **Imports:**
    -   Organizar imports em três seções: bibliotecas padrão, bibliotecas de terceiros, módulos locais.
    -   Ordenar alfabeticamente dentro de cada seção.

## 4. Padrões de Implementação de Funcionalidade

-   **Novas Flags do RA.Aid:**
    -   **OBRIGATÓRIO:** Adicionar a nova flag ao [`CommandBuilder`](PLAN.MD:974) ([`ra_aid_start/core/command_builder.py`](ra_aid_start/core/command_builder.py)).
    -   **OBRIGATÓRIO:** Incluir a configuração da nova flag no [`ConfigurationWizard`](PLAN.MD:959) ([`ra_aid_start/ui/wizards.py`](ra_aid_start/ui/wizards.py)).
    -   **OBRIGATÓRIO:** Se a flag for armazenada no preset, atualizar o modelo [`Preset`](PLAN.MD:986) ([`ra_aid_start/models/preset.py`](ra_aid_start/models/preset.py)).
    -   **OBRIGATÓRIO:** Referenciar o mapeamento de flags em [`PLAN.MD:403-645`](PLAN.MD:403) para consistência.
-   **Novos Menus ou Elementos de UI:**
    -   **OBRIGATÓRIO:** Seguir o design e a estrutura de menus detalhados em [`PLAN.MD:1680-2910`](PLAN.MD:1680).
    -   **OBRIGATÓRIO:** Utilizar a biblioteca `rich` para toda a saída e interações no terminal. Ver [`PLAN.MD:653`](PLAN.MD:653).
    -   Integrar novas telas em [`ra_aid_start/ui/menu_system.py`](ra_aid_start/ui/menu_system.py) ou [`ra_aid_start/ui/wizards.py`](ra_aid_start/ui/wizards.py) conforme apropriado.
-   **Gerenciamento de Dados (Presets e Modelos):**
    -   **OBRIGATÓRIO:** Todas as operações de CRUD para presets devem usar [`PresetManager`](PLAN.MD:665) ([`ra_aid_start/core/preset_manager.py`](ra_aid_start/core/preset_manager.py)).
    -   **OBRIGATÓRIO:** Todas as operações de CRUD para modelos LLM devem usar [`ModelManager`](PLAN.MD:677) ([`ra_aid_start/core/model_manager.py`](ra_aid_start/core/model_manager.py)).
    -   Os dados são armazenados em arquivos JSON no diretório `~/.ra-aid-start/`. A manipulação direta desses arquivos é **PROIBIDA**; usar sempre os Managers.
-   **Validação:**
    -   **OBRIGATÓRIO:** Utilizar `pydantic` para definir e validar modelos de dados como `Preset` e `Model`. Ver [`PLAN.MD:655`](PLAN.MD:655).
    -   **OBRIGATÓRIO:** Utilizar `jsonschema` para validação de schemas JSON, especialmente para dados importados/exportados. Ver [`PLAN.MD:656`](PLAN.MD:656) e [`ra_aid_start/data/schemas.py`](ra_aid_start/data/schemas.py).
    -   Implementar regras de validação específicas em [`ra_aid_start/models/validation.py`](ra_aid_start/models/validation.py) e referenciá-las nos managers e wizards.

## 5. Padrões de Uso de Framework/Plugin/Biblioteca de Terceiros

-   **`click`:**
    -   **OBRIGATÓRIO:** Usar para definir todos os comandos CLI, opções e argumentos em [`ra_aid_start/__main__.py`](ra_aid_start/__main__.py). Ver [`PLAN.MD:654`](PLAN.MD:654).
-   **`rich`:**
    -   **OBRIGATÓRIO:** Usar para toda a formatação de saída no terminal (cores, tabelas, painéis, etc.) em [`ra_aid_start/ui/display.py`](ra_aid_start/ui/display.py) e outros módulos de UI. Ver [`PLAN.MD:653`](PLAN.MD:653).
-   **`pydantic`:**
    -   **OBRIGATÓRIO:** Usar para definir os modelos de dados em [`ra_aid_start/models/`](ra_aid_start/models/) (ex: `Preset`, `Model`). Ver [`PLAN.MD:655`](PLAN.MD:655).
-   **`jsonschema`:**
    -   **OBRIGATÓRIO:** Usar para validar a estrutura de arquivos JSON lidos ou antes de serem escritos, especialmente em `json_handler.py` e pelos managers. Schemas devem residir em [`ra_aid_start/data/schemas.py`](ra_aid_start/data/schemas.py). Ver [`PLAN.MD:656`](PLAN.MD:656).
-   **`pathlib`:**
    -   **OBRIGATÓRIO:** Usar para toda manipulação de caminhos de arquivo. Ver [`PLAN.MD:657`](PLAN.MD:657). Evitar o uso do módulo `os.path`.

## 6. Padrões de Fluxo de Trabalho

-   **Fluxo de Desenvolvimento:**
    -   **OBRIGATÓRIO:** Seguir as fases de desenvolvimento e os itens de cada fase conforme descrito em [`PLAN.MD:1387-1577`](PLAN.MD:1387).
-   **Fluxo de Configuração Assistida (Wizard):**
    -   O [`ConfigurationWizard`](PLAN.MD:959) ([`ra_aid_start/ui/wizards.py`](ra_aid_start/ui/wizards.py)) é o fluxo central para criar/editar presets.
    -   **OBRIGATÓRIO:** O wizard deve guiar o usuário através de todas as 47 flags relevantes de forma condicional, conforme detalhado em [`PLAN.MD:222-365`](PLAN.MD:222) e [`PLAN.MD:2705-2910`](PLAN.MD:2705).
-   **Testes:**
    -   **OBRIGATÓRIO:** Escrever testes unitários para novas funcionalidades.
    -   **OBRIGATÓRIO:** Manter uma correspondência entre módulos de código e módulos de teste (ex: `core/preset_manager.py` -> `tests/test_preset_manager.py`).

## 7. Padrões de Interação de Arquivos Chave

-   **Modificação de Modelos de Dados ([`ra_aid_start/models/`](ra_aid_start/models/)):**
    -   Se [`preset.py`](ra_aid_start/models/preset.py) for modificado (ex: nova flag no preset):
        -   **OBRIGATÓRIO:** Atualizar [`PresetManager`](ra_aid_start/core/preset_manager.py) para lidar com o novo campo (leitura, escrita, validação).
        -   **OBRIGATÓRIO:** Atualizar [`ConfigurationWizard`](ra_aid_start/ui/wizards.py) para incluir a configuração do novo campo.
        -   **OBRIGATÓRIO:** Atualizar [`CommandBuilder`](ra_aid_start/core/command_builder.py) se o novo campo afeta a construção do comando.
        -   **OBRIGATÓRIO:** Atualizar schemas em [`ra_aid_start/data/schemas.py`](ra_aid_start/data/schemas.py).
    -   Se [`provider.py`](ra_aid_start/models/provider.py) ou a estrutura de modelos LLM for modificada:
        -   **OBRIGATÓRIO:** Atualizar [`ModelManager`](ra_aid_start/core/model_manager.py).
        -   **OBRIGATÓRIO:** Atualizar [`ConfigurationWizard`](ra_aid_start/ui/wizards.py) nas seções de configuração de modelos.
        -   **OBRIGATÓRIO:** Atualizar [`default_models.py`](ra_aid_start/data/default_models.py) se aplicável.
-   **Arquivos de Dados Padrão ([`ra_aid_start/data/`](ra_aid_start/data/)):**
    -   [`default_models.py`](ra_aid_start/data/default_models.py): Contém a lista inicial de modelos. Modificar apenas para atualizar os modelos padrão fornecidos com a aplicação.
    -   [`schemas.py`](ra_aid_start/data/schemas.py): Contém schemas JSON. **OBRIGATÓRIO:** Atualizar ao modificar a estrutura dos dados JSON (presets, modelos).
-   **Testes ([`tests/`](tests/)):**
    -   **OBRIGATÓRIO:** Ao adicionar/modificar funcionalidade em um módulo em `ra_aid_start/`, adicionar/atualizar os testes correspondentes em `tests/`.
    -   Ex: Modificações em [`ra_aid_start/core/preset_manager.py`](ra_aid_start/core/preset_manager.py) exigem atualização de [`tests/test_preset_manager.py`](tests/test_preset_manager.py).
-   **Dependências:**
    -   **OBRIGATÓRIO:** Ao adicionar uma nova dependência, adicioná-la a [`requirements.txt`](requirements.txt) e [`setup.py`](setup.py).

## 8. Padrões de Tomada de Decisão da IA

-   **Prioridade de Modificação:**
    1.  **FAZER:** Priorizar a modificação e extensão de módulos existentes (`core/`, `ui/`, `models/`) antes de criar novos arquivos ou módulos, a menos que a nova funcionalidade seja distinta e grande o suficiente para justificar um novo módulo.
    2.  **NÃO FAZER:** Criar um novo arquivo para uma pequena funcionalidade de UI se ela puder ser integrada logicamente em [`menu_system.py`](ra_aid_start/ui/menu_system.py) ou [`wizards.py`](ra_aid_start/ui/wizards.py).
-   **Resolução de Dúvidas:**
    -   Para dúvidas sobre flags específicas do `ra-aid`: Consultar [`PLAN.MD:403-645`](PLAN.MD:403).
    -   Para dúvidas sobre o design da UI e menus: Consultar [`PLAN.MD:1680-2910`](PLAN.MD:1680).
    -   Para dúvidas sobre a estrutura de dados de presets ou modelos: Consultar [`PLAN.MD:375-394`](PLAN.MD:375) (Modelos) e [`PLAN.MD:986-1001`](PLAN.MD:986) (Preset).
-   **Exemplos de Decisão:**
    -   **Cenário:** Adicionar uma nova opção de logging (ex: `--log-format`).
        -   **O QUE FAZER:**
            1.  Modificar [`ConfigurationWizard`](ra_aid_start/ui/wizards.py) para adicionar uma pergunta sobre o formato do log.
            2.  Modificar [`CommandBuilder`](ra_aid_start/core/command_builder.py) para adicionar a flag `--log-format` ao comando gerado.
            3.  Se a opção for salva no preset, atualizar [`Preset`](ra_aid_start/models/preset.py) e [`PresetManager`](ra_aid_start/core/preset_manager.py).
            4.  Adicionar testes para a nova flag.
        -   **O QUE NÃO FAZER:** Criar um novo módulo `logging_configurator.py` apenas para esta flag.
    -   **Cenário:** Usuário pede para "melhorar a exibição de presets".
        -   **O QUE FAZER:** Analisar [`ra_aid_start/ui/menu_system.py`](ra_aid_start/ui/menu_system.py) e [`ra_aid_start/ui/display.py`](ra_aid_start/ui/display.py) e propor melhorias usando `rich` (ex: usar tabelas, cores diferentes para status).
        -   **O QUE NÃO FAZER:** Mudar a lógica de como os presets são carregados por [`PresetManager`](ra_aid_start/core/preset_manager.py) sem que isso seja explicitamente necessário para a melhoria da exibição.

## 9. Ações Proibidas

-   **PROIBIDO:** Alterar a estrutura de armazenamento de dados do usuário (`~/.ra-aid-start/`) ou o formato dos arquivos JSON principais (presets, modelos) sem uma especificação clara e atualização dos schemas em [`ra_aid_start/data/schemas.py`](ra_aid_start/data/schemas.py) e dos respectivos managers.
-   **PROIBIDO:** Introduzir novas dependências de terceiros sem:
    1.  Adicioná-las a [`requirements.txt`](requirements.txt).
    2.  Adicioná-las a `install_requires` em [`setup.py`](setup.py).
-   **PROIBIDO:** Modificar a assinatura (parâmetros, tipo de retorno) de métodos públicos nas classes Manager ([`PresetManager`](ra_aid_start/core/preset_manager.py), [`ModelManager`](ra_aid_start/core/model_manager.py), [`ConfigManager`](ra_aid_start/core/config_manager.py)) ou classes de UI principais sem atualizar todos os seus usos no código.
-   **PROIBIDO:** "Hardcodar" caminhos de arquivo. **OBRIGATÓRIO:** Usar `pathlib` e construir caminhos dinamicamente, especialmente para o diretório de dados do usuário (`~/.ra-aid-start/`). O `ConfigManager` deve fornecer o caminho base para dados do usuário.
-   **PROIBIDO:** Escrever código que não siga os padrões de formatação (PEP 8) ou tipagem.
-   **PROIBIDO:** Ignorar a escrita de testes unitários para novas funcionalidades ou correções de bugs significativas.
-   **PROIBIDO:** Adicionar funcionalidades não especificadas no [`PLAN.MD`](PLAN.MD) ou não solicitadas pelo usuário.
-   **PROIBIDO:** Interagir diretamente com arquivos de configuração (presets.json, models/*.json) fora das classes `PresetManager` e `ModelManager`.