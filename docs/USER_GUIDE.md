# Guia do Usuário - RA AID Start

Bem-vindo ao RA AID Start! Esta ferramenta foi projetada para simplificar a configuração e o uso do CLI `ra-aid`.

## Sumário

1.  [Introdução](#introdução)
2.  [Instalação](#instalação)
3.  [Primeiros Passos - Menu Principal](#primeiros-passos---menu-principal)
4.  [Gerenciando Presets](#gerenciando-presets)
    *   [Criando um Novo Preset](#criando-um-novo-preset)
    *   [Selecionando e Executando um Preset](#selecionando-e-executando-um-preset)
    *   [Editando um Preset Existente](#editando-um-preset-existente)
    *   [Visualizando um Preset](#visualizando-um-preset)
    *   [Excluindo um Preset](#excluindo-um-preset)
5.  [Gerenciando Modelos de LLM](#gerenciando-modelos-de-llm)
    *   [Visualizando Modelos por Provedor](#visualizando-modelos-por-provedor)
    *   [Restaurando Modelos Padrão](#restaurando-modelos-padrão)
    *   [Adicionar, Editar, Remover Modelos (Funcionalidade Futura)](#adicionar-editar-remover-modelos-funcionalidade-futura)
6.  [Backup e Restauração](#backup-e-restauração)
7.  [Entendendo os Presets](#entendendo-os-presets)
    *   [Informações Básicas](#informações-básicas)
    *   [Modo de Operação](#modo-de-operação)
    *   [Configurações Específicas do Modo](#configurações-específicas-do-modo)
    *   [Configuração de Modelos LLM](#configuração-de-modelos-llm)
    *   [Configuração de Ferramentas de Desenvolvimento](#configuração-de-ferramentas-de-desenvolvimento)
    *   [Configurações de Exibição e Logging](#configurações-de-exibição-e-logging)
    *   [Configurações Avançadas](#configurações-avançadas)

---

## 1. Introdução

RA AID Start é uma interface de linha de comando (CLI) que atua como um configurador e lançador para a ferramenta principal `ra-aid`. O objetivo é tornar mais fácil para os usuários definir, salvar e reutilizar configurações complexas (presets) para diferentes tarefas de automação e interação com modelos de linguagem.

## 2. Instalação

*(As instruções detalhadas de instalação serão fornecidas assim que o empacotamento do projeto for finalizado. Geralmente, envolverá um comando como `pip install ra-aid-start` ou usando Poetry.)*

**Pré-requisitos:**
*   Python 3.9 ou superior.
*   A ferramenta `ra-aid` deve estar acessível no seu sistema.

## 3. Primeiros Passos - Menu Principal

Para iniciar o RA AID Start, abra seu terminal e execute:
```bash
ra-aid-start
```
Você será saudado com o Menu Principal:

```
 Menu Principal

1. Selecionar e Executar Preset
2. Configurar/Editar Preset
3. Gerenciar Modelos
4. Backup/Restore
5. Sair
```

Use os números correspondentes para navegar pelas opções.

## 4. Gerenciando Presets

Presets são configurações salvas que você pode reutilizar para executar `ra-aid` com um conjunto específico de parâmetros.

### Criando um Novo Preset

1.  No Menu Principal, escolha a opção `2. Configurar/Editar Preset`.
2.  No submenu "Gerenciar Presets", escolha `1. Criar Novo Preset`.
3.  O **Assistente de Configuração** será iniciado. Siga os passos:
    *   **Informações Básicas:** Forneça um nome único e uma descrição opcional para o seu preset.
    *   **Modo de Operação:** Selecione o modo principal de operação (Chat, Mensagem, Arquivo, Servidor).
    *   **Configurações Específicas do Modo:** Configure opções relevantes para o modo escolhido (ex: para modo Chat, pode configurar arquivo de histórico, persona, etc.).
    *   **Configuração de Modelos LLM:** Selecione o modelo principal (obrigatório), um modelo "expert" (opcional) e modelos especializados (opcional) para diferentes tarefas. Você escolherá o provedor (ex: OpenAI, Anthropic) e depois o modelo específico.
    *   **Configuração de Ferramentas de Desenvolvimento:** Opções para integrar com ferramentas como Aider, definir ferramentas customizadas e configurar testes automatizados.
    *   **Configurações de Exibição e Logging:** Controle o que é exibido durante a execução (custos, pensamentos do modelo) e como os logs são tratados.
    *   **Configurações Avançadas:** Ajuste fino de parâmetros como limites de recursão, tokens, temperatura do modelo, etc. (Esta etapa é opcional).
4.  **Sumário e Confirmação:** Revise todas as configurações e o preview do comando que será gerado. Confirme para salvar o preset.

### Selecionando e Executando um Preset

1.  No Menu Principal, escolha a opção `1. Selecionar e Executar Preset`.
2.  Uma lista de presets salvos será exibida. Escolha um pelo ID.
3.  Os detalhes do preset e o comando completo serão mostrados.
4.  Você terá as opções:
    *   `1. Executar Preset`: Executa o comando associado ao preset.
    *   `2. Apenas Mostrar Comando`: Exibe o comando sem executá-lo.
    *   `3. Voltar`.

### Editando um Preset Existente

1.  No Menu Principal, escolha `2. Configurar/Editar Preset`.
2.  No submenu, escolha `2. Editar Preset Existente`.
3.  Selecione o preset que deseja editar da lista.
4.  O Assistente de Configuração será iniciado, pré-preenchido com os dados do preset selecionado. Modifique as seções conforme necessário e salve.

### Visualizando um Preset

1.  No Menu Principal, escolha `2. Configurar/Editar Preset`.
2.  No submenu, escolha `4. Visualizar Preset`.
3.  Selecione o preset que deseja visualizar. Os detalhes e o comando gerado serão exibidos.

### Excluindo um Preset

1.  No Menu Principal, escolha `2. Configurar/Editar Preset`.
2.  No submenu, escolha `3. Excluir Preset`.
3.  Selecione o preset que deseja excluir e confirme a exclusão.

## 5. Gerenciando Modelos de LLM

RA AID Start permite que você gerencie uma lista de modelos de linguagem de diferentes provedores.

### Visualizando Modelos por Provedor

1.  No Menu Principal, escolha `3. Gerenciar Modelos`.
2.  No submenu, escolha `1. Visualizar Modelos por Provider`.
3.  Selecione um provedor da lista. Os modelos associados a esse provedor serão exibidos.

### Restaurando Modelos Padrão

Esta opção restaura a lista de modelos para os padrões definidos na aplicação para provedores conhecidos (OpenAI, Anthropic, Google).
**Atenção:** Isso sobrescreverá quaisquer modelos existentes com o mesmo nome para os provedores padrão.

1.  No Menu Principal, escolha `3. Gerenciar Modelos`.
2.  No submenu, escolha `7. Restaurar Modelos Padrões`.
3.  Confirme a ação.

### Adicionar, Editar, Remover Modelos (Funcionalidade Futura)

As opções para adicionar, editar e remover modelos individualmente estão planejadas para futuras versões. Atualmente, você pode gerenciar os arquivos JSON de modelos manualmente no diretório `~/.ra-aid-start/models/` ou usar a opção de restaurar padrões.

## 6. Backup e Restauração

RA AID Start possui um sistema de backup para proteger suas configurações de presets e modelos.

1.  No Menu Principal, escolha `4. Backup/Restore`.
2.  Você terá opções para:
    *   **Criar Backup:** Salva o estado atual dos seus presets e modelos em um arquivo de backup nomeado com data e hora.
    *   **Listar Backups:** Mostra todos os backups disponíveis.
    *   **Restaurar Backup:** Permite selecionar um backup anterior para restaurar. **Atenção:** Restaurar um backup sobrescreverá suas configurações atuais. Um backup do estado atual será feito automaticamente antes da restauração, como medida de segurança.
    *   **Excluir Backup (Funcionalidade Futura):** Permitirá remover arquivos de backup específicos.

## 7. Entendendo os Presets

Um preset no RA AID Start é uma coleção de configurações que definem como o `ra-aid` deve operar. Abaixo estão os principais componentes de um preset que você configurará através do assistente:

### Informações Básicas
*   **Nome:** Um nome único e descritivo para o seu preset.
*   **Descrição:** Uma breve explicação do que o preset faz.

### Modo de Operação
Define a tarefa principal que o `ra-aid` executará. Exemplos:
*   `Chat Interativo`: Para conversas contínuas.
*   `Mensagem/Tarefa Única`: Para processar uma única instrução ou prompt.
*   `Arquivo de Texto`: Para processar o conteúdo de um arquivo.
*   `Servidor Web (API)`: Para executar o `ra-aid` como um servidor API.

### Configurações Específicas do Modo
Dependendo do modo de operação escolhido, opções adicionais estarão disponíveis.
*   **Modo Chat:**
    *   `Arquivo de histórico de chat`: Salva e carrega o histórico da conversa.
    *   `Arquivo de persona do chat`: Define uma persona para o assistente.
    *   `ID da sessão de chat`: Permite retomar sessões específicas.
    *   `Modo Cowboy`: Desabilita certas confirmações para uma interação mais rápida.
*   **Modo Mensagem/Arquivo:**
    *   `Modo Apenas Pesquisa`: Limita a IA a realizar pesquisas sem executar ações.
*   **Modo Servidor Web:**
    *   `Host da API`: O endereço de host para o servidor.
    *   `Porta da API`: A porta em que o servidor escutará.
    *   `Permitir CORS`: Habilita Cross-Origin Resource Sharing.

### Configuração de Modelos LLM
Você pode definir diferentes modelos para diferentes propósitos dentro de um mesmo preset.
*   **Modelo Principal:** O modelo usado por padrão para a tarefa principal. É obrigatório.
*   **Modelo Expert (Opcional):** Um modelo, possivelmente mais poderoso ou especializado, que pode ser invocado para tarefas específicas ou quando um raciocínio mais complexo é necessário.
*   **Modelos Especializados (Opcional):** Uma lista de modelos configurados para tarefas muito específicas (ex: um modelo para geração de código, outro para tradução).

### Configuração de Ferramentas de Desenvolvimento
*   **Usar Aider:** Integração com a ferramenta Aider para desenvolvimento assistido por IA no seu repositório git.
    *   `Arquivo de configuração do Aider`: Caminho para o arquivo de configuração do Aider.
*   **Ferramentas Customizadas:** Caminho para um arquivo Python contendo ferramentas personalizadas que o `ra-aid` pode usar.
*   **Comando para executar testes:** Define um comando para rodar testes (ex: `pytest`).
    *   `Executar testes automaticamente`: Se um comando de teste é fornecido, esta opção permite que os testes sejam executados automaticamente após certas ações da IA.

### Configurações de Exibição e Logging
*   **Mostrar rastreamento de custo:** Exibe informações sobre o custo estimado do uso da API do LLM.
*   **Mostrar pensamentos do modelo:** Exibe os "pensamentos" ou passos intermediários do modelo de IA.
*   **Modo de Logging:** Define para onde os logs são enviados (`stdout`, `stderr`, `file`, `dual`, `none`).
*   **Nível de Logging:** Controla a verbosidade dos logs (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
*   **Logger Formatado:** Usa um formato de log mais legível.
*   **Arquivo de Log:** Se o modo de log for `file` ou `dual`, especifica o caminho do arquivo de log.

### Configurações Avançadas
Estas são opções para usuários que desejam um controle mais granular sobre o comportamento do `ra-aid`.
*   **Limite de recursão:** Controla a profundidade de recursão em certas operações.
*   **Diretório de estado do projeto:** Onde o `ra-aid` armazena informações sobre o estado do projeto.
*   **Limpar memória do projeto ao iniciar:** Apaga o estado anterior do projeto no início de uma nova execução.
*   **Assistência de raciocínio:** Habilita funcionalidades de auxílio ao raciocínio da IA.
*   **Limites de Tokens (Total, Entrada, Saída):** Controlam o número máximo de tokens usados.
*   **Parâmetros de Geração do Modelo:**
    *   `Temperatura`: Controla a aleatoriedade da saída do modelo. Valores mais altos = mais criativo/aleatório.
    *   `Top P`: Controla a diversidade através da amostragem nucleus.
    *   `Top K`: Controla a diversidade limitando o número de próximos tokens considerados.
    *   `Penalidade de Frequência`: Penaliza tokens que já apareceram, incentivando novidade.
    *   `Penalidade de Presença`: Penaliza tokens que já apareceram recentemente.

---

Este guia deve ajudá-lo a começar a usar o RA AID Start. Para funcionalidades mais avançadas ou solução de problemas, consulte o README do projeto ou abra uma issue no repositório.