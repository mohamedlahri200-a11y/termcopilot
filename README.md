# TermCopilot 🤖

Agent IA en ligne de commande pour l'administration système Linux — diagnostic automatique des pannes via l'analyse des logs système, correctifs proposés par IA, et exécution sécurisée avec confirmation humaine.

## 🎯 Fonctionnalités

- **Diagnostic automatique** : analyse les logs (`journalctl`), les services en échec (`systemctl --failed`) et les métriques système (CPU, RAM, disque)
- **Analyse par IA** : les données sont envoyées à un LLM (Groq / GPT-OSS) qui identifie la cause du problème et propose des correctifs
- **Exécution sécurisée** : chaque commande proposée est validée par un moteur de sécurité (whitelist/blacklist), avec confirmation humaine obligatoire pour toute action sensible
- **Mode surveillance continue** : `monitor` scrute le système en boucle et déclenche un diagnostic dès qu'une anomalie apparaît
- **Historique complet** : chaque diagnostic est enregistré dans une base SQLite locale, consultable via `history`

## 🏗️ Architecture
## 📁 Structure du projet[200~termcopilot/
├── termcopilot/
│ ├── collector/ # collecte des logs et métriques système
│ ├── ai/ # intégration API IA (diagnostic)
│ ├── security/ # validation et exécution sécurisée des commandes
│ ├── cli/ # interface en ligne de commande (Click)
│ └── storage/ # historique des diagnostics (SQLite)
├── tests/ # tests unitaires + scripts de simulation de panne
├── requirements.txt
└── README.md~
## 🚀 Installation

```bash
git clone https://github.com/mohamedlahri200-a11y/termcopilot.git
cd termcopilot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=ta_cle_ici" > .env
```

## 💻 Utilisation

```bash
python3 -m termcopilot.cli diagnose   # diagnostic ponctuel du système
python3 -m termcopilot.cli fix        # diagnostic + propose et exécute les correctifs (avec confirmation)
python3 -m termcopilot.cli monitor    # surveillance continue en arrière-plan
python3 -m termcopilot.cli history    # consulte l'historique des diagnostics passés
```

## 🎬 Démo (simulation de panne)

```bash
bash tests/simulate_failure.sh    # crée un service qui échoue volontairement
python3 -m termcopilot.cli diagnose   # TermCopilot détecte et diagnostique la panne
bash tests/cleanup.sh             # nettoie l'environnement de test
```

## 🧪 Tests

```bash
pytest tests/ -v
```

## 🔐 Sécurité

- Aucune commande destructrice (`rm -rf /`, `mkfs`, `shutdown`, etc.) n'est jamais exécutable, même avec confirmation (blacklist stricte)
- Les commandes de lecture seule (`ls`, `systemctl status`, `journalctl`, etc.) s'exécutent automatiquement
- Toute commande modifiant l'état du système nécessite une confirmation explicite de l'utilisateur

## 🛠️ Stack technique

- **Python 3** — langage principal
- **Click** — interface CLI
- **psutil** — collecte des métriques système
- **Groq API (GPT-OSS 120B)** — diagnostic intelligent
- **SQLite** — historique et audit

## 👤 Auteur

Mohamed Lahri — Étudiant en Génie Informatique, Génie Logiciel et Intelligence Artificielle
