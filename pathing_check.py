import os
import yaml

import glob

import datetime

today = str(datetime.datetime.now())[:10]

def dtime() -> str:
    return str(datetime.datetime.now())[:23]

def log(*z):
    print(dtime(), " --- ", *z)

with open('ollama_pathing.yml') as f:
    d = yaml.safe_load(f)
SOURCE = d['models_source_dir']
TARGET = d['backup_target_dir']
log('source at:',SOURCE)
log('target at:',TARGET)

if 'models' in os.listdir(SOURCE):
    log(f"{SOURCE} contains 'models/' folder, looks good")

mk = glob.glob(os.path.join(SOURCE, 'models', 'manifests'))
bm = glob.glob(os.path.join(SOURCE, 'models', 'blobs'))
expected = mk + bm
for p in expected:
    log(p)

unexpected = [ d for d in os.listdir(SOURCE) if d != 'models' ]

for p in unexpected:
    log(f"WARNING: unexpected directory models/{p}, if you put it there, we hope you know what it is")
