import pandas as pd
df = pd.read_csv('all_models_20260720.csv')
df['model_context'] = df['model_context'].apply(lambda z: z.replace(' context window','')).apply(lambda z: z.replace('K','000').replace('M','000000')).apply(int)
df = df.dropna().reset_index(drop=True)
df = df[df.model_size.apply(lambda z: 'TB' not in z)]
df = df[df.model_size.apply(lambda z: 'Usage' not in z)]
df = df[df.tagged_model.apply(lambda z: 'mlx' not in z.lower())]
df = df.dropna().reset_index(drop=True)

time_delta_texts = [ '1 week ago'
                    , '2 weeks ago'
                    , '3 weeks ago'
                    , '4 weeks ago'
                    , '1 month ago'
                    , '2 months ago'
                    , '3 months ago'
                    , '4 months ago'
                    , '5 months ago'
                    , '6 months ago'
                    , '7 months ago'
                    , '8 months ago'
                    , '9 months ago'
                    , '10 months ago'
                    , '11 months ago'
                    , '12 months ago'
                    , '1 year ago'
                    , '2 years ago'
                    ]
time_delta_days = [7,14,21,28,30,60,90,120,150,180,210,240,270,300,330,360,364,728]
time_replacer = dict(zip(time_delta_texts,time_delta_days))
df['last_updated_at'] = df['last_updated_at'].apply(lambda z: time_replacer[z])

df['size_unit'] = df.model_size.apply(lambda z: z[ z.find('B') - 1 : z.find('B') + 1] )
df['size_number'] = df.model_size.apply(lambda z: z.replace( z[ z.find('B') - 1 : z.find('B') + 1], '') ).apply(float)

assert 'MB' in list(df.size_unit.unique())
assert 'GB' in list(df.size_unit.unique())
assert len(list(df.size_unit.unique())) == 2
df['size_MB'] = df[['size_unit','size_number']].apply(lambda z: round( z['size_number'] * 1000 ) if z['size_unit'] == 'GB' else round( z['size_number'] ) ,axis=1).apply(int)
cols = ['last_updated_at', 'size_MB', 'tagged_model', 'model_context', 'model_modalities', ]
df = df[cols]
df = df.sort_values(['size_MB','last_updated_at'],ascending=True).reset_index(drop=True)
df = df[ ( df.size_MB < 16000 ) & ( df.size_MB > 400 ) & ( df.last_updated_at < 400 )].reset_index(drop=True)
df = df.copy()
vl = df[df.model_modalities != 'Text input']
vl = df[df.model_modalities == 'Text input']

for z in list(vl.tagged_model.unique()):
    print(f"ollama pull {z}")

# use like: python analyse_all_models.py >> all_pulls.sh; bash all_pulls.sh
