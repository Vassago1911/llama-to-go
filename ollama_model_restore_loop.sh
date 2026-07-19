#!/usr/bin/env bash
BACKUP_DIR=$(python -c "
import yaml
with open('ollama_pathing.yml') as f:
    d = yaml.safe_load(f)
print(d['backup_target_dir'])"
)
echo "Backup wurde laut ollama_pathing.yml gespeichert unter:"
echo "$BACKUP_DIR"

for zip_file in "$BACKUP_DIR"/*.zip; do
    [ -e "$zip_file" ] || continue
    # echo "Restoring $zip_file ..."
    python3 ollama_model_import.py "$zip_file"
done
echo "All models restored."
