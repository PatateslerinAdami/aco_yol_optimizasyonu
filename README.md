# aco_yol_optimizasyonu


pip install -r requirements.txt


.streamlit/secrets.toml içinde api key girmek gerekir. GOOGLE_API_KEY = ""


streamlit run main.py ile çalıştırılabilir


Karınca Sayısı: Her iterasyonda yola çıkan ajan sayısı. Artması çözüm kalitesini artırabilir ancak süreyi uzatır.


İterasyon Sayısı: Algoritmanın kaç döngü çalışacağı.

Alpha (Feromon Etkisi): Karıncaların daha önce gidilen (feromonlu) yolları tercih etme eğilimi.


Beta (Mesafe Etkisi): Karıncaların daha yakın noktaları tercih etme eğilimi (Heuristik bilgi).


Buharlaşma Oranı: Her tur sonunda yollardaki feromonun ne kadarının uçacağını belirler. (Yerel minimumdan kaçmak için önemlidir).
