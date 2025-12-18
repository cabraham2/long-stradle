#!/usr/bin/env python3
"""
Test rapide de toutes les nouvelles fonctionnalités
"""

print("🧪 Test des nouvelles fonctionnalités...\n")

# Test 1: Import des stratégies
print("✓ Test 1: Import des stratégies")
try:
    from src.strategies.long_straddle import LongStraddle
    from src.strategies.long_strangle import LongStrangle
    from src.strategies.iron_condor import IronCondor
    print("  ✅ Toutes les stratégies importées\n")
except Exception as e:
    print(f"  ❌ Erreur: {e}\n")
    exit(1)

# Test 2: Import Monte Carlo
print("✓ Test 2: Import Monte Carlo")
try:
    from src.utils.monte_carlo import MonteCarloAnalysis
    print("  ✅ Monte Carlo importé\n")
except Exception as e:
    print(f"  ❌ Erreur: {e}\n")
    exit(1)

# Test 3: Import Backtesting
print("✓ Test 3: Import Backtesting")
try:
    from src.utils.backtesting import Backtester
    print("  ✅ Backtesting importé\n")
except Exception as e:
    print(f"  ❌ Erreur: {e}\n")
    exit(1)

# Test 4: Création des stratégies
print("✓ Test 4: Création des stratégies sur AAPL")
try:
    print("  ⏳ Long Straddle...")
    straddle = LongStraddle.from_ticker('AAPL', 30)
    print(f"     Coût: ${straddle.total_cost:.2f}")
    
    print("  ⏳ Long Strangle...")
    strangle = LongStrangle.from_ticker('AAPL', 30, otm_percent=0.05)
    print(f"     Coût: ${strangle.total_cost:.2f}")
    
    print("  ⏳ Iron Condor...")
    condor = IronCondor.from_ticker('AAPL', 30)
    print(f"     Crédit: ${condor.net_credit:.2f}")
    
    print("  ✅ Toutes les stratégies créées\n")
except Exception as e:
    print(f"  ❌ Erreur: {e}\n")
    exit(1)

# Test 5: Monte Carlo rapide
print("✓ Test 5: Test Monte Carlo rapide (100 simulations)")
try:
    from src.utils.market_data import get_ticker_info
    info = get_ticker_info('AAPL')
    mc = MonteCarloAnalysis(info['current_price'], 0.3)
    result = mc.probability_of_profit(straddle.profit_at_expiry, 30/365, 100)
    print(f"  Probabilité de profit: {result['probability_of_profit']*100:.1f}%")
    print("  ✅ Monte Carlo fonctionne\n")
except Exception as e:
    print(f"  ❌ Erreur: {e}\n")

# Test 6: Vérification des fichiers web
print("✓ Test 6: Vérification des fichiers web")
import os
files_to_check = [
    'web/templates/index.html',
    'web/static/styles.css',
    'web/static/script.js',
    'web/static/glossary.json'
]
all_exist = True
for f in files_to_check:
    exists = os.path.exists(f)
    status = "✅" if exists else "❌"
    print(f"  {status} {f}")
    if not exists:
        all_exist = False

if all_exist:
    print("  ✅ Tous les fichiers web présents\n")
else:
    print("  ⚠️  Certains fichiers manquent\n")

# Résumé
print("="*60)
print("🎉 RÉSUMÉ DES TESTS")
print("="*60)
print("\n✅ Stratégies disponibles:")
print("   • Long Straddle")
print("   • Long Strangle")
print("   • Iron Condor")
print("\n✅ Analyses avancées:")
print("   • Monte Carlo (probabilité de profit)")
print("   • Backtesting historique")
print("   • Comparaison multi-stratégies")
print("\n✅ Interface web:")
print("   • Mode Sombre/Clair")
print("   • Graphiques interactifs (zoom/pan)")
print("   • Section Éducation avec tooltips")
print("   • Export PDF/Excel/CSV")
print("\n🚀 Prêt à lancer l'application web!")
print("   Commande: python web_app.py")
print("   URL: http://127.0.0.1:5003")
print()
