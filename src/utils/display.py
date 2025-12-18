"""
Display utilities with colors for terminal output
Module pour afficher des données avec des couleurs dans le terminal
"""

from colorama import Fore, Back, Style, init

# Initialiser colorama
init(autoreset=True)


def print_header(text: str):
    """Affiche un en-tête stylisé"""
    print(f"\n{Back.BLUE}{Fore.WHITE}{Style.BRIGHT} {text} {Style.RESET_ALL}")


def print_section(text: str):
    """Affiche une section"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}━━━ {text} ━━━{Style.RESET_ALL}")


def print_success(text: str):
    """Affiche un message de succès"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")


def print_error(text: str):
    """Affiche un message d'erreur"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")


def print_warning(text: str):
    """Affiche un avertissement"""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")


def print_info(text: str):
    """Affiche une information"""
    print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")


def colored_number(value: float, show_sign: bool = True) -> str:
    """
    Retourne un nombre coloré en fonction de sa valeur
    
    Args:
        value: La valeur numérique
        show_sign: Afficher le signe + pour les positifs
        
    Returns:
        String avec couleur
    """
    if value > 0:
        sign = "+" if show_sign else ""
        return f"{Fore.GREEN}{Style.BRIGHT}{sign}{value:.2f}{Style.RESET_ALL}"
    elif value < 0:
        return f"{Fore.RED}{Style.BRIGHT}{value:.2f}{Style.RESET_ALL}"
    else:
        return f"{Fore.WHITE}{value:.2f}{Style.RESET_ALL}"


def colored_percentage(value: float, show_sign: bool = True) -> str:
    """
    Retourne un pourcentage coloré
    
    Args:
        value: La valeur en pourcentage
        show_sign: Afficher le signe + pour les positifs
        
    Returns:
        String avec couleur et symbole %
    """
    if value > 0:
        sign = "+" if show_sign else ""
        return f"{Fore.GREEN}{Style.BRIGHT}{sign}{value:.2f}%{Style.RESET_ALL}"
    elif value < 0:
        return f"{Fore.RED}{Style.BRIGHT}{value:.2f}%{Style.RESET_ALL}"
    else:
        return f"{Fore.WHITE}{value:.2f}%{Style.RESET_ALL}"


def print_ticker_info(info: dict):
    """
    Affiche les informations d'un ticker de manière formatée
    
    Args:
        info: Dictionnaire avec les informations du ticker
    """
    print_header(f" {info['ticker']} - {info['name']} ")
    
    # Section Prix
    print_section("Prix et Variation")
    print(f"  Prix actuel:        {Fore.CYAN}{Style.BRIGHT}{info['currency']} {info['current_price']:.2f}{Style.RESET_ALL}")
    print(f"  Clôture précédente: {info['currency']} {info['previous_close']:.2f}")
    
    change_str = colored_number(info['day_change'])
    change_pct_str = colored_percentage(info['day_change_pct'])
    print(f"  Variation:          {change_str} ({change_pct_str})")
    
    # Section Marché
    print_section("Informations de Marché")
    print(f"  Capitalisation:     {Fore.YELLOW}{info['market_cap_str']}{Style.RESET_ALL}")
    print(f"  Volume:             {info['volume']:,}")
    print(f"  Volume moyen:       {info['avg_volume']:,}")
    
    # Section Range
    print_section("Fourchette")
    print(f"  Jour:               {info['day_low']:.2f} - {info['day_high']:.2f}")
    print(f"  52 semaines:        {info['week_52_low']:.2f} - {info['week_52_high']:.2f}")
    
    # Section Secteur
    if info['sector'] != 'N/A':
        print_section("Secteur")
        print(f"  Secteur:            {info['sector']}")
        print(f"  Industrie:          {info['industry']}")


def print_straddle_summary(summary: dict):
    """
    Affiche le résumé d'un straddle de manière formatée
    
    Args:
        summary: Dictionnaire avec le résumé du straddle
    """
    print_header(" Analyse Long Straddle ")
    
    # Paramètres
    print_section("Paramètres")
    print(f"  Strike:             ${summary['strike']:.2f}")
    print(f"  Échéance:           {summary['time_to_expiry_days']} jours ({summary['time_to_expiry_years']:.4f} ans)")
    print(f"  Volatilité:         {summary['volatility']*100:.2f}%")
    print(f"  Taux sans risque:   {summary['risk_free_rate']*100:.2f}%")
    
    # Prix
    print_section("Pricing")
    print(f"  Prix Call:          {Fore.CYAN}${summary['call_price']:.2f}{Style.RESET_ALL}")
    print(f"  Prix Put:           {Fore.CYAN}${summary['put_price']:.2f}{Style.RESET_ALL}")
    print(f"  Coût Total:         {Fore.YELLOW}{Style.BRIGHT}${summary['total_cost']:.2f}{Style.RESET_ALL}")
    
    # Risque/Rendement
    print_section("Risque & Rendement")
    print(f"  Perte maximale:     {Fore.RED}${summary['max_loss']:.2f}{Style.RESET_ALL}")
    print(f"  Profit maximum:     {Fore.GREEN}{summary['max_profit']}{Style.RESET_ALL}")
    print(f"  Break-even inf.:    ${summary['lower_break_even']:.2f}")
    print(f"  Break-even sup.:    ${summary['upper_break_even']:.2f}")
    print(f"  Mouvement requis:   {Fore.YELLOW}±{summary['break_even_move_pct']:.2f}%{Style.RESET_ALL}")
    
    # Greeks
    print_section("Greeks")
    greeks = summary['greeks']
    print(f"  Delta:              {greeks['delta']:.4f}")
    print(f"  Gamma:              {Fore.GREEN}{greeks['gamma']:.4f}{Style.RESET_ALL}")
    print(f"  Vega:               {Fore.GREEN}{greeks['vega']:.4f}{Style.RESET_ALL}")
    print(f"  Theta:              {Fore.RED}{greeks['theta']:.4f}{Style.RESET_ALL}")
    print(f"  Rho:                {greeks['rho']:.4f}")


def print_profit_table(straddle, scenarios: list):
    """
    Affiche un tableau de profits/pertes
    
    Args:
        straddle: Instance de LongStraddle
        scenarios: Liste de pourcentages de variation
    """
    print_section("Scénarios de Profit/Perte")
    
    print(f"\n  {Fore.CYAN}Prix spot actuel: ${straddle.S:.2f}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Coût du straddle: ${straddle.price():.2f}{Style.RESET_ALL}\n")
    
    # En-tête
    print(f"  {'Prix Final':<15} {'Variation':<12} {'Payoff':<12} {'P&L Net':<12} {'Statut'}")
    print(f"  {'-'*70}")
    
    for pct in scenarios:
        final_price = straddle.S * (1 + pct/100)
        profit = straddle.profit_at_expiry(final_price)
        payoff = straddle.payoff_at_expiry(final_price)
        
        if profit > 0:
            status = f"{Fore.GREEN}✓ PROFIT{Style.RESET_ALL}"
            pnl_str = f"{Fore.GREEN}${profit:.2f}{Style.RESET_ALL}"
        elif profit < 0:
            status = f"{Fore.RED}✗ PERTE{Style.RESET_ALL}"
            pnl_str = f"{Fore.RED}${profit:.2f}{Style.RESET_ALL}"
        else:
            status = f"{Fore.YELLOW}= BREAK-EVEN{Style.RESET_ALL}"
            pnl_str = f"${profit:.2f}"
        
        var_str = colored_percentage(pct)
        
        print(f"  ${final_price:<14.2f} {var_str:<20} ${payoff:<11.2f} {pnl_str:<20} {status}")


def print_banner():
    """Affiche une bannière stylisée"""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║               {Fore.YELLOW}OPTIONS PRICER - LONG STRADDLE{Fore.CYAN}                      ║
║                                                                      ║
║          {Fore.WHITE}Pricing d'options avec modèle Black-Scholes{Fore.CYAN}            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)


def input_prompt(message: str) -> str:
    """
    Affiche un prompt stylisé pour l'input utilisateur
    
    Args:
        message: Le message à afficher
        
    Returns:
        L'input de l'utilisateur
    """
    return input(f"{Fore.YELLOW}❯ {message}{Style.RESET_ALL} ")
