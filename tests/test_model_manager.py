import pytest
import shutil
import json
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import patch, MagicMock

from ra_aid_start.core.model_manager import ModelManager, ModelManagerError, DEFAULT_MODELS_DIR_NAME
from ra_aid_start.models.model import Model
from ra_aid_start.utils.json_handler import JsonHandlerError
from ra_aid_start.data.default_models import DEFAULT_MODELS_DATA # Para testar restore_defaults

# Diretório base temporário para os testes
TEST_BASE_STORAGE_PATH_MM = Path("./temp_test_model_manager_storage")
TEST_MODELS_PATH_MM = TEST_BASE_STORAGE_PATH_MM / DEFAULT_MODELS_DIR_NAME

@pytest.fixture(autouse=True)
def manage_test_environment_mm():
    """Cria e limpa o ambiente de teste para cada função de teste do ModelManager."""
    if TEST_BASE_STORAGE_PATH_MM.exists():
        shutil.rmtree(TEST_BASE_STORAGE_PATH_MM)
    TEST_BASE_STORAGE_PATH_MM.mkdir(parents=True, exist_ok=True)
    yield
    if TEST_BASE_STORAGE_PATH_MM.exists():
        shutil.rmtree(TEST_BASE_STORAGE_PATH_MM)

class TestModelManager:

    def get_manager_instance(self) -> ModelManager:
        """Helper para obter uma instância do ModelManager com o caminho de teste."""
        return ModelManager(base_storage_path=TEST_BASE_STORAGE_PATH_MM)

    def create_dummy_provider_file(self, manager: ModelManager, provider_name: str, models_data: List[Dict[str, Any]]):
        """Helper para criar um arquivo de provedor diretamente para fins de teste."""
        provider_file_path = manager._get_provider_file_path(provider_name)
        provider_file_path.parent.mkdir(parents=True, exist_ok=True) # Garante que TEST_MODELS_PATH_MM exista
        with open(provider_file_path, "w") as f:
            json.dump(models_data, f)
        return provider_file_path

    # Testes para __init__
    def test_init_creates_models_directory(self):
        """Verifica se o diretório de modelos é criado na inicialização."""
        assert not TEST_MODELS_PATH_MM.exists()
        self.get_manager_instance() # A inicialização deve criar o diretório
        assert TEST_MODELS_PATH_MM.exists()
        assert TEST_MODELS_PATH_MM.is_dir()

    def test_init_failure_permission_denied(self, mocker):
        """Testa falha na inicialização se a criação do diretório falhar."""
        mocker.patch("ra_aid_start.utils.file_handler.ensure_dir_exists", side_effect=OSError("Permission denied"))
        with pytest.raises(ModelManagerError, match="Could not initialize model storage"):
            self.get_manager_instance()

    # Testes para _get_provider_file_path
    def test_get_provider_file_path_valid_name(self):
        manager = self.get_manager_instance()
        expected_path = TEST_MODELS_PATH_MM / "openai_models.json"
        assert manager._get_provider_file_path("OpenAI") == expected_path

    def test_get_provider_file_path_sanitizes_name(self):
        manager = self.get_manager_instance()
        assert manager._get_provider_file_path("My Provider") == TEST_MODELS_PATH_MM / "my_provider_models.json"
        assert manager._get_provider_file_path("Provider/With/Slashes") == TEST_MODELS_PATH_MM / "provider_with_slashes_models.json"
        assert manager._get_provider_file_path("  Leading Space Provider  ") == TEST_MODELS_PATH_MM / "leading_space_provider_models.json"
        assert manager._get_provider_file_path("Test-Provider_123") == TEST_MODELS_PATH_MM / "test-provider_123_models.json"

    def test_get_provider_file_path_empty_name_raises_error(self):
        manager = self.get_manager_instance()
        with pytest.raises(ValueError, match="Provider name cannot be empty."):
            manager._get_provider_file_path("")
        with pytest.raises(ValueError, match="Provider name cannot be empty."):
            manager._get_provider_file_path("   ")
    
    def test_get_provider_file_path_problematic_name_raises_error(self):
        manager = self.get_manager_instance()
        with pytest.raises(ValueError, match="Provider name '////' results in an empty sanitized name."):
            manager._get_provider_file_path("////")


    # Testes para save_models_for_provider
    def test_save_models_for_provider_success(self):
        manager = self.get_manager_instance()
        provider = "TestProviderSave"
        models_to_save = [
            Model(name="model1", provider=provider, description="desc1"),
            Model(name="model2", provider=provider, is_default=True)
        ]
        success = manager.save_models_for_provider(provider, models_to_save)
        assert success
        provider_file = manager._get_provider_file_path(provider)
        assert provider_file.exists()
        
        loaded_data = json.loads(provider_file.read_text())
        assert len(loaded_data) == 2
        assert loaded_data[0]["name"] == "model1"
        assert loaded_data[1]["name"] == "model2"
        assert loaded_data[1]["is_default"] is True

    def test_save_models_for_provider_empty_list(self):
        manager = self.get_manager_instance()
        provider = "TestProviderEmptySave"
        success = manager.save_models_for_provider(provider, [])
        assert success
        provider_file = manager._get_provider_file_path(provider)
        assert provider_file.exists()
        loaded_data = json.loads(provider_file.read_text())
        assert loaded_data == []

    def test_save_models_for_provider_json_error(self, mocker):
        manager = self.get_manager_instance()
        provider = "TestProviderSaveFail"
        models_to_save = [Model(name="m1", provider=provider)]
        mocker.patch("ra_aid_start.utils.json_handler.save_json", side_effect=JsonHandlerError("Disk full"))
        
        success = manager.save_models_for_provider(provider, models_to_save)
        assert not success
        # O arquivo pode ou não existir dependendo de quando save_json falha.
        # Idealmente, se save_json falha, o arquivo não deve ser deixado em estado corrompido.

    def test_save_models_for_provider_empty_provider_name(self):
        manager = self.get_manager_instance()
        assert not manager.save_models_for_provider("", [Model(name="m", provider="")])


    # Testes para get_models_for_provider
    def test_get_models_for_provider_success(self):
        manager = self.get_manager_instance()
        provider = "TestProviderGet"
        models_data = [
            {"name": "modelA", "provider": provider, "description": "A"},
            {"name": "modelB", "provider": provider, "is_default": True}
        ]
        self.create_dummy_provider_file(manager, provider, models_data)

        loaded_models = manager.get_models_for_provider(provider)
        assert len(loaded_models) == 2
        assert loaded_models[0].name == "modelA"
        assert loaded_models[0].provider == provider
        assert loaded_models[1].name == "modelB"
        assert loaded_models[1].is_default is True

    def test_get_models_for_provider_file_not_found(self):
        manager = self.get_manager_instance()
        models = manager.get_models_for_provider("NonExistentProvider")
        assert models == []

    def test_get_models_for_provider_json_decode_error(self, mocker):
        manager = self.get_manager_instance()
        provider = "CorruptedJSONProvider"
        provider_file = manager._get_provider_file_path(provider)
        provider_file.parent.mkdir(parents=True, exist_ok=True)
        provider_file.write_text("[{corrupted]") # JSON inválido

        # Mock load_json para simular o erro de forma controlada
        mocker.patch("ra_aid_start.utils.json_handler.load_json", side_effect=JsonHandlerError("Bad JSON"))
        
        models = manager.get_models_for_provider(provider)
        assert models == [] # Deve retornar lista vazia e logar o erro

    def test_get_models_for_provider_invalid_schema(self):
        manager = self.get_manager_instance()
        provider = "InvalidSchemaProvider"
        # 'name' é obrigatório para Model
        models_data = [{"description": "Invalid model, no name", "provider":provider}]
        self.create_dummy_provider_file(manager, provider, models_data)

        models = manager.get_models_for_provider(provider)
        assert models == [] # Modelo inválido deve ser pulado, resultando em lista vazia

    def test_get_models_for_provider_partial_valid_schema(self):
        manager = self.get_manager_instance()
        provider = "PartialValidProvider"
        models_data = [
            {"name": "ValidModel", "provider": provider},
            {"description": "Invalid model, no name", "provider": provider}
        ]
        self.create_dummy_provider_file(manager, provider, models_data)
        
        models = manager.get_models_for_provider(provider)
        assert len(models) == 1
        assert models[0].name == "ValidModel"

    def test_get_models_for_provider_mismatched_provider_in_data(self, mocker):
        manager = self.get_manager_instance()
        provider_arg = "TargetProvider"
        other_provider_in_data = "OtherProvider"
        models_data = [
            {"name": "modelX", "provider": other_provider_in_data, "description": "X"}
        ]
        self.create_dummy_provider_file(manager, provider_arg, models_data)
        
        mock_logger_warning = mocker.patch.object(manager.logger, 'warning')
        
        loaded_models = manager.get_models_for_provider(provider_arg)
        assert len(loaded_models) == 1
        assert loaded_models[0].name == "modelX"
        # O ModelManager deve corrigir o campo 'provider' no objeto Model carregado
        assert loaded_models[0].provider == provider_arg 
        mock_logger_warning.assert_called_once_with(
            f"Model data for provider '{provider_arg}' has mismatched provider field: '{other_provider_in_data}'. Using '{provider_arg}'."
        )

    def test_get_models_for_provider_provider_field_missing_in_data(self, mocker):
        manager = self.get_manager_instance()
        provider_arg = "ProviderToSet"
        models_data = [
            {"name": "modelY", "description": "Y"} # Campo 'provider' ausente
        ]
        self.create_dummy_provider_file(manager, provider_arg, models_data)
        
        loaded_models = manager.get_models_for_provider(provider_arg)
        assert len(loaded_models) == 1
        assert loaded_models[0].name == "modelY"
        assert loaded_models[0].provider == provider_arg # Deve ser definido para provider_arg

    def test_get_models_for_provider_empty_provider_name(self):
        manager = self.get_manager_instance()
        assert manager.get_models_for_provider("") == []
        assert manager.get_models_for_provider("  ") == []

    # Testes para add_model
    def test_add_model_success(self):
        manager = self.get_manager_instance()
        provider = "ProviderAdd"
        model_data = {"name": "newModel", "provider": provider, "description": "A new model"}
        
        added_model = manager.add_model(provider, model_data)
        assert added_model is not None
        assert added_model.name == "newModel"
        assert added_model.provider == provider

        # Verificar se foi salvo no arquivo
        loaded_models = manager.get_models_for_provider(provider)
        assert len(loaded_models) == 1
        assert loaded_models[0].name == "newModel"

    def test_add_model_duplicate_name_fails(self):
        manager = self.get_manager_instance()
        provider = "ProviderAddDup"
        model_data = {"name": "dupModel", "provider": provider}
        manager.add_model(provider, model_data) # Adiciona o primeiro

        model_data_dup = {"name": "dupModel", "provider": provider, "description": "duplicado"}
        added_model_dup = manager.add_model(provider, model_data_dup)
        assert added_model_dup is None # Deve falhar ao adicionar duplicado

        loaded_models = manager.get_models_for_provider(provider)
        assert len(loaded_models) == 1 # Apenas o primeiro deve existir

    def test_add_model_invalid_data_fails(self):
        manager = self.get_manager_instance()
        provider = "ProviderAddInvalid"
        # 'name' é obrigatório
        invalid_model_data = {"description": "Model without a name", "provider": provider}
        
        added_model = manager.add_model(provider, invalid_model_data)
        assert added_model is None
        assert not (manager._get_provider_file_path(provider)).exists() # Nenhum arquivo deve ser criado

    def test_add_model_mismatched_provider_in_data_is_corrected(self, mocker):
        manager = self.get_manager_instance()
        target_provider = "TargetProvAdd"
        data_provider = "DataProvAdd"
        model_data = {"name": "modelWithDiffProv", "provider": data_provider, "description": "Test"}

        mock_logger_warning = mocker.patch.object(manager.logger, 'warning')
        added_model = manager.add_model(target_provider, model_data)
        
        assert added_model is not None
        assert added_model.provider == target_provider # Deve ser corrigido para target_provider
        mock_logger_warning.assert_called_once_with(
            f"Provider in model_data ('{data_provider}') differs from target provider ('{target_provider}'). Overriding to '{target_provider}'."
        )
        loaded_models = manager.get_models_for_provider(target_provider)
        assert len(loaded_models) == 1
        assert loaded_models[0].provider == target_provider


    def test_add_model_save_fails(self, mocker):
        manager = self.get_manager_instance()
        provider = "ProviderAddSaveFail"
        model_data = {"name": "modelWillFailSave", "provider": provider}
        
        mocker.patch.object(manager, 'save_models_for_provider', return_value=False)
        
        added_model = manager.add_model(provider, model_data)
        assert added_model is None
        # O arquivo do provedor não deve ser criado ou deve estar vazio se save falhou após get_models (que cria vazio)
        # A lógica atual de add_model chama get_models_for_provider, que pode criar um arquivo vazio se não existir.
        # Depois, se save_models_for_provider falhar, o arquivo vazio pode persistir.
        # Isso é aceitável, mas o modelo não estará lá.
        models_after_fail = manager.get_models_for_provider(provider)
        assert len(models_after_fail) == 0


    # Testes para update_model
    def test_update_model_success(self):
        manager = self.get_manager_instance()
        provider = "ProviderUpdate"
        model_name = "modelToUpdate"
        initial_model_data = {"name": model_name, "provider": provider, "description": "Initial", "is_default": False}
        manager.add_model(provider, initial_model_data)

        update_payload = {"description": "Updated Description", "is_default": True, "context_window": 1024}
        updated_model = manager.update_model(provider, model_name, update_payload)

        assert updated_model is not None
        assert updated_model.name == model_name # Nome não deve mudar
        assert updated_model.provider == provider # Provider não deve mudar
        assert updated_model.description == "Updated Description"
        assert updated_model.is_default is True
        assert updated_model.context_window == 1024

        reloaded_model = manager.get_models_for_provider(provider)[0]
        assert reloaded_model.description == "Updated Description"
        assert reloaded_model.is_default is True

    def test_update_model_sets_other_defaults_to_false(self):
        manager = self.get_manager_instance()
        provider = "ProviderUpdateDefaultLogic"
        manager.add_model(provider, {"name": "model1", "provider": provider, "is_default": True})
        manager.add_model(provider, {"name": "model2", "provider": provider, "is_default": False})
        manager.add_model(provider, {"name": "model3", "provider": provider, "is_default": False})

        # Atualizar model2 para ser o padrão
        manager.update_model(provider, "model2", {"is_default": True})

        models = manager.get_models_for_provider(provider)
        model1_found = next(m for m in models if m.name == "model1")
        model2_found = next(m for m in models if m.name == "model2")
        model3_found = next(m for m in models if m.name == "model3")

        assert not model1_found.is_default
        assert model2_found.is_default
        assert not model3_found.is_default


    def test_update_model_not_found(self):
        manager = self.get_manager_instance()
        provider = "ProviderUpdateNotFound"
        update_payload = {"description": "desc"}
        
        updated_model = manager.update_model(provider, "nonExistentModel", update_payload)
        assert updated_model is None
        # Garantir que nenhum arquivo de provedor foi criado se não existia
        assert not (TEST_MODELS_PATH_MM / f"{provider.lower()}_models.json").exists()


    def test_update_model_invalid_data_fails_validation(self, mocker):
        manager = self.get_manager_instance()
        provider = "ProviderUpdateInvalidData"
        model_name = "modelUpdateInvalid"
        initial_data = {"name": model_name, "provider": provider, "context_window": 100}
        manager.add_model(provider, initial_data)

        # context_window deve ser int, passar string é inválido
        invalid_update_payload = {"context_window": "not_an_int"}
        
        mock_logger_error = mocker.patch.object(manager.logger, 'error')
        updated_model = manager.update_model(provider, model_name, invalid_update_payload)
        
        assert updated_model is None # Atualização deve falhar na validação Pydantic
        mock_logger_error.assert_called_with(
            mocker.ANY # A mensagem exata pode variar
        )

        # Verificar que o modelo original não foi corrompido
        reloaded_model = manager.get_models_for_provider(provider)[0]
        assert reloaded_model.context_window == 100 # Deve permanecer o original

    def test_update_model_cannot_change_name_or_provider(self):
        manager = self.get_manager_instance()
        provider = "ProviderUpdateImmutable"
        model_name = "immutableName"
        manager.add_model(provider, {"name": model_name, "provider": provider, "description": "Original"})

        update_payload = {"name": "newNameAttempt", "provider": "newProviderAttempt", "description": "Desc Updated"}
        updated_model = manager.update_model(provider, model_name, update_payload)
        
        assert updated_model is not None
        assert updated_model.name == model_name # Nome não deve ter mudado
        assert updated_model.provider == provider # Provider não deve ter mudado
        assert updated_model.description == "Desc Updated"


    # Testes para remove_model
    def test_remove_model_success(self):
        manager = self.get_manager_instance()
        provider = "ProviderRemove"
        model_name = "modelToRemove"
        manager.add_model(provider, {"name": "otherModel", "provider": provider})
        manager.add_model(provider, {"name": model_name, "provider": provider})
        
        assert len(manager.get_models_for_provider(provider)) == 2
        
        remove_success = manager.remove_model(provider, model_name)
        assert remove_success
        
        remaining_models = manager.get_models_for_provider(provider)
        assert len(remaining_models) == 1
        assert remaining_models[0].name == "otherModel"

    def test_remove_model_not_found_returns_true(self, mocker):
        manager = self.get_manager_instance()
        provider = "ProviderRemoveNotFound"
        # Criar o arquivo do provedor, mas sem o modelo a ser removido
        manager.save_models_for_provider(provider, [Model(name="someOtherModel", provider=provider)])

        mock_logger_info = mocker.patch.object(manager.logger, 'info')
        remove_success = manager.remove_model(provider, "nonExistentToRemove")
        
        assert remove_success # Considerado sucesso pois o estado (não existe) é alcançado
        mock_logger_info.assert_any_call( # Pode haver outros logs info de get_models
            f"Model 'nonExistentToRemove' not found for provider '{provider}'. Nothing to remove."
        )
        assert len(manager.get_models_for_provider(provider)) == 1 # O outro modelo ainda deve estar lá

    def test_remove_model_from_empty_provider_file_returns_true(self):
        manager = self.get_manager_instance()
        provider = "ProviderRemoveEmpty"
        # Garante que o arquivo do provedor exista, mas vazio
        manager.save_models_for_provider(provider, [])
        
        remove_success = manager.remove_model(provider, "anyModelName")
        assert remove_success
        assert manager.get_models_for_provider(provider) == []
        
    def test_remove_model_provider_file_does_not_exist_returns_true(self):
        manager = self.get_manager_instance()
        provider = "ProviderRemoveNoFile"
        # Não criar o arquivo do provedor
        
        remove_success = manager.remove_model(provider, "anyModelName")
        assert remove_success # get_models_for_provider retornará [], então a lógica de "não encontrado" se aplica
        assert not (manager._get_provider_file_path(provider)).exists()


    def test_remove_model_save_fails(self, mocker):
        manager = self.get_manager_instance()
        provider = "ProviderRemoveSaveFail"
        model_name = "modelToRemoveButSaveFails"
        manager.add_model(provider, {"name": model_name, "provider": provider})

        mocker.patch.object(manager, 'save_models_for_provider', return_value=False)
        
        remove_success = manager.remove_model(provider, model_name)
        assert not remove_success
        
        # Como save falhou, o modelo ainda deve estar "presente" na memória da instância do manager
        # se get_models_for_provider for chamado novamente sem recarregar do disco (o que não acontece aqui).
        # O teste importante é que o arquivo no disco não deve ser alterado para o estado de remoção.
        # No entanto, a implementação atual de ModelManager não mantém estado em memória além do carregamento.
        # Se save_models_for_provider falha, o arquivo no disco permanece como estava antes da tentativa de remoção.
        # Para verificar isso, precisaríamos de uma forma de ler o arquivo diretamente sem ModelManager.
        # Ou, confiar que se save_models_for_provider retorna False, o arquivo não foi modificado com sucesso.
        
        # Vamos mockar save_json diretamente para ter mais controle sobre o estado do arquivo
        mocker.resetall() # Limpar mocks anteriores
        manager_fresh = self.get_manager_instance() # Nova instância para estado limpo
        manager_fresh.add_model(provider, {"name": model_name, "provider": provider}) # Recriar modelo

        mock_save_json = mocker.patch("ra_aid_start.utils.json_handler.save_json", side_effect=JsonHandlerError("Disk Full Error"))
        
        remove_success_fresh = manager_fresh.remove_model(provider, model_name)
        assert not remove_success_fresh
        mock_save_json.assert_called_once() # save_json deve ter sido tentado

        # Verificar que o arquivo ainda contém o modelo original
        # Isso requer que o add_model inicial tenha funcionado e criado o arquivo.
        provider_file_path = manager_fresh._get_provider_file_path(provider)
        if provider_file_path.exists():
            data_on_disk = json.loads(provider_file_path.read_text())
            assert any(m['name'] == model_name for m in data_on_disk)
        else:
            # Se o add_model inicial falhou em criar o arquivo por algum motivo (não esperado neste fluxo)
            # este sub-teste não é totalmente válido. Mas o principal é que remove_success_fresh é False.
            pass

    # Testes para export_models
    def test_export_models_single_provider_success(self):
        manager = self.get_manager_instance()
        provider = "ProviderExportSingle"
        models_data = [
            {"name": "modelE1", "provider": provider, "description": "E1"},
            {"name": "modelE2", "provider": provider, "is_default": True}
        ]
        self.create_dummy_provider_file(manager, provider, models_data)
        # Criar outro provedor para garantir que apenas o especificado seja exportado
        self.create_dummy_provider_file(manager, "OtherProvider", [{"name":"otherM", "provider":"OtherProvider"}])


        exported_data = manager.export_models(provider_name=provider)
        assert provider in exported_data
        assert len(exported_data[provider]) == 2
        assert exported_data[provider][0]["name"] == "modelE1"
        assert "OtherProvider" not in exported_data

    def test_export_models_all_providers_success(self):
        manager = self.get_manager_instance()
        provider1 = "ProviderExportAll1"
        provider2 = "ProviderExportAll2"
        models_data1 = [{"name": "m1a", "provider": provider1, "description": "A"}]
        models_data2 = [
            {"name": "m2b", "provider": provider2, "description": "B"},
            {"name": "m2c", "provider": provider2, "description": "C"}
        ]
        self.create_dummy_provider_file(manager, provider1, models_data1)
        self.create_dummy_provider_file(manager, provider2, models_data2)

        exported_data = manager.export_models() # Exportar todos
        assert provider1 in exported_data
        assert provider2 in exported_data
        assert len(exported_data[provider1]) == 1
        assert len(exported_data[provider2]) == 2
        assert exported_data[provider1][0]["name"] == "m1a"
        assert exported_data[provider2][1]["name"] == "m2c"

    def test_export_models_provider_not_found(self):
        manager = self.get_manager_instance()
        exported_data = manager.export_models(provider_name="NonExistentExportProvider")
        # A implementação atual de export_models para um único provedor retorna
        # {"NonExistentExportProvider": []} se o arquivo do provedor não for encontrado.
        # Isso é razoável.
        assert "NonExistentExportProvider" in exported_data
        assert exported_data["NonExistentExportProvider"] == []
        
    def test_export_models_no_providers_exist(self):
        manager = self.get_manager_instance()
        # Nenhum arquivo de provedor criado
        exported_data = manager.export_models()
        assert exported_data == {}

    # Testes para import_models
    def test_import_models_dict_format_overwrite_success(self):
        manager = self.get_manager_instance()
        provider_to_overwrite = "ProviderImportOverwrite"
        # Criar dados existentes que serão sobrescritos
        self.create_dummy_provider_file(manager, provider_to_overwrite, [{"name":"oldModel", "provider":provider_to_overwrite}])

        import_file_path = TEST_MODELS_PATH_MM / "import_data_overwrite.json" # Usar o diretório de models para o arquivo de import temporário
        import_data_dict = {
            provider_to_overwrite: [
                {"name": "importedM1", "provider": provider_to_overwrite, "description": "Imp1"},
                {"name": "importedM2", "provider": provider_to_overwrite, "is_default": True}
            ],
            "NewProviderImport": [
                {"name": "newProvM1", "provider": "NewProviderImport"}
            ]
        }
        with open(import_file_path, "w") as f:
            json.dump(import_data_dict, f)

        success = manager.import_models(import_file_path, merge=False) # merge=False para sobrescrever
        assert success

        # Verificar provider_to_overwrite
        overwritten_models = manager.get_models_for_provider(provider_to_overwrite)
        assert len(overwritten_models) == 2
        assert overwritten_models[0].name == "importedM1"
        assert overwritten_models[1].name == "importedM2"
        assert overwritten_models[1].is_default is True

        # Verificar NewProviderImport
        new_provider_models = manager.get_models_for_provider("NewProviderImport")
        assert len(new_provider_models) == 1
        assert new_provider_models[0].name == "newProvM1"

    def test_import_models_list_format_merge_success(self):
        manager = self.get_manager_instance()
        provider_to_merge = "ProviderImportMerge"
        # Dados existentes
        manager.add_model(provider_to_merge, {"name": "existingM1", "provider": provider_to_merge, "description": "Original Desc"})
        manager.add_model(provider_to_merge, {"name": "toBeUpdated", "provider": provider_to_merge, "context_window": 100})

        import_file_path = TEST_MODELS_PATH_MM / "import_data_merge.json"
        # Lista de modelos, alguns para provider_to_merge, outros para um novo provider
        import_data_list = [
            {"name": "toBeUpdated", "provider": provider_to_merge, "description": "Updated Desc", "context_window": 200}, # Atualiza existente
            {"name": "newMergedM", "provider": provider_to_merge, "is_default": True}, # Adiciona novo a provider_to_merge
            {"name": "anotherNewM", "provider": "AnotherMergeProv", "description":"Desc"} # Novo modelo para novo provedor
        ]
        with open(import_file_path, "w") as f:
            json.dump(import_data_list, f)

        success = manager.import_models(import_file_path, merge=True) # merge=True (padrão)
        assert success

        # Verificar provider_to_merge
        merged_models = manager.get_models_for_provider(provider_to_merge)
        # Ordenar por nome para asserções consistentes se a ordem não for garantida
        merged_models.sort(key=lambda m: m.name)
        
        assert len(merged_models) == 3 # existingM1, toBeUpdated (atualizado), newMergedM
        
        updated_model = next(m for m in merged_models if m.name == "toBeUpdated")
        assert updated_model.description == "Updated Desc"
        assert updated_model.context_window == 200 # Verifique se o campo foi atualizado
        
        new_model = next(m for m in merged_models if m.name == "newMergedM")
        assert new_model.is_default is True
        
        existing_model = next(m for m in merged_models if m.name == "existingM1")
        assert existing_model.description == "Original Desc" # Não foi tocado

        # Verificar AnotherMergeProv
        another_prov_models = manager.get_models_for_provider("AnotherMergeProv")
        assert len(another_prov_models) == 1
        assert another_prov_models[0].name == "anotherNewM"

    def test_import_models_list_format_with_default_provider(self):
        manager = self.get_manager_instance()
        default_prov = "DefaultProviderForImport"
        import_file_path = TEST_MODELS_PATH_MM / "import_list_default.json"
        import_data_list_no_prov = [
            {"name": "modelA"}, # Sem provider, usará default_prov
            {"name": "modelB", "provider": "ExplicitProvider"} # Com provider explícito
        ]
        with open(import_file_path, "w") as f:
            json.dump(import_data_list_no_prov, f)
        
        success = manager.import_models(import_file_path, default_provider=default_prov, merge=False)
        assert success

        default_prov_models = manager.get_models_for_provider(default_prov)
        assert len(default_prov_models) == 1
        assert default_prov_models[0].name == "modelA"
        assert default_prov_models[0].provider == default_prov

        explicit_prov_models = manager.get_models_for_provider("ExplicitProvider")
        assert len(explicit_prov_models) == 1
        assert explicit_prov_models[0].name == "modelB"
        assert explicit_prov_models[0].provider == "ExplicitProvider"


    def test_import_models_file_not_found(self):
        manager = self.get_manager_instance()
        assert not manager.import_models(Path("non_existent_import_file.json"))

    def test_import_models_corrupted_json(self):
        manager = self.get_manager_instance()
        corrupted_file = TEST_MODELS_PATH_MM / "corrupted_import.json"
        corrupted_file.write_text("[{not_json:")
        assert not manager.import_models(corrupted_file)

    def test_import_models_invalid_model_data_in_file(self):
        manager = self.get_manager_instance()
        provider = "ImportInvalidDataProv"
        import_file_path = TEST_MODELS_PATH_MM / "import_invalid_model.json"
        import_data = {
            provider: [
                {"name": "validModel", "provider": provider},
                {"description": "invalid, no name", "provider": provider} # Inválido
            ]
        }
        with open(import_file_path, "w") as f:
            json.dump(import_data, f)
        
        success = manager.import_models(import_file_path, merge=False)
        assert success # Sucesso parcial, pois um modelo é válido

        imported_models = manager.get_models_for_provider(provider)
        assert len(imported_models) == 1 # Apenas o válido deve ser importado
        assert imported_models[0].name == "validModel"


    # Testes para restore_defaults
    def test_restore_defaults_single_provider_success(self):
        manager = self.get_manager_instance()
        provider_to_restore = "OpenAI" # Assumindo que OpenAI está em DEFAULT_MODELS_DATA
        
        # Criar um arquivo existente para este provedor que será sobrescrito
        self.create_dummy_provider_file(manager, provider_to_restore, [{"name":"customOpenAIModel", "provider":provider_to_restore}])
        assert len(manager.get_models_for_provider(provider_to_restore)) == 1
        assert manager.get_models_for_provider(provider_to_restore)[0].name == "customOpenAIModel"

        success = manager.restore_defaults(provider_name=provider_to_restore)
        assert success

        restored_models = manager.get_models_for_provider(provider_to_restore)
        default_openai_models = DEFAULT_MODELS_DATA.get(provider_to_restore, [])
        
        assert len(restored_models) == len(default_openai_models)
        assert restored_models[0].name == default_openai_models[0]["name"]
        assert restored_models[0].created_by == "system-default" # Verificar um campo dos defaults

    def test_restore_defaults_all_providers_success(self):
        manager = self.get_manager_instance()
        # Criar arquivos customizados para provedores que existem nos defaults
        self.create_dummy_provider_file(manager, "OpenAI", [{"name":"customOpenAI", "provider":"OpenAI"}])
        self.create_dummy_provider_file(manager, "Anthropic", [{"name":"customAnthropic", "provider":"Anthropic"}])
        # E um provedor que não está nos defaults, não deve ser afetado
        self.create_dummy_provider_file(manager, "MyCustomProvider", [{"name":"myModel", "provider":"MyCustomProvider"}])


        success = manager.restore_defaults() # Restaurar todos
        assert success

        # Verificar OpenAI
        openai_restored = manager.get_models_for_provider("OpenAI")
        assert openai_restored[0].name == DEFAULT_MODELS_DATA["OpenAI"][0]["name"]
        
        # Verificar Anthropic
        anthropic_restored = manager.get_models_for_provider("Anthropic")
        assert anthropic_restored[0].name == DEFAULT_MODELS_DATA["Anthropic"][0]["name"]

        # Verificar Google (deve ter sido criado a partir dos defaults)
        google_restored = manager.get_models_for_provider("Google") # Assumindo que Google está nos defaults
        if "Google" in DEFAULT_MODELS_DATA:
            assert len(google_restored) == len(DEFAULT_MODELS_DATA["Google"])
            assert google_restored[0].name == DEFAULT_MODELS_DATA["Google"][0]["name"]
        else: # Caso Google não esteja nos defaults (o teste deve ser ajustado)
            assert not google_restored

        # MyCustomProvider não deve ser tocado pois não está em DEFAULT_MODELS_DATA
        my_custom_models = manager.get_models_for_provider("MyCustomProvider")
        assert len(my_custom_models) == 1
        assert my_custom_models[0].name == "myModel"


    def test_restore_defaults_provider_not_in_defaults(self):
        manager = self.get_manager_instance()
        assert not manager.restore_defaults(provider_name="UnknownProviderNotInDefaults")

    def test_restore_defaults_empty_default_data(self, mocker):
        manager = self.get_manager_instance()
        # Mockar DEFAULT_MODELS_DATA para ser vazio
        mocker.patch("ra_aid_start.core.model_manager.DEFAULT_MODELS_DATA", {})
        assert not manager.restore_defaults() # Nada a restaurar
        assert not manager.restore_defaults(provider_name="AnyProvider") # Provedor não estará em defaults vazios

    def test_restore_defaults_invalid_model_in_defaults(self, mocker):
        manager = self.get_manager_instance()
        provider_with_bad_default = "BadDefaultProv"
        # Mockar DEFAULT_MODELS_DATA para ter um modelo inválido
        # Acessar via o caminho completo para o mock
        bad_defaults = {
            provider_with_bad_default: [
                {"description": "invalid model, no name", "provider": provider_with_bad_default}
            ]
        }
        # O patch deve ser no local onde DEFAULT_MODELS_DATA é importado e usado,
        # que é ra_aid_start.core.model_manager
        mocker.patch("ra_aid_start.core.model_manager.DEFAULT_MODELS_DATA", bad_defaults)
        
        mock_logger_error = mocker.patch.object(manager.logger, 'error')
        success = manager.restore_defaults(provider_name=provider_with_bad_default)
        
        assert not success # Deve falhar porque o único modelo padrão é inválido
        
        # Acessar a mensagem de erro pode ser complicado se ela for formatada dinamicamente.
        # Vamos verificar se o logger foi chamado com uma mensagem que contenha partes esperadas.
        called_with_correct_message = False
        for call_args in mock_logger_error.call_args_list:
            args, _ = call_args
            if len(args) > 0:
                log_message = args[0]
                if (f"Invalid model data in default_models.py for provider '{provider_with_bad_default}'" in log_message and
                        "model 'N/A'" in log_message): # N/A porque o nome está ausente
                    called_with_correct_message = True
                    break
        assert called_with_correct_message

        # O arquivo do provedor não deve ser criado ou deve estar vazio
        assert not manager.get_models_for_provider(provider_with_bad_default)