# 🐙 GitHub Repo Recommender — NLP-Driven

Système de recommandation de repositories GitHub basé sur NLP (TF-IDF + Similarité Cosinus).

## 📦 Dataset
- **github_top_repositories_V2.csv** — 5 000 repositories GitHub top-rated
- 20 domaines : Machine Learning, Deep Learning, Python, JavaScript, Java, C++, Go, Rust, Data Science, Web Dev, Android, iOS, Blockchain, Cybersecurity, DevOps, Frontend, Backend, Game Dev, Cloud, AI

## 🚀 Lancer l'application
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🔧 Pipeline NLP
1. Nettoyage & tokenisation (NLTK)
2. Suppression stopwords FR+EN
3. Porter Stemmer
4. TF-IDF vectorisation (bigrammes, 10k features)
5. Similarité Cosinus pour le ranking

## 📁 Structure
```
├── app.py                          # Application Streamlit principale
├── config.py                       # Configuration
├── github_top_repositories_V2.csv  # Dataset (5000 repos)
├── requirements.txt
└── systeme_recommandation.py       # Module NLP standalone
```

## 🎓 Projet NLP 4ING — Université 8 Mai 45, Guelma — 2026
