import numpy as np
import random

class KarincaKolonisiOptimizasyonu:
    def __init__(self, mesafeler, karinca_sayisi, en_iyi_n, iterasyon_sayisi, buharlasma, alpha=1, beta=1):
        self.mesafeler = mesafeler
        # Başlangıçta tüm yollara eşit feromon
        self.feromon = np.ones(self.mesafeler.shape) / len(mesafeler)
        self.tum_indeksler = range(len(mesafeler))
        self.karinca_sayisi = karinca_sayisi
        self.en_iyi_n = en_iyi_n
        self.iterasyon_sayisi = iterasyon_sayisi
        self.buharlasma = buharlasma
        self.alpha = alpha  # Feromon önemi
        self.beta = beta    # Mesafe önemi

    def calistir(self):
        en_kisa_yol = None
        tum_zamanlarin_en_kisa_mesafesi = float('inf')
        gecmis = []

        for i in range(self.iterasyon_sayisi):
            tum_yollar = self.tum_yollari_olustur()
            self.feromon_dagit(tum_yollar, self.en_iyi_n, en_kisa_yol=en_kisa_yol)
            
            # Mevcut iterasyondaki en iyi yolu bul
            iterasyondaki_en_kisa = min(tum_yollar, key=lambda x: x[1])
            
            if iterasyondaki_en_kisa[1] < tum_zamanlarin_en_kisa_mesafesi:
                tum_zamanlarin_en_kisa_mesafesi = iterasyondaki_en_kisa[1]
                en_kisa_yol = iterasyondaki_en_kisa[0]
            
            # Feromon buharlaşması
            self.feromon = self.feromon * self.buharlasma
            gecmis.append(tum_zamanlarin_en_kisa_mesafesi)
            
        return en_kisa_yol, tum_zamanlarin_en_kisa_mesafesi, gecmis

    def tum_yollari_olustur(self):
        tum_yollar = []
        for i in range(self.karinca_sayisi):
            yol = self.yol_olustur(0) # 0 her zaman başlangıç noktası
            tum_yollar.append((yol, self.yol_mesafesini_hesapla(yol)))
        return tum_yollar

    def yol_olustur(self, baslangic):
        yol = [baslangic]
        ziyaret_edilenler = set(yol)
        onceki = baslangic
        
        for i in range(len(self.mesafeler) - 1):
            hareket = self.hareket_sec(self.feromon[onceki], self.mesafeler[onceki], ziyaret_edilenler)
            yol.append(hareket)
            onceki = hareket
            ziyaret_edilenler.add(hareket)
        
        yol.append(baslangic) # Başlangıca dönüş
        return yol

    def hareket_sec(self, feromon, mesafe, ziyaret_edilenler):
        feromon = np.copy(feromon)
        feromon[list(ziyaret_edilenler)] = 0 # Gidilen yerlerin feromonunu sıfırla

        # Olasılık hesaplama (ACO Formülü)
        satir = feromon ** self.alpha * (( 1.0 / (mesafe + 0.0001)) ** self.beta)
        norm_satir = satir / satir.sum()
        
        hareket = np.random.choice(self.tum_indeksler, 1, p=norm_satir)[0]
        return hareket

    def yol_mesafesini_hesapla(self, yol):
        toplam_mesafe = 0
        for i in range(len(yol) - 1):
            toplam_mesafe += self.mesafeler[yol[i]][yol[i+1]]
        return toplam_mesafe

    def feromon_dagit(self, tum_yollar, en_iyi_n, en_kisa_yol):
        sirali_yollar = sorted(tum_yollar, key=lambda x: x[1])
        
        # Sadece en iyi N karınca feromon bırakır
        for yol, mesafe in sirali_yollar[:en_iyi_n]:
            for i in range(len(yol) - 1):
                self.feromon[yol[i]][yol[i+1]] += 1.0 / self.mesafeler[yol[i]][yol[i+1]]
