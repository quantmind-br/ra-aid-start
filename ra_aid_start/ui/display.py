"""
Utilitários de Display para a Interface do Usuário.

Este módulo fornece funções para exibir informações formatadas no console
usando a biblioteca Rich. Inclui helpers para tabelas, painéis, texto estilizado
e mensagens padronizadas de sucesso, aviso, erro e informação.
"""
from typing import List, Any, Optional, Dict
from rich.console import Console
from rich.table import Table, Column
from rich.panel import Panel
from rich.text import Text
from rich.box import SIMPLE_HEAVY, ROUNDED

# Inicializa um console global para ser usado pelas funções
_console = Console()

def display_table(
    headers: List[str],
    rows: List[List[Any]],
    title: Optional[str] = None,
    box_style: Optional[Any] = SIMPLE_HEAVY,
    show_lines: bool = True,
    column_styles: Optional[List[Optional[str]]] = None,
    column_justifications: Optional[List[Optional[str]]] = None,
    column_min_widths: Optional[List[Optional[int]]] = None,
    column_max_widths: Optional[List[Optional[int]]] = None,
    column_overflows: Optional[List[Optional[str]]] = None
) -> None:
    """
    Exibe uma tabela formatada no console.

    Args:
        headers: Lista de strings para os cabeçalhos das colunas.
        rows: Lista de listas, onde cada sublista representa uma linha de dados.
        title: Título opcional para a tabela.
        box_style: Estilo da borda da tabela (ex: SIMPLE_HEAVY, ROUNDED).
        show_lines: Se True, exibe linhas entre as linhas da tabela.
        column_styles: Lista opcional de estilos CSS para cada coluna.
        column_justifications: Lista opcional de justificações ('left', 'center', 'right') para cada coluna.
        column_min_widths: Lista opcional de larguras mínimas para cada coluna.
        column_max_widths: Lista opcional de larguras máximas para cada coluna.
        column_overflows: Lista opcional de comportamentos de overflow ('fold', 'crop', 'ellipsis') para cada coluna.
    """
    table = Table(title=title, box=box_style, show_lines=show_lines)

    for i, header in enumerate(headers):
        col_kwargs: Dict[str, Any] = {}
        if column_styles and i < len(column_styles) and column_styles[i]:
            col_kwargs["style"] = column_styles[i]
        if column_justifications and i < len(column_justifications) and column_justifications[i]:
            col_kwargs["justify"] = column_justifications[i]
        if column_min_widths and i < len(column_min_widths) and column_min_widths[i] is not None:
            col_kwargs["min_width"] = column_min_widths[i]
        if column_max_widths and i < len(column_max_widths) and column_max_widths[i] is not None:
            col_kwargs["max_width"] = column_max_widths[i]
        if column_overflows and i < len(column_overflows) and column_overflows[i]:
            col_kwargs["overflow"] = column_overflows[i]
        
        table.add_column(header, **col_kwargs)

    for row in rows:
        # Converte todos os itens da linha para string para evitar problemas com rich
        table.add_row(*(str(item) for item in row))
    
    _console.print(table)

def display_panel(
    content: Any,
    title: Optional[str] = None,
    border_style: str = "blue",
    expand: bool = False,
    padding: Any = (0, 1) # (vertical, horizontal)
) -> None:
    """
    Exibe um painel formatado no console.

    Args:
        content: O conteúdo a ser exibido dentro do painel (pode ser Text, str, etc.).
        title: Título opcional para o painel.
        border_style: Estilo da borda do painel.
        expand: Se True, o painel se expandirá para preencher a largura disponível.
        padding: Preenchimento dentro do painel.
    """
    _console.print(Panel(
        content,
        title=title,
        border_style=border_style,
        expand=expand,
        padding=padding
    ))

def display_text(
    message: str,
    style: Optional[str] = None,
    justify: Optional[str] = None, # "left", "center", "right", "full"
    overflow: Optional[str] = None, # "fold", "crop", "ellipsis", "ignore"
    end: str = "\n"
) -> None:
    """
    Exibe um texto estilizado no console.

    Args:
        message: A mensagem de texto a ser exibida.
        style: Estilo CSS opcional para o texto.
        justify: Justificação opcional do texto.
        overflow: Comportamento de overflow opcional.
        end: Caractere de fim de linha.
    """
    text = Text(message, style=style, justify=justify, overflow=overflow)
    _console.print(text, end=end)

def display_success(message: str, title: Optional[str] = "Sucesso") -> None:
    """
    Exibe uma mensagem de sucesso formatada em um painel.

    Args:
        message: A mensagem de sucesso.
        title: Título para o painel de sucesso.
    """
    display_panel(Text(message, style="green"), title=f"[bold green]{title}[/bold green]", border_style="green")

def display_warning(message: str, title: Optional[str] = "Aviso") -> None:
    """
    Exibe uma mensagem de aviso formatada em um painel.

    Args:
        message: A mensagem de aviso.
        title: Título para o painel de aviso.
    """
    display_panel(Text(message, style="yellow"), title=f"[bold yellow]{title}[/bold yellow]", border_style="yellow")

def display_error(message: str, title: Optional[str] = "Erro") -> None:
    """
    Exibe uma mensagem de erro formatada em um painel.

    Args:
        message: A mensagem de erro.
        title: Título para o painel de erro.
    """
    display_panel(Text(message, style="red"), title=f"[bold red]{title}[/bold red]", border_style="red")

def display_info(message: str, title: Optional[str] = "Informação") -> None:
    """
    Exibe uma mensagem informativa formatada em um painel.

    Args:
        message: A mensagem informativa.
        title: Título para o painel de informação.
    """
    display_panel(Text(message, style="cyan"), title=f"[bold cyan]{title}[/bold cyan]", border_style="cyan")

if __name__ == "__main__":
    # Exemplos de uso
    display_success("Operação concluída com êxito!")
    display_error("Falha ao processar o arquivo.", title="Erro de Arquivo")
    display_warning("O limite de taxa da API será atingido em breve.")
    display_info("O sistema será reiniciado para manutenção às 02:00.")

    display_text("Este é um texto simples.", style="bold magenta")
    display_text("Texto centralizado.", justify="center", style="underline blue")

    headers_ex = ["ID", "Nome", "Status"]
    rows_ex = [
        [1, "Tarefa Alpha", "Concluída"],
        [2, "Tarefa Beta", "Em Progresso"],
        [3, "Tarefa Gamma", "Pendente"]
    ]
    display_table(headers_ex, rows_ex, title="Status das Tarefas", column_styles=["dim", "cyan", "yellow"])

    complex_panel_content = Text()
    complex_panel_content.append("Linha 1: Informação importante.\n", style="bold")
    complex_panel_content.append("Linha 2: Detalhes adicionais aqui.")
    display_panel(complex_panel_content, title="Painel Complexo", border_style="magenta", padding=(1,2))