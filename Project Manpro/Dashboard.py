import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from datetime import date
from sklearn.neighbors import KNeighborsClassifier # pip install scikit-learn
from sklearn.model_selection import GridSearchCV
from streamlit_option_menu import option_menu #pip install streamlit-option-menu


st.set_page_config(page_title="Dashboard UMKM", page_icon=":bar_chart:", layout="wide")

# ==== TAKE EXCEL DATA ====
def get_data_from_excel():
    df = pd.read_excel(
        io="Data_After_Prepro_rev.xlsx",
        engine="openpyxl",
    )
    return df
umkm_df = get_data_from_excel()

# ==== MAINPAGE ====
st.title(":bar_chart: Dashboard UMKM")
st.write("Pada Bagian ini anda dapat melihat grafik berdasarkan data dalam database UMKM")

#Inisiasi row pertama
left_column, middle_column, right_column = st.columns(3)

# -- total perusahaan -- (gomel)
total_perusahaan = int(umkm_df["Nama_Perusahaan"].count())
with left_column:
    st.subheader("Total Perusahaan :")
    st.subheader(f"{total_perusahaan} UMKM")

# -- total sektor -- (jason)
df_sektor = umkm_df.groupby(['Sektor']).count()
total_sektor = int(df_sektor["Nama_Perusahaan"].count())
with middle_column:
    st.subheader("Total Sektor :")
    st.subheader(f"{total_sektor} sektor")

# -- total provinsi -- (cijo)
df_provinsi = umkm_df.groupby(['Provinsi']).count()
total_provinsi = int(df_provinsi["Nama_Perusahaan"].count())    
with right_column:
    st.subheader("Total Provinsi :")
    st.subheader(f"{total_provinsi} provinsi")


left_column, middle_column, right_column = st.columns(3)
# -- Bar Chart jml umk per provinsi -- (cijo)
kenaikan_perusahaan = umkm_df.groupby(['Tahun_Mulai']).count().cumsum()
fig_kenaikan = px.bar(
    kenaikan_perusahaan["Nama_Perusahaan"],
    x="Nama_Perusahaan",
    y=kenaikan_perusahaan.index,
    orientation="h",
    title="<b>Jumlah UMKM per tahun</b>",
)
left_column.plotly_chart(fig_kenaikan, use_container_width=True)

#-- Pie Chart jml umkm per provinsi-- (cijo)
jml_perusahaan_provinsi = umkm_df.groupby(['Provinsi']).count()
fig_perusahaan_provinsi = px.pie(
    jml_perusahaan_provinsi,
    values="Nama_Perusahaan",
    names=jml_perusahaan_provinsi.index,
    title="<b>Jumlah UMKM per Provinsi</b>",
    template="plotly_white",
)

left_column.plotly_chart(fig_perusahaan_provinsi, use_container_width=True)

# #-- Line Chart jml umkm per provinsi-- (cijo)
# jml_perusahaan_provinsi = umkm_df.groupby(['Provinsi']).count()
# fig_perusahaan_provinsi = px.line(
#     jml_perusahaan_provinsi,
#     x=jml_perusahaan_provinsi.index,
#     y="Nama_Perusahaan",
#     title="<b>Jumlah UMKM per Provinsi</b>",
#     template="plotly_white",
# )

# left_column.plotly_chart(fig_perusahaan_provinsi, use_container_width=True)

# -- Bar Chart jml umkm per sektor -- (jason)
jml_perusahaan_sektor = umkm_df.groupby(['Sektor']).count().sort_values(by=["Nama_Perusahaan"])
fig_perusahaan_sektor = px.bar(
    jml_perusahaan_sektor,
    x="Nama_Perusahaan",
    y=jml_perusahaan_sektor.index,
    orientation="h",
    title="<b>Jumlah UMKM per Sektor</b>",
    template="plotly_white",
)
middle_column.plotly_chart(fig_perusahaan_sektor, use_container_width=True)

# -- Line Chart jml umkm sesuai kemampuan produksi -- (jason)
jml_perusahaan_sektor = umkm_df.groupby(['Kemampuan_Produksi']).count().sort_values(by=["Nama_Perusahaan"])
fig_perusahaan_sektor = px.line(
    jml_perusahaan_sektor,
    x=jml_perusahaan_sektor.index,
    y="Nama_Perusahaan",
    title="<b>Jumlah UMKM sesuai kemampuan produksi</b>",
    template="plotly_white",
)
middle_column.plotly_chart(fig_perusahaan_sektor, use_container_width=True)

# -- Area Chart jml umkm melalui pembiayaan bank -- (jason)
jml_perusahaan_sektor = umkm_df.groupby(['Pembiayaan_Bank']).count().sort_values(by=["Nama_Perusahaan"])
fig_perusahaan_sektor = px.area(
    jml_perusahaan_sektor,
    x=jml_perusahaan_sektor.index,
    y="Nama_Perusahaan",
    title="<b>Jumlah UMKM melaului pembiayaan bank</b>",
    template="plotly_white",
)
middle_column.plotly_chart(fig_perusahaan_sektor, use_container_width=True)

# -- Line Chart kenaikan umkm per tahun -- (gomel)
kenaikan_perusahaan = umkm_df.groupby(['Tahun_Mulai']).count().cumsum()
fig_kenaikan = px.line(
    kenaikan_perusahaan["Nama_Perusahaan"],
    x=kenaikan_perusahaan.index,
    y="Nama_Perusahaan",
    orientation="h",
    title="<b>Jumlah UMKM per tahun</b>",
)
right_column.plotly_chart(fig_kenaikan, use_container_width=True)

# -- Pie Chart jml umkm per tahun mulai -- (jason)
jml_perusahaan_sektor = umkm_df.groupby(['Sektor']).count().sort_values(by=["Nama_Perusahaan"])
fig_perusahaan_sektor = px.pie(
    jml_perusahaan_sektor,
    names=jml_perusahaan_sektor.index,
    values="Nama_Perusahaan",
    title="<b>Jumlah UMKM per sektor</b>",
    template="plotly_white",
)
right_column.plotly_chart(fig_perusahaan_sektor, use_container_width=True)

#Perbandingan jumlah UMKM dari 1995 - 2010 dengan 2011 - 2020 (Jason) (diperbaiki)
# Menentukan range tahun
# # umkm_df['Tahun_Mulai'] = pd.to_datetime(umkm_df['Tahun_Mulai'])
# # umkm_df['Tahun_Range'] = pd.cut(umkm_df['Tahun_Mulai'].dt.year, bins=[1995, 2010, 2020], labels=['1995-2010', '2011-2020'])
# # # # Menghitung jumlah perusahaan berdasarkan range tahun
# # jml_perusahaan_tahun = umkm_df.groupby('Tahun_Range').sum('Jumlah_Perusahaan').size().reset_index(name='Jumlah_Perusahaan')
# # # # Membuat bar chart
# # fig_perusahaan_tahun = px.bar(
# #      jml_perusahaan_tahun,
# #      x='Jumlah_Perusahaan',
# #      y='Tahun_Range',
# #      title='<b>Perbandingan Jumlah Perusahaan antara 1995 - 2010 dengan 2011 - 2020 </b>',
# #      template='plotly_white',
# #  )
# # Menampilkan bar chart
# right_column.plotly_chart(fig_perusahaan_tahun, use_container_width=True)

st.markdown("##")
st.markdown("##")

# -- Bagian List Data --
st.title(":bar_chart: List Data")
st.write("List dari database UMKM")
umkm_df["Tahun_Mulai"] = umkm_df["Tahun_Mulai"].astype(str)
st.dataframe(umkm_df)


# -- Bagian Checkbox Tanggal --
default = date.today()
pilihan = st.sidebar.checkbox("Gunakan Tanggal Mulai Default", value=True)
if pilihan:
    today = default
    st.sidebar.write("Tanggal saat ini:", today)
else:
    today = st.sidebar.date_input("Masukkan Tanggal")
    st.sidebar.write("Tanggal saat ini:", today) 

# -- Bagian memilih data yang ingin dimasukkan --
options_form = st.sidebar.form("Options_form")
Nama_Perusahaan = options_form.text_input("Masukkan Nama Perusahaan")
Provinsi = options_form.selectbox("Pilih Provinsi :", 
                             umkm_df["Provinsi"].unique(), 
                             label_visibility="visible")
Jenis_Produk = options_form.text_input("Masukkan Jenis Produk")
Sektor = options_form.selectbox("Pilih Sektor :", 
                             umkm_df["Sektor"].unique(), 
                             label_visibility="visible")
Kemampuan_Produksi = options_form.number_input("Masukkan Jumlah Kemampuan Produksi :", 
                min_value=int(0), 
                max_value=int(10000), 
                value=int(0),
                label_visibility="visible")
Satuan_Barang = options_form.text_input("Masukkan Jenis Satuan Barang :")
Tahun_Mulai = options_form.selectbox("Masukkan Tahun Mulai", range(1950,(today.year+1)))
Pembiayaan_Bank = options_form.selectbox("Apakah ada pembiayaan bank :", 
                             umkm_df["Pembiayaan_Bank"].unique(), 
                             label_visibility="visible")
add_data = options_form.form_submit_button()

# -- Memasukkan data dalam excel --
if add_data:
    st.write(Nama_Perusahaan, Provinsi, Jenis_Produk, Sektor, Kemampuan_Produksi, Satuan_Barang, Tahun_Mulai, Pembiayaan_Bank)
    new_data = {"Nama_Perusahaan":Nama_Perusahaan, "Provinsi":Provinsi, "Jenis_Produk":Jenis_Produk, "Sektor":Sektor, "Kemampuan_Produksi":Kemampuan_Produksi,
                "Satuan_Barang": Satuan_Barang, "Tahun_Mulai":Tahun_Mulai, "Pembiayaan_Bank":Pembiayaan_Bank}
    umkm_df = umkm_df.append(new_data, ignore_index = True)
    st.header("New File")
    umkm_df.to_excel("Data_After_Prepro_rev.xlsx", index=False)