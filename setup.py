"""
Installation et Setup - Système de Recommandation d'Outils IA
================================================================
Ce script installe toutes les dépendances et configure l'environnement
"""

import subprocess
import sys
import os
import platform

def print_header(title):
    """Affiche un titre formaté"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def print_step(step_num, total, message):
    """Affiche une étape"""
    print(f"[{step_num}/{total}] ⏳ {message}...")

def print_ok(message):
    """Affiche un message de succès"""
    print(f"    ✅ {message}")

def print_error(message):
    """Affiche un message d'erreur"""
    print(f"    ❌ {message}")
    
def print_warning(message):
    """Affiche un avertissement"""
    print(f"    ⚠️  {message}")

def check_python_version():
    """Vérifie que Python 3.8+ est installé"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ requis, vous avez Python {version.major}.{version.minor}")
        return False
    print_ok(f"Python {version.major}.{version.minor} détecté")
    return True

def install_packages():
    """Installe les packages Python"""
    packages = [
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "nltk>=3.6.0",
        "matplotlib>=3.4.0",
        "plotly>=5.0.0",
        "streamlit>=1.20.0",
        "gensim>=4.0.0",
    ]
    
    print_step(1, 4, "Installation des packages Python")
    
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print_ok("pip à jour")
    except Exception as e:
        print_warning(f"Impossible de mettre à jour pip: {e}")
    
    for package in packages:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package, "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            pkg_name = package.split(">=")[0]
            print_ok(f"{pkg_name} installé")
        except Exception as e:
            print_error(f"Impossible d'installer {package}")
            return False
    
    return True

def verify_dataset():
    """Vérifie que le dataset existe"""
    print_step(2, 4, "Vérification du dataset")
    
    if os.path.exists("ai_tools_dataset.csv"):
        file_size = os.path.getsize("ai_tools_dataset.csv") / 1024
        print_ok(f"Dataset trouvé ({file_size:.1f} KB)")
        return True
    else:
        print_error("ai_tools_dataset.csv non trouvé")
        print_warning("Assurez-vous que le fichier est dans le répertoire courant")
        return False

def download_nltk_resources():
    """Télécharge les ressources NLTK"""
    print_step(3, 4, "Téléchargement des ressources NLTK")
    
    try:
        import nltk
        resources = ['punkt', 'stopwords', 'punkt_tab']
        for resource in resources:
            try:
                nltk.download(resource, quiet=True)
                print_ok(f"Ressource '{resource}' téléchargée")
            except Exception:
                print_warning(f"Impossible de télécharger '{resource}'")
        return True
    except Exception as e:
        print_error(f"Erreur NLTK: {e}")
        return False

def test_imports():
    """Teste l'import de tous les modules"""
    print_step(4, 4, "Test des imports")
    
    modules = {
        'pandas': 'pd',
        'numpy': 'np',
        'sklearn': 'sklearn',
        'nltk': 'nltk',
        'matplotlib': 'mpl',
        'plotly': 'plotly',
        'streamlit': 'st',
    }
    
    all_ok = True
    for module, alias in modules.items():
        try:
            __import__(module)
            print_ok(f"{module} importable")
        except ImportError:
            print_error(f"{module} non disponible")
            all_ok = False
    
    return all_ok

def create_shortcuts():
    """Crée des raccourcis (Windows uniquement)"""
    if platform.system() != "Windows":
        return True
    
    # Raccourci Bureau
    desktop_path = os.path.expanduser("~/Desktop")
    shortcut_path = os.path.join(desktop_path, "IA Recommandations.lnk")
    
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = os.path.abspath("lancer_app.bat")
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.IconLocation = "🤖"
        shortcut.save()
        print_ok(f"Raccourci créé sur le Bureau")
        return True
    except Exception:
        print_warning("Impossible de créer le raccourci (non critique)")
        return True

def main():
    """Fonction principale"""
    
    print_header("🤖 INSTALLATION - Système de Recommandation d'Outils IA")
    
    # Vérifications préalables
    if not check_python_version():
        print_error("Installation annulée")
        return False
    
    # Installation
    if not install_packages():
        print_error("Erreur lors de l'installation des packages")
        return False
    
    # Vérification du dataset
    if not verify_dataset():
        print_warning("Le dataset est manquant - l'app ne fonctionnera pas correctement")
    
    # NLTK
    if not download_nltk_resources():
        print_warning("Certaines ressources NLTK n'ont pas pu être téléchargées")
    
    # Tests d'import
    if not test_imports():
        print_error("Certains modules n'ont pas pu être importés")
        return False
    
    # Raccourcis (Windows)
    if platform.system() == "Windows":
        create_shortcuts()
    
    # Succès
    print_header("✅ INSTALLATION RÉUSSIE !")
    
    print("""
    🚀 Pour lancer l'application:
    
    Option 1 (Windows):
        Double-cliquez sur: lancer_app.bat
    
    Option 2 (Terminal):
        python lancer_app.py
    
    Option 3 (Streamlit):
        streamlit run app.py
    
    📖 Documentation:
        - README.md
        - GUIDE_UTILISATION.md
        - RESUME_PROJET.md
    
    💡 L'application s'ouvrira à: http://localhost:8501
    """)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Installation interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)
