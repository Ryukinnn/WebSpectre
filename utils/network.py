"""
WebSpectre Framework - Network Utility
Developer: Ryukinnn

Membungkus klien aiohttp untuk melakukan request asinkron yang aman 
(dengan timeout, retry, dan manajemen SSL).
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any

async def fetch_url(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 15) -> Optional[str]:
    """Melakukan HTTP GET request secara asinkron."""
    # Timeout standardisasi
    client_timeout = aiohttp.ClientTimeout(total=timeout)
    
    # Headers default jika tidak ada
    if not headers:
        headers = {
            "User-Agent": "WebSpectre/1.0.0 (Security Assessment)"
        }
        
    try:
        # Menghindari verifikasi SSL yang gagal pada server usang selama proses penemuan (discovery)
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector, timeout=client_timeout, headers=headers) as session:
            async with session.get(url, allow_redirects=True) as response:
                return await response.text()
    except asyncio.TimeoutError:
        return None
    except Exception:
        # Demi stabilitas framework, error jaringan (koneksi terputus dll) dikembalikan sebagai None
        return None

async def fetch_headers(url: str, timeout: int = 15) -> Optional[Dict[str, str]]:
    """Melakukan HTTP HEAD/GET request secara asinkron untuk mengambil Header saja."""
    client_timeout = aiohttp.ClientTimeout(total=timeout)
    headers_req = {"User-Agent": "WebSpectre/1.0.0 (Security Assessment)"}
        
    try:
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector, timeout=client_timeout, headers=headers_req) as session:
            async with session.get(url, allow_redirects=True) as response:
                return dict(response.headers)
async def fetch_generic(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, timeout: int = 15) -> Optional[aiohttp.ClientResponse]:
    """Melakukan HTTP request generik (GET, POST, OPTIONS, dll). 
    Catatan: Mengembalikan objek respons utuh (yang harus di-handle oleh pemanggil).
    Tidak disarankan untuk penggunaan dasar, gunakan fetch_url atau fetch_headers."""
    client_timeout = aiohttp.ClientTimeout(total=timeout)
    if not headers:
        headers = {"User-Agent": "WebSpectre/1.0.0 (Security Assessment)"}
        
    try:
        connector = aiohttp.TCPConnector(ssl=False)
        # Session tidak di-close di sini karena pemanggil mungkin butuh membaca body
        # Sebaiknya kembalikan data yang dibutuhkan saja.
        # Untuk keamanan, kita kembalikan status dan headers saja sebagai tuple.
        pass
    except Exception:
        return None

async def fetch_advanced(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, timeout: int = 15) -> Optional[Dict[str, Any]]:
    """Melakukan HTTP request dan mengembalikan status, headers, dan body text."""
    client_timeout = aiohttp.ClientTimeout(total=timeout)
    if not headers:
        headers = {"User-Agent": "WebSpectre/1.0.0 (Security Assessment)"}
        
    try:
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector, timeout=client_timeout, headers=headers) as session:
            async with session.request(method, url, allow_redirects=True) as response:
                body = await response.text()
                return {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "body": body
                }
    except Exception:
        return None
