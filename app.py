
"""
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference
"""

import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

############## data ################3
dk = pd.read_csv("data/produksi_minyak_mentah_lengkap.csv")
df_tabel = pd.read_csv("data/produksi_minyak_mentah_lengkap.csv")
kode = pd.read_csv("data/kode_negara_lengkap.csv")

############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called

image = Image.open('img/destia.jpeg')
st.image(image, width = 250)

st.title("Statistik Jumlah Produksi Minyak Mentah")
st.markdown("*Sumber data berasal dari [Produksi Minyak Mentah](https://drive.google.com/file/d/1ON5nCzIZ2BLfaxNJOv0HjQy8nj4c2a9k/view?usp=sharing)*")

st.sidebar.title("Pengaturan")

############## User input ###########
select_negara = st.sidebar.selectbox(
     'Pilih Negara',
     (df['name'].unique()), 
     index=0)

st.sidebar.write("Produksi minyak ", 
    select_negara, 
    "berdasarkan tahun di tampilkan pada Grafik A")

select_tahun = st.sidebar.selectbox(
     'Pilih Tahun',
     (df['tahun'].unique()), 
     index=0)

st.sidebar.write("Negara dengan produksi minyak terbesar pada tahun ", 
    str(select_tahun), 
    "ditampilkan pada Grafik B")

n_tampil = st.sidebar.number_input("Jumlah negara yang ingin ditampilkan pada Grafik B dan C", 
    min_value=1, max_value=10, value=5)

## Grafik A
st.subheader('Jumlah produksi minyak mentah suatu negara pertahun')
data_select = df.loc[(df["name"] == select_negara)]
get_kode_negara = data_select['kode_negara'].iloc[0]

data_grafik_a = df.loc[(df["kode_negara"] == get_kode_negara)]

judul = 'Produksi Minyak ' + select_negara + ' (A)'

fig = px.line(data_grafik_a, x="tahun", y="produksi", title= judul)

st.plotly_chart(fig, use_container_width=True)

### grafik B
st.subheader('Jumlah produksi minyak mentah terbesar')
data_grafik_b = df.loc[(df["tahun"] == select_tahun)].sort_values(by='produksi', ascending=False)
data_grafik_b = data_grafik_b.iloc[:n_tampil]


title_b= str(n_tampil) + ' negara dengan produksi minyak terbesar pada tahun ' + str(select_tahun) + ' (B)'

fig_b = px.bar(data_grafik_b, x='name', y='produksi', title = title_b,
    color = 'name')
fig_b.update_layout(showlegend=False) 
st.plotly_chart(fig_b, use_container_width=True)


### grafik C
st.subheader('Jumlah produksi kumulatif minyak mentah terbesar')

data_agregat = df.groupby('kode_negara').sum().sort_values(by='produksi', ascending=False).reset_index()

data_agregat = data_agregat.iloc[:n_tampil]

#join data
data_agregat_fix = pd.merge(data_agregat, kode[['name','alpha-3']], left_on=['kode_negara'], right_on=['alpha-3'], how='left')

title_c= str(n_tampil) + ' negara dengan produksi minyak kumulatif terbesar' + ' (C)'

fig_c = px.bar(data_agregat_fix, x='name', y='produksi', 
    color='name', title = title_c)
fig_c.update_layout(showlegend=False) 
st.plotly_chart(fig_c, use_container_width=True)


### tabel data
st.subheader('Tabel Representasi Data')

st.dataframe(df_tabel)

####
st.subheader('SUMMARY')

#data
data_agregat_c = df.groupby('kode_negara').sum().sort_values(by='produksi', ascending=False).reset_index()

data_agregat_fix_c = pd.merge(data_agregat_c, kode[['name','alpha-3','region','sub-region']], 
                              left_on=['kode_negara'], right_on=['alpha-3'], how='left')

#data untuk negara max
data_max = data_agregat_fix_c.loc[data_agregat_fix_c['produksi'] >= data_agregat_fix_c['produksi'].max(),
                      ['kode_negara', 'name', 'produksi', 'region', 'sub-region']],

text_max = ('Produksi Minyak Terbesar  \n' + 
            '  \nNama negara: ' + data_max['name'].values[0] +
            '  \nKode Negara: ' + data_max['kode_negara'].values[0] + 
            '  \nRegion: ' + data_max['region'].values[0] +
            '  \nSub-Region: ' + data_max['sub-region'].values[0] +
            '  \nTotal Produksi: ' + str(round(data_max['produksi'].values[0], 2)))

#data untuk negara min tidak sama dengan 0
data_minimum_nol = data_agregat_fix_c[data_agregat_fix_c['produksi'] > 0]
data_min = data_minimum_nol.loc[data_minimum_nol['produksi'] == data_minimum_nol['produksi'].min(),
                      [ 'kode_negara', 'name', 'produksi', 'region', 'sub-region']]

text_min = ('Produksi Minyak Terkecil  \n' + 
            '  \nNama negara: ' + data_min['name'].values[0] +
            '  \nKode Negara: ' + data_min['kode_negara'].values[0] + 
            '  \nRegion: ' + data_min['region'].values[0] +
            '  \nSub-Region: ' + data_min['sub-region'].values[0] +
            '  \nTotal Produksi: ' + str(round(data_min['produksi'].values[0], 2)) +
            '  \n')

#data produksi 0
data_nol = data_agregat_fix_c.iloc[136,]
text_nol = ('Produksi Minyak 0  \n' + 
     '  \nNama negara: ' + data_nol[4] +
     '  \nKode Negara: ' + data_nol[0] +
     '  \nRegion: ' + data_nol[6] +
     '  \nSub-Region: ' + data_nol[7] +
     '  \nTotal Produksi:' + str(round(data_nol[3], 2)))

nol_etc = ('Negara lain dengan produksi minyak 0:  \n' +
    '  \n1. Belgium' +
    '  \n2. Finland' +
    '  \n3. Iceland' + 
    '  \n4. Ireland' +
    '  \n5. Bosnia')

data_table_nol = data_agregat_fix_c.loc[data_agregat_fix_c['produksi'] == 0,
    [ 'kode_negara', 'name', 'produksi', 'region', 'sub-region']].reset_index()

st.write('Summary Produksi minyak kumulatif')
m1, m2 = st.columns((1,1))

m1.info(text_max)

m2.info(text_min)

##### summary pilih tahun ########
st.write('Summary Produksi minyak per tahun')

tahun_summary = st.selectbox(
     'Masukkan Tahun',
     (df['tahun'].unique()), 
     index=0)

m3, m4 = st.columns((1,1))

#menyiapkan data filter
data_filter = pd.merge(df_tabel, kode[['name','alpha-3','region','sub-region']], 
                              left_on=['kode_negara'], right_on=['alpha-3'], how='left')

data_filter = data_filter.loc[df_tabel['produksi'] > 0,
    ['kode_negara', 'name_x', 'produksi', 'region_x', 'sub-region_x', 'tahun']]

data_filter_tahun = data_filter.loc[data_filter['tahun'] == tahun_summary,
    ['kode_negara', 'name_x', 'produksi', 'region_x', 'sub-region_x', 'tahun']]

#mengambil data min dan teks
data_min_filter = data_filter_tahun.loc[data_filter_tahun['produksi'] == data_filter_tahun['produksi'].min(),
    ['kode_negara', 'name_x', 'produksi', 'region_x', 'sub-region_x', 'tahun']]

text_min_filter = ('Produksi Minyak terkecil pada tahun ' + str(tahun_summary) + 
            '  \nNama negara: ' + data_min_filter['name_x'].values[0] +
            '  \nKode Negara: ' + data_min_filter['kode_negara'].values[0] + 
            '  \nRegion: ' + data_min_filter['region_x'].values[0] +
            '  \nSub-Region: ' + data_min_filter['sub-region_x'].values[0] +
            '  \nTotal Produksi: ' + str(round(data_min_filter['produksi'].values[0], 2)) +
            '  \n')

#mengambil data max dan teks
data_max_filter = data_filter_tahun.loc[data_filter_tahun['produksi'] == data_filter_tahun['produksi'].max(),
    ['kode_negara', 'name_x', 'produksi', 'region_x', 'sub-region_x', 'tahun']]

text_max_filter = ('Produksi Minyak terbesar pada tahun ' + str(tahun_summary) + 
            '  \nNama negara: ' + data_max_filter['name_x'].values[0] +
            '  \nKode Negara: ' + data_max_filter['kode_negara'].values[0] + 
            '  \nRegion: ' + data_max_filter['region_x'].values[0] +
            '  \nSub-Region: ' + data_max_filter['sub-region_x'].values[0] +
            '  \nTotal Produksi: ' + str(round(data_max_filter['produksi'].values[0], 2)) +
            '  \n')


m3.info(text_max_filter)
m4.info(text_min_filter)

### tabel 0
st.write('Tabel Negara dengan produksi minyak mentah 0')
st.dataframe(data_table_nol.iloc[:,1:6])
