"""
Module Web/API Scan
--------------------
Intègre :
  - OWASP ZAP (API mode)
  - Dependency-Check (OWASP)
  - SSLyze via module scan
"""

import subprocess
import shutil
import logging
import requests
from typing import Any

logger = logging.getLogger(__name__)


class WebScanModule:
    def run(self, target: str, options: dict) -> dict:
        results: dict[str, Any] = {"target": target}

        if options.get("zap", True):
            results["zap"] = self._zap_scan(target, options)

        if options.get("dep_check", False):
            results["dependency_check"] = self._dependency_check(options.get("project_path", "."))

        return results

    def _zap_scan(self, target: str, options: dict) -> dict:
        zap_url  = options.get("zap_url", "http://localhost:8080")
        zap_key  = options.get("zap_api_key", "")
        scan_type = options.get("scan_type", "spider")

        try:
            if scan_type == "spider":
                r = requests.get(
                    f"{zap_url}/JSON/spider/action/scan/",
                    params={"apikey": zap_key, "url": target},
                    timeout=10,
                )
                r.raise_for_status()
                return {"scan_id": r.json().get("scan"), "type": "spider"}
            elif scan_type == "active":
                r = requests.get(
                    f"{zap_url}/JSON/ascan/action/scan/",
                    params={"apikey": zap_key, "url": target},
                    timeout=10,
                )
                r.raise_for_status()
                return {"scan_id": r.json().get("scan"), "type": "active"}
            else:
                return {"error": f"Type de scan ZAP inconnu : {scan_type}"}
        except requests.RequestException as e:
            return {"error": f"ZAP non disponible : {e}"}

    def _dependency_check(self, project_path: str) -> dict:
        dc_bin = shutil.which("dependency-check") or shutil.which("dependency-check.sh")
        if not dc_bin:
            return {"error": "dependency-check non installé"}
        try:
            cmd = [dc_bin, "--project", "pentest", "--scan", project_path, "--format", "JSON", "--out", "/tmp/depcheck"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            return {"output": proc.stdout[-2000:]}
        except Exception as e:
            return {"error": str(e)}
