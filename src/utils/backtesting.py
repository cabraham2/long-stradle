"""
Backtesting historique pour stratégies d'options
Teste les stratégies sur données historiques réelles
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from ..models.black_scholes import Call, Put


class Backtester:
    """Backtesting de stratégies d'options sur données historiques"""
    
    def __init__(self, ticker: str, start_date: str, end_date: str):
        """
        Initialise le backtester
        
        Args:
            ticker: Symbole du ticker
            start_date: Date de début (format 'YYYY-MM-DD')
            end_date: Date de fin (format 'YYYY-MM-DD')
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Charge les données historiques depuis Yahoo Finance"""
        ticker_obj = yf.Ticker(self.ticker)
        self.data = ticker_obj.history(start=self.start_date, end=self.end_date)
        
        if self.data.empty:
            raise ValueError(f"Aucune donnée disponible pour {self.ticker} entre {self.start_date} et {self.end_date}")
        
        # Calcul des rendements et volatilité historique
        self.data['Returns'] = self.data['Close'].pct_change()
        self.data['Volatility'] = self.data['Returns'].rolling(window=30).std() * np.sqrt(252)
    
    def calculate_historical_volatility(self, window: int = 30) -> pd.Series:
        """
        Calcule la volatilité historique roulante
        
        Args:
            window: Fenêtre de calcul en jours
            
        Returns:
            Série de volatilités
        """
        returns = self.data['Close'].pct_change()
        volatility = returns.rolling(window=window).std() * np.sqrt(252)
        return volatility
    
    def backtest_strategy(self, strategy_class, 
                         holding_period_days: int = 30,
                         rebalance_frequency_days: int = 30,
                         **strategy_params) -> Dict:
        """
        Backtest une stratégie sur la période historique
        
        Args:
            strategy_class: Classe de la stratégie (LongStraddle, LongStrangle, etc.)
            holding_period_days: Durée de détention de la position
            rebalance_frequency_days: Fréquence de rééquilibrage
            **strategy_params: Paramètres additionnels pour la stratégie
            
        Returns:
            Résultats du backtest
        """
        results = []
        trades = []
        
        # Parcourir les dates avec la fréquence de rééquilibrage
        dates = self.data.index[::rebalance_frequency_days]
        
        for i, entry_date in enumerate(dates):
            # Vérifier qu'on a assez de données pour le holding period
            exit_date = entry_date + timedelta(days=holding_period_days)
            if exit_date not in self.data.index:
                # Trouver la date la plus proche
                future_dates = self.data.index[self.data.index > exit_date]
                if len(future_dates) == 0:
                    break
                exit_date = future_dates[0]
            
            # Prix d'entrée et de sortie
            entry_price = self.data.loc[entry_date, 'Close']
            exit_price = self.data.loc[exit_date, 'Close']
            
            # Volatilité historique au moment de l'entrée
            volatility = self.data.loc[entry_date, 'Volatility']
            if pd.isna(volatility) or volatility <= 0:
                volatility = 0.3  # Valeur par défaut
            
            # Créer la stratégie
            try:
                time_to_expiry_years = holding_period_days / 365.0
                
                # Construction selon le type de stratégie
                if strategy_class.__name__ == 'LongStraddle':
                    from ..strategies.long_straddle import LongStraddle
                    strike = strategy_params.get('strike', entry_price)
                    call = Call(entry_price, strike, time_to_expiry_years, 0.05, volatility)
                    put = Put(entry_price, strike, time_to_expiry_years, 0.05, volatility)
                    strategy = LongStraddle(call, put)
                
                elif strategy_class.__name__ == 'LongStrangle':
                    from ..strategies.long_strangle import LongStrangle
                    otm_pct = strategy_params.get('otm_percent', 0.05)
                    call_strike = entry_price * (1 + otm_pct)
                    put_strike = entry_price * (1 - otm_pct)
                    call = Call(entry_price, call_strike, time_to_expiry_years, 0.05, volatility)
                    put = Put(entry_price, put_strike, time_to_expiry_years, 0.05, volatility)
                    strategy = LongStrangle(call, put)
                
                else:
                    continue
                
                # Calcul du P&L
                initial_cost = strategy.total_cost
                profit_at_exit = strategy.profit_at_expiry(exit_price)
                roi = (profit_at_exit / initial_cost) * 100 if initial_cost != 0 else 0
                
                trade = {
                    'entry_date': entry_date,
                    'exit_date': exit_date,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'price_change': exit_price - entry_price,
                    'price_change_pct': ((exit_price - entry_price) / entry_price) * 100,
                    'initial_cost': initial_cost,
                    'profit': profit_at_exit,
                    'roi': roi,
                    'volatility': volatility,
                    'holding_days': (exit_date - entry_date).days
                }
                
                trades.append(trade)
                results.append(profit_at_exit)
            
            except Exception as e:
                print(f"Erreur pour trade du {entry_date}: {e}")
                continue
        
        # Calcul des statistiques globales
        if not results:
            return {
                'success': False,
                'error': 'Aucun trade valide trouvé'
            }
        
        results_array = np.array(results)
        winning_trades = results_array[results_array > 0]
        losing_trades = results_array[results_array < 0]
        
        total_trades = len(results)
        winning_count = len(winning_trades)
        losing_count = len(losing_trades)
        win_rate = (winning_count / total_trades) * 100 if total_trades > 0 else 0
        
        avg_win = np.mean(winning_trades) if len(winning_trades) > 0 else 0
        avg_loss = np.mean(losing_trades) if len(losing_trades) > 0 else 0
        
        total_profit = np.sum(results)
        avg_profit = np.mean(results)
        
        # Profit factor
        total_gains = np.sum(winning_trades) if len(winning_trades) > 0 else 0
        total_losses = abs(np.sum(losing_trades)) if len(losing_trades) > 0 else 1
        profit_factor = total_gains / total_losses if total_losses != 0 else float('inf')
        
        # Sharpe ratio (simplifié)
        sharpe_ratio = (avg_profit / np.std(results)) * np.sqrt(252 / rebalance_frequency_days) if np.std(results) != 0 else 0
        
        # Maximum drawdown
        cumulative = np.cumsum(results)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = cumulative - running_max
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0
        
        return {
            'success': True,
            'ticker': self.ticker,
            'strategy': strategy_class.__name__,
            'period': f"{self.start_date} à {self.end_date}",
            'total_trades': total_trades,
            'winning_trades': winning_count,
            'losing_trades': losing_count,
            'win_rate': win_rate,
            'total_profit': total_profit,
            'avg_profit_per_trade': avg_profit,
            'avg_winning_trade': avg_win,
            'avg_losing_trade': avg_loss,
            'profit_factor': profit_factor,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'best_trade': np.max(results),
            'worst_trade': np.min(results),
            'holding_period_days': holding_period_days,
            'rebalance_frequency_days': rebalance_frequency_days,
            'trades': trades,
            'equity_curve': cumulative.tolist() if len(cumulative) > 0 else []
        }
    
    def compare_strategies(self, strategies: List[tuple], 
                          holding_period_days: int = 30) -> Dict:
        """
        Compare plusieurs stratégies sur la même période
        
        Args:
            strategies: Liste de tuples (strategy_class, params_dict)
            holding_period_days: Durée de détention
            
        Returns:
            Résultats comparatifs
        """
        comparison = {}
        
        for strategy_class, params in strategies:
            result = self.backtest_strategy(
                strategy_class,
                holding_period_days=holding_period_days,
                **params
            )
            
            if result['success']:
                comparison[strategy_class.__name__] = {
                    'win_rate': result['win_rate'],
                    'total_profit': result['total_profit'],
                    'avg_profit': result['avg_profit_per_trade'],
                    'profit_factor': result['profit_factor'],
                    'sharpe_ratio': result['sharpe_ratio'],
                    'max_drawdown': result['max_drawdown']
                }
        
        return comparison
    
    def optimal_holding_period(self, strategy_class,
                              min_days: int = 7,
                              max_days: int = 90,
                              step: int = 7,
                              **strategy_params) -> List[Dict]:
        """
        Trouve la période de détention optimale
        
        Args:
            strategy_class: Classe de stratégie
            min_days: Minimum de jours
            max_days: Maximum de jours
            step: Pas d'incrémentation
            **strategy_params: Paramètres de stratégie
            
        Returns:
            Liste de résultats par période
        """
        results = []
        
        for holding_days in range(min_days, max_days + 1, step):
            backtest_result = self.backtest_strategy(
                strategy_class,
                holding_period_days=holding_days,
                rebalance_frequency_days=holding_days,
                **strategy_params
            )
            
            if backtest_result['success']:
                results.append({
                    'holding_period': holding_days,
                    'total_profit': backtest_result['total_profit'],
                    'win_rate': backtest_result['win_rate'],
                    'sharpe_ratio': backtest_result['sharpe_ratio'],
                    'profit_factor': backtest_result['profit_factor']
                })
        
        return results
