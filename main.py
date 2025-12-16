import streamlit as st
import pandas as pd

from veri.adresler import tum_adresleri_getir
from core.api_yoneticisi import GoogleHaritalarYoneticisi
from core.karinca_algoritmasi import KarincaKolonisiOptimizasyonu
from gorsel.gorsellestirme import rotayi_haritada_ciz
from streamlit_folium import st_folium

st.set_page_config(page_title="Karınca Kolonisi Rota Optimizasyonu", layout="wide")

def ana_fonksiyon():
    st.title("Sağlık Ekibi Rota Optimizasyonu (Senaryo 0)")
    st.markdown("""
    Bu uygulama Google Maps API (Geocoding ve Distance Matrix) kullanarak
    en kısa rotayı **Karınca Kolonisi Algoritması** ile belirler.
    """)

    # Session State (Oturum Durumu) Değişkenleri - Türkçe
    if "analiz_tamamlandi" not in st.session_state:
        st.session_state.analiz_tamamlandi = False
    if "koordinatlar" not in st.session_state:
        st.session_state.koordinatlar = None
    if "gecerli_adresler" not in st.session_state:
        st.session_state.gecerli_adresler = None
    if "en_iyi_yol" not in st.session_state:
        st.session_state.en_iyi_yol = None
    if "en_iyi_mesafe" not in st.session_state:
        st.session_state.en_iyi_mesafe = None
    if "gecmis" not in st.session_state:
        st.session_state.gecmis = None

    st.sidebar.header("Ayarlar")

    api_anahtari = st.secrets.get("GOOGLE_API_KEY")
    if not api_anahtari:
        api_anahtari = st.sidebar.text_input("Google Maps API Anahtarı:", type="password")

    st.sidebar.subheader("Algoritma Parametreleri")
    karinca_sayisi = st.sidebar.slider("Karınca Sayısı", 10, 100, 30)
    iterasyon_sayisi = st.sidebar.slider("İterasyon Sayısı", 10, 200, 50)
    alpha = st.sidebar.slider("Alpha (Feromon Etkisi)", 0.1, 5.0, 1.0)
    beta = st.sidebar.slider("Beta (Mesafe Etkisi)", 0.1, 5.0, 2.0)
    buharlasma = st.sidebar.slider("Buharlaşma Oranı", 0.1, 0.9, 0.5)

    adresler = tum_adresleri_getir()
    st.subheader(f"Ziyaret Edilecek {len(adresler)} Nokta")

    with st.expander("Adres Listesini Görüntüle"):
        st.write(adresler)

    if st.button("Analizi Başlat"):
        if not api_anahtari:
            st.error("Lütfen Google Maps API anahtarını giriniz.")
            st.stop()

        yonetici = GoogleHaritalarYoneticisi(api_anahtari)

        with st.spinner("Adresler koordinatlara dönüştürülüyor..."):
            koordinatlar, gecerli_adresler = yonetici.adreslerden_koordinat_getir(adresler)
            st.session_state.koordinatlar = koordinatlar
            st.session_state.gecerli_adresler = gecerli_adresler

        with st.spinner("Mesafe matrisi hesaplanıyor..."):
            mesafe_matrisi = yonetici.mesafe_matrisi_olustur(koordinatlar)

        with st.spinner("En kısa rota hesaplanıyor (Karınca Kolonisi)..."):
            optimizator = KarincaKolonisiOptimizasyonu(
                mesafeler=mesafe_matrisi,
                karinca_sayisi=karinca_sayisi,
                en_iyi_n=karinca_sayisi // 2,
                iterasyon_sayisi=iterasyon_sayisi,
                buharlasma=buharlasma,
                alpha=alpha,
                beta=beta
            )
            en_iyi_yol, en_iyi_mesafe, gecmis = optimizator.calistir()

            st.session_state.en_iyi_yol = en_iyi_yol
            st.session_state.en_iyi_mesafe = en_iyi_mesafe
            st.session_state.gecmis = gecmis
            st.session_state.analiz_tamamlandi = True

    if st.session_state.analiz_tamamlandi:
        st.success(
            f"Optimizasyon tamamlandı. Toplam mesafe: "
            f"{st.session_state.en_iyi_mesafe:.2f} km"
        )

        sutun1, sutun2 = st.columns([2, 1])

        with sutun1:
            st.markdown("### Optimize Edilmiş Rota")
            harita_objesi = rotayi_haritada_ciz(
                st.session_state.koordinatlar,
                st.session_state.en_iyi_yol,
                st.session_state.gecerli_adresler
            )
            st_folium(harita_objesi, width=800, height=500)

        with sutun2:
            st.markdown("### Yakınsama Grafiği")
            grafik_verisi = pd.DataFrame(
                st.session_state.gecmis,
                columns=["Mesafe (km)"]
            )
            st.line_chart(grafik_verisi)

            st.markdown("### Ziyaret Sırası")
            yol_indeksleri = st.session_state.en_iyi_yol
            adres_listesi = st.session_state.gecerli_adresler

            for i, indeks in enumerate(yol_indeksleri):
                isim = adres_listesi[indeks].split(",")[0]
                if i == 0:
                    st.write(f"🏁 **Başlangıç:** {isim}")
                elif i == len(yol_indeksleri) - 1:
                    st.write(f"🏠 **Dönüş:** {isim}")
                else:
                    st.write(f"{i}. {isim}")

if __name__ == "__main__":
    ana_fonksiyon()