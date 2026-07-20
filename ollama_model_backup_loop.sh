#!/usr/bin/env bash
BACKUP_DIR=$(python -c "
import yaml
with open('ollama_pathing.yml') as f:
    d = yaml.safe_load(f)
print(d['backup_target_dir'])"
)
echo "Backup wurde laut ollama_pathing.yml gespeichert unter:"
echo "$BACKUP_DIR"

ollama list | tail -n +2 | while read -r name id size modified; do
    [[ -z "$name" ]] && continue

    # Check if the model name contains '/', skip it
    if [[ "$name" == *"/"* ]]; then
        echo "Skipping $name (Contains '/')"
        continue
    fi

    model_name="${name%%:*}"
    model_tag="${name#*:}"
    [[ "$model_tag" == "$model_name" ]] && model_tag="latest"

    target="${BACKUP_DIR}/${model_name}_${model_tag}.zip"

    if [ -f "$target" ]; then
        echo "Skipping $model_name:$model_tag (Backup already exists)"
    else
        echo "Exporting $model_name:$model_tag → $target ..."
        python3 ollama_model_export.py "$model_name" "$model_tag" --output "$target"
    fi
done
