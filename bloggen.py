import os, sys
from shutil import rmtree
import json
from config import config as appConfig
import mistune
import yaml
import datetime

# http://pyyaml.org/wiki/PyYAMLDocumentation
# https://github.com/lepture/mistune


# -------------------------------------
# Basics
# -------------------------------------

postmds_dict = []
postmds_sorted = []
data_json = None
data_categories = []


# -------------------------------------
# Get MDs files
# -------------------------------------

if os.path.isdir(appConfig['postmds']):
    sortdates = []

    for md in os.listdir(appConfig['postmds']):
        md_path = os.path.join(appConfig['postmds'],md)
        
        if os.path.isfile(md_path):
            mdsp = md.split('.')
            md_nam = mdsp[0]
            md_ext = mdsp[1]
            
            if md_ext in ('md','markdown','mdown','mkdn','mkd','mdwn','mdtxt','mdtext','text','txt'):
                config = None
                post = None

                html = md_nam + '.html'
                permalink = 'http://' + appConfig['domain'] + '/' + html

                with open(md_path,'r') as mdfile:
                    content = []
                    for line in mdfile:
                        content.append(line)

                    content = '\n'.join(content).split('======================================================')
                    config = yaml.load(content[1].strip())
                    post = content[2].strip()

                if 'category' in config.keys():
                    data_categories.append(config['category'])

                config.update({ 'id' : md_nam })
                config.update({ 'markdown' : md })
                config.update({ 'html' : html })
                config.update({ 'permalink' : permalink })
                config.update({ 'date' : config['date'].strftime('%Y-%m-%d') })
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

        site = dict(domain=appConfig['domain'],title=appConfig['site-title'])
        data = dict(categories=categories, post=postmds_sorted, site=site)
        data_json = json.dumps(data,indent=4)

        if os.path.exists(appConfig['output']):
            rmtree(appConfig['output'])
        os.makedirs(appConfig['output'])

        with open(os.path.join(appConfig['output'],'allpost.json'),'w') as j:
            j.write(data_json)

    if len(postmds_dict):
        for row in postmds_dict:
            html = mistune.markdown(row['post'])
            with open(os.path.join(appConfig['output'],row['html']),'w') as h:
                h.write(html)








