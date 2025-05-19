import os
import subprocess
from tqdm import tqdm

input_root = "/home/w.wu.751/passive-acoustic-biodiversity/kendall-frost-march-2025"
output_dir = os.path.join(input_root, "BirdNET_baseline_output")
log_file_path = os.path.join(output_dir, "birdnet_run_log.txt")

latitude = 32.7909
longitude = -117.2298
week = 11
threads = 2

wav_files = []
for root, _, files in os.walk(input_root):
    for file in files:
        if file.lower().endswith(".wav"):
            wav_files.append(os.path.join(root, file))

os.makedirs(output_dir, exist_ok=True)


with open(log_file_path, "a") as log_file:
    log_file.write(f"Starting BirdNET batch analysis on {len(wav_files)} files...\n\n")
    for wav_path in tqdm(wav_files, desc="Analyzing audio files"):
        log_file.write(f"Analyzing {wav_path}\n")
        command = [
            "python3", "-m", "birdnet_analyzer.analyze",
            wav_path,
            "--output", output_dir,
            "--lat", str(latitude),
            "--lon", str(longitude),
            "--week", str(week),
            "-t", str(threads)
        ]
        subprocess.run(command, stdout=log_file, stderr=log_file)

    log_file.write("\nBatch analysis complete.\n")

print(f"Finished analyzing {len(wav_files)} files.")
print(f"Output saved to: {output_dir}")
print(f"Log file saved to: {log_file_path}")
