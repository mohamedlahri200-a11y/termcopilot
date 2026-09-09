from termcopilot.collector.metrics import get_system_metrics


def test_metrics_structure():
    metrics = get_system_metrics()
    assert "cpu_percent" in metrics
    assert "memory" in metrics
    assert "disk" in metrics
    assert 0 <= metrics["cpu_percent"] <= 100


def test_metrics_memory_values():
    metrics = get_system_metrics()
    assert metrics["memory"]["used_gb"] <= metrics["memory"]["total_gb"]
