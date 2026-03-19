# YouTube Video İndirici & Dönüştürücü 🎬🎧

Bu proje, YouTube'dan yüksek kaliteli videolar veya yalnızca ses dosyaları indirmeyi ve bilgisayarınızda mevcut bazı videoları MP3 formatına dönüştürmeyi sağlayan Python araçları içerir.

## 🛠 Kurulum ve Hazırlık

Python bağımlılıklarınızı yönetmek ve komutları sorunsuz çalıştırmak için, bir sanal ortam (virtual environment - `.venv`) kullanılmaktadır. Terminal üzerinden her kullanımdan önce bu ortamı aktif etmelisiniz.

Proje klasörüne gidin:
```bash
cd /Users/thomasmuentzer/Desktop/projects/ytvideos
```

Sanal ortamı aktif edin:
```bash
source .venv/bin/activate
```

*(Not: Ortam aktiflendiğinde komut satırınızın başında `(.venv)` ibaresini görmelisiniz. İsterseniz bu işlemi her sefere yapmamak için direkt `.venv/bin/python3` yolunu da kullanabilirsiniz.)*

---

## 🚀 1. YouTube'dan İndirme (`yt_videpdownloader.py`)

İndirilen dosyalar varsayılan olarak **Masaüstünüze (Desktop)** kaydedilir. Dilerseniz `-o` bayrağıyla (örneğin `-o /Baska/Bir/Klasor`) bunu değiştirebilirsiniz.

### Tek Bir Videoyu İndirmek
Örneğin videoyu MP4 formatında ve en fazla 720p kalitede indirmek için:
```bash
python3 yt_videpdownloader.py "YOUTUBE_LİNKİ" --height 720
```

### Yalnızca Ses (MP3) Olarak İndirmek
Videodaki sesi direkt çekip MP3 dosyası olarak almak için:
```bash
python3 yt_videpdownloader.py "YOUTUBE_LİNKİ" --mp3
```

### Ucu Uca (Sırayla) Birden Fazla Link İndirmek
Birden fazla videoyu arka arkaya verebilirsiniz.
```bash
python3 yt_videpdownloader.py "LİNK_1" "LİNK_2" "LİNK_3" --mp3
```

### Bir Liste Dosyasından (.txt) Toplu MP3 İndirmek
Elinizde çok sayıda link var ise, bunları `liste.txt` isminde bir dosyaya her satıra bir tane gelecek şekilde koyabilirsiniz. Daha sonra bu listeyi okutarak toplam indirme yapabilirsiniz:
```bash
python3 yt_videpdownloader.py --batch-file liste.txt --mp3
```
*(Yukarıdaki betik sadece `--mp3` kullanıldığı için ses olarak çeker, isterseniz `--mp3` kısmını silerek normal video gibi de listeyi çekebilirsiniz).*

---

## 💽 2. Mevcut Bilgisayardaki Videoları Sese Çevirmek (`video_converter.py`)

Zaten indirmiş olduğunuz veya halihazırda bulunan video (.mp4, .mov, .mkv gibi) dosyalarınızı da tek bir komutla topluca MP3'e çevirebilirsiniz.

**Kullanım Adımları:**
1. Dosyanın içindeki ayarlanmış kaynak klasöre (`/Users/thomasmuentzer/Desktop/yt_videos`) dönüştürmek istediğiniz videoları atın.
2. Script'i çalıştırın:
```bash
python3 video_converter.py
```
Bu adımla birlikte, gösterdiğiniz klasörün içerisine "audios" adında taze bir hedef klasör oluşturulacak ve dönüştürülen sesler doğrudan oraya aktarılacaktır.
