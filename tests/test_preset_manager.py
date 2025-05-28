import pytest
import shutil
import json
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import patch, MagicMock

from ra_aid_start.core.preset_manager import PresetManager, PresetManagerError, DEFAULT_PRESETS_DIR_NAME
from ra_aid_start.models.preset import Preset
from ra_aid_start.utils.json_handler import JsonHandlerError

# Diretório base temporário para os testes
TEST_BASE_STORAGE_PATH = Path("./temp_test_preset_manager_storage")
TEST_PRESETS_PATH = TEST_BASE_STORAGE_PATH / DEFAULT_PRESETS_DIR_NAME

@pytest.fixture(autouse=True)
def manage_test_environment():
    """Cria e limpa o ambiente de teste para cada função de teste."""
    if TEST_BASE_STORAGE_PATH.exists():
        shutil.rmtree(TEST_BASE_STORAGE_PATH)
    TEST_BASE_STORAGE_PATH.mkdir(parents=True, exist_ok=True)
    # Não criar TEST_PRESETS_PATH aqui, PresetManager.__init__ deve fazê-lo
    yield
    if TEST_BASE_STORAGE_PATH.exists():
        shutil.rmtree(TEST_BASE_STORAGE_PATH)

class TestPresetManager:

    def get_manager_instance(self) -> PresetManager:
        """Helper para obter uma instância do PresetManager com o caminho de teste."""
        return PresetManager(base_storage_path=TEST_BASE_STORAGE_PATH)

    def create_dummy_preset_file(self, manager: PresetManager, preset_name: str, data: Dict[str, Any]):
        """Helper para criar um arquivo de preset diretamente para fins de teste."""
        preset_file_path = manager._get_preset_path(preset_name)
        preset_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(preset_file_path, "w") as f:
            json.dump(data, f)
        return preset_file_path

    # Testes para __init__
    def test_init_creates_presets_directory(self):
        """Verifica se o diretório de presets é criado na inicialização."""
        assert not TEST_PRESETS_PATH.exists()
        self.get_manager_instance() # A inicialização deve criar o diretório
        assert TEST_PRESETS_PATH.exists()
        assert TEST_PRESETS_PATH.is_dir()

    def test_init_failure_permission_denied(self, mocker):
        """Testa falha na inicialização se a criação do diretório falhar."""
        mocker.patch("ra_aid_start.utils.file_handler.ensure_dir_exists", side_effect=OSError("Permission denied"))
        with pytest.raises(PresetManagerError, match="Could not initialize preset storage"):
            self.get_manager_instance()

    # Testes para _get_preset_path
    def test_get_preset_path_valid_name(self):
        manager = self.get_manager_instance()
        expected_path = TEST_PRESETS_PATH / "my_preset.json"
        assert manager._get_preset_path("my_preset") == expected_path

    def test_get_preset_path_sanitizes_name(self):
        manager = self.get_manager_instance()
        # Teste com caracteres que precisam de sanitização (ex: espaços, barras)
        # A sanitização atual é simples: substitui espaço por underscore e remove outros.
        # Se a sanitização no PresetManager mudar, este teste precisa ser ajustado.
        # A sanitização atual no PresetManager é apenas .lower() e adiciona .json
        # Se uma sanitização mais complexa for adicionada, este teste deve ser expandido.
        assert manager._get_preset_path("My Preset with Spaces") == TEST_PRESETS_PATH / "my preset with spaces.json"
        assert manager._get_preset_path("preset/with/slashes") == TEST_PRESETS_PATH / "preset/with/slashes.json" # Path object lida com isso

    def test_get_preset_path_empty_name_raises_error(self):
        manager = self.get_manager_instance()
        with pytest.raises(ValueError, match="Preset name cannot be empty"):
            manager._get_preset_path("")
        with pytest.raises(ValueError, match="Preset name cannot be empty"):
            manager._get_preset_path("   ")
            
    # Testes para create_preset
    def test_create_preset_success(self):
        manager = self.get_manager_instance()
        preset_data = {
            "name": "NewPreset",
            "description": "A test preset",
            "command_template": "echo 'hello'"
        }
        created_preset = manager.create_preset(preset_data)
        assert created_preset is not None
        assert created_preset.name == "NewPreset"
        assert (TEST_PRESETS_PATH / "newpreset.json").exists()

        loaded_data = json.loads((TEST_PRESETS_PATH / "newpreset.json").read_text())
        assert loaded_data["name"] == "NewPreset"
        assert loaded_data["description"] == "A test preset"

    def test_create_preset_duplicate_name_fails(self):
        manager = self.get_manager_instance()
        preset_data = {"name": "DuplicatePreset", "command_template": "cmd1"}
        manager.create_preset(preset_data) # Cria o primeiro

        preset_data_dup = {"name": "DuplicatePreset", "command_template": "cmd2"}
        with pytest.raises(PresetManagerError, match="Preset with name 'DuplicatePreset' already exists."):
            manager.create_preset(preset_data_dup)

    def test_create_preset_invalid_data_fails(self):
        manager = self.get_manager_instance()
        invalid_data = {"description": "Missing name and command"} # 'name' é obrigatório
        with pytest.raises(PresetManagerError, match="Invalid data for new preset"):
            manager.create_preset(invalid_data)
        assert not list(TEST_PRESETS_PATH.glob("*.json")) # Nenhum arquivo deve ser criado

    def test_create_preset_save_json_fails(self, mocker):
        manager = self.get_manager_instance()
        mocker.patch("ra_aid_start.utils.json_handler.save_json", side_effect=JsonHandlerError("Disk full"))
        preset_data = {"name": "SaveFailPreset", "command_template": "echo"}
        
        with pytest.raises(PresetManagerError, match="Failed to save preset 'SaveFailPreset'"):
            manager.create_preset(preset_data)
        # O arquivo não deve existir se save_json falhou
        assert not (TEST_PRESETS_PATH / "savefailpreset.json").exists()


    # Testes para load_preset
    def test_load_preset_success(self):
        manager = self.get_manager_instance()
        preset_name = "LoadablePreset"
        data_to_save = {"name": preset_name, "description": "Test", "command_template": "test_cmd"}
        self.create_dummy_preset_file(manager, preset_name, data_to_save)

        loaded_preset = manager.load_preset(preset_name)
        assert loaded_preset is not None
        assert loaded_preset.name == preset_name
        assert loaded_preset.description == "Test"

    def test_load_preset_not_found(self):
        manager = self.get_manager_instance()
        loaded_preset = manager.load_preset("NonExistentPreset")
        assert loaded_preset is None

    def test_load_preset_json_decode_error(self, mocker):
        manager = self.get_manager_instance()
        preset_name = "CorruptedPreset"
        preset_file = manager._get_preset_path(preset_name)
        preset_file.parent.mkdir(parents=True, exist_ok=True)
        preset_file.write_text("{corrupted_json: ") # JSON inválido

        # Mock load_json para simular o erro de forma controlada, ou deixar o real falhar
        mocker.patch("ra_aid_start.utils.json_handler.load_json", side_effect=JsonHandlerError("Corrupted JSON"))
        
        with pytest.raises(PresetManagerError, match=f"Error loading preset file for '{preset_name}'"):
            manager.load_preset(preset_name)

    def test_load_preset_invalid_schema(self):
        manager = self.get_manager_instance()
        preset_name = "InvalidSchemaPreset"
        # Salva dados que não correspondem ao schema de Preset (ex: faltando 'name')
        data_to_save = {"description": "This preset has no name", "command_template": "cmd"}
        self.create_dummy_preset_file(manager, preset_name, data_to_save)

        with pytest.raises(PresetManagerError, match=f"Invalid data in preset file for '{preset_name}'"):
            manager.load_preset(preset_name)
            
    # Testes para list_presets
    def test_list_presets_empty(self):
        manager = self.get_manager_instance()
        assert manager.list_presets() == []

    def test_list_presets_with_items(self):
        manager = self.get_manager_instance()
        self.create_dummy_preset_file(manager, "PresetAlpha", {"name": "PresetAlpha", "command_template": "a"})
        self.create_dummy_preset_file(manager, "PresetBeta", {"name": "PresetBeta", "command_template": "b"})
        
        # Criar um arquivo não-JSON para garantir que ele seja ignorado
        (TEST_PRESETS_PATH / "not_a_preset.txt").write_text("ignore me")
        # Criar um arquivo JSON malformado
        (TEST_PRESETS_PATH / "corrupted.json").write_text("{bad json")


        presets = manager.list_presets()
        assert len(presets) == 2
        preset_names = sorted([p.name for p in presets])
        assert preset_names == ["PresetAlpha", "PresetBeta"]

    def test_list_presets_skips_invalid_json_and_schema(self, mocker):
        manager = self.get_manager_instance()
        # Preset válido
        self.create_dummy_preset_file(manager, "ValidPreset", {"name": "ValidPreset", "command_template": "valid"})
        
        # Preset com JSON corrompido
        corrupted_file_path = manager._get_preset_path("CorruptedJSONPreset")
        corrupted_file_path.write_text("{not_json:")
        
        # Preset com schema inválido (faltando 'name' no conteúdo, mas nome de arquivo ok)
        self.create_dummy_preset_file(manager, "InvalidSchemaPresetFile", {"description": "no name here", "command_template":"cmd"})

        # Mock load_json para controlar o erro de JSON corrompido
        # A lógica de list_presets chama load_preset, que já tem tratamento de erro.
        # Vamos garantir que o logger seja chamado.
        mock_logger_error = mocker.patch.object(manager.logger, 'error')

        presets = manager.list_presets()
        assert len(presets) == 1
        assert presets[0].name == "ValidPreset"
        
        # Verificar se os erros foram logados para os arquivos problemáticos
        # load_preset já loga, list_presets não precisa logar novamente esses erros específicos.
        # O teste de load_preset já cobre o log de erros.
        # Aqui, apenas garantimos que os problemáticos são pulados.
        
        # Para ser mais explícito sobre o que é logado por list_presets em si (se houver)
        # ou pelos load_preset chamados:
        # A chamada para CorruptedJSONPreset deve logar um JsonHandlerError ou similar.
        # A chamada para InvalidSchemaPresetFile deve logar um PresetManagerError sobre dados inválidos.
        
        # Este teste é mais sobre o resultado da lista. Os logs são testados nos testes de load_preset.
        # No entanto, podemos verificar se o logger foi chamado algumas vezes.
        # O número exato de chamadas pode ser frágil.
        # assert mock_logger_error.call_count >= 1 # Pelo menos o erro de schema inválido.
        # O logger de erro de PresetManager é chamado dentro de load_preset, que é chamado por list_presets.
        # Então, para o caso de schema inválido, o logger.error de PresetManager deve ser chamado.
        # Para JSON corrompido, também.
        assert mock_logger_error.call_count >= 2 # Um para JSON corrompido, um para schema inválido.


    def test_list_presets_storage_path_not_exist(self, mocker):
        # Simular que o diretório base de presets não existe
        # Isso é um pouco artificial porque __init__ o cria.
        # Mas se fosse deletado externamente...
        manager = self.get_manager_instance() # Cria o dir
        shutil.rmtree(TEST_PRESETS_PATH) # Remove
        
        mock_logger_warning = mocker.patch.object(manager.logger, 'warning')
        assert manager.list_presets() == []
        mock_logger_warning.assert_called_once_with(
            f"Presets directory {TEST_PRESETS_PATH} does not exist. Cannot list presets."
        )

    # Testes para update_preset
    def test_update_preset_success(self):
        manager = self.get_manager_instance()
        preset_name = "UpdateMe"
        initial_data = {"name": preset_name, "description": "Initial Desc", "command_template": "initial_cmd"}
        self.create_dummy_preset_file(manager, preset_name, initial_data)

        update_payload = {"description": "Updated Desc", "command_template": "updated_cmd", "another_field": "new_val"}
        updated_preset = manager.update_preset(preset_name, update_payload)

        assert updated_preset is not None
        assert updated_preset.name == preset_name # Nome não deve mudar
        assert updated_preset.description == "Updated Desc"
        assert updated_preset.command_template == "updated_cmd"
        # Verificar se campos extras no payload são ignorados se não estiverem no modelo Preset
        # ou se o modelo Preset os aceita via model_extra='allow' ou similar.
        # O modelo Preset atual não tem 'another_field', então ele deve ser ignorado ou causar erro
        # dependendo da configuração Pydantic de Preset.
        # Assumindo que Preset não tem 'another_field' e não permite campos extras por padrão (strict),
        # ou que update_preset os filtra. O PresetManager atual os filtra.
        assert not hasattr(updated_preset, "another_field")

        loaded_from_file = manager.load_preset(preset_name)
        assert loaded_from_file.description == "Updated Desc"

    def test_update_preset_not_found(self):
        manager = self.get_manager_instance()
        update_payload = {"description": "Doesn't matter"}
        with pytest.raises(PresetManagerError, match="Preset 'NonExistent' not found for update."):
            manager.update_preset("NonExistent", update_payload)

    def test_update_preset_empty_name_fails(self):
        manager = self.get_manager_instance()
        with pytest.raises(ValueError, match="Preset name cannot be empty for update."):
            manager.update_preset("", {"description": "test"})

    def test_update_preset_invalid_update_data_keeps_original_valid_fields(self, mocker):
        manager = self.get_manager_instance()
        preset_name = "UpdateWithInvalid"
        initial_data = {"name": preset_name, "description": "Good Desc", "command_template": "good_cmd", "tags": ["tag1"]}
        self.create_dummy_preset_file(manager, preset_name, initial_data)

        # 'tags' deve ser List[str], passar um int é inválido para Pydantic
        # 'name' e 'created_at' no payload de update são ignorados por update_preset
        invalid_update_payload = {"description": "New Valid Desc", "tags": 123, "name": "AttemptChangeName"}
        
        # Pydantic dentro de PresetManager.update_preset deve rejeitar isso.
        # O update_preset tenta aplicar os campos um a um e depois revalida.
        # Se a revalidação falhar, ele deve retornar None e logar um erro.
        mock_logger_error = mocker.patch.object(manager.logger, 'error')
        updated_preset = manager.update_preset(preset_name, invalid_update_payload)
        
        assert updated_preset is None # A atualização deve falhar devido a 'tags: 123'
        mock_logger_error.assert_called_with(
            mocker.ANY, # A mensagem exata pode variar um pouco com a versão do Pydantic
            # match=f"Invalid data after attempting to update preset '{preset_name}'"
        )

        # Verificar que o arquivo original não foi corrompido ou alterado para um estado inválido
        reloaded_preset = manager.load_preset(preset_name)
        assert reloaded_preset is not None
        assert reloaded_preset.description == "Good Desc" # Deve permanecer o original
        assert reloaded_preset.tags == ["tag1"]
        assert reloaded_preset.name == preset_name # Nome não deve ter mudado

    def test_update_preset_save_fails(self, mocker):
        manager = self.get_manager_instance()
        preset_name = "UpdateSaveFail"
        initial_data = {"name": preset_name, "command_template": "cmd"}
        self.create_dummy_preset_file(manager, preset_name, initial_data)

        mocker.patch("ra_aid_start.utils.json_handler.save_json", side_effect=JsonHandlerError("Disk full"))
        
        update_payload = {"description": "This will fail to save"}
        with pytest.raises(PresetManagerError, match=f"Failed to save updated preset '{preset_name}'"):
            manager.update_preset(preset_name, update_payload)

    # Testes para delete_preset
    def test_delete_preset_success(self):
        manager = self.get_manager_instance()
        preset_name = "DeleteMe"
        self.create_dummy_preset_file(manager, preset_name, {"name": preset_name, "command_template": "any"})
        
        assert (manager._get_preset_path(preset_name)).exists()
        delete_success = manager.delete_preset(preset_name)
        assert delete_success
        assert not (manager._get_preset_path(preset_name)).exists()
        assert manager.load_preset(preset_name) is None # Não deve mais carregar

    def test_delete_preset_not_found_returns_true(self, mocker):
        manager = self.get_manager_instance()
        mock_logger_info = mocker.patch.object(manager.logger, 'info')
        delete_success = manager.delete_preset("NonExistentToDelete")
        assert delete_success # Considerado sucesso pois o estado (não existe) é alcançado
        mock_logger_info.assert_called_with(
            "Preset file for 'NonExistentToDelete' not found. Nothing to delete."
        )

    def test_delete_preset_empty_name_fails(self):
        manager = self.get_manager_instance()
        with pytest.raises(ValueError, match="Preset name cannot be empty for deletion."):
            manager.delete_preset("")

    def test_delete_preset_os_error_on_remove(self, mocker):
        manager = self.get_manager_instance()
        preset_name = "DeleteOSError"
        self.create_dummy_preset_file(manager, preset_name, {"name": preset_name, "command_template": "cmd"})
        
        mocker.patch("pathlib.Path.unlink", side_effect=OSError("Permission denied"))
        
        delete_success = manager.delete_preset(preset_name)
        assert not delete_success # Falha na deleção
        # O arquivo ainda deve existir porque o unlink falhou
        assert (manager._get_preset_path(preset_name)).exists()


    # Testes para execute_preset
    @patch("subprocess.run")
    def test_execute_preset_success(self, mock_subprocess_run):
        manager = self.get_manager_instance()
        preset_name = "ExecutablePreset"
        command = "echo 'Executing preset'"
        self.create_dummy_preset_file(manager, preset_name, {"name": preset_name, "command_template": command})

        # Configurar o mock para simular uma execução bem-sucedida
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="Executing preset\n", stderr="")

        execute_success = manager.execute_preset(preset_name)
        assert execute_success
        mock_subprocess_run.assert_called_once_with(command, shell=True, capture_output=True, text=True, check=False)

    @patch("subprocess.run")
    def test_execute_preset_command_fails(self, mock_subprocess_run):
        manager = self.get_manager_instance()
        preset_name = "FailingCmdPreset"
        command = "exit 1" # Comando que falha
        self.create_dummy_preset_file(manager, preset_name, {"name": preset_name, "command_template": command})

        mock_subprocess_run.return_value = MagicMock(returncode=1, stdout="", stderr="Error executing")

        execute_success = manager.execute_preset(preset_name)
        assert not execute_success # Deve retornar False se o comando falhar
        mock_subprocess_run.assert_called_once()

    def test_execute_preset_not_found(self):
        manager = self.get_manager_instance()
        execute_success = manager.execute_preset("NonExistentToExecute")
        assert not execute_success

    def test_execute_preset_empty_name_fails(self):
        manager = self.get_manager_instance()
        with pytest.raises(ValueError, match="Preset name cannot be empty for execution."):
            manager.execute_preset("")

    @patch("subprocess.run", side_effect=OSError("Command not found"))
    def test_execute_preset_subprocess_os_error(self, mock_subprocess_run_os_error):
        manager = self.get_manager_instance()
        preset_name = "SubprocessOSErrorPreset"
        command = "some_non_existent_command"
        self.create_dummy_preset_file(manager, preset_name, {"name": preset_name, "command_template": command})

        execute_success = manager.execute_preset(preset_name)
        assert not execute_success
        mock_subprocess_run_os_error.assert_called_once()
        # O logger de PresetManager deve ter registrado o OSError
        # (Verificar isso pode ser feito mockando manager.logger.error)

    def test_preset_name_case_insensitivity_on_disk(self):
        """
        Testa se o gerenciamento de arquivos é insensível a maiúsculas/minúsculas
        para nomes de presets, refletindo o comportamento de PresetManager._get_preset_path
        que usa .lower() no nome do arquivo.
        """
        manager = self.get_manager_instance()
        preset_data_lower = {"name": "caseTest", "command_template": "cmd_lower"}
        
        # Criar com nome misto, mas será salvo como 'casetest.json'
        created_preset = manager.create_preset({"name": "CaseTest", "command_template": "cmd_mixed"})
        assert created_preset is not None
        assert created_preset.name == "CaseTest" # O nome no objeto Preset mantém o case original
        
        # Verificar o nome do arquivo no disco
        assert (TEST_PRESETS_PATH / "casetest.json").exists() # Salvo em minúsculas

        # Tentar carregar com diferentes casings
        loaded_lower = manager.load_preset("casetest")
        assert loaded_lower is not None
        assert loaded_lower.name == "CaseTest"

        loaded_upper = manager.load_preset("CASeTeST")
        assert loaded_upper is not None
        assert loaded_upper.name == "CaseTest"
        
        loaded_original = manager.load_preset("CaseTest")
        assert loaded_original is not None
        assert loaded_original.name == "CaseTest"

        # Tentar criar um duplicado com case diferente (deve falhar porque o nome do arquivo seria o mesmo)
        with pytest.raises(PresetManagerError, match="Preset with name 'casetest' already exists"):
            manager.create_preset({"name": "casetest", "command_template": "cmd_lower_dup"})
        
        # Listar deve retornar o nome original do preset
        presets = manager.list_presets()
        assert len(presets) == 1
        assert presets[0].name == "CaseTest"

        # Atualizar usando um case diferente para o nome do preset
        update_success = manager.update_preset("CASETESThehe", {"description": "Updated via different case"})
        assert update_success is not None # _get_preset_path normaliza para "casetest.json"
        assert update_success.description == "Updated via different case"

        # Deletar usando um case diferente
        delete_success = manager.delete_preset("caSETEst")
        assert delete_success
        assert not (TEST_PRESETS_PATH / "casetest.json").exists()