import psutil
import json
from datetime import datetime


def get_system_metrics():
    """Récupère les métriques système actuelles."""
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "percent": psutil.virtual_memory().percent,
            "used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
            "total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        },
        "disk": {
            "percent": psutil.disk_usage("/").percent,
            "used_gb": round(psutil.disk_usage("/").used / (1024**3), 2),
            "total_gb": round(psutil.disk_usage("/").total / (1024**3), 2),
        },
        "top_processes": get_top_processes(),
    }


def get_top_processes(limit=5):
    """Retourne les processus les plus gourmands en CPU."""
    processes = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    processes.sort(key=lambda p: p["cpu_percent"] or 0, reverse=True)
    return processes[:limit]


if __name__ == "__main__":
    print(json.dumps(get_system_metrics(), indent=2))
