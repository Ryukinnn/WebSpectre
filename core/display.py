"""
WebSpectre Framework - Output Manager
Developer: Ryukinnn

Modul ini bertanggung jawab atas seluruh manajemen antarmuka dan log.
Menyediakan sistem pelaporan terpusat agar antarmuka tetap konsisten dan profesional.
Mendukung level pesan (INFO, BERHASIL, PERINGATAN, RISIKO, ERROR) menggunakan rich.
"""

import sys
import logging
from typing import Optional, Any
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

class OutputManager:
    """Manajer output terpusat untuk CLI dan Logging."""
    
    def __init__(self, log_level: str = "INFO"):
        self.console = Console()
        self.logger = self._setup_logger(log_level)
    
    def _setup_logger(self, log_level: str) -> logging.Logger:
        """Menginisialisasi sistem logging ke file."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logger = logging.getLogger("WebSpectre")
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        # Mencegah duplikasi handler
        if not logger.handlers:
            # File handler untuk error
            error_handler = logging.FileHandler("logs/errors.log", encoding="utf-8")
            error_handler.setLevel(logging.ERROR)
            error_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
            error_handler.setFormatter(error_formatter)
            
            # File handler untuk informasi umum
            main_handler = logging.FileHandler("logs/spectre.log", encoding="utf-8")
            main_handler.setLevel(logging.DEBUG)
            main_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
            main_handler.setFormatter(main_formatter)
            
            logger.addHandler(error_handler)
            logger.addHandler(main_handler)
            
        return logger

    def info(self, message: str, module: Optional[str] = None):
        """Menampilkan informasi standar."""
        prefix = f"[{module}] " if module else ""
        self.console.print(f"[bold cyan][INFO][/bold cyan] {prefix}{message}")
        self.logger.info(f"{prefix}{message}")

    def success(self, message: str, module: Optional[str] = None):
        """Menampilkan pesan keberhasilan."""
        prefix = f"[{module}] " if module else ""
        self.console.print(f"[bold green][BERHASIL][/bold green] {prefix}{message}")
        self.logger.info(f"SUCCESS: {prefix}{message}")

    def warning(self, message: str, module: Optional[str] = None):
        """Menampilkan peringatan (non-kritis)."""
        prefix = f"[{module}] " if module else ""
        self.console.print(f"[bold yellow][PERINGATAN][/bold yellow] {prefix}{message}")
        self.logger.warning(f"{prefix}{message}")

    def risk(self, message: str, level: str = "SEDANG", module: Optional[str] = None):
        """
        Menampilkan temuan risiko.
        Level dapat berupa: RENDAH, SEDANG, TINGGI, KRITIS
        """
        prefix = f"[{module}] " if module else ""
        
        color = "yellow"
        if level.upper() == "KRITIS":
            color = "red bold reverse"
        elif level.upper() == "TINGGI":
            color = "red"
        elif level.upper() == "RENDAH":
            color = "blue"
            
        self.console.print(f"[{color}][RISIKO {level.upper()}][/{color}] {prefix}{message}")
        self.logger.warning(f"RISK ({level}): {prefix}{message}")

    def error(self, message: str, cause: Optional[str] = None, solution: Optional[str] = None, module: Optional[str] = None):
        """
        Menampilkan pesan error terstruktur dengan penyebab dan solusi.
        Tidak akan mematikan program secara paksa untuk mencegah crash tak terduga.
        """
        prefix = f"[{module}] " if module else ""
        self.logger.error(f"{prefix}{message}")
        
        error_text = f"[bold red]{message}[/bold red]\n"
        if cause:
            error_text += f"\n[bold white]Kemungkinan penyebab:[/bold white]\n{cause}\n"
            self.logger.error(f"Cause: {cause}")
        if solution:
            error_text += f"\n[bold green]Solusi:[/bold green]\n{solution}"
            self.logger.error(f"Solution: {solution}")
            
        self.console.print(Panel(error_text, title="[bold red reverse] ERROR [/bold red reverse]", border_style="red", expand=False))

    def render_table(self, title: str, columns: list, rows: list):
        """Merender tabel informasi secara konsisten."""
        table = Table(title=title, style="cyan", border_style="cyan")
        for col in columns:
            table.add_column(col)
        for row in rows:
            table.add_row(*row)
        self.console.print(table)
