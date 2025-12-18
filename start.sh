#!/bin/bash

# Script de démarrage pour l'application Options Pricer

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║               OPTIONS PRICER - LONG STRADDLE                        ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✓ Python 3 détecté: $(python3 --version)"
echo ""

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    echo "✓ Environnement virtuel créé"
    echo ""
fi

# Activer l'environnement virtuel
echo "🔄 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -q -r requirements.txt
echo "✓ Dépendances installées"
echo ""

# Menu de choix
echo "Choisissez une option:"
echo "  1) 🖥️  Interface Terminal (mode interactif)"
echo "  2) 🌐 Interface Web (serveur Flask)"
echo "  3) 🎬 Démonstration rapide"
echo "  4) 📊 Mode démo terminal"
echo ""
read -p "Votre choix (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🖥️  Lancement de l'interface terminal..."
        echo ""
        python main.py
        ;;
    2)
        echo ""
        echo "🌐 Lancement du serveur web..."
        echo ""
        python web_app.py
        ;;
    3)
        echo ""
        echo "🎬 Lancement de la démonstration..."
        echo ""
        python examples/demo.py
        ;;
    4)
        echo ""
        echo "📊 Lancement du mode démo..."
        echo ""
        python main.py --demo
        ;;
    *)
        echo ""
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

# Désactiver l'environnement virtuel à la fin
deactivate
