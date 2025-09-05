# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# --- HTML/CSS KODLARI: ANA EKRANA EKLEME ÖZELLİĞİ İÇİN ---
# Bu bölüm, uygulamanın bir PWA gibi davranmasını sağlayan etiketleri HTML'e ekler.
manifest_url = "https://raw.githubusercontent.com/tunacvk00-boop/diyet-uygulama-ikon/refs/heads/main/manifest.json"
icon_url = "blob:https://github.com/8af79aaa-8be8-48cc-9c99-4b13b8f03c44"

pwa_html_tags = f'''
    <meta name="theme-color" content="#2d3748">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="Diyet App">
    <link rel="manifest" href="{manifest_url}">
    <link rel="apple-touch-icon" href="{icon_url}">
'''
st.markdown(pwa_html_tags, unsafe_allow_html=True)
# --- HTML BÖLÜMÜ SONU ---


# --- UYGULAMA KODU ---
DEGISIM_VERILERI = {
    'Süt':   {'cho': 9, 'pro': 6, 'yag': 6, 'kkal': 114},
    'Et':    {'cho': 0, 'pro': 6, 'yag': 5, 'kkal': 69},
    'Ekmek': {'cho': 15, 'pro': 2, 'yag': 0, 'kkal': 68},
    'Sebze': {'cho': 6, 'pro': 2, 'yag': 0, 'kkal': 32},
    'Meyve': {'cho': 15, 'pro': 0, 'yag': 0, 'kkal': 60},
    'Yağ':   {'cho': 0, 'pro': 0, 'yag': 5, 'kkal': 45}
}

st.set_page_config(layout="wide", page_title="Diyet Değişim Hesaplayıcı")
st.title('Diyetisyenler için Değişim Kombinasyon Hesaplayıcı')
st.write("Belirlediğiniz hedeflere uyan tüm olası diyet değişim kombinasyonlarını bulun.")

# Yan menüyü oluştur
st.sidebar.header('Arama Kriterlerini Girin')

hedef_kalori = st.sidebar.number_input('Hedef Kalori (kkal)', min_value=0, value=1800, step=50)
tolerans = st.sidebar.number_input('Tolerans (+/- kkal)', min_value=0, value=50, step=10)

st.sidebar.subheader('Makro Yüzde Sınırları (%)')
col1, col2 = st.sidebar.columns(2)
cho_min = col1.number_input('CHO Min %', min_value=0, max_value=100, value=45)
cho_max = col2.number_input('CHO Max %', min_value=0, max_value=100, value=55)

pro_min = col1.number_input('PRO Min %', min_value=0, max_value=100, value=20)
pro_max = col2.number_input('PRO Max %', min_value=0, max_value=100, value=25)

yag_min = col1.number_input('YAĞ Min %', min_value=0, max_value=100, value=25)
yag_max = col2.number_input('YAĞ Max %', min_value=0, max_value=100, value=30)

st.sidebar.subheader('Değişim Sınırları (adet)')
degisim_sinirlari = {}
for grup in DEGISIM_VERILERI.keys():
    col1, col2 = st.sidebar.columns(2)
    min_val = col1.number_input(f'{grup} Min', min_value=0, value=2, key=f'{grup}_min', step=1)
    max_val = col2.number_input(f'{grup} Max', min_value=0, value=6, key=f'{grup}_max', step=1)
    degisim_sinirlari[grup] = {'min': min_val, 'max': max_val}

if st.sidebar.button('Hesapla', type="primary", use_container_width=True):
    with st.spinner('Milyonlarca kombinasyon taranıyor, lütfen bekleyin...'):
        hedef_kkal_min = hedef_kalori - tolerans
        hedef_kkal_max = hedef_kalori + tolerans

        hedef_cho_min_g = (hedef_kalori * (cho_min / 100.0)) / 4
        hedef_cho_max_g = (hedef_kalori * (cho_max / 100.0)) / 4
        hedef_pro_min_g = (hedef_kalori * (pro_min / 100.0)) / 4
        hedef_pro_max_g = (hedef_kalori * (pro_max / 100.0)) / 4
        hedef_yag_min_g = (hedef_kalori * (yag_min / 100.0)) / 9
        hedef_yag_max_g = (hedef_kalori * (yag_max / 100.0)) / 9

        bulunan_sonuclar = []

        for sut in range(degisim_sinirlari['Süt']['min'], degisim_sinirlari['Süt']['max'] + 1):
            for et in range(degisim_sinirlari['Et']['min'], degisim_sinirlari['Et']['max'] + 1):
                for ekmek in range(degisim_sinirlari['Ekmek']['min'], degisim_sinirlari['Ekmek']['max'] + 1):
                    for sebze in range(degisim_sinirlari['Sebze']['min'], degisim_sinirlari['Sebze']['max'] + 1):
                        for meyve in range(degisim_sinirlari['Meyve']['min'], degisim_sinirlari['Meyve']['max'] + 1):
                            for yag in range(degisim_sinirlari['Yağ']['min'], degisim_sinirlari['Yağ']['max'] + 1):
                                
                                toplam_kkal = (sut*DEGISIM_VERILERI['Süt']['kkal'] + et*DEGISIM_VERILERI['Et']['kkal'] + ekmek*DEGISIM_VERILERI['Ekmek']['kkal'] + sebze*DEGISIM_VERILERI['Sebze']['kkal'] + meyve*DEGISIM_VERILERI['Meyve']['kkal'] + yag*DEGISIM_VERILERI['Yağ']['kkal'])
                                if (hedef_kkal_min <= toplam_kkal <= hedef_kkal_max):
                                    toplam_cho_g = (sut*DEGISIM_VERILERI['Süt']['cho'] + ekmek*DEGISIM_VERILERI['Ekmek']['cho'] + sebze*DEGISIM_VERILERI['Sebze']['cho'] + meyve*DEGISIM_VERILERI['Meyve']['cho'])
                                    toplam_pro_g = (sut*DEGISIM_VERILERI['Süt']['pro'] + et*DEGISIM_VERILERI['Et']['pro'] + ekmek*DEGISIM_VERILERI['Ekmek']['pro'] + sebze*DEGISIM_VERILERI['Sebze']['pro'])
                                    toplam_yag_g = (sut*DEGISIM_VERILERI['Süt']['yag'] + et*DEGISIM_VERILERI['Et']['yag'] + yag*DEGISIM_VERILERI['Yağ']['yag'])

                                    if (hedef_cho_min_g <= toplam_cho_g <= hedef_cho_max_g and
                                        hedef_pro_min_g <= toplam_pro_g <= hedef_pro_max_g and
                                        hedef_yag_min_g <= toplam_yag_g <= hedef_yag_max_g):
                                        
                                        cho_yuzde = (toplam_cho_g * 4 / toplam_kkal) * 100
                                        pro_yuzde = (toplam_pro_g * 4 / toplam_kkal) * 100
                                        yag_yuzde = (toplam_yag_g * 9 / toplam_kkal) * 100
                                        
                                        sonuc = {
                                            "Kalori (kkal)": int(toplam_kkal),
                                            "CHO (%)": f"{cho_yuzde:.1f}",
                                            "PRO (%)": f"{pro_yuzde:.1f}",
                                            "YAĞ (%)": f"{yag_yuzde:.1f}",
                                            "Süt": sut, "Et": et, "Ekmek": ekmek, 
                                            "Sebze": sebze, "Meyve": meyve, "Yağ": yag,
                                            "CHO (g)": f"{toplam_cho_g:.1f}",
                                            "PRO (g)": f"{toplam_pro_g:.1f}",
                                            "YAĞ (g)": f"{toplam_yag_g:.1f}"
                                        }
                                        bulunan_sonuclar.append(sonuc)
        
        st.success(f"Hesaplama Tamamlandı! Kriterlerinize uyan {len(bulunan_sonuclar)} adet kombinasyon bulundu.")

        if bulunan_sonuclar:
            df = pd.DataFrame(bulunan_sonuclar)
            sutun_sirasi = ["Kalori (kkal)", "CHO (%)", "PRO (%)", "YAĞ (%)", "Süt", "Et", "Ekmek", "Sebze", "Meyve", "Yağ", "CHO (g)", "PRO (g)", "YAĞ (g)"]
            st.dataframe(df[sutun_sirasi], use_container_width=True)
        else:

            st.warning("Bu kriterlere uygun hiçbir kombinasyon bulunamadı. Lütfen arama kriterlerinizi (özellikle değişim sınırlarını) genişletip tekrar deneyin.")
