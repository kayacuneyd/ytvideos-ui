import os
import subprocess

input_folder = "/Users/thomasmuentzer/Desktop/yt_videos"
output_folder = os.path.join(input_folder, "audios")

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + ".mp3"
        output_path = os.path.join(output_folder, output_filename)

        command = [
            "ffmpeg",
            "-i", input_path,
            "-q:a", "0",   # best audio quality
            "-map", "a",
            output_path
        ]

        print(f"Converting {filename} → {output_filename}")
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

print("✅ Tüm videolar ses dosyasına dönüştürüldü.")