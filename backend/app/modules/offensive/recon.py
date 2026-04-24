"""
Module Reconnaissance
---------------------
Effectue une reconnaissance passive et active sur une cible :
  - Résolution DNS
  - Scan de ports Nmap (détection OS, services, versions)
  - Bannière grabbing
"""

import socket
import subprocess
import shutil
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

_NMAP_FINGERPRINT_RE = re.compile(
    r"\n\d+ services? unrecognized despite returning data\..*?"
    r"(?=\nDevice type:|\nService detection performed|\nNmap done:)",
    re.DOTALL,
)


def _strip_nmap_fingerprints(text: str) -> str:
    """Retire les blocs 'SF-Port...' dumpés par nmap pour les services
    non identifiés — utile en CLI mais illisibles dans un rapport."""
    return _NMAP_FINGERPRINT_RE.sub("", text) if text else text


class ReconModule:
    def run(self, target: str, options: dict) -> dict:
        results: dict[str, Any] = {"target": target, "dns": {}, "nmap": {}, "whois": ""}

        results["dns"] = self._dns_lookup(target)
        results["nmap"] = self._nmap_scan(target, options)

        if options.get("whois", False):
            results["whois"] = self._whois(target)

        return results

    def _dns_lookup(self, target: str) -> dict:
        try:
            ip = socket.gethostbyname(target)
            infos = socket.getaddrinfo(target, None)
            all_ips = sorted({i[4][0] for i in infos})
            lines = [
                f"; Résolution DNS pour {target}",
                f";; ANSWER SECTION:",
                f"{target}.    IN    A    {ip}",
            ]
            for extra in all_ips:
                if extra != ip:
                    lines.append(f"{target}.    IN    A    {extra}")
            return {
                "command": f"resolve {target}",
                "output": "\n".join(lines),
                "resolved_ip": ip,
                "all_ips": all_ips,
            }
        except socket.gaierror as e:
            logger.warning(f"DNS lookup failed for {target}: {e}")
            return {"error": str(e)}

    def _nmap_scan(self, target: str, options: dict) -> dict:
        if not shutil.which("nmap"):
            return {"error": "nmap non installé"}

        args = options.get("nmap_args", "-sV -O -Pn --top-ports 1000")
        try:
            cmd = ["nmap"] + args.split() + [target]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return {
                "command": " ".join(cmd),
                "output": _strip_nmap_fingerprints(proc.stdout),
                "stderr": proc.stderr,
            }
        except subprocess.TimeoutExpired:
            return {"error": "Timeout nmap"}
        except Exception as e:
            return {"error": str(e)}

    def _whois(self, target: str) -> str:
        if not shutil.which("whois"):
            return "whois non installé"

        # Les registries refusent les sous-domaines ("Malformed request").
        # On essaie d'abord tel quel ; si ça échoue, on retombe sur le domaine
        # racine (2 derniers labels — suffit pour .com/.org/.fr/... ; imparfait
        # pour .co.uk mais suffisant pour un usage pédagogique).
        candidates = [target]
        host = target.split("://", 1)[-1].split("/")[0].strip(".")
        labels = host.split(".")
        if len(labels) > 2:
            candidates.append(".".join(labels[-2:]))

        last_output = ""
        for q in candidates:
            try:
                proc = subprocess.run(["whois", q], capture_output=True, text=True, timeout=30)
                out = proc.stdout or ""
                last_output = out
                if "Malformed request" not in out and "No match" not in out.lower():
                    return out
            except Exception as e:
                last_output = str(e)
        return last_output or "whois : aucune donnée"
