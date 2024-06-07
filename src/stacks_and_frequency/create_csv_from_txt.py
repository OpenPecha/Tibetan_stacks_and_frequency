from pathlib import Path
import pyewts
converter = pyewts.pyewts()


def create_csv_from_txt(transcription_paths):
    csv_data = ["imagename", "transcription"]
    # for transcription_dir in transcription_dirs:
    #     transcription_name = transcription_dir.stem
    for transcription_path in transcription_paths:
        image_name = transcription_path.stem
        transcription = converter.toUnicode(transcription_path.read_text(encoding='utf-8'))
        csv_data.append([f"{image_name}.jpg", transcription])
    with open("./transcriptions.csv", "w") as f:
        for row in csv_data:
            f.write(f"{row[0]},{row[1]}\n")


def main():
    transcription_paths = list(Path("/Users/tashitsering/Desktop/Work/OCR-data-consolidation/data/lhasa_kanjur/transcriptions").iterdir())
    create_csv_from_txt(transcription_paths)




if __name__ == "__main__":
    main()