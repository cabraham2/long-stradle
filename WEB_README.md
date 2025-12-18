# Interface Web - Options Pricer

## 🌐 Vue d'ensemble

L'interface web offre une expérience interactive complète pour analyser les stratégies Long Straddle avec de nombreuses fonctionnalités avancées.

## ✨ Fonctionnalités

### 📊 Analyse de Base
- **Validation de ticker en temps réel**
- **Informations détaillées du sous-jacent**
  - Prix actuel avec variation colorée (vert/rouge)
  - Capitalisation boursière
  - Volume de trading
  - Range journalier et 52 semaines
- **Configuration du straddle**
  - Échéance personnalisable
  - Strike ATM ou personnalisé
- **Résultats détaillés**
  - Prix du call et put
  - Coût total de la stratégie
  - Greeks complets
  - Break-even points
  - Graphique interactif profit/perte

### 🔬 Analyses Avancées

#### Analyse de Volatilité
- **Volatilité historique** sur différentes périodes (30j, 60j, 90j, 180j, 252j)
- **Sensibilité à la volatilité** : impact sur le prix du straddle
- Graphiques bar et line interactifs

#### Analyse de Sensibilité (Greeks)
- **Sensibilité au prix spot** : Delta et Gamma
- **Décroissance temporelle** : Theta sur la durée de vie
- **Dual-axis charts** pour comparer plusieurs métriques

#### Heatmap de Profit
- Visualisation 2D : **Échéance vs Variation de Prix**
- Identification rapide des zones de profit
- Multiple lignes pour différentes échéances

### ⚖️ Comparateur de Stratégies
- **Comparaison automatique** de 15 configurations
- Variables :
  - 5 échéances (7, 14, 30, 60, 90 jours)
  - 3 strikes (ATM, +5%, -5%)
- **Tableau comparatif** avec métriques clés
- **Graphique de coûts** groupé par échéance

### 💾 Actions et Export
- **Export JSON** : sauvegarde complète de l'analyse
- **Impression** : rapport formaté pour impression
- **Partage** : utilisation de l'API Web Share
- **Historique** : stockage des analyses récentes

## 🎨 Design

### Thème Sombre Moderne
- Palette de couleurs professionnelle
- Dégradés subtils pour les accents
- Effets de survol et transitions fluides

### Composants
- **Cards** avec bordures et ombres
- **Tables** responsives avec hover effects
- **Graphiques** Chart.js avec thème personnalisé
- **Badges** colorés pour les statuts

### Responsive Design
- Adaptation automatique mobile/tablet/desktop
- Grids flexibles
- Navigation par onglets optimisée

## 🚀 Utilisation

### Démarrer le serveur
```bash
python web_app.py
```

Le serveur démarre sur `http://127.0.0.1:5003`

### Workflow typique

1. **Entrer un ticker** (ex: AAPL)
2. **Valider** pour charger les données de marché
3. **Configurer** l'échéance et le strike
4. **Calculer** pour obtenir les résultats

5. **Onglet Analyses Avancées** :
   - Cliquer sur "Charger l'analyse" pour la volatilité
   - Explorer les différents graphiques de sensibilité
   - Générer la heatmap

6. **Onglet Comparaison** :
   - Cliquer sur "Générer la Comparaison"
   - Analyser le tableau et les graphiques

7. **Exporter** les résultats en JSON

## 📡 API Endpoints

### POST `/api/validate_ticker`
Valide un ticker et retourne les informations

**Request:**
```json
{
  "ticker": "AAPL"
}
```

**Response:**
```json
{
  "valid": true,
  "ticker_info": {
    "ticker": "AAPL",
    "name": "Apple Inc.",
    "current_price": 180.45,
    "day_change": 2.34,
    "day_change_pct": 1.31,
    "market_cap_str": "$2.85T",
    ...
  }
}
```

### POST `/api/calculate_straddle`
Calcule le pricing du straddle

**Request:**
```json
{
  "ticker": "AAPL",
  "days": 30,
  "strike": null
}
```

**Response:**
```json
{
  "success": true,
  "summary": {
    "call_price": 5.23,
    "put_price": 4.87,
    "total_cost": 10.10,
    "greeks": {...},
    ...
  },
  "scenarios": [...]
}
```

### POST `/api/compare_strategies`
Compare différentes configurations

**Response:**
```json
{
  "success": true,
  "comparisons": [
    {
      "days": 30,
      "strike": 180.45,
      "strike_type": "ATM",
      "cost": 10.10,
      "break_even_move": 5.6,
      "theta": -0.034,
      "vega": 0.123
    },
    ...
  ]
}
```

### POST `/api/greeks_sensitivity`
Analyse de sensibilité des Greeks

**Response:**
```json
{
  "success": true,
  "volatility_sensitivity": [...],
  "time_sensitivity": [...],
  "spot_sensitivity": [...]
}
```

### POST `/api/heatmap_data`
Données pour la heatmap de profit

**Response:**
```json
{
  "success": true,
  "heatmap": [[...], [...]],
  "days_range": [7, 14, 30, 60, 90],
  "price_changes": [-30, -25, ..., 30]
}
```

### POST `/api/implied_volatility`
Volatilité historique sur différentes périodes

**Response:**
```json
{
  "success": true,
  "volatility_data": [
    {
      "period": 30,
      "period_label": "30d",
      "volatility": 25.34
    },
    ...
  ]
}
```

### POST `/api/export_json`
Exporte et sauvegarde l'analyse

### GET `/api/history`
Récupère l'historique des analyses

## 🎯 Graphiques Disponibles

1. **Profit & Perte** : Line chart avec zones colorées
2. **Volatilité Historique** : Bar chart
3. **Sensibilité à la Volatilité** : Line chart avec fill
4. **Sensibilité au Spot** : Dual-axis line chart (Prix + Delta)
5. **Décroissance Temporelle** : Line chart Theta
6. **Heatmap de Profit** : Multi-line chart
7. **Comparaison de Coûts** : Grouped bar chart

## 🔧 Technologies

- **Backend** : Flask (Python)
- **Frontend** : Vanilla JavaScript
- **Graphiques** : Chart.js
- **Styling** : CSS3 (custom)
- **Fonts** : Inter (Google Fonts)

## 📱 Compatibilité

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## ⚡ Performance

- **Chargement paresseux** des analyses avancées
- **Overlay de chargement** pour feedback utilisateur
- **Destruction des graphiques** avant recréation (pas de memory leak)
- **Données en cache** pour éviter les requêtes répétées

## 🎨 Personnalisation

### Couleurs
Modifiez les variables CSS dans `static/styles.css` :
```css
:root {
    --primary-color: #3b82f6;
    --secondary-color: #8b5cf6;
    --success-color: #10b981;
    --danger-color: #ef4444;
    ...
}
```

### Graphiques
Thème Chart.js dans `static/script.js` :
```javascript
const chartTheme = {
    textColor: '#f1f5f9',
    gridColor: 'rgba(51, 65, 85, 0.5)',
    ...
};
```

## 🐛 Debug

Activer le mode debug Flask :
```python
app.run(debug=True, host='0.0.0.0', port=5003)
```

Ouvrir la console du navigateur (F12) pour les logs JavaScript.

## 📈 Améliorations Futures

- [ ] Authentification utilisateur
- [ ] Base de données pour persistance
- [ ] Export PDF avec graphiques
- [ ] Comparaison entre tickers
- [ ] Alertes en temps réel
- [ ] Mode clair/sombre toggle
- [ ] Internationalisation (i18n)
- [ ] WebSocket pour données live

## 📝 Notes

- Les données de marché sont récupérées via Yahoo Finance
- La volatilité utilisée est historique, pas implicite
- Les calculs sont basés sur le modèle Black-Scholes
- Pas de coûts de transaction inclus
