#!/bin/bash

# ── First-time setup: write ollama_pathing.yml ────────────────────────────────
if [ "$#" -ne 0 ]; then      # any args = setup mode
    SOURCE_DIR="$1"
    TARGET_DIR="$2"

    echo "backup_target_dir: ${TARGET_DIR}" > ollama_pathing.yml
    echo "models_source_dir: ${SOURCE_DIR}" >> ollama_pathing.yml
    echo "Initialized ollama_pathing.yml — next run just 'bash run.sh'" >&2

    exit 0
fi

# ── Normal mode: read config and sync ────────────────────────────────────────
if [ ! -f ollama_pathing.yml ]; then
    echo "ollama_pathing.yml not found. Run 'bash run.sh <source> <target>' first." >&2
    exit 1
fi

BACKUP_DIR=$(python3 -c "
import yaml
with open('ollama_pathing.yml') as f:
    d = yaml.safe_load(f)
print(d['backup_target_dir'])"
)

SOURCE_DIR=$(python3 -c "
import yaml
with open('ollama_pathing.yml') as f:
    d = yaml.safe_load(f)
print(d['models_source_dir'])"
)

echo "Backup source → ${SOURCE_DIR}"
echo "Backup target → ${BACKUP_DIR}"
echo "Running sync…"
bash ollama_model_backup_sync.sh
