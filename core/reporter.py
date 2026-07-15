"""
WebSpectre Framework - Report Generator
Developer: Ryukinnn

Modul ini memproses temuan (findings) yang dikumpulkan oleh Engine, 
menghitung skor keamanan, dan merender laporan dalam berbagai format 
seperti HTML, JSON, dan Markdown.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from core.display import OutputManager

class ReportGenerator:
    """Mesin pembuat laporan profesional berdasarkan temuan keamanan."""
    
    def __init__(self, out: OutputManager, output_dir: str = "reports/"):
        self.out = out
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def _calculate_score(self, findings: List[Dict[str, Any]]) -> int:
        """Menghitung skor keamanan (0-100) berdasarkan tingkat keparahan."""
        base_score = 100
        
        weight = {
            "CRITICAL": 25,
            "HIGH": 15,
            "MEDIUM": 5,
            "LOW": 2,
            "INFO": 0
        }
        
        for f in findings:
            severity = str(f.get("severity", "INFO")).upper()
            base_score -= weight.get(severity, 0)
            
        return max(0, base_score)

    def _generate_json(self, data: Dict[str, Any], filepath: Path):
        """Menyimpan data laporan dalam format JSON murni."""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            self.out.success(f"Laporan JSON berhasil disimpan: {filepath.name}", module="Reporter")
        except Exception as e:
            self.out.error(f"Gagal menyimpan JSON: {e}", module="Reporter")

    def _generate_markdown(self, data: Dict[str, Any], filepath: Path):
        """Merender laporan dalam format Markdown (GitHub style)."""
        md_content = f"# WebSpectre Security Report\n\n"
        md_content += f"**Target:** {data['target']}  \n"
        md_content += f"**Tanggal:** {data['timestamp']}  \n"
        md_content += f"**Skor Keamanan:** {data['security_score']}/100  \n\n"
        
        md_content += "## Ringkasan Eksekutif\n\n"
        md_content += f"Analisis keamanan berhasil diselesaikan dengan total **{data['total_findings']}** temuan.\n\n"
        
        md_content += "## Detail Temuan\n\n"
        for finding in data['findings']:
            severity = finding.get("severity", "INFO")
            md_content += f"### [{severity}] {finding.get('title', 'Unknown')}\n"
            md_content += f"- **Modul:** {finding.get('module', 'Unknown')}\n"
            md_content += f"- **Deskripsi:** {finding.get('description', 'Tidak ada deskripsi.')}\n"
            if finding.get('reference'):
                md_content += f"- **Referensi:** {finding.get('reference')}\n"
            md_content += "\n"
            
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(md_content)
            self.out.success(f"Laporan Markdown berhasil disimpan: {filepath.name}", module="Reporter")
        except Exception as e:
            self.out.error(f"Gagal menyimpan Markdown: {e}", module="Reporter")

    def export(self, target: str, findings: List[Dict[str, Any]], formats: List[str]):
        """Titik masuk utama untuk mengekspor laporan ke berbagai format."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_target = target.replace("https://", "").replace("http://", "").replace("/", "_")
        
        report_data = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "developer": "Ryukinnn",
            "framework": "WebSpectre v1.0.0",
            "security_score": self._calculate_score(findings),
            "total_findings": len(findings),
            "findings": findings
        }
        
        if "json" in formats:
            self._generate_json(report_data, self.output_dir / f"webspectre_{safe_target}_{timestamp}.json")
            
        if "markdown" in formats or "md" in formats:
            self._generate_markdown(report_data, self.output_dir / f"webspectre_{safe_target}_{timestamp}.md")
            
        # Catatan: HTML dan PDF diimplementasikan di iterasi lanjutan jika diperlukan
