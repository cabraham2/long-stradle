"""
Black-Scholes Option Pricing Model
Modèle de pricing pour options européennes
"""

import numpy as np
from typing import Dict
from ..utils.math_utils import (
    calculate_d1_d2,
    standard_normal_cdf,
    standard_normal_pdf
)


class BlackScholesOption:
    """
    Classe de base pour une option européenne
    """
    
    def __init__(self, S: float, K: float, T: float, r: float, 
                 sigma: float, q: float = 0.0):
        """
        Initialise les paramètres de l'option
        
        Args:
            S: Prix spot du sous-jacent
            K: Prix d'exercice (strike)
            T: Temps jusqu'à l'échéance (en années)
            r: Taux sans risque
            sigma: Volatilité implicite
            q: Rendement du dividende (défaut: 0)
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.q = q
        
        self._validate_parameters()
        
    def _validate_parameters(self):
        """Valide les paramètres d'entrée"""
        if self.S <= 0:
            raise ValueError("Le prix spot doit être positif")
        if self.K <= 0:
            raise ValueError("Le strike doit être positif")
        if self.T <= 0:
            raise ValueError("Le temps jusqu'à l'échéance doit être positif")
        if self.sigma <= 0:
            raise ValueError("La volatilité doit être positive")
    
    def _calculate_d1_d2(self):
        """Calcule d1 et d2"""
        return calculate_d1_d2(self.S, self.K, self.T, self.r, self.sigma, self.q)


class Call(BlackScholesOption):
    """Option Call européenne"""
    
    def price(self) -> float:
        """
        Calcule le prix de l'option call
        
        Returns:
            Prix de l'option call
        """
        d1, d2 = self._calculate_d1_d2()
        
        call_price = (
            self.S * np.exp(-self.q * self.T) * standard_normal_cdf(d1) -
            self.K * np.exp(-self.r * self.T) * standard_normal_cdf(d2)
        )
        
        return call_price
    
    def delta(self) -> float:
        """Calcule le delta de l'option call"""
        d1, _ = self._calculate_d1_d2()
        return np.exp(-self.q * self.T) * standard_normal_cdf(d1)
    
    def gamma(self) -> float:
        """Calcule le gamma de l'option"""
        d1, _ = self._calculate_d1_d2()
        return (
            np.exp(-self.q * self.T) * standard_normal_pdf(d1) /
            (self.S * self.sigma * np.sqrt(self.T))
        )
    
    def vega(self) -> float:
        """Calcule le vega de l'option (sensibilité à la volatilité)"""
        d1, _ = self._calculate_d1_d2()
        return (
            self.S * np.exp(-self.q * self.T) * 
            standard_normal_pdf(d1) * np.sqrt(self.T)
        ) / 100  # Divisé par 100 pour avoir le vega pour 1% de changement
    
    def theta(self) -> float:
        """Calcule le theta de l'option call (time decay)"""
        d1, d2 = self._calculate_d1_d2()
        
        term1 = -(
            self.S * standard_normal_pdf(d1) * self.sigma * 
            np.exp(-self.q * self.T)
        ) / (2 * np.sqrt(self.T))
        
        term2 = self.q * self.S * standard_normal_cdf(d1) * np.exp(-self.q * self.T)
        term3 = self.r * self.K * np.exp(-self.r * self.T) * standard_normal_cdf(d2)
        
        return (term1 - term2 + term3) / 365  # Par jour
    
    def rho(self) -> float:
        """Calcule le rho de l'option call (sensibilité au taux)"""
        _, d2 = self._calculate_d1_d2()
        return (
            self.K * self.T * np.exp(-self.r * self.T) * 
            standard_normal_cdf(d2)
        ) / 100  # Pour 1% de changement


class Put(BlackScholesOption):
    """Option Put européenne"""
    
    def price(self) -> float:
        """
        Calcule le prix de l'option put
        
        Returns:
            Prix de l'option put
        """
        d1, d2 = self._calculate_d1_d2()
        
        put_price = (
            self.K * np.exp(-self.r * self.T) * standard_normal_cdf(-d2) -
            self.S * np.exp(-self.q * self.T) * standard_normal_cdf(-d1)
        )
        
        return put_price
    
    def delta(self) -> float:
        """Calcule le delta de l'option put"""
        d1, _ = self._calculate_d1_d2()
        return -np.exp(-self.q * self.T) * standard_normal_cdf(-d1)
    
    def gamma(self) -> float:
        """Calcule le gamma de l'option (identique au call)"""
        d1, _ = self._calculate_d1_d2()
        return (
            np.exp(-self.q * self.T) * standard_normal_pdf(d1) /
            (self.S * self.sigma * np.sqrt(self.T))
        )
    
    def vega(self) -> float:
        """Calcule le vega de l'option (identique au call)"""
        d1, _ = self._calculate_d1_d2()
        return (
            self.S * np.exp(-self.q * self.T) * 
            standard_normal_pdf(d1) * np.sqrt(self.T)
        ) / 100
    
    def theta(self) -> float:
        """Calcule le theta de l'option put"""
        d1, d2 = self._calculate_d1_d2()
        
        term1 = -(
            self.S * standard_normal_pdf(d1) * self.sigma * 
            np.exp(-self.q * self.T)
        ) / (2 * np.sqrt(self.T))
        
        term2 = self.q * self.S * standard_normal_cdf(-d1) * np.exp(-self.q * self.T)
        term3 = self.r * self.K * np.exp(-self.r * self.T) * standard_normal_cdf(-d2)
        
        return (term1 + term2 - term3) / 365
    
    def rho(self) -> float:
        """Calcule le rho de l'option put"""
        _, d2 = self._calculate_d1_d2()
        return (
            -self.K * self.T * np.exp(-self.r * self.T) * 
            standard_normal_cdf(-d2)
        ) / 100


def price_call(S: float, K: float, T: float, r: float, 
               sigma: float, q: float = 0.0) -> float:
    """
    Fonction utilitaire pour pricer rapidement un call
    
    Args:
        S: Prix spot
        K: Strike
        T: Temps à l'échéance (années)
        r: Taux sans risque
        sigma: Volatilité
        q: Dividende yield
        
    Returns:
        Prix du call
    """
    call = Call(S, K, T, r, sigma, q)
    return call.price()


def price_put(S: float, K: float, T: float, r: float, 
              sigma: float, q: float = 0.0) -> float:
    """
    Fonction utilitaire pour pricer rapidement un put
    
    Args:
        S: Prix spot
        K: Strike
        T: Temps à l'échéance (années)
        r: Taux sans risque
        sigma: Volatilité
        q: Dividende yield
        
    Returns:
        Prix du put
    """
    put = Put(S, K, T, r, sigma, q)
    return put.price()


def get_greeks(option: BlackScholesOption) -> Dict[str, float]:
    """
    Calcule tous les Greeks pour une option
    
    Args:
        option: Instance de Call ou Put
        
    Returns:
        Dictionnaire avec tous les Greeks
    """
    return {
        'delta': option.delta(),
        'gamma': option.gamma(),
        'vega': option.vega(),
        'theta': option.theta(),
        'rho': option.rho()
    }
