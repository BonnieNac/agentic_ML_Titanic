"""Visualisations Altair claires et validées pour le dataset Titanic."""

import altair as alt
import pandas as pd

# --- Palette (voir la skill dataviz : palette catégorielle/séquentielle validée) ---
BLUE = "#2a78d6"  # slot catégoriel 1 — mesure unique, hue séquentiel par défaut
ORANGE = "#eb6834"  # slot catégoriel 2 — paire validée avec BLUE (CVD Delta E 9.1)
SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"

SEQUENTIAL_RAMP = ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]

_SEX_LABELS = {"male": "Homme", "female": "Femme"}
_EMBARKED_LABELS = {"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"}
_PCLASS_LABELS = {1: "1ère classe", 2: "2ème classe", 3: "3ème classe"}
_STATUS_LABELS = {0: "Décédé(e)", 1: "A survécu"}

# Ordres d'affichage publics, réutilisés par l'app Streamlit pour trier les axes catégoriels.
SEX_ORDER = list(_SEX_LABELS.values())
EMBARKED_ORDER = list(_EMBARKED_LABELS.values())
PCLASS_ORDER = list(_PCLASS_LABELS.values())


def _base_axis(title: str | None) -> alt.Axis:
    """Configure un axe discret dans les tons muted de la palette validée."""
    return alt.Axis(title=title, labelColor=INK_SECONDARY, titleColor=INK_SECONDARY, grid=False)


def _style(chart: alt.Chart) -> alt.Chart:
    """Applique le fond, les gridlines et la typo communs à tous les graphiques."""
    styled: alt.Chart = (
        chart.properties(background=SURFACE)
        .configure_view(strokeWidth=0)
        .configure_axis(gridColor=GRID, domainColor=BASELINE, tickColor=BASELINE)
        .configure_title(color=INK_PRIMARY, fontSize=14)
        .configure_legend(labelColor=INK_SECONDARY, titleColor=INK_SECONDARY)
    )
    return styled


def survival_rate_by(df: pd.DataFrame, column: str, order: list[str], title: str) -> alt.Chart:
    """Construit un bar chart mono-hue du taux de survie par catégorie, labels directs inclus."""
    grouped = df.groupby(column, observed=True)["Survived"].agg(taux="mean", effectif="count").reset_index()
    grouped["taux_pct"] = (grouped["taux"] * 100).round(1)
    grouped["label"] = grouped["taux_pct"].astype(str) + " %"

    bars = (
        alt.Chart(grouped)
        .mark_bar(color=BLUE, size=42, cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X(f"{column}:N", sort=order, axis=_base_axis(None), title=None),
            y=alt.Y(
                "taux_pct:Q", axis=alt.Axis(title="Taux de survie (%)", grid=True), scale=alt.Scale(domain=[0, 100])
            ),
            tooltip=[
                alt.Tooltip(f"{column}:N", title="Groupe"),
                alt.Tooltip("taux_pct:Q", title="Taux de survie (%)"),
                alt.Tooltip("effectif:Q", title="Nb passagers"),
            ],
        )
    )
    labels = bars.mark_text(dy=-8, color=INK_PRIMARY, fontSize=12).encode(text="label:N")
    return _style((bars + labels).properties(title=title, width=320, height=280))


def survival_heatmap(df: pd.DataFrame) -> alt.Chart:
    """Heatmap séquentielle (une teinte) du taux de survie croisé classe x sexe."""
    grouped = df.groupby(["Pclass", "Sex"], observed=True)["Survived"].mean().reset_index()
    grouped["taux_pct"] = (grouped["Survived"] * 100).round(1)
    grouped["classe"] = grouped["Pclass"].map(_PCLASS_LABELS)
    grouped["sexe"] = grouped["Sex"].map(_SEX_LABELS)

    heat = (
        alt.Chart(grouped)
        .mark_rect(stroke=SURFACE, strokeWidth=2, cornerRadius=2)
        .encode(
            x=alt.X("classe:N", sort=list(_PCLASS_LABELS.values()), axis=_base_axis(None), title=None),
            y=alt.Y("sexe:N", sort=list(_SEX_LABELS.values()), axis=_base_axis(None), title=None),
            color=alt.Color(
                "taux_pct:Q",
                scale=alt.Scale(range=SEQUENTIAL_RAMP),
                legend=alt.Legend(title="Taux de survie (%)"),
            ),
            tooltip=[
                alt.Tooltip("classe:N", title="Classe"),
                alt.Tooltip("sexe:N", title="Sexe"),
                alt.Tooltip("taux_pct:Q", title="Taux de survie (%)"),
            ],
        )
    )
    grouped["label"] = grouped["taux_pct"].astype(str) + " %"
    text = heat.mark_text(fontSize=13, fontWeight="bold").encode(
        text="label:N",
        color=alt.value(INK_PRIMARY),
    )
    return _style((heat + text).properties(title="Taux de survie par classe et par sexe", width=320, height=220))


def age_distribution_by_survival(df: pd.DataFrame) -> alt.Chart:
    """Histogramme superposé de la distribution d'âge, coloré par statut de survie."""
    data = df.dropna(subset=["Age"]).copy()
    data["statut"] = data["Survived"].map(_STATUS_LABELS)

    chart = (
        alt.Chart(data)
        .mark_bar(opacity=0.75, stroke=SURFACE, strokeWidth=1)
        .encode(
            x=alt.X("Age:Q", bin=alt.Bin(maxbins=30), axis=alt.Axis(title="Âge")),
            y=alt.Y("count():Q", stack=None, axis=alt.Axis(title="Nombre de passagers", grid=True)),
            color=alt.Color(
                "statut:N",
                sort=list(_STATUS_LABELS.values()),
                scale=alt.Scale(domain=list(_STATUS_LABELS.values()), range=[ORANGE, BLUE]),
                legend=alt.Legend(title="Statut"),
            ),
            tooltip=[
                alt.Tooltip("statut:N", title="Statut"),
                alt.Tooltip("count():Q", title="Nombre"),
            ],
        )
    )
    return _style(chart.properties(title="Distribution de l'âge par statut de survie", height=300))


def prepare_display_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Renvoie une copie du DataFrame brut avec des colonnes catégorielles renommées, lisibles en français."""
    display = df.copy()
    display["Sexe"] = display["Sex"].map(_SEX_LABELS).fillna(display["Sex"])
    display["Embarquement"] = display["Embarked"].map(_EMBARKED_LABELS).fillna(display["Embarked"])
    display["Classe"] = display["Pclass"].map(_PCLASS_LABELS).fillna(display["Pclass"].astype(str))
    return display
