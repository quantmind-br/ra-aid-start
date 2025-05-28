import logging
import subprocess # Adicionado
import shlex      # Adicionado
from pathlib import Path
from typing import List, Optional

from ra_aid_start.models.preset import Preset
from ra_aid_start.core.command_builder import CommandBuilder
from ra_aid_start.utils.json_handler import load_json, save_json, JsonHandlerError
from ra_aid_start.utils.file_handler import ensure_dir_exists

# Configure logger for this module
logger = logging.getLogger(__name__)
# Example: logging.basicConfig(level=logging.DEBUG) # Set level as needed

DEFAULT_PRESETS_DIR_NAME = "presets"

class PresetManagerError(Exception):
    """Custom exception for PresetManager errors."""
    pass

class PresetManager:
    """Manages CRUD operations for presets."""

    def __init__(self, base_storage_path: Path):
        """
        Initializes the PresetManager.

        Args:
            base_storage_path (Path): The base directory for ra-aid-start data
                                      (e.g., Path.home() / ".ra-aid-start").
        """
        self.storage_path = base_storage_path / DEFAULT_PRESETS_DIR_NAME
        try:
            ensure_dir_exists(self.storage_path / "dummy_file_for_dir_creation.tmp") # Ensure presets dir exists
            logger.info(f"PresetManager initialized. Storage path: {self.storage_path}")
        except Exception as e:
            logger.error(f"Failed to ensure or create preset storage directory {self.storage_path}: {e}")
            # Depending on desired behavior, could re-raise or handle
            raise PresetManagerError(f"Could not initialize preset storage at {self.storage_path}: {e}") from e

    def _get_preset_path(self, name: str) -> Path:
        """Constructs the full path for a preset file given its name."""
        # Sanitize name to prevent path traversal issues, though Path should handle most.
        # For simplicity, we assume names are valid filenames here.
        # Consider adding more robust sanitization if names come from untrusted sources.
        if not name or "/" in name or "\\" in name or ".." in name:
            raise ValueError(f"Invalid preset name: {name}")
        return self.storage_path / f"{name}.json"

    def load_preset(self, name: str) -> Optional[Preset]:
        """
        Loads a specific preset by its name.

        Args:
            name (str): The name of the preset (without .json extension).

        Returns:
            Optional[Preset]: The loaded Preset object, or None if not found or error occurs.
        """
        if not name:
            logger.warning("Attempted to load preset with empty name.")
            return None
        
        preset_file_path = self._get_preset_path(name)
        logger.debug(f"Attempting to load preset from: {preset_file_path}")

        try:
            data = load_json(preset_file_path)
            preset = Preset.from_dict(data)
            logger.info(f"Preset '{name}' loaded successfully from {preset_file_path}.")
            return preset
        except JsonHandlerError as e:
            # Specific error from load_json (e.g., file not found, decode error)
            if "file not found" in str(e).lower():
                 logger.info(f"Preset file for '{name}' not found at {preset_file_path}.")
            else:
                logger.error(f"Error loading preset '{name}' from {preset_file_path}: {e}")
            return None
        except ValueError as e: # For pydantic validation errors during Preset.from_dict
            logger.error(f"Data validation error for preset '{name}' from {preset_file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred while loading preset '{name}': {e}")
            return None

    def list_presets(self) -> List[Preset]:
        """
        Lists all available presets.

        Returns:
            List[Preset]: A list of all loaded Preset objects.
        """
        presets: List[Preset] = []
        if not self.storage_path.exists() or not self.storage_path.is_dir():
            logger.warning(f"Preset storage directory {self.storage_path} does not exist or is not a directory.")
            return presets

        logger.debug(f"Listing presets from directory: {self.storage_path}")
        for preset_file in self.storage_path.glob("*.json"):
            preset_name = preset_file.stem # Name without .json extension
            try:
                # Re-use load_preset logic for consistency and error handling
                preset = self.load_preset(preset_name)
                if preset:
                    presets.append(preset)
            except Exception as e: # Catch any unexpected error during individual load
                logger.error(f"Failed to load preset '{preset_name}' during list operation: {e}")
        
        logger.info(f"Found {len(presets)} presets in {self.storage_path}.")
        return presets

    # Placeholder for save_preset, to be implemented in a subsequent task
    def save_preset(self, preset: Preset) -> bool:
        """
        Saves a Preset object to a JSON file.
        The filename will be preset.name.json.
        Updates the preset's updated_at timestamp before saving.

        Args:
            preset (Preset): The Preset object to save.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not preset.name:
            logger.error("Cannot save preset with an empty name.")
            return False
        
        # Gerar a string de comando usando CommandBuilder e atribuir ao preset
        try:
            builder = CommandBuilder()
            preset.command = builder.build_command_from_preset(preset)
            logger.debug(f"Generated command for preset '{preset.name}': {preset.command}")
        except Exception as e:
            logger.error(f"Failed to build command for preset '{preset.name}': {e}")
            # Decide if this should be a fatal error for saving
            # Por enquanto, vamos permitir salvar sem o comando se a construção falhar,
            # mas logar o erro. O campo command terá seu valor default (string vazia).
            # Alternativamente, poderia retornar False aqui.
            pass # preset.command manterá o valor que tinha (ou default se novo)

        preset.update_timestamp() # Update 'updated_at' before saving
        preset_file_path = self._get_preset_path(preset.name)
        logger.debug(f"Attempting to save preset '{preset.name}' to: {preset_file_path}")

        try:
            # Ensure the preset data is valid before saving (optional, Pydantic does this on creation)
            # if not preset.validate_preset(): # Assuming validate_preset raises an error or returns bool
            #     logger.error(f"Preset '{preset.name}' failed validation. Not saving.")
            #     return False
            
            preset_data = preset.to_dict()
            save_json(preset_file_path, preset_data)
            logger.info(f"Preset '{preset.name}' saved successfully to {preset_file_path}.")
            return True
        except JsonHandlerError as e:
            logger.error(f"Error saving preset '{preset.name}' to {preset_file_path}: {e}")
            return False
        except ValueError as e: # From _get_preset_path if name is invalid
             logger.error(f"Error saving preset: {e}")
             return False
        except Exception as e:
            logger.error(f"An unexpected error occurred while saving preset '{preset.name}': {e}")
            return False

    def create_preset(self, preset_data: dict) -> Optional[Preset]:
        """
        Creates a new Preset object from dictionary data, validates it,
        and saves it to a JSON file.

        Args:
            preset_data (dict): A dictionary containing the data for the new preset.
                                Must include 'name' and 'operation_mode'.

        Returns:
            Optional[Preset]: The created Preset object if successful, None otherwise.
        """
        try:
            preset = Preset.from_dict(preset_data) # Pydantic handles initial validation
            # You can add more business logic validation here if needed using preset.validate_preset()
            # For example:
            # if not preset.validate_preset():
            #     logger.error(f"Preset data for '{preset.name}' failed custom validation.")
            #     # Consider raising PresetManagerError or returning None based on strictness
            #     return None

        except ValueError as e: # Pydantic validation error
            logger.error(f"Invalid data for creating preset: {e}")
            return None
        except Exception as e: # Other unexpected errors during Preset creation
            logger.error(f"Unexpected error creating Preset object: {e}")
            return None

        if self.save_preset(preset):
            logger.info(f"Preset '{preset.name}' created and saved successfully.")
            return preset
        else:
            # save_preset already logs its errors
            logger.error(f"Failed to save newly created preset '{preset.name}'.")
            return None

    def update_preset(self, name: str, update_data: dict) -> Optional[Preset]:
        """
        Updates an existing preset with new data.

        Args:
            name (str): The name of the preset to update.
            update_data (dict): A dictionary containing the fields to update.
                                'created_at' and 'name' (if present) in update_data are ignored.

        Returns:
            Optional[Preset]: The updated Preset object if successful, None otherwise.
        """
        existing_preset = self.load_preset(name)
        if not existing_preset:
            logger.error(f"Cannot update preset: Preset '{name}' not found.")
            return None

        # Preserve original name and creation timestamp
        update_data.pop('name', None) # Name change should be handled by a rename/copy+delete operation
        update_data.pop('created_at', None)

        try:
            # Create a new Preset object with updated fields
            # This leverages Pydantic's validation for the updated data
            updated_preset_data = existing_preset.model_dump() # Get current data as dict
            updated_preset_data.update(update_data) # Apply changes
            
            # Ensure 'name' is present for Pydantic model creation, even if not changed
            if 'name' not in updated_preset_data:
                 updated_preset_data['name'] = existing_preset.name


            updated_preset = Preset(**updated_preset_data) # Re-validate with new data
            # updated_preset.created_at = existing_preset.created_at # Ensure created_at is not changed

        except ValueError as e: # Pydantic validation error on update
            logger.error(f"Invalid data for updating preset '{name}': {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error preparing preset update for '{name}': {e}")
            return None
        
        # The save_preset method will handle updating the 'updated_at' timestamp.
        if self.save_preset(updated_preset):
            logger.info(f"Preset '{name}' updated and saved successfully.")
            return updated_preset
        else:
            # save_preset logs its errors
            logger.error(f"Failed to save updated preset '{name}'.")
            return None

    def delete_preset(self, name: str) -> bool:
        """
        Deletes a preset file.

        Args:
            name (str): The name of the preset to delete.

        Returns:
            bool: True if successful or file did not exist, False if an error occurred during deletion.
        """
        if not name:
            logger.warning("Attempted to delete preset with empty name.")
            return False # Or raise ValueError

        try:
            preset_file_path = self._get_preset_path(name)
            if preset_file_path.exists():
                preset_file_path.unlink()
                logger.info(f"Preset '{name}' deleted successfully from {preset_file_path}.")
                return True
            else:
                logger.info(f"Preset '{name}' not found at {preset_file_path}. Nothing to delete.")
                return True # Considered success as the state (not existing) is achieved
        except ValueError as e: # From _get_preset_path
            logger.error(f"Invalid preset name for deletion: {name}. Error: {e}")
            return False
        except OSError as e:
            logger.error(f"Error deleting preset file {preset_file_path}: {e}")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred while deleting preset '{name}': {e}")
            return False

    def execute_preset(self, name: str, current_dir: Optional[Path] = None) -> bool:
        """
        (Simulated) Executes a preset.
        Loads the preset and 'executes' its command.
        Actual command execution will use subprocess and be more complex.

        Args:
            name (str): The name of the preset to execute.
            current_dir (Optional[Path]): The directory where the command should be executed.
                                         Defaults to the current working directory if None.

        Returns:
            bool: True if the command was 'executed' (simulated), False otherwise.
        """
        preset = self.load_preset(name)
        if not preset:
            logger.error(f"Cannot execute preset: Preset '{name}' not found or failed to load.")
            return False

        if not preset.command:
            logger.warning(f"Preset '{name}' has no command defined. Nothing to execute.")
            return False # Or True, depending on desired behavior for empty command

        try:
            effective_cwd = current_dir or Path.cwd()
            logger.info(f"Executing command for preset '{name}' in directory '{effective_cwd}': {preset.command}")
            
            # Usar shell=True permite que 'preset.command' seja uma string completa como seria digitada no terminal.
            # Para maior segurança e controle, shell=False e shlex.split(preset.command) é geralmente recomendado,
            # mas shell=True é mais simples se os comandos são complexos e construídos para o shell.
            # Dado que os presets são gerenciados pelo usuário, shell=True é um risco aceitável aqui.
            
            # O comando será executado e o programa Python esperará sua conclusão.
            # stdout e stderr são capturados.
            result = subprocess.run(
                preset.command,
                cwd=effective_cwd,
                shell=True,
                check=True,       # Levanta CalledProcessError em código de saída não-zero
                capture_output=True,
                text=True         # Decodifica stdout/stderr como texto
            )
            logger.info(f"Command for preset '{name}' executed successfully.")
            if result.stdout: # Log stdout apenas se não estiver vazio
                logger.info(f"Stdout:\n{result.stdout.strip()}")
            if result.stderr: # Log stderr apenas se não estiver vazio
                logger.warning(f"Stderr:\n{result.stderr.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Command for preset '{name}' failed with exit code {e.returncode}.")
            if e.stdout: # Log stdout da exceção apenas se não estiver vazio
                logger.error(f"Stdout (from error):\n{e.stdout.strip()}")
            if e.stderr: # Log stderr da exceção apenas se não estiver vazio
                logger.error(f"Stderr (from error):\n{e.stderr.strip()}")
            return False
        except FileNotFoundError:
            # Isso acontece se o comando em si (ex: 'ra-aid') não for encontrado no PATH ou como executável.
            cmd_to_report = preset.command.split()[0] if preset.command else "N/A"
            logger.error(f"Command not found when trying to execute for preset '{name}': {cmd_to_report}")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred during command execution for preset '{name}': {e}")
            return False


if __name__ == '__main__':
    # Setup basic logging for standalone script execution
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Example usage:
    # Create a temporary directory for testing
    temp_storage_dir = Path.home() / ".ra-aid-start-test-presets"
    
    # Clean up previous test run if any
    import shutil
    if temp_storage_dir.exists():
        shutil.rmtree(temp_storage_dir)
    
    pm = PresetManager(base_storage_path=temp_storage_dir.parent) # Pass parent so it creates ".ra-aid-start-test-presets/presets"

    # Test with an empty directory
    print("\n--- Testing with empty directory ---")
    all_presets_empty = pm.list_presets()
    print(f"Listed presets (empty): {len(all_presets_empty)}")
    assert len(all_presets_empty) == 0
    loaded_empty = pm.load_preset("non_existent_preset")
    print(f"Loaded non-existent preset: {loaded_empty}")
    assert loaded_empty is None

    # Create some dummy preset files for testing
    print("\n--- Creating dummy preset files ---")
    
    preset1_data = {
        "name": "test_preset_1",
        "description": "First test preset",
        "operation_mode": "chat",
        "flags": {"--model": "gpt-4"},
        "command": "ra-aid --model gpt-4"
    }
    # Manually save for testing load, or use pm.save_preset if available and tested
    # ensure_dir_exists(pm.storage_path / "dummy.tmp") # Ensure storage_path itself exists
    # save_json(pm.storage_path / "test_preset_1.json", preset1_data)
    
    preset_obj1 = Preset(**preset1_data)
    save_success1 = pm.save_preset(preset_obj1) # Using the save_preset method now
    print(f"Save preset 1 success: {save_success1}")


    preset2_data = {
        "name": "test_preset_2",
        "description": "Second test preset with more flags",
        "operation_mode": "file_diff",
        "flags": {"--file": "input.txt", "--diff": "changes.diff", "--yes": True},
        "command": "ra-aid --file input.txt --diff changes.diff --yes"
    }
    # save_json(pm.storage_path / "test_preset_2.json", preset2_data)
    preset_obj2 = Preset(**preset2_data)
    save_success2 = pm.save_preset(preset_obj2)
    print(f"Save preset 2 success: {save_success2}")


    # Create an invalid JSON file
    with open(pm.storage_path / "invalid_preset.json", "w") as f:
        f.write("{'name': 'invalid', 'description': 'this is not valid json',")
    print("Created invalid_preset.json")

    # Test list_presets
    print("\n--- Testing list_presets ---")
    all_presets = pm.list_presets()
    print(f"Number of presets found: {len(all_presets)}")
    for p in all_presets:
        print(f"  - {p.name}: {p.description}")
    assert len(all_presets) == 2 # Should only load valid ones

    # Test load_preset
    print("\n--- Testing load_preset ---")
    loaded_preset1 = pm.load_preset("test_preset_1")
    if loaded_preset1:
        print(f"Loaded test_preset_1: {loaded_preset1.name}, Command: {loaded_preset1.command}")
        assert loaded_preset1.name == "test_preset_1"
        assert loaded_preset1.flags.get("--model") == "gpt-4"
    else:
        print("Failed to load test_preset_1")
        assert False, "test_preset_1 should have loaded"

    loaded_preset_non_existent = pm.load_preset("non_existent_preset_again")
    print(f"Loaded non_existent_preset_again: {loaded_preset_non_existent}")
    assert loaded_preset_non_existent is None

    loaded_invalid = pm.load_preset("invalid_preset")
    print(f"Loaded invalid_preset: {loaded_invalid}")
    assert loaded_invalid is None # Should fail due to JSONDecodeError or Pydantic error

    # Test loading preset with invalid name
    print("\n--- Testing load_preset with invalid name ---")
    try:
        pm.load_preset("../../../etc/passwd") # Example of potentially malicious name
    except ValueError as e:
        print(f"Correctly caught ValueError for invalid name: {e}")
    
    # Clean up the temporary directory
    # import shutil # Already imported
    if temp_storage_dir.exists():
        shutil.rmtree(temp_storage_dir)
        logger.info(f"Cleaned up temporary test directory: {temp_storage_dir}")
    
    print("\nPresetManager example usage finished.")