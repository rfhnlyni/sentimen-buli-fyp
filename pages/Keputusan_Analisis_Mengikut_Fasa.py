import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt 

# Page Config
st.set_page_config(page_title="Keputusan Analisis Sentimen Mengikut Fasa", layout="wide")

# Header
st.markdown("""<h4 style="font-size: 32px; text-align: center; color: white; background-color: #4B3C91; padding: 10px; border-radius: 10px;">Sistem Analisis Sentimen Mengenai Isu Buli Di IPTA</h4>""", unsafe_allow_html=True)
st.markdown('######')
st.markdown("<h5 style='font-size: 23px;'>Analisis Mengikut Fasa</h5>", unsafe_allow_html=True)

st.markdown("<h5 style='font-size: 23px;'>Graf Perubahan Sentimen Mengikut Fasa</h5>", unsafe_allow_html=True)

# Read CSV
try:
    sentiment_phase_df = pd.read_csv('sentiment_distribution_by_phase.csv')

    sentiment_long = sentiment_phase_df.melt(id_vars='Phase', 
                                              value_vars=['negative', 'neutral', 'positive'],
                                              var_name='Sentimen', value_name='Jumlah')

    # Sort
    sentiment_long['Phase'] = pd.Categorical(sentiment_long['Phase'], ordered=True, categories=sorted(sentiment_phase_df['Phase'].tolist()))
    sentiment_long = sentiment_long.sort_values('Phase')

    # Plot line chart
    line_chart = alt.Chart(sentiment_long).mark_line(point=True).encode(
        x=alt.X('Phase:N', title='Fasa Analisis'),
        y=alt.Y('Jumlah:Q', title='Jumlah Sentimen'),
        color=alt.Color('Sentimen:N', title='Sentimen',
                        scale=alt.Scale(domain=['negative', 'neutral', 'positive'],
                                        range=['#FF6B6B', '#FFD93D', '#6BCB77'])),
        tooltip=['Phase', 'Sentimen', 'Jumlah']
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(line_chart, use_container_width=True)

except Exception as e:
    st.error(f"Gagal baca atau paparkan fail sentiment_by_phase.csv: {e}")

# Load data sentiment distribution
try:
    df_sentiment = pd.read_csv("sentiment_distribution_by_phase.csv")
    df_sentiment.rename(columns={'Phase': 'Fasa'}, inplace=True)
    df_sentiment['Fasa'] = df_sentiment['Fasa'].str.replace("Phase", "Fasa")
except Exception as e:
    st.error(f"Gagal membaca fail sentiment: {e}")
    df_sentiment = None

# Load data tweets
try:
    df_tweets = pd.read_csv("bert_results_with_phase.csv") 
    df_tweets.rename(columns={'Sentiment_Bert': 'Sentimen'}, inplace=True)
    df_tweets.rename(columns={'Phase': 'Fasa'}, inplace=True)
    df_tweets['Fasa'] = df_tweets['Fasa'].str.replace("Phase", "Fasa")
except Exception as e:
    st.error(f"Gagal membaca fail tweets: {e}")
    df_tweets = None

if df_sentiment is not None and df_tweets is not None:
    for _, row in df_sentiment.iterrows():
        fasa = row['Fasa']
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"<h5 style='font-size: 23px;'>{fasa}</h5>", unsafe_allow_html=True)
            pie_data = pd.DataFrame({
                'Sentimen': ['Positif', 'Neutral', 'Negatif'],
                'Jumlah Tweet': [row['positive'], row['neutral'], row['negative']]
            })
            
            fig = px.pie(
                pie_data,
                names='Sentimen',
                values='Jumlah Tweet',
                color='Sentimen',
                color_discrete_map={
                    'Positif': '#4CAF50',
                    'Neutral': '#FFC107',
                    'Negatif': '#F44336'
                },
                hover_data=['Jumlah Tweet']
            )
            
            fig.update_traces(
                textinfo='percent+label',
                hovertemplate='%{label}: %{value} tweet<extra></extra>'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"<h5 style='font-size: 23px;'>Tweet {fasa}</h5>", unsafe_allow_html=True)
            tweets_fasa = df_tweets[df_tweets['Fasa'] == fasa][['Username', 'Tweet', 'Sentimen']]
            if tweets_fasa.empty:
                st.write("Tiada tweet untuk fasa ini.")
            else:
                st.dataframe(tweets_fasa.reset_index(drop=True), use_container_width=True)

else:
    st.info("Data sentimen atau tweet tidak tersedia.")

# Design Button
# Inject custom CSS for the button
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #4B3C91;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #372a6d;
        color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)


# Button next page
if st.button('📊 Papar Hasil Analisis Keseluruhan', use_container_width=True):
    st.switch_page('pages/Keputusan_Analisis_Keseluruhan.py')

st.markdown("""---""")

# Footer
st.markdown("""
    <div style='text-align: center; color: grey; font-size: 14px;'>
        © 2025 Rifhan Ilyani — Final Year Project | Universiti Kebangsaan Malaysia
    </div>
""", unsafe_allow_html=True)
