"""
Script principal pour le priceur d'options Long Straddle
Interface interactive en ligne de commande
"""

import json
import sys
from src.strategies.long_straddle import LongStraddle
from src.utils.market_data import get_ticker_info, validate_ticker
from src.utils.display import (
    print_banner, print_header, print_section, print_success, 
    print_error, print_warning, print_info, input_prompt,
    print_ticker_info, print_straddle_summary, print_profit_table
)


def example_1_manual_straddle():
    """Exemple 1: Créer un straddle manuellement avec des paramètres"""
    print("=" * 70)
    print("EXEMPLE 1: Long Straddle avec paramètres manuels")
    print("=" * 70)
    
    # Paramètres
    S = 100.0      # Prix spot
    K = 100.0      # Strike ATM
    T = 30/365     # 30 jours
    r = 0.05       # Taux sans risque 5%
    sigma = 0.25   # Volatilité 25%
    
    # Créer le straddle
    straddle = LongStraddle(S, K, T, r, sigma)
    
    # Afficher le résumé
    summary = straddle.summary()
    print(f"\nPrix spot: ${summary['spot_price']:.2f}")
    print(f"Strike: ${summary['strike']:.2f}")
    print(f"Temps à échéance: {summary['time_to_expiry_days']} jours")
    print(f"Volatilité: {summary['volatility']*100:.2f}%")
    print(f"\n--- PRIX ---")
    print(f"Prix du Call: ${summary['call_price']:.2f}")
    print(f"Prix du Put: ${summary['put_price']:.2f}")
    print(f"Coût total du Straddle: ${summary['total_cost']:.2f}")
    print(f"\n--- ANALYSE DE RISQUE ---")
    print(f"Perte maximale: ${summary['max_loss']:.2f}")
    print(f"Profit maximum: {summary['max_profit']}")
    print(f"Break-even inférieur: ${summary['lower_break_even']:.2f}")
    print(f"Break-even supérieur: ${summary['upper_break_even']:.2f}")
    print(f"Mouvement requis: ±{summary['break_even_move_pct']:.2f}%")
    print(f"\n--- GREEKS ---")
    for greek, value in summary['greeks'].items():
        print(f"{greek.capitalize()}: {value:.4f}")
    
    return straddle


def example_2_ticker_straddle():
    """Exemple 2: Créer un straddle avec données de marché réelles"""
    print("\n" + "=" * 70)
    print("EXEMPLE 2: Long Straddle avec données Yahoo Finance")
    print("=" * 70)
    
    ticker = "AAPL"  # Apple
    days = 30        # 30 jours jusqu'à échéance
    
    print(f"\nRécupération des données pour {ticker}...")
    
    try:
        # Créer le straddle avec données réelles
        straddle = LongStraddle.from_ticker(ticker, days_to_expiry=days)
        
        summary = straddle.summary()
        print(f"\n✓ Données récupérées avec succès!")
        print(f"\nPrix spot de {ticker}: ${summary['spot_price']:.2f}")
        print(f"Volatilité historique: {summary['volatility']*100:.2f}%")
        print(f"Taux sans risque: {summary['risk_free_rate']*100:.2f}%")
        print(f"\nCoût du Straddle ATM: ${summary['total_cost']:.2f}")
        print(f"Break-even points: ${summary['lower_break_even']:.2f} - ${summary['upper_break_even']:.2f}")
        print(f"Mouvement requis pour profit: ±{summary['break_even_move_pct']:.2f}%")
        
        return straddle
        
    except Exception as e:
        print(f"✗ Erreur lors de la récupération des données: {e}")
        print("Vérifiez votre connexion internet et que le ticker est valide")
        return None


def example_3_profit_analysis(straddle: LongStraddle):
    """Exemple 3: Analyse des profits à différents prix"""
    print("\n" + "=" * 70)
    print("EXEMPLE 3: Analyse des profits à l'échéance")
    print("=" * 70)
    
    # Prix à analyser (en % du spot)
    price_scenarios = [-20, -10, -5, 0, 5, 10, 20]
    
    print(f"\nPrix spot actuel: ${straddle.S:.2f}")
    print(f"Coût du straddle: ${straddle.price():.2f}")
    print("\nScénarios de profit/perte à l'échéance:")
    print("-" * 70)
    print(f"{'Prix final':<15} {'Variation':<15} {'Payoff':<15} {'P&L Net':<15}")
    print("-" * 70)
    
    for pct in price_scenarios:
        final_price = straddle.S * (1 + pct/100)
        profit = straddle.profit_at_expiry(final_price)
        payoff = straddle.payoff_at_expiry(final_price)
        
        status = "✓ PROFIT" if profit > 0 else "✗ PERTE" if profit < 0 else "= BE"
        
        print(f"${final_price:<14.2f} {pct:>6}% {' '*6} "
              f"${payoff:<14.2f} ${profit:<14.2f} {status}")


def example_4_greeks_sensitivity():
    """Exemple 4: Analyse de sensibilité des Greeks"""
    print("\n" + "=" * 70)
    print("EXEMPLE 4: Sensibilité des Greeks")
    print("=" * 70)
    
    S = 100.0
    K = 100.0
    T = 30/365
    r = 0.05
    sigma = 0.25
    
    straddle = LongStraddle(S, K, T, r, sigma)
    greeks = straddle.greeks()
    
    print(f"\n--- INTERPRÉTATION DES GREEKS ---")
    print(f"\nDelta: {greeks['delta']:.4f}")
    print(f"  → Pour $1 de hausse du sous-jacent, le straddle varie de ${greeks['delta']:.2f}")
    print(f"  → Proche de 0 pour un straddle ATM (neutre directionnellement)")
    
    print(f"\nGamma: {greeks['gamma']:.4f}")
    print(f"  → Mesure l'accélération du delta")
    print(f"  → Positif: bénéficie des grands mouvements")
    
    print(f"\nVega: {greeks['vega']:.4f}")
    print(f"  → Pour +1% de volatilité, le straddle gagne ${greeks['vega']:.2f}")
    print(f"  → Positif: profite d'une hausse de volatilité")
    
    print(f"\nTheta: {greeks['theta']:.4f}")
    print(f"  → Perte quotidienne due au temps: ${greeks['theta']:.2f}/jour")
    print(f"  → Négatif: la valeur diminue avec le temps")
    
    print(f"\nRho: {greeks['rho']:.4f}")
    print(f"  → Pour +1% de taux d'intérêt, variation de ${greeks['rho']:.2f}")


def example_5_compare_strikes():
    """Exemple 5: Comparer différents strikes"""
    print("\n" + "=" * 70)
    print("EXEMPLE 5: Comparaison de différents strikes")
    print("=" * 70)
    
    S = 100.0
    T = 30/365
    r = 0.05
    sigma = 0.25
    
    strikes = [95, 100, 105]  # OTM put/call, ATM, OTM call/put
    
    print(f"\nPrix spot: ${S:.2f}")
    print("\nComparaison des straddles:")
    print("-" * 70)
    print(f"{'Strike':<10} {'Type':<10} {'Coût':<10} {'BE Inférieur':<15} {'BE Supérieur':<15}")
    print("-" * 70)
    
    for K in strikes:
        straddle = LongStraddle(S, K, T, r, sigma)
        cost = straddle.price()
        lower_be, upper_be = straddle.break_even_points()
        
        if K < S:
            strike_type = "Bearish"
        elif K > S:
            strike_type = "Bullish"
        else:
            strike_type = "ATM"
        
        print(f"${K:<9.2f} {strike_type:<10} ${cost:<9.2f} ${lower_be:<14.2f} ${upper_be:<14.2f}")


def save_analysis_to_json(straddle: LongStraddle, filename: str = "straddle_analysis.json"):
    """Sauvegarder l'analyse dans un fichier JSON"""
    summary = straddle.summary()
    
    # Convertir pour JSON (gérer 'inf')
    if summary['max_profit'] == 'Unlimited':
        summary['max_profit_numeric'] = None
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Analyse sauvegardée dans {filename}")


def get_ticker_from_user() -> str:
    """
    Demande à l'utilisateur de saisir un ticker et le valide
    
    Returns:
        Le ticker validé
    """
    while True:
        ticker = input_prompt("Entrez le ticker du sous-jacent (ex: AAPL, MSFT, TSLA):").strip().upper()
        
        if not ticker:
            print_warning("Veuillez entrer un ticker valide")
            continue
        
        print_info(f"Vérification du ticker {ticker}...")
        
        if validate_ticker(ticker):
            print_success(f"Ticker {ticker} validé!")
            return ticker
        else:
            print_error(f"Ticker {ticker} invalide ou non trouvé")
            retry = input_prompt("Voulez-vous essayer un autre ticker? (o/n):").strip().lower()
            if retry != 'o':
                print_info("Au revoir!")
                sys.exit(0)


def get_straddle_parameters():
    """
    Demande les paramètres du straddle à l'utilisateur
    
    Returns:
        Tuple (days_to_expiry, custom_strike)
    """
    print_section("Paramètres du Straddle")
    
    # Jours jusqu'à échéance
    while True:
        days_input = input_prompt("Nombre de jours jusqu'à échéance (défaut: 30):")
        if not days_input:
            days = 30
            break
        try:
            days = int(days_input)
            if days > 0:
                break
            else:
                print_error("Le nombre de jours doit être positif")
        except ValueError:
            print_error("Veuillez entrer un nombre entier")
    
    # Strike personnalisé
    strike_input = input_prompt("Strike personnalisé (appuyez sur Entrée pour ATM):").strip()
    custom_strike = None
    if strike_input:
        try:
            custom_strike = float(strike_input)
            if custom_strike <= 0:
                print_warning("Strike invalide, utilisation du strike ATM")
                custom_strike = None
        except ValueError:
            print_warning("Strike invalide, utilisation du strike ATM")
    
    return days, custom_strike


def interactive_main():
    """Mode interactif principal"""
    print_banner()
    
    # Récupérer le ticker
    ticker = get_ticker_from_user()
    
    # Récupérer les informations du ticker
    print_info("Récupération des données de marché...")
    try:
        ticker_info = get_ticker_info(ticker)
        print_ticker_info(ticker_info)
    except Exception as e:
        print_error(f"Erreur lors de la récupération des données: {e}")
        sys.exit(1)
    
    # Demander les paramètres
    days, custom_strike = get_straddle_parameters()
    
    # Créer le straddle
    print_info("Calcul du pricing du straddle...")
    try:
        straddle = LongStraddle.from_ticker(ticker, K=custom_strike, days_to_expiry=days)
        
        # Afficher le résumé
        summary = straddle.summary()
        print_straddle_summary(summary)
        
        # Afficher les scénarios de profit
        scenarios = [-30, -20, -10, -5, 0, 5, 10, 20, 30]
        print_profit_table(straddle, scenarios)
        
        # Proposer de sauvegarder
        print_section("Sauvegarde")
        save = input_prompt("Sauvegarder l'analyse en JSON? (o/n):").strip().lower()
        if save == 'o':
            filename = f"straddle_analysis_{ticker}_{days}d.json"
            save_analysis_to_json(straddle, filename)
            print_success(f"Analyse sauvegardée dans {filename}")
        
        # Proposer une autre analyse
        print_section("Nouvelle Analyse")
        another = input_prompt("Analyser un autre ticker? (o/n):").strip().lower()
        if another == 'o':
            print("\n")
            interactive_main()
        else:
            print_info("Au revoir!")
            
    except Exception as e:
        print_error(f"Erreur lors du calcul: {e}")
        sys.exit(1)


def demo_mode():
    """Mode démo avec exemples prédéfinis"""
    print_banner()
    print_header(" MODE DÉMO ")
    print_info("Démonstration avec des exemples prédéfinis\n")
    
    # Exemple 1: AAPL
    print_section("Exemple 1: Apple (AAPL) - 30 jours")
    try:
        ticker_info = get_ticker_info("AAPL")
        print_ticker_info(ticker_info)
        
        straddle = LongStraddle.from_ticker("AAPL", days_to_expiry=30)
        summary = straddle.summary()
        print_straddle_summary(summary)
        print_profit_table(straddle, [-20, -10, 0, 10, 20])
    except Exception as e:
        print_error(f"Erreur: {e}")
    
    print("\n" + "="*70)
    print_info("Fin de la démonstration")


def main():
    """Fonction principale"""
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo_mode()
    else:
        interactive_main()


if __name__ == "__main__":
    main()
