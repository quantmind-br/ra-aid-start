"""
Ponto de entrada principal para a aplicação CLI RA AID Start.

Este script inicializa e executa o sistema de menus interativos,
permitindo ao usuário gerenciar presets, modelos e executar configurações.
Utiliza a biblioteca 'click' para a interface de linha de comando.
"""
import click
from pathlib import Path
import sys

# Adicionar o diretório raiz do projeto ao sys.path para importações corretas
# __file__ em __main__.py aponta para ra_aid_start/__main__.py
# .parent é ra_aid_start/
# .parent.parent é o diretório que contém ra_aid_start/ (raiz do projeto)
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

try:
    from ra_aid_start.ui.menu_system import MenuSystem
    # Importar quaisquer outras dependências de UI ou core se necessário aqui
except ImportError as e:
    # Isso pode ajudar a diagnosticar problemas de importação se o sys.path não estiver correto
    # ou se houver um erro de digitação no nome do módulo/classe.
    print(f"Erro de importação: {e}")
    print(f"sys.path atual: {sys.path}")
    print(f"Raiz do projeto calculada: {project_root}")
    print("Verifique se o nome 'ra_aid_start.ui.menu_system.MenuSystem' está correto e acessível.")
    sys.exit(1)

@click.command()
def main_cli():
    """
    RA AID Start: Ferramenta CLI para auxiliar na configuração e execução de presets do RA.Aid.
    """
    # Verifica se a importação foi bem-sucedida antes de tentar usar MenuSystem
    if 'MenuSystem' not in globals():
        click.echo("Erro crítico: A classe MenuSystem não pôde ser importada.")
        click.echo("A aplicação não pode continuar. Verifique as mensagens de erro anteriores.")
        return

    menu = MenuSystem()
    try:
        menu.run() # Inicia o loop principal do sistema de menus
    except KeyboardInterrupt:
        menu.console.print("\n[bold yellow]Execução interrompida pelo usuário. Saindo...[/bold yellow]")
    except Exception as e:
        menu.console.print(f"\n[bold red]Ocorreu um erro inesperado na aplicação:[/bold red]")
        menu.console.print_exception(show_locals=True) # Mostra o traceback completo
        menu.console.print(f"[bold red]Erro: {e}[/bold red]")
        click.echo("A aplicação encontrou um erro e precisa ser fechada.")
    finally:
        click.echo("Obrigado por usar o RA AID Start!")

if __name__ == '__main__':
    main_cli()