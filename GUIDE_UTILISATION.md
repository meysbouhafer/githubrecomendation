<!-- 
GUIDE DE DÉMARRAGE RAPIDE
Système de Recommandation de Repositories GitHub - Interface GUI
========================================================
-->

# 🚀 GUIDE DE DÉMARRAGE RAPIDE

## ⚡ 3 Méthodes pour Lancer l'Application

### **Méthode 1 : Clic Rapide (Recommandée pour Windows)**

1. Ouvrez le dossier `c:\Users\GEEK\Desktop\files (1)`
2. **Double-cliquez** sur `lancer_app.bat`
3. L'application s'ouvre automatiquement dans votre navigateur ! 🎉

---

### **Méthode 2 : Terminal Python**

Ouvrez un terminal/PowerShell et exécutez :

```powershell
cd "c:\Users\GEEK\Desktop\files (1)"
python lancer_app.py
```

Puis visitez : http://localhost:8501

---

### **Méthode 3 : Streamlit Direct**

```powershell
cd "c:\Users\GEEK\Desktop\files (1)"
streamlit run app.py
```

---

## 📖 GUIDE D'UTILISATION COMPLÈTE

### **🏠 Page d'Accueil**

- **Bienvenue !** Présentation générale du système
- **Statistiques clés** : Nombre d'outils, outils gratuits, domaines couverts
- **Guide rapide** : Comment ça marche en 4 étapes
- **Exemples** : Requêtes que vous pouvez essayer

**→ Point de départ idéal !**

---

### **🎯 Page Recommandations (PRINCIPALE)**

C'est là que tout se passe ! ✨

#### 1. **Écrivez votre requête** 
   - Zone de texte : Décrivez votre besoin, domaine, niveau d'étude
   - Exemple : *"Je suis en médecine et je cherche des outils pour analyser des publications"*
   - Plus détaillé = meilleures recommandations !

#### 2. **Ajustez les filtres (optionnel)**
   ```
   ┌─────────────────────────────────┐
   │ Nombre de résultats : 1  [====]  5 → 10
   │ 
   │ Domaine: Tous les domaines ▼
   │ Prix:    Tous ▼
   └─────────────────────────────────┘
   ```

#### 3. **Cliquez sur "🚀 Chercher"**
   - L'IA traite votre texte
   - Calcule les similarités
   - Retourne les meilleurs résultats

#### 4. **Explorez les résultats**
   ```
   ┌─────────────────────────────────────┐
   │ #1 GitHub Copilot  💚 Excellent    │
   │    Score: 14.6% - Excellent match  │
   │                                      │
   │    Description: ...                 │
   │    Domaine: Informatique            │
   │    🔗 Visiter le site →             │
   └─────────────────────────────────────┘
   ```

**Résultats affichés avec:**
- ✅ Nom de l'outil
- 📊 Score de pertinence (pourcentage)
- 🏷️ Domaine et cas d'usage
- 💰 Type (Gratuit 💚 / Freemium 💛 / Payant ❤️)
- 🔗 Lien direct

---

### **📊 Page Exploration**

4 onglets pour explorer les données :

#### 📋 **Vue d'ensemble**
- Statistiques globales
- Répartition par prix (Pie chart)
- Top domaines (Barchart)

#### 📊 **Graphiques**
- Distribution de la longueur des descriptions
- Statistiques détaillées
- Histogrammes interactifs

#### 🔍 **Recherche**
- Trouvez un outil par son nom
- Recherche par mot-clé
- Affichage immédiat des résultats

#### 📄 **Table Complète**
- Tous les 5 000 repositories en tableau
- Colonnes: Nom, Description, Domaine, Besoin, Prix
- Triable et scrollable

---

### **📈 Page Statistiques**

#### 📊 **Métriques**
```
┌──────────────────┬──────────────────┬──────────────────┐
│  Precision@5     │    Recall@5      │    F1-score      │
│    76.0% 🟢      │    63.5% 🟡      │     0.692        │
└──────────────────┴──────────────────┴──────────────────┘
```

**Signification:**
- **Precision 76%** → 76 requêtes sur 100 donnent de vrais bons résultats
- **Recall 63.5%** → 63.5% des outils pertinents sont dans le top 5
- **F1-score** → Équilibre global

#### 🧪 **Tests**
- 4 requêtes d'exemple
- Résultats réels
- Vérification des bonnes réponses (✅)

---

### **ℹ️ Page À Propos**

- 🎓 Informations du projet académique
- 🔧 Stack technologique
- 🤖 Méthodes d'IA expliquées
- 📊 Pipeline NLP détaillé
- 📞 Support et contact

---

## 💡 CONSEILS D'UTILISATION

### ✅ Requêtes Efficaces

**Bonne requête :**
```
"Je suis étudiant en informatique, j'aime la data science et 
je cherche un outil pour écrire du code Python automatiquement"
```

**Pas assez efficace :**
```
"Je veux un outil"
```

### 🎯 **Utilisez des mots-clés**
- Votre domaine (informatique, médecine, droit, etc.)
- Votre niveau (étudiant, professionnel, chercheur)
- Ce que vous cherchez (code, présentation, traduction, etc.)
- Un cas d'usage spécifique

### 🔍 **Utilisez les filtres**
- **Domaine** : Affinez à votre spécialité
- **Prix** : Choisissez gratuit/freemium/payant
- **Nombre de résultats** : 3 pour rapide, 10 pour exhaustif

---

## 🎮 EXEMPLE COMPLET

### 📝 Scénario
Je suis étudiant en médecine et je dois analyser 50 articles scientifiques pour ma thèse.

### ⚙️ Étapes

1. **Allez sur "🎯 Recommandations"**

2. **Écrivez :**
```
Étudiant en médecine, j'ai besoin d'analyser et de résumer 
des articles scientifiques pour ma thèse. Cherche un outil IA.
```

3. **Paramètres :**
   - Résultats : 5
   - Domaine : Médecine (optionnel)
   - Prix : Tous

4. **Cliquez "🚀 Chercher"**

5. **Résultats affichés :**
   ```
   #1 Elicit      (34.8%)  ✅ Excellent match
   #2 Semantic Scholar (33.7%)  ✅ Excellent 
   #3 Connected Papers (31.0%)  🟢 Bon match
   #4 Scite      (30.6%)  🟢 Bon match
   #5 SciSpace    (29.3%)  🟢 Bon match
   ```

6. **Clic sur le lien** → Visitez l'outil !

---

## ⚙️ CONFIGURATION AVANCÉE

### **Changer le port (si 8501 est occupé)**
```powershell
streamlit run app.py --server.port 8502
```

### **Mode sans navigateur**
```powershell
streamlit run app.py --logger.level=error
```

### **Réinstaller les dépendances**
```powershell
pip install -r requirements.txt --upgrade
```

---

## 🐛 RÉSOLUTION DE PROBLÈMES

| Problème | Solution |
|----------|----------|
| **"Module not found"** | `pip install -r requirements.txt` |
| **"Port 8501 already in use"** | Utiliser `--server.port 8502` |
| **"CSV file not found"** | Vérifier que `github_top_repositories_V2.csv` est dans le même dossier |
| **App lente** | Réduire le nombre de résultats |
| **Pas de résultats** | Rédiger une requête plus détaillée |

---

## 📊 DONNÉES

### Dataset
- **Total:** 5 000 repositories GitHub
- **Gratuits:** 20 (21%)
- **Freemium:** 62 (66%)
- **Payants:** 12 (13%)

### Domaines
- Informatique, Éducation, Médecine, Recherche
- Design, Marketing, Droit, Sciences, etc.

### Cas d'usage
- Code & Programmation
- Rédaction & Texte
- Recherche Académique
- Présentation
- Image & Design
- Et bien d'autres !

---

## 🎓 INFORMATIONS ACADÉMIQUES

| Élément | Info |
|---------|------|
| **Université** | 8 Mai 45, Guelma |
| **Formation** | 4ème Année Ingénieur (4ING) |
| **Module** | Traitement du Langage Naturel (NLP) |
| **Année** | 2026 |
| **Groupe** | Ensemble du groupe NLP |

---

## 🛠️ VERSION PRÉCÉDENTE

L'ancienne version CLI est toujours disponible :
```powershell
python systeme_recommandation.py
```

Voir `README.md` pour plus de détails techniques.

---

## 📞 BESOIN D'AIDE ?

- 📖 Consultez le **README.md**
- 📧 Contactez l'équipe NLP
- 🐙 GitHub: [github.com/4ing-nlp](https://github.com)

---

**Bonne chance ! Amusez-vous bien avec l'application ! 🚀**

