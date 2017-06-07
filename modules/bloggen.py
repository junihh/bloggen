# -*- coding: utf-8 -*-

import os, sys, codecs
import json
import hashlib
import mistune
import yaml
from jinja2 import Environment, PackageLoader


# -------------------------------------
# Global vars
# -------------------------------------

reload(sys)  
sys.setdefaultencoding('utf8')

postmds_dict = []
postmds_sorted = []
data_json = None
data_categories = []

tpls = Environment(
    loader=PackageLoader('modules', '../templates')
)


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
                        html = md_nam + '.html'
                        permalink = 'http://' + settings['domain'] + '/' + html
                        postid = hashlib.sha1(html).hexdigest()

                        with open(md_path,'r') as mdfile:
                            content = []
                            config = {}
                            mdpost = None

                            for line in mdfile:
                                content.append(line)

                            content = '\n'.join(content).split('======================================================')
                            config = yaml.load(content[1].strip())
                            mdpost = content[2].strip()
                            
                            config.update({ 'id' : postid })
                            config.update({ 'html' : html })
                            config.update({ 'permalink' : permalink })
                            config.update({ 'date' : config['date'].strftime('%Y-%m-%d') })
                            config.update({ 'markdown' : mdpost })

                            if 'category' in config.keys():
                                data_categories.append(config['category'])
                            
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

                if not os.path.exists(settings['output']):
                    os.makedirs(settings['output'])

                with open(os.path.join(settings['output'],'allpost.json'),'w') as j:
                    j.write(data_json)

                make_htmls(data,settings['output'])
    else:
        print 'BLOGGEN: You forgot your site settings'


# -------------------------------------
# Output the html's
# -------------------------------------

# http://jinja.pocoo.org/docs/2.9/intro/#basic-api-usage

def make_htmls(data=None,output=None):
    with open(os.path.join(output,'index.html'),'w') as home:
        dat = {
            'site_title': data['settings']['title'],
            'categories': data['categories'],
            'rows': data['post']
        }
        htm = tpls.get_template('home.tpl').render(dat)
        home.write(htm)

    if len(data['post']) and (output is not None):
        for row in data['post']:
            with open(os.path.join(output,row['html']),'w') as page:
                image = None
                try:
                    image = row['image']
                except:
                    pass
                dat = {
                    'site_title': data['settings']['title'],
                    'categories': data['categories'],
                    'post': {
                        'id': row['id'],
                        'content': mistune.markdown(row['markdown']),
                        'title': row['title'],
                        'date': row['date'],
                        'category': row['category'],
                        'author': row['author'],
                        'permalink': row['permalink'],
                        'image': image
                    }
                }
                htm = tpls.get_template('post.tpl').render(dat)
                page.write(htm)

            

    







