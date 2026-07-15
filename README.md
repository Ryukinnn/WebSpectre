# WebSpectre Framework

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)
![License](https://img.shields.io/badge/license-MIT-red.svg)

WebSpectre adalah framework modular untuk analisis keamanan website (Website Security Assessment Framework) yang dirancang untuk pengembang, administrator sistem, dan tim keamanan siber profesional.

## Filosofi

WebSpectre dirancang dengan prinsip:
1. **Pasif & Aman**: Tidak ada eksploitasi aktif, serangan kredensial, atau muatan destruktif. Framework ini hanya menganalisis permukaan serangan, konfigurasi, dan arsitektur publik.
2. **Modularitas Tinggi**: Dibangun dengan *clean architecture* yang memungkinkan penambahan modul analisis dengan sangat mudah tanpa mengubah *core engine*.
3. **Laporan Profesional**: Menghasilkan pelaporan siap pakai bergaya korporat yang memetakan temuan ke standar industri seperti OWASP, CWE, dan estimasi skor CVSS.

## Fitur Utama

- **Antarmuka CLI Interaktif**: Dibangun dengan antarmuka terminal yang modern dan responsif.
- **Arsitektur Modular**: Mendukung hingga puluhan modul yang dimuat secara dinamis.
- **Analisis Multi-Layer**:
  - *Passive Reconnaissance* (DNS, Asset Discovery)
  - *Configuration Review* (Security Headers, CORS, CSP, SSL/TLS)
  - *Technology Fingerprinting* (CMS, WAF, Reverse Proxy)
- **Ekspor Laporan**: Mendukung HTML, Markdown, JSON, CSV, dan PDF.
- **Manajemen Konfigurasi**: Fleksibel dan dapat disesuaikan melalui `config/config.yaml`.

## Instalasi

WebSpectre dirancang secara optimal untuk lingkungan Linux (Kali Linux, Ubuntu, Debian).

```bash
# Clone repositori
git clone https://github.com/Ryukinnn/WebSpectre.git
cd WebSpectre

# Jalankan skrip setup untuk instalasi dependensi dan inisialisasi lingkungan
python3 setup.py
```

## Penggunaan

Setelah instalasi selesai, jalankan antarmuka utama:

```bash
python3 spectre.py
```

Untuk melihat informasi *framework*:
```bash
python3 spectre.py --about
```

## Struktur Proyek

- `core/`: Komponen mesin utama (*engine*, *loader*, *display*, *config*).
- `modules/`: Modul-modul keamanan (Discovery, HTTP Analysis, dll).
- `plugins/`: Ekstensi tambahan pihak ketiga.
- `reports/`: Hasil ekspor laporan keamanan.
- `config/`: Konfigurasi global sistem.

## Kontribusi

Kami menyambut kontribusi dari komunitas sumber terbuka. Silakan baca panduan kontributor sebelum mengirimkan *Pull Request*.

## Lisensi

Didistribusikan di bawah Lisensi MIT. Lihat file `LICENSE` untuk informasi lebih lanjut.

---
Dikembangkan oleh **Ryukinnn**
