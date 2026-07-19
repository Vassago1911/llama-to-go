# 🦙LLaMa-To-Go🏃‍♀️  (0.1.0 - 20260720_Jack_version)

[<img src="cc-zero.svg" alt="CC0 Lizenz" width="100"/>](https://creativecommons.org/publicdomain/zero/1.0/)

First run:
`bash run.sh $SOURCE_DIR $BACKUP_DIR`

Every next run:
`bash run.sh`

Tool function:
Saves your `.ollama/models`-files into .zip files per ollama model, and restores from pre-existing backups after that.

Use:
If you have multiple devices with similar ollama setups you only need to load the model ones to share in your LAN and backup to an eternal disk.

Das Projekt besteht aus:

0. **ollama_pathing.yml** - hat zwei Werte: models_source_dir, backup_target_dir, fuer Quelle und Backupziel
1. **run.sh** - Haupt-Eintragspunkt: ruft backup_sync.sh auf
2. **ollama_model_backup_sync.sh** - Dispatcher mit 3 Schritten: Check, Backup, Restore  
3. **pathing_check.py** - Validiert Quell/Target-Verzeichnis und erwartet 'models/' Unterstruktur
4. **ollama_model_backup_loop.sh** - Schleife über `ollama list`, erstellt ZIP via export.py wenn nicht existierend
5. **ollama_model_restore_loop.sh** - Schleife über alle .zip Dateien, importiert mit overwrite-Schutz
6. **ollama_model_export.py** - Erstellt ZIP-Backups nach `backup_target_dir` aus `ollama list` und Quellverzeichnis `models_source_dir` aus der `ollama_pathing.yml`
7. **ollama_model_import.py** - Extrahiert alle LLM-Backup-ZIP-Dateien ins `model_source_dir` ohne ueberschreiben der schon vorhandenen
