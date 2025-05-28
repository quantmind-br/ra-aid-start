import pytest
from pathlib import Path
import sys

# Adicionar o diretório raiz do projeto ao sys.path para importações diretas
project_root_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root_path))

from ra_aid_start.core.command_builder import CommandBuilder
from ra_aid_start.models.preset import Preset

@pytest.fixture
def builder() -> CommandBuilder:
    """Retorna uma nova instância de CommandBuilder para cada teste."""
    return CommandBuilder()

# Testes para add_flag e get_command_string
def test_empty_command(builder: CommandBuilder):
    assert builder.get_command_string() == "ra-aid"

def test_add_single_long_boolean_flag(builder: CommandBuilder):
    builder.add_flag("verbose")
    assert builder.get_command_string() == "ra-aid --verbose"

def test_add_single_short_boolean_flag(builder: CommandBuilder):
    builder.add_flag("v")
    assert builder.get_command_string() == "ra-aid -v"

def test_add_single_long_flag_with_value(builder: CommandBuilder):
    builder.add_flag("model", "gpt-4o")
    assert builder.get_command_string() == "ra-aid --model gpt-4o"

def test_add_single_short_flag_with_value(builder: CommandBuilder):
    builder.add_flag("p", "my_project")
    assert builder.get_command_string() == "ra-aid -p my_project"

def test_add_flag_with_value_true(builder: CommandBuilder):
    builder.add_flag("force", True)
    assert builder.get_command_string() == "ra-aid --force"

def test_add_flag_with_value_false(builder: CommandBuilder):
    builder.add_flag("no-backup", False) # Esta flag não deve aparecer
    assert builder.get_command_string() == "ra-aid"

def test_add_flag_with_value_containing_spaces(builder: CommandBuilder):
    builder.add_flag("file-path", "/path/to my file/file.txt")
    assert builder.get_command_string() == 'ra-aid --file-path "/path/to my file/file.txt"'

def test_add_flag_with_numeric_value(builder: CommandBuilder):
    builder.add_flag("retries", 3)
    assert builder.get_command_string() == "ra-aid --retries 3"

def test_add_multiple_flags(builder: CommandBuilder):
    builder.add_flag("verbose")
    builder.add_flag("model", "claude-3")
    builder.add_flag("c", "config.yaml")
    # A ordem pode variar dependendo da implementação do dicionário,
    # então testamos a presença dos componentes.
    command_str = builder.get_command_string()
    assert command_str.startswith("ra-aid")
    assert "--verbose" in command_str
    assert "--model claude-3" in command_str
    assert "-c config.yaml" in command_str

def test_add_flag_with_hyphens_in_name(builder: CommandBuilder):
    builder.add_flag("--output-dir", "/tmp/output")
    assert builder.get_command_string() == "ra-aid --output-dir /tmp/output"
    builder._flags.clear() # Limpar para próximo teste no mesmo builder
    builder.add_flag("-o", "/tmp/output_short")
    assert builder.get_command_string() == "ra-aid -o /tmp/output_short"


# Testes para remove_flag
def test_remove_existing_flag(builder: CommandBuilder):
    builder.add_flag("verbose")
    builder.add_flag("model", "gpt-4")
    builder.remove_flag("verbose")
    command_str = builder.get_command_string()
    assert "ra-aid --model gpt-4" == command_str
    assert "--verbose" not in command_str

def test_remove_flag_with_hyphens(builder: CommandBuilder):
    builder.add_flag("--config", "my.cfg")
    builder.remove_flag("--config")
    assert builder.get_command_string() == "ra-aid"
    builder.add_flag("-c", "my.cfg")
    builder.remove_flag("-c")
    assert builder.get_command_string() == "ra-aid"


def test_remove_non_existing_flag(builder: CommandBuilder):
    builder.add_flag("model", "gpt-4")
    builder.remove_flag("non_existent_flag") # Não deve dar erro
    assert builder.get_command_string() == "ra-aid --model gpt-4"

def test_chaining_operations(builder: CommandBuilder):
    builder.add_flag("mode", "test").add_flag("debug", True).remove_flag("mode")
    command_str = builder.get_command_string()
    assert "ra-aid --debug" == command_str
    assert "--mode" not in command_str

# Testes para build_command_from_preset
def test_build_command_from_preset_chat_mode_no_flags(builder: CommandBuilder):
    preset = Preset(name="TestChat", operation_mode="chat", flags={})
    command = builder.build_command_from_preset(preset)
    assert command == "ra-aid --chat"

def test_build_command_from_preset_chat_mode_with_flags(builder: CommandBuilder):
    preset_flags = {
        "temperature": 0.7,
        "cowboy_mode": True, # Será --cowboy-mode
        "api_key_env": "MY_API_KEY" # Será --api-key-env MY_API_KEY
    }
    preset = Preset(name="ChatPro", operation_mode="chat", flags=preset_flags)
    command = builder.build_command_from_preset(preset)
    assert command.startswith("ra-aid --chat")
    assert "--temperature 0.7" in command
    assert "--cowboy-mode" in command # Booleano True
    assert "--api-key-env MY_API_KEY" in command

def test_build_command_from_preset_script_mode(builder: CommandBuilder):
    preset_flags = {"script-path": "scripts/run.py", "args": "--user test"}
    preset = Preset(name="RunMyScript", operation_mode="run_script", flags=preset_flags)
    command = builder.build_command_from_preset(preset)
    assert command.startswith("ra-aid --script-mode")
    assert "--script-path scripts/run.py" in command
    assert '--args "--user test"' in command # Valor com espaços

def test_build_command_from_preset_tool_mode(builder: CommandBuilder):
    preset_flags = {"tool-name": "my_tool", "tool-args": "arg1 arg2"}
    preset = Preset(name="MyToolPreset", operation_mode="execute_tool", flags=preset_flags)
    command = builder.build_command_from_preset(preset)
    assert command.startswith("ra-aid --tool-mode")
    assert "--tool-name my_tool" in command
    assert '--tool-args "arg1 arg2"' in command

def test_build_command_from_preset_agent_mode(builder: CommandBuilder):
    preset = Preset(name="AgentPreset", operation_mode="agent", flags={"loop_count": 5})
    command = builder.build_command_from_preset(preset)
    assert command.startswith("ra-aid --agent-mode")
    assert "--loop-count 5" in command

def test_build_command_from_preset_flags_with_hyphens_in_keys(builder: CommandBuilder):
    # Testar se preset.flags já vem com chaves formatadas como flags CLI
    preset_flags = {
        "--model-id": "specific-model-001",
        "no_stream": True # Deve virar --no-stream
    }
    preset = Preset(name="HyphenFlags", operation_mode="chat", flags=preset_flags)
    command = builder.build_command_from_preset(preset)
    assert command.startswith("ra-aid --chat")
    assert "--model-id specific-model-001" in command
    assert "--no-stream" in command

def test_build_command_clears_previous_flags(builder: CommandBuilder):
    builder.add_flag("stale-flag", "old_value")
    preset = Preset(name="FreshPreset", operation_mode="chat", flags={"new_flag": "fresh"})
    command = builder.build_command_from_preset(preset)
    assert command == "ra-aid --chat --new-flag fresh"  # Corrigido de _ para -
    assert "stale-flag" not in command

# Testes para validate_command
def test_validate_command_valid(builder: CommandBuilder):
    assert builder.validate_command("ra-aid --some-flag") == True
    assert builder.validate_command("ra-aid") == True

def test_validate_command_invalid_prefix(builder: CommandBuilder):
    assert builder.validate_command("my-tool --some-flag") == False

def test_validate_command_empty_string(builder: CommandBuilder):
    assert builder.validate_command("") == False

def test_validate_command_with_leading_spaces(builder: CommandBuilder):
    assert builder.validate_command("  ra-aid --test") == True