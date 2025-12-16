import googlemaps
import numpy as np
import streamlit as st
import time

class GoogleHaritalarYoneticisi:
    def __init__(self, api_anahtari):
        self.gmaps = googlemaps.Client(key=api_anahtari)

    def adreslerden_koordinat_getir(self, adres_listesi):
        koordinatlar = []
        gecerli_adresler = []

        # İlerleme çubuğu
        ilerleme_cubugu = st.progress(0)
        durum_metni = st.empty()

        for i, adres in enumerate(adres_listesi):
            durum_metni.text(
                f"Konum aranıyor ({i + 1}/{len(adres_listesi)}): {adres}"
            )

            try:
                geocode_sonucu = self.gmaps.geocode(adres)

                if geocode_sonucu:
                    konum = geocode_sonucu[0]['geometry']['location']
                    koordinatlar.append((konum['lat'], konum['lng']))
                    gecerli_adresler.append(adres)
                else:
                    st.error(f"Hata: Google '{adres}' adresini bulamadı.")
                    st.stop()

            except Exception as hata:
                st.error(f"API hatası ({adres}): {hata}")
                st.stop()

            ilerleme_cubugu.progress((i + 1) / len(adres_listesi))
            time.sleep(1.0) # API limitlerine takılmamak için bekleme

        durum_metni.empty()
        ilerleme_cubugu.empty()

        return koordinatlar, gecerli_adresler

    def mesafe_matrisi_olustur(self, koordinatlar):
        n = len(koordinatlar)
        matris = np.zeros((n, n))
        baslangiclar = [f"{enlem},{boylam}" for enlem, boylam in koordinatlar]

        ilerleme_cubugu = st.progress(0)
        durum_metni = st.empty()

        for i in range(n):
            durum_metni.text(f"Mesafe matrisi hesaplanıyor ({i + 1}/{n})")

            try:
                sonuc = self.gmaps.distance_matrix(
                    origins=[baslangiclar[i]],
                    destinations=baslangiclar,
                    mode="driving"
                )

                if sonuc['status'] == 'OK':
                    elemanlar = sonuc['rows'][0]['elements']
                    for j, eleman in enumerate(elemanlar):
                        if eleman['status'] == 'OK':
                            # Metreyi kilometreye çevir
                            matris[i][j] = (
                                eleman['distance']['value'] / 1000.0
                            )
                        else:
                            matris[i][j] = 9999.0 # Ulaşılamazsa yüksek değer
                else:
                    st.error(f"Distance Matrix API hatası: {sonuc['status']}")
                    st.stop()

            except Exception as hata:
                st.error(f"Mesafe hesaplama hatası: {hata}")
                st.stop()

            ilerleme_cubugu.progress((i + 1) / n)
            time.sleep(0.5)

        durum_metni.empty()
        ilerleme_cubugu.empty()

        return matris