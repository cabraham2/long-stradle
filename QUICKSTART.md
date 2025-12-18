# 🚀 Guide de Démarrage Rapide

## Préparation

1. **Rendre le script exécutable** :
```bash
chmod +x start.sh
```

2. **Lancer l'application** :
```bash
./start.sh
```

Le script vous proposera :
- Option 1 : Interface Terminal (mode interactif)
- Option 2 : **Interface Web** (⭐ recommandé)
- Option 3 : Démonstration rapide
- Option 4 : Mode démo terminal

## 🌐 Accès à l'Interface Web

Après avoir lancé l'option 2, ouvrez votre navigateur à :
```
http://127.0.0.1:5003
```

## 📝 Que Dire dans Votre Présentation

### Contexte
"J'ai réalisé ce projet dans le cadre de mon Master 2 G2C où nous devions créer un priceur d'options, soit en VBA soit en Python. J'ai choisi Python pour créer une solution complète et professionnelle."

### Objectif
"Le but était d'expliquer et d'implémenter le calcul d'un Long Straddle, une stratégie d'options qui consiste à acheter un call et un put au même strike pour profiter de mouvements importants de prix, peu importe la direction."

### Fonctionnalités Principales
"Le projet comporte trois composantes :

1. **Le modèle de pricing** : Implémentation du modèle Black-Scholes pour calculer le prix théorique des options européennes et tous les Greeks (Delta, Gamma, Vega, Theta, Rho).

2. **L'interface web** (point fort du projet) : Une application Flask moderne qui permet de :
   - Analyser n'importe quelle action via son ticker (AAPL, TSLA, etc.)
   - Visualiser les profits/pertes avec des graphiques interactifs
   - Faire des analyses avancées (Monte Carlo, sensibilité, heatmaps)
   - Comparer différentes stratégies (Straddle, Strangle, Iron Condor)
   - Exporter les résultats

3. **Les données en temps réel** : Le système récupère automatiquement les prix du marché via l'API Yahoo Finance."

### Architecture
"L'architecture est modulaire :
- `src/models/` contient le modèle Black-Scholes
- `src/strategies/` implémente les différentes stratégies
- `src/utils/` gère les données de marché et les calculs
- `web/` contient l'interface utilisateur (HTML, CSS, JS)
- `web_app.py` est le serveur Flask qui orchestre tout"

### Démonstration
"Pour lancer le projet, j'utilise un script shell (`start.sh`) qui automatise tout :
- Vérifie que Python est installé
- Crée l'environnement virtuel
- Installe les dépendances
- Lance l'interface de votre choix

L'interface web est l'accès principal car elle offre la meilleure expérience utilisateur avec tous les graphiques et analyses interactives."

## 🎯 Points Forts à Mentionner

1. **Approche académique rigoureuse** : Formules mathématiques exactes du modèle Black-Scholes
2. **Interface professionnelle** : Interface web moderne et intuitive
3. **Données réelles** : Connexion à Yahoo Finance pour données de marché
4. **Extensible** : Architecture modulaire permettant d'ajouter facilement de nouvelles stratégies
5. **Documentation complète** : README détaillé, exemples de code, documentation technique

## 📧 Partage du Projet

Le projet est disponible sur GitHub :
```
https://github.com/cabraham2/long-stradle
```

Profil LinkedIn :
```
https://www.linkedin.com/in/clément-abraham-530566164
```
