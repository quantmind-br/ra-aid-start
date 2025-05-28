"""
Assistentes de Configuração para RA AID Start.

Este módulo define a classe ConfigurationWizard, um assistente interativo
passo a passo para guiar o usuário na criação ou edição de presets de
configuração para a ferramenta. Coleta informações sobre modo de operação,
modelos LLM, ferramentas, logging e outras configurações avançadas.
"""
from typing import Optional, Dict, Any, List
from pathlib import Path
import sys

# Adicionar o diretório raiz do projeto ao sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from ra_aid_start.core.preset_manager import PresetManager
from ra_aid_start.core.model_manager import ModelManager
from ra_aid_start.models.preset import Preset
from ra_aid_start.models.model import Model # Adicionado para type hinting
from ra_aid_start.models.validation import ValidationRules
from ra_aid_start.core.command_builder import CommandBuilder # Adicionado import
from ra_aid_start.ui.display import display_error, display_info, display_success, display_panel, display_warning # Supondo que display existe
from rich.console import Console
from rich.prompt import Prompt, InvalidResponse, Confirm
from rich.text import Text as RichText # Renomeado para evitar conflito com typing.Text
from rich.table import Table
from rich.panel import Panel as RichPanel # Para evitar conflito com display_panel

class ConfigurationWizard:
    """
    Um assistente interativo para criar ou editar configurações de Preset.
    """
    def __init__(self, preset_manager: PresetManager, model_manager: ModelManager, validation_rules: ValidationRules, console: Optional[Console] = None):
        """
        Inicializa o ConfigurationWizard.

        Args:
            preset_manager: Uma instância de PresetManager.
            model_manager: Uma instância de ModelManager.
            validation_rules: Uma instância de ValidationRules.
            console: Uma instância opcional de rich.console.Console.
        """
        self.preset_manager = preset_manager
        self.model_manager = model_manager
        self.validation_rules = validation_rules
        self.console = console or Console()
        self.current_preset_data: Dict[str, Any] = {} # Para armazenar os dados do preset durante a configuração
        self.is_editing: bool = False # Adicionado para rastrear se está editando
        self.original_preset_name: Optional[str] = None # Adicionado para rastrear nome original ao editar

    def _validate_preset_name(self, name: str) -> bool:
        """Valida o nome do preset (não pode estar vazio e não pode existir se for novo)."""
        if not name.strip():
            display_error("O nome do preset não pode estar vazio.")
            return False
        # Adicionar lógica para verificar se o nome já existe se for um novo preset
        # Se estiver editando, o nome pode ser o mesmo.
        # Esta validação pode ser mais complexa dependendo do modo (novo vs editar)
        return True

    def collect_basic_info(self) -> bool:
        """
        Coleta o nome (obrigatório) e a descrição (opcional) para o preset.
        Atualiza self.current_preset_data.
        Retorna True se as informações foram coletadas com sucesso, False caso contrário.
        """
        self.console.print(display_panel("Informações Básicas do Preset", title="[bold sky_blue1]Passo 1 de X[/bold sky_blue1]"))

        # Nome do Preset
        while True:
            name = Prompt.ask("Nome do Preset (obrigatório)")
            if self._validate_preset_name(name):
                self.current_preset_data["name"] = name.strip()
                break
        
        # Descrição do Preset
        description = Prompt.ask("Descrição do Preset (opcional, pressione Enter para pular)", default="")
        self.current_preset_data["description"] = description.strip() # default="" no Prompt.ask garante que é string

        display_info(f"Nome: {self.current_preset_data['name']}, Descrição: {self.current_preset_data['description'] or 'N/A'}")
        return True

    def select_operation_mode(self) -> bool:
        """
        Permite ao usuário selecionar o modo de operação principal para o preset.
        Atualiza self.current_preset_data com a flag correspondente (ex: 'chat_mode': True).
        Retorna True se um modo foi selecionado, False se o usuário optou por cancelar/voltar (se aplicável).
        """
        self.console.print(display_panel("Modo de Operação", title="[bold sky_blue1]Passo 2 de X[/bold sky_blue1]"))

        operation_modes = {
            "1": {"label": "Chat Interativo", "flag_name": "chat_mode", "command_flag": "--chat", "value": "chat"},
            "2": {"label": "Mensagem/Tarefa Única", "flag_name": "message_mode", "command_flag": "--message", "value": "message"},
            "3": {"label": "Arquivo de Texto", "flag_name": "file_mode", "command_flag": "--file", "value": "file"},
            "4": {"label": "Servidor Web (API)", "flag_name": "server_mode", "command_flag": "--server", "value": "server"}
            # Adicionar "5": "Voltar/Cancelar" se quisermos permitir isso aqui
        }
        
        # Resetar flags de modo de operação anteriores
        for mode_details in operation_modes.values():
            if "flag_name" in mode_details: # Garante que apenas entradas com flag_name sejam processadas
                 self.current_preset_data[mode_details["flag_name"]] = False


        options_text = RichText("Selecione o modo de operação principal para este preset:\n\n")
        choices_map = {}
        for key, mode_info in operation_modes.items():
            if "label" in mode_info: # Checa se 'label' existe
                options_text.append(f"{key}. {mode_info['label']}\n")
                choices_map[key] = mode_info
        
        self.console.print(options_text)
        
        # Usar Prompt.ask com as chaves do choices_map como 'choices'
        # Isso também validará a entrada do usuário.
        user_choice_key = Prompt.ask("Escolha uma opção", choices=list(choices_map.keys()))

        selected_mode_info = choices_map.get(user_choice_key)

        if selected_mode_info and "flag_name" in selected_mode_info and "value" in selected_mode_info:
            self.current_preset_data[selected_mode_info["flag_name"]] = True
            self.current_preset_data["operation_mode"] = selected_mode_info["value"]
            # Poderíamos também armazenar o command_flag se for útil diretamente
            # self.current_preset_data["operation_mode_command"] = selected_mode_info["command_flag"]
            display_info(f"Modo de operação selecionado: {selected_mode_info['label']} (valor: {selected_mode_info['value']})")
            return True
        else:
            # Isso não deveria acontecer se Prompt.ask for usado corretamente com 'choices'
            display_error("Seleção de modo de operação inválida.")
            return False

    def _get_active_operation_mode(self) -> Optional[str]:
        """Retorna a string da flag de comando do modo de operação ativo, ou None."""
        # Reutiliza a definição de operation_modes para encontrar a flag ativa
        operation_modes_config = { # Definido aqui para não depender de estar dentro de select_operation_mode
            "chat_mode": "--chat",
            "message_mode": "--message",
            "file_mode": "--file",
            "server_mode": "--server"
        }
        for flag_name, command_flag in operation_modes_config.items():
            if self.current_preset_data.get(flag_name, False):
                return command_flag
        return None

    def configure_conditional_settings(self) -> bool:
        """
        Coleta configurações específicas baseadas no modo de operação principal selecionado.
        Atualiza self.current_preset_data.
        Retorna True se as configurações foram coletadas com sucesso, False caso contrário.
        """
        self.console.print(display_panel("Configurações Específicas do Modo", title="[bold sky_blue1]Passo 3 de X[/bold sky_blue1]"))
        
        active_mode_command = self._get_active_operation_mode()

        if not active_mode_command:
            display_error("Nenhum modo de operação principal ativo. Não é possível configurar definições condicionais.")
            return False

        display_info(f"Configurando para o modo: {active_mode_command}")

        # Durante a edição, preservar flags existentes nas flags do preset
        # Durante criação nova, resetar campos condicionais para evitar persistência de configurações de modos anteriores
        if not self.is_editing:
            # Esta lista deve ser mais completa baseada em todas as flags condicionais possíveis.
            conditional_flags_to_reset = [
                "chat_history_file", "chat_persona_file", "chat_session_id", "cowboy_mode",
                "message_file", "research_only", "task_file",
                "api_host", "api_port", "allow_cors"
            ]
            for flag_key in conditional_flags_to_reset:
                if flag_key in self.current_preset_data: # Remove se existir
                    del self.current_preset_data[flag_key]
                # Ou definir como None/False se preferir manter a chave
                # self.current_preset_data[flag_key] = None


        if active_mode_command == "--chat":
            self.console.print(display_info("Configurações para Modo Chat:"))
            # Garantir que flags existe
            if "flags" not in self.current_preset_data:
                self.current_preset_data["flags"] = {}
            
            # Obter valores padrão das flags existentes se estiver editando
            default_history = self.current_preset_data["flags"].get("chat_history_file", "") if self.is_editing else ""
            default_persona = self.current_preset_data["flags"].get("chat_persona_file", "") if self.is_editing else ""
            default_session = self.current_preset_data["flags"].get("chat_session_id", "") if self.is_editing else ""
            default_cowboy = self.current_preset_data["flags"].get("cowboy_mode", False) if self.is_editing else False
            
            self.current_preset_data["flags"]["chat_history_file"] = Prompt.ask("Arquivo de histórico de chat (opcional)", default=default_history).strip() or None
            self.current_preset_data["flags"]["chat_persona_file"] = Prompt.ask("Arquivo de persona do chat (opcional)", default=default_persona).strip() or None
            self.current_preset_data["flags"]["chat_session_id"] = Prompt.ask("ID da sessão de chat (opcional)", default=default_session).strip() or None
            self.current_preset_data["flags"]["cowboy_mode"] = Confirm.ask("Ativar Modo Cowboy (sem confirmações)?", default=default_cowboy)
        
        elif active_mode_command == "--message" or active_mode_command == "--file":
            self.console.print(display_info(f"Configurações para Modo {active_mode_command}:"))
            # Garantir que flags existe
            if "flags" not in self.current_preset_data:
                self.current_preset_data["flags"] = {}
            
            if active_mode_command == "--message":
                 # Para --message, o próprio texto da mensagem é fornecido na CLI, não configurado aqui.
                 # Mas pode haver flags relacionadas.
                 pass # Nenhuma configuração específica de MENSAGEM no wizard por enquanto, além das gerais.
            
            # Para --file, o nome do arquivo é fornecido na CLI.
            # Flags como --research-only podem ser relevantes para ambos.
            default_research = self.current_preset_data["flags"].get("research_only", False) if self.is_editing else False
            self.current_preset_data["flags"]["research_only"] = Confirm.ask("Ativar Modo Apenas Pesquisa (--research-only)?", default=default_research)
            # self.current_preset_data["task_file"] = Prompt.ask("Arquivo de tarefa (se aplicável, opcional)", default="").strip() or None
            # A flag --task-file é mais uma forma de entrada, como --file, não uma configuração de preset em si.

        elif active_mode_command == "--server":
            self.console.print(display_info("Configurações para Modo Servidor Web:"))
            # Garantir que flags existe
            if "flags" not in self.current_preset_data:
                self.current_preset_data["flags"] = {}
            
            # Obter valores padrão das flags existentes se estiver editando
            default_host = self.current_preset_data["flags"].get("api_host", "127.0.0.1") if self.is_editing else "127.0.0.1"
            default_port = str(self.current_preset_data["flags"].get("api_port", 8000)) if self.is_editing else "8000"
            default_cors = self.current_preset_data["flags"].get("allow_cors", False) if self.is_editing else False
            
            self.current_preset_data["flags"]["api_host"] = Prompt.ask("Host da API", default=default_host).strip()
            # Validar porta como inteiro
            while True:
                port_str = Prompt.ask("Porta da API", default=default_port).strip()
                try:
                    self.current_preset_data["flags"]["api_port"] = int(port_str)
                    if 0 <= self.current_preset_data["flags"]["api_port"] <= 65535:
                        break
                    else:
                        display_error("Porta inválida. Deve ser entre 0 e 65535.")
                except ValueError:
                    display_error("Porta inválida. Deve ser um número inteiro.")
            self.current_preset_data["flags"]["allow_cors"] = Confirm.ask("Permitir CORS (Cross-Origin Resource Sharing)?", default=default_cors)
        
        else:
            display_warning(f"Nenhuma configuração condicional específica para o modo '{active_mode_command}'.")

        display_info("Configurações condicionais coletadas.")
        # self.console.print(self.current_preset_data) # Para depuração
        return True

    def _select_model_for_category(self, category_name_display: str, category_key_prefix: str, is_mandatory: bool) -> bool:
        """
        Auxiliar para selecionar um provedor e um modelo para uma categoria específica.
        Atualiza self.current_preset_data com '{category_key_prefix}_provider' e '{category_key_prefix}_name'.
        Retorna True se um modelo foi selecionado (ou se não era mandatório e o usuário pulou),
        False se era mandatório e o usuário não selecionou, ou se ocorreu um erro.
        """
        self.console.print(f"\nConfigurando modelo [bold]{category_name_display}[/bold]:")

        if not is_mandatory:
            if not Confirm.ask(f"Deseja configurar um modelo {category_name_display}?", default=False):
                # Limpar quaisquer chaves anteriores para esta categoria opcional se o usuário pular
                self.current_preset_data.pop(f"{category_key_prefix}_provider", None)
                self.current_preset_data.pop(f"{category_key_prefix}_name", None)
                display_info(f"Configuração do modelo {category_name_display} pulada.")
                return True # Sucesso ao pular uma etapa opcional

        # Listar Provedores
        providers = self.model_manager.get_available_providers()
        if not providers:
            display_error(f"Nenhum provedor de modelo encontrado para a categoria {category_name_display}.")
            return False if is_mandatory else True # Falha se obrigatório, sucesso se opcional e não há provedores

        provider_choices = {str(i+1): p for i, p in enumerate(providers)}
        provider_options_text = RichText(f"Selecione o provedor para o modelo {category_name_display}:\n")
        for k, v in provider_choices.items():
            provider_options_text.append(f"{k}. {v}\n")
        self.console.print(provider_options_text)
        
        chosen_provider_key = Prompt.ask("Escolha um provedor", choices=list(provider_choices.keys()))
        selected_provider = provider_choices[chosen_provider_key]

        # Listar Modelos do Provedor
        models_from_provider: List[Model] = self.model_manager.get_models_for_provider(selected_provider)
        if not models_from_provider:
            msg = f"Nenhum modelo encontrado para o provedor '{selected_provider}' (categoria: {category_name_display})."
            if is_mandatory:
                display_error(msg)
                return False
            else:
                display_warning(msg + " Pulando esta seleção.")
                # Limpar chaves se o usuário selecionou um provedor mas não há modelos e é opcional
                self.current_preset_data.pop(f"{category_key_prefix}_provider", None)
                self.current_preset_data.pop(f"{category_key_prefix}_name", None)
                return True


        model_choices = {str(i+1): m for i, m in enumerate(models_from_provider)}
        model_options_text = RichText(f"Selecione o modelo do provedor '{selected_provider}' para {category_name_display}:\n")
        for k, v_model in model_choices.items():
            model_options_text.append(f"{k}. {v_model.name}\n")
        self.console.print(model_options_text)

        chosen_model_key = Prompt.ask("Escolha um modelo", choices=list(model_choices.keys()))
        selected_model_obj = model_choices[chosen_model_key]

        self.current_preset_data[f"{category_key_prefix}_provider"] = selected_provider
        self.current_preset_data[f"{category_key_prefix}_name"] = selected_model_obj.name # ou model_id, dependendo do que é usado para identificar
        # Poderia ser útil armazenar o model_id também:
        # self.current_preset_data[f"{category_key_prefix}_model_id"] = selected_model_obj.model_id
        
        display_info(f"Modelo {category_name_display} selecionado: {selected_provider} / {selected_model_obj.name}")
        return True

    def configure_models(self) -> bool:
        """
        Permite ao usuário selecionar modelos LLM (principal, expert, especializados).
        Atualiza self.current_preset_data.
        Retorna True se as configurações foram coletadas com sucesso, False caso contrário.
        """
        self.console.print(display_panel("Configuração de Modelos LLM", title="[bold sky_blue1]Passo 4 de X[/bold sky_blue1]"))

        # Durante criação nova, limpar configurações de modelo anteriores para evitar persistência indesejada
        # Durante edição, preservar configurações existentes
        if not self.is_editing:
            keys_to_clear = [
                "main_model_provider", "main_model_name",
                "expert_model_provider", "expert_model_name",
                "research_provider", "research_name", # Para _select_model_for_category
                "planner_provider", "planner_name"   # Para _select_model_for_category
            ]
            for key in keys_to_clear:
                self.current_preset_data.pop(key, None)

        # Modelo Principal (Obrigatório)
        if not self._select_model_for_category("Principal", "main_model", is_mandatory=True):
            display_error("Falha ao configurar o modelo Principal obrigatório.")
            return False
        
        # Modelo Expert (Opcional)
        if not self._select_model_for_category("Expert (Opcional)", "expert_model", is_mandatory=False):
            display_error("Ocorreu um erro durante a configuração do modelo Expert opcional.")
            return False

        # Modelo de Pesquisa (Opcional)
        if not self._select_model_for_category(
            category_name_display="Pesquisa (Opcional)",
            category_key_prefix="research", # Salvará como research_provider, research_name
            is_mandatory=False
        ):
            display_error("Ocorreu um erro durante a configuração do modelo de Pesquisa opcional.")
            return False # Erro na função, não que o usuário pulou

        # Modelo de Planejamento (Opcional)
        if not self._select_model_for_category(
            category_name_display="Planejamento (Opcional)",
            category_key_prefix="planner", # Salvará como planner_provider, planner_name
            is_mandatory=False
        ):
            display_error("Ocorreu um erro durante a configuração do modelo de Planejamento opcional.")
            return False # Erro na função, não que o usuário pulou

        display_info("Configuração de modelos LLM concluída.")
        # self.console.print(self.current_preset_data) # Para depuração
        return True

    def configure_tools(self) -> bool:
        """
        Configura flags relacionadas a ferramentas de desenvolvimento.
        Atualiza self.current_preset_data.
        Retorna True se as configurações foram coletadas com sucesso, False caso contrário.
        """
        self.console.print(display_panel("Configuração de Ferramentas de Desenvolvimento", title="[bold sky_blue1]Passo 5 de X[/bold sky_blue1]"))

        # Limpar/inicializar chaves de ferramentas
        tool_keys_to_clear = [
            "use_aider", "aider_config", "custom_tools",
            "test_cmd", "auto_test"
        ]
        for key in tool_keys_to_clear:
            self.current_preset_data.pop(key, None)

        # Integração Aider
        self.current_preset_data["use_aider"] = Confirm.ask("Deseja usar integração com Aider (--use-aider)?", default=False)
        if self.current_preset_data["use_aider"]:
            self.current_preset_data["aider_config"] = Prompt.ask("Caminho para o arquivo de configuração do Aider (--aider-config, opcional)", default="").strip() or None
        else:
            self.current_preset_data["aider_config"] = None # Garante que é None se use_aider for False

        # Ferramentas Customizadas
        self.current_preset_data["custom_tools"] = Prompt.ask("Caminho para ferramentas customizadas (--custom-tools, opcional, ex: path/to/tools.py)", default="").strip() or None

        # Testes Automatizados
        self.current_preset_data["test_cmd"] = Prompt.ask("Comando para executar testes (--test-cmd, opcional, ex: pytest -k my_test)", default="").strip() or None
        if self.current_preset_data["test_cmd"]: # Só pergunta por auto-test se um test-cmd foi fornecido
            self.current_preset_data["auto_test"] = Confirm.ask("Executar testes automaticamente após cada modificação (--auto-test)?", default=False)
        else:
            self.current_preset_data["auto_test"] = False # Garante que é False se não houver test_cmd

        display_info("Configuração de ferramentas de desenvolvimento concluída.")
        # self.console.print(self.current_preset_data) # Para depuração
        return True

    def configure_display(self) -> bool:
        """
        Configura flags relacionadas à exibição de informações durante a execução.
        Atualiza self.current_preset_data.
        Retorna True se as configurações foram coletadas com sucesso.
        """
        self.console.print(display_panel("Configurações de Exibição", title="[bold sky_blue1]Passo 6A de X[/bold sky_blue1]")) # Marcando como 6A

        display_keys_to_clear = ["show_cost", "show_thoughts"]
        for key in display_keys_to_clear:
            self.current_preset_data.pop(key, None)

        self.current_preset_data["show_cost"] = Confirm.ask("Mostrar rastreamento de custo (--show-cost)?", default=False)
        self.current_preset_data["show_thoughts"] = Confirm.ask("Mostrar pensamentos do modelo (--show-thoughts)?", default=False)
        
        display_info("Configurações de exibição concluídas.")
        return True

    def configure_logging(self) -> bool:
        """
        Configura flags relacionadas ao logging.
        Atualiza self.current_preset_data.
        Retorna True se as configurações foram coletadas com sucesso.
        """
        self.console.print(display_panel("Configurações de Logging", title="[bold sky_blue1]Passo 6B de X[/bold sky_blue1]")) # Marcando como 6B

        logging_keys_to_clear = ["log_mode", "log_level", "pretty_logger", "log_file"]
        for key in logging_keys_to_clear:
            self.current_preset_data.pop(key, None)

        # Log Mode
        log_mode_choices = ["stdout", "stderr", "file", "dual", "none"]
        self.current_preset_data["log_mode"] = Prompt.ask(
            "Modo de logging (--log-mode)",
            choices=log_mode_choices,
            default="stdout"
        )

        # Log Level
        log_level_choices = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        self.current_preset_data["log_level"] = Prompt.ask(
            "Nível de logging (--log-level)",
            choices=log_level_choices,
            default="INFO"
        ).upper() # Garantir que seja maiúsculo como nas flags

        # Pretty Logger
        self.current_preset_data["pretty_logger"] = Confirm.ask("Usar logger formatado/bonito (--pretty-logger)?", default=True)

        # Log File (condicional)
        if self.current_preset_data["log_mode"] in ["file", "dual"]:
            self.current_preset_data["log_file"] = Prompt.ask(
                "Caminho para o arquivo de log (--log-file, opcional se modo 'file' ou 'dual')",
                default="ra_aid.log" # Sugerir um padrão
            ).strip() or "ra_aid.log" # Garante um valor se deixado em branco após sugestão
        else:
            self.current_preset_data["log_file"] = None
            
        display_info("Configurações de logging concluídas.")
        return True

    def _ask_for_numeric_value(self, prompt_text: str, value_type: type, key: str, min_val: Optional[float] = None, max_val: Optional[float] = None, default_val_str: str = "") -> bool:
        """
        Auxiliar para pedir um valor numérico (int ou float), validar e armazenar.
        Retorna True se o valor foi definido ou pulado, False em caso de erro de entrada persistente.
        """
        while True:
            val_str = Prompt.ask(f"{prompt_text} (opcional, Enter para pular)", default=default_val_str).strip()
            if not val_str:
                self.current_preset_data[key] = None
                return True
            try:
                value = value_type(val_str)
                if min_val is not None and value < min_val:
                    display_error(f"Valor deve ser maior ou igual a {min_val}.")
                    continue
                if max_val is not None and value > max_val:
                    display_error(f"Valor deve ser menor ou igual a {max_val}.")
                    continue
                self.current_preset_data[key] = value
                return True
            except ValueError:
                display_error(f"Entrada inválida. Por favor, insira um número {value_type.__name__} válido.")
            # Adicionar uma forma de sair do loop se o usuário não conseguir fornecer valor válido?
            # Por enquanto, assume que o usuário corrigirá ou pulará.

    def configure_advanced(self) -> bool:
        """
        Coleta configurações avançadas diversas.
        Atualiza self.current_preset_data.
        Retorna True se as configurações foram coletadas com sucesso.
        """
        self.console.print(display_panel("Configurações Avançadas", title="[bold sky_blue1]Passo 7 de X[/bold sky_blue1]"))

        advanced_keys_to_clear = [
            "recursion_limit", "project_state_dir", "wipe_project_memory", "reasoning_assistance",
            "max_total_tokens", "max_input_tokens", "max_output_tokens",
            "temperature", "top_p", "top_k", "frequency_penalty", "presence_penalty"
        ]
        for key in advanced_keys_to_clear:
            self.current_preset_data.pop(key, None)

        # Perguntar se o usuário deseja configurar as opções avançadas
        if not Confirm.ask("Deseja configurar opções avançadas (limites, parâmetros de modelo, etc.)?", default=False):
            display_info("Configurações avançadas puladas.")
            return True

        # Limites e Diretórios
        if not self._ask_for_numeric_value("Limite de recursão (--recursion-limit)", int, "recursion_limit", min_val=0): return False
        
        project_state_dir_val = Prompt.ask("Diretório de estado do projeto (--project-state-dir, opcional)", default="").strip()
        self.current_preset_data["project_state_dir"] = project_state_dir_val or None
        
        self.current_preset_data["wipe_project_memory"] = Confirm.ask("Limpar memória do projeto ao iniciar (--wipe-project-memory)?", default=False)
        self.current_preset_data["reasoning_assistance"] = Confirm.ask("Habilitar assistência de raciocínio (--reasoning-assistance)?", default=False)

        # Limites de Tokens
        self.console.print(RichText("\nLimites de Tokens (opcional):", style="bold cyan"))
        if not self._ask_for_numeric_value("Máximo de tokens totais (--max-total-tokens)", int, "max_total_tokens", min_val=1): return False
        if not self._ask_for_numeric_value("Máximo de tokens de entrada (--max-input-tokens)", int, "max_input_tokens", min_val=1): return False
        if not self._ask_for_numeric_value("Máximo de tokens de saída (--max-output-tokens)", int, "max_output_tokens", min_val=1): return False

        # Parâmetros de Geração do Modelo
        self.console.print(RichText("\nParâmetros de Geração do Modelo (opcional):", style="bold cyan"))
        if not self._ask_for_numeric_value("Temperatura (--temperature, 0.0-2.0)", float, "temperature", min_val=0.0, max_val=2.0): return False
        if not self._ask_for_numeric_value("Top P (--top-p, 0.0-1.0)", float, "top_p", min_val=0.0, max_val=1.0): return False
        if not self._ask_for_numeric_value("Top K (--top-k)", int, "top_k", min_val=0): return False
        if not self._ask_for_numeric_value("Penalidade de Frequência (--frequency-penalty, -2.0-2.0)", float, "frequency_penalty", min_val=-2.0, max_val=2.0): return False
        if not self._ask_for_numeric_value("Penalidade de Presença (--presence-penalty, -2.0-2.0)", float, "presence_penalty", min_val=-2.0, max_val=2.0): return False

        display_info("Configurações avançadas concluídas.")
        return True

    def start_wizard(self, existing_preset_name: Optional[str] = None) -> Optional[Preset]:
        """
        Inicia o assistente de configuração para criar um novo preset ou editar um existente.

        Args:
            existing_preset_name: O nome de um preset existente para editar. Se None, um novo preset será criado.

        Returns:
            Um objeto Preset configurado ou None se o processo for cancelado.
        """
        if existing_preset_name:
            self.console.print(display_info(f"Editando preset existente: {existing_preset_name}"))
            # Lógica para carregar dados do preset existente em self.current_preset_data
            preset_to_edit = self.preset_manager.get_preset(existing_preset_name)
            if preset_to_edit:
                self.current_preset_data = preset_to_edit.model_dump() # Usar model_dump para Pydantic v2+
                self.is_editing = True
                self.original_preset_name = existing_preset_name
            else:
                display_error(f"Preset '{existing_preset_name}' não encontrado.")
                return None
        else:
            self.console.print(display_info("Iniciando assistente para criar novo preset..."))
            self.current_preset_data = {} # Começa com dados vazios para um novo preset
            self.is_editing = False
            self.original_preset_name = None

        # Placeholder para os passos do wizard
        if not self.collect_basic_info():
            display_error("Falha ao coletar informações básicas. Assistente cancelado.")
            return None
        display_success("Passo 1: Informações Básicas concluídas.")
        
        if not self.select_operation_mode():
            display_error("Falha ao selecionar o modo de operação. Assistente cancelado.")
            return None
        display_success("Passo 2: Modo de Operação concluído.")

        if not self.configure_conditional_settings():
            display_error("Falha ao configurar definições condicionais. Assistente cancelado.")
            return None
        display_success("Passo 3: Configurações Específicas do Modo concluídas.")
        
        if not self.configure_models():
            display_error("Falha ao configurar os modelos LLM. Assistente cancelado.")
            return None
        display_success("Passo 4: Configuração de Modelos LLM concluída.")
        
        if not self.configure_tools():
            display_error("Falha ao configurar as ferramentas de desenvolvimento. Assistente cancelado.")
            return None
        display_success("Passo 5: Configuração de Ferramentas concluída.")
        
        if not self.configure_display():
            display_error("Falha ao configurar as definições de exibição. Assistente cancelado.")
            return None
        display_success("Passo 6A: Configurações de Exibição concluídas.")

        if not self.configure_logging():
            display_error("Falha ao configurar as definições de logging. Assistente cancelado.")
            return None
        display_success("Passo 6B: Configurações de Logging concluídas.")
            
        if not self.configure_advanced():
            display_error("Falha ao configurar as definições avançadas. Assistente cancelado.")
            return None
        display_success("Passo 7: Configurações Avançadas concluídas.")

        # 8. Sumário, Validação e Confirmação
        if self.show_summary_and_confirm():
            # Se o usuário confirmou, tentamos criar e salvar o Preset
            try:
                self.console.print(f"DEBUG WIZARD (ALL FLOWS): current_preset_data before Preset creation: {self.current_preset_data}") # DEBUG Renomeado e mantido
                self.console.print(f"DEBUG WIZARD (ALL FLOWS): flags in current_preset_data for Preset creation: {self.current_preset_data.get('flags')}") # DEBUG ADICIONADO
                final_preset_obj = Preset(**self.current_preset_data)
                
                if self.is_editing and self.original_preset_name and final_preset_obj.name != self.original_preset_name:
                    # Caso de edição com renomeação
                    if self.preset_manager.save_preset(final_preset_obj): # Salva com o novo nome
                        # Se o salvamento com novo nome for bem-sucedido, exclui o antigo
                        if self.preset_manager.delete_preset(self.original_preset_name):
                            display_success(f"Preset '{self.original_preset_name}' renomeado para '{final_preset_obj.name}' e salvo com sucesso!")
                        else:
                            # O novo foi salvo, mas o antigo não pôde ser excluído. Isso é um estado parcial.
                            display_warning(f"Preset salvo como '{final_preset_obj.name}', mas falha ao excluir o preset original '{self.original_preset_name}'.")
                        return final_preset_obj
                    else:
                        display_error(f"Falha ao salvar o preset renomeado '{final_preset_obj.name}'.")
                        return None
                else:
                    # Caso de criação de novo preset ou edição sem renomeação
                    if self.preset_manager.save_preset(final_preset_obj):
                        display_success(f"Preset '{final_preset_obj.name}' salvo com sucesso!")
                        return final_preset_obj
                    else:
                        display_error(f"Falha ao salvar o preset '{final_preset_obj.name}'.")
                        return None

            except Exception as e: # Captura ValidationError do Pydantic e outros
                display_error(f"Erro de validação ao criar o Preset: {e}")
                # Aqui, poderíamos oferecer ao usuário a chance de voltar e corrigir,
                # mas por enquanto, o wizard falha.
                return None
        else:
            # Usuário cancelou no sumário ou a validação falhou e ele não quis continuar (se essa lógica estiver em show_summary_and_confirm)
            display_warning("Criação/edição do preset cancelada pelo usuário ou devido a erros de validação não resolvidos.")
            return None

    def show_summary_and_confirm(self) -> bool:
        """
        Exibe um sumário de todas as configurações coletadas e pede confirmação final ao usuário.
        """
        self.console.print(RichPanel("[bold cyan]Sumário do Preset[/bold cyan]", title="Sumário e Confirmação", expand=False, padding=(1,2)))
        
        summary_table = Table(title="Configurações do Preset", show_header=True, header_style="bold magenta")
        summary_table.add_column("Configuração", style="dim cyan", width=30)
        summary_table.add_column("Valor", style="white")

        # Ordenar para melhor visualização
        sorted_data = dict(sorted(self.current_preset_data.items()))

        for key, value in sorted_data.items():
            if value is not None: # Não mostrar valores None
                if isinstance(value, list) or isinstance(value, dict):
                    if not value: # Não mostrar listas/dicionários vazios
                        continue
                    summary_table.add_row(key, str(value))
                elif isinstance(value, bool):
                    summary_table.add_row(key, "[green]Sim[/green]" if value else "[red]Não[/red]")
                else:
                    summary_table.add_row(key, str(value))
        
        if not summary_table.rows:
            display_warning("Nenhuma configuração para exibir no sumário.")
        else:
            self.console.print(summary_table)

        # Gerar e exibir preview do comando usando CommandBuilder
        self.console.print("\n[bold steel_blue]Preview do Comando Gerado:[/bold steel_blue]")
        
        preview_command_str = "[italic red]Preview indisponível: dados insuficientes.[/italic red]"
        preset_name_for_preview = self.current_preset_data.get("name")
        operation_mode_for_preview = self.current_preset_data.get("operation_mode")
        
        flags_for_builder: Dict[str, Any] = {}

        if "flags" in self.current_preset_data:
            for flag_key, flag_val in self.current_preset_data["flags"].items():
                if flag_val is not None:
                    if isinstance(flag_val, bool) and not flag_val:
                        continue
                    flags_for_builder[flag_key] = flag_val
        
        if self.current_preset_data.get("main_model_provider") and self.current_preset_data.get("main_model_name"):
            flags_for_builder["main_model"] = f"{self.current_preset_data['main_model_provider']}:{self.current_preset_data['main_model_name']}"
        
        if self.current_preset_data.get("expert_model_provider") and self.current_preset_data.get("expert_model_name"):
            flags_for_builder["expert_model"] = f"{self.current_preset_data['expert_model_provider']}:{self.current_preset_data['expert_model_name']}"
        
        # Modelo de Pesquisa
        if self.current_preset_data.get("research_provider") and self.current_preset_data.get("research_name"):
            flags_for_builder["research_provider"] = self.current_preset_data["research_provider"]
            flags_for_builder["research_model"] = self.current_preset_data["research_name"]

        # Modelo de Planejamento
        if self.current_preset_data.get("planner_provider") and self.current_preset_data.get("planner_name"):
            flags_for_builder["planner_provider"] = self.current_preset_data["planner_provider"]
            flags_for_builder["planner_model"] = self.current_preset_data["planner_name"]

        direct_mapping_keys = [
            "log_mode", "log_level", "pretty_logger", "log_file",
            "show_cost", "show_thoughts",
            "use_aider", "aider_config", "custom_tools", "test_cmd", "auto_test"
        ]
        for key in direct_mapping_keys:
            value = self.current_preset_data.get(key)
            if value is not None:
                if isinstance(value, bool) and not value:
                    continue
                flags_for_builder[key] = value
        
        if preset_name_for_preview and operation_mode_for_preview:
            temp_preset_dict = {
                "name": preset_name_for_preview,
                "description": self.current_preset_data.get("description", ""),
                "operation_mode": operation_mode_for_preview,
                "flags": flags_for_builder,
            }
            try:
                temp_preset_obj = Preset(**temp_preset_dict)
                builder = CommandBuilder()
                preview_command_str = builder.build_command_from_preset(temp_preset_obj)
            except Exception as e:
                preview_command_str = f"[italic red]Erro ao gerar preview do comando: {e}[/italic red]"
        
        self.console.print(RichText(preview_command_str, style="mono"))

        return Confirm.ask(
            "\n[bold]As configurações acima estão corretas e você deseja salvar este preset?[/bold]",
            default=True,
            console=self.console
        )

if __name__ == '__main__':
    # Configuração para teste local
    console_test = Console()
    base_dir_test = Path.home() / ".ra-aid-start-test-wizard"
    presets_dir_test = base_dir_test / "presets"
    models_dir_test = base_dir_test / "models"
    
    presets_dir_test.mkdir(parents=True, exist_ok=True)
    models_dir_test.mkdir(parents=True, exist_ok=True)

    pm = PresetManager(storage_dir=presets_dir_test)
    mm = ModelManager(storage_dir=models_dir_test)
    vr = ValidationRules() # Instanciar ValidationRules

    wizard = ConfigurationWizard(preset_manager=pm, model_manager=mm, validation_rules=vr, console=console_test)

    # --- Mocking para ModelManager (para testes mais robustos de configure_models) ---
    class MockModel(Model): # Definir MockModel aqui se não estiver globalmente acessível
        pass

    original_get_providers = mm.get_available_providers
    original_get_models = mm.get_models_for_provider

    def mock_get_providers_main_test() -> List[str]:
        return ["OpenAI_Test", "Anthropic_Test"]

    def mock_get_models_main_test(provider_name: str) -> List[Model]:
        if provider_name == "OpenAI_Test":
            return [
                MockModel(name="gpt-4o-test", model_id="openai/gpt-4o-test", provider="OpenAI_Test", can_tools=True),
                MockModel(name="gpt-3.5-turbo-test", model_id="openai/gpt-3.5-turbo-test", provider="OpenAI_Test")
            ]
        if provider_name == "Anthropic_Test":
            return [MockModel(name="claude-3-opus-test", model_id="anthropic/claude-3-opus-test", provider="Anthropic_Test")]
        return []
    # --- Fim do Mocking para ModelManager ---


    # Teste do fluxo completo do wizard com mocks de input
    console_test.print("\n[bold yellow]--- Testando fluxo completo do wizard (Criação) ---[/bold yellow]")
    
    # Salvar Prompt.ask e Confirm.ask originais
    original_prompt_ask_main = Prompt.ask
    original_confirm_ask_main = Confirm.ask

    # Mock de inputs para um fluxo de criação
    mock_wizard_inputs = iter([
        "Meu Preset Teste Wizard", # Nome
        "Descrição do preset de teste via wizard", # Descrição
        "1", # Modo Chat
        "chat_history.txt", # Histórico
        "chat_persona.txt", # Persona
        "sessao123", # ID Sessão
        "n", # Cowboy mode (Não)
        # configure_models
        "y", # Configurar modelo principal (sim, pois é obrigatório) - este prompt não existe mais, é direto
        "1", # Provedor OpenAI_Test
        "1", # Modelo gpt-4o-test
        "y", # Configurar modelo expert? (Sim)
        "2", # Provedor Anthropic_Test
        "1", # Modelo claude-3-opus-test
        "n", # Configurar modelos especializados? (Não)
        # configure_tools
        "y", # Usar Aider? (Sim)
        "aider_conf.yml", # Aider config
        "custom_tools.py", # Custom tools
        "pytest", # Test command
        "y", # Auto-test? (Sim)
        # configure_display
        "y", # Show cost? (Sim)
        "n", # Show thoughts? (Não)
        # configure_logging
        "dual", # Log mode
        "DEBUG", # Log level
        "y", # Pretty logger? (Sim)
        "app_wizard.log", # Log file
        # configure_advanced
        "y", # Configurar avançadas? (Sim)
        "5", # Recursion limit
        "/tmp/wizard_state", # Project state dir
        "y", # Wipe project memory? (Sim)
        "n", # Reasoning assistance? (Não)
        "8000", # Max total tokens
        "6000", # Max input tokens
        "2000", # Max output tokens
        "0.8", # Temperature
        "0.95", # Top P
        "50", # Top K
        "0.1", # Freq penalty
        "0.2", # Pres penalty
        # show_summary_and_confirm
        "y"  # Confirmar para salvar? (Sim)
    ])

    def mocked_prompt_ask_main_flow(prompt_text: str, choices: Optional[List[str]] = None, default: Optional[str] = None, **kwargs: Any) -> str:
        try:
            next_val = next(mock_wizard_inputs)
            console_test.print(f"[dim]Mock Ask: '{prompt_text}' (Choices: {choices}, Default: {default}) -> Resposta: '{next_val}'[/dim]")
            # Simular validação de choices se houver
            if choices and next_val not in choices:
                # Isso pode acontecer se o mock não estiver alinhado com as opções reais
                # Para um teste robusto, isso deveria ser um erro ou o mock deveria ser mais inteligente.
                # Por simplicidade, aqui apenas logamos e retornamos o valor mockado.
                console_test.print(f"[bold red]Alerta de Mock: Resposta '{next_val}' não está nas escolhas {choices} para '{prompt_text}'[/bold red]")
            return next_val
        except StopIteration:
            console_test.print(f"[bold red]Mock Ask: Fim dos inputs mockados para '{prompt_text}'. Usando default ou primeira escolha.[/bold red]")
            if default is not None: return default
            if choices: return choices[0]
            return "fallback_mock_value"
            
    def mocked_confirm_ask_main_flow(prompt_text: str, default: bool = False, **kwargs: Any) -> bool:
        try:
            next_val_str = next(mock_wizard_inputs)
            next_val_bool = next_val_str.lower() in ['y', 'yes', 'true']
            console_test.print(f"[dim]Mock Confirm: '{prompt_text}' (Default: {default}) -> Resposta: '{next_val_str}' ({next_val_bool})[/dim]")
            return next_val_bool
        except StopIteration:
            console_test.print(f"[bold red]Mock Confirm: Fim dos inputs mockados para '{prompt_text}'. Usando default.[/bold red]")
            return default

    Prompt.ask = mocked_prompt_ask_main_flow # type: ignore
    Confirm.ask = mocked_confirm_ask_main_flow # type: ignore
    mm.get_available_providers = mock_get_providers_main_test
    mm.get_models_for_provider = mock_get_models_main_test


    created_preset = wizard.start_wizard()
    if created_preset:
        console_test.print(f"\n[bold green]Preset de teste do wizard criado com sucesso: '{created_preset.name}'[/bold green]")
        console_test.print(created_preset.model_dump_json(indent=2))
        
        # Verificar alguns valores esperados
        assert created_preset.name == "Meu Preset Teste Wizard"
        assert created_preset.chat_mode is True
        assert created_preset.main_model_provider == "OpenAI_Test"
        assert created_preset.main_model_name == "gpt-4o-test"
        assert created_preset.temperature == 0.8
        assert created_preset.log_file == "app_wizard.log"

        # Testar edição
        console_test.print("\n[bold yellow]--- Testando fluxo completo do wizard (Edição) ---[/bold yellow]")
        mock_edit_inputs = iter([
            "Meu Preset Editado", # Novo nome
            "Descrição editada.", # Nova descrição
            # ... (outros inputs podem ser 'n' para pular ou novos valores)
            # Para simplificar, vamos assumir que o usuário só muda nome e descrição e confirma
            # Os prompts para cada etapa ainda serão chamados, então precisamos fornecer 'n' ou valores padrão
            "1", # Modo Chat (manter)
            "", # Histórico (pular)
            "", # Persona (pular)
            "", # ID Sessão (pular)
            "n", # Cowboy (Não)
            # configure_models (manter os mesmos)
            "1", # Provedor OpenAI_Test
            "1", # Modelo gpt-4o-test
            "n", # Não configurar expert
            "n", # Não configurar especializados
            # configure_tools (manter os mesmos)
            "n", # Não usar Aider
            "",  # Custom tools (pular)
            "",  # Test command (pular)
            # configure_display (manter)
            "n", # Show cost (Não)
            "n", # Show thoughts (Não)
            # configure_logging (manter)
            "stdout", # Log mode
            "INFO", # Log level
            "n", # Pretty logger (Não)
            # configure_advanced (pular)
            "n", # Não configurar avançadas
            # show_summary_and_confirm
            "y"  # Confirmar para salvar? (Sim)
        ])
        
        # Resetar o iterador de mock_wizard_inputs para os inputs de edição
        mock_wizard_inputs = mock_edit_inputs

        edited_preset = wizard.start_wizard(existing_preset_name="Meu Preset Teste Wizard")
        if edited_preset:
            console_test.print(f"\n[bold green]Preset editado com sucesso: '{edited_preset.name}'[/bold green]")
            console_test.print(edited_preset.model_dump_json(indent=2))
            assert edited_preset.name == "Meu Preset Editado"
            assert edited_preset.description == "Descrição editada."
            assert pm.get_preset("Meu Preset Teste Wizard") is None # Original deve ter sido removido
            assert pm.get_preset("Meu Preset Editado") is not None
        else:
            console_test.print("[bold red]Falha ao editar o preset de teste do wizard.[/bold red]")

    else:
        console_test.print("[bold red]Falha ao criar o preset de teste do wizard.[/bold red]")

    # Restaurar funções originais
    Prompt.ask = original_prompt_ask_main # type: ignore
    Confirm.ask = original_confirm_ask_main # type: ignore
    mm.get_available_providers = original_get_providers
    mm.get_models_for_provider = original_get_models


    # Limpar diretórios de teste
    # import shutil
    # if base_dir_test.exists():
    #     console_test.print(f"\nLimpando diretório de teste: {base_dir_test}")
    #     shutil.rmtree(base_dir_test)

    console_test.print("\n--- Testes manuais/interativos (descomente para usar) ---")
    # console_test.print("\n--- Testando wizard.collect_basic_info() ---")
    # # Limpar dados antes de coletar
    # wizard.current_preset_data = {}
    # if wizard.collect_basic_info():
    #     console_test.print(f"Dados básicos coletados: {wizard.current_preset_data}")
    # else:
    #     console_test.print("Coleta de dados básicos falhou ou foi cancelada.")
    #
    # console_test.print("\n--- Testando wizard.select_operation_mode() ---")
    # wizard.current_preset_data = {} # Resetar para o teste do modo
    # if wizard.select_operation_mode():
    #     console_test.print(f"Modo de operação selecionado e dados atualizados: {wizard.current_preset_data}")
    # else:
    #     console_test.print("Seleção de modo de operação falhou ou foi cancelada.")
    #
    # console_test.print("\n--- Testando wizard.configure_conditional_settings() ---")
    # # Simular que um modo foi selecionado antes
    # wizard.current_preset_data = {"chat_mode": True, "name": "test_chat"} # Exemplo para modo chat
    # if wizard.configure_conditional_settings():
    #     console_test.print(f"Configurações condicionais (chat) coletadas: {wizard.current_preset_data}")
    # else:
    #     console_test.print("Coleta de configurações condicionais falhou.")
    #
    # wizard.current_preset_data = {"file_mode": True, "name": "test_file"} # Exemplo para modo file
    # if wizard.configure_conditional_settings():
    #     console_test.print(f"Configurações condicionais (file) coletadas: {wizard.current_preset_data}")
    # else:
    #     console_test.print("Coleta de configurações condicionais falhou.")
    #
    # wizard.current_preset_data = {"server_mode": True, "name": "test_server"} # Exemplo para modo server
    # if wizard.configure_conditional_settings():
    #     console_test.print(f"Configurações condicionais (server) coletadas: {wizard.current_preset_data}")
    # else:
    #     console_test.print("Coleta de configurações condicionais falhou.")

    console_test.print("\n--- Testando wizard.configure_models() ---")
    # Simular dados anteriores e um ModelManager com alguns modelos
    wizard.current_preset_data = {"name": "test_models_config", "chat_mode": True}
    
    # Mock ModelManager (simplificado)
    class MockModel(Model):
        pass

    mock_models_data = {
        "provider_a": [MockModel(name="model_a1", model_id="pa/a1", provider="provider_a"), MockModel(name="model_a2", model_id="pa/a2", provider="provider_a")],
        "provider_b": [MockModel(name="model_b1", model_id="pb/b1", provider="provider_b")]
    }
    wizard.model_manager.get_available_providers = mock_get_providers
    wizard.model_manager.get_models_for_provider = mock_get_models

    if wizard.configure_models():
        console_test.print(f"Configuração de modelos LLM concluída. Dados: {wizard.current_preset_data}")
    else:
        console_test.print("Configuração de modelos LLM falhou.")
    
    # Restaurar métodos originais do ModelManager
    wizard.model_manager.get_available_providers = original_get_providers
    wizard.model_manager.get_models_for_provider = original_get_models

    console_test.print("\n--- Testando wizard.configure_tools() ---")
    wizard.current_preset_data = {"name": "test_tools_config", "chat_mode": True}
    if wizard.configure_tools():
        console_test.print(f"Configuração de ferramentas de desenvolvimento concluída. Dados: {wizard.current_preset_data}")
    else:
        console_test.print("Configuração de ferramentas de desenvolvimento falhou.")

    console_test.print("\n--- Testando wizard.configure_display() ---")
    wizard.current_preset_data = {"name": "test_display_config"}
    if wizard.configure_display():
        console_test.print(f"Configuração de display concluída. Dados: {wizard.current_preset_data}")
    else:
        console_test.print("Configuração de display falhou.")

    console_test.print("\n--- Testando wizard.configure_logging() ---")
    wizard.current_preset_data = {"name": "test_logging_config"}
    if wizard.configure_logging():
        console_test.print(f"Configuração de logging concluída. Dados: {wizard.current_preset_data}")
    else:
        console_test.print("Configuração de logging falhou.")

    # Teste com log_mode que pede log_file
    # Salvar o Prompt.ask original para restaurar depois
    original_prompt_ask_func = Prompt.ask
    
    # Definir o mock_prompt_ask_for_logging
    def mock_prompt_ask_for_logging(prompt_text: str, choices: Optional[List[str]] = None, default: Optional[str] = None, **kwargs: Any) -> str:
        if "Modo de logging" in prompt_text:
            return "file" # Simula usuário escolhendo 'file'
        if "Nível de logging" in prompt_text:
            return "DEBUG"
        if "Caminho para o arquivo de log" in prompt_text:
            return "test.log" # Simula usuário digitando 'test.log'
        # Fallback para o comportamento original para outros prompts
        return original_prompt_ask_func(prompt_text, choices=choices, default=default, **kwargs)

    Prompt.ask = mock_prompt_ask_for_logging # type: ignore
    console_test.print("\n--- Testando wizard.configure_logging() com log_mode='file' (mocked input) ---")
    wizard.current_preset_data = {"name": "test_logging_file_config_forced"} # Resetar dados para este teste
    if wizard.configure_logging(): # Deve pedir log_file devido ao mock
        console_test.print(f"Configuração de logging (com file) concluída. Dados: {wizard.current_preset_data}")
        assert wizard.current_preset_data.get("log_mode") == "file"
        assert wizard.current_preset_data.get("log_file") == "test.log"
        assert wizard.current_preset_data.get("log_level") == "DEBUG"
    else:
        console_test.print("Configuração de logging (com file) falhou.")
    Prompt.ask = original_prompt_ask_func # Restaurar o Prompt.ask original

    console_test.print("\n--- Testando wizard.configure_advanced() ---")
    wizard.current_preset_data = {"name": "test_advanced_config"}
    # Mock para simular entrada de usuário para configure_advanced
    # Este mock é simplificado; um teste real precisaria de mais cenários.
    def mock_prompt_advanced(prompt_text: str, default: Optional[str] = "", **kwargs: Any) -> str:
        if "Deseja configurar opções avançadas" in prompt_text: return "yes" # Entra na configuração avançada
        if "Limite de recursão" in prompt_text: return "10"
        if "Diretório de estado do projeto" in prompt_text: return "/tmp/state"
        if "Limpar memória do projeto" in prompt_text: return "yes"
        if "Habilitar assistência de raciocínio" in prompt_text: return "no"
        if "Máximo de tokens totais" in prompt_text: return "4000"
        if "Máximo de tokens de entrada" in prompt_text: return "2000"
        if "Máximo de tokens de saída" in prompt_text: return "1000"
        if "Temperatura" in prompt_text: return "0.7"
        if "Top P" in prompt_text: return "0.9"
        if "Top K" in prompt_text: return "40"
        if "Penalidade de Frequência" in prompt_text: return "0.1"
        if "Penalidade de Presença" in prompt_text: return "0.1"
        return default if default is not None else ""

    original_prompt_ask_adv = Prompt.ask
    original_prompt_confirm_adv = Prompt.confirm
    Prompt.ask = mock_prompt_advanced # type: ignore
    Prompt.confirm = lambda _text, default=False: True if "Deseja configurar opções avançadas" in _text or "Limpar memória" in _text else default


    if wizard.configure_advanced():
        console_test.print(f"Configuração avançada concluída. Dados: {wizard.current_preset_data}")
        assert wizard.current_preset_data.get("recursion_limit") == 10
        assert wizard.current_preset_data.get("temperature") == 0.7
    else:
        console_test.print("Configuração avançada falhou.")
    
    Prompt.ask = original_prompt_ask_adv
    Prompt.confirm = original_prompt_confirm_adv


    console_test.print("\n--- Testando criação de novo preset (placeholder com todas as etapas até agora) ---")
    wizard.current_preset_data = {} # Resetar para o fluxo completo do wizard
    new_preset_mock = wizard.start_wizard()
    if new_preset_mock:
        console_test.print(f"Preset mockado retornado: {new_preset_mock.name}")
        console_test.print(f"Descrição: {new_preset_mock.description}")
        console_test.print(f"Dados do wizard após todas as etapas atuais: {wizard.current_preset_data}")


    # console_test.print("\n--- Testando edição de preset (placeholder) ---")
    # # Para testar edição, precisaríamos de um preset salvo e a lógica de carregamento em start_wizard
    # # wizard.current_preset_data = {} # Resetar
    # # pm.save_preset(Preset(name="preset_para_editar", command="test command", chat_mode=True, cowboy_mode=True)) # Salvar um para teste
    # # edit_preset_mock = wizard.start_wizard(existing_preset_name="preset_para_editar")
    # # if edit_preset_mock:
    # #     console_test.print(f"Preset mockado (edição) retornado: {edit_preset_mock.name}")
    # #     console_test.print(f"Dados do wizard após edição (placeholder): {wizard.current_preset_data}")