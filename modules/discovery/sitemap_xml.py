"""
WebSpectre Framework - Sitemap.xml Discovery Module
Developer: Ryukinnn
"""

from core.base import BaseModule
from utils.network import fetch_url
from utils.validator import normalize_target
import urllib.parse

class SitemapXmlModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "Sitemap.xml Analysis",
            "description": "Mencari file sitemap.xml untuk menemukan arsitektur dan endpoint tersembunyi.",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "Discovery",
            "risk_level": "INFO"
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        target = normalize_target(target)
        parsed = urllib.parse.urlparse(target)
        sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
        
        content = await fetch_url(sitemap_url)
        
        if content and "<urlset" in content:
            # Penghitungan sederhana tanpa memparsing XML penuh demi kecepatan
            url_count = content.count("<loc>")
            
            self.add_finding(
                title="File sitemap.xml Ditemukan",
                description=f"Ditemukan {url_count} endpoint di dalam sitemap.xml yang dapat digunakan untuk pemetaan web lebih lanjut.",
                severity="INFO",
                reference=sitemap_url
            )
        else:
            self.add_finding(
                title="File sitemap.xml Tidak Ditemukan",
                description="Target tidak mengekspos sitemap.xml di lokasi standar.",
                severity="INFO"
            )

    def cleanup(self) -> None:
        pass
