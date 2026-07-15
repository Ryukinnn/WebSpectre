"""
WebSpectre Framework - Content Management System (CMS) Detection Module
Developer: Ryukinnn
"""

from core.base import BaseModule
from utils.network import fetch_advanced
from utils.validator import normalize_target

class CMSDetectModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "CMS Fingerprinting",
            "description": "Mengidentifikasi Content Management System (CMS) yang digunakan (WordPress, Joomla, dll).",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "Technology Analysis",
            "risk_level": "INFO"
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        target = normalize_target(target)
        response = await fetch_advanced(target)
        
        if not response:
            return
            
        body = response["body"].lower()
        headers = {k.lower(): v for k, v in response["headers"].items()}
        
        cms_found = None
        
        # WordPress Deteksi
        if "wp-content" in body or "wp-includes" in body or "wordpress" in body:
            cms_found = "WordPress"
            
        # Joomla Deteksi
        elif "joomla!" in body or "index.php?option=com_" in body or "generator" in body and "joomla" in body:
            cms_found = "Joomla"
            
        # Drupal Deteksi
        elif "drupal.org" in body or "sites/default" in body:
            cms_found = "Drupal"
            
        # Ghost Deteksi
        elif "ghost-blog" in body or "ghost.org" in body:
            cms_found = "Ghost"
            
        # Mengecek via Header (misal X-Powered-By atau X-Generator)
        if not cms_found:
            for v in headers.values():
                val = v.lower()
                if "wordpress" in val:
                    cms_found = "WordPress"
                elif "joomla" in val:
                    cms_found = "Joomla"
                elif "drupal" in val:
                    cms_found = "Drupal"
        
        if cms_found:
            self.add_finding(
                title="CMS Teridentifikasi",
                description=f"Target dikonfirmasi menggunakan sistem manajemen konten: {cms_found}",
                severity="INFO"
            )
        else:
            self.add_finding(
                title="CMS Tidak Dikenali",
                description="Target tidak menggunakan CMS standar yang dapat dikenali secara statis.",
                severity="INFO"
            )

    def cleanup(self) -> None:
        pass
