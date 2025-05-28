"""
Gerenciador de Backup para RA AID Start.

Este módulo define a classe BackupManager, responsável por criar,
listar e restaurar backups dos dados da aplicação, especificamente
os diretórios de presets e modelos.
"""
import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from ra_aid_start.utils.file_handler import ensure_dir_exists # Supondo que temos isso

# Nomes padrão para diretórios, idealmente importados de onde são definidos
# Por enquanto, vamos defini-los aqui ou assumir que são passados.
# Para consistência, deveriam vir de PresetManager e ModelManager ou de um config central.
PRESETS_DIR_NAME = "presets"
MODELS_DIR_NAME = "models"
BACKUPS_DIR_NAME = "backups"

logger = logging.getLogger(__name__)

class BackupManagerError(Exception):
    """Custom exception for BackupManager errors."""
    pass

class BackupManager:
    """Manages backups of application configurations (presets and models)."""

    def __init__(self, base_storage_path: Path):
        """
        Initializes the BackupManager.

        Args:
            base_storage_path (Path): The base directory for ra-aid-start data
                                      (e.g., Path.home() / ".ra-aid-start").
                                      Backups will be stored in a 'backups' subdirectory
                                      within this base path.
        """
        if not base_storage_path:
            raise ValueError("base_storage_path cannot be None or empty.")

        self.base_storage_path = base_storage_path
        self.presets_path = self.base_storage_path / PRESETS_DIR_NAME
        self.models_path = self.base_storage_path / MODELS_DIR_NAME
        self.backups_root_path = self.base_storage_path / BACKUPS_DIR_NAME

        try:
            ensure_dir_exists(self.backups_root_path / "dummy_for_creation.tmp")
            logger.info(f"BackupManager initialized. Backups will be stored in: {self.backups_root_path}")
        except Exception as e:
            logger.error(f"Failed to ensure or create backup root directory {self.backups_root_path}: {e}")
            raise BackupManagerError(f"Could not initialize backup storage at {self.backups_root_path}: {e}") from e

    def create_backup(self, backup_name_prefix: str = "auto") -> Optional[str]:
        """
        Creates a new backup of the current presets and models.

        The backup will be stored in a new subdirectory within the backups_root_path,
        named with the prefix and a timestamp (e.g., "auto_YYYYMMDD_HHMMSS_ffffff").

        Args:
            backup_name_prefix (str): A prefix for the backup directory name.

        Returns:
            Optional[str]: The name of the created backup directory (timestamp part) if successful,
                           None otherwise.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup_dir_name = f"{backup_name_prefix}_{timestamp}"
        current_backup_path = self.backups_root_path / backup_dir_name

        try:
            ensure_dir_exists(current_backup_path / "dummy_for_creation.tmp")
            logger.info(f"Creating backup in: {current_backup_path}")

            # Backup presets
            backup_presets_target_path = current_backup_path / PRESETS_DIR_NAME
            if self.presets_path.exists() and self.presets_path.is_dir():
                shutil.copytree(self.presets_path, backup_presets_target_path, dirs_exist_ok=True)
                logger.debug(f"Presets backed up to {backup_presets_target_path}")
            else:
                logger.info(f"Presets directory {self.presets_path} does not exist. Skipping presets backup.")
                # Create an empty dir in backup to signify it was considered
                ensure_dir_exists(backup_presets_target_path / "dummy_for_creation.tmp")


            # Backup models
            backup_models_target_path = current_backup_path / MODELS_DIR_NAME
            if self.models_path.exists() and self.models_path.is_dir():
                shutil.copytree(self.models_path, backup_models_target_path, dirs_exist_ok=True)
                logger.debug(f"Models backed up to {backup_models_target_path}")
            else:
                logger.info(f"Models directory {self.models_path} does not exist. Skipping models backup.")
                ensure_dir_exists(backup_models_target_path / "dummy_for_creation.tmp")

            logger.info(f"Backup '{backup_dir_name}' created successfully.")
            return backup_dir_name
        except Exception as e:
            logger.error(f"Failed to create backup '{backup_dir_name}': {e}")
            # Attempt to clean up partially created backup directory
            if current_backup_path.exists():
                try:
                    shutil.rmtree(current_backup_path)
                    logger.info(f"Cleaned up partially created backup directory: {current_backup_path}")
                except Exception as e_clean:
                    logger.error(f"Failed to clean up partial backup directory {current_backup_path}: {e_clean}")
            return None

    def list_backups(self) -> List[str]:
        """
        Lists all available backup directory names.

        Returns:
            List[str]: A list of backup names (directory names within the backups_root_path),
                       sorted by name (typically chronological).
        """
        if not self.backups_root_path.exists() or not self.backups_root_path.is_dir():
            logger.info("Backups directory does not exist. No backups to list.")
            return []

        backups = []
        for item in self.backups_root_path.iterdir():
            if item.is_dir():
                # Basic check: does it contain 'presets' and 'models' subdirs?
                # This is a simple heuristic. A more robust check might involve metadata.
                if (item / PRESETS_DIR_NAME).exists() and (item / MODELS_DIR_NAME).exists():
                    backups.append(item.name)
                else:
                    logger.debug(f"Skipping directory {item.name} as it does not appear to be a valid backup structure.")
        
        backups.sort() # Sorts alphabetically, which should be chronological due to timestamp
        logger.info(f"Found {len(backups)} backups: {backups}")
        return backups

    def restore_backup(self, backup_name: str, create_pre_restore_backup: bool = True) -> bool:
        """
        Restores presets and models from a specified backup.

        Args:
            backup_name (str): The name of the backup directory to restore from.
            create_pre_restore_backup (bool): If True, creates a backup of the current state
                                             before restoring.

        Returns:
            bool: True if restoration was successful, False otherwise.
        """
        backup_to_restore_path = self.backups_root_path / backup_name
        if not backup_name or not backup_name.strip():
            logger.error("Backup name cannot be empty for restoration.")
            return False

        if not backup_to_restore_path.exists() or not backup_to_restore_path.is_dir():
            logger.error(f"Backup '{backup_name}' not found at {backup_to_restore_path}.")
            return False

        # Check for source presets and models in the backup
        source_presets = backup_to_restore_path / PRESETS_DIR_NAME
        source_models = backup_to_restore_path / MODELS_DIR_NAME

        if not source_presets.exists() or not source_presets.is_dir():
            logger.error(f"Presets directory not found in backup '{backup_name}'. Cannot restore presets.")
            # Decide if partial restore is allowed or if this is a fatal error for the whole op
            # For now, let's assume it should exist, even if empty.
            return False
        if not source_models.exists() or not source_models.is_dir():
            logger.error(f"Models directory not found in backup '{backup_name}'. Cannot restore models.")
            return False

        if create_pre_restore_backup:
            pre_restore_backup_name = self.create_backup(backup_name_prefix="pre_restore")
            if not pre_restore_backup_name:
                logger.error("Failed to create a pre-restore backup. Aborting restoration to prevent data loss.")
                return False
            logger.info(f"Pre-restore backup created: {pre_restore_backup_name}")

        try:
            logger.info(f"Starting restoration from backup '{backup_name}'.")

            # Clear current presets and models directories
            if self.presets_path.exists():
                shutil.rmtree(self.presets_path)
                logger.debug(f"Removed existing presets directory: {self.presets_path}")
            ensure_dir_exists(self.presets_path / "dummy.tmp") # Recreate after deleting

            if self.models_path.exists():
                shutil.rmtree(self.models_path)
                logger.debug(f"Removed existing models directory: {self.models_path}")
            ensure_dir_exists(self.models_path / "dummy.tmp") # Recreate

            # Copy from backup
            logger.debug(f"Copying presets from {source_presets} to {self.presets_path}")
            shutil.copytree(source_presets, self.presets_path, dirs_exist_ok=True)
            
            logger.debug(f"Copying models from {source_models} to {self.models_path}")
            shutil.copytree(source_models, self.models_path, dirs_exist_ok=True)

            logger.info(f"Successfully restored configuration from backup '{backup_name}'.")
            return True

        except Exception as e:
            logger.error(f"Failed to restore from backup '{backup_name}': {e}")
            # Potentially attempt to restore the pre_restore_backup if one was made
            # This would be more complex rollback logic.
            return False

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a temporary directory for testing
    temp_base_dir = Path.home() / ".ra-aid-start-test-backupmanager"
    if temp_base_dir.exists():
        shutil.rmtree(temp_base_dir)
    ensure_dir_exists(temp_base_dir / "dummy.tmp")

    bm = BackupManager(base_storage_path=temp_base_dir)

    # Create some dummy preset and model files to backup
    ensure_dir_exists(bm.presets_path / "dummy.tmp")
    ensure_dir_exists(bm.models_path / "dummy.tmp")
    
    with open(bm.presets_path / "test_preset1.json", "w") as f:
        f.write('{"name": "Test Preset 1"}')
    with open(bm.models_path / "openai_models.json", "w") as f:
        f.write('[{"name": "gpt-4o-test"}]')
    
    print(f"Presets path: {bm.presets_path}")
    print(f"Models path: {bm.models_path}")
    print(f"Backups root path: {bm.backups_root_path}")

    # Test create_backup
    print("\n--- Testing create_backup ---")
    backup1_name = bm.create_backup(backup_name_prefix="testrun")
    if backup1_name:
        print(f"Backup 1 created: {backup1_name}")
        assert (bm.backups_root_path / backup1_name).exists()
        assert (bm.backups_root_path / backup1_name / PRESETS_DIR_NAME / "test_preset1.json").exists()
        assert (bm.backups_root_path / backup1_name / MODELS_DIR_NAME / "openai_models.json").exists()
    else:
        print("Failed to create backup 1.")

    # Modify original data
    with open(bm.presets_path / "test_preset2_new.json", "w") as f:
        f.write('{"name": "Test Preset 2 New"}')
    if (bm.presets_path / "test_preset1.json").exists():
        (bm.presets_path / "test_preset1.json").unlink() # Delete old preset

    backup2_name = bm.create_backup(backup_name_prefix="testrun")
    if backup2_name:
        print(f"Backup 2 created: {backup2_name}")
        assert not (bm.backups_root_path / backup2_name / PRESETS_DIR_NAME / "test_preset1.json").exists()
        assert (bm.backups_root_path / backup2_name / PRESETS_DIR_NAME / "test_preset2_new.json").exists()

    # Test list_backups
    print("\n--- Testing list_backups ---")
    backups_list = bm.list_backups()
    print(f"Available backups: {backups_list}")
    assert len(backups_list) >= 2 # Could be more if run multiple times
    assert backup1_name in backups_list
    assert backup2_name in backups_list

    # Test restore_backup
    print("\n--- Testing restore_backup (restoring backup1) ---")
    if backup1_name:
        # Before restore: preset2_new.json should exist, preset1.json should not
        assert (bm.presets_path / "test_preset2_new.json").exists()
        assert not (bm.presets_path / "test_preset1.json").exists()
        
        restore_success = bm.restore_backup(backup1_name, create_pre_restore_backup=True)
        print(f"Restore success: {restore_success}")
        if restore_success:
            # After restore: preset1.json should exist, preset2_new.json should not
            assert (bm.presets_path / "test_preset1.json").exists()
            assert not (bm.presets_path / "test_preset2_new.json").exists()
            print("Files correctly restored from backup1.")
            
            # Check if pre-restore backup was created
            pre_restore_backups = [b for b in bm.list_backups() if b.startswith("pre_restore")]
            print(f"Pre-restore backups found: {pre_restore_backups}")
            assert len(pre_restore_backups) > 0


    # Test restoring a non-existent backup
    print("\n--- Testing restore_backup (non-existent) ---")
    restore_fail = bm.restore_backup("non_existent_backup_123")
    print(f"Restore non-existent success (should be False): {restore_fail}")
    assert not restore_fail

    # Clean up
    print("\n--- Cleaning up ---")
    if temp_base_dir.exists():
        shutil.rmtree(temp_base_dir)
        logger.info(f"Cleaned up temporary test directory: {temp_base_dir}")

    print("\nBackupManager example usage finished.")