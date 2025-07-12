import streamlit as st

# Title
st.set_page_config(page_title="Sistem Analisis Sentimen Buli", layout="wide")

# Buli in IPTA
st.markdown("<h4 style='font-size: 32px; text-align: center; color: white; background-color: #4B3C91; padding: 10px; border-radius: 10px;'>Sistem Analisis Sentimen Mengenai Isu Buli Di IPTA</h4>", unsafe_allow_html=True)
st.markdown('######')

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("")
    st.image('buli_ipta.jpg', caption='Sumber: Google Images', use_container_width=True)

with col2:
    st.markdown("<h4 style='color: #4B3C91;'>Buli Di Institusi Pengajian Tinggi Awam (IPTA)</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: justify;'>
    Isu buli di Institusi Pengajian Tinggi Awam (IPTA) sering berlaku pada masa ini dan kebanyakannya turut menjadi kes jenayah kerana melibatkan penderaan secara fizikal dan berakhir dengan kehilangan nyawa. Kejadian-kejadian ini bukan sahaja memberi kesan negatif kepada mangsa dari segi fizikal dan emosi, tetapi juga mencerminkan masalah yang lebih besar dalam ekosistem pendidikan dan sosial. Kes ini telah pun menarik perhatian negara tetapi juga menimbulkan persoalan mendalam tentang isu buli dan penderaan yang berlaku di institusi pendidikan. Ia juga mendorong kepada perbincangan tentang langkah-langkah yang perlu diambil untuk menangani jenayah buli dalam kalangan pelajar di negara ini, serta bagaimana sistem sosial dan pendidikan dapat memainkan peranan penting dalam mencegah kejadian serupa.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(" ")

    st.markdown("<h4 style='color: #4B3C91;'>Sistem Analisis Sentimen Mengenai Isu Buli di IPTA</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: justify;'>
    Sebagai respons terhadap kejadian-kejadian ini, sistem analisis sentimen ini dibangunkan untuk menganalisis pendapat dan reaksi awam terhadap isu buli yang kebanyakannya berlaku di IPTA, terutamanya dalam kalangan pengguna aplikasi X. 
    Sistem ini bertujuan untuk memahami perasaan umum mengenai kes ini, sama ada positif, negatif, atau neutral, dengan mengklasifikasikan tweet–tweet dan perbincangan dalam talian. 
    Melalui analisis sentimen ini, diharapkan kita dapat memahami pasti tahap kesedaran masyarakat mengenai isu buli serta langkah-langkah pencegahan yang dapat diambil untuk menanganinya. </div>
    """, unsafe_allow_html=True)
st.markdown("")

# Button display analysis
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

# Button
if st.button('📊 Papar Hasil Analisis Keseluruhan', use_container_width=True):
    st.switch_page('pages/Keputusan_Analisis_Keseluruhan.py')

st.markdown("""---""")  

st.markdown(
    "<div style='text-align: center; color: grey; font-size: 14px;'>"
    "© 2025 Rifhan Ilyani — Final Year Project | Universiti Kebangsaan Malaysia"
    "</div>",
    unsafe_allow_html=True
)
