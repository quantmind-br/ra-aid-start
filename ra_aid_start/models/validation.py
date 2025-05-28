import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

# Supondo que Preset e Model possam ser importados se necessário para type hints
# from ra_aid_start.models.preset import Preset
# from ra_aid_start.models.model import Model

logger = logging.getLogger(__name__)

class ValidationRules:
    """
    Provides static methods for various validation tasks across the application.
    These methods can be used by managers, wizards, or other components
    to ensure data integrity and consistency.
    """

    @staticmethod
    def validate_provider_model_combination(
        provider_name: str,
        model_name: str,
        # model_manager: Optional[Any] = None # ModelManager instance for checking existence
    ) -> List[str]:
        """
        Validates if a given model is compatible or known for a specific provider.
        Initially, this can be a placeholder.
        Later, it might check against a list of known models from ModelManager.

        Args:
            provider_name (str): The name of the LLM provider.
            model_name (str): The name of the model.
            # model_manager: An instance of ModelManager to query available models (optional, for future use).

        Returns:
            List[str]: A list of error messages. Empty if valid.
        """
        errors: List[str] = []
        logger.debug(f"Validating provider '{provider_name}' and model '{model_name}' combination.")
        # Placeholder logic:
        if not provider_name or not provider_name.strip():
            errors.append("Provider name cannot be empty.")
        if not model_name or not model_name.strip():
            errors.append("Model name cannot be empty.")
        
        # Example future logic (requires ModelManager):
        # if model_manager:
        #     provider_models = model_manager.get_models_for_provider(provider_name)
        #     if not any(m.name == model_name for m in provider_models):
        #         errors.append(f"Model '{model_name}' is not a known model for provider '{provider_name}'.")
        
        if not errors:
            logger.info(f"Provider-model combination '{provider_name}'-'{model_name}' passed placeholder validation.")
        else:
            logger.warning(f"Provider-model combination validation failed for '{provider_name}'-'{model_name}': {errors}")
        return errors

    @staticmethod
    def validate_flag_dependencies(
        preset_data: Dict[str, Any] # Or a Preset object
    ) -> List[str]:
        """
        Validates dependencies between different flags or settings in a preset.
        E.g., if '--some-feature-flag' is True, then '--related-setting' must be set.

        Args:
            preset_data (Dict[str, Any]): A dictionary representing preset configuration.

        Returns:
            List[str]: A list of error messages regarding unmet dependencies. Empty if all good.
        """
        errors: List[str] = []
        logger.debug(f"Validating flag dependencies for preset data: {preset_data.get('name', 'N/A')}")
        # Placeholder logic:
        # Example: if preset_data.get("use_aider") and not preset_data.get("aider_git_dir"):
        #     errors.append("Aider integration requires 'aider_git_dir' to be specified.")
        
        if not errors:
            logger.info(f"Flag dependency validation passed for preset '{preset_data.get('name', 'N/A')}' (placeholder).")
        else:
            logger.warning(f"Flag dependency validation failed for preset '{preset_data.get('name', 'N/A')}': {errors}")
        return errors

    @staticmethod
    def validate_conflicting_flags(
        preset_data: Dict[str, Any] # Or a Preset object
    ) -> List[str]:
        """
        Validates for conflicting flags or settings in a preset.
        E.g., '--feature-a' and '--feature-b' cannot both be True.

        Args:
            preset_data (Dict[str, Any]): A dictionary representing preset configuration.

        Returns:
            List[str]: A list of error messages regarding conflicting flags. Empty if no conflicts.
        """
        errors: List[str] = []
        logger.debug(f"Validating conflicting flags for preset data: {preset_data.get('name', 'N/A')}")
        # Placeholder logic:
        # Example: if preset_data.get("mode") == "chat" and preset_data.get("input_file"):
        #    errors.append("Chat mode cannot be used with a specified input file.")

        if not errors:
            logger.info(f"Conflicting flag validation passed for preset '{preset_data.get('name', 'N/A')}' (placeholder).")
        else:
            logger.warning(f"Conflicting flag validation failed for preset '{preset_data.get('name', 'N/A')}': {errors}")
        return errors

    @staticmethod
    def validate_file_paths(
        paths_to_check: Dict[str, Path], # e.g., {"config_file": Path(...), "output_dir": Path(...)}
        check_existence: bool = False,
        check_is_file: Optional[List[str]] = None, # List of keys from paths_to_check that must be files
        check_is_dir: Optional[List[str]] = None   # List of keys from paths_to_check that must be dirs
    ) -> List[str]:
        """
        Validates a list of file or directory paths.

        Args:
            paths_to_check (Dict[str, Path]): A dictionary where keys are descriptive names
                                             and values are Path objects.
            check_existence (bool): If True, checks if each path exists.
            check_is_file (Optional[List[str]]): List of keys that must point to existing files.
            check_is_dir (Optional[List[str]]): List of keys that must point to existing directories.

        Returns:
            List[str]: A list of error messages. Empty if all paths are valid.
        """
        errors: List[str] = []
        logger.debug(f"Validating file paths: {paths_to_check}")

        if check_is_file is None:
            check_is_file = []
        if check_is_dir is None:
            check_is_dir = []

        for name, path_obj in paths_to_check.items():
            if not isinstance(path_obj, Path):
                errors.append(f"Path for '{name}' is not a valid Path object: {path_obj}")
                continue

            if check_existence or name in check_is_file or name in check_is_dir:
                if not path_obj.exists():
                    errors.append(f"Path for '{name}' does not exist: {path_obj}")
                    continue # Skip further checks if it doesn't exist

            if name in check_is_file:
                if not path_obj.is_file():
                    errors.append(f"Path for '{name}' is not a file: {path_obj}")
            
            if name in check_is_dir:
                if not path_obj.is_dir():
                    errors.append(f"Path for '{name}' is not a directory: {path_obj}")
        
        if not errors:
            logger.info(f"File path validation passed (placeholder checks).")
        else:
            logger.warning(f"File path validation failed: {errors}")
        return errors

    @staticmethod
    def validate_numeric_ranges(
        values_to_check: Dict[str, Any], # e.g., {"temperature": 0.5, "max_tokens": 100}
        range_constraints: Dict[str, Tuple[Optional[float], Optional[float]]] 
        # e.g., {"temperature": (0.0, 1.0), "max_tokens": (1, None)}
    ) -> List[str]:
        """
        Validates if numeric values fall within specified ranges.

        Args:
            values_to_check (Dict[str, Any]): Dictionary of numeric values.
            range_constraints (Dict[str, Tuple[Optional[float], Optional[float]]]):
                Dictionary defining min (inclusive) and max (inclusive) for each value.
                None means no bound on that side.

        Returns:
            List[str]: A list of error messages. Empty if all values are within ranges.
        """
        errors: List[str] = []
        logger.debug(f"Validating numeric ranges for values: {values_to_check}")

        for name, value in values_to_check.items():
            if name not in range_constraints:
                logger.debug(f"No range constraint defined for '{name}'. Skipping.")
                continue

            if not isinstance(value, (int, float)):
                errors.append(f"Value for '{name}' is not numeric: {value}")
                continue

            min_val, max_val = range_constraints[name]

            if min_val is not None and value < min_val:
                errors.append(f"Value for '{name}' ({value}) is less than minimum allowed ({min_val}).")
            
            if max_val is not None and value > max_val:
                errors.append(f"Value for '{name}' ({value}) is greater than maximum allowed ({max_val}).")
        
        if not errors:
            logger.info(f"Numeric range validation passed (placeholder checks).")
        else:
            logger.warning(f"Numeric range validation failed: {errors}")
        return errors

    @classmethod
    def validate_all_preset_data(cls, preset_data: Dict[str, Any]) -> List[str]:
        """
        Executa todas as validações relevantes nos dados do preset coletados.
        Este é um método de conveniência que chama validadores mais específicos.
        """
        all_errors: List[str] = []
        logger.debug(f"Iniciando validação geral para preset: {preset_data.get('name', 'N/A')}")

        # Validação de combinação provedor/modelo (exemplo para main_model)
        # Em uma implementação real, isso seria feito para todos os modelos configurados (expert, specialized)
        if preset_data.get("main_model_provider") and preset_data.get("main_model_name"):
            all_errors.extend(cls.validate_provider_model_combination(
                str(preset_data.get("main_model_provider")),
                str(preset_data.get("main_model_name"))
            ))
        
        # Validação de dependências de flags
        all_errors.extend(cls.validate_flag_dependencies(preset_data))

        # Validação de flags conflitantes
        all_errors.extend(cls.validate_conflicting_flags(preset_data))

        # Validação de caminhos de arquivo (exemplo)
        paths_to_validate: Dict[str, Path] = {}
        file_path_keys = ["chat_history_file", "chat_persona_file", "project_state_dir", "custom_tools", "log_file", "aider_config"]
        for key in file_path_keys:
            if preset_data.get(key):
                try:
                    paths_to_validate[key] = Path(str(preset_data[key]))
                except TypeError:
                     all_errors.append(f"Valor inválido para o caminho '{key}': {preset_data[key]}")


        # Define quais chaves devem ser arquivos ou diretórios (exemplo, pode precisar de mais lógica)
        # Por enquanto, apenas verificamos se são paths válidos se fornecidos, sem checar existência ou tipo.
        if paths_to_validate:
             all_errors.extend(cls.validate_file_paths(paths_to_validate, check_existence=False))


        # Validação de intervalos numéricos (exemplo)
        numeric_values: Dict[str, Any] = {}
        numeric_constraints: Dict[str, Tuple[Optional[float], Optional[float]]] = {}
        
        numeric_fields_with_constraints = {
            "recursion_limit": (0, None),
            "max_total_tokens": (1, None),
            "max_input_tokens": (1, None),
            "max_output_tokens": (1, None),
            "temperature": (0.0, 2.0),
            "top_p": (0.0, 1.0),
            "top_k": (0, None),
            "frequency_penalty": (-2.0, 2.0),
            "presence_penalty": (-2.0, 2.0),
            "api_port": (0, 65535)
        }

        for field, constraint in numeric_fields_with_constraints.items():
            if preset_data.get(field) is not None: # Apenas validar se o valor foi fornecido
                numeric_values[field] = preset_data[field]
                numeric_constraints[field] = constraint
        
        if numeric_values:
            all_errors.extend(cls.validate_numeric_ranges(numeric_values, numeric_constraints))

        if not all_errors:
            logger.info(f"Validação geral de dados do preset '{preset_data.get('name', 'N/A')}' passou (placeholders podem estar ativos).")
        else:
            logger.warning(f"Validação geral de dados do preset '{preset_data.get('name', 'N/A')}' encontrou erros: {all_errors}")
        
        return all_errors


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    print("--- Testing validate_provider_model_combination ---")
    errors_pm = ValidationRules.validate_provider_model_combination("OpenAI", "gpt-4o")
    print(f"Provider-Model errors (should be empty): {errors_pm}")
    assert not errors_pm
    errors_pm_fail = ValidationRules.validate_provider_model_combination("", "gpt-4o")
    print(f"Provider-Model errors (should have error): {errors_pm_fail}")
    assert len(errors_pm_fail) > 0

    print("\n--- Testing validate_flag_dependencies (placeholder) ---")
    dummy_preset_data = {"name": "TestPreset", "use_aider": True, "aider_git_dir": "/path/to/git"}
    errors_fd = ValidationRules.validate_flag_dependencies(dummy_preset_data)
    print(f"Flag dependency errors (should be empty for placeholder): {errors_fd}")
    assert not errors_fd
    
    # Example for future:
    # dummy_preset_data_fail = {"name": "TestPresetFail", "use_aider": True}
    # errors_fd_fail = ValidationRules.validate_flag_dependencies(dummy_preset_data_fail) # Assuming rule is active
    # print(f"Flag dependency errors (should have error if rule active): {errors_fd_fail}")
    # assert len(errors_fd_fail) > 0 


    print("\n--- Testing validate_conflicting_flags (placeholder) ---")
    errors_cf = ValidationRules.validate_conflicting_flags(dummy_preset_data)
    print(f"Conflicting flag errors (should be empty for placeholder): {errors_cf}")
    assert not errors_cf

    print("\n--- Testing validate_file_paths ---")
    # Create dummy files/dirs for testing
    test_dir = Path("./temp_validation_test_dir")
    test_file = test_dir / "test_file.txt"
    if not test_dir.exists():
        test_dir.mkdir(parents=True, exist_ok=True)
    if not test_file.exists():
        with open(test_file, "w") as f:
            f.write("test")
            
    paths = {
        "config": test_file, 
        "output": test_dir,
        "non_existent": Path("./non_existent_file.tmp")
    }
    errors_fp = ValidationRules.validate_file_paths(
        paths, 
        check_existence=False, 
        check_is_file=["config"], 
        check_is_dir=["output"]
    )
    print(f"File path errors (should be empty): {errors_fp}")
    assert not errors_fp
    
    errors_fp_exist = ValidationRules.validate_file_paths(
        paths, 
        check_existence=True
    )
    print(f"File path errors with existence check (should have 1 error for non_existent): {errors_fp_exist}")
    assert len(errors_fp_exist) == 1
    assert any("non_existent" in e for e in errors_fp_exist)

    # Clean up dummy files/dirs
    if test_file.exists():
        test_file.unlink()
    if test_dir.exists():
        test_dir.rmdir()


    print("\n--- Testing validate_numeric_ranges ---")
    values = {"temperature": 0.7, "max_tokens": 2000, "invalid_val": "abc"}
    constraints = {
        "temperature": (0.0, 1.0),
        "max_tokens": (1, 4096),
        "invalid_val": (0, 100) # This will also catch type error
    }
    errors_nr = ValidationRules.validate_numeric_ranges(values, constraints)
    print(f"Numeric range errors (should have 1 for invalid_val type): {errors_nr}")
    assert len(errors_nr) == 1
    assert any("invalid_val" in e and "not numeric" in e for e in errors_nr)

    values_fail = {"temperature": 1.5, "max_tokens": 0}
    errors_nr_fail = ValidationRules.validate_numeric_ranges(values_fail, constraints)
    print(f"Numeric range errors (should have 2 errors): {errors_nr_fail}")
    assert len(errors_nr_fail) == 2

    print("\n--- Testing validate_all_preset_data ---")
    valid_data = {
        "name": "TestValidPreset",
        "main_model_provider": "OpenAI",
        "main_model_name": "gpt-4o",
        "temperature": 0.7,
        "log_file": "some.log" # Será convertido para Path
    }
    errors_all_valid = ValidationRules.validate_all_preset_data(valid_data)
    print(f"All preset data errors (valid, should be empty): {errors_all_valid}")
    assert not errors_all_valid

    invalid_data_temp = {
        "name": "TestInvalidTemp",
        "main_model_provider": "OpenAI",
        "main_model_name": "gpt-4o",
        "temperature": 2.5 # Fora do intervalo
    }
    errors_all_invalid_temp = ValidationRules.validate_all_preset_data(invalid_data_temp)
    print(f"All preset data errors (invalid temp): {errors_all_invalid_temp}")
    assert len(errors_all_invalid_temp) == 1
    assert any("temperature" in e for e in errors_all_invalid_temp)
    
    print("\nValidationRules example usage finished.")