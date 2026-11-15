import streamlit as st
import pandas as pd
import plotly.express as px


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Wine Discovery",
    page_icon="🍷",
    layout="wide"
)


# =====================================================
# 2. CUSTOM DESIGN
# =====================================================

st.markdown("""
<style>
.stApp {
    background-color: #151116;
    color: #F5EDE8;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

h1 {
    color: #F2D6D0 !important;
    font-family: Georgia, serif;
    font-size: 42px !important;
}

h2, h3 {
    color: #D99AA6 !important;
    font-family: Georgia, serif;
}

p {
    color: #D8CDD2;
}

[data-testid="stMetric"] {
    background-color: #261B24;
    border: 1px solid #68404F;
    padding: 20px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #D9A7B1 !important;
}

[data-testid="stMetricValue"] {
    color: #F5E6E9 !important;
}

.stSelectbox label,
.stMultiSelect label,
.stSlider label,
.stNumberInput label,
.stTextInput label {
    color: #E5B8C1 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #68404F;
    border-radius: 10px;
}

hr {
    border-color: #68404F;
}


/* Navigation */

.top-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 20px 0 30px 0;
    padding: 15px;
    background: #261B24;
    border: 1px solid #68404F;
    border-radius: 12px;
}

.top-nav a {
    color: #F2D6D0 !important;
    background: #49303D;
    padding: 10px 16px;
    border-radius: 8px;
    text-decoration: none !important;
    font-size: 14px;
    transition: 0.2s;
}

.top-nav a:hover {
    background: #85485E;
    color: white !important;
}


/* Wine Cards */

.wine-card {
    background: linear-gradient(145deg, #30202B, #1D171D);
    border: 1px solid #754454;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 16px;
    height: 390px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.wine-card h3 {
    color: #F2D6D0 !important;
    font-family: Georgia, serif;
    font-size: 21px;
    line-height: 1.3;
    margin: 12px 0 5px 0;
}

.wine-card .winery {
    color: #D99AA6;
    font-size: 14px;
    margin-bottom: 12px;
}

.wine-card .wine-type {
    display: inline-block;
    background-color: #603344;
    color: #F5DCE2;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    width: fit-content;
    align-self: flex-start;
    margin-bottom: 5px;
}

.wine-card .rating {
    font-size: 15px;
    color: #F5D6A5;
    margin-bottom: 6px;
}

.wine-card .score {
    color: #E6A8B5;
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 5px;
}

.wine-card .details {
    color: #C9B9C1;
    font-size: 13px;
    line-height: 1.7;
}

.wine-card a {
    display: inline-block;
    color: #F2B7C4 !important;
    text-decoration: none;
    border: 1px solid #A45B70;
    padding: 7px 13px;
    border-radius: 7px;
    margin-top: auto;
    width: fit-content;
    align-self: flex-start;
}

.wine-card a:hover {
    background-color: #603344;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. LOAD DATASETS
# =====================================================

@st.cache_data
def load_quality_data():

    red_wine = pd.read_csv(
        "data/winequality-red.csv",
        sep=";"
    )

    white_wine = pd.read_csv(
        "data/winequality-white.csv",
        sep=";"
    )

    red_wine = red_wine.drop_duplicates().copy()
    white_wine = white_wine.drop_duplicates().copy()

    red_wine["wine_type"] = "Red"
    white_wine["wine_type"] = "White"

    wine = pd.concat(
        [red_wine, white_wine],
        ignore_index=True
    )

    return wine


@st.cache_data
def load_vivino_data():

    return pd.read_csv("data/vivino_cleaned.csv")


wine = load_quality_data()
vivino = load_vivino_data()


# =====================================================
# 4. WEIGHTED RATING CALCULATION
# =====================================================

average_rating = vivino["rating"].mean()

minimum_reviews_for_ranking = 100

vivino["weighted_rating"] = (
    (
        vivino["ratings_count"]
        / (
            vivino["ratings_count"]
            + minimum_reviews_for_ranking
        )
    ) * vivino["rating"]
    +
    (
        minimum_reviews_for_ranking
        / (
            vivino["ratings_count"]
            + minimum_reviews_for_ranking
        )
    ) * average_rating
)


# =====================================================
# 5. MAIN TITLE AND NAVIGATION
# =====================================================

st.title("🍷 Wine Discovery")

st.write(
    "Explore wine quality, discover real wine brands, "
    "and find wines that match your preferences."
)

st.markdown("""
<div class="top-nav">
    <a href="#quality-overview">📊 Quality Overview</a>
    <a href="#quality-analysis">🍷 Quality Analysis</a>
    <a href="#chemical-explorer">🧪 Chemical Properties</a>
    <a href="#real-wines">🍇 Real Wine Collection</a>
    <a href="#wine-finder">🔎 Wine Finder</a>
</div>
""", unsafe_allow_html=True)

st.divider()


# =====================================================
# 6. WINE QUALITY OVERVIEW
# =====================================================

st.markdown(
    '<div id="quality-overview"></div>',
    unsafe_allow_html=True
)

st.header("Wine Quality Overview")

st.write(
    "Explore the chemical characteristics and laboratory "
    "quality scores of red and white wines."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Wine Samples", f"{len(wine):,}")

with col2:
    st.metric(
        "Red Wine Samples",
        f"{len(wine[wine['wine_type'] == 'Red']):,}"
    )

with col3:
    st.metric(
        "White Wine Samples",
        f"{len(wine[wine['wine_type'] == 'White']):,}"
    )

selected_type = st.selectbox(
    "Explore wine type:",
    ["All", "Red", "White"]
)

if selected_type == "All":
    filtered_wine = wine.copy()
else:
    filtered_wine = wine[
        wine["wine_type"] == selected_type
    ]

with st.expander("View Wine Quality Dataset"):

    st.dataframe(
        filtered_wine.head(20),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# 7. WINE QUALITY ANALYSIS
# =====================================================

st.markdown(
    '<div id="quality-analysis"></div>',
    unsafe_allow_html=True
)

st.subheader("Wine Quality Analysis")

chart1, chart2 = st.columns(2)

with chart1:

    quality_counts = (
        filtered_wine["quality"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    quality_counts.columns = [
        "Quality",
        "Number of Samples"
    ]

    fig1 = px.bar(
        quality_counts,
        x="Quality",
        y="Number of Samples",
        title="Wine Quality Distribution",
        color_discrete_sequence=["#B76E79"]
    )

    fig1.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151116",
        plot_bgcolor="#151116"
    )

    st.plotly_chart(fig1, use_container_width=True)


with chart2:

    average_quality = (
        wine.groupby("wine_type")["quality"]
        .mean()
        .reset_index()
    )

    fig2 = px.bar(
        average_quality,
        x="wine_type",
        y="quality",
        color="wine_type",
        title="Average Quality by Wine Type",
        color_discrete_map={
            "Red": "#9E425B",
            "White": "#D9A0A7"
        }
    )

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151116",
        plot_bgcolor="#151116",
        showlegend=False
    )

    st.plotly_chart(fig2, use_container_width=True)


fig3 = px.scatter(
    filtered_wine,
    x="alcohol",
    y="quality",
    color="wine_type",
    title="Alcohol Content vs Wine Quality",
    color_discrete_map={
        "Red": "#9E425B",
        "White": "#D9A0A7"
    },
    opacity=0.6
)

fig3.update_layout(
    template="plotly_dark",
    paper_bgcolor="#151116",
    plot_bgcolor="#151116"
)

st.plotly_chart(fig3, use_container_width=True)


# =====================================================
# 8. CHEMICAL PROPERTIES EXPLORER
# =====================================================

st.markdown(
    '<div id="chemical-explorer"></div>',
    unsafe_allow_html=True
)

st.divider()

st.header("Chemical Properties Explorer")

st.write(
    "Investigate the distribution of chemical properties "
    "and their relationship with laboratory wine quality."
)

chemical_properties = {
    "Alcohol": "alcohol",
    "Volatile Acidity": "volatile acidity",
    "Citric Acid": "citric acid",
    "Residual Sugar": "residual sugar",
    "Fixed Acidity": "fixed acidity",
    "Chlorides": "chlorides",
    "Sulphates": "sulphates",
    "Density": "density",
    "pH": "pH",
    "Free Sulfur Dioxide": "free sulfur dioxide",
    "Total Sulfur Dioxide": "total sulfur dioxide"
}

selected_chemical = st.selectbox(
    "Choose a chemical property:",
    list(chemical_properties.keys())
)

chemical_column = chemical_properties[selected_chemical]

chemical_col1, chemical_col2 = st.columns(2)

with chemical_col1:

    fig4 = px.histogram(
        filtered_wine,
        x=chemical_column,
        color="wine_type",
        marginal="box",
        title=f"{selected_chemical} Distribution",
        color_discrete_map={
            "Red": "#9E425B",
            "White": "#D9A0A7"
        }
    )

    fig4.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151116",
        plot_bgcolor="#151116"
    )

    st.plotly_chart(fig4, use_container_width=True)


with chemical_col2:

    fig5 = px.scatter(
        filtered_wine,
        x=chemical_column,
        y="quality",
        color="wine_type",
        title=f"{selected_chemical} vs Quality",
        color_discrete_map={
            "Red": "#9E425B",
            "White": "#D9A0A7"
        },
        opacity=0.6
    )

    fig5.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151116",
        plot_bgcolor="#151116"
    )

    st.plotly_chart(fig5, use_container_width=True)


# =====================================================
# 9. REAL WINE COLLECTION
# =====================================================

st.markdown(
    '<div id="real-wines"></div>',
    unsafe_allow_html=True
)

st.divider()

st.header("Real Wine Collection")

st.write(
    "Discover real wines from different wineries, "
    "countries, and regions."
)

vcol1, vcol2, vcol3 = st.columns(3)

with vcol1:
    st.metric("Wine Records", f"{len(vivino):,}")

with vcol2:
    st.metric("Countries", vivino["country"].nunique())

with vcol3:
    st.metric("Wineries", vivino["winery_name"].nunique())


with st.expander("Explore Wine Collection"):

    collection_columns = [
        "wine_name",
        "winery_name",
        "wine_type",
        "rating",
        "ratings_count",
        "country",
        "region",
        "vintage_year"
    ]

    st.dataframe(
        vivino[collection_columns].head(30),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# 10. INTERACTIVE WINE FINDER
# =====================================================

st.markdown(
    '<div id="wine-finder"></div>',
    unsafe_allow_html=True
)

st.divider()

st.header("🍷 Find Your Perfect Wine")

st.write(
    "Discover wines that match your preferences. "
    "Filter by wine type, country, customer rating, "
    "popularity, or search for a specific winery."
)


wine_types = sorted(
    vivino["wine_type"].dropna().unique().tolist()
)

selected_wine_types = st.multiselect(
    "Choose wine types:",
    options=wine_types,
    default=wine_types
)


countries = sorted(
    vivino["country"].dropna().unique().tolist()
)

selected_countries = st.multiselect(
    "Choose countries:",
    options=countries
)


minimum_rating = st.slider(
    "Minimum customer rating:",
    min_value=2.0,
    max_value=5.0,
    value=4.0,
    step=0.1
)


minimum_reviews = st.number_input(
    "Minimum number of customer reviews:",
    min_value=0,
    max_value=int(vivino["ratings_count"].max()),
    value=100,
    step=50
)


search_term = st.text_input(
    "Search by wine or winery:",
    placeholder="Example: Cabernet Sauvignon or Antinori"
)


# =====================================================
# 11. FILTER AND RANK RECOMMENDATIONS
# =====================================================

recommendations = vivino.copy()

recommendations = recommendations[
    recommendations["wine_type"].isin(selected_wine_types)
]

if selected_countries:

    recommendations = recommendations[
        recommendations["country"].isin(selected_countries)
    ]

recommendations = recommendations[
    recommendations["rating"] >= minimum_rating
]

recommendations = recommendations[
    recommendations["ratings_count"] >= minimum_reviews
]

if search_term:

    search_mask = (
        recommendations["wine_name"].str.contains(
            search_term,
            case=False,
            na=False
        )
        |
        recommendations["winery_name"].str.contains(
            search_term,
            case=False,
            na=False
        )
    )

    recommendations = recommendations[search_mask]


recommendations = recommendations.sort_values(
    by="weighted_rating",
    ascending=False
)


# =====================================================
# 12. WINE RECOMMENDATION CARDS
# =====================================================

st.subheader("Your Wine Recommendations")

result_col1, result_col2 = st.columns(2)

with result_col1:

    st.metric(
        "Matching Wines",
        f"{len(recommendations):,}"
    )

with result_col2:

    if not recommendations.empty:

        st.metric(
            "Highest Weighted Rating",
            f"{recommendations['weighted_rating'].max():.2f} ⭐"
        )

    else:

        st.metric(
            "Highest Weighted Rating",
            "—"
        )


if recommendations.empty:

    st.warning(
        "No wines match your preferences. "
        "Try adjusting your filters."
    )

else:

    st.caption(
        "Wines are ranked from highest to lowest weighted rating."
    )

    for i in range(0, min(len(recommendations), 50), 2):

        columns = st.columns(2)

        for j in range(2):

            index = i + j

            if index >= min(len(recommendations), 50):
                break

            row = recommendations.iloc[index]

            wine_name = str(row["wine_name"])
            winery = str(row["winery_name"])
            wine_type = str(row["wine_type"])
            country = str(row["country"])
            region = str(row["region"])

            rating = row["rating"]
            weighted_rating = row["weighted_rating"]
            reviews = int(row["ratings_count"])

            vintage = row["vintage_year"]

            if pd.isna(vintage):
                vintage = "Not specified"
            else:
                vintage = str(int(vintage))

            wine_url = row.get("vivino_url", "")

            if pd.isna(wine_url):
                wine_url = ""

            link_html = ""

            if wine_url:
                link_html = (
                    f'<a href="{wine_url}" '
                    f'target="_blank">View on Vivino ↗</a>'
                )

            card_html = f"""
            <div class="wine-card">

                <div class="wine-type">
                    {wine_type}
                </div>

                <h3>{wine_name}</h3>

                <div class="winery">
                    {winery}
                </div>

                <div class="rating">
                    ⭐ Customer Rating: {rating:.1f}/5
                </div>

                <div class="score">
                    ✨ Weighted Rating: {weighted_rating:.2f}/5
                </div>

                <div class="details">
                    💬 {reviews:,} customer reviews<br>
                    🌍 {region}, {country}<br>
                    🍇 Vintage: {vintage}
                </div>

                {link_html}

            </div>
            """

            with columns[j]:
                st.html(card_html)

    if len(recommendations) > 50:

        st.caption(
            f"Showing the top 50 of "
            f"{len(recommendations):,} matching wines."
        )


# =====================================================
# 13. FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div style="text-align: center; color: #D99AA6;">
        <p>Wine Discovery | Intermediate Python Project</p>
        <p>Data sources: UCI Wine Quality and Vivino dataset</p>
    </div>
    """,
    unsafe_allow_html=True
)
