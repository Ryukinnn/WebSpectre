#!/usr/bin/env python3
"""
WebSpectre Framework - Primary Entry Point
Developer: Ryukinnn
Version: 1.0.0

File ini adalah titik masuk utama (entry point) untuk seluruh fungsionalitas WebSpectre.
Menangani inisialisasi antarmuka CLI, parsing argumen, dan menu utama.
"""

import os
import sys
import time
import argparse
import platform

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    from rich.prompt import IntPrompt
    from rich import box
except ImportError:
    print("[!] Error: Library 'rich' tidak ditemukan.")
    print("[*] Jalankan instalasi: python3 setup.py")
    sys.exit(1)

from core.config import ConfigManager
from core.loader import PluginLoader
from core.display import OutputManager
from core.engine import AssessmentEngine

console = Console()
VERSION = "1.0.0"

def clear_screen():
    """Membersihkan layar terminal untuk tampilan yang profesional."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    """Menampilkan logo ASCII dan informasi developer."""
    logo = """[bold cyan]
 ██╗    ██╗███████╗██████╗ ███████╗██████╗ ███████╗ ██████╗████████╗██████╗ ███████╗
 ██║    ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔════╝
 ██║ █╗ ██║█████╗  ██████╔╝███████╗██████╔╝█████╗  ██║        ██║   ██████╔╝█████╗  
 ██║███╗██║██╔══╝  ██╔══██╗╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══██╗██╔══╝  
 ╚███╔███╔╝███████╗██████╔╝███████║██║     ███████╗╚██████╗   ██║   ██║  ██║███████╗
  ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝
[/bold cyan]"""
    console.print(logo, justify="center")
    
    header = f"""[bold white]WebSpectre Framework[/bold white]
[cyan]Website Security Assessment[/cyan]
Versi {VERSION}

[dim]Developer:[/dim]
[bold green]Ryukinnn[/bold green]"""
    
    console.print(Panel(header, border_style="cyan", box=box.DOUBLE, padding=(1, 5), expand=False), justify="center")
    console.print()

def loading_sequence():
    """Menampilkan animasi loading inisialisasi sistem."""
    tasks_info = [
        "Memuat konfigurasi",
        "Memeriksa dependensi",
        "Memuat modul keamanan",
        "Menginisialisasi database",
        "Sistem siap digunakan"
    ]
    
    with Progress(
        SpinnerColumn(spinner_name="dots", style="cyan"),
        TextColumn("[bold white]{task.description}"),
        console=console,
        transient=False
    ) as progress:
        tasks = [progress.add_task(desc, total=1) for desc in tasks_info]
        for task_id in tasks:
            time.sleep(0.3)  # Mensimulasikan proses inisialisasi nyata
            progress.update(task_id, advance=1, description=f"[bold green][✓][/bold green] {tasks_info[task_id]}")
    console.print()

def show_system_info(loader: PluginLoader):
    """Menampilkan informasi sistem saat ini dalam bentuk tabel."""
    table = Table(box=box.MINIMAL, border_style="cyan", expand=False)
    table.add_column("Komponen", style="cyan", no_wrap=True)
    table.add_column("Status / Informasi", style="white")

    total_modules = len(loader.loaded_modules)
    
    table.add_row("Sistem Operasi", f"{platform.system()} {platform.release()}")
    table.add_row("Versi Python", platform.python_version())
    table.add_row("Versi Framework", VERSION)
    table.add_row("Modul Dimuat", f"{total_modules} Modul Aktif")
    table.add_row("Status Konfigurasi", "[green]Valid[/green]")

    console.print(Panel(table, title="[bold white]Informasi Sistem[/bold white]", border_style="cyan", expand=False))
    console.print()

def show_about():
    """Menampilkan informasi tentang framework via argumen --about."""
    clear_screen()
    console.print(Panel.fit(
        "[bold cyan]WebSpectre Framework[/bold cyan]\n\n"
        "[dim]Dikembangkan oleh:[/dim] [bold green]Ryukinnn[/bold green]\n\n"
        "Framework analisis keamanan website berbasis Python.\n"
        "Dirancang untuk melakukan audit keamanan yang komprehensif\n"
        "dan profesional secara modular.",
        border_style="cyan",
        title="Tentang WebSpectre"
    ))
    sys.exit(0)

def main_menu(engine: AssessmentEngine, out: OutputManager, config: ConfigManager):
    """Merender menu utama yang interaktif."""
    menu_text = """[bold cyan]1.[/bold cyan] Analisis Website Lengkap
[bold cyan]2.[/bold cyan] Pemeriksaan Konfigurasi & HTTP
[bold cyan]3.[/bold cyan] Analisis Teknologi & Discovery
[bold cyan]4.[/bold cyan] Manajemen Modul
[bold cyan]5.[/bold cyan] Buat Laporan
[bold cyan]6.[/bold cyan] Pengaturan
[bold cyan]0.[/bold cyan] Keluar"""

    while True:
        console.print(Panel(menu_text, title="[bold white]Menu Utama[/bold white]", border_style="cyan", box=box.HEAVY, expand=False))
        
        try:
            # Validasi input ketat dengan rich IntPrompt
            pilihan = IntPrompt.ask("[bold cyan]Pilih menu[/bold cyan]", choices=["0", "1", "2", "3", "4", "5", "6"])
            
            if pilihan == 0:
                out.success("Terima kasih telah menggunakan WebSpectre Framework. Sampai jumpa!")
                break
                
            elif pilihan == 1:
                target = console.input("[bold cyan][?] Masukkan URL Target (contoh: example.com):[/bold cyan] ").strip()
                if not target:
                    out.error("Target tidak boleh kosong!")
                    continue
                from utils.validator import normalize_target
                target = normalize_target(target)
                engine.start_assessment(target)
                
            elif pilihan == 2:
                target = console.input("[bold cyan][?] Masukkan URL Target (contoh: example.com):[/bold cyan] ").strip()
                if not target:
                    continue
                from utils.validator import normalize_target
                target = normalize_target(target)
                
                # Backup modul asli, filter hanya kategori HTTP Analysis
                all_mods = engine.loaded_modules
                engine.loaded_modules = [m for m in all_mods if m.meta.get("category") == "HTTP Analysis"]
                if not engine.loaded_modules:
                    out.warning("Tidak ada modul HTTP Analysis yang dimuat.")
                else:
                    engine.start_assessment(target)
                # Restore
                engine.loaded_modules = all_mods
                
            elif pilihan == 3:
                target = console.input("[bold cyan][?] Masukkan URL Target (contoh: example.com):[/bold cyan] ").strip()
                if not target:
                    continue
                from utils.validator import normalize_target
                target = normalize_target(target)
                
                # Backup modul asli, filter hanya kategori Technology Analysis & Discovery
                all_mods = engine.loaded_modules
                engine.loaded_modules = [m for m in all_mods if m.meta.get("category") in ["Technology Analysis", "Discovery"]]
                if not engine.loaded_modules:
                    out.warning("Tidak ada modul kategori tersebut yang dimuat.")
                else:
                    engine.start_assessment(target)
                # Restore
                engine.loaded_modules = all_mods
                
            elif pilihan == 4:
                table = Table(box=box.SIMPLE, border_style="cyan")
                table.add_column("No", style="cyan", justify="right")
                table.add_column("Nama Modul", style="white")
                table.add_column("Kategori", style="green")
                table.add_column("Tingkat Risiko", style="yellow")
                
                for idx, m in enumerate(engine.loaded_modules, start=1):
                    table.add_row(str(idx), m.meta.get("name"), m.meta.get("category"), m.meta.get("risk_level"))
                
                console.print(Panel(table, title="[bold white]Daftar Modul Terinstal[/bold white]", border_style="cyan"))
                
            elif pilihan == 5:
                if not engine.all_findings:
                    out.warning("Belum ada data temuan. Jalankan Analisis Website terlebih dahulu.")
                else:
                    from core.reporter import ReportGenerator
                    reporter = ReportGenerator(out=out, output_dir=config.get("reporting.save_directory", "reports/"))
                    formats = ["json", "md"]
                    reporter.export(engine.last_target, engine.all_findings, formats)
                    out.info(f"Laporan digenerate untuk target: {engine.last_target}")
                    
            elif pilihan == 6:
                table = Table(title="Konfigurasi Sistem (config/config.yaml)", box=box.SIMPLE, border_style="cyan")
                table.add_column("Kunci Konfigurasi", style="cyan")
                table.add_column("Nilai Saat Ini", style="white")
                
                for k, v in config.config_data.items():
                    if isinstance(v, dict):
                        for sub_k, sub_v in v.items():
                            table.add_row(f"{k}.{sub_k}", str(sub_v))
                    else:
                        table.add_row(k, str(v))
                        
                console.print(table)

        except KeyboardInterrupt:
            out.warning("\nInterupsi terdeteksi. Kembali ke menu utama.")
        except Exception as e:
            out.error(f"Terjadi kesalahan sistem: {str(e)}", cause=str(e), solution="Periksa logs/errors.log")

def main():
    # Manajemen argumen command-line
    parser = argparse.ArgumentParser(description="WebSpectre Framework - Website Security Assessment")
    parser.add_argument("--about", action="store_true", help="Tampilkan informasi tentang WebSpectre")
    
    args = parser.parse_args()
    
    if args.about:
        show_about()

    # Inisialisasi Core Framework
    out = OutputManager(log_level="INFO")
    config = ConfigManager()
    loader = PluginLoader(out=out)
    engine = AssessmentEngine(out=out, max_concurrent_tasks=config.max_threads)
    
    # Eksekusi urutan antarmuka
    clear_screen()
    show_banner()
    loading_sequence()
    
    # Load plugins
    modules = loader.load_all()
    engine.register_modules(modules)
    
    show_system_info(loader)
    main_menu(engine, out, config)

if __name__ == "__main__":
    # Cegah eksekusi dengan Python versi lama
    if sys.version_info < (3, 12):
        print("[!] WebSpectre membutuhkan Python 3.12+.")
        sys.exit(1)
    
    main()
