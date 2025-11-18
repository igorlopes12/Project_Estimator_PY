import json
import os
import logging
from pathlib import Path
from threading import Lock

logger = logging.getLogger(__name__)
lock = Lock()


class ProjectManager:
    """Gerenciador de projetos com suporte a armazenamento local e em rede."""

    def __init__(self, path):
        """
        Inicializa o gerenciador com o caminho do arquivo JSON.

        Args:
            path: Caminho para o arquivo JSON (local ou rede)
        """
        self.path = Path(path)
        self._ensure_directory()
        self._ensure_file_exists()

    def _ensure_directory(self):
        """Garante que o diretório pai existe."""
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Erro ao criar diretório {self.path.parent}: {e}")
            raise

    def _ensure_file_exists(self):
        """Garante que o arquivo JSON existe, criando vazio se necessário."""
        try:
            if not self.path.exists():
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False)
                logger.info(f"Arquivo criado: {self.path}")
        except Exception as e:
            logger.error(f"Erro ao criar arquivo {self.path}: {e}")
            raise

    def load_projects(self):
        """
        Carrega os projetos do arquivo JSON.

        Returns:
            Lista com os projetos
        """
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                projects = json.load(f)
                logger.debug(f"Projetos carregados de {self.path}: {len(projects)} itens")
                return projects
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON de {self.path}: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro ao carregar projetos de {self.path}: {e}")
            return []

    def save_projects(self, projects):
        """
        Salva os projetos no arquivo JSON.

        Args:
            projects: Lista com os projetos a salvar
        """
        with lock:
            try:
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(projects, f, indent=4, ensure_ascii=False)
                logger.debug(f"Projetos salvos em {self.path}: {len(projects)} itens")
            except Exception as e:
                logger.error(f"Erro ao salvar projetos em {self.path}: {e}")
                raise
