"""
Sistema de Menus Interativos para RA AID Start.

Este módulo define a classe MenuSystem, responsável por apresentar
a interface de linha de comando principal da aplicação, permitindo
ao usuário navegar entre as funcionalidades de gerenciamento de presets,
modelos, execução de presets e outras operações.
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from rich.box import SIMPLE_HEAVY
from pathlib import Path # Para obter o diretório do usuário
from typing import List, Dict, Any, Optional # Para type hinting
import json # Para json.JSONDecodeError

# Adicionar o diretório raiz do projeto ao sys.path
import sys
import os
# Obtém o diretório do script atual (menu_system.py) -> ra_aid_start/ui
# Sobe dois níveis para obter o diretório raiz do projeto
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from ra_aid_start.core.preset_manager import PresetManager
from ra_aid_start.models.preset import Preset # Para type hinting
from ra_aid_start.core.model_manager import ModelManager
from ra_aid_start.models.model import Model # Para type hinting
from ra_aid_start.ui.display import display_error, display_info, display_success, display_warning, display_panel # Adicionado
from ra_aid_start.ui.wizards import ConfigurationWizard # Adicionado para integração
from ra_aid_start.models.validation import ValidationRules # Adicionado para ConfigurationWizard
from ra_aid_start.utils.json_handler import save_json # Added for export models

class MenuSystem:
    """
    Gerencia a exibição e navegação dos menus da aplicação.
    """
    def __init__(self):
        self.console = Console()
        # Determinar o diretório base para os dados da aplicação
        # Usaremos ~/.ra-aid-start como padrão
        self.base_data_dir = Path.home() / ".ra-aid-start"
        self.presets_dir = self.base_data_dir / "presets"
        self.models_dir = self.base_data_dir / "models"
        
        self.preset_manager = PresetManager(base_storage_path=self.base_data_dir)
        self.model_manager = ModelManager(base_storage_path=self.base_data_dir)
        self.validation_rules = ValidationRules() # Instanciar para o Wizard

        self.options = {
            "1": "Selecionar e Executar Preset",
            "2": "Configurar/Editar Preset",
            "3": "Gerenciar Modelos",
            "4": "Backup/Restore",
            "5": "Sair"
        }

    def display_main_menu(self):
        """
        Exibe o menu principal formatado.
        """
        menu_text = Text("\nMenu Principal\n\n", justify="center", style="bold cyan")
        for key, value in self.options.items():
            menu_text.append(f"{key}. {value}\n", style="white")
        
        self.console.print(Panel(
            menu_text,
            title="[bold green]RA AID Start[/bold green]",
            expand=False,
            border_style="blue"
        ))

    def get_user_choice(self) -> str:
        """
        Captura a escolha do usuário.
        """
        choice = Prompt.ask("Escolha uma opção", choices=list(self.options.keys()), show_choices=False)
        return choice

    def run(self):
        """
        Loop principal do menu.
        """
        while True:
            self.display_main_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self._handle_select_execute_preset()
            elif choice == "2":
                self._handle_manage_presets()
            elif choice == "3":
                self._handle_manage_models()
            elif choice == "4":
                display_warning("Opção 4 selecionada: Backup/Restore (Funcionalidade futura)")
                # Lógica para backup/restore
                pass
            elif choice == "5":
                display_info("Saindo...")
                break
            else:
                display_error("Opção inválida. Tente novamente.")
            
            Prompt.ask("\nPressione Enter para continuar...") # Pausa para o usuário ver a mensagem

    def _handle_select_execute_preset(self):
        """
        Lida com a lógica de selecionar e executar um preset.
        """
        self.console.print(Panel(Text("Selecionar e Executar Preset", justify="center", style="bold green")))
        
        presets = self.preset_manager.list_presets()

        if not presets:
            display_warning("Nenhum preset encontrado.")
            return

        table = Table(title="Presets Disponíveis", box=SIMPLE_HEAVY, show_lines=True)
        table.add_column("ID", style="dim", width=5, justify="center")
        table.add_column("Nome", style="cyan", min_width=20)
        table.add_column("Comando (Resumido)", style="magenta", min_width=30, overflow="ellipsis")

        preset_map = {} # Mapeia o número da lista para o nome do preset (ID)
        for i, preset_obj in enumerate(presets, 1): # preset_obj é um objeto Preset
            actual_preset_name_str = preset_obj.name # Usar o atributo .name para a string do nome
            try:
                # O objeto preset_obj de list_presets() já deve ter o comando.
                # Se não tiver, ou se quisermos garantir o mais recente, podemos carregar.
                # Por ora, vamos assumir que preset_obj.command é suficiente.
                if preset_obj.command:
                    command_summary = (preset_obj.command[:70] + "...") if len(preset_obj.command) > 70 else preset_obj.command
                else:
                    # Fallback: tentar carregar se o comando não estiver no objeto listado
                    # (Isso pode acontecer se o save_preset não conseguiu gerar o comando anteriormente)
                    loaded_for_command = self.preset_manager.load_preset(actual_preset_name_str)
                    if loaded_for_command and loaded_for_command.command:
                         command_summary = (loaded_for_command.command[:70] + "...") if len(loaded_for_command.command) > 70 else loaded_for_command.command
                    else:
                        command_summary = "N/A"
            except Exception:
                command_summary = "[dim]Erro ao obter comando[/dim]"
            
            table.add_row(str(i), actual_preset_name_str, command_summary) # Passar a string do nome
            preset_map[str(i)] = actual_preset_name_str # Mapear para o nome (string)
        
        self.console.print(table)

        if not preset_map: # Redundante devido à verificação anterior, mas seguro
            display_warning("Nenhum preset válido para seleção.")
            return

        choice = Prompt.ask("Escolha um preset pelo ID (número) ou 'v' para voltar", choices=list(preset_map.keys()) + ['v'], show_choices=False)

        if choice.lower() == 'v':
            return

        selected_preset_name = preset_map.get(choice)
        if not selected_preset_name:
            display_error("Seleção inválida.")
            return

        try:
            preset = self.preset_manager.load_preset(selected_preset_name)
            if not preset:
                display_error(f"Erro ao carregar o preset '{selected_preset_name}'.")
                return
        except Exception as e:
            display_error(f"Erro ao carregar o preset '{selected_preset_name}': {e}")
            return

        details_text = Text(f"Detalhes do Preset: {preset.name}\n\n", style="bold cyan")
        details_text.append(f"Nome: {preset.name}\n", style="white")
        details_text.append(f"Descrição: {preset.description or 'N/A'}\n", style="white")
        details_text.append(f"Comando Completo:\n", style="white")
        details_text.append(f"{preset.command}\n\n", style="yellow")
        
        self.console.print(Panel(
            details_text,
            title=f"[bold green]Preset: {preset.name}[/bold green]",
            expand=False,
            border_style="blue"
        ))

        sub_options = {
            "1": "Executar Preset",
            "2": "Apenas Mostrar Comando",
            "3": "Voltar"
        }
        sub_menu_text = Text("\nOpções:\n", style="bold")
        for k, v in sub_options.items():
            sub_menu_text.append(f"{k}. {v}\n")
        self.console.print(sub_menu_text)
        
        sub_choice = Prompt.ask("Escolha uma opção", choices=list(sub_options.keys()), show_choices=False)

        if sub_choice == "1":
            display_info(f"Executando preset '{preset.name}'...")
            try:
                # Garantir que o PresetManager tenha sido inicializado corretamente
                # Se o preset_manager foi inicializado no __init__ da classe, ele já deve estar pronto
                execution_successful = self.preset_manager.execute_preset(preset.name)
                if execution_successful:
                    display_success(f"Preset '{preset.name}' parece ter sido executado.")
                    display_info("Encerrando a aplicação conforme solicitado...")
                    sys.exit(0)
                else:
                    display_error(f"Falha ao executar o preset '{preset.name}'. Verifique os logs para mais detalhes.")
            except Exception as e:
                display_error(f"Erro inesperado ao tentar executar o preset '{preset.name}': {e}")
        elif sub_choice == "2":
            display_info(f"Comando para '{preset.name}':\n{preset.command}", title="Comando do Preset")
        elif sub_choice == "3":
            return # Volta ao menu principal

    def _handle_manage_presets(self):
        """
        Lida com a lógica de gerenciar presets (criar, editar, excluir, etc.).
        """
        manage_options = {
            "1": "Criar Novo Preset",
            "2": "Editar Preset Existente",
            "3": "Excluir Preset",
            "4": "Visualizar Preset",
            "5": "Importar Presets",
            "6": "Exportar Presets",
            "7": "Voltar ao Menu Principal"
        }

        while True:
            self.console.print(Panel(Text("Gerenciar Presets", justify="center", style="bold green")))
            
            menu_text = Text()
            for key, value in manage_options.items():
                menu_text.append(f"{key}. {value}\n", style="white")
            self.console.print(menu_text)

            choice = Prompt.ask("Escolha uma opção", choices=list(manage_options.keys()), show_choices=False)

            if choice == "1": # Criar Novo Preset
                wizard = ConfigurationWizard(
                    preset_manager=self.preset_manager,
                    model_manager=self.model_manager,
                    validation_rules=self.validation_rules, # Passar ValidationRules
                    console=self.console
                )
                new_preset = wizard.start_wizard()
                if new_preset:
                    display_success(f"Novo preset '{new_preset.name}' criado através do assistente.")
                else:
                    display_warning("Criação de novo preset cancelada ou falhou no assistente.")
            elif choice == "2": # Editar Preset Existente
                self._select_and_perform_action_on_preset("editar")
            elif choice == "3": # Excluir Preset
                self._select_and_perform_action_on_preset("excluir")
            elif choice == "4": # Visualizar Preset
                self._select_and_perform_action_on_preset("visualizar")
            elif choice == "5": # Importar Presets
                display_warning("Funcionalidade 'Importar Presets' a ser implementada.")
                # Lógica para self.preset_manager.import_presets()
            elif choice == "6": # Exportar Presets
                display_warning("Funcionalidade 'Exportar Presets' a ser implementada.")
                # Lógica para self.preset_manager.export_presets()
            elif choice == "7": # Voltar
                break
            else:
                display_error("Opção inválida. Tente novamente.")
            
            if choice != "7": # Não pausar se estiver voltando
                Prompt.ask("\nPressione Enter para continuar...")

    def _select_and_perform_action_on_preset(self, action: str):
        """
        Lista presets e permite ao usuário selecionar um para uma ação específica (visualizar, excluir, editar).
        """
        self.console.print(Panel(Text(f"{action.capitalize()} Preset", justify="center", style="bold green")))
        
        presets = self.preset_manager.list_presets()
        if not presets:
            display_warning("Nenhum preset encontrado.")
            return

        table = Table(title="Presets Disponíveis", box=SIMPLE_HEAVY, show_lines=True)
        table.add_column("ID", style="dim", width=5, justify="center")
        table.add_column("Nome", style="cyan", min_width=20)

        preset_map = {}
        for i, preset_obj in enumerate(presets, 1): # Iterar sobre objetos Preset
            table.add_row(str(i), preset_obj.name)
            preset_map[str(i)] = preset_obj.name # Mapear para o nome do preset
        
        self.console.print(table)

        if not preset_map:
            display_warning("Nenhum preset válido para seleção.")
            return

        choice = Prompt.ask(f"Escolha um preset pelo ID para {action} ou 'v' para voltar", choices=list(preset_map.keys()) + ['v'], show_choices=False)

        if choice.lower() == 'v':
            return

        selected_preset_name = preset_map.get(choice)
        if not selected_preset_name:
            display_error("Seleção inválida.")
            return

        try:
            preset = self.preset_manager.load_preset(selected_preset_name)
            if not preset:
                display_error(f"Erro ao carregar o preset '{selected_preset_name}'.")
                return
        except Exception as e:
            display_error(f"Erro ao carregar o preset '{selected_preset_name}': {e}")
            return

        if action == "visualizar":
            details_text = Text(f"Detalhes do Preset: {preset.name}\n\n", style="bold cyan")
            details_text.append(f"Nome: {preset.name}\n", style="white")
            details_text.append(f"Descrição: {preset.description or 'N/A'}\n", style="white")
            details_text.append(f"Comando Completo:\n", style="white")
            details_text.append(f"{preset.command}\n\n", style="yellow")
            self.console.print(Panel(details_text, title=f"[bold green]Preset: {preset.name}[/bold green]", expand=False, border_style="blue"))
        
        elif action == "excluir":
            confirm = Prompt.ask(f"Tem certeza que deseja excluir o preset '{preset.name}'? (s/n)", choices=["s", "n"], default="n")
            if confirm.lower() == 's':
                try:
                    if self.preset_manager.delete_preset(preset.name):
                        display_success(f"Preset '{preset.name}' excluído com sucesso.")
                    else:
                        # O delete_preset deve idealmente já logar/retornar erro específico
                        display_error(f"Erro ao excluir o preset '{preset.name}' (PresetManager).")
                except Exception as e:
                    display_error(f"Erro ao excluir o preset '{preset.name}': {e}")
            else:
                display_warning("Exclusão cancelada.")

        elif action == "editar":
            wizard = ConfigurationWizard(
                preset_manager=self.preset_manager,
                model_manager=self.model_manager,
                validation_rules=self.validation_rules, # Passar ValidationRules
                console=self.console
            )
            edited_preset = wizard.start_wizard(existing_preset_name=selected_preset_name) # Passar nome do preset
            if edited_preset:
                display_success(f"Preset '{edited_preset.name}' editado através do assistente.")
            else:
                display_warning(f"Edição do preset '{selected_preset_name}' cancelada ou falhou no assistente.")

    def _add_new_model_ui(self):
        """
        Interface para adicionar um novo modelo LLM.
        """
        self.console.print(Panel(Text("Adicionar Novo Modelo LLM", justify="center", style="bold green")))

        try:
            provider = Prompt.ask("Nome do Provider (ex: openai, anthropic)")
            if not provider.strip():
                display_error("Nome do Provider é obrigatório.")
                return

            model_name = Prompt.ask("Nome do Modelo (ex: gpt-4, claude-3-opus)")
            if not model_name.strip():
                display_error("Nome do Modelo é obrigatório.")
                return
            
            provider = provider.strip() # Garante que não há espaços extras
            model_name = model_name.strip()

            description = Prompt.ask("Descrição do Modelo (opcional)")
            
            recommended_for_str = Prompt.ask("Recomendado para (separado por vírgulas, opcional, ex: coding,writing)")
            recommended_for_list = [r.strip() for r in recommended_for_str.split(',')] if recommended_for_str.strip() else []

            is_default_str = Prompt.ask("É modelo padrão para este provider? (s/n)", choices=["s", "n"], default="n")
            is_default_bool = is_default_str.lower() == 's'

            supports_temp_str = Prompt.ask("Suporta ajuste de temperatura? (s/n)", choices=["s", "n"], default="s")
            supports_temp_bool = supports_temp_str.lower() == 's'

            context_window_str = Prompt.ask("Janela de Contexto (opcional, ex: 4096)")
            context_window_int = None
            if context_window_str.strip():
                try:
                    context_window_int = int(context_window_str)
                except ValueError:
                    display_warning("Janela de contexto inválida, será ignorada.")

            model_data = {
                "name": model_name,
                "description": description.strip() if description else None,
                "provider": provider, # Provider para o Pydantic Model
                "recommended_for": recommended_for_list,
                "is_default": is_default_bool,
                "supports_temperature": supports_temp_bool,
                "context_window": context_window_int,
                "created_by": "user" 
            }

            new_model = self.model_manager.add_model(provider, model_data)

            if new_model:
                display_success(f"Modelo '{new_model.name}' adicionado com sucesso ao provider '{provider}'.")
            else:
                # ModelManager.add_model deve logar o erro específico.
                # Aqui, damos uma mensagem genérica de falha.
                display_error(f"Falha ao adicionar modelo '{model_name}' ao provider '{provider}'. Verifique se o modelo já existe ou os dados são válidos.")

        except Exception as e:
            display_error(f"Ocorreu um erro inesperado ao adicionar o modelo: {e}")

    def _edit_existing_model_ui(self):
        """
        Interface para editar um modelo LLM existente.
        """
        self.console.print(Panel(Text("Editar Modelo Existente", justify="center", style="bold green")))

        try:
            # 1. Select Provider
            providers = self.model_manager.get_available_providers()
            if not providers:
                display_warning("Nenhum provider com modelos encontrado.")
                return

            display_info("Providers disponíveis:")
            provider_map = {}
            for i, provider_name in enumerate(providers, 1):
                self.console.print(f"{i}. {provider_name}")
                provider_map[str(i)] = provider_name
            
            provider_choice = Prompt.ask("Escolha um provider pelo número ou 'v' para voltar", choices=list(provider_map.keys()) + ['v'], show_choices=False)

            if provider_choice.lower() == 'v':
                return
            
            selected_provider_name = provider_map.get(provider_choice)
            if not selected_provider_name:
                display_error("Seleção de provider inválida.")
                return

            # 2. Select Model from Provider
            models: List[Model] = self.model_manager.get_models_for_provider(selected_provider_name)
            if not models:
                display_warning(f"Nenhum modelo encontrado para o provider '{selected_provider_name}'.")
                return

            display_info(f"Modelos disponíveis para o provider '{selected_provider_name}':")
            model_map = {}
            model_table = Table(title=f"Modelos em {selected_provider_name}", box=SIMPLE_HEAVY)
            model_table.add_column("ID", style="dim", width=5, justify="center")
            model_table.add_column("Nome", style="cyan", min_width=20)
            model_table.add_column("Descrição", style="magenta", min_width=30, overflow="ellipsis")

            for i, model_obj in enumerate(models, 1):
                model_table.add_row(str(i), model_obj.name, model_obj.description or "N/A")
                model_map[str(i)] = model_obj.name
            
            self.console.print(model_table)
            
            model_choice = Prompt.ask("Escolha um modelo pelo ID para editar ou 'v' para voltar", choices=list(model_map.keys()) + ['v'], show_choices=False)

            if model_choice.lower() == 'v':
                return

            selected_model_name = model_map.get(model_choice)
            if not selected_model_name:
                display_error("Seleção de modelo inválida.")
                return

            # 3. Display Current Model Details
            current_model = next((m for m in models if m.name == selected_model_name), None)
            if not current_model:
                display_error(f"Modelo '{selected_model_name}' não encontrado no provider '{selected_provider_name}'.") # Should not happen if logic is correct
                return

            details_table = Table(title=f"Detalhes Atuais de '{current_model.name}' (Provider: {current_model.provider})", box=SIMPLE_HEAVY, show_lines=True)
            details_table.add_column("Campo", style="bold blue")
            details_table.add_column("Valor Atual", style="white")

            details_table.add_row("Descrição", current_model.description or "N/A")
            details_table.add_row("Recomendado Para", ", ".join(current_model.recommended_for) if current_model.recommended_for else "N/A")
            details_table.add_row("É Padrão?", "Sim" if current_model.is_default else "Não")
            details_table.add_row("Suporta Temperatura?", "Sim" if current_model.supports_temperature else "Não")
            details_table.add_row("Janela de Contexto", str(current_model.context_window) if current_model.context_window is not None else "N/A")
            self.console.print(details_table)
            
            display_info("Deixe o campo em branco para não alterar o valor.")
            update_data: Dict[str, Any] = {}

            # 4. Prompt for Fields to Update
            new_description = Prompt.ask(f"Nova Descrição (atual: '{current_model.description or 'N/A'}', Enter para manter)", default="").strip()
            if new_description:
                update_data['description'] = new_description

            new_recommended_for_str = Prompt.ask(f"Novas Recomendações (atual: {','.join(current_model.recommended_for) if current_model.recommended_for else 'N/A'}, Enter para manter, separado por vírgulas)", default="").strip()
            if new_recommended_for_str:
                update_data['recommended_for'] = [r.strip() for r in new_recommended_for_str.split(',') if r.strip()]

            new_is_default_str = Prompt.ask(f"É modelo padrão? (atual: {'s' if current_model.is_default else 'n'}, Enter para manter) (s/n)", choices=["s", "n", ""], default="").lower()
            if new_is_default_str:
                update_data['is_default'] = new_is_default_str == 's'

            new_supports_temp_str = Prompt.ask(f"Suporta ajuste de temperatura? (atual: {'s' if current_model.supports_temperature else 'n'}, Enter para manter) (s/n)", choices=["s", "n", ""], default="").lower()
            if new_supports_temp_str:
                update_data['supports_temperature'] = new_supports_temp_str == 's'
            
            new_context_window_str = Prompt.ask(f"Nova Janela de Contexto (atual: {current_model.context_window or 'N/A'}, Enter para manter)", default="").strip()
            if new_context_window_str:
                try:
                    update_data['context_window'] = int(new_context_window_str)
                except ValueError:
                    display_warning(f"Valor '{new_context_window_str}' para janela de contexto é inválido e será ignorado.")

            # 5. If update_data is empty
            if not update_data:
                display_info("Nenhuma alteração fornecida.")
                return

            # 6. Call update_model
            updated_model = self.model_manager.update_model(selected_provider_name, selected_model_name, update_data)

            # 7. Display success or error
            if updated_model:
                display_success(f"Modelo '{updated_model.name}' atualizado com sucesso.")
            else:
                display_error(f"Falha ao atualizar modelo '{selected_model_name}'. Verifique os logs.")
        
        except Exception as e:
            display_error(f"Ocorreu um erro inesperado ao editar o modelo: {e}")

    def _remove_model_ui(self):
        """
        Interface para remover um modelo LLM existente.
        """
        self.console.print(Panel(Text("Remover Modelo LLM", justify="center", style="bold green")))

        try:
            # 1. Select Provider
            providers = self.model_manager.get_available_providers()
            if not providers:
                display_warning("Nenhum provider com modelos encontrado.")
                return

            display_info("Providers disponíveis:")
            provider_map = {}
            provider_table = Table(title="Providers", box=SIMPLE_HEAVY)
            provider_table.add_column("ID", style="dim", width=5, justify="center")
            provider_table.add_column("Nome do Provider", style="cyan", min_width=20)

            for i, provider_name in enumerate(providers, 1):
                provider_table.add_row(str(i), provider_name)
                provider_map[str(i)] = provider_name
            
            self.console.print(provider_table)
            
            provider_choice = Prompt.ask("Escolha um provider pelo número ou 'v' para voltar", choices=list(provider_map.keys()) + ['v'], show_choices=False)

            if provider_choice.lower() == 'v':
                return
            
            selected_provider_name = provider_map.get(provider_choice)
            if not selected_provider_name:
                display_error("Seleção de provider inválida.")
                return

            # 2. Select Model from Provider
            models: List[Model] = self.model_manager.get_models_for_provider(selected_provider_name)
            if not models:
                display_warning(f"Nenhum modelo encontrado para o provider '{selected_provider_name}'.")
                return

            display_info(f"Modelos disponíveis para o provider '{selected_provider_name}':")
            model_map = {}
            model_table = Table(title=f"Modelos em {selected_provider_name}", box=SIMPLE_HEAVY)
            model_table.add_column("ID", style="dim", width=5, justify="center")
            model_table.add_column("Nome", style="cyan", min_width=20)
            model_table.add_column("Descrição", style="magenta", min_width=30, overflow="ellipsis")

            for i, model_obj in enumerate(models, 1):
                model_table.add_row(str(i), model_obj.name, model_obj.description or "N/A")
                model_map[str(i)] = model_obj.name # Store the model name
            
            self.console.print(model_table)
            
            model_choice = Prompt.ask("Escolha um modelo pelo ID para remover ou 'v' para voltar", choices=list(model_map.keys()) + ['v'], show_choices=False)

            if model_choice.lower() == 'v':
                return

            selected_model_name = model_map.get(model_choice)
            if not selected_model_name:
                display_error("Seleção de modelo inválida.")
                return

            # 3. Confirmation
            confirm = Prompt.ask(
                f"Tem certeza que deseja remover o modelo '[bold yellow]{selected_model_name}[/bold yellow]' do provider '[bold cyan]{selected_provider_name}[/bold cyan]'? (s/n)",
                choices=["s", "n"],
                default="n"
            )

            if confirm.lower() != 's':
                display_warning("Remoção cancelada.")
                return

            # 4. Call remove_model
            success = self.model_manager.remove_model(selected_provider_name, selected_model_name)

            # 5. Display success or error
            if success:
                display_success(f"Modelo '{selected_model_name}' removido com sucesso do provider '{selected_provider_name}'.")
            else:
                display_error(f"Falha ao remover o modelo '{selected_model_name}'. Verifique os logs.")
        
        except Exception as e:
            display_error(f"Ocorreu um erro inesperado ao remover o modelo: {e}")

    def _import_models_ui(self):
        """
        Interface para importar modelos LLM de um arquivo JSON.
        """
        self.console.print(Panel(Text("Importar Modelos LLM de Arquivo JSON", justify="center", style="bold green")))

        try:
            file_path_str = Prompt.ask("Caminho completo para o arquivo JSON de modelos")
            if not file_path_str.strip():
                display_error("Caminho do arquivo não pode ser vazio.")
                return
            
            file_path = Path(file_path_str.strip())

            if not file_path.is_file():
                display_error(f"Arquivo não encontrado: {file_path}")
                return

            default_provider_str = Prompt.ask("Nome do Provider padrão (opcional, deixe em branco se o JSON já especifica providers)").strip()
            default_provider = default_provider_str if default_provider_str else None
            
            merge_str = Prompt.ask(
                "Mesclar com modelos existentes? (s/n) (s=mesclar, n=sobrescrever conflitantes no mesmo provider)",
                choices=["s", "n"],
                default="s"
            )
            merge_bool = merge_str.lower() == 's'

            success = self.model_manager.import_models(
                file_path=file_path,
                default_provider=default_provider,
                merge=merge_bool
            )

            if success:
                display_success(f"Modelos importados com sucesso de '{file_path}'.")
            else:
                display_error(f"Falha ao importar modelos de '{file_path}'. Verifique o formato do arquivo e os logs.")

        except json.JSONDecodeError as jde:
            display_error(f"Erro ao decodificar o arquivo JSON: {file_path}. Detalhes: {jde}")
        except FileNotFoundError: # Should be caught by is_file() check, but good to have
             display_error(f"Arquivo não encontrado: {file_path}")
        except Exception as e:
            display_error(f"Ocorreu um erro inesperado ao importar modelos: {e}")

    def _export_models_ui(self):
        """
        Interface para exportar modelos LLM para um arquivo JSON.
        """
        self.console.print(Panel(Text("Exportar Modelos LLM para Arquivo JSON", justify="center", style="bold green")))

        try:
            provider_name_input = Prompt.ask("Nome do Provider para exportar (deixe em branco para todos os providers)")
            provider_name_or_none = provider_name_input.strip() if provider_name_input.strip() else None

            exported_data = self.model_manager.export_models(provider_name_or_none)

            if not exported_data:
                if provider_name_or_none:
                    display_warning(f"Nenhum modelo encontrado para o provider '{provider_name_or_none}' para exportar.")
                else:
                    display_warning("Nenhum modelo encontrado em nenhum provider para exportar.")
                return

            file_path_str = Prompt.ask("Caminho completo para salvar o arquivo JSON (ex: /caminho/para/modelos_exportados.json)")
            if not file_path_str.strip():
                display_error("Caminho do arquivo não pode ser vazio.")
                return
            
            file_path = Path(file_path_str.strip())

            # Ensure parent directory exists
            try:
                file_path.parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                display_error(f"Erro ao criar diretório pai para '{file_path}': {e}")
                return

            try:
                save_json(file_path, exported_data)
                display_success(f"Modelos exportados com sucesso para '{file_path}'.")
            except Exception as e:
                display_error(f"Erro ao salvar arquivo JSON: {e}")

        except Exception as e:
            display_error(f"Ocorreu um erro inesperado ao exportar modelos: {e}")


    def _handle_manage_models(self):
        """
        Lida com a lógica de gerenciar modelos LLM.
        """
        manage_models_options = {
            "1": "Visualizar Modelos por Provider",
            "2": "Adicionar Novo Modelo",
            "3": "Editar Modelo Existente",
            "4": "Remover Modelo",
            "5": "Importar Modelos",
            "6": "Exportar Modelos",
            "7": "Restaurar Modelos Padrões",
            "8": "Voltar ao Menu Principal"
        }

        while True:
            self.console.print(Panel(Text("Gerenciar Modelos LLM", justify="center", style="bold green")))
            
            menu_text = Text()
            for key, value in manage_models_options.items():
                menu_text.append(f"{key}. {value}\n", style="white")
            self.console.print(menu_text)

            choice = Prompt.ask("Escolha uma opção", choices=list(manage_models_options.keys()), show_choices=False)

            if choice == "1": # Visualizar Modelos por Provider
                self._view_models_by_provider()
            elif choice == "2": # Adicionar Novo Modelo
                self._add_new_model_ui() 
            elif choice == "3": # Editar Modelo Existente
                self._edit_existing_model_ui()
            elif choice == "4": # Remover Modelo
                self._remove_model_ui()
            elif choice == "5": # Importar Modelos
                self._import_models_ui()
            elif choice == "6": # Exportar Modelos
                self._export_models_ui() # INTEGRATION POINT
            elif choice == "7": # Restaurar Modelos Padrões
                self._restore_default_models()
            elif choice == "8": # Voltar
                break
            else:
                display_error("Opção inválida. Tente novamente.")
            
            if choice != "8":
                Prompt.ask("\nPressione Enter para continuar...")

    def _view_models_by_provider(self):
        """
        Permite ao usuário selecionar um provider e visualizar seus modelos.
        """
        self.console.print(Panel(Text("Visualizar Modelos por Provider", justify="center", style="bold green")))
        
        try:
            providers = self.model_manager.get_available_providers() 
        except FileNotFoundError: 
            display_warning(f"Diretório de modelos ({self.models_dir}) não encontrado ou inacessível.")
            return
        except Exception as e:
            display_error(f"Erro ao listar providers: {e}")
            return

        if not providers:
            display_warning("Nenhum provider (arquivo de modelo) encontrado. Você pode adicionar modelos para criar novos providers.")
            return

        display_info("Providers disponíveis:")
        provider_map = {}
        for i, provider_name in enumerate(providers, 1):
            self.console.print(f"{i}. {provider_name}")
            provider_map[str(i)] = provider_name
        
        provider_choice = Prompt.ask("Escolha um provider pelo número ou 'v' para voltar", choices=list(provider_map.keys()) + ['v'], show_choices=False)

        if provider_choice.lower() == 'v':
            return

        selected_provider = provider_map.get(provider_choice)
        if not selected_provider:
            display_error("Seleção de provider inválida.")
            return

        try:
            models = self.model_manager.get_models_for_provider(selected_provider)
        except Exception as e:
            display_error(f"Erro ao carregar modelos para o provider '{selected_provider}': {e}")
            return

        if not models:
            display_warning(f"Nenhum modelo encontrado para o provider '{selected_provider}'.")
            return

        table = Table(title=f"Modelos para {selected_provider}", box=SIMPLE_HEAVY, show_lines=True)
        table.add_column("Nome", style="cyan", min_width=20)
        table.add_column("Descrição", style="magenta", min_width=30, overflow="ellipsis")
        table.add_column("Provider", style="green", min_width=15) 
        table.add_column("É Padrão?", style="yellow", justify="center")
        table.add_column("Ctx Win", style="blue", justify="center") # Context Window
        table.add_column("Temp?", style="red", justify="center") # Supports Temperature

        for model in models:
            table.add_row(
                model.name,
                model.description or "N/A",
                model.provider, 
                "Sim" if model.is_default else "Não",
                str(model.context_window) if model.context_window is not None else "N/A",
                "Sim" if model.supports_temperature else "Não"
            )
        self.console.print(table)

    def _restore_default_models(self):
        """
        Lida com a restauração dos modelos padrão.
        """
        options = {
            "1": "Restaurar para um Provider Específico",
            "2": "Restaurar Todos os Providers Padrão",
            "3": "Voltar"
        }
        self.console.print(Panel(Text("Restaurar Modelos Padrão", justify="center", style="bold yellow")))
        menu_text = Text()
        for k,v in options.items():
            menu_text.append(f"{k}. {v}\n")
        self.console.print(menu_text)

        choice = Prompt.ask("Escolha uma opção", choices=list(options.keys()), show_choices=False)

        provider_to_restore: Optional[str] = None
        if choice == "1":
            try:
                default_providers = list(self.model_manager.default_models_data.keys())
                if not default_providers:
                    display_warning("Nenhum provider padrão definido nos dados internos.")
                    return

                display_info("Providers padrão que podem ser restaurados:")
                provider_map = {}
                for i, p_name in enumerate(default_providers, 1):
                    self.console.print(f"{i}. {p_name}")
                    provider_map[str(i)] = p_name
                
                p_choice = Prompt.ask("Escolha um provider para restaurar ou 'v' para voltar", choices=list(provider_map.keys()) + ['v'], show_choices=False)
                if p_choice.lower() == 'v':
                    return
                provider_to_restore = provider_map.get(p_choice)
                if not provider_to_restore:
                    display_error("Seleção inválida.")
                    return
                
                confirm_msg = (
                    f"Tem certeza que deseja restaurar os modelos padrão para o provider [bold cyan]{provider_to_restore}[/bold cyan]?\n"
                    "Isso [bold red]SOBRESCREVERÁ[/bold red] quaisquer modelos existentes com o mesmo nome neste provider."
                )

            except Exception as e:
                display_error(f"Erro ao listar providers para restauração: {e}")
                return
        elif choice == "2":
            confirm_msg = (
                "Tem certeza que deseja restaurar todos os modelos para os padrões de fábrica?\n"
                "Isso [bold red]SOBRESCREVERÁ[/bold red] quaisquer modelos existentes com o mesmo nome nos providers padrão."
            )
        elif choice == "3":
            return
        else: 
            display_error("Opção inválida.")
            return

        confirm = Prompt.ask(confirm_msg, choices=["s", "n"], default="n")
        
        if confirm.lower() == 's':
            try:
                if self.model_manager.restore_defaults(provider_name=provider_to_restore):
                    if provider_to_restore:
                        display_success(f"Modelos padrão para o provider '{provider_to_restore}' restaurados com sucesso!")
                    else:
                        display_success("Todos os modelos padrão restaurados com sucesso!")
                else:
                    display_error(f"Falha ao restaurar modelos padrão (o ModelManager retornou False). Verifique os logs.")

            except Exception as e:
                display_error(f"Erro ao restaurar modelos padrão: {e}")
        else:
            display_warning("Restauração cancelada.")


if __name__ == "__main__":
    menu = MenuSystem()
    menu.run()
