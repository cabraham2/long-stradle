"""
Démonstration Complète des Nouvelles Fonctionnalités
Options Pricer Pro - Version Améliorée
"""

import sys
from src.strategies.long_straddle import LongStraddle
from src.strategies.long_strangle import LongStrangle
from src.strategies.iron_condor import IronCondor
from src.utils.monte_carlo import MonteCarloAnalysis
from src.utils.backtesting import Backtester
from src.utils.display import *

def demo_multi_strategies():
    """Démonstration de la comparaison multi-stratégies"""
    print("\n" + "="*70)
    print("  DÉMONSTRATION: COMPARAISON MULTI-STRATÉGIES")
    print("="*70 + "\n")
    
    ticker = "AAPL"
    days = 30
    
    print(f"📊 Comparaison de 3 stratégies sur {ticker} (échéance: {days} jours)\n")
    
    try:
        # Créer les 3 stratégies
        print("⏳ Création des stratégies...")
        straddle = LongStraddle.from_ticker(ticker, days)
        strangle = LongStrangle.from_ticker(ticker, days, otm_percent=0.05)
        condor = IronCondor.from_ticker(ticker, days)
        
        # Résumés
        print(f"\n{colored('1. LONG STRADDLE', Fore.CYAN)}")
        print(f"   Coût total: {colored(f'${straddle.total_cost:.2f}', Fore.YELLOW)}")
        print(f"   Perte max: {colored(f'${abs(straddle.max_loss()):.2f}', Fore.RED)}")
        print(f"   Profit max: {colored('Illimité', Fore.GREEN)}")
        be_lower, be_upper = straddle.break_even_points()
        print(f"   Break-even: ${be_lower:.2f} - ${be_upper:.2f}")
        
        print(f"\n{colored('2. LONG STRANGLE', Fore.CYAN)}")
        print(f"   Coût total: {colored(f'${strangle.total_cost:.2f}', Fore.YELLOW)}")
        print(f"   Perte max: {colored(f'${abs(strangle.max_loss()):.2f}', Fore.RED)}")
        print(f"   Profit max: {colored('Illimité', Fore.GREEN)}")
        be_lower, be_upper = strangle.break_even_points()
        print(f"   Break-even: ${be_lower:.2f} - ${be_upper:.2f}")
        
        print(f"\n{colored('3. IRON CONDOR', Fore.CYAN)}")
        print(f"   Crédit net: {colored(f'${condor.net_credit:.2f}', Fore.GREEN)}")
        print(f"   Perte max: {colored(f'${abs(condor.max_loss()):.2f}', Fore.RED)}")
        print(f"   Profit max: {colored(f'${condor.max_profit():.2f}', Fore.YELLOW)}")
        be_lower, be_upper = condor.break_even_points()
        print(f"   Break-even: ${be_lower:.2f} - ${be_upper:.2f}")
        
        print("\n✅ Comparaison terminée!")
        
    except Exception as e:
        print(f"{colored(f'❌ Erreur: {e}', Fore.RED)}")


def demo_monte_carlo():
    """Démonstration de l'analyse Monte Carlo"""
    print("\n" + "="*70)
    print("  DÉMONSTRATION: ANALYSE MONTE CARLO")
    print("="*70 + "\n")
    
    ticker = "AAPL"
    days = 30
    num_simulations = 5000
    
    print(f"🎲 Simulation Monte Carlo sur {ticker} ({num_simulations} simulations)\n")
    
    try:
        # Créer stratégie
        print("⏳ Création de la stratégie Long Straddle...")
        straddle = LongStraddle.from_ticker(ticker, days)
        
        # Récupérer info pour volatilité
        from src.utils.market_data import get_ticker_info
        info = get_ticker_info(ticker)
        spot_price = info['current_price']
        volatility = info.get('implied_volatility', 0.3)
        
        print(f"   Prix spot: ${spot_price:.2f}")
        print(f"   Volatilité: {volatility*100:.1f}%")
        
        # Monte Carlo
        print(f"\n⏳ Simulation de {num_simulations} scénarios...")
        mc = MonteCarloAnalysis(spot_price, volatility)
        result = mc.probability_of_profit(
            straddle.profit_at_expiry,
            days / 365.0,
            num_simulations
        )
        
        # Afficher résultats
        print(f"\n{colored('RÉSULTATS MONTE CARLO', Fore.CYAN)}")
        prob_color = Fore.GREEN if result['probability_of_profit'] > 0.5 else Fore.YELLOW
        print(f"   Probabilité de profit: {colored(f'{result[\"probability_of_profit\"]*100:.2f}%', prob_color)}")
        print(f"   Probabilité de perte: {colored(f'{result[\"probability_of_loss\"]*100:.2f}%', Fore.RED)}")
        print(f"   Espérance de gain: {colored_number(result['expected_profit'])}")
        print(f"   Médiane: {colored_number(result['median_profit'])}")
        print(f"   Écart-type: ${result['std_profit']:.2f}")
        print(f"   Ratio Risque/Récompense: {colored(f'{result[\"risk_reward_ratio\"]:.2f}', Fore.GREEN)}")
        
        print(f"\n{colored('PERCENTILES', Fore.CYAN)}")
        print(f"   5ème percentile (VaR 95%): {colored_number(result['percentiles']['5th'])}")
        print(f"   25ème percentile: {colored_number(result['percentiles']['25th'])}")
        print(f"   50ème percentile (médiane): {colored_number(result['percentiles']['50th'])}")
        print(f"   75ème percentile: {colored_number(result['percentiles']['75th'])}")
        print(f"   95ème percentile: {colored_number(result['percentiles']['95th'])}")
        
        # VaR
        var_result = mc.value_at_risk(
            straddle.profit_at_expiry,
            days / 365.0,
            confidence_level=0.95,
            num_simulations=num_simulations
        )
        
        print(f"\n{colored('VALUE AT RISK (95%)', Fore.CYAN)}")
        print(f"   VaR: {colored_number(var_result['value_at_risk'])}")
        print(f"   CVaR: {colored_number(var_result['conditional_var'])}")
        print(f"   {var_result['interpretation']}")
        
        # Break-even probability
        be_lower, be_upper = straddle.break_even_points()
        be_analysis = mc.breakeven_probability_analysis(
            (be_lower, be_upper),
            days / 365.0,
            num_simulations
        )
        
        print(f"\n{colored('ANALYSE BREAK-EVEN', Fore.CYAN)}")
        print(f"   Prob. prix < BE inférieur (${be_lower:.2f}): {colored(f'{be_analysis[\"prob_below_lower_be\"]*100:.2f}%', Fore.GREEN)}")
        print(f"   Prob. prix > BE supérieur (${be_upper:.2f}): {colored(f'{be_analysis[\"prob_above_upper_be\"]*100:.2f}%', Fore.GREEN)}")
        print(f"   Prob. entre les BE (perte): {colored(f'{be_analysis[\"prob_between_be\"]*100:.2f}%', Fore.RED)}")
        print(f"   Prob. profitable totale: {colored(f'{be_analysis[\"prob_profitable\"]*100:.2f}%', Fore.GREEN)}")
        
        print("\n✅ Analyse Monte Carlo terminée!")
        
    except Exception as e:
        print(f"{colored(f'❌ Erreur: {e}', Fore.RED)}")


def demo_backtesting():
    """Démonstration du backtesting historique"""
    print("\n" + "="*70)
    print("  DÉMONSTRATION: BACKTESTING HISTORIQUE")
    print("="*70 + "\n")
    
    ticker = "AAPL"
    holding_days = 30
    
    print(f"📈 Backtesting de Long Straddle sur {ticker} (dernière année)")
    print(f"   Période de détention: {holding_days} jours\n")
    
    try:
        from datetime import datetime
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = datetime.now().replace(year=datetime.now().year - 1).strftime('%Y-%m-%d')
        
        print("⏳ Chargement des données historiques...")
        backtester = Backtester(ticker, start_date, end_date)
        
        print("⏳ Exécution du backtest (peut prendre 10-20 secondes)...")
        result = backtester.backtest_strategy(
            LongStraddle,
            holding_period_days=holding_days,
            rebalance_frequency_days=holding_days
        )
        
        if result['success']:
            print(f"\n{colored('RÉSULTATS BACKTEST', Fore.CYAN)}")
            print(f"   Période: {result['period']}")
            print(f"   Total trades: {colored(str(result['total_trades']), Fore.YELLOW)}")
            print(f"   Trades gagnants: {colored(str(result['winning_trades']), Fore.GREEN)}")
            print(f"   Trades perdants: {colored(str(result['losing_trades']), Fore.RED)}")
            wr_color = Fore.GREEN if result['win_rate'] > 50 else Fore.YELLOW
            print(f"   Taux de réussite: {colored(f'{result[\"win_rate\"]:.2f}%', wr_color)}")
            
            print(f"\n{colored('PERFORMANCE', Fore.CYAN)}")
            print(f"   Profit total: {colored_number(result['total_profit'])}")
            print(f"   Profit moyen/trade: {colored_number(result['avg_profit_per_trade'])}")
            print(f"   Gain moyen (trades +): {colored_number(result['avg_winning_trade'])}")
            print(f"   Perte moyenne (trades -): {colored_number(result['avg_losing_trade'])}")
            
            print(f"\n{colored('MÉTRIQUES', Fore.CYAN)}")
            pf_color = Fore.GREEN if result['profit_factor'] > 1 else Fore.RED
            print(f"   Profit Factor: {colored(f'{result[\"profit_factor\"]:.2f}', pf_color)}")
            sr_color = Fore.GREEN if result['sharpe_ratio'] > 0 else Fore.RED
            print(f"   Sharpe Ratio: {colored(f'{result[\"sharpe_ratio\"]:.2f}', sr_color)}")
            print(f"   Max Drawdown: {colored_number(result['max_drawdown'])}")
            print(f"   Meilleur trade: {colored_number(result['best_trade'])}")
            print(f"   Pire trade: {colored_number(result['worst_trade'])}")
            
            print("\n✅ Backtest terminé!")
            
            # Afficher quelques trades
            if result['trades']:
                print(f"\n{colored('DERNIERS TRADES', Fore.CYAN)}")
                for i, trade in enumerate(result['trades'][-3:], 1):
                    profit_color = Fore.GREEN if trade['profit'] > 0 else Fore.RED
                    print(f"   Trade {len(result['trades'])-3+i}:")
                    print(f"      Entrée: {trade['entry_date'].strftime('%Y-%m-%d')} @ ${trade['entry_price']:.2f}")
                    print(f"      Sortie: {trade['exit_date'].strftime('%Y-%m-%d')} @ ${trade['exit_price']:.2f}")
                    print(f"      P&L: {colored(f'${trade[\"profit\"]:.2f}', profit_color)} ({colored(f'{trade[\"roi\"]:.1f}%', profit_color)})")
        else:
            print(f"{colored(f'❌ Erreur: {result[\"error\"]}', Fore.RED)}")
        
    except Exception as e:
        print(f"{colored(f'❌ Erreur: {e}', Fore.RED)}")


def main():
    """Menu principal"""
    init_colorama()
    
    print("\n" + "="*70)
    print(f"  {colored('OPTIONS PRICER PRO - DÉMONSTRATIONS', Fore.CYAN + Style.BRIGHT)}")
    print("="*70 + "\n")
    
    print("Choisissez une démonstration:\n")
    print("1. Comparaison Multi-Stratégies (Straddle vs Strangle vs Iron Condor)")
    print("2. Analyse Monte Carlo (Probabilité de profit)")
    print("3. Backtesting Historique (Performance sur 1 an)")
    print("4. Tout exécuter")
    print("0. Quitter\n")
    
    choice = input("Votre choix: ").strip()
    
    if choice == "1":
        demo_multi_strategies()
    elif choice == "2":
        demo_monte_carlo()
    elif choice == "3":
        demo_backtesting()
    elif choice == "4":
        demo_multi_strategies()
        input("\nAppuyez sur Entrée pour continuer...")
        demo_monte_carlo()
        input("\nAppuyez sur Entrée pour continuer...")
        demo_backtesting()
    elif choice == "0":
        print("\nAu revoir! 👋")
        return
    else:
        print(f"{colored('❌ Choix invalide', Fore.RED)}")
    
    print("\n" + "="*70)
    print("  Démonstration terminée!")
    print("  Pour plus d'info, consultez README_FEATURES.md")
    print("  Pour l'interface web: python web_app.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
