import subprocess
import json


def get_recent_logs(minutes=10, priority="err", max_lines=15):
    """
    Récupère les logs système récents via journalctl (limité en nombre de lignes).
    priority: emerg, alert, crit, err, warning, notice, info, debug
    """
    try:
        result = subprocess.run(
            [
                "journalctl",
                f"--since=-{minutes}min",
                "-p", priority,
                "--no-pager",
                "-o", "short-iso",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        return lines[-max_lines:]
    except FileNotFoundError:
        return ["journalctl non disponible sur ce système"]
    except Exception as e:
        return [f"Erreur lors de la récupération des logs: {e}"]


def get_failed_services():
    """Liste les services systemd qui ont échoué."""
    try:
        result = subprocess.run(
            ["systemctl", "--failed", "--no-pager", "--no-legend"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception as e:
        return [f"Erreur: {e}"]


def get_diagnostic_bundle():
    """Rassemble toutes les infos de diagnostic en un seul objet, limité en taille."""
    from termcopilot.collector.metrics import get_system_metrics

    return {
        "metrics": get_system_metrics(),
        "recent_error_logs": get_recent_logs(minutes=10, priority="err", max_lines=15),
        "failed_services": get_failed_services()[:10],
    }


if __name__ == "__main__":
    print(json.dumps(get_diagnostic_bundle(), indent=2, default=str))
