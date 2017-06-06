import os, sys
from shutil import rmtree
import json
import mistune
import yaml


# -------------------------------------
# Global vars
# -------------------------------------

postmds_dict = []
postmds_sorted = []
data_json = None
data_categories = []


# -------------------------------------
# Get MDs files
# -------------------------------------

def maker(settings=None):
    if settings is not None:
        if os.path.isdir(settings['postmds']):
            sortdates = []

            for md in os.listdir(settings['postmds']):
                md_path = os.path.join(settings['postmds'],md)
                
                if os.path.isfile(md_path):
                    mdsp = md.split('.')
                    md_nam = mdsp[0]
                    md_ext = mdsp[1]
                    
                    if md_ext in ('md','markdown','mdown','mkdn','mkd','mdwn','mdtxt','mdtext','text','txt'):
                        config = None
                        post = None

                        html = md_nam + '.html'
                        permalink = 'http://' + settings['domain'] + '/' + html

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

                site = dict(domain=settings['domain'],title=settings['site_title'])
                data = dict(categories=categories, post=postmds_sorted, settings=site)
                data_json = json.dumps(data,indent=4)

                if os.path.exists(settings['output']):
                    rmtree(settings['output'])
                os.makedirs(settings['output'])

                with open(os.path.join(settings['output'],'allpost.json'),'w') as j:
                    j.write(data_json)

                make_htmls(postmds_dict,settings['output'])
    else:
        print 'BLOGGEN: You forgot your site settings'


# -------------------------------------
# Output the html's
# -------------------------------------

def make_htmls(rows=None,output=None):
    if len(rows) and (output is not None):
        for row in rows:
            html = mistune.markdown(row['post'])
            with open(os.path.join(output,row['html']),'w') as h:
                h.write(html)

