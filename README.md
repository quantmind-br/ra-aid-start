# RA AID Start

## Sobre o Projeto

RA AID Start é uma ferramenta CLI projetada para auxiliar na configuração e execução de comandos para a ferramenta `ra-aid` (Robotic Automation AID). Ela permite aos usuários gerenciar presets de configuração, modelos de linguagem e executar tarefas de automação de forma simplificada através de uma interface interativa.

## Funcionalidades

*   **Gerenciamento de Presets:** Crie, edite, execute e exclua presets de configuração.
*   **Gerenciamento de Modelos:** Adicione, edite, remova e visualize modelos de linguagem (LLMs) por provedor.
*   **Interface Interativa:** Menus e assistentes guiados para facilitar a configuração.
*   **Geração de Comandos:** Construção automática de strings de comando para `ra-aid` com base nos presets.
*   **Sistema de Backup:** Crie e restaure backups das configurações de presets e modelos.
*   **Validação de Dados:** Regras de validação para garantir a integridade dos dados de configuração.

## Pré-requisitos

*   Python 3.9 ou superior
*   Poetry (para desenvolvimento e gerenciamento de dependências)
*   A ferramenta `ra-aid` (o CLI principal que este utilitário ajuda a configurar)

## Instalação

```bash
# Instruções de instalação (a serem definidas após o empacotamento com Poetry)
# Exemplo:
# poetry install
# ou
# pip install ra-aid-start
```

## Uso Básico

Após a instalação, execute o comando:

```bash
ra-aid-start
```

Isso iniciará a interface interativa do menu principal, onde você poderá:
1.  Selecionar e Executar um Preset existente.
2.  Configurar/Editar Presets (criar novos ou modificar existentes).
3.  Gerenciar Modelos de LLM.
4.  Realizar Backup ou Restauração das configurações.

## Exemplos

*(Esta seção será preenchida com exemplos de uso mais concretos após a finalização das funcionalidades principais.)*

**Exemplo 1: Criando um novo preset para chat**
1.  Execute `ra-aid-start`.
2.  Escolha a opção "Configurar/Editar Preset".
3.  Escolha "Criar Novo Preset".
4.  Siga as instruções do assistente para definir:
    *   Nome e descrição do preset.
    *   Modo de operação: "Chat Interativo".
    *   Configurações específicas do modo chat (ex: arquivo de histórico, persona).
    *   Modelos LLM (principal, expert, etc.).
    *   Outras configurações (ferramentas, display, logging, avançadas).
5.  Revise o sumário e confirme para salvar.

**Exemplo 2: Executando um preset existente**
1.  Execute `ra-aid-start`.
2.  Escolha a opção "Selecionar e Executar Preset".
3.  Selecione o preset desejado da lista.
4.  Confirme a execução.

## Contribuição

Contribuições são bem-vindas! Por favor, siga estas etapas:

1.  Faça um fork do projeto.
2.  Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`).
3.  Faça commit de suas alterações (`git commit -m 'Add some AmazingFeature'`).
4.  Faça push para a branch (`git push origin feature/AmazingFeature`).
5.  Abra um Pull Request.

*(Mais detalhes sobre padrões de código, testes e processo de contribuição podem ser adicionados aqui.)*

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
*(Nota: O arquivo LICENSE ainda não foi criado.)*