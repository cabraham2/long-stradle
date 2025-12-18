# 📁 Exemples et Démonstrations

Ce dossier contient des fichiers de démonstration et des exemples d'utilisation du priceur d'options.

## 📝 Fichiers

### `demo.py`
Démonstration complète des fonctionnalités de base :
- Création de straddles avec paramètres manuels
- Utilisation de données de marché en temps réel
- Calcul des Greeks
- Analyse de scénarios

**Lancer :**
```bash
python examples/demo.py
```

### `demo_advanced.py`
Exemples avancés incluant :
- Simulations Monte Carlo
- Backtesting sur données historiques
- Comparaison de stratégies multiples
- Analyses de sensibilité complexes

**Lancer :**
```bash
python examples/demo_advanced.py
```

### `test_features.py`
Tests unitaires et validation des fonctionnalités :
- Vérification des calculs Black-Scholes
- Tests des Greeks
- Validation des stratégies

**Lancer :**
```bash
python examples/test_features.py
```

## 📊 Fichiers JSON

Les fichiers `straddle_analysis_*.json` contiennent des résultats d'analyses sauvegardées pour référence.

## 💡 Utilisation Recommandée

Pour une utilisation normale du projet, privilégiez :
- **Interface Web** : `python web_app.py` (recommandé)
- **Interface Terminal** : `python main.py`

Ces fichiers sont uniquement à titre d'exemple et de référence.
