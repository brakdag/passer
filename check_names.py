from paser.tools.tools_functions import buscar_en_internet
import json

# Lista de nombres candidatos de 4-5 letras para validar si ya existen en PyPI/GitHub
nombres_candidatos = [
    "passr",
    "psrra",
    "pserr",
    "sparr",
    "gornn",
    "actua",
    "reacr",
    "react",
    "fcall",
    "vuelo"
]

resultados = {}
for nombre in nombres_candidatos:
    # Verificamos si parece haber proyectos con ese nombre.
    # Nota: buscar_en_internet es una herramienta de buscador, 
    # no verifica el registro de PyPI directamente, pero nos da una idea.
    resultados[nombre] = buscar_en_internet(f"pypi {nombre} python package")

print(json.dumps(resultados, indent=2))
