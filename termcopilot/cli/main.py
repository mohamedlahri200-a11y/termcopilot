import click
import json
from termcopilot.collector.logs import get_diagnostic_bundle
from termcopilot.ai.diagnose import diagnose_system
from termcopilot.security.validator import execute_command


@click.group()
def cli():
    """TermCopilot — Agent IA pour l'administration système Linux."""
    pass


@cli.command()
def diagnose():
    """Analyse l'état actuel du système et affiche un diagnostic IA."""
    click.echo("🔍 Collecte des données système...")
    bundle = get_diagnostic_bundle()

    click.echo("🤖 Analyse par l'IA en cours...")
    result = diagnose_system(bundle)

    click.echo(f"\n📋 Diagnostic : {result.get('diagnostic')}")
    click.echo(f"🚨 Gravité : {result.get('gravite')}")

    causes = result.get("causes_possibles", [])
    if causes:
        click.echo("\nCauses possibles :")
        for c in causes:
            click.echo(f"  - {c}")

    actions = result.get("actions_recommandees", [])
    if actions:
        click.echo("\nActions recommandées :")
        for i, a in enumerate(actions, 1):
            tag = "⚠️  DANGEREUSE" if a.get("dangereuse") else "✅ sûre"
            click.echo(f"  {i}. [{tag}] {a['commande']} — {a['description']}")

    return result


@cli.command()
def fix():
    """Diagnostique puis propose d'exécuter les correctifs (avec confirmation)."""
    ctx = click.get_current_context()
    result = ctx.invoke(diagnose)
    actions = result.get("actions_recommandees", [])

    if not actions:
        click.echo("\n✅ Aucune action nécessaire.")
        return

    for a in actions:
        outcome = execute_command(a["commande"], force_confirm=True)
        if outcome["executed"]:
            click.echo(f"✅ Exécuté : {a['commande']}")
        else:
            click.echo(f"⏭️  Ignoré : {a['commande']} ({outcome['reason']})")


@cli.command()
@click.option("--interval", default=60, help="Intervalle en secondes entre les vérifications")
def monitor(interval):
    """Surveille le système en continu et alerte en cas de problème."""
    import time

    click.echo(f"👁️  Surveillance active (toutes les {interval}s). Ctrl+C pour arrêter.")
    ctx = click.get_current_context()
    try:
        while True:
            bundle = get_diagnostic_bundle()
            if bundle["failed_services"] or bundle["recent_error_logs"]:
                click.echo("\n🚨 Anomalie détectée, lancement du diagnostic...")
                ctx.invoke(diagnose)
            time.sleep(interval)
    except KeyboardInterrupt:
        click.echo("\n👋 Surveillance arrêtée.")


if __name__ == "__main__":
    cli()
