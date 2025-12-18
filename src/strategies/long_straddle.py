"""
Long Straddle Strategy
Stratégie combinant un call et un put ATM pour profiter de la volatilité
"""

from typing import Dict, Optional, Tuple
from ..models.black_scholes import Call, Put, get_greeks
from ..utils.market_data import get_market_data


class LongStraddle:
    """
    Long Straddle: Achat d'un call et d'un put au même strike (généralement ATM)
    Profite d'une forte variation du sous-jacent dans n'importe quelle direction
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialise la stratégie Long Straddle
        
        Deux modes d'utilisation:
        1. LongStraddle(call_option, put_option) - avec objets Call/Put
        2. LongStraddle(S, K, T, r, sigma, q=0.0) - avec paramètres numériques
        """
        # Mode 1: Call et Put objects
        if len(args) == 2 and isinstance(args[0], Call) and isinstance(args[1], Put):
            self.call = args[0]
            self.put = args[1]
            self.S = self.call.S
            self.K = self.call.K
            self.T = self.call.T
            self.r = self.call.r
            self.sigma = self.call.sigma
            self.q = self.call.q
        # Mode 2: Paramètres numériques
        else:
            S = args[0] if len(args) > 0 else kwargs.get('S')
            K = args[1] if len(args) > 1 else kwargs.get('K')
            T = args[2] if len(args) > 2 else kwargs.get('T')
            r = args[3] if len(args) > 3 else kwargs.get('r')
            sigma = args[4] if len(args) > 4 else kwargs.get('sigma')
            q = args[5] if len(args) > 5 else kwargs.get('q', 0.0)
            
            self.S = S
            self.K = K
            self.T = T
            self.r = r
            self.sigma = sigma
            self.q = q
            
            # Créer les options call et put
            self.call = Call(S, K, T, r, sigma, q)
            self.put = Put(S, K, T, r, sigma, q)
        
    @classmethod
    def create_atm(cls, S: float, T: float, r: float, 
                   sigma: float, q: float = 0.0):
        """
        Crée un Long Straddle ATM (at-the-money)
        
        Args:
            S: Prix spot du sous-jacent
            T: Temps jusqu'à l'échéance (en années)
            r: Taux sans risque
            sigma: Volatilité implicite
            q: Rendement du dividende
            
        Returns:
            Instance de LongStraddle avec K = S
        """
        return cls(S, S, T, r, sigma, q)
    
    @classmethod
    def from_ticker(cls, ticker: str, K: Optional[float] = None, 
                    days_to_expiry: int = 30) -> 'LongStraddle':
        """
        Crée un Long Straddle en récupérant les données depuis Yahoo Finance
        
        Args:
            ticker: Symbole du ticker (ex: 'AAPL')
            K: Prix d'exercice (si None, utilise le prix spot pour ATM)
            days_to_expiry: Nombre de jours jusqu'à l'échéance
            
        Returns:
            Instance de LongStraddle avec données de marché
        """
        # Récupérer les données de marché
        S, sigma, r = get_market_data(ticker)
        
        # Si pas de strike spécifié, utiliser ATM
        if K is None:
            K = S
        
        # Convertir jours en années
        T = days_to_expiry / 365.0
        
        return cls(S, K, T, r, sigma)
    
    def price(self) -> float:
        """
        Calcule le prix total du straddle (coût d'entrée)
        
        Returns:
            Prix total = prix du call + prix du put
        """
        call_price = self.call.price()
        put_price = self.put.price()
        
        return call_price + put_price
    
    @property
    def total_cost(self) -> float:
        """
        Alias pour price() pour compatibilité avec les autres stratégies
        
        Returns:
            Prix total du straddle
        """
        return self.price()
    
    def break_even_points(self) -> Tuple[float, float]:
        """
        Calcule les points morts (break-even) de la stratégie
        
        Returns:
            Tuple (lower_break_even, upper_break_even)
        """
        total_premium = self.price()
        
        lower_be = self.K - total_premium
        upper_be = self.K + total_premium
        
        return lower_be, upper_be
    
    def payoff_at_expiry(self, S_T: float) -> float:
        """
        Calcule le payoff à l'échéance pour un prix donné du sous-jacent
        (sans inclure le coût initial)
        
        Args:
            S_T: Prix du sous-jacent à l'échéance
            
        Returns:
            Payoff brut à l'échéance
        """
        call_payoff = max(S_T - self.K, 0)
        put_payoff = max(self.K - S_T, 0)
        
        return call_payoff + put_payoff
    
    def profit_at_expiry(self, S_T: float) -> float:
        """
        Calcule le profit/perte net à l'échéance
        
        Args:
            S_T: Prix du sous-jacent à l'échéance
            
        Returns:
            Profit net (payoff - coût initial)
        """
        initial_cost = self.price()
        payoff = self.payoff_at_expiry(S_T)
        
        return payoff - initial_cost
    
    def greeks(self) -> Dict[str, float]:
        """
        Calcule les Greeks combinés du straddle
        
        Returns:
            Dictionnaire avec les Greeks de la stratégie
        """
        call_greeks = get_greeks(self.call)
        put_greeks = get_greeks(self.put)
        
        return {
            'delta': call_greeks['delta'] + put_greeks['delta'],
            'gamma': call_greeks['gamma'] + put_greeks['gamma'],
            'vega': call_greeks['vega'] + put_greeks['vega'],
            'theta': call_greeks['theta'] + put_greeks['theta'],
            'rho': call_greeks['rho'] + put_greeks['rho']
        }
    
    def max_loss(self) -> float:
        """
        Calcule la perte maximale (limitée au coût d'achat)
        
        Returns:
            Perte maximale
        """
        return self.price()
    
    def max_profit(self) -> float:
        """
        Profit maximum théorique (illimité)
        
        Returns:
            float('inf') car le profit est théoriquement illimité
        """
        return float('inf')
    
    def summary(self) -> Dict:
        """
        Génère un résumé complet de la stratégie
        
        Returns:
            Dictionnaire avec toutes les informations importantes
        """
        call_price = self.call.price()
        put_price = self.put.price()
        total_price = call_price + put_price
        lower_be, upper_be = self.break_even_points()
        greeks = self.greeks()
        
        return {
            'strategy': 'Long Straddle',
            'spot_price': self.S,
            'strike': self.K,
            'time_to_expiry_years': self.T,
            'time_to_expiry_days': int(self.T * 365),
            'volatility': self.sigma,
            'risk_free_rate': self.r,
            'call_price': call_price,
            'put_price': put_price,
            'total_cost': total_price,
            'max_loss': total_price,
            'max_profit': 'Unlimited',
            'lower_break_even': lower_be,
            'upper_break_even': upper_be,
            'break_even_move_pct': ((upper_be - self.S) / self.S) * 100,
            'greeks': greeks
        }
    
    def __repr__(self) -> str:
        """Représentation en string de la stratégie"""
        summary = self.summary()
        return (
            f"LongStraddle(S={self.S:.2f}, K={self.K:.2f}, "
            f"T={self.T:.4f}y, Cost={summary['total_cost']:.2f})"
        )


def analyze_straddle(ticker: str, strike: Optional[float] = None,
                     days_to_expiry: int = 30) -> Dict:
    """
    Fonction utilitaire pour analyser rapidement un straddle
    
    Args:
        ticker: Symbole du ticker
        strike: Prix d'exercice (None pour ATM)
        days_to_expiry: Jours jusqu'à échéance
        
    Returns:
        Résumé complet de la stratégie
    """
    straddle = LongStraddle.from_ticker(ticker, strike, days_to_expiry)
    return straddle.summary()
