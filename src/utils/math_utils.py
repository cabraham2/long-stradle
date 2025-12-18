"""
Financial Mathematics Utilities
Fonctions mathématiques pour les calculs financiers
"""

import numpy as np
from scipy.stats import norm
from typing import Tuple


def calculate_d1(S: float, K: float, T: float, r: float, 
                 sigma: float, q: float = 0.0) -> float:
    """
    Calcule d1 pour le modèle Black-Scholes
    
    Args:
        S: Prix spot du sous-jacent
        K: Prix d'exercice (strike)
        T: Temps jusqu'à l'échéance (en années)
        r: Taux sans risque
        sigma: Volatilité implicite
        q: Rendement du dividende (défaut: 0)
        
    Returns:
        La valeur de d1
    """
    if T <= 0:
        raise ValueError("Le temps jusqu'à l'échéance doit être positif")
    
    if sigma <= 0:
        raise ValueError("La volatilité doit être positive")
    
    numerator = np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T
    denominator = sigma * np.sqrt(T)
    
    return numerator / denominator


def calculate_d2(d1: float, sigma: float, T: float) -> float:
    """
    Calcule d2 pour le modèle Black-Scholes
    
    Args:
        d1: Valeur de d1
        sigma: Volatilité implicite
        T: Temps jusqu'à l'échéance (en années)
        
    Returns:
        La valeur de d2
    """
    return d1 - sigma * np.sqrt(T)


def calculate_d1_d2(S: float, K: float, T: float, r: float, 
                    sigma: float, q: float = 0.0) -> Tuple[float, float]:
    """
    Calcule d1 et d2 pour le modèle Black-Scholes
    
    Args:
        S: Prix spot du sous-jacent
        K: Prix d'exercice
        T: Temps jusqu'à l'échéance (en années)
        r: Taux sans risque
        sigma: Volatilité
        q: Rendement du dividende (défaut: 0)
        
    Returns:
        Tuple (d1, d2)
    """
    d1 = calculate_d1(S, K, T, r, sigma, q)
    d2 = calculate_d2(d1, sigma, T)
    
    return d1, d2


def standard_normal_cdf(x: float) -> float:
    """
    Fonction de répartition de la loi normale standard
    
    Args:
        x: Valeur pour laquelle calculer la CDF
        
    Returns:
        La probabilité cumulative
    """
    return norm.cdf(x)


def standard_normal_pdf(x: float) -> float:
    """
    Fonction de densité de la loi normale standard
    
    Args:
        x: Valeur pour laquelle calculer la PDF
        
    Returns:
        La densité de probabilité
    """
    return norm.pdf(x)


def years_to_expiry(days: int) -> float:
    """
    Convertit des jours en fraction d'année
    
    Args:
        days: Nombre de jours jusqu'à l'échéance
        
    Returns:
        Temps en années
    """
    return days / 365.0


def annualize_volatility(daily_vol: float) -> float:
    """
    Annualise une volatilité journalière
    
    Args:
        daily_vol: Volatilité journalière
        
    Returns:
        Volatilité annualisée
    """
    return daily_vol * np.sqrt(252)
