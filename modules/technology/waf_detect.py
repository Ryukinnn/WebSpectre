"""
WebSpectre Framework - Web Application Firewall (WAF) Detection Module
Developer: Ryukinnn
"""

from core.base import BaseModule
from utils.network import fetch_advanced
from utils.validator import normalize_target

class WAFDetectModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.meta = {
            "name": "WAF Fingerprinting",
            "description": "Mendeteksi keberadaan Web Application Firewall (WAF) yang melindungi target.",
            "author": "Ryukinnn",
            "version": "1.0.0",
            "category": "Technology Analysis",
            "risk_level": "INFO"
        }

    def setup(self) -> bool:
        return True

    async def execute(self, target: str) -> None:
        target = normalize_target(target)
        
        # Kirim payload berbahaya dasar (XSS/SQLi) untuk memicu respons WAF
        # payload = "<script>alert('webspectre')</script> OR 1=1"
        # Kita tempatkan payload di query parameter
        trigger_url = f"{target.rstrip('/')}/?q=%3Cscript%3Ealert(1)%3C/script%3E"
        
        response = await fetch_advanced(trigger_url)
        
        if not response:
            return
            
        status = response["status"]
        headers = {k.lower(): v for k, v in response["headers"].items()}
        body = response["body"].lower()
        
        waf_detected = None
        
        # Cek berdasarkan HTTP Headers yang terkenal
        if "cf-ray" in headers or "server" in headers and "cloudflare" in headers["server"].lower():
            waf_detected = "Cloudflare"
        elif "x-sucuri-id" in headers or "server" in headers and "sucuri" in headers["server"].lower():
            waf_detected = "Sucuri WAF"
        elif "server" in headers and "akamai" in headers["server"].lower():
            waf_detected = "Akamai"
        elif "x-amz-cf-id" in headers:
            waf_detected = "AWS WAF"
        
        # Cek berdasarkan block page atau status code anomali
        if not waf_detected:
            if status in [403, 406, 501] and ("waf" in body or "forbidden" in body or "blocked" in body):
                waf_detected = "Generic/Unknown WAF"
                
        if waf_detected:
            self.add_finding(
                title="Web Application Firewall (WAF) Terdeteksi",
                description=f"Target dilindungi oleh WAF: {waf_detected}.",
                severity="INFO"
            )
        else:
            self.add_finding(
                title="Tidak Ada WAF Terdeteksi",
                description="Tidak ada sistem proteksi WAF yang memblokir payload injeksi dasar.",
                severity="LOW"
            )

    def cleanup(self) -> None:
        pass
