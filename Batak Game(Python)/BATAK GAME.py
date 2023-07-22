# -- BATAK OYUNU --

#   Aşağıdaki kurallara sahip bir kod yazılmıştır:
# + Önceden belirlenen sayıda tur adedi ile oynanması sağlanmalıdır.
# + Her oyuncunun tur başında kaç el alacağını tahmin etmelidir. Bu 3 farklı şekilde yapılabilir:
#   1) Her oyuncu için rastgele belirlenebilir (mantıklı değil)
#   2) Oyuncunun kartlarına göre bilgisayar karar vermeye çalışabilir (yapması zor)
#   3) Kullanıcı her oyuncu için bu değeri girebilir (yapması kolay)
# + Puanlama sistemi olmalı ve her tur sonunda güncel puan tablosu gösterilmelidir:
#   - Oyuncu tahmin ettiği eli alırsa "tahmin x 10" puan kazanır (3 tahmin edip tam 3 el almışsa 30 puan)
#   - Fazladan aldığı her el için 1 puan eklenir (3 tahmin edip 5 aldıysa: 32)
#   - Tahmininden az el alırsa "tahmin x 10" puan kaybeder (3 tahmin edip 2 aldıysa: -30)

n = int((input('kaç tur oynansın: ')))
for i in range (1, int(n+1)):

    import random

    A = ['♠', '♣', '♥', '♦']
    B = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    deste = []
    for i in A:
        for j in B:
            deste.append(i+j)

        random.shuffle(deste)

    oyuncular = {}
    oyuncu_sira = ['oyuncu1', 'oyuncu2', 'oyuncu3', 'oyuncu4']  # oyuncu isimleri girilecek ise boş liste olmalı
        # print("OYUNCULARIN İSİMLERİNİ GİRİN:") # oyuncu isimleri girilecek ise bu satır açılmalı
    for i in range(4):
            # oyuncular.setdefault(input("Oyuncu " + str(i+1) + ": "), {}.fromkeys(A))
            oyuncular.setdefault(oyuncu_sira[i], {}.fromkeys(A)) # isimler girilecek ise bu kapatılmalı, üstteki açılmalı

    for oyuncu in oyuncular:
            # oyuncu_sira.append(oyuncu)  # oyuncu isimleri girilecek ise bu satır açılmalı
            for i in A:
                oyuncular[oyuncu][i] = []
            for i in range(13):
                kart = random.choice(deste)
                oyuncular[oyuncu][kart[0]].append(kart[1:])
                deste.remove(kart)

    print("\nDAĞITILAN KARTLAR:")
    for oyuncu in oyuncular:
            print(oyuncu + ":")
            for karttip in oyuncular[oyuncu]:
                oyuncular[oyuncu][karttip].sort(key=B.index)  # kartlar B listesindeki sıraya göre dizilir
                print(karttip, oyuncular[oyuncu][karttip])
                
            



    print("\nOYUN BAŞLADI...")  # Oyun sadece 1 tur (13 el) oynanacak
    # her oyuncu için bir teklif belirleyelim
    
    tahminler = []
    for oyuncu in oyuncular:
        tahmin = input(f"{oyuncu}, tahmininizi girin: ")
        tahminler.append(tahmin + oyuncu)
        if len(tahminler) == len(oyuncular):
            break
  
    oyun_skor = dict()
    macaAtildi = False
    sira = random.randrange(4)  # oyuna başlayacak oyuncu rastgele belirleniyor
    for el in range(13):  # 13 el oynanacak
            print(str(el+1) + ". el:")
            oynayan = 0
            oynanan_kartlar = []  # bu liste içine kimin hangi kartı attığı yazılacak
            while oynayan < 4:
                oyuncu = oyuncu_sira[sira]
                if oynayan == 0:  # ilk kart atacak oyuncu ise kart tipi belirlenecek (rastgele)
                    while True:
                        if macaAtildi:  # Maça önceki bir elde koz olarak kullanıldı ise oyuncu Maça ile başlayabilir
                            kart_tipi = random.choice(A)
                        else:  # Maça önceki bir elde koz olarak kullanılmadı ise diğer üç kart tipinden atabilir
                            kart_tipi = random.choice(A[1:])
                        if len(oyuncular[oyuncu_sira[sira]][kart_tipi]):  # o tipte kartı yoksa döngü devam edecek
                            break
                    oyuncu_kart = (oyuncu, kart_tipi, oyuncular[oyuncu][kart_tipi].pop())  # o tipteki en büyük kartı atıyor
                    # NOT: Oyuncunun o tipteki en büyük kartı atması çoğu durumda mantıklı değil. Rastgele olarak seçilmesi veya
                    # en küçüğü atmak da mantıklı olmaz. Oyuncunun mantıklı bir kart atmasını sağlamak için birçok ilave kontrol
                    # eklenmesi gerekir (Daha önce 'A' çıktı ise 'K' ile başlamak mantıklı olabilir vb.). Bu programda o elin
                    # ilk kartı atılırken de, sonraki kartlar için de mantıklı olmasına yönelik kontroller bulunmamaktadır.
                else:  # diğer oyuncular ilk oyuncunun belirlediği kart tipinde kart atacak
                    if len(oyuncular[oyuncu][kart_tipi]):  # o kart tipinde kartı varsa en büyük olanı atacak
                        oyuncu_kart = (oyuncu, kart_tipi, oyuncular[oyuncu][kart_tipi].pop())
                    elif len(oyuncular[oyuncu]['♠']):  # o kart tipinde kartı yoksa en küçük maça kartını atacak
                        oyuncu_kart = (oyuncu, '♠', oyuncular[oyuncu]['♠'].pop(0))
                        macaAtildi = True  # Maça koz olarak oynandığı için sonraki ellerde doğrudan Maça atılabilecek
                    else:  # maça kartı da yoksa, diğer 2 tipin hangisinde daha çok kart varsa en küçük kartı atacak
                        kart_tipleri = A[1:].copy()  # maça hariç diğer 3 kart tipi kopyalandı
                        if kart_tipi != '♠':  # oynanan kart tipi maça değilse
                            kart_tipleri.remove(kart_tipi)  # oynanan kart tipi de oyuncuda olmadığı için silindi
                        if len(oyuncular[oyuncu][kart_tipleri[0]]) > len(oyuncular[oyuncu][kart_tipleri[1]]):
                            oyuncu_kart = (oyuncu, kart_tipleri[0], oyuncular[oyuncu][kart_tipleri[0]].pop())       
                        else:
                            if oyuncular[oyuncu][kart_tipleri[1]]:
                                oyuncu_kart = (oyuncu, kart_tipleri[1], oyuncular[oyuncu][kart_tipleri[1]].pop(0))
                            else:
                                print(f"{oyuncu} adlı oyuncunun {kart_tipleri[1]} kartı kalmadı!")
                print(oyuncu_kart[0], oyuncu_kart[1] + oyuncu_kart[2])
                oynanan_kartlar.append(oyuncu_kart)
                oynayan += 1
                sira += 1
                if sira >= 4:
                    sira -= 4
            # atılan 4 karta göre eli kazananı bulma:
            en_buyuk = oynanan_kartlar[0]   # ilk atılanı en büyük kart kabul et
            for kart in oynanan_kartlar[1:]:
                if kart[1] == en_buyuk[1] and B.index(kart[2]) > B.index(en_buyuk[2]):
                    en_buyuk = kart  # en büyük ile aynı kart tipinde daha büyük atıldı ise en büyük kart kabul et
                elif en_buyuk[1] != '♠' and kart[1] == '♠':
                    en_buyuk = kart  # en büyük maça değilken maça atıldı ise en büyük kart kabul et
            print("eli kazanan:", en_buyuk[0])
            sira = oyuncu_sira.index(en_buyuk[0])
            oyun_skor[en_buyuk[0]] = oyun_skor.setdefault(en_buyuk[0], 0) + 1

            # puan hesaplama
    def skor_hesabı(tahminler):
        skor = 0
        for i in range(1, len(tahminler)+1):
            if int(tahminler)[i] == (en_buyuk[i]):
                skor = int(tahminler)[i] * 10
                if int(tahminler)[i] > (en_buyuk[i]):
                    skor += int(tahminler)[i] - (en_buyuk[i])
                elif tahminler[i] < en_buyuk[i]:
                    skor -= tahminler[i] * 10    
            else:
                skor -= tahminler[i] * 10
        return skor

    print("SKOR:", oyun_skor)  # oyuncuların kaçar el adığını gösterir (gerçek kurallara göre bir puanlama sistemi yok)
