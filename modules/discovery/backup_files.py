"""
WebSpectre Framework - Backup Files Discovery Module
Developer: Ryukinnn
"""

import asyncio
from core.base import BaseModule
from utils.network import fetch_advanced
from utils.validator import normalize_target
import urllib.parse

class BackupFilesModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "Backup Files Discovery",
            "description": "Mencari file cadangan yang tertinggal (seperti .bak, .zip) yang mungkin membocorkan *source code*.",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "Discovery",
            "risk_level": "HIGH"
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        target = normalize_target(target)
        parsed = urllib.parse.urlparse(target)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        # Daftar ekstensi dan file umum
        common_backups = [
            "/backup.zip", "/backup.tar.gz", "/backup.sql",
            "/db.sql", "/dump.sql", "/config.php.bak",
            "/.env.bak", "/.git/config", "/.svn/entries"
        ]
        
        async def check_file(path: str):
            url = f"{base_url}{path}"
            # Lakukan request HEAD/GET untuk melihat apakah file ada (status 200)
            response = await fetch_advanced(url, method="HEAD")
            if response and response["status"] == 200:
                # Validasi tambahan untuk menghindari false positive (misal halaman 404 kustom yang mereturn 200)
                content_type = response["headers"].get("Content-Type", "").lower()
                if "text/html" not in content_type:
                    self.add_finding(
                        title="File Sensitif Terberekspos",
                        description=f"Ditemukan file yang diduga sebagai cadangan atau file rahasia: {url}",
                        severity="HIGH",
                        reference=url
                    )

        # Cek secara paralel
        tasks = [check_file(path) for path in common_backups]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        if not self.findings:
            self.add_finding(
                title="Tidak Ditemukan File Cadangan",
                description="Sistem tidak mendeteksi adanya file cadangan standar di root direktori.",
                severity="INFO"
            )

    def cleanup(self) -> None:
        pass
