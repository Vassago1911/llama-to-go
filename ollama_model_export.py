import json
import zipfile
import argparse
from pathlib import Path

import yaml
with open('ollama_pathing.yml') as f:
    d = yaml.safe_load(f)
SOURCE = d['models_source_dir']
TARGET = d['backup_target_dir']

def get_model_manifest_path(registry, repository, model_name, model_tag):
    return Path(f"{SOURCE}/models/manifests/{registry}/{repository}/{model_name}/{model_tag}")

def get_blob_file_path(digest):
    return Path(f"{SOURCE}/models/blobs/sha256-{digest.split(':')[1]}")

def read_manifest(manifest_path):
    with open(Path.joinpath(Path(SOURCE), manifest_path), 'r') as file:
        return json.load(file)

def create_zip(model_name, model_tag, output_zip):
    repository = 'library'
    registry = 'registry.ollama.ai'
    manifest_path = get_model_manifest_path(registry, repository, model_name, model_tag)
    manifest = read_manifest(manifest_path)

    with zipfile.ZipFile(output_zip, 'w') as zipf:
            # Pfad zum Manifest auf der Festplatte
            full_manifest_path = Path.joinpath(Path(SOURCE), manifest_path)
            # arcname bestimmt den Pfad innerhalb der ZIP
            zipf.write(full_manifest_path, arcname=manifest_path)

            # Add blobs
            for layer in manifest['layers']:
                blob_path = get_blob_file_path(layer['digest'])
                full_blob_path = Path.joinpath(Path(SOURCE), blob_path)
                zipf.write(full_blob_path, arcname=blob_path)

            # Add config blob
            config_blob_path = get_blob_file_path(manifest['config']['digest'])
            full_config_path = Path.joinpath(Path(SOURCE), config_blob_path)
            zipf.write(full_config_path, arcname=config_blob_path)

    print(f"Model '{model_name}:{model_tag}' exported successfully to '{output_zip}'")
    # print("You can import it to another Ollama instance with 'tar -xf <modelname>_<tag>_export.zip'")

def main():
    parser = argparse.ArgumentParser(description='Export Ollama model to a zip file.')
    parser.add_argument('model_name', type=str, help='Name of the model (e.g., gemma)')
    parser.add_argument('model_tag', type=str, help='Tag of the model (e.g., 2b)')
    parser.add_argument('--output', type=str, default='model_export.zip', help='Output zip file name')
    args = parser.parse_args()

    create_zip(args.model_name, args.model_tag, args.output)

if __name__ == "__main__":
    main()
