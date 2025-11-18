# core/config.py
from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Caminho de rede (ou None para usar diretório local)
NETWORK_PATH = r"\\Nadc1rpaorcfs01\DEV\ProjectEstimatorApp"

# Define o diretório de dados
if NETWORK_PATH:
    DATA_DIR = Path(NETWORK_PATH)
else:
    DATA_DIR = PROJECT_ROOT / "data"

# Garante que o diretório existe
try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(f"Aviso: Não foi possível criar diretório {DATA_DIR}: {e}")
    # Fallback para diretório local se houver erro
    DATA_DIR = PROJECT_ROOT / "data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

# Caminhos dos arquivos JSON
TEMPLATES_PATH = DATA_DIR / "templates.json"
PROJECTS_PATH = DATA_DIR / "projects.json"
