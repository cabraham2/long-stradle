"""
Market Data Fetcher
Module pour récupérer les données de marché depuis Yahoo Finance
"""

import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict


def get_spot_price(ticker: str) -> float:
    """
    Récupère le prix spot actuel d'un sous-jacent
    
    Args:
        ticker: Le symbole du ticker (ex: 'AAPL', 'MSFT')
        
    Returns:
        Le prix spot actuel
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d')
    
    if data.empty:
        raise ValueError(f"Aucune donnée disponible pour {ticker}")
    
    return float(data['Close'].iloc[-1])


def get_historical_volatility(ticker: str, period: int = 252) -> float:
    """
    Calcule la volatilité historique annualisée
    
    Args:
        ticker: Le symbole du ticker
        period: Nombre de jours de trading pour le calcul (défaut: 252)
        
    Returns:
        La volatilité annualisée (en décimal, pas en %)
    """
    stock = yf.Ticker(ticker)
    
    # Récupérer les données historiques
    end_date = datetime.now()
    start_date = end_date - timedelta(days=int(period * 1.5))  # Marge pour les jours non-trading
    
    data = stock.history(start=start_date, end=end_date)
    
    if len(data) < 30:
        raise ValueError(f"Pas assez de données historiques pour {ticker}")
    
    # Calculer les rendements logarithmiques
    returns = np.log(data['Close'] / data['Close'].shift(1))
    returns = returns.dropna()
    
    # Volatilité annualisée
    volatility = returns.std() * np.sqrt(252)
    
    return float(volatility)


def get_risk_free_rate() -> float:
    """
    Récupère le taux sans risque approximatif (US Treasury 3-month)
    
    Returns:
        Le taux sans risque annualisé (en décimal)
    """
    try:
        treasury = yf.Ticker("^IRX")  # 13 Week Treasury Bill
        data = treasury.history(period='5d')
        
        if not data.empty:
            # Le taux est en pourcentage, on le convertit en décimal
            rate = float(data['Close'].iloc[-1]) / 100
            return rate
    except:
        pass
    
    # Valeur par défaut si échec
    return 0.05  # 5% par défaut


def get_market_data(ticker: str, 
                    volatility_period: int = 252) -> Tuple[float, float, float]:
    """
    Récupère toutes les données de marché nécessaires pour le pricing
    
    Args:
        ticker: Le symbole du ticker
        volatility_period: Période pour le calcul de volatilité
        
    Returns:
        Tuple (spot_price, volatility, risk_free_rate)
    """
    spot_price = get_spot_price(ticker)
    volatility = get_historical_volatility(ticker, volatility_period)
    risk_free_rate = get_risk_free_rate()
    
    return spot_price, volatility, risk_free_rate


def get_dividend_yield(ticker: str) -> float:
    """
    Récupère le rendement du dividende
    
    Args:
        ticker: Le symbole du ticker
        
    Returns:
        Le rendement du dividende annualisé (en décimal)
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        dividend_yield = info.get('dividendYield', 0.0)
        if dividend_yield is None:
            dividend_yield = 0.0
            
        return float(dividend_yield)
    except:
        return 0.0


def validate_ticker(ticker: str) -> bool:
    """
    Vérifie si un ticker est valide
    
    Args:
        ticker: Le symbole du ticker
        
    Returns:
        True si le ticker est valide, False sinon
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        return not data.empty
    except:
        return False


def get_ticker_info(ticker: str) -> Dict:
    """
    Récupère les informations détaillées d'un ticker
    
    Args:
        ticker: Le symbole du ticker
        
    Returns:
        Dictionnaire avec les informations du ticker
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    history = stock.history(period='5d')
    
    if history.empty:
        raise ValueError(f"Aucune donnée disponible pour {ticker}")
    
    # Prix actuel et précédent
    current_price = float(history['Close'].iloc[-1])
    previous_close = info.get('previousClose', current_price)
    
    # Calcul de la variation
    day_change = current_price - previous_close
    day_change_pct = (day_change / previous_close) * 100 if previous_close else 0
    
    # Market cap
    market_cap = info.get('marketCap', 0)
    
    # Formater le market cap
    if market_cap >= 1e12:
        market_cap_str = f"${market_cap/1e12:.2f}T"
    elif market_cap >= 1e9:
        market_cap_str = f"${market_cap/1e9:.2f}B"
    elif market_cap >= 1e6:
        market_cap_str = f"${market_cap/1e6:.2f}M"
    else:
        market_cap_str = f"${market_cap:,.0f}"
    
    return {
        'ticker': ticker.upper(),
        'name': info.get('longName', ticker),
        'currency': info.get('currency', 'USD'),
        'current_price': current_price,
        'previous_close': previous_close,
        'day_change': day_change,
        'day_change_pct': day_change_pct,
        'market_cap': market_cap,
        'market_cap_str': market_cap_str,
        'volume': info.get('volume', 0),
        'avg_volume': info.get('averageVolume', 0),
        'day_high': history['High'].iloc[-1],
        'day_low': history['Low'].iloc[-1],
        'week_52_high': info.get('fiftyTwoWeekHigh', 0),
        'week_52_low': info.get('fiftyTwoWeekLow', 0),
        'sector': info.get('sector', 'N/A'),
        'industry': info.get('industry', 'N/A'),
    }
