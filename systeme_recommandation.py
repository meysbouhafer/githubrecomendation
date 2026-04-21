"""
GitHub Repo Recommender — Hybride TF-IDF + SBERT
==================================================
Deux moteurs combinés :
  - TF-IDF (sparse, lexical, rapide)           → bon pour les mots-clés exacts
  - SBERT  (dense, sémantique, sentence-transformers) → bon pour les paraphrases
  
L'ambiguïté de la requête (longueur + entropie TF-IDF) ajuste dynamiquement
le coefficient α : requête courte/vague → plus de SBERT, précise → plus de TF-IDF.
"""

import re
import warnings
from typing import Optional

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings("ignore")

DATASET_PATH = "github_top_repositories_V2.csv"

# Modèle SBERT — léger et multilingue, change selon besoin
SBERT_MODEL = "all-MiniLM-L6-v2"


# ---------------------------------------------------------------------------
# Setup NLTK
# ---------------------------------------------------------------------------

def setup_nltk() -> None:
    for resource in ["punkt", "stopwords", "punkt_tab"]:
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Prétraitement texte (identique à l'original)
# ---------------------------------------------------------------------------

def pretraiter_texte(texte: str) -> str:
    texte = str(texte).lower()
    texte = re.sub(r"[^a-z0-9\s\-]", " ", texte)
    texte = re.sub(r"\s+", " ", texte).strip()

    try:
        tokens = word_tokenize(texte, language="english")
    except Exception:
        tokens = texte.split()

    try:
        mots_vides = set(stopwords.words("french")) | set(stopwords.words("english"))
    except Exception:
        mots_vides = set()

    tokens = [t for t in tokens if t not in mots_vides and len(t) > 2]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens]
    return " ".join(tokens)


# ---------------------------------------------------------------------------
# Chargement dataset
# ---------------------------------------------------------------------------

def charger_dataset(chemin: str = DATASET_PATH) -> pd.DataFrame:
    df = pd.read_csv(chemin)

    df["Description"]       = df["Description"].fillna("")
    df["Topics"]            = df["Topics"].fillna("")
    df["Domain"]            = df["Domain"].fillna("Unknown")
    df["Primary Language"]  = df["Primary Language"].fillna("N/A").replace("0", "N/A")
    df["License"]           = df["License"].fillna("No License").replace("0", "No License")
    df["Stars Count"]       = pd.to_numeric(df["Stars Count"], errors="coerce").fillna(0).astype(int)
    df["Forks Count"]       = pd.to_numeric(df["Forks Count"], errors="coerce").fillna(0).astype(int)

    df["texte_complet"] = (
        df["Repository Name"].astype(str) + " "
        + df["Description"].astype(str)   + " "
        + df["Domain"].astype(str)        + " "
        + df["Topics"].astype(str)        + " "
        + df["Primary Language"].astype(str)
    )
    df["texte_traite"] = df["texte_complet"].apply(pretraiter_texte)
    return df


# ---------------------------------------------------------------------------
# Détection d'ambiguïté → coefficient α dynamique
# ---------------------------------------------------------------------------

def calculer_alpha(
    requete: str,
    vectoriseur: TfidfVectorizer,
    alpha_min: float = 0.2,
    alpha_max: float = 0.8,
) -> float:
    """
    Retourne α ∈ [alpha_min, alpha_max], le poids du TF-IDF dans la fusion.
    
    Logique :
      - Requête courte (1-2 tokens) ou mots inconnus du vocabulaire → TF-IDF moins fiable → α bas
      - Requête précise et couverte par le vocabulaire → α élevé
      - Entropie des scores TF-IDF sparse : si très concentrée → requête spécifique → α monte
    """
    tokens_bruts = requete.lower().split()
    n_tokens = len(tokens_bruts)

    # Score de couverture vocabulaire
    vocab = set(vectoriseur.vocabulary_.keys())
    tokens_traites = pretraiter_texte(requete).split()
    couverture = sum(1 for t in tokens_traites if t in vocab) / max(len(tokens_traites), 1)

    # Longueur normalisée (saturée à 10 tokens)
    long_norm = min(n_tokens / 10.0, 1.0)

    # Score composite → alpha
    score = 0.5 * couverture + 0.5 * long_norm
    alpha = alpha_min + score * (alpha_max - alpha_min)
    return float(np.clip(alpha, alpha_min, alpha_max))


# ---------------------------------------------------------------------------
# Moteur TF-IDF (reprend l'original, légèrement factorisé)
# ---------------------------------------------------------------------------

class MoteurTFIDF:
    def __init__(self) -> None:
        self.vectoriseur = TfidfVectorizer(
            ngram_range=(1, 2), max_features=10_000, sublinear_tf=True
        )
        self.matrice: Optional[object] = None

    def entrainer(self, textes: pd.Series) -> None:
        self.matrice = self.vectoriseur.fit_transform(textes)

    def scorer(self, requete: str) -> np.ndarray:
        requete_traitee = pretraiter_texte(requete)
        vecteur = self.vectoriseur.transform([requete_traitee])
        return cosine_similarity(vecteur, self.matrice).flatten()


# ---------------------------------------------------------------------------
# Moteur SBERT
# ---------------------------------------------------------------------------

class MoteurSBERT:
    """
    Encode les textes avec sentence-transformers (SBERT).
    Installe le paquet si absent : pip install sentence-transformers
    """

    def __init__(self, nom_modele: str = SBERT_MODEL) -> None:
        self.nom_modele = nom_modele
        self.modele = None
        self.embeddings: Optional[np.ndarray] = None

    def _charger_modele(self) -> None:
        if self.modele is None:
            try:
                from sentence_transformers import SentenceTransformer
                print(f"[SBERT] Chargement du modèle '{self.nom_modele}'…")
                self.modele = SentenceTransformer(self.nom_modele)
            except ImportError:
                raise ImportError(
                    "sentence-transformers n'est pas installé.\n"
                    "Exécutez : pip install sentence-transformers"
                )

    def entrainer(self, textes: pd.Series, batch_size: int = 64) -> None:
        self._charger_modele()
        print(f"[SBERT] Encodage de {len(textes):,} textes…")
        self.embeddings = self.modele.encode(
            textes.tolist(),
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,   # cosine = produit scalaire après normalisation
        )
        print("[SBERT] Encodage terminé.")

    def scorer(self, requete: str) -> np.ndarray:
        if self.embeddings is None:
            raise RuntimeError("SBERT non entraîné.")
        self._charger_modele()
        vecteur = self.modele.encode(
            [requete],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        # Produit scalaire = cosine car vecteurs normalisés
        return (self.embeddings @ vecteur.T).flatten()


# ---------------------------------------------------------------------------
# Recommandateur hybride TF-IDF + SBERT
# ---------------------------------------------------------------------------

class RecommandateurHybride:
    """
    Fusionne les scores TF-IDF et SBERT via un coefficient α adaptatif.
    
    score_final = α · score_tfidf + (1-α) · score_sbert
    
    α est calculé automatiquement à partir de l'ambiguïté de la requête,
    ou peut être fixé manuellement (alpha_fixe ∈ [0, 1]).
    """

    def __init__(self, utiliser_sbert: bool = True) -> None:
        self.tfidf  = MoteurTFIDF()
        self.sbert  = MoteurSBERT() if utiliser_sbert else None
        self.df: Optional[pd.DataFrame] = None
        self.utiliser_sbert = utiliser_sbert

    def entrainer(self, df: pd.DataFrame) -> None:
        self.df = df.copy()

        # TF-IDF sur texte prétraité (stemming, stop-words)
        print("[TF-IDF] Entraînement…")
        self.tfidf.entrainer(df["texte_traite"])
        print("[TF-IDF] Terminé.")

        # SBERT sur texte original riche (pas de stemming → meilleure sémantique)
        if self.utiliser_sbert and self.sbert is not None:
            self.sbert.entrainer(df["texte_complet"])

    def recommander(
        self,
        requete: str,
        top_k: int = 5,
        filtre_domaine: Optional[str] = None,
        filtre_langue: Optional[str] = None,
        min_stars: int = 0,
        alpha_fixe: Optional[float] = None,
    ) -> pd.DataFrame:
        """
        Paramètres
        ----------
        requete       : texte libre de l'utilisateur
        top_k         : nombre de résultats à retourner
        filtre_domaine: filtre optionnel sur la colonne Domain
        filtre_langue : filtre optionnel sur Primary Language
        min_stars     : seuil minimum d'étoiles
        alpha_fixe    : si fourni, utilise cette valeur fixe pour α
                        (0.0 = SBERT pur, 1.0 = TF-IDF pur)
        """
        if self.df is None:
            raise RuntimeError("Modèle non entraîné.")

        # --- Scores individuels ---
        scores_tfidf = self.tfidf.scorer(requete)

        if self.utiliser_sbert and self.sbert is not None:
            scores_sbert = self.sbert.scorer(requete)
        else:
            scores_sbert = scores_tfidf  # fallback

        # --- Coefficient α ---
        if alpha_fixe is not None:
            alpha = float(np.clip(alpha_fixe, 0.0, 1.0))
        else:
            alpha = calculer_alpha(requete, self.tfidf.vectoriseur)

        # --- Fusion ---
        scores_final = alpha * scores_tfidf + (1.0 - alpha) * scores_sbert

        # --- Construction du dataframe résultat ---
        df_resultat = self.df.copy()
        df_resultat["score"]        = scores_final
        df_resultat["score_tfidf"]  = scores_tfidf
        df_resultat["score_sbert"]  = scores_sbert
        df_resultat["alpha"]        = round(alpha, 3)

        # --- Filtres ---
        if filtre_domaine:
            masque = df_resultat["Domain"].str.lower().str.contains(
                filtre_domaine.lower(), na=False
            )
            df_resultat = df_resultat[masque]

        if filtre_langue:
            df_resultat = df_resultat[df_resultat["Primary Language"] == filtre_langue]

        if min_stars > 0:
            df_resultat = df_resultat[df_resultat["Stars Count"] >= min_stars]

        colonnes = [
            "Repository Name", "Full Name", "Description",
            "Domain", "Primary Language", "Stars Count", "Forks Count",
            "License", "score", "score_tfidf", "score_sbert", "alpha",
        ]
        return (
            df_resultat
            .nlargest(top_k, "score")[colonnes]
            .reset_index(drop=True)
        )


# ---------------------------------------------------------------------------
# Démonstration CLI
# ---------------------------------------------------------------------------

def demo_cli() -> None:
    print("=" * 70)
    print(" GITHUB REPO RECOMMENDER — HYBRIDE TF-IDF + SBERT")
    print("=" * 70)

    df = charger_dataset(DATASET_PATH)
    print(f"Dataset chargée : {len(df):,} repositories\n")

    rec = RecommandateurHybride(utiliser_sbert=True)
    rec.entrainer(df)

    requetes = [
        ("machine learning framework python deep learning", None, None),
        ("natural language processing",                    None, "Python"),
        ("distributed systems fault tolerance",            None, None),
    ]

    for requete, domaine, langue in requetes:
        print("\n" + "=" * 70)
        print(f"Requête : {requete}")
        if domaine: print(f"  Filtre domaine   : {domaine}")
        if langue:  print(f"  Filtre langage   : {langue}")

        resultats = rec.recommander(
            requete, top_k=5,
            filtre_domaine=domaine,
            filtre_langue=langue,
        )

        alpha_utilise = resultats["alpha"].iloc[0] if not resultats.empty else "N/A"
        print(f"  α utilisé : {alpha_utilise}  (TF-IDF={alpha_utilise}, SBERT={round(1-float(alpha_utilise),3)})")

        for i, row in resultats.iterrows():
            print("-" * 70)
            print(f"#{i+1} {row['Repository Name']}  ({row['Full Name']})")
            print(
                f"  Score final : {row['score']:.4f}"
                f"  | TF-IDF : {row['score_tfidf']:.4f}"
                f"  | SBERT  : {row['score_sbert']:.4f}"
            )
            print(f"  Langage : {row['Primary Language']}  | Stars : {row['Stars Count']:,}")
            print(f"  Domaine : {row['Domain']}")
            print(f"  {str(row['Description'])[:140]}")


if __name__ == "__main__":
    setup_nltk()
    demo_cli()