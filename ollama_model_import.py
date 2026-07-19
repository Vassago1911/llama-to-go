import zipfile
import argparse
from pathlib import Path

def import_model(input_zip):
    extract_to = Path('/')
    total_files = 0
    restored_files = 0
    skipped_files = 0

    with zipfile.ZipFile(input_zip, 'r') as zipf:
        file_list = zipf.infolist()
        total_files = len(file_list)

        for file_info in file_list:
            target_path = extract_to / file_info.filename
            # print( target_path )

            # Prüfen, ob Datei existiert und nicht leer ist
            if target_path.exists():
                skipped_files += 1
            else:
                # Verzeichnisstruktur sicherstellen
                target_path.parent.mkdir(parents=True, exist_ok=True)
                # Einzelne Datei extrahieren
                with zipf.open(file_info) as source, open(target_path, "wb") as target:
                    target.write(source.read())
                restored_files += 1

    if file_list:
        file_info = file_list[0]
        print(f"{input_zip:>64} --> {file_info.filename.split('models/')[0]} : {restored_files}/{total_files} files restored.")

def main():
    parser = argparse.ArgumentParser(description='Import Ollama model with smart overwrite protection.')
    parser.add_argument('zip_file', type=str, help='Path to the zip file')
    args = parser.parse_args()
    import_model(args.zip_file)

if __name__ == "__main__":
    main()
