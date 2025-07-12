import streamlit as st
import pandas as pd
import altair as alt

# Page config
st.set_page_config(page_title='Keputusan Analisis Sentimen', layout='wide')

# Read accuracy value
def read_accuracy(file_path):
    try:
        df = pd.read_csv(file_path)
        if 'Accuracy' not in df.columns or df.empty:
            raise ValueError(f"Fail '{file_path}' tidak mengandungi lajur 'Accuracy' atau kosong.")
        return float(df['Accuracy'].iloc[0])
    except Exception as e:
        st.error(f"Ralat membaca ketepatan dari '{file_path}': {e}")
        return None

# Read CSV with fallback
def read_csv_file(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Gagal membaca fail '{file_path}': {e}")
        return pd.DataFrame()

# Read data
svm_acc_value = read_accuracy('svm_accuracy.csv')
bert_acc_value = read_accuracy('bert_accuracy.csv')

svm_classification_report = read_csv_file('svm_classification_report.csv')
bert_classification_report = read_csv_file('bert_classification_report.csv')
svm_results = read_csv_file('svm_results.csv')
bert_results = read_csv_file('bert_results.csv')

# Check accuracy
if svm_acc_value is not None and bert_acc_value is not None:
    combined_accuracy = pd.DataFrame({
        'Model': ['SVM', 'BERT'],
        'Ketepatan': [svm_acc_value, bert_acc_value]
    })

    # Show header
    st.markdown(
        "<h4 style='font-size: 32px; text-align: center; color: white; background-color: #4B3C91; padding: 10px; border-radius: 10px;'>"
        "Sistem Analisis Sentimen Mengenai Isu Buli Di IPTA</h4>", 
        unsafe_allow_html=True
    )
    st.markdown('######')
    st.markdown("<h5 style='font-size: 23px;'>Analisis Keseluruhan</h5>", unsafe_allow_html=True)

    # Layout
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<h5 style='font-size: 18px;'>Perbandingan Ketepatan Model</h5>", unsafe_allow_html=True)
        st.table(combined_accuracy)

        st.markdown("<h5 style='font-size: 18px;'>Visualisasi Perbandingan Model</h5>", unsafe_allow_html=True)
        chart = alt.Chart(combined_accuracy).mark_bar(size=60).encode(
            x=alt.X('Model', sort=None, axis=alt.Axis(title=None, labels=False, ticks=False)),
            y=alt.Y('Ketepatan', title='Ketepatan', scale=alt.Scale(domain=[0, 1])),
            color=alt.Color('Model', scale=alt.Scale(range=['#4B3C91', '#FF6F61'])),
            tooltip=['Model', alt.Tooltip('Ketepatan', format='.2f')]
        ).properties(height=380)

        text = chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-10,
            fontSize=14,
            fontWeight='bold'
        ).encode(
            text=alt.Text('Ketepatan:Q', format='.2f')
        )

        st.altair_chart(chart + text, use_container_width=True)

    with col2:
        st.markdown("<h5 style='font-size: 18px;'>Laporan Klasifikasi Model SVM</h5>", unsafe_allow_html=True)
        st.table(svm_classification_report)
        st.markdown("<h5 style='font-size: 18px;'>Laporan Klasifikasi Model BERT</h5>", unsafe_allow_html=True)
        st.table(bert_classification_report)

    st.markdown('------')
    st.markdown("<h5 style='font-size: 23px;'>Analisis Terperinci</h5>", unsafe_allow_html=True)

    if not svm_results.empty:
        st.markdown("<h5 style='font-size: 18px;'>Keseluruhan SVM</h5>", unsafe_allow_html=True)
        st.table(svm_results.head(5))
        with st.expander("Lihat Hasil Keseluruhan SVM"):
            st.dataframe(svm_results, use_container_width=True)

    if not bert_results.empty:
        st.markdown("<h5 style='font-size: 18px;'>Keseluruhan BERT</h5>", unsafe_allow_html=True)
        st.table(bert_results.head(5))
        with st.expander("Lihat Hasil Keseluruhan BERT"):
            st.dataframe(bert_results, use_container_width=True)

    # Pie Chart Section
st.markdown("<h5 style='font-size: 23px;'>Analisis Berdasarkan Kategori</h5>", unsafe_allow_html=True)

# Model SVM
if not svm_results.empty and 'Predicted' in svm_results.columns:
    st.markdown("<h5 style='font-size: 20px;'>Model SVM</h5>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<h5 style='font-size: 16px;'>Pilih Kategori untuk Melihat Tweet</h5>", unsafe_allow_html=True)
        svm_pie_data = svm_results['Predicted'].value_counts().reset_index()
        svm_pie_data.columns = ['Kategori', 'Jumlah']
        svm_selected_category = st.selectbox("Kategori", svm_pie_data['Kategori'], key="svm_category")

        pie_chart = alt.Chart(svm_pie_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Jumlah", type="quantitative"),
            color=alt.Color(field="Kategori", type="nominal", scale=alt.Scale(scheme="tableau10")),
            tooltip=['Kategori', 'Jumlah']
        ).properties(width=300, height=300)

        st.altair_chart(pie_chart, use_container_width=False)

    with col2:
        filtered = svm_results[svm_results['Predicted'] == svm_selected_category]
        if 'Tweet' in filtered.columns:
            st.markdown("<h5 style='font-size: 16px;'>Keputusan Analisis</h5>", unsafe_allow_html=True)
            st.dataframe(filtered[['Tweet', 'Actual', 'Predicted']].head(10), use_container_width=True)
            with st.expander("Lihat Keseluruhan"):
                st.dataframe(filtered, use_container_width=True)

# Model BERT
if not bert_results.empty and 'Predicted' in bert_results.columns:
    st.markdown("<h5 style='font-size: 20px;'>Model BERT</h5>", unsafe_allow_html=True)
    col3, col4 = st.columns([1, 2])
    
    with col3:
        st.markdown("<h5 style='font-size: 16px;'>Pilih Kategori untuk Melihat Tweet</h5>", unsafe_allow_html=True)
        bert_pie_data = bert_results['Predicted'].value_counts().reset_index()
        bert_pie_data.columns = ['Kategori', 'Jumlah']
        bert_selected_category = st.selectbox("Kategori", bert_pie_data['Kategori'], key="bert_category")

        bert_pie_chart = alt.Chart(bert_pie_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Jumlah", type="quantitative"),
            color=alt.Color(field="Kategori", type="nominal", scale=alt.Scale(scheme="tableau10")),
            tooltip=['Kategori', 'Jumlah']
        ).properties(width=300, height=300)

        st.altair_chart(bert_pie_chart, use_container_width=False)

    with col4:
        filtered_bert = bert_results[bert_results['Predicted'] == bert_selected_category]
        if 'Tweet' in filtered_bert.columns:
            st.markdown("<h5 style='font-size: 16px;'>Keputusan Analisis</h5>", unsafe_allow_html=True)
            st.dataframe(filtered_bert[['Tweet', 'Actual', 'Predicted']].head(10), use_container_width=True)
            with st.expander("Lihat Keseluruhan"):
                st.dataframe(filtered_bert, use_container_width=True)
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

# Button with color
if st.button('📊 Papar Hasil Analisis Mengikut Fasa', use_container_width=True):
    st.switch_page('pages/Keputusan_Analisis_Mengikut_Fasa.py')

st.markdown("""---""")  

st.markdown(
    "<div style='text-align: center; color: grey; font-size: 14px;'>"
    "© 2025 Rifhan Ilyani — Final Year Project | Universiti Kebangsaan Malaysia"
    "</div>",
    unsafe_allow_html=True
)


