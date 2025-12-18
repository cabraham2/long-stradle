"""
Analyse Monte Carlo pour les stratégies d'options
Simule des milliers de scénarios pour estimer la probabilité de profit
"""

import numpy as np
from typing import Dict, List, Tuple, Callable


class MonteCarloAnalysis:
    """Analyse Monte Carlo pour stratégies d'options"""
    
    def __init__(self, spot_price: float, volatility: float, risk_free_rate: float = 0.05):
        """
        Initialise l'analyse Monte Carlo
        
        Args:
            spot_price: Prix actuel du sous-jacent
            volatility: Volatilité annualisée (ex: 0.3 pour 30%)
            risk_free_rate: Taux sans risque annualisé
        """
        self.spot_price = spot_price
        self.volatility = volatility
        self.risk_free_rate = risk_free_rate
    
    def simulate_price_paths(self, time_to_expiry_years: float, 
                            num_simulations: int = 10000,
                            num_steps: int = 252) -> np.ndarray:
        """
        Simule des chemins de prix selon le mouvement brownien géométrique
        
        Args:
            time_to_expiry_years: Temps jusqu'à l'expiration en années
            num_simulations: Nombre de simulations
            num_steps: Nombre de pas de temps (252 = jours de trading par an)
            
        Returns:
            Array de shape (num_simulations, num_steps) avec les prix simulés
        """
        dt = time_to_expiry_years / num_steps
        
        # Drift et diffusion du mouvement brownien géométrique
        drift = (self.risk_free_rate - 0.5 * self.volatility**2) * dt
        diffusion = self.volatility * np.sqrt(dt)
        
        # Génération des chocs aléatoires
        random_shocks = np.random.standard_normal((num_simulations, num_steps))
        
        # Calcul des rendements logarithmiques
        log_returns = drift + diffusion * random_shocks
        
        # Conversion en prix
        price_paths = self.spot_price * np.exp(np.cumsum(log_returns, axis=1))
        
        return price_paths
    
    def simulate_final_prices(self, time_to_expiry_years: float,
                             num_simulations: int = 10000) -> np.ndarray:
        """
        Simule uniquement les prix finaux à l'expiration
        
        Args:
            time_to_expiry_years: Temps jusqu'à l'expiration en années
            num_simulations: Nombre de simulations
            
        Returns:
            Array de prix finaux
        """
        # Drift et diffusion
        drift = (self.risk_free_rate - 0.5 * self.volatility**2) * time_to_expiry_years
        diffusion = self.volatility * np.sqrt(time_to_expiry_years)
        
        # Génération des prix finaux
        random_shocks = np.random.standard_normal(num_simulations)
        log_returns = drift + diffusion * random_shocks
        final_prices = self.spot_price * np.exp(log_returns)
        
        return final_prices
    
    def probability_of_profit(self, strategy_payoff_func: Callable[[float], float],
                             time_to_expiry_years: float,
                             num_simulations: int = 10000) -> Dict:
        """
        Calcule la probabilité de profit pour une stratégie donnée
        
        Args:
            strategy_payoff_func: Fonction qui calcule le P&L à partir d'un prix final
            time_to_expiry_years: Temps jusqu'à l'expiration en années
            num_simulations: Nombre de simulations
            
        Returns:
            Dictionnaire avec statistiques Monte Carlo
        """
        # Simulation des prix finaux
        final_prices = self.simulate_final_prices(time_to_expiry_years, num_simulations)
        
        # Calcul des P&L pour chaque scénario
        payoffs = np.array([strategy_payoff_func(price) for price in final_prices])
        
        # Statistiques
        profitable_outcomes = np.sum(payoffs > 0)
        prob_profit = profitable_outcomes / num_simulations
        
        expected_profit = np.mean(payoffs)
        median_profit = np.median(payoffs)
        std_profit = np.std(payoffs)
        
        # Percentiles
        percentiles = {
            '5th': np.percentile(payoffs, 5),
            '25th': np.percentile(payoffs, 25),
            '50th': median_profit,
            '75th': np.percentile(payoffs, 75),
            '95th': np.percentile(payoffs, 95)
        }
        
        # Ratio risque/récompense
        expected_gain = np.mean(payoffs[payoffs > 0]) if np.any(payoffs > 0) else 0
        expected_loss = np.mean(payoffs[payoffs < 0]) if np.any(payoffs < 0) else 0
        risk_reward_ratio = abs(expected_gain / expected_loss) if expected_loss != 0 else float('inf')
        
        return {
            'probability_of_profit': prob_profit,
            'probability_of_loss': 1 - prob_profit,
            'expected_profit': expected_profit,
            'median_profit': median_profit,
            'std_profit': std_profit,
            'percentiles': percentiles,
            'expected_gain': expected_gain,
            'expected_loss': expected_loss,
            'risk_reward_ratio': risk_reward_ratio,
            'max_simulated_profit': np.max(payoffs),
            'max_simulated_loss': np.min(payoffs),
            'num_simulations': num_simulations,
            'simulated_prices': final_prices.tolist(),
            'simulated_payoffs': payoffs.tolist()
        }
    
    def value_at_risk(self, strategy_payoff_func: Callable[[float], float],
                     time_to_expiry_years: float,
                     confidence_level: float = 0.95,
                     num_simulations: int = 10000) -> Dict:
        """
        Calcule la Value at Risk (VaR) et Conditional VaR (CVaR)
        
        Args:
            strategy_payoff_func: Fonction qui calcule le P&L
            time_to_expiry_years: Temps jusqu'à l'expiration
            confidence_level: Niveau de confiance (0.95 = 95%)
            num_simulations: Nombre de simulations
            
        Returns:
            Dictionnaire avec VaR et CVaR
        """
        final_prices = self.simulate_final_prices(time_to_expiry_years, num_simulations)
        payoffs = np.array([strategy_payoff_func(price) for price in final_prices])
        
        # VaR: perte maximale au niveau de confiance donné
        var_percentile = (1 - confidence_level) * 100
        var = np.percentile(payoffs, var_percentile)
        
        # CVaR (Expected Shortfall): perte moyenne au-delà de la VaR
        cvar = np.mean(payoffs[payoffs <= var])
        
        return {
            'confidence_level': confidence_level,
            'value_at_risk': var,
            'conditional_var': cvar,
            'interpretation': f"Avec {confidence_level*100}% de confiance, la perte ne dépassera pas ${abs(var):.2f}"
        }
    
    def optimal_strike_analysis(self, strategy_class, 
                                time_to_expiry_years: float,
                                strike_range: Tuple[float, float],
                                num_strikes: int = 20,
                                num_simulations: int = 5000) -> List[Dict]:
        """
        Analyse plusieurs strikes pour trouver l'optimal
        
        Args:
            strategy_class: Classe de stratégie (ex: LongStraddle)
            time_to_expiry_years: Temps jusqu'à l'expiration
            strike_range: Tuple (min_strike, max_strike)
            num_strikes: Nombre de strikes à tester
            num_simulations: Simulations par strike
            
        Returns:
            Liste de résultats pour chaque strike
        """
        strikes = np.linspace(strike_range[0], strike_range[1], num_strikes)
        results = []
        
        for strike in strikes:
            # Créer la stratégie avec ce strike
            # Note: Cette fonction est générique, adapter selon la stratégie
            payoff_func = lambda price: max(0, abs(price - strike) - self.spot_price * 0.1)
            
            mc_result = self.probability_of_profit(payoff_func, time_to_expiry_years, num_simulations)
            
            results.append({
                'strike': strike,
                'probability_of_profit': mc_result['probability_of_profit'],
                'expected_profit': mc_result['expected_profit'],
                'risk_reward_ratio': mc_result['risk_reward_ratio']
            })
        
        return results
    
    def breakeven_probability_analysis(self, break_even_points: Tuple[float, float],
                                      time_to_expiry_years: float,
                                      num_simulations: int = 10000) -> Dict:
        """
        Analyse la probabilité d'atteindre les points de break-even
        
        Args:
            break_even_points: Tuple (lower_be, upper_be)
            time_to_expiry_years: Temps jusqu'à l'expiration
            num_simulations: Nombre de simulations
            
        Returns:
            Probabilités d'atteindre chaque break-even
        """
        final_prices = self.simulate_final_prices(time_to_expiry_years, num_simulations)
        
        lower_be, upper_be = break_even_points
        
        # Probabilité d'être en dehors de la zone de perte
        prob_below_lower = np.sum(final_prices < lower_be) / num_simulations
        prob_above_upper = np.sum(final_prices > upper_be) / num_simulations
        prob_between = 1 - prob_below_lower - prob_above_upper
        
        return {
            'prob_below_lower_be': prob_below_lower,
            'prob_above_upper_be': prob_above_upper,
            'prob_between_be': prob_between,
            'prob_profitable': prob_below_lower + prob_above_upper,
            'lower_break_even': lower_be,
            'upper_break_even': upper_be
        }
