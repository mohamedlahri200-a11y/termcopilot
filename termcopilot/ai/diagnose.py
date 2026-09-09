import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """Tu es TermCopilot, un agent IA expert en administration système Linux.
Tu reçois des données de diagnostic (métriques système, logs d'erreurs, services en échec).

Ta réponse doit être un JSON strict avec cette structure exacte, sans texte avant/après :
{
  "diagnostic": "résumé clair du problème détecté (ou 'Aucun problème détecté')",
  "gravite": "faible|moyenne|critique",
  "causes_possibles": ["cause 1", "cause 2"],
  "actions_recommandees": [
    {"commande": "commande bash exacte", "description": "ce que fait la commande", "dangereuse": true/false}
  ]
}

Marque "dangereuse": true pour toute commande qui modifie, supprime, redémarre ou arrête quelque chose.
Marque "dangereuse": false uniquement pour les commandes de lecture seule (diagnostic).
Limite-toi à 6 actions recommandées maximum.
"""

MAX_PAYLOAD_CHARS = 6000


def diagnose_system(diagnostic_bundle):
    """Envoie les données système à Groq et récupère un diagnostic structuré."""
    payload = json.dumps(diagnostic_bundle, indent=2, default=str)
    if len(payload) > MAX_PAYLOAD_CHARS:
        payload = payload[:MAX_PAYLOAD_CHARS] + "\n... (tronqué)"

    user_message = f"""Voici les données de diagnostic système :

{payload}

Analyse ces données et fournis ton diagnostic au format JSON demandé."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        max_tokens=1200,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    text = response.choices[0].message.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "diagnostic": "Erreur de parsing de la réponse IA",
            "gravite": "inconnue",
            "causes_possibles": [],
            "actions_recommandees": [],
            "raw_response": text,
        }


if __name__ == "__main__":
    from termcopilot.collector.logs import get_diagnostic_bundle

    bundle = get_diagnostic_bundle()
    result = diagnose_system(bundle)
    print(json.dumps(result, indent=2, ensure_ascii=False))
