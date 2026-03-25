import streamlit as st
import pandas as pd

st.set_page_config(page_title="IMDB Movie Explorer", layout="wide")

st.title("🎬 IMDB Movie Explorer")

# Data
imdb = pd.read_csv('IMDB-Movie-Data.csv')
imdb = imdb[['Title','Genre','Director','Actors','Year','Rating']]

# Filters
text_title = st.text_input('Title')
text_actor = st.text_input('Actors')
text_director = st.text_input('Director')

genre_list = imdb['Genre'].str.split(',').explode().unique()
genre = st.multiselect('Genre', genre_list)

year = st.selectbox('Year', ['All'] + sorted(imdb['Year'].unique()))

search_btn = st.button("🔍 Search")

# Filter logic
if search_btn:
    filtered = imdb.copy()

    if text_title:
        filtered = filtered[filtered['Title'].str.contains(text_title, case=False)]

    if text_actor:
        filtered = filtered[filtered['Actors'].str.contains(text_actor, case=False)]

    if text_director:
        filtered = filtered[filtered['Director'].str.contains(text_director, case=False)]

    if genre:
        for g in genre:
            filtered = filtered[filtered['Genre'].str.contains(g)]

    if year != 'All':
        filtered = filtered[filtered['Year'] == year]

    filtered = filtered.sort_values('Rating', ascending=False).reset_index(drop=True)

    st.markdown("---")

    if len(filtered) == 0:
        st.warning("No results found")
    else:
        st.subheader("Results")

        # 🔹 Stylish result count
        st.markdown(
            f"""
            <div style="font-size:18px;font-weight:500;margin-bottom:20px">
                {len(filtered)} results found
            </div>
            """,
            unsafe_allow_html=True
        )

        # 🔹 CARD STYLE (CSS)
        st.markdown("""
        <style>
        .movie-card {
            background: linear-gradient(145deg, #ffffff, #f0f2f6);
            padding: 18px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.08);
            transition: 0.3s;
        }
        .movie-card:hover {
            transform: scale(1.03);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        .title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .meta {
            font-size: 14px;
            color: #555;
        }
        .rating {
            font-size: 16px;
            font-weight: bold;
            color: #ffb400;
            margin-bottom: 6px;
        }
        </style>
        """, unsafe_allow_html=True)

        # 🔹 2-li grid
        for i in range(0, len(filtered), 2):
            col1, col2 = st.columns(2)

            with col1:
                row = filtered.iloc[i]
                st.markdown(f"""
                <div class="movie-card">
                    <div class="title">🎥 {row['Title']} ({row['Year']})</div>
                    <div class="rating">⭐ {row['Rating']}</div>
                    <div class="meta">🎭 {row['Genre']}</div>
                    <div class="meta">🎬 {row['Director']}</div>
                    <div class="meta">👥 {row['Actors']}</div>
                </div>
                """, unsafe_allow_html=True)

            if i + 1 < len(filtered):
                with col2:
                    row = filtered.iloc[i + 1]
                    st.markdown(f"""
                    <div class="movie-card">
                        <div class="title">🎥 {row['Title']} ({row['Year']})</div>
                        <div class="rating">⭐ {row['Rating']}</div>
                        <div class="meta">🎭 {row['Genre']}</div>
                        <div class="meta">🎬 {row['Director']}</div>
                        <div class="meta">👥 {row['Actors']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    