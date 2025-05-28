import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from ra_aid_start.models.model import Model
from ra_aid_start.utils.json_handler import load_json, save_json, JsonHandlerError
from ra_aid_start.utils.file_handler import ensure_dir_exists
from ra_aid_start.data.default_models import DEFAULT_MODELS_DATA

# Configure logger for this module
logger = logging.getLogger(__name__)
# Example: logging.basicConfig(level=logging.DEBUG)

DEFAULT_MODELS_DIR_NAME = "models" # Subdiretório para arquivos de modelo por provedor

class ModelManagerError(Exception):
    """Custom exception for ModelManager errors."""
    pass

class ModelManager:
    """Manages LLM models, organized by provider."""

    def __init__(self, base_storage_path: Path):
        """
        Initializes the ModelManager.

        Args:
            base_storage_path (Path): The base directory for ra-aid-start data
                                      (e.g., Path.home() / ".ra-aid-start").
                                      Models will be stored in a 'models' subdirectory.
        """
        self.storage_path = base_storage_path / DEFAULT_MODELS_DIR_NAME
        try:
            # Ensure the main models directory exists
            ensure_dir_exists(self.storage_path / "dummy_file_for_dir_creation.tmp")
            logger.info(f"ModelManager initialized. Storage path for models: {self.storage_path}")

            logger.info(f"Checking for default model files in {self.storage_path} against DEFAULT_MODELS_DATA...")
            default_providers_restored_count = 0
            for provider_key_in_defaults in DEFAULT_MODELS_DATA.keys():
                try:
                    provider_file_path = self._get_provider_file_path(provider_key_in_defaults)
                    if not provider_file_path.exists():
                        logger.info(f"Model file for default provider '{provider_key_in_defaults}' not found at {provider_file_path}. Attempting to restore.")
                        models_to_save = []
                        for m_data in DEFAULT_MODELS_DATA[provider_key_in_defaults]:
                            # Ensure 'provider' field is consistent with the key if missing or different in data
                            if 'provider' not in m_data or m_data['provider'] != provider_key_in_defaults:
                                m_data_copy = m_data.copy() # Avoid modifying DEFAULT_MODELS_DATA directly
                                m_data_copy['provider'] = provider_key_in_defaults
                                models_to_save.append(Model(**m_data_copy))
                            else:
                                models_to_save.append(Model(**m_data))
                        
                        if self.save_models_for_provider(provider_key_in_defaults, models_to_save):
                            logger.info(f"Successfully restored default models for provider '{provider_key_in_defaults}'.")
                            default_providers_restored_count += 1
                        else:
                            logger.error(f"Failed to restore default models for provider '{provider_key_in_defaults}'.")
                except Exception as e_restore_specific:
                    logger.error(f"Error during specific restore check for provider '{provider_key_in_defaults}': {e_restore_specific}")

            if default_providers_restored_count > 0:
                logger.info(f"Restored default models for {default_providers_restored_count} provider(s).")
            
            # Final check: if still no model files, it's an issue (e.g., DEFAULT_MODELS_DATA was empty or all saves failed)
            if not any(self.storage_path.glob("*_models.json")):
                logger.warning(f"After checks, no provider model files exist in {self.storage_path}. Model list may be empty. This could be due to empty DEFAULT_MODELS_DATA or save failures.")

        except Exception as e:
            logger.error(f"Failed to ensure or create model storage directory {self.storage_path}: {e}")
            raise ModelManagerError(f"Could not initialize model storage at {self.storage_path}: {e}") from e

    def _get_provider_file_path(self, provider: str) -> Path:
        """
        Constructs the full path for a provider's model file.
        Converts provider name to lowercase and replaces spaces/special chars for filename.
        """
        if not provider or not provider.strip():
            raise ValueError("Provider name cannot be empty.")
        
        # Simple sanitization for filename: lowercase, replace space with underscore
        # More robust slugification might be needed for broader character sets.
        sanitized_provider_name = provider.lower().replace(" ", "_").replace("/", "_").replace("\\", "_")
        # Remove other potentially problematic characters for filenames
        sanitized_provider_name = "".join(c for c in sanitized_provider_name if c.isalnum() or c in ['_', '-'])
        if not sanitized_provider_name: # if all chars were problematic
             raise ValueError(f"Provider name '{provider}' results in an empty sanitized name.")

        return self.storage_path / f"{sanitized_provider_name}_models.json"

    def get_models_for_provider(self, provider: str) -> List[Model]:
        """
        Loads all models for a specific provider from its JSON file.
        The file is expected to contain a list of model dictionaries.

        Args:
            provider (str): The name of the provider.

        Returns:
            List[Model]: A list of Model objects for the provider. Returns an empty list
                         if the provider file is not found or contains invalid data.
        """
        models: List[Model] = []
        if not provider or not provider.strip():
            logger.warning("Attempted to get models for an empty provider name.")
            return models

        try:
            provider_file_path = self._get_provider_file_path(provider)
            logger.debug(f"Attempting to load models for provider '{provider}' from: {provider_file_path}")

            if not provider_file_path.exists():
                logger.info(f"Model file for provider '{provider}' not found at {provider_file_path}. Returning empty list.")
                return models

            # load_json should return a list of dicts for this case
            data_list = load_json(provider_file_path)
            
            if not isinstance(data_list, list):
                logger.error(f"Model file for provider '{provider}' at {provider_file_path} does not contain a list. Found type: {type(data_list)}")
                return models

            for model_data in data_list:
                if not isinstance(model_data, dict):
                    logger.warning(f"Skipping non-dictionary item in model list for provider '{provider}': {model_data}")
                    continue
                try:
                    # Ensure provider field in model_data matches, or set it if missing
                    if 'provider' not in model_data:
                        model_data['provider'] = provider # Set provider if not in the data
                    elif model_data['provider'] != provider:
                        logger.warning(f"Model data for provider '{provider}' has mismatched provider field: '{model_data['provider']}'. Using '{provider}'.")
                        model_data['provider'] = provider
                        
                    models.append(Model(**model_data)) # Pydantic handles validation
                except ValueError as ve: # Pydantic validation error
                    logger.error(f"Invalid model data for provider '{provider}' in file {provider_file_path}. Details: {ve}. Data: {model_data}")
                except Exception as e_inner:
                    logger.error(f"Unexpected error parsing a model for provider '{provider}'. Details: {e_inner}. Data: {model_data}")
            
            logger.info(f"Successfully loaded {len(models)} models for provider '{provider}'.")

        except ValueError as ve_path: # From _get_provider_file_path
            logger.error(f"Cannot get models for provider '{provider}': {ve_path}")
        except JsonHandlerError as e:
            logger.error(f"Error loading model file for provider '{provider}': {e}")
        except Exception as e_outer:
            logger.error(f"An unexpected error occurred while getting models for provider '{provider}': {e_outer}")
            
        return models

    def get_available_providers(self) -> List[str]:
        """
        Lists all unique provider names for which model files exist.

        Returns:
            List[str]: A list of unique provider names.
        """
        providers = set()
        if not self.storage_path.exists() or not self.storage_path.is_dir():
            logger.warning(f"Model storage directory {self.storage_path} not found. Cannot list providers.")
            return []

        for provider_file_path in self.storage_path.glob("*_models.json"):
            try:
                models_data_list = load_json(provider_file_path) # List[Dict]
                if isinstance(models_data_list, list) and models_data_list:
                    first_model_data = models_data_list[0]
                    if isinstance(first_model_data, dict) and 'provider' in first_model_data:
                        providers.add(first_model_data['provider'])
                    else:
                        logger.warning(f"Could not determine provider from data in {provider_file_path} for provider listing. File might be empty or malformed.")
            except JsonHandlerError as jhe:
                logger.error(f"Error loading file {provider_file_path} for listing providers: {jhe}")
            except Exception as e: # Catch any other unexpected error during file processing
                logger.error(f"Unexpected error processing file {provider_file_path} for listing providers: {e}")
        
        sorted_providers = sorted(list(providers))
        logger.info(f"Found available providers: {sorted_providers}")
        return sorted_providers

    # Placeholder for saving models, to be implemented in a subsequent task
    def save_models_for_provider(self, provider: str, models_list: List[Model]) -> bool:
        """
        Saves a list of Model objects for a specific provider to its JSON file.
        Overwrites the existing file for that provider.

        Args:
            provider (str): The name of the provider.
            models_list (List[Model]): A list of Model objects to save.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not provider or not provider.strip():
            logger.error("Provider name cannot be empty when saving models.")
            return False

        try:
            provider_file_path = self._get_provider_file_path(provider)
            logger.debug(f"Attempting to save {len(models_list)} models for provider '{provider}' to: {provider_file_path}")
            
            # Convert list of Model objects to list of dicts
            data_to_save = [model.model_dump(mode='json') for model in models_list]
            
            save_json(provider_file_path, data_to_save)
            logger.info(f"Successfully saved {len(models_list)} models for provider '{provider}' to {provider_file_path}.")
            return True
        except ValueError as ve_path: # From _get_provider_file_path
            logger.error(f"Cannot save models for provider '{provider}': {ve_path}")
            return False
        except JsonHandlerError as e:
            logger.error(f"Error saving model file for provider '{provider}': {e}")
            return False
        except Exception as e_outer: # Catch any other unexpected error
            logger.error(f"An unexpected error occurred while saving models for provider '{provider}': {e_outer}")
            return False

    def add_model(self, provider: str, model_data: Dict[str, Any]) -> Optional[Model]:
        """
        Adds a new model to the specified provider.
        The model_data must include 'name'. The 'provider' field in model_data
        will be overridden by the 'provider' argument if different.

        Args:
            provider (str): The name of the provider.
            model_data (Dict[str, Any]): A dictionary containing the data for the new model.

        Returns:
            Optional[Model]: The created Model object if successful, None otherwise.
        """
        if not provider or not provider.strip():
            logger.error("Provider name cannot be empty when adding a model.")
            return None
        
        # Ensure the provider in model_data matches the specified provider, or set it.
        if 'provider' not in model_data or model_data['provider'] != provider:
            logger.warning(f"Provider in model_data ('{model_data.get('provider')}') differs from target provider ('{provider}'). Overriding to '{provider}'.")
            model_data['provider'] = provider

        try:
            new_model = Model(**model_data) # Validate data by creating Model instance
        except ValueError as ve: # Pydantic validation error
            logger.error(f"Invalid data for new model under provider '{provider}': {ve}. Data: {model_data}")
            return None
        except Exception as e:
             logger.error(f"Unexpected error creating Model object for provider '{provider}': {e}. Data: {model_data}")
             return None

        models_list = self.get_models_for_provider(provider)

        # Check if model with the same name already exists for this provider
        for existing_model in models_list:
            if existing_model.name == new_model.name:
                logger.error(f"Model with name '{new_model.name}' already exists for provider '{provider}'. Use update_model instead.")
                return None # Or raise an error

        models_list.append(new_model)

        if self.save_models_for_provider(provider, models_list):
            logger.info(f"Model '{new_model.name}' added successfully to provider '{provider}'.")
            return new_model
        else:
            # save_models_for_provider logs its errors
            logger.error(f"Failed to save updated model list after adding '{new_model.name}' to provider '{provider}'.")
            return None

    def update_model(self, provider: str, model_name: str, update_data: Dict[str, Any]) -> Optional[Model]:
        """
        Updates an existing model for a specific provider.
        'name' and 'provider' fields in update_data are ignored to prevent changing them.

        Args:
            provider (str): The name of the provider.
            model_name (str): The name of the model to update.
            update_data (Dict[str, Any]): A dictionary containing the fields to update.

        Returns:
            Optional[Model]: The updated Model object if successful, None otherwise.
        """
        if not provider or not provider.strip() or not model_name or not model_name.strip():
            logger.error("Provider name and model name cannot be empty for update.")
            return None

        models_list = self.get_models_for_provider(provider)
        model_to_update_index = -1

        for i, model in enumerate(models_list):
            if model.name == model_name:
                model_to_update_index = i
                break
        
        if model_to_update_index == -1:
            logger.error(f"Model '{model_name}' not found for provider '{provider}'. Cannot update.")
            return None

        existing_model_data = models_list[model_to_update_index].model_dump()
        
        # Ensure name and provider are not changed by update_data
        update_data.pop('name', None)
        update_data.pop('provider', None)
        # Also, created_at should generally not be updated
        update_data.pop('created_at', None)


        # Apply updates
        for key, value in update_data.items():
            if hasattr(models_list[model_to_update_index], key):
                setattr(models_list[model_to_update_index], key, value)
            else:
                logger.warning(f"Attempted to update non-existent field '{key}' for model '{model_name}'. Ignoring.")
        
        # Re-validate the updated model by creating a new instance from its dict representation
        try:
            # Get the updated data, ensuring provider is correct.
            current_model_dict = models_list[model_to_update_index].model_dump()
            current_model_dict['provider'] = provider # Ensure provider consistency

            updated_model_instance = Model(**current_model_dict)
            models_list[model_to_update_index] = updated_model_instance # Replace with validated instance
        except ValueError as ve:
            logger.error(f"Invalid data after attempting to update model '{model_name}' for provider '{provider}': {ve}")
            return None # Or revert changes / reload original list

        # If is_default is being set to True, ensure no other model for this provider is default
        if updated_model_instance.is_default:
            for i, m in enumerate(models_list):
                if m.name != updated_model_instance.name and m.is_default:
                    logger.info(f"Model '{m.name}' is no longer the default for provider '{provider}' as '{updated_model_instance.name}' is now default.")
                    models_list[i].is_default = False


        if self.save_models_for_provider(provider, models_list):
            logger.info(f"Model '{model_name}' updated successfully for provider '{provider}'.")
            return models_list[model_to_update_index] # Return the updated model from the list
        else:
            logger.error(f"Failed to save updated model list for provider '{provider}' after updating '{model_name}'.")
            return None

    def remove_model(self, provider: str, model_name: str) -> bool:
        """
        Removes a model from the specified provider.

        Args:
            provider (str): The name of the provider.
            model_name (str): The name of the model to remove.

        Returns:
            bool: True if the model was removed successfully or was not found,
                  False if an error occurred during saving the updated list.
        """
        if not provider or not provider.strip() or not model_name or not model_name.strip():
            logger.error("Provider name and model name cannot be empty for removal.")
            return False

        models_list = self.get_models_for_provider(provider)
        
        initial_len = len(models_list)
        # Filter out the model to be removed
        models_list_after_removal = [model for model in models_list if model.name != model_name]

        if len(models_list_after_removal) == initial_len:
            logger.info(f"Model '{model_name}' not found for provider '{provider}'. Nothing to remove.")
            return True # Considered success as the state (model not in list) is achieved

        # If the removed model was the default, there's no automatic selection of a new default here.
        # This could be a future enhancement or handled by UI/calling code.

        if self.save_models_for_provider(provider, models_list_after_removal):
            logger.info(f"Model '{model_name}' removed successfully from provider '{provider}'.")
            return True
        else:
            logger.error(f"Failed to save updated model list for provider '{provider}' after removing '{model_name}'.")
            # Potentially, the list in memory is now out of sync with the (failed) save.
            # For robustness, one might reload or revert, but for now, just signal failure.
            return False

    def export_models(self, provider_name: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Exports models to a dictionary structure.

        Args:
            provider_name (Optional[str]): If specified, exports models only for this provider.
                                         If None, exports all models from all providers.

        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary where keys are provider names
                                             and values are lists of model data (dictionaries).
                                             Returns an empty dict if an error occurs or no models.
        """
        exported_data: Dict[str, List[Dict[str, Any]]] = {}

        if provider_name:
            if not provider_name.strip():
                logger.warning("Export requested for an empty provider name. Returning empty data.")
                return exported_data
            try:
                models_list = self.get_models_for_provider(provider_name)
                if models_list:
                    exported_data[provider_name] = [model.model_dump(mode='json') for model in models_list]
                else: # Provider exists but no models, or provider file doesn't exist
                    exported_data[provider_name] = []
                logger.info(f"Exported {len(exported_data.get(provider_name, []))} models for provider '{provider_name}'.")
            except Exception as e:
                logger.error(f"Error exporting models for provider '{provider_name}': {e}")
                # Optionally return partial data or an error structure
                return {} # Return empty on error for specific provider export
        else: # Export all providers
            if not self.storage_path.exists() or not self.storage_path.is_dir():
                logger.warning(f"Model storage directory {self.storage_path} not found. Cannot export all models.")
                return exported_data
            
            logger.debug(f"Exporting all models from: {self.storage_path}")
            for provider_file in self.storage_path.glob("*_models.json"):
                # Extract provider name from filename (e.g., "openai_models.json" -> "openai")
                # This is a bit simplistic and assumes a consistent naming from _get_provider_file_path
                # A more robust way might be to store provider names separately or parse them differently.
                # For now, we derive it, assuming it matches the key used in _get_provider_file_path's sanitized output.
                
                # Attempt to reverse the sanitization or use a known list of providers if available.
                # This part is tricky if sanitization is complex.
                # For now, we'll try to load and use the provider field from the first model if possible,
                # or use the filename stem as a fallback.
                
                current_provider_name_from_file = ""
                try:
                    models_in_file = load_json(provider_file) # This is List[Dict]
                    if isinstance(models_in_file, list) and models_in_file:
                        # Try to get provider from first model's data
                        if isinstance(models_in_file[0], dict) and 'provider' in models_in_file[0]:
                           current_provider_name_from_file = models_in_file[0]['provider']
                        
                    if not current_provider_name_from_file: # Fallback to filename stem
                        # Attempt to match filename stem to a "cleaned" version of original provider names
                        # This is complex. A simpler approach for now:
                        # Assume the filename stem (before '_models') is the sanitized provider name.
                        # We need a way to map this back or ensure consistency.
                        # For this implementation, we'll re-use get_models_for_provider which handles this.
                        # This means we need to guess the original provider name.
                        # This is not ideal. A better way would be to list providers by scanning directory names
                        # if each provider had its own directory, or by having a manifest file.
                        # Given current structure (flat files in 'models/'), we parse filename.
                        filename_stem = provider_file.stem
                        if filename_stem.endswith("_models"):
                            # This is the sanitized provider name used for the file.
                            # We need to call get_models_for_provider with an "original" provider name
                            # that would result in this sanitized name. This is hard to reverse perfectly.
                            # Let's assume for export all, we iterate and load each file,
                            # and the provider name is correctly set within each model object by get_models_for_provider.
                            
                            # A simpler loop for "export all":
                            # Iterate through all known provider files.
                            # For each file, extract a "best guess" provider name.
                            # Then load models using that provider name.
                            
                            # Let's refine: iterate files, extract potential provider name from filename
                            # then use get_models_for_provider with that name.
                            # The _get_provider_file_path creates "sanitized_models.json".
                            # So, provider_file.stem gives "sanitized_models". We need "sanitized".
                            
                            # This approach is flawed if sanitization is not perfectly reversible or unique.
                            # A better "export_all" would scan for all provider files,
                            # then for each file, load its content (which is a list of model dicts),
                            # and group them by the 'provider' field found within each model dict.
                            
                            # Revised approach for export_all:
                            temp_models_list = load_json(provider_file)
                            if isinstance(temp_models_list, list):
                                for model_data_dict in temp_models_list:
                                    if isinstance(model_data_dict, dict) and 'provider' in model_data_dict and 'name' in model_data_dict:
                                        prov = model_data_dict['provider']
                                        if prov not in exported_data:
                                            exported_data[prov] = []
                                        # To avoid duplicates if a model dict appears in multiple files (unlikely with current save logic)
                                        # We assume here that model_dump is the desired format for export.
                                        # No, we should export the Model objects' dicts.
                                        # So, we should load them as Model objects first.
                                        # This means calling self.get_models_for_provider for each distinct provider name found.

                                        # Let's stick to the simpler interpretation for now:
                                        # If we have openai_models.json, we assume provider is "OpenAI" (or whatever maps to "openai")
                                        # This is still tricky.
                                        
                                        # Safest for "export all" is to list all files,
                                        # load each, and then group by the 'provider' field within the Model objects.
                                        # This requires loading all models into memory first.
                                        pass # Will be handled by the refined loop below.


                except Exception as e_load_filename:
                    logger.error(f"Could not determine provider or load data from file {provider_file} for export all: {e_load_filename}")
                    continue
            
            # Refined loop for export_all:
            # 1. Get all provider files.
            # 2. For each file, assume its name (stem minus _models) is the "key" provider.
            # 3. Load models *for that key provider*. This ensures consistency with how they are stored/retrieved.
            
            # This is still not perfect if sanitization isn't unique.
            # The MOST robust "export_all" without prior knowledge of all provider names:
            all_provider_files = list(self.storage_path.glob("*_models.json"))
            all_loaded_models: Dict[str, List[Model]] = {} # provider_name -> List[Model]

            for p_file in all_provider_files:
                try:
                    models_data_list = load_json(p_file) # List[Dict]
                    if not isinstance(models_data_list, list):
                        logger.warning(f"Skipping non-list file during export all: {p_file}")
                        continue
                    for model_dict in models_data_list:
                        if isinstance(model_dict, dict) and 'provider' in model_dict and 'name' in model_dict:
                            actual_provider = model_dict['provider']
                            try:
                                model_obj = Model(**model_dict)
                                if actual_provider not in all_loaded_models:
                                    all_loaded_models[actual_provider] = []
                                # Avoid duplicates if somehow a model is listed twice in a file (should not happen with current save)
                                if not any(m.name == model_obj.name for m in all_loaded_models[actual_provider]):
                                     all_loaded_models[actual_provider].append(model_obj)
                            except ValueError as ve_model:
                                logger.warning(f"Skipping invalid model data in {p_file} during export all: {ve_model}")
                except JsonHandlerError as jhe:
                    logger.error(f"Error loading file {p_file} for export all: {jhe}")
                except Exception as e_gen:
                    logger.error(f"Unexpected error processing file {p_file} for export all: {e_gen}")
            
            for prov, model_list_objs in all_loaded_models.items():
                exported_data[prov] = [m.model_dump(mode='json') for m in model_list_objs]
            
            logger.info(f"Exported models for {len(exported_data)} providers.")

        return exported_data

    def import_models(self, file_path: Path, default_provider: Optional[str] = None, merge: bool = True) -> bool:
        """
        Imports models from a JSON file.
        The JSON file can be a dictionary (provider_name -> list of model_dicts)
        or a single list of model_dicts (requires default_provider or 'provider' in each dict).

        Args:
            file_path (Path): Path to the JSON file to import.
            default_provider (Optional[str]): If the root of JSON is a list of models,
                                              this provider name is used if 'provider'
                                              is missing in a model_dict.
            merge (bool): If True, merges imported models with existing ones.
                          If a model with the same name exists for a provider, it's updated.
                          If False, overwrites existing models for the providers found in the file.
                          (For list-based import, 'merge=False' effectively replaces all models
                           for the default_provider or providers found in data).

        Returns:
            bool: True if import was successful (at least one model processed), False otherwise.
        """
        if not file_path.exists() or not file_path.is_file():
            logger.error(f"Import file not found or is not a file: {file_path}")
            return False

        success_flag = False
        processed_providers = set()

        try:
            imported_data_structure = load_json(file_path)
        except JsonHandlerError as e:
            logger.error(f"Error loading import file {file_path}: {e}")
            return False

        models_to_process_by_provider: Dict[str, List[Dict[str, Any]]] = {}

        if isinstance(imported_data_structure, dict): # Format: {"provider1": [model_dict_1,...], ...}
            models_to_process_by_provider = imported_data_structure
        elif isinstance(imported_data_structure, list): # Format: [model_dict_1, model_dict_2, ...]
            for model_data_dict in imported_data_structure:
                if not isinstance(model_data_dict, dict):
                    logger.warning(f"Skipping non-dictionary item in import list from {file_path}: {model_data_dict}")
                    continue
                
                current_provider = model_data_dict.get('provider')
                if not current_provider:
                    if default_provider:
                        current_provider = default_provider
                        model_data_dict['provider'] = default_provider # Add provider to data
                    else:
                        logger.error(f"Model data in list from {file_path} is missing 'provider' field and no default_provider specified. Skipping: {model_data_dict.get('name', 'N/A')}")
                        continue
                
                if current_provider not in models_to_process_by_provider:
                    models_to_process_by_provider[current_provider] = []
                models_to_process_by_provider[current_provider].append(model_data_dict)
        else:
            logger.error(f"Import file {file_path} has an unsupported root structure (must be dict or list). Found: {type(imported_data_structure)}")
            return False

        # Process models for each provider
        for provider, model_data_list_to_import in models_to_process_by_provider.items():
            if not provider or not provider.strip():
                logger.warning(f"Skipping models with empty provider name from import file {file_path}.")
                continue

            processed_providers.add(provider)
            existing_models_list = self.get_models_for_provider(provider) if merge else []
            
            # For merge=True, create a dict for quick lookup of existing models by name
            existing_models_map = {model.name: model for model in existing_models_list} if merge else {}

            final_models_for_provider: List[Model] = []
            
            if not merge: # Overwrite mode for this provider
                logger.info(f"Importing models for provider '{provider}' in overwrite mode.")
                for model_data_to_add in model_data_list_to_import:
                    model_data_to_add['provider'] = provider # Ensure provider consistency
                    try:
                        new_model = Model(**model_data_to_add)
                        # Check for duplicates within the import list itself for this provider if overwriting
                        if not any(m.name == new_model.name for m in final_models_for_provider):
                            final_models_for_provider.append(new_model)
                        else:
                            logger.warning(f"Duplicate model name '{new_model.name}' found within import data for provider '{provider}'. Keeping first instance.")
                        success_flag = True
                    except ValueError as ve:
                        logger.error(f"Invalid model data during import for provider '{provider}', model '{model_data_to_add.get('name', 'N/A')}': {ve}")
                    except Exception as e_model_create:
                        logger.error(f"Error creating model instance during import for '{model_data_to_add.get('name', 'N/A')}': {e_model_create}")

            else: # Merge mode for this provider
                logger.info(f"Importing models for provider '{provider}' in merge mode.")
                # Add existing models that are not in the import list (or will not be updated)
                # This logic is complex if we want to truly merge.
                # A simpler merge: iterate import list. If exists, update. If not, add.
                # Then, add all existing models that were NOT in the import list.

                # Let's use the update/add logic:
                current_provider_models = {m.name: m for m in self.get_models_for_provider(provider)}

                for model_data_to_import in model_data_list_to_import:
                    model_data_to_import['provider'] = provider # Ensure provider
                    model_name_to_import = model_data_to_import.get('name')
                    if not model_name_to_import:
                        logger.warning(f"Skipping model data without a name for provider '{provider}' during merge.")
                        continue

                    if model_name_to_import in current_provider_models: # Update existing
                        # Pop name, provider, created_at from model_data_to_import before passing as update_data
                        update_dict = model_data_to_import.copy()
                        update_dict.pop('name', None)
                        update_dict.pop('provider', None)
                        update_dict.pop('created_at', None)
                        updated_model = self.update_model(provider, model_name_to_import, update_dict)
                        if updated_model:
                            success_flag = True
                        # update_model already saves the whole list, so we don't need to manage final_models_for_provider here
                        # This makes merge strategy complex if we want to batch saves.
                        # For now, update_model modifies and saves. This means get_models_for_provider will be fresh.
                    else: # Add new
                        added_model = self.add_model(provider, model_data_to_import)
                        if added_model:
                            success_flag = True
                # After all adds/updates for this provider in merge mode, the provider's file is already saved by add/update.
                # So, no separate save_models_for_provider call is needed here for merge=True.
                # This makes the logic a bit different from overwrite.
                # Let's adjust: for merge, we build the final list and save once.

                # REVISED MERGE LOGIC:
                # Build a map of new/updated models from the import file.
                imported_models_map: Dict[str, Model] = {}
                for model_data_dict_imp in model_data_list_to_import:
                    model_data_dict_imp['provider'] = provider
                    try:
                        model_obj = Model(**model_data_dict_imp)
                        if model_obj.name in imported_models_map:
                             logger.warning(f"Duplicate model name '{model_obj.name}' in import data for provider '{provider}'. Using first one encountered.")
                             continue
                        imported_models_map[model_obj.name] = model_obj
                        success_flag = True # At least one model parsed correctly
                    except ValueError as ve:
                        logger.error(f"Invalid model data during import for provider '{provider}', model '{model_data_dict_imp.get('name', 'N/A')}': {ve}")
                    except Exception as e_mc:
                        logger.error(f"Error creating model instance during import for '{model_data_dict_imp.get('name', 'N/A')}': {e_mc}")

                # Merge with existing: existing_models_map takes precedence for non-updated fields
                # For models in imported_models_map:
                #   If it exists in existing_models_map, update existing.
                #   If not, add it.
                # Then, add all from existing_models_map that were not in imported_models_map.
                
                merged_list: List[Model] = []
                final_names = set()

                # Process imported models (update or add)
                for name, new_model_obj in imported_models_map.items():
                    if name in existing_models_map: # Update
                        existing_model_obj = existing_models_map[name]
                        # Update fields of existing_model_obj from new_model_obj
                        # Pydantic's update_forward_refs or copy(update=...) is better
                        update_dict_for_existing = new_model_obj.model_dump(exclude_unset=True)
                        update_dict_for_existing.pop('created_at', None) # Don't overwrite created_at
                        update_dict_for_existing.pop('provider', None) # Provider should match
                        
                        # Recreate the model to ensure validation
                        try:
                            final_model_data = existing_model_obj.model_dump()
                            final_model_data.update(update_dict_for_existing)
                            final_model_data['provider'] = provider # ensure
                            updated_model = Model(**final_model_data)
                            merged_list.append(updated_model)
                            final_names.add(name)
                        except ValueError as ve_upd:
                            logger.error(f"Error re-validating model '{name}' during merge update: {ve_upd}. Keeping original.")
                            merged_list.append(existing_model_obj) # Keep original if update fails validation
                            final_names.add(name)
                    else: # Add new
                        merged_list.append(new_model_obj)
                        final_names.add(name)
                
                # Add existing models that were not part of the import
                for name, existing_model_obj in existing_models_map.items():
                    if name not in final_names:
                        merged_list.append(existing_model_obj)
                
                final_models_for_provider = merged_list


            # Save the final list for the provider (only if not in merge mode that saves per add/update)
            if not merge: # Overwrite mode, save the built list
                if not self.save_models_for_provider(provider, final_models_for_provider):
                    logger.error(f"Failed to save imported models for provider '{provider}' (overwrite mode).")
                    # success_flag might still be true if some models parsed, but save failed.
                    # This needs careful thought on overall success reporting.
                else:
                    logger.info(f"Successfully imported and overwrote {len(final_models_for_provider)} models for provider '{provider}'.")
            elif merge: # Merge mode, save the built merged_list
                 if not self.save_models_for_provider(provider, final_models_for_provider):
                    logger.error(f"Failed to save imported models for provider '{provider}' (merge mode).")
                 else:
                    logger.info(f"Successfully imported and merged {len(final_models_for_provider)} models for provider '{provider}'.")


        if not processed_providers and not success_flag: # No providers found in file or all failed early
            logger.warning(f"No valid model data found to import from {file_path}.")
            return False
            
        return success_flag # True if at least one model was successfully parsed/processed, even if some saves failed.

    def restore_defaults(self, provider_name: Optional[str] = None) -> bool:
        """
        Restores default models for a specific provider or all providers.
        The default models are sourced from ra_aid_start.data.default_models.DEFAULT_MODELS_DATA.
        This will overwrite existing models for the specified provider(s).

        Args:
            provider_name (Optional[str]): The name of the provider to restore defaults for.
                                         If None, restores defaults for all providers defined
                                         in DEFAULT_MODELS_DATA.

        Returns:
            bool: True if at least one provider's defaults were successfully restored, False otherwise.
        """
        overall_success = False
        providers_to_restore = []

        if provider_name:
            if not provider_name.strip():
                logger.error("Provider name cannot be empty when restoring defaults.")
                return False
            if provider_name in DEFAULT_MODELS_DATA:
                providers_to_restore.append(provider_name)
            else:
                logger.warning(f"Provider '{provider_name}' not found in default models data. Cannot restore.")
                return False
        else: # Restore all providers defined in DEFAULT_MODELS_DATA
            providers_to_restore.extend(DEFAULT_MODELS_DATA.keys())
            if not providers_to_restore:
                logger.info("No providers found in default models data to restore.")
                return False # Or True, as there's nothing to do. Let's say False as no action taken.

        logger.info(f"Attempting to restore default models for providers: {providers_to_restore}")

        for prov_name in providers_to_restore:
            default_model_data_list = DEFAULT_MODELS_DATA.get(prov_name)
            if default_model_data_list is None: # Should not happen if prov_name came from .keys()
                logger.warning(f"Default model data for provider '{prov_name}' unexpectedly missing. Skipping.")
                continue

            default_models_objects: List[Model] = []
            for model_data in default_model_data_list:
                try:
                    # Ensure provider field is consistent, though it should be in default_models.py
                    model_data['provider'] = prov_name
                    default_models_objects.append(Model(**model_data))
                except ValueError as ve:
                    logger.error(f"Invalid model data in default_models.py for provider '{prov_name}', model '{model_data.get('name', 'N/A')}': {ve}")
                except Exception as e_create:
                    logger.error(f"Unexpected error creating Model instance from default data for '{prov_name}', model '{model_data.get('name', 'N/A')}': {e_create}")
            
            if not default_models_objects and default_model_data_list: # All models for this provider failed parsing
                 logger.error(f"No valid models could be parsed from default data for provider '{prov_name}'. Skipping save.")
                 continue
            
            if self.save_models_for_provider(prov_name, default_models_objects):
                logger.info(f"Successfully restored {len(default_models_objects)} default models for provider '{prov_name}'.")
                overall_success = True
            else:
                # save_models_for_provider logs its own errors
                logger.error(f"Failed to save restored default models for provider '{prov_name}'.")
        
        if not overall_success and providers_to_restore:
            logger.warning(f"Failed to restore defaults for any of the targeted providers: {providers_to_restore}")
        elif overall_success:
            logger.info("Default model restoration process completed.")
            
        return overall_success

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    temp_mm_storage_dir = Path.home() / ".ra-aid-start-test-modelmanager"
    
    import shutil
    if temp_mm_storage_dir.exists():
        shutil.rmtree(temp_mm_storage_dir)

    mm = ModelManager(base_storage_path=temp_mm_storage_dir.parent) # Creates .ra-aid-start-test-modelmanager/models/

    print(f"\n--- ModelManager Storage Path: {mm.storage_path} ---")

    # Test with non-existent provider
    print("\n--- Testing get_models_for_provider (provider not found) ---")
    openai_models_empty = mm.get_models_for_provider("OpenAI")
    print(f"OpenAI models (should be empty): {openai_models_empty}")
    assert len(openai_models_empty) == 0

    # Create dummy data for OpenAI
    openai_models_data = [
        {"name": "gpt-4o", "provider": "OpenAI", "description": "Flagship model", "context_window": 128000},
        {"name": "gpt-3.5-turbo", "provider": "OpenAI", "is_default": True, "context_window": 16385},
        {"name": "text-embedding-ada-002", "provider": "OpenAI", "recommended_for": ["embedding"]}, # Mismatched provider will be corrected
    ]
    # Manually save for testing or use save_models_for_provider
    # provider_file = mm._get_provider_file_path("OpenAI")
    # ensure_dir_exists(provider_file)
    # save_json(provider_file, openai_models_data)
    
    print("\n--- Saving OpenAI models ---")
    save_openai_success = mm.save_models_for_provider("OpenAI", [Model(**data) for data in openai_models_data])
    print(f"Save OpenAI models success: {save_openai_success}")
    assert save_openai_success

    # Test get_models_for_provider for OpenAI
    print("\n--- Testing get_models_for_provider (OpenAI) ---")
    openai_models_loaded = mm.get_models_for_provider("OpenAI")
    print(f"Number of OpenAI models loaded: {len(openai_models_loaded)}")
    for m in openai_models_loaded:
        print(f"  - {m.name} (Provider: {m.provider}, Default: {m.is_default})")
    assert len(openai_models_loaded) == 3
    assert openai_models_loaded[0].name == "gpt-4o"
    assert openai_models_loaded[1].is_default is True
    assert openai_models_loaded[2].provider == "OpenAI" # Check if provider was corrected

    # Create dummy data for Anthropic
    anthropic_models_data = [
        Model(name="claude-3-opus-20240229", provider="Anthropic", context_window=200000),
        Model(name="claude-3-sonnet-20240229", provider="Anthropic", context_window=200000, is_default=True),
    ]
    print("\n--- Saving Anthropic models ---")
    save_anthropic_success = mm.save_models_for_provider("Anthropic", anthropic_models_data)
    print(f"Save Anthropic models success: {save_anthropic_success}")
    assert save_anthropic_success
    
    # Test get_models_for_provider for Anthropic
    print("\n--- Testing get_models_for_provider (Anthropic) ---")
    anthropic_models_loaded = mm.get_models_for_provider("Anthropic")
    print(f"Number of Anthropic models loaded: {len(anthropic_models_loaded)}")
    assert len(anthropic_models_loaded) == 2

    # Test with an invalid provider name for file path
    print("\n--- Testing with invalid provider name for file path ---")
    invalid_provider_models = mm.get_models_for_provider("Invalid/Provider Name")
    assert len(invalid_provider_models) == 0 # Should log error and return empty

    # Test with a provider file that is not a list
    print("\n--- Testing with provider file that is not a list ---")
    not_a_list_provider = "NotAListProvider"
    not_a_list_file = mm._get_provider_file_path(not_a_list_provider)
    ensure_dir_exists(not_a_list_file)
    save_json(not_a_list_file, {"error": "this is a dict, not a list"})
    not_a_list_models = mm.get_models_for_provider(not_a_list_provider)
    assert len(not_a_list_models) == 0 # Should log error and return empty

    # Test with a provider file that has invalid model data
    print("\n--- Testing with provider file containing invalid model data ---")
    invalid_data_provider = "InvalidDataProvider"
    invalid_data_file = mm._get_provider_file_path(invalid_data_provider)
    ensure_dir_exists(invalid_data_file)
    save_json(invalid_data_file, [{"name": "good_model", "provider": invalid_data_provider}, {"provider": invalid_data_provider}]) # Second model missing 'name'
    invalid_data_models = mm.get_models_for_provider(invalid_data_provider)
    print(f"Number of models from invalid data file: {len(invalid_data_models)}")
    assert len(invalid_data_models) == 1 # Only the valid model should be loaded

    # Clean up
    if temp_mm_storage_dir.exists():
        shutil.rmtree(temp_mm_storage_dir)
        logger.info(f"\nCleaned up temporary test directory: {temp_mm_storage_dir}")

    print("\nModelManager example usage finished.")