from datetime import datetime
from typing import Dict, Any, TypeVar, Type
from pydantic import BaseModel, Field

T = TypeVar('T', bound='Preset')

class Preset(BaseModel):
    """
    Representa um preset de configuração para a ferramenta RA AID.

    Um preset armazena um conjunto de configurações, incluindo o modo de operação
    e flags específicas, que podem ser salvas e reutilizadas.

    Atributos:
        name (str): O nome único do preset.
        description (str): Uma descrição opcional do preset.
        operation_mode (str): O modo de operação principal (ex: "chat", "file_diff").
        flags (Dict[str, Any]): Um dicionário de flags e seus valores para o comando.
        created_at (datetime): Timestamp de quando o preset foi criado.
        updated_at (datetime): Timestamp da última atualização do preset.
        command (str): A string de comando completa gerada a partir do preset.
    """
    name: str
    description: str = ""
    operation_mode: str
    flags: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    command: str = "" # Será gerado pelo CommandBuilder

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Preset object to a dictionary."""
        return self.model_dump(mode='json')

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Creates a Preset object from a dictionary."""
        return cls(**data)

    def validate_preset(self) -> bool: # Renomeado de validate() para evitar conflito com pydantic
        """
        Validates the preset data.
        Placeholder for now.
        """
        # TODO: Implementar lógica de validação detalhada conforme PLAN.MD
        if not self.name:
            # logger.error("Preset name cannot be empty.") # Exemplo de logging
            return False
        if not self.operation_mode:
            # logger.error("Operation mode must be specified.")
            return False
        # Adicionar mais regras de validação aqui
        return True

    def update_timestamp(self):
        """Updates the updated_at timestamp to the current time."""
        self.updated_at = datetime.now()

# Exemplo de uso (pode ser removido ou movido para testes)
if __name__ == '__main__':
    preset_data_ok = {
        "name": "Test Preset",
        "description": "A preset for testing purposes.",
        "operation_mode": "chat",
        "flags": {"--model": "gpt-4o", "--temperature": "0.7"},
        "command": "ra-aid --model gpt-4o --temperature 0.7"
    }
    preset1 = Preset.from_dict(preset_data_ok)
    print("Preset 1 (from_dict):", preset1)
    print("Preset 1 (to_dict):", preset1.to_dict())
    print("Preset 1 validation:", preset1.validate_preset())

    preset_data_minimal = {
        "name": "Minimal Preset",
        "operation_mode": "message"
    }
    preset2 = Preset(**preset_data_minimal)
    print("\nPreset 2 (direct instantiation):", preset2)
    preset2.update_timestamp()
    print("Preset 2 (after update_timestamp):", preset2)
    print("Preset 2 validation:", preset2.validate_preset())

    preset_data_invalid_name = {
        "name": "", # Nome inválido
        "operation_mode": "file"
    }
    try:
        preset3 = Preset(**preset_data_invalid_name) # Pydantic validará campos obrigatórios
        print("\nPreset 3 (invalid):", preset3) # Não deve chegar aqui se name for obrigatório e vazio
        print("Preset 3 validation:", preset3.validate_preset())
    except Exception as e:
        print(f"\nError creating Preset 3: {e}")

    # Testando default factory para created_at e updated_at
    preset4 = Preset(name="Timestamp Test", operation_mode="chat")
    print(f"\nPreset 4 created_at: {preset4.created_at}")
    print(f"Preset 4 updated_at: {preset4.updated_at}")