"""
Long Strangle Strategy
Acheter un Call OTM + Acheter un Put OTM
Profit si mouvement important dans les deux sens
"""

from ..models.black_scholes import Call, Put
from ..utils.market_data import get_ticker_info
import numpy as np


class LongStrangle:
    """Stratégie Long Strangle avec Call et Put OTM"""
    
    def __init__(self, call_option: Call, put_option: Put):
        """
        Initialise un Long Strangle
        
        Args:
            call_option: Option Call OTM
            put_option: Option Put OTM
        """
        if call_option.K <= put_option.K:
            raise ValueError("Le strike du Call doit être supérieur au strike du Put pour un Strangle")
        
        self.call = call_option
        self.put = put_option
    
    def price(self) -> float:
        """Calcule le coût total de la stratégie"""
        return self.call.price() + self.put.price()
    
    @property
    def total_cost(self) -> float:
        """Alias pour price() pour compatibilité"""
        return self.price()
    
    @classmethod
    def from_ticker(cls, ticker: str, time_to_expiry_days: int, 
                    call_strike: float = None, put_strike: float = None,
                    otm_percent: float = 0.05):
        """
        Crée un Long Strangle depuis un ticker Yahoo Finance
        
        Args:
            ticker: Symbole du ticker
            time_to_expiry_days: Nombre de jours jusqu'à l'expiration
            call_strike: Strike du call (optionnel, défaut = spot * (1 + otm_percent))
            put_strike: Strike du put (optionnel, défaut = spot * (1 - otm_percent))
            otm_percent: Pourcentage OTM par défaut (0.05 = 5%)
        """
        info = get_ticker_info(ticker)
        spot_price = info['current_price']
        volatility = info.get('implied_volatility', 0.3)
        risk_free_rate = 0.05
        time_to_expiry_years = time_to_expiry_days / 365.0
        
        # Calcul des strikes OTM si non fournis
        if call_strike is None:
            call_strike = spot_price * (1 + otm_percent)
        if put_strike is None:
            put_strike = spot_price * (1 - otm_percent)
        
        if call_strike <= put_strike:
            raise ValueError(f"Le strike du Call ({call_strike:.2f}) doit être > strike du Put ({put_strike:.2f})")
        
        call = Call(spot_price, call_strike, time_to_expiry_years, risk_free_rate, volatility)
        put = Put(spot_price, put_strike, time_to_expiry_years, risk_free_rate, volatility)
        
        return cls(call, put)
    
    def break_even_points(self) -> tuple:
        """Calcule les points de break-even"""
        total = self.price()
        lower_be = self.put.K - total
        upper_be = self.call.K + total
        return (lower_be, upper_be)
    
    def profit_at_expiry(self, final_price: float) -> float:
        """
        Calcule le profit/perte à l'expiration pour un prix donné
        
        Args:
            final_price: Prix du sous-jacent à l'expiration
            
        Returns:
            Profit ou perte (négatif)
        """
        call_payoff = max(0, final_price - self.call.K)
        put_payoff = max(0, self.put.K - final_price)
        total_payoff = call_payoff + put_payoff
        
        return total_payoff - self.price()
    
    def max_loss(self) -> float:
        """Perte maximale (coût total de la stratégie)"""
        return -self.price()
    
    def greeks(self) -> dict:
        """Calcule les Greeks combinés du Strangle"""
        return {
            'delta': self.call.delta() + self.put.delta(),
            'gamma': self.call.gamma() + self.put.gamma(),
            'vega': self.call.vega() + self.put.vega(),
            'theta': self.call.theta() + self.put.theta(),
            'rho': self.call.rho() + self.put.rho()
        }
    
    def summary(self) -> dict:
        """Retourne un résumé complet de la stratégie"""
        lower_be, upper_be = self.break_even_points()
        greeks = self.greeks()
        
        spot_price = self.call.S
        required_move_lower = abs(lower_be - spot_price) / spot_price * 100
        required_move_upper = abs(upper_be - spot_price) / spot_price * 100
        
        return {
            'strategy': 'Long Strangle',
            'spot_price': spot_price,
            'call_strike': self.call.K,
            'put_strike': self.put.K,
            'call_price': self.call.price(),
            'put_price': self.put.price(),
            'total_cost': self.total_cost,
            'max_loss': self.max_loss(),
            'max_profit': 'Illimité',
            'lower_break_even': lower_be,
            'upper_break_even': upper_be,
            'required_move_lower_pct': required_move_lower,
            'required_move_upper_pct': required_move_upper,
            'time_to_expiry_days': int(self.call.T * 365),
            'greeks': greeks
        }
