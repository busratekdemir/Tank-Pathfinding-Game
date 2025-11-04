Harika, dosyaların GitHub'a yüklenmesi en zor kısımdı. Tebrikler\!

Elbette, işte GitHub deposu için hazırladığımız **detaylı `README.md`** taslağı. Bu metin, projenin ne yaptığını ve hangi teknolojileri kullandığını çok net bir şekilde açıklar.

Bunu kopyalayıp GitHub'daki `README.md` dosyana yapıştırabilirsin.

-----

# Tank Pathfinding (BFS Algorithm)

Bu proje, Python, Tkinter ve Pillow kütüphaneleri kullanılarak oluşturulmuş interaktif bir yol bulma (pathfinding) görselleştirme aracıdır. Kullanıcılar dinamik olarak bir ızgara üzerinde engeller oluşturabilir ve "Başla" butonuna bastıklarında, bir tankın **BFS (Breadth-First Search - Genişlik Öncelikli Arama)** algoritmasını kullanarak hedefe giden en kısa yolu bulmasını izleyebilirler.

Bu proje, orijinal olarak bir PDF dokümanında belirtilen konseptten esinlenilerek geliştirilmiştir.

`![tank-animated](https://github.com/user-attachments/assets/6e37887a-87d2-4138-bfe6-0aff9ec954d4)` 

## 🚀 Temel Özellikler

  * **Dinamik Izgara:** "Height" (Yükseklik) ve "Width" (Genişlik) değerlerini girerek istediğiniz boyutta bir ızgara oluşturun.
  * **İnteraktif Engel Ekleme:** Izgara üzerindeki herhangi bir kareye tıklayarak bir engel ("duvar") ekleyin veya kaldırın.
  * **En Kısa Yol Bulma:** "Start" butonuna basıldığında, program **BFS algoritmasını** kullanarak Başlangıç (sol üst) noktasından Hedef (sağ alt) noktasına giden en kısa yolu hesaplar.
  * **Görsel Animasyon:** Tank, bulunan en kısa yolu takip ederek hareket eder.
  * **Dinamik Görüntü İşleme:** Program, `Pillow` kütüphanesini kullanarak tek bir tank resmini (`tank_original.gif`) yükler ve bu resmi kod içinde 4 farklı yöne (yukarı, aşağı, sol, sağ) otomatik olarak döndürür.
  * **Temalar:** Koyu tema desteği ile modern bir arayüz sunar.

## 🛠️ Kullanılan Teknolojiler

  * **Python 3:** Ana programlama dili.
  * **Tkinter:** Grafiksel kullanıcı arayüzü (GUI) için kullanıldı.
  * **Pillow (PIL):** Tank resmini yeniden boyutlandırmak ve dinamik olarak döndürmek için kullanıldı.
  * **Algoritma:** BFS (Breadth-First Search).

## ⚡ Nasıl Çalıştırılır

1.  Bu depoyu (repository) klonlayın veya indirin.
2.  Gerekli kütüphaneyi kurun:
    ```bash
    pip install Pillow
    ```
3.  Proje klasöründe `main.py` dosyasını çalıştırın:
    ```bash
    python main.py
    ```
4.  Arayüzdeki "Draw" butonuna basın, engellerinizi ekleyin ve "Start"a tıklayın\!
