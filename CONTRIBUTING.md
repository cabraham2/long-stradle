# Guide de Contribution

Merci de votre intérêt pour contribuer à Options Pricer ! 🎉

## 🚀 Comment contribuer

### 1. Fork et Clone
```bash
git clone https://github.com/cabraham2/strangle.git
cd strangle
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Créer une branche
```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
```

### 4. Faire vos modifications
- Suivez le style de code existant
- Ajoutez des docstrings pour les nouvelles fonctions
- Testez vos modifications

### 5. Committer
```bash
git add .
git commit -m "feat: description de la fonctionnalité"
```

Convention de commit :
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage
- `refactor:` Refactorisation
- `test:` Tests
- `chore:` Maintenance

### 6. Push et Pull Request
```bash
git push origin feature/ma-nouvelle-fonctionnalite
```

Créez une Pull Request sur GitHub avec une description claire.

## 📋 Idées de Contributions

### Nouvelles Stratégies
- Long Strangle
- Iron Condor
- Butterfly
- Calendar Spread

### Modèles de Pricing
- Modèle binomial
- Monte Carlo
- Volatilité implicite (Newton-Raphson)

### Fonctionnalités Interface Web
- Authentification utilisateur
- Base de données pour historique
- Export PDF avec graphiques
- WebSocket pour données en temps réel
- Mode clair/sombre toggle

### Analyses Avancées
- Backtesting de stratégies
- Optimisation de portfolio
- VaR (Value at Risk)
- Stress testing

### Sources de Données
- Bloomberg API
- Alpha Vantage
- Interactive Brokers
- Données intraday

## 🎨 Style de Code

### Python
- PEP 8
- Type hints recommandés
- Docstrings Google style

```python
def ma_fonction(param1: str, param2: int) -> float:
    """
    Description courte
    
    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2
        
    Returns:
        Description du retour
    """
    pass
```

### JavaScript
- ES6+
- CamelCase pour les fonctions
- Commentaires JSDoc

```javascript
/**
 * Description de la fonction
 * @param {string} param1 - Description
 * @returns {number} Description du retour
 */
function maFonction(param1) {
    // ...
}
```

### CSS
- BEM naming convention
- Variables CSS pour les couleurs
- Mobile-first

## 🧪 Tests

Avant de soumettre :
```bash
# Tester l'import des modules
python -c "from src.strategies.long_straddle import LongStraddle"

# Lancer la démo
python demo.py

# Vérifier l'interface terminal
python main.py --demo

# Tester l'interface web
python web_app.py
```

## 📝 Documentation

- Mettez à jour le README.md si nécessaire
- Ajoutez des exemples d'utilisation
- Documentez les nouvelles API

## 🐛 Rapporter un Bug

Utilisez les Issues GitHub avec :
- Description claire du problème
- Steps to reproduce
- Comportement attendu vs actuel
- Environnement (OS, Python version)
- Stack trace si applicable

## 💡 Proposer une Fonctionnalité

Ouvrez une Issue avec :
- Description de la fonctionnalité
- Cas d'usage
- Mockups si applicable (UI)
- Impact sur l'architecture

## ⚖️ Licence

En contribuant, vous acceptez que vos contributions soient sous licence MIT.

## 🤝 Code de Conduite

- Soyez respectueux
- Accueillez la diversité
- Concentrez-vous sur ce qui est meilleur pour la communauté

## 📞 Questions ?

Ouvrez une Discussion GitHub ou contactez les mainteneurs.

Merci pour votre contribution ! 🙏
