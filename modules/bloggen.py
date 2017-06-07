# -*- coding: utf-8 -*-

import os, sys
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

postymls_dict = []
postymls_sorted = []
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
        if os.path.isdir(settings['posts']):
            sortdates = []

            for yml in os.listdir(settings['posts']):
                yml_path = os.path.join(settings['posts'],yml)
                
                if os.path.isfile(yml_path):
                    yml_nam, yml_ext = os.path.splitext(yml)
                    yml_ext = yml_ext[1:]
                    
                    if yml_ext in ('md','markdown','mdown','mkdn','mkd','mdwn','mdtxt','mdtext','text','txt','yml','yaml'):
                        html = yml_nam + '.html'
                        permalink = 'http://' + settings['domain'] + '/' + html
                        postid = hashlib.sha1(yml).hexdigest()

                        with open(yml_path,'r') as ymlfile:
                            content = []
                            config = {}
                            mrkdwn = None

                            for line in ymlfile:
                                content.append(line)

                            content = '\n'.join(content).split('======================================================')
                            config = yaml.load(content[0].strip())
                            mrkdwn = content[1].strip()
                            
                            config.update({ 'id': postid })
                            config.update({ 'file': html })
                            config.update({ 'permalink': permalink })
                            config.update({ 'date': config['date'].strftime('%Y-%m-%d') })
                            config.update({ 'content': mrkdwn })

                            configKeys = config.keys()
                            if 'excerpt' in configKeys:
                                config.update({ 'excerpt': config['excerpt'].replace('\n',' ') })
                            if 'category' in configKeys:
                                data_categories.append(config['category'])
                            
                            sortdates.append(config['date'])
                            postymls_dict.append(config)

            if len(postymls_dict):
                sortdates = sorted(sortdates,reverse=True)
                categories = sorted(list(set(data_categories)))

                for d in sortdates:
                    for r,row in enumerate(postymls_dict):
                        if row['date'] == d:
                            postymls_sorted.append(row)

                site = dict(domain=settings['domain'],title=settings['site_title'])
                data = dict(categories=categories, post=postymls_sorted, settings=site)
                data_json = json.dumps(data,indent=4)

                if not os.path.exists(settings['output']):
                    os.makedirs(settings['output'])

                with open(os.path.join(settings['output'],'allpost.json'),'w') as j:
                    j.write(data_json)

                htmls(data,settings['output'])

    else:
        print 'BLOGGEN: You forgot your site settings'


# -------------------------------------
# HTML's
# -------------------------------------

def htmls(data=None,output=None):
    if len(data['post']) and (output is not None):

        # Remove all *.html pages inside output directory
        for h in os.listdir(output):
            h_path = os.path.join(output,h)
            if os.path.isfile(h_path) and h.endswith('.html'):
                os.remove(h_path)

        # Output index.html
        with open(os.path.join(output,'index.html'),'w') as home:
            dat = {
                'site_title': data['settings']['title'],
                'categories': data['categories'],
                'rows': data['post']
            }
            htm = tpls.get_template('home.tpl').render(dat)
            home.write(htm)

        # Output all post pages
        for row in data['post']:
            with open(os.path.join(output,row['file']),'w') as page:
                image = row['image'] if ('image' in row.keys()) else None
                content = mistune.markdown(row['content'])
                dat = {
                    'site_title': data['settings']['title'],
                    'categories': data['categories'],
                    'post': {
                        'id': row['id'],
                        'content': content,
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

