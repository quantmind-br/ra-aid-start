from typing import Any, Dict, Optional
from ra_aid_start.models.preset import Preset # Adicionado import

class CommandBuilder:
    """
    Constrói strings de comando para a CLI ra-aid de forma programática.

    Esta classe fornece uma interface fluente para adicionar e remover flags
    e seus valores. Também pode gerar uma string de comando completa
    a partir de um objeto Preset, convertendo automaticamente os nomes das flags
    e formatando os valores conforme necessário.
    """
    def __init__(self):
        """
        Inicializa o CommandBuilder com um dicionário vazio para armazenar flags.
        """
        self._flags: Dict[str, Any] = {}
        self._base_command: str = "ra-aid"

    def add_flag(self, flag: str, value: Any = None) -> 'CommandBuilder':
        """
        Adiciona uma flag e seu valor opcional.

        Args:
            flag (str): O nome da flag (ex: '--verbose', '-p').
            value (Any, optional): O valor da flag. Se None, a flag é considerada booleana (presente ou ausente).
                                   Defaults to None.

        Returns:
            CommandBuilder: A própria instância para permitir encadeamento.
        """
        # Remove '--' ou '-' do início se já estiverem presentes para padronização interna
        # A lógica de formatação final cuidará de adicionar os prefixos corretos.
        processed_flag = flag.lstrip('-')
        self._flags[processed_flag] = value
        return self

    def remove_flag(self, flag: str) -> 'CommandBuilder':
        """
        Remove uma flag.

        Args:
            flag (str): O nome da flag a ser removida.

        Returns:
            CommandBuilder: A própria instância para permitir encadeamento.
        """
        processed_flag = flag.lstrip('-')
        if processed_flag in self._flags:
            del self._flags[processed_flag]
        return self

    def get_command_string(self) -> str:
        """
        Constrói e retorna a string de comando completa.

        Returns:
            str: A string de comando formatada.
        """
        parts = [self._base_command]
        for flag, value in self._flags.items():
            # Determinar o prefixo correto para a flag
            # Flags curtas (um caractere) geralmente usam '-', longas usam '--'
            # Esta é uma simplificação; um mapeamento mais robusto pode ser necessário
            # para flags que têm formas curtas e longas.
            prefix = "--" if len(flag) > 1 else "-"
            
            if value is None or value is True: # Flags booleanas ou sem valor explícito
                parts.append(f"{prefix}{flag}")
            elif value is False: # Flag booleana explicitamente desativada (não adicionar)
                pass
            else:
                # Para flags com valor, formatar como --flag=valor ou --flag valor
                # A CLI ra-aid pode ter uma preferência. Usarei '--flag valor' por enquanto.
                # Se o valor contiver espaços, ele deve ser colocado entre aspas.
                value_str = str(value)
                if ' ' in value_str and not (value_str.startswith('"') and value_str.endswith('"')):
                    parts.append(f'{prefix}{flag} "{value_str}"')
                else:
                    parts.append(f"{prefix}{flag} {value_str}")
        return " ".join(parts)

    def build_command_from_preset(self, preset: Preset) -> str:
        """
        Constrói a string de comando completa a partir de um objeto Preset.

        Este método limpa quaisquer flags (`self._flags`) existentes antes de
        processar o novo preset. Ele adiciona uma flag correspondente ao
        `preset.operation_mode` e, em seguida, processa todas as flags
        definidas em `preset.flags`, convertendo chaves snake_case para
        kebab-case para uso na CLI.

        Args:
            preset (Preset): O objeto Preset contendo as configurações
                             a partir das quais o comando será construído.

        Returns:
            str: A string de comando completa e formatada.
        """
        self._flags.clear()

        # 1. Adicionar a flag de modo de operação principal
        # Os detalhes específicos do modo (como --script-path) virão de preset.flags
        if preset.operation_mode == "chat":
            self.add_flag("chat")
        elif preset.operation_mode == "message":
            self.add_flag("message")
        elif preset.operation_mode == "file":
            self.add_flag("file")
        elif preset.operation_mode == "server":
            self.add_flag("server")
        elif preset.operation_mode == "run_script": # Modo legado/não-wizard
            self.add_flag("script-mode")
        elif preset.operation_mode == "execute_tool": # Modo legado/não-wizard
            self.add_flag("tool-mode")
        elif preset.operation_mode == "agent": # Modo legado/não-wizard
            self.add_flag("agent-mode")
        # else:
            # Idealmente, logar um aviso ou erro se o modo não for reconhecido
            # print(f"Aviso: Modo de operação '{preset.operation_mode}' não mapeado diretamente para uma flag no CommandBuilder.")

        # 2. Processar todas as flags definidas em preset.flags
        # Assume-se que as chaves em preset.flags são os nomes das flags da CLI
        # (sem os hífens iniciais, ou com eles, pois add_flag os remove)
        # e os valores são os valores corretos para essas flags.
        if preset.flags:
            for key_from_preset, flag_value in preset.flags.items():
                # Converter snake_case (comum em Python/Pydantic) para kebab-case (comum em CLI)
                # Se a chave já for kebab-case ou tiver hífens, replace não fará mal.
                cli_style_flag_name = key_from_preset.replace("_", "-")
                self.add_flag(cli_style_flag_name, flag_value)
        
        return self.get_command_string()

    def validate_command(self, command: str) -> bool:
        """
        Valida uma string de comando.
        Atualmente, implementa uma verificação básica.

        Args:
            command (str): A string de comando a ser validada.

        Returns:
            bool: True se o comando for considerado válido (basicamante), False caso contrário.
        """
        if not command:
            return False
        # Verificação básica: o comando deve começar com a base command (ex: "ra-aid")
        if command.strip().startswith(self._base_command):
            # TODO: Implementar validações mais complexas aqui no futuro,
            # como verificar a validade das flags, combinações de flags,
            # e valores de flags usando, por exemplo, um esquema ou ValidationRules.
            return True
        return False

if __name__ == '__main__':
    # Exemplo de uso (para teste rápido)
    builder = CommandBuilder()
    
    # Adicionando flags
    builder.add_flag("verbose") \
           .add_flag("profile", "dev_profile") \
           .add_flag("p", "project_x") # Exemplo de flag curta
    
    print(f"Comando 1: {builder.get_command_string()}")
    # Esperado: ra-aid --verbose --profile dev_profile -p project_x (ou similar)

    builder.add_flag("config-file", "/path/to/config with spaces.json")
    builder.add_flag("force", True)
    builder.add_flag("no-backup", False) # Não deve aparecer
    
    print(f"Comando 2: {builder.get_command_string()}")
    # Esperado: ra-aid --verbose --profile dev_profile -p project_x --config-file "/path/to/config with spaces.json" --force

    builder.remove_flag("verbose")
    builder.remove_flag("--profile") # Testar remoção com prefixo

    print(f"Comando 3: {builder.get_command_string()}")
    # Esperado: ra-aid -p project_x --config-file "/path/to/config with spaces.json" --force
    
    builder_empty = CommandBuilder()
    print(f"Comando Vazio: {builder_empty.get_command_string()}")
    # Esperado: ra-aid