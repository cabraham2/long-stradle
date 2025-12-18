"""
Iron Condor Strategy
Bull Put Spread + Bear Call Spread
Profit si le prix reste dans une range
"""

from ..models.black_scholes import Call, Put
from ..utils.market_data import get_ticker_info
import numpy as np


class IronCondor:
    """Stratégie Iron Condor avec 4 options"""
    
    def __init__(self, 
                 long_put: Put,    # Put acheté (strike le plus bas)
                 short_put: Put,   # Put vendu (strike moyen-bas)
                 short_call: Call, # Call vendu (strike moyen-haut)
                 long_call: Call): # Call acheté (strike le plus haut)
        """
        Initialise un Iron Condor
        
        Args:
            long_put: Put acheté (protection downside)
            short_put: Put vendu (génère crédit)
            short_call: Call vendu (génère crédit)
            long_call: Call acheté (protection upside)
        """
        # Validation des strikes
        if not (long_put.K < short_put.K < short_call.K < long_call.K):
            raise ValueError("Les strikes doivent être: long_put < short_put < short_call < long_call")
        
        self.long_put = long_put
        self.short_put = short_put
        self.short_call = short_call
        self.long_call = long_call
    
    def price(self) -> float:
        """Calcule le crédit net reçu (négatif = coût)"""
        return (
            self.short_put.price() + self.short_call.price() - 
            self.long_put.price() - self.long_call.price()
        )
    
    @property
    def net_credit(self) -> float:
        """Alias pour price() pour compatibilité"""
        return self.price()
    
    @property
    def put_spread_width(self) -> float:
        """Largeur du put spread"""
        return self.short_put.K - self.long_put.K
    
    @property
    def call_spread_width(self) -> float:
        """Largeur du call spread"""
        return self.long_call.K - self.short_call.K
    
    @classmethod
    def from_ticker(cls, ticker: str, time_to_expiry_days: int,
                    put_spread_width_pct: float = 0.05,
                    call_spread_width_pct: float = 0.05,
                    center_offset_pct: float = 0.10):
        """
        Crée un Iron Condor depuis un ticker Yahoo Finance
        
        Args:
            ticker: Symbole du ticker
            time_to_expiry_days: Nombre de jours jusqu'à l'expiration
            put_spread_width_pct: Largeur du put spread en % du spot (0.05 = 5%)
            call_spread_width_pct: Largeur du call spread en % du spot
            center_offset_pct: Distance du centre par rapport au spot (0.10 = 10%)
        """
        info = get_ticker_info(ticker)
        spot_price = info['current_price']
        volatility = info.get('implied_volatility', 0.3)
        risk_free_rate = 0.05
        time_to_expiry_years = time_to_expiry_days / 365.0
        
        # Calcul des strikes symétriques autour du spot
        put_width = spot_price * put_spread_width_pct
        call_width = spot_price * call_spread_width_pct
        offset = spot_price * center_offset_pct
        
        # Strikes du put spread
        short_put_strike = spot_price - offset
        long_put_strike = short_put_strike - put_width
        
        # Strikes du call spread
        short_call_strike = spot_price + offset
        long_call_strike = short_call_strike + call_width
        
        # Création des options
        long_put = Put(spot_price, long_put_strike, time_to_expiry_years, risk_free_rate, volatility)
        short_put = Put(spot_price, short_put_strike, time_to_expiry_years, risk_free_rate, volatility)
        short_call = Call(spot_price, short_call_strike, time_to_expiry_years, risk_free_rate, volatility)
        long_call = Call(spot_price, long_call_strike, time_to_expiry_years, risk_free_rate, volatility)
        
        return cls(long_put, short_put, short_call, long_call)
    
    def break_even_points(self) -> tuple:
        """Calcule les points de break-even"""
        credit = self.price()
        lower_be = self.short_put.K - credit
        upper_be = self.short_call.K + credit
        return (lower_be, upper_be)
    
    def profit_at_expiry(self, final_price: float) -> float:
        """
        Calcule le profit/perte à l'expiration pour un prix donné
        
        Args:
            final_price: Prix du sous-jacent à l'expiration
            
        Returns:
            Profit ou perte
        """
        # Payoff du put spread (court)
        long_put_payoff = max(0, self.long_put.K - final_price)
        short_put_payoff = -max(0, self.short_put.K - final_price)
        
        # Payoff du call spread (court)
        short_call_payoff = -max(0, final_price - self.short_call.K)
        long_call_payoff = max(0, final_price - self.long_call.K)
        
        total_payoff = long_put_payoff + short_put_payoff + short_call_payoff + long_call_payoff
        
        return total_payoff + self.price()
    
    def max_profit(self) -> float:
        """Profit maximum (crédit net reçu)"""
        return self.price()
    
    def max_loss(self) -> float:
        """Perte maximale"""
        # La perte max est la largeur du plus grand spread moins le crédit
        max_spread_width = max(self.put_spread_width, self.call_spread_width)
        return -(max_spread_width - self.price())
    
    def greeks(self) -> dict:
        """Calcule les Greeks combinés de l'Iron Condor"""
        return {
            'delta': (
                self.long_put.delta() + self.short_put.delta() * -1 +
                self.short_call.delta() * -1 + self.long_call.delta()
            ),
            'gamma': (
                self.long_put.gamma() - self.short_put.gamma() -
                self.short_call.gamma() + self.long_call.gamma()
            ),
            'vega': (
                self.long_put.vega() - self.short_put.vega() -
                self.short_call.vega() + self.long_call.vega()
            ),
            'theta': (
                self.long_put.theta() - self.short_put.theta() -
                self.short_call.theta() + self.long_call.theta()
            ),
            'rho': (
                self.long_put.rho() - self.short_put.rho() -
                self.short_call.rho() + self.long_call.rho()
            )
        }
    
    def summary(self) -> dict:
        """Retourne un résumé complet de la stratégie"""
        lower_be, upper_be = self.break_even_points()
        greeks = self.greeks()
        
        spot_price = self.long_put.S
        profit_range_width = upper_be - lower_be
        profit_range_pct = (profit_range_width / spot_price) * 100
        
        return {
            'strategy': 'Iron Condor',
            'spot_price': spot_price,
            'long_put_strike': self.long_put.K,
            'short_put_strike': self.short_put.K,
            'short_call_strike': self.short_call.K,
            'long_call_strike': self.long_call.K,
            'net_credit': self.net_credit,
            'max_profit': self.max_profit(),
            'max_loss': self.max_loss(),
            'lower_break_even': lower_be,
            'upper_break_even': upper_be,
            'profit_range_width': profit_range_width,
            'profit_range_pct': profit_range_pct,
            'put_spread_width': self.put_spread_width,
            'call_spread_width': self.call_spread_width,
            'time_to_expiry_days': int(self.long_put.T * 365),
            'greeks': greeks
        }
