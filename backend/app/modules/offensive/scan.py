"""
Module Scan de Vulnérabilités
------------------------------
Intègre :
  - Nmap NSE (scripts vulnérabilité)
  - Nikto (serveurs web)
  - SSLyze (audit TLS/SSL)
"""

import subprocess
import shutil
import logging
from typing import Any

logger = logging.getLogger(__name__)


class ScanModule:
    def run(self, target: str, options: dict) -> dict:
        results: dict[str, Any] = {"target": target}

        results["nmap_vuln"] = self._nmap_vuln(target, options)

        if options.get("nikto", True):
            results["nikto"] = self._nikto(target, options)

        if options.get("sslyze", False):
            results["sslyze"] = self._sslyze(target)

        return results

    def _nmap_vuln(self, target: str, options: dict) -> dict:
        if not shutil.which("nmap"):
            return {"error": "nmap non installé"}
        port = options.get("port", "")
        port_arg = ["-p", str(port)] if port else []
        try:
            cmd = ["nmap", "--script=vuln"] + port_arg + [target, "-oX", "-"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            return {"raw_xml": proc.stdout}
        except subprocess.TimeoutExpired:
            return {"error": "Timeout nmap vuln"}
        except Exception as e:
            return {"error": str(e)}

    def _nikto(self, target: str, options: dict) -> dict:
        if not shutil.which("nikto"):
            return {"error": "nikto non installé"}
        port = options.get("port", 80)
        try:
            cmd = ["nikto", "-h", target, "-p", str(port), "-Format", "json", "-output", "/dev/stdout"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return {"output": proc.stdout, "stderr": proc.stderr}
        except Exception as e:
            return {"error": str(e)}

    def _sslyze(self, target: str) -> dict:
        try:
            import sslyze
            from sslyze import Scanner, ServerScanRequest, ServerNetworkLocation
            from sslyze.plugins.scan_commands import ScanCommand

            location = ServerNetworkLocation(target, 443)
            request = ServerScanRequest(
                server_location=location,
                scan_commands={ScanCommand.CERTIFICATE_INFO, ScanCommand.SSL_2_0_CIPHER_SUITES, ScanCommand.TLS_1_3_CIPHER_SUITES},
            )
            scanner = Scanner()
            scanner.queue_scans([request])
            for result in scanner.get_results():
                return {"scan_result": str(result)}
        except ImportError:
            return {"error": "sslyze non installé"}
        except Exception as e:
            return {"error": str(e)}
