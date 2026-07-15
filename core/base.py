"""
WebSpectre Framework - Base Module
Developer: Ryukinnn

Mendefinisikan antarmuka abstrak (Abstract Base Class) yang harus 
diimplementasikan oleh setiap modul keamanan di dalam WebSpectre.
Memastikan konsistensi input, eksekusi, dan output antar modul.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseModule(ABC):
    """
    Kelas dasar untuk semua modul keamanan WebSpectre.
    Semua plugin kustom harus mewarisi kelas ini.
    """
    
    def __init__(self):
        # Metadata modul (Wajib didefinisikan oleh modul anak)
        self.meta: Dict[str, str] = {
            "name": "Unnamed Module",
            "description": "No description provided",
            "author": "Unknown",
            "version": "1.0.0",
            "category": "Uncategorized",
            "risk_level": "INFO"  # INFO, LOW, MEDIUM, HIGH, CRITICAL
        }
        
        # Opsi yang digunakan oleh modul
        self.options: Dict[str, Any] = {}
        
        # Menyimpan daftar temuan hasil eksekusi modul
        self.findings: List[Dict[str, Any]] = []

    @abstractmethod
    def setup(self) -> bool:
        """
        Fase persiapan sebelum modul dijalankan.
        Digunakan untuk inisialisasi sesi, memeriksa koneksi, atau memvalidasi target.
        
        Returns:
            bool: True jika persiapan berhasil dan modul siap dieksekusi.
        """
        pass

    @abstractmethod
    async def execute(self, target: str) -> None:
        """
        Logika utama analisis keamanan.
        Harus berjalan secara asinkron (async) agar tidak memblokir antarmuka utama.
        
        Args:
            target (str): URL atau alamat IP yang sedang dianalisis.
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """
        Membersihkan memori, menutup koneksi jaringan, atau 
        menghapus file sementara setelah modul selesai.
        """
        pass

    def add_finding(self, title: str, description: str, severity: str, reference: str = ""):
        """Mendaftarkan temuan keamanan ke dalam sistem pelaporan pusat."""
        self.findings.append({
            "title": title,
            "description": description,
            "severity": severity,
            "reference": reference,
            "module": self.meta["name"]
        })

    def get_findings(self) -> List[Dict[str, Any]]:
        """Mengembalikan seluruh temuan yang didapatkan modul ini."""
        return self.findings
