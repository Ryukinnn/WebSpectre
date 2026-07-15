"""
WebSpectre Framework - Configuration Manager
Developer: Ryukinnn

Modul ini bertanggung jawab untuk memuat dan mengelola konfigurasi sistem.
Berinteraksi dengan file YAML di direktori config/ untuk menentukan 
perilaku framework, tema, bahasa, dan parameter performa.
"""

import yaml
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """Mengelola pembacaan dan validasi konfigurasi aplikasi."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config_data: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """Memuat file konfigurasi YAML."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"File konfigurasi tidak ditemukan di {self.config_path}. "
                "Jalankan 'python3 setup.py' untuk membuat konfigurasi default."
            )
            
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                self.config_data = yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Format file konfigurasi tidak valid: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Mengambil nilai dari konfigurasi menggunakan dot notation (misal: 'app.name').
        Mengembalikan nilai default jika kunci tidak ditemukan.
        """
        keys = key.split('.')
        value = self.config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    @property
    def language(self) -> str:
        """Mengembalikan bahasa yang dipilih, default 'id' (Indonesia)."""
        return self.get("app.language", "id")

    @property
    def async_mode(self) -> bool:
        """Menentukan apakah mode asinkron diaktifkan untuk performa maksimal."""
        return self.get("performance.async_mode", True)

    @property
    def max_threads(self) -> int:
        """Mengembalikan jumlah maksimal thread yang diizinkan."""
        return self.get("performance.max_threads", 10)
