from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Model(BaseModel):
    """
    Representa um modelo de linguagem (LLM) com seus metadados.

    Atributos:
        name (str): O nome identificador do modelo (ex: "gpt-4o").
        provider (str): O provedor do modelo (ex: "OpenAI", "Anthropic").
        description (str): Uma breve descrição do modelo.
        recommended_for (List[str]): Lista de casos de uso ou tarefas recomendadas.
        is_default (bool): Indica se este é o modelo padrão para seu provedor.
        supports_temperature (bool): Indica se o modelo suporta ajuste de temperatura.
        context_window (Optional[int]): O tamanho da janela de contexto do modelo em tokens.
        created_by (str): Indica quem criou o registro do modelo ("system" ou "user").
        created_at (datetime): Timestamp de quando o registro do modelo foi criado.
    """
    name: str
    provider: str
    description: str = ""
    recommended_for: List[str] = Field(default_factory=list)
    is_default: bool = False
    supports_temperature: bool = True # Assumindo True por padrão, pode ser ajustado
    context_window: Optional[int] = None
    created_by: str = "system" # Pode ser 'user' ou 'system'
    created_at: datetime = Field(default_factory=datetime.now)
    # updated_at: datetime = Field(default_factory=datetime.now) # Adicionado para consistência, se necessário

    # Métodos to_dict e from_dict podem ser úteis aqui também, similar ao Preset
    # Mas como Pydantic já lida bem com isso, podem ser omitidos se não houver lógica customizada.

    def __str__(self) -> str:
        return f"{self.provider} - {self.name}"

# Exemplo de uso (pode ser removido ou movido para testes)
if __name__ == '__main__':
    model1_data = {
        "name": "gpt-4o",
        "provider": "OpenAI",
        "description": "Latest OpenAI model with improved vision and speed.",
        "recommended_for": ["general_chat", "coding_assistance", "content_generation"],
        "is_default": True,
        "supports_temperature": True,
        "context_window": 128000,
        "created_by": "system"
    }
    model1 = Model(**model1_data)
    print("Model 1:", model1)
    print("Model 1 JSON:", model1.model_dump_json(indent=2))

    model2_data = {
        "name": "claude-3-opus-20240229",
        "provider": "Anthropic",
        "description": "Most powerful Claude 3 model.",
        "recommended_for": ["complex_reasoning", "research", "long_form_content"],
        "context_window": 200000
    }
    model2 = Model(**model2_data)
    print("\nModel 2:", model2)

    model3_data = {
        "name": "Gemini 1.5 Pro",
        "provider": "Google",
        "recommended_for": ["multimodal", "large_context"],
        "supports_temperature": False # Exemplo
    }
    model3 = Model(**model3_data)
    print("\nModel 3:", model3)
    print(f"Model 3 created_at: {model3.created_at}")