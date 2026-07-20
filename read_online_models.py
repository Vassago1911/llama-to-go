import pandas as pd
import requests
from bs4 import BeautifulSoup

import datetime

today = str(datetime.datetime.now())[:10]

def dtime() -> str:
    return str(datetime.datetime.now())[:23]

def log(*z):
    print(dtime(), " --- ", *z)

df = pd.read_csv('ollama_models_20260720.csv',sep=';')

def str_resolves_to_int(hashstr:str):
    try:
        _ = int(hashstr,base=16)
        return True
    except Exception as _:
        return False

def model_file_url(model_name:str):
    tmp = f"https://ollama.com/library/{model_name}/tags"
    return tmp

def get_model_soup_at_ix(ix:int=53):
    model_names = list( df.model_name.unique() )
    model_urls = sorted( list(map(model_file_url,model_names)) )

    res = requests.get(model_urls[ix])
    soup = BeautifulSoup(res.content, 'html.parser').find_all('span')
    return soup

def get_model_name_at_ix(ix:int=16):
    model_names = list( df.model_name.unique() )
    model_urls = sorted( list(map(model_file_url,model_names)) )
    return model_urls[ix]

def soup_to_rows(soup, model_name):
    soup = [ s.text.replace('\n',' ') for s in soup ]
    for _ in range(5):
        soup = [ s.replace('  ', ' ').strip() for s in soup if s not in ('','MLX') ]
    soup = [ s.replace(' MLX','_mlx') for s in soup ]
    standard_hash = '5571076f3d70'
    hashes = [ h for h in soup if len(h) == len(standard_hash) ]
    hashes = [ h for h in hashes if str_resolves_to_int(h) ]
    unique_hashes = []
    for h in hashes:
        if h not in unique_hashes:
            unique_hashes = unique_hashes + [h]
    hashes = unique_hashes
    soup_text = ' '.join(soup)
    soup_words = soup_text.split(' ')
    hash_indices = []
    row_indices = []
    for hash in unique_hashes:
        hash_indices = [ i for i, x in enumerate(soup_words) if x == hash ]
        assert len(hash_indices) % 3 == 0, 'strange hash index count, please check the displayed page for quirks'
        while len(hash_indices) > 0:
            first3, rest = hash_indices[:3], hash_indices[3:]
            row_indices = row_indices + [first3]
            hash_indices = rest
    # min_hash_ix = min(map(min,row_indices))
    # header_text = ' '.join( soup_words[ : min_hash_ix - 1 ] )
    rows = []
    for ixs in row_indices:
        row = ' '.join( soup_words[ ixs[0] - 1: ixs[2] + 1])
        if ':' in row.split(' ')[0]:
            rows = rows + [ row ]
    rows = [ ( row.split(' ')[-1], row ) for row in rows ]
    rows = [ hash + ' • ' + ' '.join( row.split(hash)[:2] ) for hash, row in rows ]
    rows = [ [z.strip() for z in row.split('•') ] for row in rows ]
    rows = pd.DataFrame(rows,columns=['model_hash','tagged_model','model_size','model_context','model_modalities','last_updated_at'])
    rows['model_url'] = model_name
    rows = rows[['model_url','model_hash','tagged_model','model_size','model_context','model_modalities','last_updated_at']].copy()
    return rows

def collect_all_rows():
    model_names = list( df.model_name.unique() )
    total_res = []
    for i, _ in enumerate(model_names):
        log('getting row', i)
        soup = get_model_soup_at_ix(i)
        model_name = get_model_name_at_ix(i)
        rows = soup_to_rows(soup, model_name)
        if len(total_res) == 0:
            total_res = rows
        else:
            total_res = pd.concat([total_res,rows], ignore_index=True)
    return total_res

rows = collect_all_rows()
rows.to_csv('all_models_20260720.csv',index=False)
