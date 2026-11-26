# TD11 - Dashboard Dash : répartition du travail

Équipe g03-T19, travail réparti entre 3 élèves. Référence : `labs/TD11_DASH_DASHBOARD.md`.

## Objectif

Créer `src/dashboard.py`, qui affiche le résultat de `build_market_snapshot()`. Le dashboard ne fait que de la présentation.

## Répartition

| Rôle | Nom | Mission | Parties du TD | Branche | Relit la PR de |
|---|---|---|---|---|---|
| Élève 1 : base et intégration | à compléter | Dépendances, squelette, assemblage, contrôles finaux | 3 à 6, 10 à 13 | `feature/dash-dashboard` | Élève 2 |
| Élève 2 : informations | à compléter | Contexte et trois performances | 7 et 8 | `feature/dash-indicators` | Élève 3 |
| Élève 3 : graphique | à compléter | Graphique base 100 et capture | 9 | `feature/dash-chart` | Élève 1 |

## Ordre de travail

1. L'élève 1 crée la base, ouvre sa PR et la merge après relecture.
2. Les élèves 2 et 3 partent d'un `main` à jour et travaillent en parallèle.
3. Chacun modifie uniquement sa fonction, ce qui limite les conflits.
4. Après les deux merges, l'élève 1 effectue les contrôles finaux.

## Règles communes

- `dashboard.py` n'appelle ni Yahoo ni Bloomberg.
- `dashboard.py` ne calcule ni rendement, ni base 100, ni performance relative.
- Le mode `APPROVED_SAMPLE` reste visible. Ne jamais le présenter comme du Bloomberg LIVE.
- Aucun identifiant ni mot de passe dans Git. Ne pas ajouter `.venv`.
- Si une commande Git affiche une erreur, s'arrêter avant de lancer la suivante.

## Préparation (chaque élève)

Commandes Windows (PowerShell), depuis la racine du dépôt. La première ligne ne sert que si `.venv` n'existe pas encore. Sous Linux ou Codespaces, utiliser `python`.

```powershell
py -m venv .venv
git switch main
git pull
git status
git switch -c NOM_DE_TA_BRANCHE
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Élève 1 : base et intégration

1. Installer les bibliothèques : `.\.venv\Scripts\python.exe -m pip install dash plotly`
2. Ajouter `dash` et `plotly` dans `requirements.txt`, chacun sur sa propre ligne, en conservant `yfinance`.
3. Créer `src/dashboard.py` avec ce squelette :

```python
from dash import Dash, dcc, html
import plotly.graph_objects as go

from main import build_market_snapshot


def build_information(snapshot):
    """Student 2: context and the three performance values."""
    return html.Div("Context and performance: to do")


def build_figure(snapshot):
    """Student 3: base-100 chart."""
    return go.Figure()


snapshot = build_market_snapshot()
app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("MarketPulse"),
        build_information(snapshot),
        dcc.Graph(figure=build_figure(snapshot)),
    ]
)


if __name__ == "__main__":
    app.run(debug=False)
```

4. Tester, puis envoyer :

```powershell
.\.venv\Scripts\python.exe src/dashboard.py
```

Ouvrir http://127.0.0.1:8050/ puis arrêter le serveur avec `Ctrl+C`.

```powershell
git add requirements.txt src/dashboard.py
git commit -m "feat: add MarketPulse Dash dashboard"
git push -u origin feature/dash-dashboard
```

## Élève 2 : informations

Compléter `build_information(snapshot)`, qui retourne un `html.Div` contenant :

| Affichage | Champ du snapshot |
|---|---|
| Source | `provider` |
| Mode | `access_mode` |
| Instrument | `instrument` (`ticker`, `name`) |
| Benchmark | `benchmark` (`ticker`, `name`) |
| Période | `lookback` |
| Intervalle | `interval` |
| Rendement de l'instrument | `instrument_return`, format `+.2f` en % |
| Rendement du benchmark | `benchmark_return`, format `+.2f` en % |
| Performance relative | `relative_performance`, format `+.2f` en points |

```powershell
git add src/dashboard.py
git commit -m "feat: add dashboard indicators"
git push -u origin feature/dash-indicators
```

## Élève 3 : graphique

Compléter `build_figure(snapshot)` :

- une courbe pour `instrument_base_100` et une pour `benchmark_base_100` ;
- `date` en abscisse, `value` en ordonnée ;
- le ticker comme nom de chaque courbe ;
- un titre et des noms d'axes ;
- vérifier que les deux courbes commencent à 100.

```powershell
git add src/dashboard.py
git commit -m "feat: add base-100 chart"
git push -u origin feature/dash-chart
```

Après intégration, faire la capture `02_dash_dashboard.png` montrant le dashboard complet, à conserver pour le Checkpoint C.

## Pull Requests

La cible est toujours le `main` de `Lapoutre772/esilv-marketpulse-g03-T19`, pas le dépôt `plensy`. Chaque PR est relue avant le merge.

## Contrôles finaux (élève 1)

```powershell
git switch main
git pull
.\.venv\Scripts\python.exe src/main.py
.\.venv\Scripts\python.exe src/dashboard.py
```

- [ ] `dash` et `plotly` sont dans `requirements.txt`
- [ ] Source, mode, instrument, benchmark, période et intervalle sont visibles
- [ ] Les trois performances sont visibles
- [ ] Un seul graphique contient les deux courbes base 100
- [ ] Le terminal et le dashboard donnent les mêmes valeurs
- [ ] `dashboard.py` ne contient ni appel fournisseur ni formule
- [ ] Les trois PR ont été relues

## Point ouvert

Le TD11 cite `docs/12_MARKETPULSE_APPLICATION_SNAPSHOT_CONTRACT.md`, absent du dépôt. Le snapshot actuel contient les champs listés dans le TD11, mais sa conformité au document reste à vérifier avec l'enseignant.
