"""Application Streamlit principale pour l'exploration et la visualisation de données."""

from pathlib import Path

import pandas as pd
import pretty_errors  # noqa: F401
import streamlit as st
import viz
from loguru import logger
from streamlit.runtime.uploaded_file_manager import UploadedFile

from titanic_ml.core.data_io.loader import load_data as load_titanic_dataset
from titanic_ml.core.utils import get_project_version


# --- CONFIGURATION DE LA PAGE ---
def set_page_config() -> None:
    """Initialise la mise en page et la configuration de la page."""
    logger.info("Initialisation de la mise en page")
    st.set_page_config(page_title="Titanic ML - UI", page_icon="📊", layout="wide")


# --- CHARGEMENT DES ASSETS ---
@st.cache_data(show_spinner=False)
def _read_css_file(css_path: Path) -> str:
    """Lit le fichier CSS et le met en cache pour éviter les I/O à chaque rendu."""
    if css_path.exists():
        with open(css_path) as f:
            return f.read()
    return ""


def load_assets() -> None:
    """Charge le CSS personnalisé et les animations d'arrière-plan."""
    css_path = Path(__file__).parent / "assets" / "style.css"
    css_content = _read_css_file(css_path)
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

    # Injecte les éléments d'arrière-plan animés définis dans style.css
    st.markdown('<div class="grid-background"></div>', unsafe_allow_html=True)
    st.markdown('<div class="glow-orb glow-orb-1"></div>', unsafe_allow_html=True)
    st.markdown('<div class="glow-orb glow-orb-2"></div>', unsafe_allow_html=True)


# --- COMPOSANTS UI ---
def display_hero() -> None:
    """Affiche la section Hero avec les classes CSS du projet."""
    st.markdown(
        """
        <div class="hero">
            <h1 class="hero-title">
                <span class="hero-title-line">Data Control Center</span>
                <span class="hero-title-highlight">Titanic ML</span>
            </h1>
            <p class="hero-subtitle">
                Exemple d'interface Streamlit pour explorer le dataset Titanic.
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )


def sidebar() -> UploadedFile | None:
    """Gère la configuration de la barre latérale et le téléversement de fichiers."""
    logger.info("Configuration de la barre latérale")
    with st.sidebar:
        st.caption(f"v{get_project_version()}")
        st.markdown("---")

        st.subheader("📁 Paramètres des données")
        dataset_file = st.file_uploader("Charger un dataset", type=["parquet", "csv", "xlsx", "xls"])

        st.session_state["gen_count"] = st.number_input("Lignes à afficher", value=100, min_value=1)

        st.markdown("---")
        st.info("Astuce : charge data/raw/titanic.csv pour explorer le dataset d'entraînement.")
    return dataset_file


def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie le dataframe pour éviter les erreurs de sérialisation Arrow sur les colonnes mixtes."""
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str)
    return df


# --- OPTIMISATION PAR CACHE ---
@st.cache_data(show_spinner="Chargement du dataset Titanic...")
def get_titanic_dataframe() -> pd.DataFrame:
    """Charge (et met en cache) le dataset Titanic d'entraînement pour les visualisations."""
    return load_titanic_dataset()


@st.cache_data(show_spinner="Chargement des données...")
def get_cached_dataframe(file_bytes: bytes, file_name: str) -> pd.DataFrame | None:
    """Utilise le cache Streamlit pour éviter de recharger le fichier à chaque interaction."""
    import io

    df = None
    if file_name.endswith(".parquet"):
        df = pd.read_parquet(io.BytesIO(file_bytes))
    elif file_name.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(file_bytes))
    elif file_name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(io.BytesIO(file_bytes))

    if df is not None:
        return sanitize_dataframe(df)
    return None


def load_data(dataset_file: UploadedFile | None) -> bool:
    """Centralise la logique de chargement des données via le cache Streamlit."""
    if dataset_file is not None:
        file_name = dataset_file.name.lower()
        prev_file = st.session_state.get("current_file_obj")

        if dataset_file != prev_file:
            logger.info(f"Nouveau dataset détecté : {file_name}. Réinitialisation du renderer.")
            st.session_state.pop("pyg_renderer", None)
            st.session_state["current_file_obj"] = dataset_file
            st.session_state["current_file"] = file_name

            try:
                st.session_state.pyg_data = get_cached_dataframe(dataset_file.getvalue(), file_name)
                logger.info(f"Dataset '{file_name}' chargé avec succès")
            except (pd.errors.ParserError, pd.errors.EmptyDataError, ValueError, TypeError) as e:
                st.error(f"Erreur de lecture du fichier (format invalide ou corrompu) : {e}")
                return False
    else:
        st.session_state.pop("pyg_data", None)
        st.session_state.pop("pyg_renderer", None)
        st.session_state.pop("current_file_obj", None)
        st.session_state["current_file"] = None
    return True


# --- VISUALISATIONS TITANIC ---
def display_titanic_visualizations() -> None:
    """Affiche un tableau de bord de visualisations claires sur le dataset Titanic d'entraînement."""
    df = get_titanic_dataframe()
    display_df = viz.prepare_display_frame(df)

    st.subheader("Vue d'ensemble")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Passagers", f"{len(df):,}".replace(",", " "))
    with col2:
        st.metric("Taux de survie global", f"{df['Survived'].mean() * 100:.1f} %")
    with col3:
        st.metric("Âge moyen", f"{df['Age'].mean():.1f} ans")

    st.markdown("---")
    st.subheader("Qui a survécu ?")
    col_class, col_sex = st.columns(2)
    with col_class:
        st.altair_chart(
            viz.survival_rate_by(
                display_df,
                "Classe",
                order=viz.PCLASS_ORDER,
                title="Taux de survie par classe",
            ),
            use_container_width=True,
        )
    with col_sex:
        st.altair_chart(
            viz.survival_rate_by(
                display_df,
                "Sexe",
                order=viz.SEX_ORDER,
                title="Taux de survie par sexe",
            ),
            use_container_width=True,
        )

    st.altair_chart(viz.survival_heatmap(df), use_container_width=True)

    st.markdown("---")
    st.subheader("Âge et port d'embarquement")
    st.altair_chart(viz.age_distribution_by_survival(df), use_container_width=True)
    st.altair_chart(
        viz.survival_rate_by(
            display_df,
            "Embarquement",
            order=viz.EMBARKED_ORDER,
            title="Taux de survie par port d'embarquement",
        ),
        use_container_width=True,
    )

    with st.expander("📄 Voir les données utilisées (vue table)"):
        st.dataframe(display_df, use_container_width=True)


# --- EXÉCUTION PRINCIPALE ---
def main() -> None:
    """Exécute le flux principal de l'application."""
    set_page_config()
    load_assets()

    dataset_file = sidebar()
    load_data(dataset_file)
    display_hero()

    tab_summary, tab_viz, tab_explore = st.tabs(
        ["📋 Aperçu du dataset", "📊 Visualisations Titanic", "🔍 Analyse visuelle"]
    )

    with tab_summary:
        if "pyg_data" in st.session_state:
            st.subheader("Informations générales")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Nb lignes", f"{len(st.session_state.pyg_data):,}".replace(",", " "))
            with col2:
                st.metric("Nb colonnes", len(st.session_state.pyg_data.columns))
            with col3:
                st.metric("Fichier", st.session_state.get("current_file", "Inconnu"))

            st.markdown("---")
            st.subheader("Statistiques")
            if st.button("📊 Générer les statistiques"):
                st.dataframe(st.session_state.pyg_data.describe().T, use_container_width=True)

            st.markdown("---")
            st.subheader("Aperçu du dataset")
            rows_to_show = st.session_state.get("gen_count", 100)
            st.dataframe(st.session_state.pyg_data.head(rows_to_show), use_container_width=True)
        else:
            st.info("💡 Charge un dataset depuis le menu de gauche.")

    with tab_viz:
        display_titanic_visualizations()

    with tab_explore:
        if "pyg_data" in st.session_state:
            st.markdown("---")
            st.subheader("🔍 Explorateur de données interactif")

            try:
                from pygwalker.api.streamlit import StreamlitRenderer
            except ImportError as e:
                st.error(
                    "⚠️ L'explorateur Pygwalker est indisponible : incompatibilité entre les versions "
                    f"installées de `pygwalker` et `streamlit` ({e}). "
                    'Essaie de figer une version compatible de Streamlit (`uv add "streamlit<1.6x"`) '
                    "ou de mettre à jour `pygwalker`."
                )
            else:
                if "pyg_renderer" not in st.session_state:
                    st.session_state.pyg_renderer = StreamlitRenderer(
                        st.session_state.pyg_data,
                        spec="./app/assets/pygwalker_config.json",
                        env="streamlit",
                        theme_key="streamlit",
                        use_kernel_calc=True,
                    )

                st.session_state.pyg_renderer.explorer()
        else:
            st.info("💡 Charge un dataset depuis le menu de gauche pour débloquer l'explorateur interactif.")


if __name__ == "__main__":
    logger.info("Démarrage de l'application Streamlit")
    main()
