from functools import wraps
from pydantic import ValidationError
import inspect

def validate_args(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Obtener los nombres de los argumentos de la función original
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            try:
                # Validar usando el esquema de Pydantic
                validated_data = schema(**bound_args.arguments)
                return func(**validated_data.dict())
            except ValidationError as e:
                return f"Error de validación: {str(e)}"
        return wrapper
    return decorator
