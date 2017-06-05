import os, sys
from shutil import rmtree
import json
from config import config
import mistune

# Markdown parser
# https://github.com/lepture/mistune


# -------------------------------------
# Basics
# -------------------------------------

config_domain = config['domain']
config_postmds = config['postmds']
config_output = config['output']

postmds_dict = []
postmds_sorted = []
data_json = None
data_categories = []


# -------------------------------------
# Get MDs files
# -------------------------------------

if os.path.isdir(config_postmds):
    sortdates = []

    for md in os.listdir(config_postmds):
        md_path = os.path.join(config_postmds,md)
        
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
                postmds_dict.append(config)

    if len(postmds_dict):
        sortdates = sorted(sortdates,reverse=True)
        categories = sorted(list(set(data_categories)))

        for d in sortdates:
            for r,row in enumerate(postmds_dict):
                if row['date'] == d:
                    postmds_sorted.append(row)

        data = dict(categories=categories, post=postmds_sorted)
        data_json = json.dumps(data,indent=4)

        if os.path.exists(config_output):
            rmtree(config_output)
        os.makedirs(config_output)

        with open(os.path.join(config_output,'allpost.json'),'w') as j:
            j.write(data_json)


    if len(postmds_dict):
        for row in postmds_dict:
            html = mistune.markdown(row['post'])
            with open(os.path.join(config_output,row['html']),'w') as h:
                h.write(html)








