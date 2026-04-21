<!-- 
FICHIER INDEX - Accès rapide à toutes les ressources du projet
================================================================
-->

# 📑 INDEX DU PROJET - ACCÈS RAPIDE

## 🚀 LANCER L'APPLICATION

### **Clic Rapide (Windows)**
👉 **Double-cliquez sur:** `lancer_app.bat`

### **Terminal Python**
```bash
python lancer_app.py
```

### **Streamlit Direct**
```bash
streamlit run app.py
```

---

## 📂 STRUCTURE DU PROJET

```
files (1)/
│
├─ 🖥️ APPLICATION (GUI STREAMLIT)
│  ├─ app.py                    ← 🌟 App principale
│  ├─ lancer_app.py            ← Lanceur Python
│  ├─ lancer_app.bat           ← Lanceur Windows
│  ├─ lancer_app.sh            ← Lanceur Linux/Mac
│  └─ config.py                ← Configuration
│
├─ 📜 SCRIPTS (VERSION CLI)
│  └─ systeme_recommandation.py ← App texte
│
├─ 📦 ENVIRONNEMENT
│  ├─ requirements.txt          ← Dépendances
│  └─ setup.py                  ← Installation auto
│
├─ 📊 DONNÉES
│  ├─ github_top_repositories_V2.csv      ← 5 000 repositories GitHub
│  ├─ distribution_dataset.png  ← Graphique 1
│  ├─ comparaison_methodes.png  ← Graphique 2
│  └─ scores_recommandation.png ← Graphique 3
│
└─ 📚 DOCUMENTATION
   ├─ README.md                 ← Tech doc
   ├─ GUIDE_UTILISATION.md      ← Guide user
   ├─ RESUME_PROJET.md          ← Vue d'ensemble
   └─ INDEX.md                  ← Ce fichier
```

---

## 📖 FICHIERS DOCUMENTATION

| Fichier | Description | Pour qui |
|---------|-------------|----------|
| **README.md** | Documentation technique complète | Développeurs |
| **GUIDE_UTILISATION.md** | Guide étape par étape | Utilisateurs |
| **RESUME_PROJET.md** | Vue d'ensemble du projet | Tous |
| **INDEX.md** | Navigation rapide (ce fichier) | Tous |

---

## 🎯 PAR RÔLE - COMMENT UTILISER ?

### 👤 **Je suis utilisateur final**
1. **Double-cliquez:** `lancer_app.bat`
2. **Lire:** `GUIDE_UTILISATION.md`
3. **Utiliser** via l'interface http://localhost:8501

### 👨‍💻 **Je suis développeur**
1. **Installer:** `python setup.py`
2. **Lire:** `README.md`
3. **Personalliser:** Modifiez `config.py`
4. **Lancer:** `python app.py` ou `streamlit run app.py`

### 🎓 **Je fais un rapport/présentation**
1. **Lire:** `RESUME_PROJET.md` (vue d'ensemble)
2. **Explorer:** `GUIDE_UTILISATION.md` (exemples)
3. **Utiliser:** Captures d'écran de l'app

---

## ✨ PAGES DE L'APPLICATION

### 🏠 **Accueil** (`app.py` - page 0)
- Bienvenue et explications
- Stats globales
- Exemples de requêtes

### 🎯 **Recommandations** (`app.py` - page 1) ⭐ PRINCIPALE
- Zone de texte pour requête
- Filtres (domaine, prix, nombre résultats)
- Affichage des résultats avec scores
- Liens directs vers les outils

### 📊 **Exploration** (`app.py` - page 2)
- Vue d'ensemble (stats)
- Graphiques interactifs
- Recherche d'outils
- Table complète du dataset

### 📈 **Statistiques** (`app.py` - page 3)
- Métriques: Precision@5 (76%), Recall@5 (63.5%)
- F1-score détaillé
- Tests sur 4 requêtes d'exemple

### ⭐ **Favoris** (`app.py` - page 4) 🆕
- Ajouter des outils favoris
- Gérer votre collection
- Accès rapide à vos sélections

### ℹ️ **À propos** (`app.py` - page 5)
- Infos académiques
- Technologie utilisée
- Contact et support

---

## 🔧 FICHIERS DE CONFIGURATION

### `config.py` - Configuration centralisée
- Paramètres NLP
- Paramètres TF-IDF
- Paramètres Streamlit
- Strings UI
- Couleurs et styles

**Modifier pour:**
- Changer le nombre de résultats par défaut
- Ajuster la sensibilité des requêtes
- Personnaliser les couleurs
- Modifier les textes de l'interface

### `requirements.txt` - Dépendances
- pandas, numpy, scikit-learn
- nltk, matplotlib, plotly
- streamlit, gensim

---

## 🚨 RÉSOLUTION DE PROBLÈMES

### ❌ "ModuleNotFoundError"
```bash
python setup.py
# Ou:
pip install -r requirements.txt
```

### ❌ "Port 8501 already in use"
```bash
streamlit run app.py --server.port 8502
```

### ❌ "CSV not found"
⚠️ `github_top_repositories_V2.csv` doit être dans le même dossier

### ❌ "App très lente"
→ Réduisez les résultats (5 au lieu de 10)

### ❌ "Pas de résultats"
→ Écrivez une requête plus détaillée

---

## 📊 STATISTIQUES

| Métrique | Valeur |
|----------|--------|
| **Repositories GitHub** | 5 000 |
| **Domaines** | 15+ |
| **Précision** | 76% |
| **Pages GUI** | 6 |
| **Lignes code** | ~1,100 |
| **Dépendances** | 8 |

---

## 🎓 PROJET ACADÉMIQUE

- **Université:** 8 Mai 45, Guelma 🏫
- **Module:** Traitement du Langage Naturel (NLP)
- **Année:** 4ING (2025-2026)
- **Status:** ✅ Complet et fonctionnel

---

## 🛠️ INSTALLATION RAPIDE

### Méthode 1 : Auto-Installation
```bash
python setup.py
```

### Méthode 2 : Manuel
```bash
pip install -r requirements.txt
```

### Méthode 3 : Pas d'installation (si déjà installé)
```bash
python lancer_app.py
```

---

## 🚀 DÉMARRAGE RAPIDE

### 3 Étapes
1. **Ouvrir** le dossier du projet
2. **Double-cliquer** `lancer_app.bat`
3. **Attendre** que le navigateur s'ouvre

✓ **La app est prête !**

---

## 📋 CHECKLIST D'UTILISATION

- [ ] Tous les fichiers sont téléchargés
- [ ] Python 3.8+ est installé
- [ ] `lancer_app.bat` a été exécuté
- [ ] L'app s'ouvre sur http://localhost:8501
- [ ] Je peux écrire une requête et chercher
- [ ] Les résultats s'affichent
- [ ] Je peux explorer le dataset

✅ **Si tout est coché, l'app fonctionne parfaitement !**

---

## 🎯 PROCHAIN PAS

### Pour les utilisateurs
→ Allez sur [GUIDE_UTILISATION.md](GUIDE_UTILISATION.md)

### Pour les développeurs
→ Consultez [README.md](README.md)

### Pour le contexte complet
→ Lisez [RESUME_PROJET.md](RESUME_PROJET.md)

---

## ⚡ COMMANDES RAPIDES

```powershell
# Lancer l'app
python lancer_app.py

# Voir version Python
python --version

# Réinstaller dépendances
pip install -r requirements.txt --upgrade

# Lancer version CLI
python systeme_recommandation.py

# Lancer avec port personnalisé
streamlit run app.py --server.port 8502
```

---

## 🆘 SUPPORT

| Question | Réponse |
|----------|---------|
| **Ça ne démarre pas** | Lire: [GUIDE_UTILISATION.md](#) |
| **Mon requête ne donne rien** | Écrire plus de détails |
| **Je veux modifier l'app** | Éditer: `app.py`, `config.py` |
| **L'interface est lente** | Réduire les résultats |
| **Je veux les anciens outils** | Utiliser: `systeme_recommandation.py` |

---

## 📈 VERSIONS

- **v1.0** (CLI) → Script texte `systeme_recommandation.py`
- **v2.0** (GUI) → Application Streamlit `app.py` ✨ NOUVELLE

---

## 🎉 BIENVENUE !

**Vous êtes maintenant prêt à utiliser le système de recommandation de repositories GitHub!**

Amusez-vous bien ! 🚀

---

**Besoin d'aide?**
- 📖 Documentation: [README.md](README.md)
- 👤 Guide utilisateur: [GUIDE_UTILISATION.md](GUIDE_UTILISATION.md)
- 📋 Vue d'ensemble: [RESUME_PROJET.md](RESUME_PROJET.md)

**Made with ❤️ by NLP 4ING Team**

