"""
Système de Recommandation d'Outils IA pour Étudiants
======================================================
Projet NLP - 4ING - Université 8 Mai 45
Module : Traitement Automatique du Langage Naturel

Ce système recommande des outils IA adaptés à un étudiant
selon son domaine d'études et son besoin exprimé en texte libre.
"""

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
import warnings
warnings.filterwarnings('ignore')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# ─────────────────────────────────────────────────────────────────────────────
# 0. TÉLÉCHARGEMENT DES RESSOURCES NLTK
# ─────────────────────────────────────────────────────────────────────────────
def setup_nltk():
    for resource in ['punkt', 'stopwords', 'punkt_tab']:
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            pass

setup_nltk()

# ─────────────────────────────────────────────────────────────────────────────
# 1. CHARGEMENT ET EXPLORATION DU DATASET
# ─────────────────────────────────────────────────────────────────────────────
def charger_dataset(chemin='ai_tools_dataset.csv'):
    """Charge le dataset et affiche des statistiques descriptives."""
    df = pd.read_csv(chemin)
    print("=" * 60)
    print("EXPLORATION DU DATASET")
    print("=" * 60)
    print(f"Nombre d'outils : {len(df)}")
    print(f"Colonnes        : {list(df.columns)}")
    print(f"\nDistribution par type de prix :")
    print(df['gratuit'].value_counts().to_string())
    print(f"\nLongueur moyenne des descriptions : {df['description'].str.len().mean():.0f} caractères")

    # Créer un texte combiné pour la vectorisation
    df['texte_complet'] = (
        df['nom'] + ' ' +
        df['description'] + ' ' +
        df['domaine'] + ' ' +
        df['besoin']
    )
    return df

# ─────────────────────────────────────────────────────────────────────────────
# 2. PRÉTRAITEMENT NLP
# ─────────────────────────────────────────────────────────────────────────────
def pretraiter_texte(texte, langue='french'):
    """
    Pipeline de prétraitement NLP :
    1. Mise en minuscules
    2. Suppression de la ponctuation et des chiffres
    3. Tokenisation
    4. Suppression des stopwords
    5. Stemming
    """
    # Minuscules
    texte = texte.lower()

    # Suppression des caractères spéciaux et chiffres
    texte = re.sub(r'[^a-zàâäéèêëîïôùûüç\s]', ' ', texte)
    texte = re.sub(r'\s+', ' ', texte).strip()

    # Tokenisation
    try:
        tokens = word_tokenize(texte, language=langue)
    except Exception:
        tokens = texte.split()

    # Suppression des stopwords
    try:
        mots_vides_fr = set(stopwords.words('french'))
        mots_vides_en = set(stopwords.words('english'))
        mots_vides = mots_vides_fr | mots_vides_en
    except Exception:
        mots_vides = set()

    tokens = [t for t in tokens if t not in mots_vides and len(t) > 2]

    # Stemming (optionnel — commentez si vous préférez sans)
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens]

    return ' '.join(tokens)


def pretraiter_dataset(df):
    """Applique le prétraitement à tout le dataset."""
    print("\n" + "=" * 60)
    print("PRÉTRAITEMENT NLP")
    print("=" * 60)
    df['texte_traite'] = df['texte_complet'].apply(pretraiter_texte)
    print("Prétraitement terminé.")
    print("\nExemple avant :", df['texte_complet'].iloc[0][:80])
    print("Exemple après  :", df['texte_traite'].iloc[0][:80])
    return df

# ─────────────────────────────────────────────────────────────────────────────
# 3. MÉTHODE 1 : TF-IDF + SIMILARITÉ COSINUS
# ─────────────────────────────────────────────────────────────────────────────
class RecommandateurTFIDF:
    def __init__(self):
        self.vectoriseur = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True
        )
        self.matrice_tfidf = None
        self.df = None

    def entrainer(self, df):
        self.df = df
        self.matrice_tfidf = self.vectoriseur.fit_transform(df['texte_traite'])
        print(f"\n[TF-IDF] Matrice créée : {self.matrice_tfidf.shape}")

    def recommander(self, requete, top_k=5, filtre_domaine=None):
        """Retourne les top_k outils les plus similaires à la requête."""
        requete_traitee = pretraiter_texte(requete)
        vecteur_requete = self.vectoriseur.transform([requete_traitee])

        scores = cosine_similarity(vecteur_requete, self.matrice_tfidf).flatten()

        df_resultat = self.df.copy()
        df_resultat['score_tfidf'] = scores

        # Filtrage optionnel par domaine
        if filtre_domaine:
            masque = df_resultat['domaine'].str.lower().str.contains(
                filtre_domaine.lower(), na=False
            )
            df_resultat = df_resultat[masque]

        return df_resultat.nlargest(top_k, 'score_tfidf')[
            ['nom', 'description', 'domaine', 'besoin', 'gratuit', 'lien', 'score_tfidf']
        ].reset_index(drop=True)

# ─────────────────────────────────────────────────────────────────────────────
# 4. MÉTHODE 2 : WORD2VEC + SIMILARITÉ COSINUS
# ─────────────────────────────────────────────────────────────────────────────
class RecommandateurWord2Vec:
    def __init__(self):
        self.modele = None
        self.vecteurs_outils = None
        self.df = None

    def _phrase_vers_vecteur(self, texte):
        """Moyenne des vecteurs Word2Vec des tokens présents dans le modèle."""
        tokens = texte.split()
        vecteurs = [
            self.modele.wv[t] for t in tokens if t in self.modele.wv
        ]
        if not vecteurs:
            return np.zeros(self.modele.vector_size)
        return np.mean(vecteurs, axis=0)

    def entrainer(self, df):
        try:
            from gensim.models import Word2Vec
        except ImportError:
            print("[Word2Vec] gensim non installé. pip install gensim")
            return False

        self.df = df
        corpus = [texte.split() for texte in df['texte_traite']]

        self.modele = Word2Vec(
            sentences=corpus,
            vector_size=100,
            window=5,
            min_count=1,
            workers=2,
            epochs=20,
            seed=42
        )

        self.vecteurs_outils = np.array([
            self._phrase_vers_vecteur(texte) for texte in df['texte_traite']
        ])
        print(f"[Word2Vec] Modèle entraîné | Vocabulaire : {len(self.modele.wv)} mots")
        return True

    def recommander(self, requete, top_k=5, filtre_domaine=None):
        requete_traitee = pretraiter_texte(requete)
        vecteur_requete = self._phrase_vers_vecteur(requete_traitee).reshape(1, -1)

        scores = cosine_similarity(vecteur_requete, self.vecteurs_outils).flatten()

        df_resultat = self.df.copy()
        df_resultat['score_w2v'] = scores

        if filtre_domaine:
            masque = df_resultat['domaine'].str.lower().str.contains(
                filtre_domaine.lower(), na=False
            )
            df_resultat = df_resultat[masque]

        return df_resultat.nlargest(top_k, 'score_w2v')[
            ['nom', 'description', 'domaine', 'besoin', 'gratuit', 'lien', 'score_w2v']
        ].reset_index(drop=True)

# ─────────────────────────────────────────────────────────────────────────────
# 5. ÉVALUATION — Precision@K et Recall@K
# ─────────────────────────────────────────────────────────────────────────────

REQUETES_TEST = [
    {
        "requete": "je suis en informatique et je veux générer du code automatiquement",
        "pertinents": ["GitHub Copilot", "Tabnine", "Codeium", "Cursor", "Blackbox AI", "Replit AI"]
    },
    {
        "requete": "j'ai besoin de traduire des documents académiques en anglais",
        "pertinents": ["DeepL", "ChatGPT", "Claude", "Gemini", "QuillBot", "Wordtune"]
    },
    {
        "requete": "je veux trouver des articles scientifiques pour ma thèse",
        "pertinents": ["Elicit", "Consensus", "Research Rabbit", "Scite", "Semantic Scholar", "Connected Papers", "SciSpace"]
    },
    {
        "requete": "étudiant en médecine cherche à analyser des publications scientifiques",
        "pertinents": ["Elicit", "Consensus", "Scite", "SciSpace", "Research Rabbit", "Semantic Scholar"]
    },
    {
        "requete": "je veux créer une belle présentation pour mon exposé",
        "pertinents": ["Gamma", "Beautiful AI", "Tome", "Canva AI", "Copilot Microsoft", "Notion AI"]
    },
    {
        "requete": "étudiant en droit je cherche un outil pour analyser des contrats",
        "pertinents": ["Harvey AI", "Legalyze", "Casetext", "Lexis Plus AI", "Docusign AI"]
    },
    {
        "requete": "je veux générer des images pour mon projet de design graphique",
        "pertinents": ["Midjourney", "DALL-E 3", "Canva AI", "Adobe Firefly", "Leonardo AI", "Stable Diffusion"]
    },
    {
        "requete": "j'ai besoin de résumer un long document PDF rapidement",
        "pertinents": ["Humata", "ChatPDF", "Adobe Acrobat AI", "ChatGPT", "Claude", "SciSpace"]
    },
    {
        "requete": "apprendre les mathématiques et résoudre des équations",
        "pertinents": ["Wolfram Alpha", "Symbolab", "Photomath", "GeoGebra AI", "Desmos", "Khanmigo"]
    },
    {
        "requete": "je veux créer une vidéo pour mon projet multimédia",
        "pertinents": ["RunwayML", "Lumen5", "Pictory", "Synthesia", "Pika Labs", "Descript"]
    }
]


def evaluer_systeme(recommandeur, methode_nom, top_k=5):
    """Calcule Precision@K et Recall@K sur les requêtes de test."""
    precisions = []
    recalls = []

    for test in REQUETES_TEST:
        resultats = recommandeur.recommander(test["requete"], top_k=top_k)
        recommandes = set(resultats['nom'].tolist())
        pertinents = set(test["pertinents"])

        vrais_positifs = recommandes & pertinents
        precision = len(vrais_positifs) / top_k if top_k > 0 else 0
        recall = len(vrais_positifs) / len(pertinents) if pertinents else 0

        precisions.append(precision)
        recalls.append(recall)

    moy_precision = np.mean(precisions)
    moy_recall = np.mean(recalls)
    f1 = (2 * moy_precision * moy_recall / (moy_precision + moy_recall)
          if (moy_precision + moy_recall) > 0 else 0)

    print(f"\n{'─'*50}")
    print(f"ÉVALUATION — {methode_nom} (Top-{top_k})")
    print(f"{'─'*50}")
    print(f"  Precision@{top_k} moyenne : {moy_precision:.4f}  ({moy_precision*100:.1f}%)")
    print(f"  Recall@{top_k} moyenne    : {moy_recall:.4f}  ({moy_recall*100:.1f}%)")
    print(f"  F1-score                  : {f1:.4f}")

    return {
        "methode": methode_nom,
        "precision": moy_precision,
        "recall": moy_recall,
        "f1": f1,
        "precisions": precisions,
        "recalls": recalls
    }

# ─────────────────────────────────────────────────────────────────────────────
# 6. VISUALISATIONS
# ─────────────────────────────────────────────────────────────────────────────
def visualiser_distribution(df):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Exploration du dataset — Outils IA", fontsize=14)

    # Distribution par prix
    counts = df['gratuit'].value_counts()
    colors = ['#4CAF50', '#2196F3', '#FF9800']
    axes[0].bar(counts.index, counts.values, color=colors[:len(counts)])
    axes[0].set_title("Répartition par type de prix")
    axes[0].set_xlabel("Type")
    axes[0].set_ylabel("Nombre d'outils")
    for i, v in enumerate(counts.values):
        axes[0].text(i, v + 0.5, str(v), ha='center', fontweight='bold')

    # Longueur des descriptions
    longueurs = df['description'].str.len()
    axes[1].hist(longueurs, bins=20, color='#7B68EE', edgecolor='white')
    axes[1].set_title("Distribution de la longueur des descriptions")
    axes[1].set_xlabel("Nombre de caractères")
    axes[1].set_ylabel("Fréquence")
    axes[1].axvline(longueurs.mean(), color='red', linestyle='--',
                    label=f'Moyenne: {longueurs.mean():.0f}')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig('distribution_dataset.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n[Figure] distribution_dataset.png sauvegardée")


def visualiser_comparaison(resultats_tfidf, resultats_w2v, top_k=5):
    methodes = ['TF-IDF', 'Word2Vec']
    precisions = [resultats_tfidf['precision'], resultats_w2v['precision']]
    recalls = [resultats_tfidf['recall'], resultats_w2v['recall']]
    f1s = [resultats_tfidf['f1'], resultats_w2v['f1']]

    x = np.arange(len(methodes))
    largeur = 0.25

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"Comparaison des méthodes (Top-{top_k})", fontsize=14)

    # Barres de métriques
    bars1 = axes[0].bar(x - largeur, precisions, largeur, label='Precision', color='#4CAF50')
    bars2 = axes[0].bar(x,           recalls,    largeur, label='Recall',    color='#2196F3')
    bars3 = axes[0].bar(x + largeur, f1s,        largeur, label='F1-score',  color='#FF9800')

    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            h = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width()/2, h + 0.005,
                         f'{h:.2f}', ha='center', va='bottom', fontsize=9)

    axes[0].set_title("Métriques d'évaluation par méthode")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(methodes)
    axes[0].set_ylim(0, 1.1)
    axes[0].legend()
    axes[0].set_ylabel("Score")

    # Précision par requête de test
    requetes_courtes = [f"Q{i+1}" for i in range(len(REQUETES_TEST))]
    axes[1].plot(requetes_courtes, resultats_tfidf['precisions'],
                 'o-', label='TF-IDF', color='#4CAF50', linewidth=2)
    axes[1].plot(requetes_courtes, resultats_w2v['precisions'],
                 's-', label='Word2Vec', color='#FF9800', linewidth=2)
    axes[1].set_title(f"Precision@{top_k} par requête de test")
    axes[1].set_xlabel("Requête")
    axes[1].set_ylabel(f"Precision@{top_k}")
    axes[1].set_ylim(0, 1.1)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('comparaison_methodes.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("[Figure] comparaison_methodes.png sauvegardée")


def visualiser_scores_tfidf(df, requete, scores_col='score_tfidf', top_k=10):
    top = df.nlargest(top_k, scores_col)[['nom', scores_col]]
    fig, ax = plt.subplots(figsize=(10, 5))
    couleurs = ['#4CAF50' if s > 0.1 else '#2196F3' if s > 0.05 else '#FF9800'
                for s in top[scores_col]]
    bars = ax.barh(top['nom'][::-1], top[scores_col][::-1], color=couleurs[::-1])
    ax.set_title(f"Top-{top_k} recommandations\n'{requete[:60]}...'", fontsize=11)
    ax.set_xlabel("Score de similarité")
    for bar, val in zip(bars, top[scores_col][::-1]):
        ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}', va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig('scores_recommandation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("[Figure] scores_recommandation.png sauvegardée")

# ─────────────────────────────────────────────────────────────────────────────
# 7. INTERFACE UTILISATEUR (démonstration)
# ─────────────────────────────────────────────────────────────────────────────
def afficher_recommandations(resultats, methode_nom):
    score_col = 'score_tfidf' if 'tfidf' in methode_nom.lower() else 'score_w2v'
    print(f"\n{'='*60}")
    print(f"  RÉSULTATS — {methode_nom}")
    print(f"{'='*60}")
    for i, (_, row) in enumerate(resultats.iterrows(), 1):
        score = row.get(score_col, row.get('score_tfidf', row.get('score_w2v', 0)))
        print(f"\n  {i}. {row['nom']}  [{row['gratuit']}]  (score: {score:.4f})")
        print(f"     Domaine : {row['domaine']}")
        print(f"     Usage   : {row['besoin'][:70]}")
        print(f"     Lien    : {row['lien']}")


def demo_systeme(rec_tfidf, rec_w2v_ok, rec_w2v):
    requetes_demo = [
        "je suis étudiant en informatique et je veux apprendre à programmer",
        "j'ai besoin d'un outil pour rédiger ma thèse et corriger mon texte",
        "étudiant en médecine je veux rechercher des articles scientifiques",
        "je cherche un outil pour créer des présentations professionnelles",
    ]

    for requete in requetes_demo:
        print(f"\n{'#'*60}")
        print(f"  REQUÊTE : {requete}")
        print(f"{'#'*60}")

        res_tfidf = rec_tfidf.recommander(requete, top_k=5)
        afficher_recommandations(res_tfidf, "TF-IDF")

        if rec_w2v_ok:
            res_w2v = rec_w2v.recommander(requete, top_k=5)
            afficher_recommandations(res_w2v, "Word2Vec")


# ─────────────────────────────────────────────────────────────────────────────
# 8. PIPELINE PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("\n" + "="*60)
    print("  SYSTÈME DE RECOMMANDATION D'OUTILS IA POUR ÉTUDIANTS")
    print("  Projet NLP — 4ING — Université 8 Mai 45")
    print("="*60)

    # Étape 1 : Chargement
    df = charger_dataset('ai_tools_dataset.csv')

    # Étape 2 : Exploration visuelle
    visualiser_distribution(df)

    # Étape 3 : Prétraitement
    df = pretraiter_dataset(df)

    # Étape 4 : Méthode 1 — TF-IDF
    print("\n" + "="*60)
    print("MÉTHODE 1 : TF-IDF + SIMILARITÉ COSINUS")
    print("="*60)
    rec_tfidf = RecommandateurTFIDF()
    rec_tfidf.entrainer(df)

    # Étape 5 : Méthode 2 — Word2Vec
    print("\n" + "="*60)
    print("MÉTHODE 2 : WORD2VEC + SIMILARITÉ COSINUS")
    print("="*60)
    rec_w2v = RecommandateurWord2Vec()
    w2v_ok = rec_w2v.entrainer(df)

    # Étape 6 : Démonstration
    print("\n" + "="*60)
    print("DÉMONSTRATION DU SYSTÈME")
    print("="*60)
    demo_systeme(rec_tfidf, w2v_ok, rec_w2v)

    # Étape 7 : Évaluation et comparaison
    print("\n" + "="*60)
    print("ÉVALUATION ET COMPARAISON DES MÉTHODES")
    print("="*60)
    top_k = 5
    res_tfidf = evaluer_systeme(rec_tfidf, "TF-IDF", top_k=top_k)

    if w2v_ok:
        res_w2v = evaluer_systeme(rec_w2v, "Word2Vec", top_k=top_k)
        visualiser_comparaison(res_tfidf, res_w2v, top_k=top_k)
    else:
        print("\n[Word2Vec] gensim absent — comparaison partielle uniquement.")

    # Visualisation des scores pour une requête exemple
    requete_exemple = "je suis en informatique et je veux générer du code automatiquement"
    res_demo = rec_tfidf.recommander(requete_exemple, top_k=10)
    visualiser_scores_tfidf(res_demo, requete_exemple, top_k=10)

    print("\n" + "="*60)
    print("TRAITEMENT TERMINÉ — Figures sauvegardées dans le dossier courant.")
    print("="*60)


if __name__ == "__main__":
    main()
