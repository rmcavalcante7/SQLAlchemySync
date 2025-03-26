import subprocess
import toml

# Obtém a versão do Python corretamente
python_version = subprocess.run(
    ["python", "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
    capture_output=True, text=True
).stdout.strip()

# Obtém a lista de bibliotecas instaladas
dependencies = subprocess.run(["pip", "freeze"], capture_output=True, text=True).stdout.splitlines()

# # Converte para o formato necessário (sem os hashes de versão fixa)
# dependencies = [pkg for pkg in dependencies]

# Estrutura do pyproject.toml
pyproject_data = {
    
    "build-system": {
        "requires": ["setuptools", "wheel"],
        "build-backend": "setuptools.build_meta",
    },
    "project": {
        "name": "meu_projeto",
        "version": "0.1.0",
        "requires-python": f"=={python_version}",
        "dependencies": dependencies,
    },
}

# Escreve o arquivo pyproject.toml
with open("pyproject.toml", "w", encoding="utf-8") as f:
    toml.dump(pyproject_data, f)

print("Arquivo pyproject.toml gerado com sucesso!")
