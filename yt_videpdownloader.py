#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
from datetime import datetime
import sys

try:
    import yt_dlp
except ImportError:
    print("yt-dlp yüklü değil. Önce: pip install -U yt-dlp", file=sys.stderr)
    sys.exit(1)

def desktop_path():
    # Masaüstü (Windows/Mac/Linux) uyumlu
    return str(Path.home() / "Desktop")

def build_format(height):
    """
    İstenen maksimum yüksekliğe göre format dizesi.
    Örn: 480 -> bestvideo[height<=480]+bestaudio/best[height<=480]
    """
    return f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"

def main():
    parser = argparse.ArgumentParser(
        description="YouTube video/playlist indirici (varsayılan hedef: Masaüstü)."
    )
    parser.add_argument("urls", nargs="*", help="Video veya playlist URL(leri)")
    parser.add_argument(
        "-a", "--batch-file",
        help="Her satırında bir URL olan liste dosyası (.txt) ile toplu indirme"
    )
    parser.add_argument(
        "-o", "--outdir",
        default=desktop_path(),
        help="Çıktı klasörü (varsayılan: Masaüstü)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=480,
        help="Maksimum video yüksekliği (varsayılan: 480)"
    )
    parser.add_argument(
        "--audio-only",
        action="store_true",
        help="Sadece ses indir (m4a/mp3 benzeri)"
    )
    parser.add_argument(
        "--mp3",
        action="store_true",
        help="Sadece ses indirip MP3'e dönüştür (ffmpeg gerektirir)"
    )
    parser.add_argument(
        "--playlist",
        action="store_true",
        help="URL bir oynatma listesi ise playlist sırasıyla isimlendir"
    )
    parser.add_argument(
        "--no-duplicates",
        action="store_true",
        help="Aynı dosyayı tekrar indirmemek için indirme arşivi kullan"
    )
    parser.add_argument(
        "--subtitles",
        action="store_true",
        help="Mevcutsa altyazıları indir ve videoya gömme (ffmpeg gerektirir)"
    )
    args = parser.parse_args()

    urls_to_download = list(args.urls)
    
    if args.batch_file:
        try:
            with open(args.batch_file, "r", encoding="utf-8") as f:
                batch_urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
                urls_to_download.extend(batch_urls)
        except Exception as e:
            print(f"Toplu indirme dosyası okunurken hata oluştu: {e}", file=sys.stderr)
            sys.exit(1)

    if not urls_to_download:
        print("Lütfen en az bir adet URL veya --batch-file parametresi ile liste belirtin.", file=sys.stderr)
        sys.exit(1)

    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)

    # Çıktı dosya adı şablonu
    if args.playlist:
        out_tmpl = os.path.join(outdir, "%(playlist_index)03d - %(title)s.%(ext)s")
    else:
        out_tmpl = os.path.join(outdir, "%(title)s.%(ext)s")

    # İndirme arşivi (tekrarları önlemek için)
    archive_file = os.path.join(outdir, "downloaded.txt") if args.no_duplicates else None

    ydl_opts = {
        "outtmpl": out_tmpl,
        "restrictfilenames": True,        # Dosya adlarını sade tut
        "noprogress": False,              # Konsolda ilerleme göstergesi
        "quiet": False,
        "merge_output_format": "mp4",     # Video + ses birleştirme hedefi
        "ignoreerrors": True,             # Hata olsa da diğerlerini dene
        "concurrent_fragment_downloads": 4,
    }

    if archive_file:
        ydl_opts["download_archive"] = archive_file

    # Ses-sadece modları
    if args.audio_only or args.mp3:
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3" if args.mp3 else "m4a",
                    "preferredquality": "0"
                }
            ],
            "merge_output_format": None,  # Ses için birleştirme yok
        })
    else:
        # Video formatını yüksekliği sınırlayarak seç
        ydl_opts["format"] = build_format(args.height)

    # Altyazı seçenekleri
    if args.subtitles:
        ydl_opts.update({
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["all"],
            "embedsubtitles": True,
        })

    # Basit ilerleme callback’i
    def hook(d):
        if d.get("status") == "downloading":
            # Konsol çıktısını sade tut
            pass
        elif d.get("status") == "finished":
            print(f"✅ Tamamlandı: {d.get('filename')} ({datetime.now().strftime('%H:%M:%S')})")

    ydl_opts["progress_hooks"] = [hook]

    print(f"📥 İndirme başlıyor → {len(urls_to_download)} adet URL listeye alındı.")
    print(f"💾 Kayıt klasörü: {outdir}")
    if not (args.audio_only or args.mp3):
        print(f"🎞️ Maks. yükseklik: {args.height}p")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Playlist kullanımını otomatik algılar; ancak isimlendirme için flag verdik
        ydl.download(urls_to_download)

if __name__ == "__main__":
    main()