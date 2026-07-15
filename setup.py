#!/usr/bin/env python3
"""
WebSpectre Framework - Setup Script
Developer: Ryukinnn
Version: 1.0.0

Script ini hanya digunakan untuk instalasi awal WebSpectre.
Tanggung jawab:
- Memeriksa versi Python (3.12+)
- Memeriksa kompatibilitas sistem operasi (Kali Linux, Ubuntu, Debian)
- Menginstall dependensi dari requirements.txt
- Memastikan struktur direktori
- Membuat file konfigurasi default
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path

# Warna ANSI untuk output awal sebelum rich terinstall
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def print_step(msg):
    print(f"{CYAN}[*]{RESET} {msg}")

def print_success(msg):
    print(f"{GREEN}[✓]{RESET} {msg}")

def print_error(msg):
    print(f"{RED}[✗]{RESET} {msg}")
    sys.exit(1)

def print_warning(msg):
    print(f"{YELLOW}[!]{RESET} {msg}")

def check_python():
    print_step("Memeriksa versi Python...")
    if sys.version_info < (3, 12):
        print_error(f"WebSpectre membutuhkan Python 3.12 atau lebih baru. Terdeteksi: {sys.version_info.major}.{sys.version_info.minor}")
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor} terdeteksi.")

def check_os():
    print_step("Memeriksa sistem operasi...")
    if sys.platform != "linux":
        print_warning("WebSpectre dirancang untuk Kali Linux, Ubuntu, atau Debian.")
        print_warning("Menjalankan di OS selain Linux mungkin menyebabkan beberapa modul tidak stabil.")
    else:
        # Pengecekan spesifik distro Linux bisa dilakukan di sini jika diperlukan
        print_success("Sistem operasi Linux terdeteksi.")

def install_dependencies():
    print_step("Menginstall dependensi dari requirements.txt...")
    req_file = Path("requirements.txt")
    if not req_file.exists():
        print_error("File requirements.txt tidak ditemukan.")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"])
        print_success("Semua dependensi berhasil diinstall.")
    except subprocess.CalledProcessError:
        print_error("Gagal menginstall dependensi. Periksa koneksi internet Anda atau hak akses pip.")

def initialize_workspace():
    # Menggunakan rich setelah dipastikan terinstall
    try:
        from rich.console import Console
        from rich.progress import Progress, SpinnerColumn, TextColumn
        from rich.panel import Panel
    except ImportError:
        print_error("Library 'rich' gagal dimuat setelah instalasi. Silakan jalankan instalasi manual: pip install -r requirements.txt")

    console = Console()
    console.print()
    console.print(Panel.fit(
        "[bold cyan]WebSpectre Setup[/bold cyan]\n[dim]Dikembangkan oleh: Ryukinnn[/dim]",
        border_style="cyan"
    ))

    base_dir = Path(__file__).parent

    # Direktori yang diperlukan
    dirs = [
        "core", "modules", "plugins", "config", 
        "reports", "logs", "database", "assets", 
        "templates", "utils", "docs", "examples", "tests"
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task_dir = progress.add_task("[cyan]Memverifikasi struktur direktori...", total=len(dirs))
        for d in dirs:
            dir_path = base_dir / d
            dir_path.mkdir(exist_ok=True)
            # Buat __init__.py untuk direktori paket Python
            if d in ["core", "modules", "plugins", "utils"]:
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    init_file.touch()
            progress.advance(task_dir)

        task_cfg = progress.add_task("[cyan]Membuat konfigurasi default...", total=1)
        config_file = base_dir / "config" / "config.yaml"
        if not config_file.exists():
            default_config = """# WebSpectre Default Configuration
# Developer: Ryukinnn
# Version: 1.0.0

app:
  name: "WebSpectre"
  version: "1.0.0"
  language: "id"  # id = Indonesia, en = English
  theme: "dark"
  log_level: "INFO"

performance:
  max_threads: 10
  timeout: 30
  async_mode: true

reporting:
  default_format: "html"
  save_directory: "reports/"

network:
  user_agent: "WebSpectre/1.0.0 (Security Assessment)"
  verify_ssl: false
  follow_redirects: true
"""
            config_file.write_text(default_config)
        progress.advance(task_cfg)

    console.print("\n[bold green][✓] Instalasi dan inisialisasi ruang kerja berhasil![/bold green]")
    console.print("[cyan]Anda sekarang dapat menjalankan WebSpectre dengan perintah:[/cyan]")
    console.print("[bold yellow]python3 spectre.py[/bold yellow]\n")

def main():
    print(f"{GREEN}================================================{RESET}")
    print(f"{GREEN}        Instalasi WebSpectre Framework{RESET}")
    print(f"{GREEN}================================================{RESET}\n")
    
    try:
        check_python()
        check_os()
        install_dependencies()
        initialize_workspace()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Instalasi dibatalkan oleh pengguna.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}[✗] Terjadi kesalahan fatal: {e}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
