sek_uniq = {'Barang Kayu dan Hasil Hutan Lainnya':1,
    'Tekstil Barang Kulit dan Alas Kaki':2, 'Makanan dan Minuman':3,
    'Barang Lainnya':4, 'Alat Angkutan, Mesin dan Lainnya':5,
    'Semen dan Barang Galian':6, 'Pupuk, Kimia dan Barang dari Karet':7,
    'Logam Dasar Besi dan Baja':8}
provinsi = "Barang Lainnya"
for key, value in sek_uniq.items():
    provinsi = provinsi.replace(key,str(value))

print(provinsi)
