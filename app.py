import streamlit as st
import pandas as pd
import altair as alt

# ----- Page setup -----
st.set_page_config(
    page_title="BTD Battles 2 Win Rates",
    page_icon="🎈",
    layout="wide",
)

ACCENT = "#2F9E44"  # a cheerful "winning" green, Bloons-map style

# ----- Theme: fonts, colors, and Bloons-y decorations -----
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700&family=Luckiest+Guy&display=swap');

    html, body, [class*="css"], .stMarkdown, .stText, p, span, label, li, small,
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"], [data-testid="stMetricDelta"],
    [data-testid="stWidgetLabel"], [data-testid="stMarkdownContainer"], [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] *, button {
        font-family: 'Baloo 2', sans-serif !important;
    }

    /* Readable dark-green text everywhere in the main area */
    html, body, [class*="css"], .stMarkdown, .stText, p, span, label, li, small,
    [data-testid="stMetricLabel"], [data-testid="stMetricDelta"],
    [data-testid="stWidgetLabel"], [data-testid="stMarkdownContainer"], [data-testid="stCaptionContainer"] {
        color: #1B4332 !important;
    }

    h1, h2, h3, h4 {
        font-family: 'Baloo 2', sans-serif !important;
        font-weight: 700 !important;
        color: #1B4332 !important;
    }

    /* Grassy "map" background for the whole app */
    .stApp {
        background: linear-gradient(180deg, #CFF3E0 0%, #BFE9C8 45%, #AEE1B6 100%);
    }

    /* Sidebar styled like a tower-defense control panel — stays light-on-dark, overrides the rule above */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E3A 0%, #164A2E 100%);
    }
    [data-testid="stSidebar"] * {
        color: #F2FFF4 !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #FFD43B !important;
    }

    /* Big bouncy title with a rainbow-of-bloons gradient */
    .btd-title {
        font-family: 'Luckiest Guy', cursive !important;
        font-size: 2.6rem;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #FF6B6B, #FFA94D, #FFD93D, #51CF66, #339AF0, #9775FA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0;
    }

    /* Undo the gradient-text clipping just for the balloon emoji, so they
       keep their normal colors instead of turning invisible */
    .btd-title .bloon-emoji {
        -webkit-text-fill-color: initial;
        background: none;
        -webkit-background-clip: border-box;
        background-clip: border-box;
    }

    /* Win-rate numbers pop in green */
    [data-testid="stMetricValue"] {
        color: #2F9E44 !important;
    }

    /* Dividers restyled as a cheery dashed line instead of plain gray */
    hr {
        border: none;
        border-top: 3px dashed #51CF66;
        opacity: 0.7;
    }

    /* Gentle bob for inline balloon emoji */
    @keyframes bob {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    .bloon-emoji {
        display: inline-block;
        animation: bob 2.2s ease-in-out infinite;
    }

    /* Rising balloons strip */
    @keyframes rise {
        0% { transform: translateY(0) rotate(0deg); opacity: 0.9; }
        100% { transform: translateY(-140px) rotate(8deg); opacity: 0; }
    }
    .balloon-strip {
        position: relative;
        height: 60px;
        overflow: hidden;
    }
    .balloon-strip span {
        position: absolute;
        bottom: 0;
        font-size: 26px;
        animation: rise 4s ease-in infinite;
    }
    </style>

    <div class="balloon-strip">
        <span style="left:5%;  animation-delay:0s;">🔴</span>
        <span style="left:18%; animation-delay:0.8s;">🟢</span>
        <span style="left:32%; animation-delay:1.6s;">🔵</span>
        <span style="left:46%; animation-delay:0.4s;">🟡</span>
        <span style="left:60%; animation-delay:1.2s;">🟣</span>
        <span style="left:74%; animation-delay:2s;">⚫</span>
        <span style="left:88%; animation-delay:0.2s;">🔴</span>
    </div>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    return pd.read_csv("matches.csv")


def win_rate_bar(data: pd.DataFrame, category_col: str, label: str, height: int = 320):
    """
    A bar chart of win rate per category.

    - The y-axis is locked to the 0%-100% range (scale domain=[0, 1]), so it can
      never be scrolled or zoomed into negative territory.
    - We never call .interactive() on this chart, so there's no pan/zoom at all —
      that's what was letting you scroll to -1 before.
    - Bars are sorted highest win rate first.
    - Hovering a bar shows the exact win rate and number of games it's based on.
    - All labels are forced to show (labelOverlap=False) so none get silently
      dropped when there are a lot of categories.
    """
    chart_df = data.reset_index()
    order = list(chart_df[category_col])

    chart = (
        alt.Chart(chart_df)
        .mark_bar(
            color=ACCENT,
            cornerRadiusTopLeft=4,
            cornerRadiusTopRight=4,
            size=28,
        )
        .encode(
            x=alt.X(
                f"{category_col}:N",
                sort=order,
                title=None,
                axis=alt.Axis(
                    labelAngle=-90,
                    labelOverlap=False,
                    labelFontSize=11,
                    grid=False,
                    labelLimit=140,
                ),
            ),
            y=alt.Y(
                "win_rate:Q",
                title="Win rate",
                scale=alt.Scale(domain=[0, 1], clamp=True),
                axis=alt.Axis(format="%", grid=True, gridOpacity=0.15),
            ),
            tooltip=[
                alt.Tooltip(f"{category_col}:N", title=label),
                alt.Tooltip("win_rate:Q", title="Win rate", format=".1%"),
                alt.Tooltip("games:Q", title="Games"),
            ],
        )
        .properties(height=height)
    )
    st.altair_chart(chart, use_container_width=True)


# ----- Header -----
st.markdown(
    "<div class='btd-title'>"
    "<span class='bloon-emoji'>🎈</span> BTD Battles 2 — Combo Win Rates "
    "<span class='bloon-emoji' style='animation-delay:0.6s;'>🎈</span>"
    "</div>",
    unsafe_allow_html=True,
)
st.caption(
    "Data collected from Ninja Kiwi's official Open Data API. "
    "Use the slider in the sidebar to control how many games-played a combo needs "
    "before it counts."
)

df = load_data()

with st.sidebar:
    st.header("Settings")
    min_games = st.slider(
        "Minimum games to include",
        min_value=1,
        max_value=50,
        value=15,
        help="Combos with fewer games than this are hidden — they do not "
             "have enough data to be reliable.",
    )
    st.markdown("---")
    st.metric("Matches in dataset", f"{df['match_id'].nunique():,}")

st.divider()

# ----- Headline: best combo right now -----
all_combo_stats = (
    df.groupby(["hero_base", "towers"])["won"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "win_rate", "count": "games"})
)
all_combo_stats = all_combo_stats[all_combo_stats["games"] >= min_games].sort_values(
    "win_rate", ascending=False
)

st.subheader("Best combo right now:")
if len(all_combo_stats) > 0:
    best_hero, best_towers = all_combo_stats.index[0]
    best_row = all_combo_stats.iloc[0]
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Win rate", f"{best_row['win_rate']:.0%}", f"{int(best_row['games'])} games")
        with col2:
            st.markdown(f"**Hero:** {best_hero}")
            st.markdown(f"**Towers:** {best_towers}")
else:
    st.info("No combo meets this game threshold yet — try lowering the slider in the sidebar.")

st.divider()

# ----- Hero win rates -----
st.subheader("Hero win rates")
hero_stats = (
    df.groupby("hero_base")["won"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "win_rate", "count": "games"})
)
hero_stats = hero_stats[hero_stats["games"] >= min_games].sort_values("win_rate", ascending=False)

if len(hero_stats) > 0:
    win_rate_bar(hero_stats, "hero_base", "Hero")
    st.dataframe(hero_stats.style.format({"win_rate": "{:.1%}"}), use_container_width=True)
else:
    st.info("No heroes meet this game threshold yet.")

st.divider()

# ----- Tower win rates -----
st.subheader("Tower win rates")
tower_long = df.melt(id_vars=["won"], value_vars=["tower1", "tower2", "tower3"], value_name="tower")
tower_stats = (
    tower_long.groupby("tower")["won"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "win_rate", "count": "games"})
)
tower_stats = tower_stats[tower_stats["games"] >= min_games].sort_values("win_rate", ascending=False)

if len(tower_stats) > 0:
    win_rate_bar(tower_stats, "tower", "Tower", height=380)
    st.dataframe(tower_stats.style.format({"win_rate": "{:.1%}"}), use_container_width=True)
else:
    st.info("No towers meet this game threshold yet.")

st.divider()

# ----- Combo explorer -----
st.subheader("Combo win rates")
hero_options = ["All heroes"] + sorted(df["hero_base"].unique())
selected_hero = st.selectbox("Filter to a hero", hero_options)

combo_df = df if selected_hero == "All heroes" else df[df["hero_base"] == selected_hero]
combo_stats = (
    combo_df.groupby(["hero_base", "towers"])["won"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "win_rate", "count": "games"})
)
combo_stats = combo_stats[combo_stats["games"] >= min_games].sort_values("win_rate", ascending=False)

st.caption(f"{len(combo_stats)} combo(s) meet the {min_games}-game threshold")

if len(combo_stats) > 0:
    top_combos = combo_stats.head(10).reset_index()
    top_combos["combo_label"] = top_combos["hero_base"] + " + " + top_combos["towers"]
    top_combos = top_combos.set_index("combo_label")
    win_rate_bar(top_combos, "combo_label", "Combo", height=420)
    st.dataframe(combo_stats.style.format({"win_rate": "{:.1%}"}), use_container_width=True)
else:
    st.info("No combos meet this game threshold yet — try lowering the slider.")

st.divider()
st.markdown(
    """
    <div class="balloon-strip">
        <span style="left:10%; animation-delay:0.3s;">🟡</span>
        <span style="left:30%; animation-delay:1.1s;">🔵</span>
        <span style="left:50%; animation-delay:0.6s;">🔴</span>
        <span style="left:70%; animation-delay:1.8s;">🟢</span>
        <span style="left:88%; animation-delay:0.9s;">🟣</span>
    </div>
    """,
    unsafe_allow_html=True,
)