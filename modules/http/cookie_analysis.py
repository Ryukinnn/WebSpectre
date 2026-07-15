"""
WebSpectre Framework - Cookie Analysis Module
Developer: Ryukinnn
"""

from core.base import BaseModule
from utils.network import fetch_advanced
from utils.validator import normalize_target

class CookieAnalysisModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "Cookie Security Analysis",
            "description": "Memeriksa parameter keamanan pada cookie (HttpOnly, Secure, SameSite).",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "HTTP Analysis",
            "risk_level": "MEDIUM"
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        target = normalize_target(target)
        response = await fetch_advanced(target)
        
        if not response:
            return
            
        headers = response["headers"]
        
        # Ekstrak header Set-Cookie (menangani jika ada banyak Set-Cookie)
        # aiohttp merangkum multiple Set-Cookie menjadi string yang dipisahkan koma atau multi-dict
        # Jika dictionary biasa, kita mungkin hanya dapat satu. aiohttp mengembalikan dict standar
        # Untuk analisis mendalam, modul ini mengambil Set-Cookie mentah
        cookies = [v for k, v in headers.items() if k.lower() == "set-cookie"]
        
        if not cookies:
            self.add_finding(
                title="Tidak Ada Cookie Ditetapkan",
                description="Target tidak mengatur cookie HTTP saat diakses.",
                severity="INFO"
            )
            return

        for cookie_string in cookies:
            cookie_parts = cookie_string.lower().split(";")
            
            missing_flags = []
            if " httponly" not in cookie_parts and "httponly" not in cookie_parts:
                missing_flags.append("HttpOnly (Rentan XSS)")
            if " secure" not in cookie_parts and "secure" not in cookie_parts:
                missing_flags.append("Secure (Rentan Intersepsi)")
            if not any("samesite" in p for p in cookie_parts):
                missing_flags.append("SameSite (Rentan CSRF)")
                
            if missing_flags:
                # Mengambil nama cookie saja
                cookie_name = cookie_string.split("=")[0]
                self.add_finding(
                    title=f"Cookie '{cookie_name}' Tidak Aman",
                    description=f"Cookie ini kehilangan atribut keamanan penting: {', '.join(missing_flags)}",
                    severity="MEDIUM"
                )
            else:
                self.add_finding(
                    title="Cookie Aman",
                    description=f"Cookie yang ditetapkan telah mematuhi standar keamanan.",
                    severity="INFO"
                )

    def cleanup(self) -> None:
        pass
