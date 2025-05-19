import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
from pathlib import Path
from pydub import AudioSegment
from tqdm import tqdm

folder_path = '/home/w.wu.751/passive-acoustic-biodiversity/kendall-frost-march-2025/BirdNET_baseline_output'
all_files = glob.glob(os.path.join(folder_path, "*.BirdNET.selection.table.txt"))

dfs = []
for file in all_files:
    df = pd.read_csv(file, sep='\t')
    dfs.append(df)

all_data = pd.concat(dfs, ignore_index=True)

nocall_count = (all_data['Common Name'] == 'nocall').sum()
print(f"Number of nocall detections: {nocall_count}")
clean_data = all_data[all_data['Common Name'] != 'nocall']

output_root = "/home/w.wu.751/passive-acoustic-biodiversity/kendall-frost-march-2025/species_audio_clips"
Path(output_root).mkdir(exist_ok=True)

# Loop through each detection in clean_data
for idx, row in tqdm(clean_data.iterrows(), total=len(clean_data)):
    try:
        species = row['Common Name'].strip().replace(" ", "_")
        file_path = row['Begin Path']
        offset_sec = float(row['File Offset (s)'])
        end_time_sec = float(row['End Time (s)'])

        audio = AudioSegment.from_wav(file_path)

        start_ms = int(offset_sec * 1000)
        end_ms = int(end_time_sec * 1000)
        segment = audio[start_ms:end_ms]

        species_folder = Path(output_root) / species
        species_folder.mkdir(exist_ok=True)

        filename = Path(file_path).stem
        clip_filename = f"{filename}_{int(start_ms)}ms_{int(end_ms)}ms.wav"
        clip_path = species_folder / clip_filename

        segment.export(clip_path, format="wav")

    except Exception as e:
        print(f"Error processing row {idx} ({row['Common Name']}): {e}")
