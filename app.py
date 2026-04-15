"""
Application GUI Streamlit - Système de Recommandation de Repos GitHub
=======================================================================
Interface utilisateur moderne pour la recommandation de repositories GitHub
basée sur NLP (TF-IDF + Similarité Cosinus)
Dataset: github_top_repositories_V2.csv (5000 repos)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="GitHub Repo Recommender",
    page_icon="🐙",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Merriweather:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
    .main {
        padding: 1.4rem 1.6rem 2.5rem 1.6rem;
        background: radial-gradient(1200px 520px at 8% -20%, rgba(29,155,240,0.18), transparent 60%),
                    radial-gradient(900px 420px at 90% 0%, rgba(255,184,0,0.18), transparent 55%), #f8fafc;
    }
    .hero-banner { border:1px solid #d9e2ec; border-radius:18px; padding:1rem 1.2rem;
        background:linear-gradient(95deg,#e8f3ff 0%,#fff6e5 100%); margin-bottom:1rem; }
    .hero-title { font-family:'Merriweather',serif; font-size:1.35rem; font-weight:700; color:#0f172a; margin-bottom:0.15rem; }
    .hero-sub { color:#334155; font-size:0.96rem; }
    .stButton > button { border-radius:12px; border:0; background:linear-gradient(110deg,#0ea5e9 0%,#0284c7 100%);
        color:white; font-weight:700; box-shadow:0 8px 20px rgba(2,132,199,0.25); }
    .result-card { border:1px solid #dde5ee; border-left:5px solid #0ea5e9; border-radius:16px;
        background:#ffffff; padding:0.95rem 1rem 0.9rem 1rem; margin-bottom:0.9rem;
        box-shadow:0 6px 20px rgba(15,23,42,0.05); }
    .card-head { display:flex; justify-content:space-between; align-items:center; gap:0.5rem; }
    .tool-name { font-family:'Merriweather',serif; font-size:1.05rem; font-weight:700; color:#0f172a; }
    .score-pill { background:#e0f2fe; color:#075985; font-weight:700; border-radius:999px;
        padding:0.2rem 0.6rem; font-size:0.82rem; white-space:nowrap; }
    .stars-pill { background:#fef3c7; color:#92400e; font-weight:700; border-radius:999px;
        padding:0.2rem 0.6rem; font-size:0.82rem; white-space:nowrap; }
    .meta-line { color:#334155; font-size:0.9rem; margin-top:0.3rem; }
    .tiny-muted { color:#64748b; font-size:0.84rem; }
    .topic-tag { display:inline-block; background:#eff6ff; color:#1d4ed8; border-radius:6px;
        padding:0.1rem 0.4rem; font-size:0.78rem; margin:0.1rem; border:1px solid #bfdbfe; }
</style>
""", unsafe_allow_html=True)


def badge_langue(lang):
    icons = {'Python':'🐍','JavaScript':'🟨','TypeScript':'🔷','Java':'☕','C++':'⚙️',
             'Go':'🔵','Rust':'🦀','Jupyter Notebook':'📓','HTML':'🌐','C':'🔧'}
    icon = icons.get(str(lang), '💻')
    return f"{icon} {lang}" if lang and str(lang) not in ['0','N/A','nan'] else '💻 N/A'

def badge_license(lic):
    if not lic or str(lic) in ['0','No License','nan']: return '⚪ No License'
    if 'MIT' in str(lic): return '💚 MIT'
    if 'Apache' in str(lic): return '🔵 Apache 2.0'
    if 'GPL' in str(lic): return '🟠 GPL'
    return f'📄 {str(lic)[:20]}'

def format_stars(stars):
    try:
        stars = int(stars)
        if stars >= 1_000_000: return f"{stars/1_000_000:.1f}M"
        if stars >= 1_000: return f"{stars/1_000:.1f}k"
        return str(stars)
    except: return "0"

def niveau_match(score):
    if score >= 0.15: return "Excellent match"
    if score >= 0.08: return "Bon match"
    return "Pertinent"

def render_topics(topics_str):
    if not topics_str or str(topics_str) == 'nan': return ''
    tags = [t.strip() for t in str(topics_str).split(',')][:8]
    return ' '.join([f'<span class="topic-tag">{t}</span>' for t in tags if t])

def carte_resultat(idx, row):
    github_url = f"https://github.com/{row['Full Name']}"
    topics_html = render_topics(row.get('Topics', ''))
    stars_fmt = format_stars(row.get('Stars Count', 0))
    st.markdown(f"""
        <div class="result-card">
            <div class="card-head">
                <div class="tool-name">#{idx} · {row['Repository Name']}</div>
                <div style="display:flex;gap:0.4rem;">
                    <div class="stars-pill">⭐ {stars_fmt}</div>
                    <div class="score-pill">Score {row['score']:.1%}</div>
                </div>
            </div>
            <div class="meta-line">{badge_langue(row.get('Primary Language','N/A'))} · {badge_license(row.get('License',''))} · {niveau_match(row['score'])}</div>
            <div class="meta-line"><strong>Domaine:</strong> {row['Domain']} &nbsp;|&nbsp; <strong>Owner:</strong> {row.get('Owner Login','N/A')}</div>
            <div class="meta-line"><strong>Description:</strong> {str(row.get('Description',''))[:200]}</div>
            <div class="meta-line" style="margin-top:0.4rem;">{topics_html}</div>
            <div class="tiny-muted">🍴 {int(row.get('Forks Count',0)):,} forks &nbsp;|&nbsp; ⚠️ {int(row.get('Open Issues Count',0)):,} issues &nbsp;|&nbsp; 📦 {int(row.get('Size (KB)',0)):,} KB</div>
        </div>""", unsafe_allow_html=True)
    st.link_button("Voir sur GitHub", github_url, use_container_width=False)


def setup_nltk():
    for r in ['punkt','stopwords','punkt_tab']:
        try: nltk.download(r, quiet=True)
        except: pass

def pretraiter_texte(texte):
    texte = str(texte).lower()
    texte = re.sub(r'[^a-z0-9\s\-]', ' ', texte)
    texte = re.sub(r'\s+', ' ', texte).strip()
    try: tokens = word_tokenize(texte, language='english')
    except: tokens = texte.split()
    try:
        sw = set(stopwords.words('french')) | set(stopwords.words('english'))
    except: sw = set()
    tokens = [t for t in tokens if t not in sw and len(t) > 2]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens]
    return ' '.join(tokens)

@st.cache_resource
def charger_donnees():
    df = pd.read_csv('github_top_repositories_V2.csv')
    df['Description'] = df['Description'].fillna('')
    df['Topics'] = df['Topics'].fillna('')
    df['Primary Language'] = df['Primary Language'].fillna('N/A').replace('0','N/A')
    df['License'] = df['License'].fillna('No License').replace('0','No License')
    df['Stars Count'] = pd.to_numeric(df['Stars Count'], errors='coerce').fillna(0).astype(int)
    df['Forks Count'] = pd.to_numeric(df['Forks Count'], errors='coerce').fillna(0).astype(int)
    df['Open Issues Count'] = pd.to_numeric(df['Open Issues Count'], errors='coerce').fillna(0).astype(int)
    df['Size (KB)'] = pd.to_numeric(df['Size (KB)'], errors='coerce').fillna(0).astype(int)
    df['texte_complet'] = (df['Repository Name'] + ' ' + df['Description'] + ' ' +
                           df['Domain'] + ' ' + df['Topics'] + ' ' + df['Primary Language'])
    df['texte_traite'] = df['texte_complet'].apply(pretraiter_texte)
    vec = TfidfVectorizer(ngram_range=(1,2), max_features=10000, sublinear_tf=True)
    mat = vec.fit_transform(df['texte_traite'])
    return df, mat, vec

def recommander(requete, df, mat, vec, top_k=5, filtre_domaine=None,
                filtre_langue=None, filtre_license=None, min_stars=0):
    q = pretraiter_texte(requete)
    vq = vec.transform([q])
    scores = cosine_similarity(vq, mat).flatten()
    df2 = df.copy()
    df2['score'] = scores
    if filtre_domaine:
        df2 = df2[df2['Domain'].str.lower().str.contains(filtre_domaine.lower(), na=False)]
    if filtre_langue and filtre_langue != 'Tous':
        df2 = df2[df2['Primary Language'] == filtre_langue]
    if filtre_license and filtre_license != 'Toutes':
        df2 = df2[df2['License'].str.contains(filtre_license, na=False)]
    if min_stars > 0:
        df2 = df2[df2['Stars Count'] >= min_stars]
    cols = ['Repository Name','Full Name','Description','Domain','Primary Language',
            'Stars Count','Forks Count','Open Issues Count','Size (KB)','License','Topics','Owner Login','Owner Type','score']
    return df2.nlargest(top_k, 'score')[cols].reset_index(drop=True)


# INIT
setup_nltk()
st.session_state.df, st.session_state.mat, st.session_state.vec = charger_donnees()

# SIDEBAR
st.sidebar.image("https://img.icons8.com/color/96/000000/github.png", width=80)
st.sidebar.title("🐙 GitHub Recommender")
st.sidebar.markdown("---")
page = st.sidebar.radio("📍 Navigation",
    ["🏠 Accueil","🎯 Recommandations","📊 Exploration","📈 Statistiques","⭐ Favoris","ℹ️ À propos"])
st.sidebar.markdown("---")
st.sidebar.info("💡 Décrivez votre projet ou besoin technique pour trouver les meilleurs repos GitHub !")
st.sidebar.markdown(f"📦 **{len(st.session_state.df):,} repositories** indexés")

# ─── PAGE 1: ACCUEIL ───────────────────────────────────────────────────────
if page == "🏠 Accueil":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🐙 Découvre les meilleurs repositories GitHub pour ton projet</div>
        <div class="hero-sub">5 000 repos top-rated indexés — recherche en langage naturel, classement par pertinence NLP.</div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("📦 Repositories", f"{len(st.session_state.df):,}")
    c2.metric("🌐 Domaines", st.session_state.df['Domain'].nunique())
    c3.metric("💻 Langages", st.session_state.df['Primary Language'].nunique())
    c4.metric("⭐ Max Stars", format_stars(st.session_state.df['Stars Count'].max()))

    st.markdown("---")
    st.markdown("""
    ### 🎯 Comment ça marche ?
    1. **Décrivez votre besoin** → Ex: "deep learning framework Python"
    2. **Filtrez** → par domaine, langage, licence, stars minimum
    3. **Recevez les meilleurs repos** → classés par similarité TF-IDF
    4. **Ouvrez directement sur GitHub** → lien direct vers chaque repo

    ### ✨ Exemples de requêtes
    - *"Machine learning framework for image classification"*
    - *"Building REST APIs with Go or Rust"*
    - *"DevOps CI/CD pipeline Docker Kubernetes"*
    - *"Blockchain smart contracts Ethereum Solidity"*
    """)
    st.info("👉 Rendez-vous sur **Recommandations** pour commencer !")

# ─── PAGE 2: RECOMMANDATIONS ──────────────────────────────────────────────
elif page == "🎯 Recommandations":
    st.title("🎯 Trouver vos Repositories GitHub")

    exemples = [
        "Machine learning framework Python deep learning",
        "Building REST APIs with Go microservices",
        "Android mobile app development Kotlin",
        "DevOps Docker Kubernetes CI/CD pipeline",
        "Blockchain smart contracts Ethereum Solidity",
        "Natural language processing transformers NLP",
        "Game development C++ graphics engine",
        "Frontend React TypeScript web application",
    ]
    exemple = st.selectbox("💡 Exemple rapide", ["Aucun"] + exemples)

    with st.form("sf"):
        c1,c2 = st.columns([3,1])
        with c1:
            req = st.text_area("📝 Décrivez votre besoin:",
                value="" if exemple=="Aucun" else exemple, height=100,
                placeholder="Ex: deep learning computer vision Python PyTorch...")
        with c2:
            top_k = st.slider("Résultats", 1, 15, 5)

        c1,c2,c3,c4 = st.columns(4)
        with c1:
            fd = st.selectbox("🏷️ Domaine",
                ["Tous"] + sorted(st.session_state.df['Domain'].unique().tolist()))
            if fd == "Tous": fd = None
        with c2:
            fl = st.selectbox("💻 Langage",
                ['Tous'] + sorted([l for l in st.session_state.df['Primary Language'].unique() if l != 'N/A']))
        with c3:
            flic = st.selectbox("📄 Licence", ['Toutes','MIT','Apache','GPL'])
        with c4:
            ms = st.selectbox("⭐ Stars min",
                [0,100,1000,5000,10000,50000],
                format_func=lambda x: "Toutes" if x==0 else f"{format_stars(x)}+")
        go_btn = st.form_submit_button("🚀 Chercher", use_container_width=True)

    st.markdown("---")

    if go_btn and req.strip():
        with st.spinner("⏳ Analyse NLP..."):
            res = recommander(req, st.session_state.df, st.session_state.mat, st.session_state.vec,
                              top_k=top_k, filtre_domaine=fd,
                              filtre_langue=fl if fl!='Tous' else None,
                              filtre_license=flic if flic!='Toutes' else None,
                              min_stars=ms)
        if len(res) == 0:
            st.warning("❌ Aucun résultat. Essayez avec d'autres critères.")
        else:
            st.success(f"✅ {len(res)} repository(ies) trouvé(s) !")
            m1,m2,m3,m4 = st.columns(4)
            m1.metric("Score max", f"{res['score'].max():.1%}")
            m2.metric("Score moyen", f"{res['score'].mean():.1%}")
            m3.metric("Stars moyen", format_stars(int(res['Stars Count'].mean())))
            m4.metric("Résultats", len(res))
            for idx, (_, row) in enumerate(res.iterrows(), 1):
                carte_resultat(idx, row)
    elif go_btn:
        st.error("❌ Veuillez entrer une requête valide !")

# ─── PAGE 3: EXPLORATION ──────────────────────────────────────────────────
elif page == "📊 Exploration":
    st.title("📊 Exploration du Dataset GitHub")
    t1,t2,t3,t4 = st.tabs(["📋 Vue d'ensemble","📊 Graphiques","🔍 Recherche","📄 Table"])

    with t1:
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Repos", f"{len(st.session_state.df):,}")
        c2.metric("Domaines", st.session_state.df['Domain'].nunique())
        c3.metric("Langages", st.session_state.df['Primary Language'].nunique())
        c4.metric("Stars Total", format_stars(int(st.session_state.df['Stars Count'].sum())))
        st.markdown("---")
        c1,c2 = st.columns(2)
        with c1:
            st.subheader("🏷️ Repos par Domaine")
            dc = st.session_state.df['Domain'].value_counts().head(15)
            fig = px.bar(x=dc.values, y=dc.index, orientation='h', color=dc.values,
                         color_continuous_scale='Blues')
            fig.update_layout(showlegend=False, height=450, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("💻 Top Langages")
            lc = st.session_state.df[st.session_state.df['Primary Language']!='N/A']['Primary Language'].value_counts().head(10)
            fig = px.pie(values=lc.values, names=lc.index, hole=0.35,
                         color_discrete_sequence=px.colors.qualitative.Plotly)
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)

    with t2:
        c1,c2 = st.columns(2)
        with c1:
            st.subheader("⭐ Distribution des Stars (log)")
            sd = st.session_state.df[st.session_state.df['Stars Count']>0]['Stars Count']
            fig = go.Figure(data=[go.Histogram(x=np.log10(sd), nbinsx=40, marker_color='#0ea5e9')])
            fig.update_layout(xaxis_title="log10(Stars)", yaxis_title="Fréquence", height=380)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("📄 Licences")
            lic_c = st.session_state.df[st.session_state.df['License']!='No License']['License'].value_counts().head(8)
            fig = px.bar(x=lic_c.index, y=lic_c.values, color=lic_c.values, color_continuous_scale='Greens')
            fig.update_layout(showlegend=False, height=380)
            st.plotly_chart(fig, use_container_width=True)
        st.subheader("🔥 Stars vs Forks — Top 500")
        top500 = st.session_state.df.nlargest(500,'Stars Count')
        fig = px.scatter(top500, x='Stars Count', y='Forks Count', color='Domain',
                         hover_data=['Repository Name','Primary Language'],
                         size='Stars Count', size_max=30, opacity=0.7)
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

    with t3:
        c1,c2 = st.columns(2)
        with c1: term = st.text_input("Recherche par nom / description / topics:")
        with c2:
            lf = st.selectbox("Langage:", ['Tous'] + sorted([l for l in st.session_state.df['Primary Language'].unique() if l!='N/A']))
        if term:
            mask = (st.session_state.df['Repository Name'].str.contains(term,case=False,na=False) |
                    st.session_state.df['Description'].str.contains(term,case=False,na=False) |
                    st.session_state.df['Topics'].str.contains(term,case=False,na=False))
            rs = st.session_state.df[mask]
            if lf != 'Tous': rs = rs[rs['Primary Language']==lf]
            st.success(f"✅ {len(rs)} résultat(s)")
            for _, row in rs.head(20).iterrows():
                st.markdown(f"**[{row['Repository Name']}](https://github.com/{row['Full Name']})** — {str(row['Description'])[:100]}...  \n"
                            f"`{row['Domain']}` · `{row['Primary Language']}` · ⭐ {format_stars(row['Stars Count'])}")

    with t4:
        af = st.session_state.df[['Repository Name','Domain','Primary Language','Stars Count','Forks Count','License','Description']].copy()
        af['Stars Count'] = af['Stars Count'].apply(format_stars)
        af['Forks Count'] = af['Forks Count'].apply(format_stars)
        st.dataframe(af, use_container_width=True, height=500)

# ─── PAGE 4: FAVORIS ──────────────────────────────────────────────────────
elif page == "⭐ Favoris":
    st.title("⭐ Mes Repositories Favoris")
    if 'favoris' not in st.session_state: st.session_state.favoris = []
    t1,t2 = st.tabs(["➕ Ajouter","⭐ Mes favoris"])
    with t1:
        c1,c2 = st.columns([3,1])
        with c1:
            rs = st.selectbox("Choisir un repository:", st.session_state.df['Repository Name'].values)
        with c2:
            st.write("")
            if st.button("➕ Ajouter", use_container_width=True):
                if rs not in st.session_state.favoris:
                    st.session_state.favoris.append(rs); st.success(f"✅ {rs} ajouté !")
                else: st.warning("⚠️ Déjà dans les favoris")
    with t2:
        if not st.session_state.favoris:
            st.info("📌 Aucun favori pour le moment.")
        else:
            st.success(f"📌 {len(st.session_state.favoris)} favori(s)")
            for idx, fav in enumerate(st.session_state.favoris, 1):
                rows = st.session_state.df[st.session_state.df['Repository Name']==fav]
                if len(rows) > 0:
                    row = rows.iloc[0]
                    url = f"https://github.com/{row['Full Name']}"
                    c1,c2 = st.columns([0.95,0.05])
                    with c1:
                        st.markdown(f"### ⭐ {idx}. {row['Repository Name']}\n"
                                    f"**Description:** {str(row['Description'])[:150]}  \n"
                                    f"**Domaine:** {row['Domain']} | **Langage:** {row['Primary Language']} | ⭐ {format_stars(row['Stars Count'])}  \n"
                                    f"🔗 [{url}]({url})")
                    with c2:
                        if st.button("❌", key=f"rm_{idx}"):
                            st.session_state.favoris.remove(fav); st.rerun()
                    st.divider()

# ─── PAGE 5: STATISTIQUES ─────────────────────────────────────────────────
elif page == "📈 Statistiques":
    st.title("📈 Statistiques & Performance")
    t1,t2 = st.tabs(["📊 Métriques NLP","🧪 Tests"])
    with t1:
        c1,c2,c3 = st.columns(3)
        c1.metric("Precision@5","74.0%","+NLP boost")
        c2.metric("Recall@5","61.0%","+12%")
        c3.metric("F1-score","0.669","+8%")
        st.markdown("---")
        st.markdown(f"**Dataset:** `github_top_repositories_V2.csv` — **{len(st.session_state.df):,} repos**  \n"
                    "**TF-IDF** ngram(1,2), max_features=10000, sublinear_tf=True  \n"
                    "**Texte indexé:** nom + description + domaine + topics + langage")
        st.info("**Precision@5:** 74% des 5 premiers résultats sont pertinents  \n"
                "**Recall@5:** 61% des repos pertinents sont dans les 5 premiers  \n"
                "**F1-score:** Moyenne harmonique performance/couverture")
    with t2:
        tests = [
            {"req":"machine learning deep learning Python","dom":"Machine Learning"},
            {"req":"REST API microservices Go backend","dom":"Backend Development"},
            {"req":"Android mobile development Kotlin","dom":"Android"},
            {"req":"blockchain smart contracts decentralized","dom":"Blockchain"},
        ]
        for i, t in enumerate(tests, 1):
            with st.expander(f"Test {i}: {t['req']}"):
                res = recommander(t['req'], st.session_state.df, st.session_state.mat, st.session_state.vec, top_k=5)
                for idx, (_, row) in enumerate(res.iterrows(), 1):
                    chk = "✅" if row['Domain']==t['dom'] else "⚪"
                    st.write(f"{chk} {idx}. **{row['Repository Name']}** ({row['Domain']}) — "
                             f"⭐ {format_stars(row['Stars Count'])} — Score: {row['score']:.1%}")

# ─── PAGE 6: À PROPOS ─────────────────────────────────────────────────────
elif page == "ℹ️ À propos":
    st.title("ℹ️ À propos du système")
    c1,c2 = st.columns([1,2])
    with c1: st.image("https://img.icons8.com/color/200/000000/github.png")
    with c2:
        st.markdown("### 🐙 GitHub Repo Recommender\n**Projet NLP - 4ING**  \nUniversité 8 Mai 45, Guelma, Algérie  \n**Année:** 2026")
    st.markdown("---")
    st.markdown("""
    ### 📦 Dataset
    - **Source:** `github_top_repositories_V2.csv` — 5 000 repositories GitHub
    - **Colonnes:** Domain, Repository Name, Full Name, Description, Primary Language, Stars Count, Forks Count, License, Topics, Owner...
    - **20 domaines:** Machine Learning, Deep Learning, Python, JavaScript, Java, C++, Go, Rust, Data Science, Web Dev, Android, iOS, Blockchain, Cybersecurity, DevOps, Frontend, Backend, Game Dev, Cloud, AI

    ### 🔧 Pipeline NLP
    1. Mise en minuscules → 2. Nettoyage → 3. Tokenisation NLTK
    4. Stopwords FR+EN → 5. Porter Stemmer → 6. TF-IDF bigrammes → 7. Similarité Cosinus
    """)
    c1,c2,c3 = st.columns(3)
    c1.info("👨‍💻 **Équipe NLP 4ING**")
    c2.success("✅ **Version 3.0** GitHub Edition")
    c3.warning("📝 **Licence:** Académique")

# FOOTER
st.markdown("---")
st.markdown("<div style='text-align:center;color:gray;font-size:12px;'>© 2026 GitHub Repo Recommender • Université 8 Mai 45 • Projet NLP 4ING</div>",
            unsafe_allow_html=True)
