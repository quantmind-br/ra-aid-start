"""
Utilitários de Manipulação de Arquivos.

Este módulo fornece funções auxiliares para operações comuns de sistema de arquivos,
como garantir a existência de diretórios.
"""
import os
from pathlib import Path
import logging

# Configurar um logger básico para este módulo, se necessário
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO) # Exemplo, ajuste conforme necessário

def ensure_dir_exists(file_path: Path | str) -> None:
    """
    Ensures that the directory for the given file_path exists.
    If it doesn't exist, it creates the directory.

    Args:
        file_path (Path | str): The path to the file (can be a Path object or a string).
    """
    path_obj = Path(file_path)
    dir_path = path_obj.parent
    try:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            # logger.info(f"Directory created: {dir_path}")
    except OSError as e:
        # logger.error(f"Error creating directory {dir_path}: {e}")
        # Re-raise a mais específica ou uma customizada se necessário
        raise # Ou raise CustomFileError(f"Could not create directory {dir_path}: {e}") from e

if __name__ == '__main__':
    # Exemplos de uso
    test_file_1 = Path("test_data/subdir1/file1.txt")
    test_file_2 = "test_data/subdir2/another/file2.json"
    
    print(f"Ensuring directory for: {test_file_1}")
    ensure_dir_exists(test_file_1)
    
    print(f"Ensuring directory for: {test_file_2}")
    ensure_dir_exists(test_file_2)
    
    # Para verificar, você pode listar os diretórios ou tentar criar arquivos neles
    # Exemplo:
    if test_file_1.parent.exists():
        print(f"Directory {test_file_1.parent} exists.")
        with open(test_file_1, "w") as f:
            f.write("Test content for file1.")
        print(f"File {test_file_1} created for testing.")
    
    if Path(test_file_2).parent.exists():
        print(f"Directory {Path(test_file_2).parent} exists.")
        # Clean up test directories (opcional)
        import shutil
        if Path("test_data").exists():
            shutil.rmtree("test_data")
            print("Cleaned up test_data directory.")

    print("File handler tests completed.")