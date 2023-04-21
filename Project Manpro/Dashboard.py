import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from sklearn.neighbors import KNeighborsClassifier # pip install scikit-learn

st.set_page_config(page_title="Dashboard UMKM", page_icon=":bar_chart:", layout="centered")

# ==== CLASSIFICATION ====
def klasifikasi (dataframe, provinsi, sektor, produksi, tahun):
    #Memasukkan data dan menampilkan data
    initial_df = dataframe

    #mengambil data yang diperlukan
    new_df = initial_df[["Provinsi","Sektor","Kemampuan_Produksi","Tahun_Mulai", "Pembiayaan_Bank"]]

    #Mengubah string menjadi angka
    prov_uniq = {'Jawa Barat':1, 'DKI Jakarta':2}
    sek_uniq = {'Barang Kayu dan Hasil Hutan Lainnya':1,
    'Tekstil Barang Kulit dan Alas Kaki':2, 'Makanan dan Minuman':3,
    'Barang Lainnya':4, 'Alat Angkutan, Mesin dan Lainnya':5,
    'Semen dan Barang Galian':6, 'Pupuk, Kimia dan Barang dari Karet':7,
    'Logam Dasar Besi dan Baja':8}

    datmin_df = new_df.copy()
    datmin_df["Provinsi"] = datmin_df["Provinsi"].replace(prov_uniq)
    datmin_df["Sektor"] = datmin_df["Sektor"].replace(sek_uniq)

    #Memulai algoritma KNN
    Features = ["Provinsi","Sektor","Kemampuan_Produksi","Tahun_Mulai"]

    #Pelatihan data
    x = datmin_df[Features].copy()
    y = datmin_df['Pembiayaan_Bank']
    knn = KNeighborsClassifier(n_neighbors=4)
    knn.fit(x,y)

    for key, value in prov_uniq.items():
        provinsi = provinsi.replace(key, str(value))

    for key, value in sek_uniq.items():
        sektor = sektor.replace(key, str(value))

    #Mencoba buat DF baru
    data = {"Provinsi": provinsi,
        "Sektor": sektor, 
        "Kemampuan_Produksi":produksi,
        "Tahun_Mulai":tahun}
    
    predict_data = pd.DataFrame(data, index=[0])

    #Memprediksi Data
    predict_data["Prediction"] = knn.predict(predict_data)
    if predict_data["Prediction"].values == "Tidak Ada":
        return "Kemungkinan untuk mendapatkan pembiayaan bank adalah ' TIDAK ADA '"    
    elif predict_data["Prediction"].values == "Ada":
        return "Kemungkinan untuk mendapatkan pembiayaan bank adalah ' ADA '"

# ==== TAKE EXCEL DATA ====
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="Data_After_Prepro_rev.xlsx",
        engine="openpyxl",
    )
    return df
umkm_df = get_data_from_excel()

# ==== MAINPAGE ====
st.title(":bar_chart: Dashboard UMKM")
st.markdown("##")

# -- Bagian Klasifikasi --
st.title(":bar_chart: Prediksi Pembiayaan")

# -> memasukkan data yang diperlukan <-
provinsi_data = st.selectbox("Pilih Provinsi :", 
                             umkm_df["Provinsi"].unique(), 
                             label_visibility="visible")
sektor_data = st.selectbox("Pilih Sektor :", 
                             umkm_df["Sektor"].unique(), 
                             label_visibility="visible")
produksi_data = st.number_input("Masukkan Jumlah Kemampuan Produksi :", 
                min_value=int(0), 
                max_value=int(10000), 
                value=int(0),
                label_visibility="visible")
tahun_data = st.number_input("Masukkan Tahun Mulai :", 
                min_value=int(1980), 
                max_value=int(2023), 
                value=int(1980),
                label_visibility="visible")

hasil_prediksi = st.button("Mulai Prediksi")

# -> menampilkan data <-
if hasil_prediksi:
    prediksi = klasifikasi(umkm_df, provinsi_data,sektor_data,produksi_data,tahun_data)
    st.write(prediksi)

st.markdown("##")
st.markdown("##")

# -- Bagian List Data --
st.title(":bar_chart: List Data")
umkm_df["Tahun_Mulai"] = umkm_df["Tahun_Mulai"].astype(str)
st.dataframe(umkm_df)
