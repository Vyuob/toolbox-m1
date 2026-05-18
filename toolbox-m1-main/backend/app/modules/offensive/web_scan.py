"""
Module Web/API Scan
--------------------
Intègre :
  - OWASP ZAP (API mode)
  - Dependency-Check (OWASP)
  - SSLyze via module scan
"""

import os
import subprocess
import shutil
import logging
import requests
from typing import Any

logger = logging.getLogger(__name__)


def _web_url(target: str, options: dict | None = None) -> str:
    opts = options or {}
    t = target.strip()
    if not t.startswith(("http://", "https://")):
        scheme = opts.get("scheme", "https")
        host = t.split("/")[0]
        t = f"{scheme}://{host}"
    return t.rstrip("/")


class WebScanModule:
    def run(self, target: str, options: dict) -> dict:
        results: dict[str, Any] = {"target": target}

        if options.get("zap", True):
            results["zap"] = self._zap_scan(target, options)

        if options.get("gobuster", False):
            results["gobuster"] = self._gobuster(target, options)

        if options.get("dep_check", False):
            results["dependency_check"] = self._dependency_check(options.get("project_path", "."))

        return results

    # Profils ZAP Spider → paramètres de /JSON/spider/action/scan/
    _ZAP_SPIDER_PROFILES = {
        "quick":    {"maxChildren": "50",   "recurse": "false"},
        "standard": {"maxChildren": "200",  "recurse": "true"},
        "deep":     {"maxChildren": "1000", "recurse": "true", "subtreeOnly": "false"},
    }

    # Profils ZAP Active → paramètres de /JSON/ascan/action/scan/
    # scanPolicyName doit être une politique existante côté ZAP.
    _ZAP_ACTIVE_PROFILES = {
        "quick":    {"recurse": "false", "scanPolicyName": "XSS-SQLi"},
        "owasp":    {"recurse": "true",  "scanPolicyName": "OWASP-Top10"},
        "full":     {"recurse": "true",  "scanPolicyName": "Default Policy"},
    }

    def _zap_scan(self, target: str, options: dict) -> dict:
        zap_url   = options.get("zap_url", "http://localhost:8080")
        zap_key   = options.get("zap_api_key", "")
        scan_type = options.get("scan_type", "spider")

        if scan_type == "spider":
            endpoint = f"{zap_url}/JSON/spider/action/scan/"
            profile_key = options.get("zap_spider_profile", "standard")
            profile_params = self._ZAP_SPIDER_PROFILES.get(
                profile_key, self._ZAP_SPIDER_PROFILES["standard"]
            )
        elif scan_type == "active":
            endpoint = f"{zap_url}/JSON/ascan/action/scan/"
            profile_key = options.get("zap_active_profile", "owasp")
            profile_params = self._ZAP_ACTIVE_PROFILES.get(
                profile_key, self._ZAP_ACTIVE_PROFILES["owasp"]
            )
        else:
            return {"error": f"Type de scan ZAP inconnu : {scan_type}"}

        params = {"apikey": zap_key, "url": target, **profile_params}

        try:
            r = requests.get(endpoint, params=params, timeout=10)
            r.raise_for_status()
            scan_id = r.json().get("scan")
            status_path = "spider" if scan_type == "spider" else "ascan"
            pretty_params = " ".join(f"{k}={v}" for k, v in profile_params.items())
            output = (
                f"$ curl -s '{endpoint}?url={target}&{pretty_params}'\n"
                f"[+] Scan ZAP {scan_type} ({profile_key}) démarré → scan_id = {scan_id}\n"
                f"[+] Suivre la progression : {zap_url}/JSON/{status_path}/view/status/?scanId={scan_id}"
            )
            return {
                "command": f"GET {endpoint}?url={target}&{pretty_params}",
                "profile": profile_key,
                "output": output,
                "scan_id": scan_id,
                "type": scan_type,
            }
        except requests.RequestException as e:
            return {"error": f"ZAP non disponible : {e}"}

    _GOBUSTER_PROFILES = {
        "quick": {
            "wordlist": "/usr/share/wordlists/dirb/common.txt",
            "threads": 10,
            "extra": "-q --no-error",
            "desc": "Wordlist courte (dirb/common) — scan rapide",
        },
        "standard": {
            "wordlist": "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt",
            "threads": 20,
            "extra": "-q --no-error",
            "desc": "Liste dirbuster small — équilibre vitesse/couverture",
        },
        "full": {
            "wordlist": "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
            "threads": 30,
            "extra": "-q --no-error",
            "desc": "Liste dirbuster medium — plus exhaustif (long)",
        },
    }

    def _gobuster(self, target: str, options: dict) -> dict:
        if not shutil.which("gobuster"):
            return {"error": "gobuster non installé"}

        url = _web_url(target, options)
        profile_key = options.get("gobuster_profile", "standard")
        profile = self._GOBUSTER_PROFILES.get(
            profile_key, self._GOBUSTER_PROFILES["standard"]
        )
        wordlist = options.get("gobuster_wordlist") or profile["wordlist"]
        threads = int(options.get("gobuster_threads") or profile["threads"])
        extensions = (options.get("gobuster_extensions") or "").strip()

        if not os.path.isfile(wordlist):
            return {"error": f"Wordlist introuvable : {wordlist}"}

        try:
            cmd = [
                "gobuster", "dir",
                "-u", url,
                "-w", wordlist,
                "-t", str(threads),
            ]
            if extensions:
                cmd.extend(["-x", extensions])
            cmd.extend(profile["extra"].split())

            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            output = (proc.stdout or "") + (proc.stderr or "")
            found = [
                ln.strip() for ln in output.splitlines()
                if ln.strip() and not ln.startswith("=") and "Progress" not in ln
            ]
            return {
                "command": " ".join(cmd),
                "url": url,
                "profile": profile_key,
                "wordlist": wordlist,
                "paths_found": len(found),
                "output": output.strip() or "(aucun chemin trouvé)",
            }
        except subprocess.TimeoutExpired:
            return {"error": "Timeout gobuster (600s)"}
        except Exception as e:
            return {"error": str(e)}

    def _dependency_check(self, project_path: str) -> dict:
        dc_bin = shutil.which("dependency-check") or shutil.which("dependency-check.sh")
        if not dc_bin:
            return {"error": "dependency-check non installé"}
        try:
            cmd = [dc_bin, "--project", "pentest", "--scan", project_path,
                   "--format", "HTML", "--out", "/tmp/depcheck"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            return {
                "command": " ".join(cmd),
                "output": proc.stdout,
                "stderr": proc.stderr,
            }
        except Exception as e:
            return {"error": str(e)}
