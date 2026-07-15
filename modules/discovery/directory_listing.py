"""
WebSpectre Framework - Directory Listing Discovery Module
Developer: Ryukinnn
"""

from core.base import BaseModule
from utils.network import fetch_advanced
from utils.validator import normalize_target

class DirectoryListingModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "Directory Listing Analysis",
            "description": "Mendeteksi apakah web server mengizinkan penampilan daftar isi direktori (Index of /).",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "Discovery",
            "risk_level": "MEDIUM"
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        target = normalize_target(target)
        
        # Mengecek URL target dan juga URL dengan path acak/umum yang mungkin memicu listing
        # Di sini kita cek path root dan folder rahasia umum
        test_paths = ["/images/", "/assets/", "/css/", "/js/", "/uploads/"]
        
        found_listing = False
        
        for path in test_paths:
            # Gunakan rstrip pada target untuk menghindari double slash
            url = f"{target.rstrip('/')}{path}"
            response = await fetch_advanced(url)
            
            if response and response["status"] == 200:
                body = response["body"].lower()
                # Tanda-tanda khas Directory Listing pada Apache, Nginx, IIS
                if "index of /" in body or "[to parent directory]" in body or "<title>index of" in body:
                    found_listing = True
                    self.add_finding(
                        title="Directory Listing Aktif",
                        description=f"Server mengekspos daftar isi direktori pada rute: {url}",
                        severity="MEDIUM",
                        reference=url
                    )
                    
        if not found_listing:
            self.add_finding(
                title="Directory Listing Dinonaktifkan",
                description="Server terkonfigurasi dengan baik untuk menyembunyikan daftar isi direktori (Index of /).",
                severity="INFO"
            )

    def cleanup(self) -> None:
        pass
