import pandas as pd
with open('/media/v/llm_bkp/LLaMa-To-Go/tmp_model_list') as f:
    content = '\n'.join( f.readlines() )

content = content.split('ago')
content = [ c + " ago" for c in content ]
for _ in range(5):
    content = [ c.replace('\n\n','\n').strip('\n') for c in content ]

content = [ (c.split('\n')[0], ( '\n'.join(c.split('\n')[1:-4]) ).replace('\n',' ').replace('  ',' '), *c.split('\n')[-4:] )  for c in content ]

print('split model descriptions according to naive text logic, got', len(content), 'models from tmp_file')

pre = len(content)
content = [ c for c in content if len(c) == 6 ]
past = len(content)

print('restricted to well parsed content entry', '' if pre == past else f"lost {pre - past} broken descriptions" )
content = pd.DataFrame(content, columns = ['model_name', 'model_description', 'skill-tags','pulls','model_subtags', 'last_updated'])
