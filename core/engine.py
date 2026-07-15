"""
WebSpectre Framework - Assessment Engine
Developer: Ryukinnn

Engine inti yang mengelola siklus hidup (lifecycle) dari proses analisis.
Tanggung jawab:
- Mengorkestrasi eksekusi modul keamanan.
- Mengelola *async event loop* untuk paralelisasi tugas.
- Mengumpulkan temuan (findings) dari setiap modul.
- Berinteraksi dengan OutputManager untuk memperbarui tampilan dashboard.
"""

import asyncio
import time
from typing import List, Dict, Any
from core.display import OutputManager
from core.base import BaseModule

class AssessmentEngine:
    """Mesin orkestrasi untuk mengeksekusi modul-modul WebSpectre."""
    
    def __init__(self, out: OutputManager, max_concurrent_tasks: int = 10):
        self.out = out
        self.max_concurrent_tasks = max_concurrent_tasks
        self.loaded_modules: List[BaseModule] = []
        self.all_findings: List[Dict[str, Any]] = []
        self.start_time = 0.0

    def register_modules(self, modules: List[BaseModule]):
        """Mendaftarkan modul-modul yang telah divalidasi oleh PluginLoader."""
        self.loaded_modules.extend(modules)
        self.out.info(f"{len(modules)} modul berhasil diregistrasi ke Engine.")

    async def _run_module(self, module: BaseModule, target: str):
        """Mengeksekusi satu modul tunggal dengan penanganan error."""
        module_name = module.meta.get('name', 'Unknown')
        
        try:
            # 1. Fase Setup
            if not module.setup():
                self.out.warning(f"Fase setup gagal. Modul dilewati.", module=module_name)
                return

            # 2. Fase Eksekusi
            # self.out.info(f"Mengeksekusi analisis...", module=module_name)
            await module.execute(target)

            # 3. Pengumpulan Temuan
            findings = module.get_findings()
            if findings:
                self.all_findings.extend(findings)
                self.out.success(f"Menemukan {len(findings)} indikasi keamanan.", module=module_name)

        except asyncio.TimeoutError:
            self.out.warning("Waktu eksekusi habis (Timeout).", module=module_name)
        except Exception as e:
            self.out.error(f"Kesalahan internal modul: {str(e)}", module=module_name)
        finally:
            # 4. Fase Cleanup
            module.cleanup()

    async def _orchestrate(self, target: str):
        """Mengelola antrean eksekusi modul secara asinkron (Concurrency)."""
        # Gunakan semaphore untuk membatasi beban jaringan
        semaphore = asyncio.Semaphore(self.max_concurrent_tasks)
        
        async def sem_run(module: BaseModule):
            async with semaphore:
                await self._run_module(module, target)
        
        tasks = [sem_run(mod) for mod in self.loaded_modules]
        
        self.out.info("Memulai proses analisis asinkron...")
        await asyncio.gather(*tasks, return_exceptions=True)

    def start_assessment(self, target: str):
        """Titik masuk sinkron yang dipanggil oleh CLI (spectre.py)."""
        self.start_time = time.time()
        self.out.info(f"Memulai analisis keamanan untuk target: [bold white]{target}[/bold white]")
        
        if not self.loaded_modules:
            self.out.error("Tidak ada modul yang dimuat. Analisis dibatalkan.", cause="PluginLoader kosong.")
            return
            
        try:
            # Menjalankan event loop asinkron utama
            asyncio.run(self._orchestrate(target))
        except KeyboardInterrupt:
            self.out.warning("Analisis dihentikan paksa oleh pengguna!")
        finally:
            elapsed = time.time() - self.start_time
            
            # Tampilkan Ringkasan Singkat
            self.out.info("=" * 50)
            self.out.info("RINGKASAN ANALISIS")
            self.out.info("=" * 50)
            self.out.info(f"Target        : {target}")
            self.out.info(f"Modul Selesai : {len(self.loaded_modules)}")
            self.out.info(f"Total Temuan  : {len(self.all_findings)}")
            self.out.info(f"Waktu Eksekusi: {elapsed:.2f} detik")
            self.out.info("=" * 50)
            
            if self.all_findings:
                self.out.success("Analisis selesai. Segera buat Laporan untuk melihat detail temuan.")
            else:
                self.out.info("Analisis selesai. Tidak ditemukan celah keamanan yang signifikan.")
