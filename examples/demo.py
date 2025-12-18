"""
Script de démonstration rapide de toutes les fonctionnalités
"""

print("🚀 Démarrage de la démonstration du priceur d'options...\n")

# Test 1: Import des modules
print("✓ Test 1: Import des modules")
try:
    from src.strategies.long_straddle import LongStraddle
    from src.utils.market_data import get_ticker_info, validate_ticker
    from src.utils.display import print_banner, print_success
    print("  Tous les modules importés avec succès!\n")
except Exception as e:
    print(f"  ✗ Erreur d'import: {e}\n")
    exit(1)

# Test 2: Validation de ticker
print("✓ Test 2: Validation de ticker")
try:
    is_valid = validate_ticker("AAPL")
    if is_valid:
        print("  AAPL est un ticker valide!\n")
    else:
        print("  Ticker invalide\n")
except Exception as e:
    print(f"  ⚠ Attention: {e}\n")

# Test 3: Récupération d'informations
print("✓ Test 3: Récupération des informations de marché")
try:
    info = get_ticker_info("AAPL")
    print(f"  Ticker: {info['ticker']}")
    print(f"  Nom: {info['name']}")
    print(f"  Prix: {info['currency']} {info['current_price']:.2f}")
    print(f"  Variation: {info['day_change']:+.2f} ({info['day_change_pct']:+.2f}%)")
    print(f"  Cap: {info['market_cap_str']}\n")
except Exception as e:
    print(f"  ⚠ Attention: {e}\n")

# Test 4: Création d'un straddle
print("✓ Test 4: Création d'un Long Straddle")
try:
    straddle = LongStraddle.from_ticker("AAPL", days_to_expiry=30)
    summary = straddle.summary()
    
    print(f"  Strike: ${summary['strike']:.2f}")
    print(f"  Échéance: {summary['time_to_expiry_days']} jours")
    print(f"  Prix Call: ${summary['call_price']:.2f}")
    print(f"  Prix Put: ${summary['put_price']:.2f}")
    print(f"  Coût Total: ${summary['total_cost']:.2f}")
    print(f"  Break-even: ${summary['lower_break_even']:.2f} - ${summary['upper_break_even']:.2f}")
    print(f"  Mouvement requis: ±{summary['break_even_move_pct']:.2f}%\n")
except Exception as e:
    print(f"  ⚠ Attention: {e}\n")

# Test 5: Calcul des Greeks
print("✓ Test 5: Calcul des Greeks")
try:
    greeks = straddle.greeks()
    print(f"  Delta: {greeks['delta']:.4f}")
    print(f"  Gamma: {greeks['gamma']:.4f}")
    print(f"  Vega: {greeks['vega']:.4f}")
    print(f"  Theta: {greeks['theta']:.4f}")
    print(f"  Rho: {greeks['rho']:.4f}\n")
except Exception as e:
    print(f"  ⚠ Attention: {e}\n")

# Test 6: Scénarios de profit
print("✓ Test 6: Scénarios de profit/perte")
try:
    scenarios = [-20, -10, 0, 10, 20]
    print("  Prix Final | Variation | P&L Net")
    print("  " + "-" * 40)
    
    for pct in scenarios:
        final_price = straddle.S * (1 + pct/100)
        profit = straddle.profit_at_expiry(final_price)
        status = "PROFIT" if profit > 0 else "PERTE" if profit < 0 else "BE"
        print(f"  ${final_price:>7.2f}  | {pct:>6}%   | ${profit:>8.2f} ({status})")
    print()
except Exception as e:
    print(f"  ⚠ Attention: {e}\n")

# Test 7: Comparaison de différentes échéances
print("✓ Test 7: Comparaison d'échéances")
try:
    print("  Échéance | Coût Total | Mouvement Requis")
    print("  " + "-" * 45)
    
    for days in [7, 14, 30, 60, 90]:
        s = LongStraddle.from_ticker("AAPL", days_to_expiry=days)
        sum_s = s.summary()
        print(f"  {days:>4} j   | ${sum_s['total_cost']:>9.2f} | ±{sum_s['break_even_move_pct']:>6.2f}%")
    print()
except Exception as e:
    print(f"  ⚠ Attention: {e}\n")

print("=" * 60)
print("✅ Démonstration terminée!")
print("=" * 60)
print("\n🖥️  Pour l'interface terminal: python main.py")
print("🌐 Pour l'interface web: python web_app.py")
print()
