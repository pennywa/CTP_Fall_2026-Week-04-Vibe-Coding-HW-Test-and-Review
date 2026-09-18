import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Set dashboard to span full browser width
st.set_page_config(
    page_title="MovieLens Vibe Coding Dashboard",
    page_icon="🎬",
    layout="wide"
)

@st.cache_data
def load_data():
    movies = pd.read_csv("data/ml-latest-small/movies.csv")
    ratings = pd.read_csv("data/ml-latest-small/ratings.csv")

    movies["year"] = pd.to_numeric(
        movies["title"].str.extract(r"\((\d{4})\)", expand=False),
        errors="coerce",
    ).astype("Int64")
    movies["clean_title"] = (
        movies["title"]
        .str.replace(r"\s*\(\d{4}\)\s*$", "", regex=True)
        .str.strip()
    )

    df = ratings.merge(movies, on="movieId", how="inner")
    return df


df = load_data()

df_genres = df.assign(genre=df["genres"].str.split("|")).explode("genre")
df_genres = df_genres[df_genres["genre"] != "(no genres listed)"]

st.title("MovieLens Dashboard")
st.write(
    f"Total rows: {len(df):,} | Unique movies: {df['movieId'].nunique():,}"
)
st.dataframe(df.head())

genre_counts = (
    df_genres.groupby("genre", as_index=False)
    .size()
    .rename(columns={"size": "rating_count"})
    .sort_values("rating_count", ascending=False)
)

fig_genre_counts = px.bar(
    genre_counts,
    x="rating_count",
    y="genre",
    orientation="h",
    title="Rating Counts by Genre",
    labels={"rating_count": "Number of ratings", "genre": "Genre"},
)
fig_genre_counts.update_yaxes(categoryorder="total ascending")

genre_avg = (
    df_genres.groupby("genre", as_index=False)["rating"]
    .mean()
    .rename(columns={"rating": "avg_rating"})
    .sort_values("avg_rating", ascending=False)
)

fig_genre_avg = px.bar(
    genre_avg,
    x="avg_rating",
    y="genre",
    orientation="h",
    title="Average Rating by Genre",
    labels={"avg_rating": "Average rating", "genre": "Genre"},
    range_x=[0, 5],
)
fig_genre_avg.update_yaxes(categoryorder="total ascending")
fig_genre_avg.update_xaxes(range=[0, 5])

catalog_avg = df["rating"].mean()
fig_genre_dots = px.scatter(
    genre_avg,
    x="avg_rating",
    y="genre",
    title="Average Rating by Genre (Cleveland Dot Plot)",
    labels={"avg_rating": "Average rating", "genre": "Genre"},
    range_x=[3.0, 4.2],
)
fig_genre_dots.update_traces(marker=dict(size=12))
fig_genre_dots.update_yaxes(
    categoryorder="array",
    categoryarray=genre_avg.sort_values("avg_rating", ascending=True)["genre"].tolist(),
)
fig_genre_dots.update_xaxes(range=[3.0, 4.2])
fig_genre_dots.add_vline(
    x=catalog_avg,
    line_dash="dash",
    annotation_text=f"Catalog avg ({catalog_avg:.2f})",
    annotation_position="top",
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Question 1 — Genre Breakdown")
    st.plotly_chart(fig_genre_counts, use_container_width=True)
    st.caption(
        "Horizontal bar charts allow easy visual comparison across 18 categories "
        "without the label collision and slice distortion typical of an 18-slice pie chart."
    )

with col2:
    st.subheader("Question 2 — Genre Satisfaction")
    tab_ai, tab_human = st.tabs(
        ["🤖 Initial AI Output", "👤 Human-in-the-Loop Refinement"]
    )

    with tab_ai:
        st.plotly_chart(fig_genre_avg, use_container_width=True)
        st.markdown(
            '**AI Default Rationale:** "A horizontal bar chart grounded from 0 to 5 '
            'preserves the full rating scale and prevents visual exaggeration of '
            'small differences."'
        )
        st.warning(
            '**Human-in-the-Loop Critique:** "This is a textbook low-signal '
            "visualization. Grounding the scale to 0 flattens all 18 genres into a "
            "monolithic blue block between 3.2 and 3.9 stars. It wastes visual ink "
            "on empty space (0 to 3) and obscures meaningful rank distinctions and "
            'score distribution."'
        )

    with tab_human:
        st.plotly_chart(fig_genre_dots, use_container_width=True)
        st.caption(
            "Dot plots remove the bar-area zero-baseline requirement, allowing a "
            "focused scale and clear relative comparisons without distorting data."
        )

yearly_ratings = (
    df.dropna(subset=["year"])
    .groupby("year", as_index=False)
    .agg(avg_rating=("rating", "mean"), rating_count=("rating", "size"))
)
yearly_ratings = yearly_ratings[yearly_ratings["rating_count"] >= 20].copy()
yearly_ratings["year"] = yearly_ratings["year"].astype(int)
yearly_ratings = yearly_ratings.sort_values("year")

fig_yearly = px.line(
    yearly_ratings,
    x="year",
    y="avg_rating",
    markers=True,
    title="Mean Rating by Movie Release Year",
    labels={"year": "Release year", "avg_rating": "Average rating"},
)

movie_stats = df.groupby("clean_title", as_index=False).agg(
    avg_rating=("rating", "mean"),
    rating_count=("rating", "size"),
)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Question 3 — Ratings Over Time")
    st.plotly_chart(fig_yearly, use_container_width=True)
    st.caption(
        "A line chart is ideal for showing continuous temporal trends, and filtering "
        "out sparse early years prevents single-movie outliers from distorting the "
        "historical pattern."
    )

with col4:
    st.subheader("Question 4 — Best Movies, With a Floor")
    min_ratings = st.slider(
        "Minimum rating count",
        min_value=10,
        max_value=200,
        value=50,
        step=10,
    )
    top_movies = (
        movie_stats[movie_stats["rating_count"] >= min_ratings]
        .sort_values("avg_rating", ascending=False)
        .head(5)
    )

    fig_top_movies = px.bar(
        top_movies,
        x="avg_rating",
        y="clean_title",
        orientation="h",
        title=f"Top 5 Movies (≥ {min_ratings} ratings)",
        labels={"avg_rating": "Average rating", "clean_title": "Movie"},
        hover_data=["rating_count"],
        range_x=[0, 5],
    )
    fig_top_movies.update_yaxes(categoryorder="total ascending")
    fig_top_movies.update_xaxes(range=[0, 5])
    fig_top_movies.update_layout(margin=dict(l=0, r=0, t=40, b=40))

    top_refined = top_movies.copy()
    top_refined["display_title"] = top_refined["clean_title"].map(
        lambda title: title[:32] + "..." if len(title) > 35 else title
    )
    top_refined["annotation"] = [
        f"{rating:.2f} ★ (n={int(count)})"
        for rating, count in zip(
            top_refined["avg_rating"], top_refined["rating_count"]
        )
    ]

    fig_top_refined = px.bar(
        top_refined,
        x="avg_rating",
        y="display_title",
        orientation="h",
        text="annotation",
        title=f"Top 5 Movies (≥ {min_ratings} ratings)",
        labels={"avg_rating": "Average rating", "display_title": "Movie"},
        hover_data=["clean_title", "rating_count"],
        range_x=[3.5, 5.0],
    )
    fig_top_refined.update_traces(
        textposition="inside",
        insidetextanchor="middle",
    )
    fig_top_refined.update_yaxes(autorange="reversed")
    fig_top_refined.update_xaxes(range=[3.5, 5.0])
    fig_top_refined.update_layout(margin=dict(l=220, r=40, t=30, b=40))

    fig_lollipop = go.Figure()
    for _, row in top_refined.iterrows():
        fig_lollipop.add_trace(
            go.Scatter(
                x=[3.5, row["avg_rating"]],
                y=[row["display_title"], row["display_title"]],
                mode="lines",
                line=dict(width=2, color="#8aabb8"),
                hoverinfo="skip",
                showlegend=False,
            )
        )
    fig_lollipop.add_trace(
        go.Scatter(
            x=top_refined["avg_rating"],
            y=top_refined["display_title"],
            mode="markers",
            marker=dict(size=15, color="#1f77b4"),
            customdata=top_refined["rating_count"],
            hovertemplate=(
                "%{y}<br>Average rating: %{x:.2f}<br>n=%{customdata}<extra></extra>"
            ),
            showlegend=False,
        )
    )
    for _, row in top_refined.iterrows():
        fig_lollipop.add_annotation(
            x=row["avg_rating"],
            y=row["display_title"],
            text=f"  {row['avg_rating']:.2f} ★ (n={int(row['rating_count'])})",
            showarrow=False,
            xanchor="left",
            yanchor="middle",
        )
    fig_lollipop.update_layout(
        title=f"Top 5 Movies (≥ {min_ratings} ratings)",
        xaxis_title="Average rating",
        yaxis_title="Movie",
        margin=dict(l=220, r=60, t=30, b=40),
    )
    fig_lollipop.update_xaxes(range=[3.4, 5.0])
    fig_lollipop.update_yaxes(autorange="reversed")

    tab_ai_q4, tab_iter1_q4, tab_iter2_q4 = st.tabs(
        [
            "🤖 Initial AI Output",
            "👤 Iteration 1: Refined Bar",
            "🎨 Iteration 2: Taste Refinement (Lollipop)",
        ]
    )

    with tab_ai_q4:
        st.plotly_chart(fig_top_movies, use_container_width=True)
        st.markdown(
            '**AI Default Rationale:** "A horizontal bar chart displays movie titles '
            'horizontally while a 0–5 axis maintains an unskewed baseline scale."'
        )
        st.warning(
            '**Human-in-the-Loop Critique:** "This chart fails in layout and '
            "analytical utility. Unconstrained labels push the canvas off-screen, "
            "truncating the x-axis label into 'Average ratir' and flattening the "
            "top scores into visually indistinguishable blue blocks. It also hides "
            'the review count—the core variable behind the floor filter."'
        )

    with tab_iter1_q4:
        st.plotly_chart(fig_top_refined, use_container_width=True)
        st.info(
            '**Human Feedback:** "Technically correct and readable, but heavy on '
            "ink. For only 5 data points, solid horizontal bars feel bulky and "
            'redundant alongside the genre charts."'
        )

    with tab_iter2_q4:
        st.plotly_chart(fig_lollipop, use_container_width=True)
        st.caption(
            '**Design Defense:** "A lollipop chart maximizes the data-to-ink ratio '
            "for small categorical leaderboards. Replacing bulky bars with slender "
            "stems introduces visual diversity to the dashboard while directing "
            'immediate focus to rank position and rating values."'
        )
