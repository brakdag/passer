from typing import Any, Dict, List, Optional, Type, TypeVar, Union

T = TypeVar("T", bound="BaseValidator")

class ValidationError(Exception):
    """Excepción personalizada para errores de validación de argumentos."""
    pass

class BaseValidator:
    """Clase base ligera para validación de esquemas de herramientas."""
    
    @classmethod
    def validate(cls: Type[T], data: Dict[str, Any]) -> T:
        """Valida los datos recibidos contra los tipos definidos en la clase."""
        instance = cls(**data)
        return instance

    def __init__(self, **data):
        for key, value in data.items():
            if not hasattr(self, key):
                raise ValidationError(f"Campo inesperado: {key}")
            setattr(self, key, value)
        
        # Validar campos requeridos (aquellos sin valor por defecto)
        for field in self.__annotations__:
            if not hasattr(self, field) and not field.startswith("Optional"):
                raise ValidationError(f"Campo requerido faltante: {field}")
