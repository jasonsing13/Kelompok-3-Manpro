import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from datetime import date
from sklearn.neighbors import KNeighborsClassifier # pip install scikit-learn
from streamlit_option_menu import option_menu #pip install streamlit-option-menu


st.title("Penambahan Data")
df = pd.read_excel(
        io="Data_After_Prepro_rev.xlsx",
        engine="openpyxl",
    )
st.write(df)

default = date.today()
pilihan = st.checkbox("Gunakan Tanggal Mulai Default", value=True)
#pilihan = st.radio("Pilih opsi tanggal:",
#                   ("Gunakan Tanggal Saat Ini","Masukkan Tanggal Manual"))
if pilihan:
    today = default
    st.sidebar.write("Tanggal saat ini:", today)
else:
    today = st.date_input("Masukkan Tanggal")
    st.sidebar.write("Tanggal saat ini:", today)  

options_form = st.sidebar.form("Options_form")
Nama_Perusahaan = options_form.text_input("Masukkan Nama Perusahaan")
Provinsi = options_form.selectbox("Pilih Provinsi :", 
                             df["Provinsi"].unique(), 
                             label_visibility="visible")
Jenis_Produk = options_form.text_input("Masukkan Jenis Produk")
Sektor = options_form.selectbox("Pilih Sektor :", 
                             df["Sektor"].unique(), 
                             label_visibility="visible")
Kemampuan_Produksi = options_form.number_input("Masukkan Jumlah Kemampuan Produksi :", 
                min_value=int(0), 
                max_value=int(10000), 
                value=int(0),
                label_visibility="visible")
Satuan_Barang = options_form.text_input("Masukkan Jenis Satuan Barang")
Tahun_Mulai = options_form.selectbox("Masukkan Tahun Mulai", range(1950,(today.year+1)))
Pembiayaan_Bank = options_form.text_input("Apakah Ada Pembiayaan Bank?")
add_data = options_form.form_submit_button() 
if add_data:
    st.write(Nama_Perusahaan, Provinsi, Jenis_Produk, Sektor, Kemampuan_Produksi, Satuan_Barang, Tahun_Mulai, Pembiayaan_Bank)
    new_data = {"Nama_Perusahaan":Nama_Perusahaan, "Provinsi":Provinsi, "Jenis_Produk":Jenis_Produk, "Sektor":Sektor, "Kemampuan_Produksi":Kemampuan_Produksi,
                "Satuan_Barang": Satuan_Barang, "Tahun_Mulai":Tahun_Mulai, "Pembiayaan_Bank":Pembiayaan_Bank}
    df = df.append(new_data, ignore_index = True)
    st.header("New File")
    df.to_excel("Data_After_Prepro_rev.xlsx", index=False) 