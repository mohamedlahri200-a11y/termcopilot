import subprocess
import shlex

# Commandes/préfixes toujours interdits, même avec confirmation
BLACKLIST = [
    "rm -rf /",
    "mkfs",
    "dd if=",
    ":(){ :|:& };:",  # fork bomb
    "> /dev/sda",
    "shutdown",
    "reboot",
    "init 0",
    "chmod -R 777 /",
]

# Commandes en lecture seule, exécutables sans confirmation
SAFE_READONLY_PREFIXES = [
    "ls", "cat", "df", "free", "ps", "top", "systemctl status",
    "journalctl", "netstat", "ss", "who", "whoami", "uptime",
    "du", "find", "grep", "head", "tail", "ping", "ping6",
    "chronyc", "ufw status",
]


def is_blacklisted(command: str) -> bool:
    return any(bad in command for bad in BLACKLIST)


def is_safe_readonly(command: str) -> bool:
    return any(command.strip().startswith(prefix) for prefix in SAFE_READONLY_PREFIXES)


def execute_command(command: str, force_confirm: bool = True) -> dict:
    """
    Exécute une commande de façon sécurisée.
    Retourne un dict avec le statut et la sortie.
    """
    if is_blacklisted(command):
        return {
            "executed": False,
            "reason": "Commande interdite (blacklist de sécurité)",
            "output": None,
        }

    needs_confirmation = force_confirm and not is_safe_readonly(command)

    if needs_confirmation:
        print(f"\n⚠️  Commande proposée : {command}")
        confirm = input("Confirmer l'exécution ? (o/N) : ").strip().lower()
        if confirm != "o":
            return {
                "executed": False,
                "reason": "Annulé par l'utilisateur",
                "output": None,
            }

    try:
        result = subprocess.run(
            shlex.split(command),
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "executed": True,
            "reason": "OK",
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode,
        }
    except Exception as e:
        return {"executed": False, "reason": str(e), "output": None}


if __name__ == "__main__":
    # Petit test manuel
    test_cmd = "ls -la"
    result = execute_command(test_cmd, force_confirm=True)
    print(result)
