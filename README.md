# 📊 Options Pricer - Long Straddle
### Projet de Pricing d'Options | Master 2 Gestion d'actifs (G2C)

Un système professionnel de pricing d'options avec interface web moderne, développé en Python pour l'analyse de stratégies d'options basées sur le modèle Black-Scholes.

---

## 👤 Auteur

**Clément Abraham**
- 🎓 Master 2 Gestion d'actifs (G2C)
- 💼 [LinkedIn](https://www.linkedin.com/in/clément-abraham-530566164)
- 🔗 [Projet GitHub](https://github.com/cabraham2/long-stradle)

---

## 📋 Contexte du Projet

Ce projet a été réalisé dans le cadre du Master 2 G2C, avec pour objectifs :
- **Objectif pédagogique** : Implémenter un modèle de pricing d'options (choix entre VBA et Python)
- **Thème** : Étude et calcul du **Long Straddle**, une stratégie d'options neutre au marché
- **Livrables** : 
  - Explication théorique du Long Straddle
  - Implémentation d'un priceur fonctionnel
  - Interface utilisateur pour faciliter l'analyse

### Qu'est-ce qu'un Long Straddle ?

Le **Long Straddle** est une stratégie d'options qui consiste à acheter simultanément un call et un put **au même strike** (généralement ATM - At The Money) et **à la même échéance**. 

**Caractéristiques :**
- ✅ **Position neutre** : Profit en cas de forte volatilité, quelle que soit la direction
- 📈 **Profit illimité** : Gains potentiels si le sous-jacent bouge fortement
- 📉 **Perte limitée** : Perte maximale = prime du call + prime du put
- 🎯 **Utilisation** : Anticipation d'un mouvement important (ex: annonce de résultats)

---

## ✨ Fonctionnalités Principales

### 🌐 **Interface Web (Accès Principal)**
L'interface web est la fonctionnalité phare du projet, offrant une expérience utilisateur complète :

#### **1. Analyse de Base**
- 🔍 **Validation en temps réel** des tickers Yahoo Finance
- 📊 **Informations détaillées** du sous-jacent (prix, capitalisation, volume, secteur)
- 💰 **Calcul instantané** du coût du straddle
- 📈 **Graphique interactif** profit/perte à l'échéance
- 🎯 **Points de break-even** automatiques
- 📋 **Greeks complets** (Delta, Gamma, Vega, Theta, Rho)

#### **2. Analyses Avancées**
- 📊 **Volatilité historique** sur plusieurs périodes (30, 60, 90 jours)
- 🔄 **Sensibilité à la volatilité** (impact sur le prix)
- 📉 **Décroissance temporelle** (Theta decay)
- 🗺️ **Heatmap de profit** (prix vs temps)
- 🎲 **Simulation Monte Carlo** (distribution des profits futurs)
- 📊 **Sensibilité au spot** (delta et gamma)

#### **3. Comparateur de Stratégies**
- ⚖️ **Comparaison** entre Long Straddle, Long Strangle, Iron Condor
- 📊 **15 configurations** testées automatiquement
- 💵 **Analyse coût/bénéfice** de chaque stratégie

#### **4. Fonctionnalités Additionnelles**
- 💾 **Export JSON** des analyses
- 🖨️ **Impression** des résultats
- 📤 **Partage** (Web Share API)
- 📜 **Historique** des analyses
- 📱 **Design responsive** (mobile-friendly)

### 🖥️ **Interface Terminal**
- Interface en ligne de commande avec affichage coloré
- Mode interactif guidé pas à pas
- Sauvegarde des analyses en JSON
- Tableau de scénarios de profit/perte

### 🔧 **Fonctionnalités Techniques**
- ⚡ **Données en temps réel** via Yahoo Finance API
- 📐 **Modèle Black-Scholes** pour le pricing
- 🎲 **Simulations Monte Carlo** pour projections stochastiques
- 📊 **Backtesting** sur données historiques
- 🧮 **Calcul exact des Greeks** (dérivées partielles)

---

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation et Lancement

**Option 1 : Script de démarrage automatique (Recommandé)**

```bash
# Rendre le script exécutable
chmod +x start.sh

# Lancer l'application
./start.sh
```

Le script `start.sh` gère automatiquement :
- ✅ Vérification de Python
- 📦 Création de l'environnement virtuel (si nécessaire)
- 📥 Installation des dépendances
- 🎯 Menu interactif pour choisir l'interface

**Option 2 : Installation manuelle**

```bash
# 1. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'interface web (recommandé)
python web_app.py

# Ou lancer l'interface terminal
python main.py
```

### Accès à l'Application

Une fois lancée, l'**interface web** est accessible à : **http://127.0.0.1:5003**

---

## 💡 Recommandation : Utiliser l'Interface Web

> **🌟 Pour la meilleure expérience, lancez l'interface web !**
> 
> L'interface web est la version **la plus aboutie et la mieux développée** du projet. Elle offre :
> - 📊 Des **graphiques interactifs** pour visualiser les profits/pertes
> - 🎨 Une **interface moderne** et intuitive
> - 📈 Des **analyses avancées** (Monte Carlo, heatmaps, sensibilités)
> - 🔄 Un **comparateur de stratégies** complet
> - 💾 Des **fonctionnalités d'export** et de partage
> 
> **Comment lancer ?**
> ```bash
> ./start.sh
> ```
> Puis sélectionnez l'option **2 - Interface Web**
> 
> ### 🛠️ Que fait le script `start.sh` ?
> 
> Le script `start.sh` automatise toute la configuration du projet :
> 1. ✅ **Vérifie** que Python 3 est installé sur votre système
> 2. 📦 **Crée** un environnement virtuel (dossier `venv/`) s'il n'existe pas déjà
> 3. 🔄 **Active** automatiquement l'environnement virtuel
> 4. 📥 **Installe** toutes les dépendances nécessaires depuis `requirements.txt`
> 5. 🎯 **Affiche un menu** interactif vous permettant de choisir :
>    - Interface Terminal (analyse en ligne de commande)
>    - **Interface Web** (serveur Flask avec interface graphique)
>    - Démonstration rapide
>    - Mode démo
> 
> C'est la **méthode la plus simple** pour démarrer le projet : une seule commande et tout est configuré !

---

## 📁 Architecture et Organisation des Fichiers

### **Structure du Projet**

```
strangle/
│
├── 🚀 FICHIERS PRINCIPAUX
│   ├── web_app.py              # ⭐ Application web Flask (INTERFACE PRINCIPALE)
│   ├── main.py                 # Interface terminal interactive
│   ├── start.sh                # Script de lancement automatique
│   └── requirements.txt        # Dépendances Python
│
├── 📦 SOURCE CODE (src/)
│   ├── models/
│   │   └── black_scholes.py    # Classes Call, Put et calcul Black-Scholes
│   ├── strategies/
│   │   ├── long_straddle.py    # Stratégie Long Straddle
│   │   ├── long_strangle.py    # Stratégie Long Strangle
│   │   └── iron_condor.py      # Stratégie Iron Condor
│   └── utils/
│       ├── market_data.py      # API Yahoo Finance (récupération données)
│       ├── math_utils.py       # Fonctions mathématiques (CDF normale, etc.)
│       ├── display.py          # Affichage terminal coloré
│       ├── monte_carlo.py      # Simulations Monte Carlo
│       └── backtesting.py      # Tests sur données historiques
│
├── 🌐 INTERFACE WEB (web/)
│   ├── templates/
│   │   └── index.html          # Template HTML principal
│   └── static/
│       ├── styles.css          # Styles CSS (thème moderne)
│       ├── script.js           # JavaScript (graphiques, API calls)
│       └── glossary.json       # Définitions termes financiers
│
├── 📊 EXEMPLES ET DEMOS (examples/)
│   ├── demo.py                 # Démonstration des fonctionnalités
│   ├── demo_advanced.py        # Exemples avancés
│   └── test_features.py        # Tests de fonctionnalités
│
├── 💾 OUTPUTS (output/)
│   └── scenarios_*.csv         # Résultats d'analyses exportées
│
└── 📚 DOCUMENTATION
    ├── README.md               # Ce fichier
    ├── README_FEATURES.md      # Détails des fonctionnalités
    ├── WEB_README.md           # Documentation interface web
    ├── CONTRIBUTING.md         # Guide de contribution
    └── CHANGELOG.md            # Historique des modifications
```

### **Description des Fichiers Clés**

| Fichier | Rôle | Usage |
|---------|------|-------|
| `web_app.py` | **Point d'entrée principal** - Serveur Flask avec toutes les routes API | `python web_app.py` |
| `main.py` | Interface en ligne de commande pour analyses rapides | `python main.py` |
| `start.sh` | Script de démarrage automatisé (setup + lancement) | `./start.sh` |
| `black_scholes.py` | Modèle de pricing Black-Scholes (Call, Put, Greeks) | Importé par les stratégies |
| `long_straddle.py` | Logique métier du Long Straddle | Core du projet |
| `market_data.py` | Connexion à Yahoo Finance pour données temps réel | Utilisé par toutes les analyses |
| `monte_carlo.py` | Simulations stochastiques de prix futurs | Analyses avancées |

---

## � Exemples d'Utilisation

### Interface Web (Recommandé)

1. **Lancer l'application** : `./start.sh` → Option 2
2. **Ouvrir** : http://127.0.0.1:5003
3. **Saisir un ticker** : Ex: AAPL, TSLA, MSFT
4. **Analyser** : Consulter les graphiques et métriques
5. **Comparer** : Tester différentes stratégies et configurations

### Utilisation Programmatique

```python
from src.strategies.long_straddle import LongStraddle

# Créer un straddle avec données temps réel
straddle = LongStraddle.from_ticker("AAPL", days_to_expiry=30)

# Obtenir le prix total
price = straddle.price()
print(f"Coût du straddle: ${price:.2f}")

# Calculer les Greeks
greeks = straddle.greeks()
print(f"Delta: {greeks['delta']:.4f}")
print(f"Vega: {greeks['vega']:.4f}")

# Points de break-even
lower_be, upper_be = straddle.break_even_points()
print(f"Break-even: ${lower_be:.2f} - ${upper_be:.2f}")
```

---

## 🎯 Comment Fonctionne le Projet

### 1. **Récupération des Données Marché**
```python
# market_data.py récupère les données via yfinance
ticker_info = get_ticker_info("AAPL")
# → Prix actuel, historique, volatilité implicite
```

### 2. **Calcul Black-Scholes**
```python
# black_scholes.py calcule le prix théorique
call = Call(S=150, K=150, T=0.08, r=0.05, sigma=0.25)
call_price = call.price()  # Formule de Black-Scholes
```

### 3. **Construction du Straddle**
```python
# long_straddle.py combine call + put
straddle_cost = call.price() + put.price()
break_even_up = K + straddle_cost
break_even_down = K - straddle_cost
```

### 4. **Analyse de Sensibilité**
```python
# Calcul des Greeks (dérivées partielles)
delta = ∂V/∂S   # Sensibilité au prix
gamma = ∂²V/∂S² # Accélération du delta
vega = ∂V/∂σ    # Sensibilité à la volatilité
theta = ∂V/∂t   # Décroissance temporelle
```

### 5. **Simulation et Visualisation**
- **Monte Carlo** : Simulation de 10,000 scénarios de prix futurs
- **Graphiques** : Rendering avec Chart.js dans l'interface web
- **Heatmaps** : Profit selon (prix spot × temps restant)

---

## 🛠️ Technologies Utilisées

| Technologie | Usage |
|-------------|-------|
| **Python 3.8+** | Langage principal |
| **Flask** | Framework web backend |
| **NumPy & SciPy** | Calculs numériques (CDF, intégrations) |
| **yfinance** | API données de marché Yahoo Finance |
| **Chart.js** | Graphiques interactifs frontend |
| **Bootstrap** | Design responsive UI |
| **colorama** | Affichage terminal coloré |

---

## � Concepts Financiers

### Le Modèle Black-Scholes

Formules utilisées pour pricer les options européennes :

**Call Option:**
$$C = S_0 N(d_1) - K e^{-rT} N(d_2)$$

**Put Option:**
$$P = K e^{-rT} N(-d_2) - S_0 N(-d_1)$$

Où :
$$d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}$$
$$d_2 = d_1 - \sigma\sqrt{T}$$

- $S_0$ : Prix actuel du sous-jacent
- $K$ : Strike (prix d'exercice)
- $T$ : Temps à échéance (en années)
- $r$ : Taux sans risque
- $\sigma$ : Volatilité implicite
- $N(·)$ : Fonction de répartition normale cumulative

### Les Greeks

| Greek | Formule | Signification |
|-------|---------|---------------|
| **Delta (Δ)** | $\frac{\partial V}{\partial S}$ | Sensibilité au prix du sous-jacent |
| **Gamma (Γ)** | $\frac{\partial^2 V}{\partial S^2}$ | Variation du delta |
| **Vega (ν)** | $\frac{\partial V}{\partial \sigma}$ | Sensibilité à la volatilité |
| **Theta (Θ)** | $\frac{\partial V}{\partial t}$ | Décroissance temporelle (time decay) |
| **Rho (ρ)** | $\frac{\partial V}{\partial r}$ | Sensibilité au taux d'intérêt |

---

## 📈 Cas d'Usage du Long Straddle

### ✅ Quand Utiliser ?
- 📊 **Avant annonces** : Résultats trimestriels, décisions de banques centrales
- 🔀 **Forte volatilité attendue** : Incertitude sur la direction mais mouvement probable
- 🎯 **Événements binaires** : Approbation FDA, élections, fusions

### ❌ Quand Éviter ?
- 💤 **Marchés calmes** : Faible volatilité, pas de catalyseurs
- 💸 **Volatilité implicite élevée** : Options déjà chères (prime élevée)
- ⏰ **Échéances longues** : Theta decay important sur la durée

---

## 🎓 Aspects Académiques

### Travail Réalisé
Ce projet répond aux exigences du Master 2 G2C :

1. ✅ **Implémentation mathématique rigoureuse** du modèle Black-Scholes
2. ✅ **Calcul exact des Greeks** (dérivées analytiques)
3. ✅ **Validation empirique** avec données de marché réelles
4. ✅ **Interface utilisateur** pour faciliter l'analyse
5. ✅ **Documentation complète** du code et des concepts

### Références Théoriques
- Black, F., & Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities"
- Hull, J. C. (2018). "Options, Futures, and Other Derivatives"
- Wilmott, P. (2006). "Paul Wilmott on Quantitative Finance"

---

## 🤝 Contribution

Les contributions sont bienvenues ! Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour les guidelines.

---

## 📝 Licence

Ce projet est réalisé dans un cadre académique (Master 2 G2C).

---

## 📞 Contact

**Clément ABRAHAM**
- 💼 LinkedIn : [Clément Abraham](https://www.linkedin.com/in/clément-abraham-530566164)
- 🐙 GitHub : [cabraham2](https://github.com/cabraham2)

---

## 🎉 Remerciements

Merci au corps professoral du Master 2 G2C pour l'encadrement de ce projet et les enseignements en finance quantitative.

---

<div align="center">
  
**⭐ Si ce projet vous a aidé, n'hésitez pas à laisser une étoile sur GitHub ! ⭐**

</div>
