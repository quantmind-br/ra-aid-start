# Lista de Pendências e Melhorias - RA AID Start

Esta lista documenta bugs conhecidos, funcionalidades pendentes e sugestões de melhorias para futuras iterações do projeto `ra-aid-start`.

## Funcionalidades Pendentes

1.  **Gerenciamento de Modelos LLM:**
    *   Implementar interface para Adicionar, Editar e Remover modelos de LLM individualmente.
        *   *Status:* Anotado como "Funcionalidade Futura" no `docs/USER_GUIDE.md`.
        *   *Prioridade:* Média.

2.  **Sistema de Backup:**
    *   Implementar interface para Excluir arquivos de backup específicos.
        *   *Status:* Anotado como "Funcionalidade Futura" no `docs/USER_GUIDE.md`.
        *   *Prioridade:* Baixa.

## Melhorias Sugeridas

### Testes
1.  **Cobertura de Testes E2E:**
    *   Expandir os testes End-to-End para cobrir fluxos de usuário mais complexos de forma automatizada.
    *   *Prioridade:* Média.
2.  **Testes de Interface Rich:**
    *   Investigar e, se viável, implementar testes automatizados para a interface baseada em Rich.
    *   *Prioridade:* Baixa (devido à complexidade).

### Instalação e Empacotamento
1.  **Instruções de Instalação:**
    *   Finalizar e detalhar as instruções de instalação no [`README.md`](README.md) após a conclusão da Fase 7 (Empacotamento).
    *   *Prioridade:* Alta (pós-Fase 7).
2.  **Arquivo de Licença:**
    *   Criar o arquivo `LICENSE` (MIT) na raiz do projeto.
    *   *Prioridade:* Média.

### Interface do Usuário (UI/UX)
1.  **Listagens Longas:**
    *   Para listas extensas (presets, modelos, backups), considerar adicionar paginação ou funcionalidade de filtro/busca.
    *   *Prioridade:* Média.
2.  **Navegação no `ConfigurationWizard` (Edição):**
    *   Ao editar um preset, permitir que o usuário "pule para uma seção" específica em vez de percorrer todas as etapas sequencialmente.
    *   *Prioridade:* Média.

### Validação de Dados
1.  **Validação de Entradas:**
    *   Revisar e reforçar a validação de todas as entradas do usuário no `ConfigurationWizard` e `MenuSystem` contra dados inesperados ou maliciosos (complementar à validação de modelos Pydantic).
    *   *Prioridade:* Média.

### Documentação
1.  **Exemplos Adicionais:**
    *   Adicionar exemplos de uso mais concretos e variados ao [`README.md`](README.md) e [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md).
    *   *Prioridade:* Baixa (contínua).
2.  **Documentação de Código (Automática):**
    *   Considerar a implementação de geração automática de documentação do código (ex: usando Sphinx) a partir dos docstrings existentes.
    *   *Prioridade:* Baixa.

### Configuração de Modelos LLM
1.  **Gerenciamento de Novos Provedores/Modelos:**
    *   Melhorar a interface ou o fluxo no `ConfigurationWizard` para lidar com cenários onde um provedor de LLM (adicionado manualmente ao JSON, por exemplo) não possui modelos definidos, ou para facilitar a adição de novos modelos a provedores existentes.
    *   *Prioridade:* Média.

### Performance
1.  **Carregamento de Listas Grandes:**
    *   Monitorar a performance ao carregar/listar um número muito grande de presets ou backups. Se necessário, implementar otimizações (ex: carregamento preguiçoso, indexação).
    *   *Prioridade:* Baixa (monitorar).

## Bugs Conhecidos
*   (Nenhum bug crítico identificado nesta revisão. A lista será atualizada se surgirem.)