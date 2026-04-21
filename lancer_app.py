"""
Script de lancement - GitHub Repo Recommender
=============================================
Lance l'application Streamlit automatiquement.
"""

import subprocess
import sys
import webbrowser
import time
import os

def main():
    print("=" * 60)
    print("  🐙 GITHUB REPO RECOMMENDER")
    print("  Lancement de l'interface graphique...")
    print("=" * 60)
    
    # Vérifier si streamlit est installé
    try:
        import streamlit
        print("✅ Streamlit détecté")
    except ImportError:
        print("❌ Streamlit n'est pas installé")
        print("Installation en cours...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "-q"])
        print("✅ Streamlit installé")
    
    # Vérifier autres dépendances
    deps = ['pandas', 'numpy', 'sklearn', 'nltk', 'matplotlib', 'plotly']
    for dep in deps:
        try:
            __import__(dep)
            print(f"✅ {dep} installé")
        except ImportError:
            print(f"⚠️  {dep} manquant - installation...")
            pip_name = 'scikit-learn' if dep == 'sklearn' else dep
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name, "-q"])
    
    print("\n" + "=" * 60)
    print("✅ Toutes les dépendances sont prêtes !")
    print("=" * 60)
    
    print("\n🚀 Démarrage de l'application...")
    print("   L'interface s'ouvrira automatiquement dans votre navigateur")
    print("   (Si ce n'est pas le cas, rendez-vous sur: http://localhost:8501)")
    print("\n💡 Appuyez sur Ctrl+C pour arrêter l'application\n")
    
    # Attendre un peu avant d'ouvrir le navigateur
    time.sleep(3)
    webbrowser.open("http://localhost:8501")
    
    # Lancer streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Application arrêtée")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
