"""
Utilitários de Manipulação de JSON.

Este módulo fornece funções para carregar dados de arquivos JSON
e salvar dados em arquivos JSON, incluindo tratamento de erros comuns
e garantia de existência de diretórios.
"""
import json
from pathlib import Path
from typing import Any, Dict, List
import logging

from .file_handler import ensure_dir_exists # Importação relativa

# Configurar um logger básico para este módulo, se necessário
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO) # Exemplo, ajuste conforme necessário

class JsonHandlerError(Exception):
    """Custom exception for JSON handling errors."""
    pass

def load_json(file_path: Path | str) -> Dict[str, Any] | List[Any]:
    """
    Loads JSON data from a file.

    Args:
        file_path (Path | str): The path to the JSON file.

    Returns:
        Dict[str, Any] | List[Any]: The loaded JSON data (can be a dict or a list).

    Raises:
        JsonHandlerError: If the file is not found, is not a valid JSON, or other OS errors occur.
    """
    path_obj = Path(file_path)
    if not path_obj.exists():
        # logger.error(f"JSON file not found: {path_obj}")
        raise JsonHandlerError(f"JSON file not found: {path_obj}")
    if not path_obj.is_file():
        # logger.error(f"Path is not a file: {path_obj}")
        raise JsonHandlerError(f"Path is not a file: {path_obj}")

    try:
        with open(path_obj, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # logger.info(f"Successfully loaded JSON from: {path_obj}")
        return data
    except json.JSONDecodeError as e:
        # logger.error(f"Error decoding JSON from {path_obj}: {e}")
        raise JsonHandlerError(f"Error decoding JSON from {path_obj}: {e}") from e
    except OSError as e:
        # logger.error(f"OS error reading JSON file {path_obj}: {e}")
        raise JsonHandlerError(f"OS error reading JSON file {path_obj}: {e}") from e

def save_json(file_path: Path | str, data: Any, indent: int = 4) -> None:
    """
    Saves data to a JSON file.

    Args:
        file_path (Path | str): The path to the JSON file.
        data (Any): The data to save (must be JSON serializable).
        indent (int): The indentation level for pretty-printing. Defaults to 4.

    Raises:
        JsonHandlerError: If there's an error during serialization or writing to the file.
    """
    path_obj = Path(file_path)
    ensure_dir_exists(path_obj) # Garante que o diretório existe

    try:
        with open(path_obj, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        # logger.info(f"Successfully saved JSON to: {path_obj}")
    except TypeError as e:
        # logger.error(f"Data is not JSON serializable for {path_obj}: {e}")
        raise JsonHandlerError(f"Data is not JSON serializable for {path_obj}: {e}") from e
    except OSError as e:
        # logger.error(f"OS error writing JSON file {path_obj}: {e}")
        raise JsonHandlerError(f"OS error writing JSON file {path_obj}: {e}") from e

if __name__ == '__main__':
    # Exemplos de uso
    test_dir = Path("test_data_json_handler")
    test_file_dict = test_dir / "test_dict.json"
    test_file_list = test_dir / "test_list.json"
    test_file_nonexistent = test_dir / "nonexistent.json"

    sample_dict_data = {"name": "Test User", "age": 30, "city": "Testville", "active": True}
    sample_list_data = [{"id": 1, "item": "apple"}, {"id": 2, "item": "banana"}]

    # Test save_json
    try:
        print(f"\nSaving dict data to: {test_file_dict}")
        save_json(test_file_dict, sample_dict_data)
        if test_file_dict.exists():
            print(f"File {test_file_dict} created successfully.")

        print(f"\nSaving list data to: {test_file_list}")
        save_json(test_file_list, sample_list_data)
        if test_file_list.exists():
            print(f"File {test_file_list} created successfully.")
    except JsonHandlerError as e:
        print(f"Error during save_json tests: {e}")

    # Test load_json
    try:
        print(f"\nLoading dict data from: {test_file_dict}")
        loaded_dict = load_json(test_file_dict)
        print("Loaded dict data:", loaded_dict)
        assert loaded_dict == sample_dict_data

        print(f"\nLoading list data from: {test_file_list}")
        loaded_list = load_json(test_file_list)
        print("Loaded list data:", loaded_list)
        assert loaded_list == sample_list_data
    except JsonHandlerError as e:
        print(f"Error during load_json tests: {e}")

    # Test load_json for non-existent file
    try:
        print(f"\nAttempting to load non-existent file: {test_file_nonexistent}")
        load_json(test_file_nonexistent)
    except JsonHandlerError as e:
        print(f"Correctly caught error for non-existent file: {e}")

    # Test load_json for invalid JSON
    invalid_json_file = test_dir / "invalid.json"
    try:
        ensure_dir_exists(invalid_json_file)
        with open(invalid_json_file, "w") as f:
            f.write("{'name': 'test', 'age': 30,}") # Invalid JSON (trailing comma, single quotes)
        print(f"\nAttempting to load invalid JSON from: {invalid_json_file}")
        load_json(invalid_json_file)
    except JsonHandlerError as e:
        print(f"Correctly caught error for invalid JSON: {e}")
    
    # Clean up test directory (opcional)
    import shutil
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print(f"\nCleaned up {test_dir} directory.")
    
    print("\nJSON handler tests completed.")