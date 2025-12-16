import folium
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def rotayi_haritada_ciz(koordinatlar, yol_indeksleri, adres_isimleri):
    baslangic_koordinati = koordinatlar[yol_indeksleri[0]]
    harita = folium.Map(location=baslangic_koordinati, zoom_start=10)

    rota_koordinatlari = [koordinatlar[i] for i in yol_indeksleri]
    
    # Çizgi çizimi
    folium.PolyLine(
        rota_koordinatlari,
        color="blue",
        weight=4,
        opacity=0.7
    ).add_to(harita)

    # İşaretçiler
    for sira, indeks in enumerate(yol_indeksleri[:-1]):
        koordinat = koordinatlar[indeks]
        isim = adres_isimleri[indeks].split(",")[0]

        ikon_rengi = "red" if sira == 0 else "blue"
        ikon_tipi = "home" if sira == 0 else "info-sign"

        folium.Marker(
            location=koordinat,
            popup=f"{sira + 1}. {isim}",
            tooltip=f"{sira + 1}. {isim}",
            icon=folium.Icon(color=ikon_rengi, icon=ikon_tipi)
        ).add_to(harita)

    return harita

def yakinsama_grafigi_ciz(gecmis):
    fig, ax = plt.subplots()
    ax.plot(gecmis, color='green')
    ax.set_title("Optimizasyon Süreci (Yakınsama)")
    ax.set_xlabel("İterasyon")
    ax.set_ylabel("Toplam Mesafe (km)")
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig
