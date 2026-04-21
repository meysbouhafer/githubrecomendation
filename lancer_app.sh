#!/bin/bash

# Lancer l'application Streamlit GUI
# Pour Linux/Mac: chmod +x lancer_app.sh && ./lancer_app.sh

echo ""
echo "============================================================"
echo "  🐙 GitHub Repo Recommender"
echo "  Interface Graphique Streamlit"
echo "============================================================"
echo ""

# Vérifier si Python est disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Erreur: Python n'est pas installé"
    exit 1
fi

echo "✅ Python détecté"

# Vérifier si Streamlit est installé
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "⚠️  Installation de Streamlit..."
    python3 -m pip install streamlit -q
    echo "✅ Streamlit installé"
fi

# Vérifier toutes les dépendances
echo ""
echo "Vérification des dépendances..."
python3 -m pip install -r requirements.txt -q
echo "✅ Dépendances prêtes"

# Lancer l'app
echo ""
echo "🚀 Démarrage de l'application..."
echo "   Interface disponible à: http://localhost:8501"
echo ""
echo "💡 Appuyez sur Ctrl+C pour arrêter"
echo ""

python3 -m streamlit run app.py

echo ""
echo "👋 Application arrêtée"
