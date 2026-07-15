"""
WebSpectre Framework - Robots.txt Discovery Module
Developer: Ryukinnn
"""

from core.base import BaseModule
from utils.network import fetch_url
from utils.validator import normalize_target
import urllib.parse

class RobotsTxtModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "Robots.txt Analysis",
            "description": "Menganalisis file robots.txt untuk menemukan direktori atau endpoint tersembunyi.",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "Discovery",
            "risk_level": "LOW"
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        target = normalize_target(target)
        parsed = urllib.parse.urlparse(target)
        
        # Susun URL robots.txt di root domain
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        content = await fetch_url(robots_url)
        
        if content and ("User-agent:" in content or "Disallow:" in content):
            lines = content.split('\n')
            disallowed_paths = [line.split(":")[1].strip() for line in lines if line.strip().lower().startswith("disallow")]
            
            if disallowed_paths:
                self.add_finding(
                    title="File robots.txt Ditemukan",
                    description=f"Ditemukan {len(disallowed_paths)} entri 'Disallow' di robots.txt yang mungkin mengekspos direktori rahasia.",
                    severity="LOW",
                    reference=robots_url
                )
            else:
                self.add_finding(
                    title="File robots.txt Ditemukan (Aman)",
                    description="File robots.txt ditemukan, tetapi tidak ada entri 'Disallow' yang mencurigakan.",
                    severity="INFO"
                )
        else:
            self.add_finding(
                title="File robots.txt Tidak Ditemukan",
                description="Target tidak mengimplementasikan file robots.txt.",
                severity="INFO"
            )

    def cleanup(self) -> None:
        pass
