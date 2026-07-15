"""
WebSpectre Framework - Plugin Loader
Developer: Ryukinnn

Modul ini bertanggung jawab untuk memindai, memvalidasi, dan memuat 
modul-modul keamanan secara dinamis dari direktori 'modules/'.
Sistem ini menggunakan 'importlib' untuk mencapai arsitektur *plug-and-play*.
"""

import os
import sys
import importlib
import inspect
from pathlib import Path
from typing import List, Type
from core.base import BaseModule
from core.display import OutputManager

class PluginLoader:
    """Sistem pemuat dinamis untuk modul keamanan WebSpectre."""
    
    def __init__(self, out: OutputManager, modules_dir: str = "modules"):
        self.out = out
        self.modules_dir = Path(modules_dir)
        self.loaded_modules: List[BaseModule] = []
        
        # Pastikan folder modul ada di sys.path agar importlib berfungsi
        if str(self.modules_dir.parent.absolute()) not in sys.path:
            sys.path.insert(0, str(self.modules_dir.parent.absolute()))

    def _is_valid_module(self, cls: Type) -> bool:
        """Memeriksa apakah sebuah kelas (class) mewarisi BaseModule dan bukan kelas abstrak."""
        return (
            inspect.isclass(cls) 
            and issubclass(cls, BaseModule) 
            and cls is not BaseModule
            and not inspect.isabstract(cls)
        )

    def load_all(self) -> List[BaseModule]:
        """
        Memindai direktori modul dan memuat semua modul Python yang valid.
        
        Returns:
            List[BaseModule]: Daftar instance dari modul-modul yang berhasil dimuat.
        """
        self.out.info(f"Memindai direktori '{self.modules_dir}' untuk modul keamanan...")
        
        if not self.modules_dir.exists() or not self.modules_dir.is_dir():
            self.out.error(f"Direktori '{self.modules_dir}' tidak ditemukan.")
            return []

        module_count = 0
        
        # Iterasi seluruh file .py di dalam direktori modul (mendukung subdirektori/kategori)
        for filepath in self.modules_dir.rglob("*.py"):
            if filepath.name == "__init__.py":
                continue
                
            # Mengonversi path file menjadi path modul Python (misal: modules.discovery.dns)
            rel_path = filepath.relative_to(self.modules_dir.parent)
            module_name = str(rel_path).replace(os.sep, ".").replace(".py", "")
            
            try:
                # Memuat file sebagai modul Python
                py_module = importlib.import_module(module_name)
                
                # Mencari kelas yang mewarisi BaseModule
                for name, obj in inspect.getmembers(py_module):
                    if self._is_valid_module(obj):
                        try:
                            # Inisialisasi modul
                            instance = obj()
                            self.loaded_modules.append(instance)
                            module_count += 1
                        except Exception as e:
                            self.out.warning(f"Gagal menginisialisasi modul '{name}' di '{module_name}': {e}")
                            
            except ImportError as e:
                self.out.error(f"Gagal memuat file '{filepath.name}'", cause=str(e))
                
        self.out.success(f"Berhasil memuat {module_count} modul keamanan.")
        return self.loaded_modules

    def get_modules_by_category(self, category: str) -> List[BaseModule]:
        """Mengambil modul yang telah dimuat berdasarkan kategorinya."""
        return [m for m in self.loaded_modules if m.meta.get("category", "").lower() == category.lower()]
