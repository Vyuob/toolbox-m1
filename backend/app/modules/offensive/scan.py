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
            results["sslyze"] = self._sslyze(target, options)

        return results

    def _nmap_vuln(self, target: str, options: dict) -> dict:
        if not shutil.which("nmap"):
            return {"error": "nmap non installé"}
        port = options.get("port", "")
        port_arg = ["-p", str(port)] if port else []
        try:
            cmd = ["nmap", "--script=vuln"] + port_arg + [target]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            return {
                "command": " ".join(cmd),
                "output": proc.stdout,
                "stderr": proc.stderr,
            }
        except subprocess.TimeoutExpired:
            return {"error": "Timeout nmap vuln"}
        except Exception as e:
            return {"error": str(e)}

    # Profils Nikto → options -Tuning (+ évasion) réellement exécutés.
    _NIKTO_PROFILES = {
        "quick":    {"tuning": "x",            "evasion": None},
        "standard": {"tuning": "x6",           "evasion": None},
        "full":     {"tuning": "0123456789abc", "evasion": None},
        "evasion":  {"tuning": "x",            "evasion": "1"},
    }

    def _nikto(self, target: str, options: dict) -> dict:
        if not shutil.which("nikto"):
            return {"error": "nikto non installé"}
        port = options.get("port") or 80
        profile = options.get("nikto_profile", "standard")
        cfg = self._NIKTO_PROFILES.get(profile, self._NIKTO_PROFILES["standard"])
        try:
            cmd = ["nikto", "-h", target, "-p", str(port),
                   "-Tuning", cfg["tuning"], "-nointeractive"]
            if cfg["evasion"]:
                cmd += ["-evasion", cfg["evasion"]]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return {
                "command": " ".join(cmd),
                "profile": profile,
                "output": proc.stdout,
                "stderr": proc.stderr,
            }
        except Exception as e:
            return {"error": str(e)}

    # Profils SSLyze → arguments passés au binaire
    _SSLYZE_PROFILES = {
        "cert":     ["--certinfo"],
        "standard": ["--regular"],
        "full":     ["--regular", "--certinfo", "--reneg", "--resum",
                     "--heartbleed", "--robot"],
    }

    def _sslyze(self, target: str, options: dict | None = None) -> dict:
        """Utilise le binaire sslyze (présent dans l'image Kali) pour produire
        le même rendu qu'en ligne de commande."""
        opts = options or {}
        profile = opts.get("sslyze_profile", "standard")
        args = self._SSLYZE_PROFILES.get(profile, self._SSLYZE_PROFILES["standard"])

        if shutil.which("sslyze"):
            try:
                host = target.split("://", 1)[-1].split("/")[0]
                if ":" not in host:
                    host = f"{host}:443"
                cmd = ["sslyze"] + args + [host]
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
                return {
                    "command": " ".join(cmd),
                    "profile": profile,
                    "output": proc.stdout,
                    "stderr": proc.stderr,
                }
            except subprocess.TimeoutExpired:
                return {"error": "Timeout sslyze"}
            except Exception as e:
                return {"error": str(e)}

        # Fallback : API Python (sortie texte reconstruite)
        try:
            from sslyze import Scanner, ServerNetworkLocation, ServerScanRequest
            from sslyze.plugins.scan_commands import ScanCommand
            location = ServerNetworkLocation(target, 443)
            request = ServerScanRequest(
                server_location=location,
                scan_commands={ScanCommand.CERTIFICATE_INFO, ScanCommand.SSL_2_0_CIPHER_SUITES, ScanCommand.TLS_1_3_CIPHER_SUITES},
            )
            scanner = Scanner()
            scanner.queue_scans([request])
            for result in scanner.get_results():
                return {"output": str(result)}
            return {"error": "sslyze : aucun résultat"}
        except ImportError:
            return {"error": "sslyze non installé"}
        except Exception as e:
            return {"error": str(e)}
