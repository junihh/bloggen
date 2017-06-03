import os, sys
from shutil import rmtree as shutil_remove
import json
from config import config


# -------------------------------------
# Basics
# -------------------------------------

config_domain = config['domain']
config_mds = config['mds']
config_output = config['output']


# -------------------------------------
# Get MDs files
# -------------------------------------

mds_dict = []
mds_sorted = []
data_json = None
data_categories = []

if os.path.isdir(config_mds):
    sortdates = []

    for md in os.listdir(config_mds):
        md_path = os.path.join(config_mds,md)
        
        if os.path.isfile(md_path):
            mdsp = md.split('.')
            md_nam = mdsp[0]
            md_ext = mdsp[1]
            
            if md_ext in ('md','markdown','mdown','mkdn','mkd','mdwn','mdtxt','mdtext','text','txt'):
                config = None
                post = None

                html = md_nam + '.html'
                permalink = 'http://' + config_domain + '/' + html

                with open(md_path,'r') as mdfile:
                    content = []
                    for line in mdfile:
                        line = line.strip()
                        if line:
                            content.append(line)

                    content = '\n'.join(content).split('======================================================')
                    config = content[1].strip()
                    post = content[2].strip()

                config_parts = config.split('\n')
                config = {}

                for part in config_parts:
                    kv = part.split(': ')
                    k = kv[0].strip()
                    v = kv[1].strip()

                    config.update({ k : v })

                    if k == 'category':
                        data_categories.append(v)

                config.update({ 'id' : md_nam })
                config.update({ 'markdown' : md })
                config.update({ 'html' : html })
                config.update({ 'permalink' : permalink })
                config.update({ 'post' : post })

                sortdates.append(config['date'])
                mds_dict.append(config)

    if len(mds_dict):
        sortdates = sorted(sortdates,reverse=True)

        for d in sortdates:
            for r,row in enumerate(mds_dict):
                if row['date'] == d:
                    mds_sorted.append(row)

        if len(sortdates):
            data_categories = sorted(list(set(data_categories)))

            data = {
                'categories': data_categories,
                'post': mds_sorted
            }

            data_json = json.dumps(data,indent=4)

            if os.path.exists(config_output):
                shutil_remove(config_output)
            os.makedirs(config_output)

            with open(os.path.join(config_output,'allpost.json'),'w') as j:
                j.write(data_json)

print data_json






