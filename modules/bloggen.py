# -*- coding: utf-8 -*-

import os, sys, hashlib, json, base64, mimetypes
from bs4 import BeautifulSoup
from filemimes import filemimes
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

templates_dir = '../templates'
tpls = Environment(
    loader=PackageLoader('modules', templates_dir)
)


# -------------------------------------
# Yaml-Markdown processing
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

                        with open(yml_path,'rt') as ymlfile:
                            content = []
                            config = {}
                            mrkdwn = None

                            for line in ymlfile:
                                content.append(line)

                            content = '\n'.join(content).split('======================================================')
                            config = yaml.load(content[0])
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

                site = dict(domain=settings['domain'], title=settings['site_title'])
                data = dict(categories=categories, post=postymls_sorted, settings=site)

                _htmls(data,settings['output'])

    else:
        print 'BLOGGEN: You forgot your site settings'


# -------------------------------------
# Make json and html's files
# -------------------------------------

def _filetoB64 (dirpath=None,sourcepath=None,raw=False):
    fstring = None
    fmime = None
    freturn = None

    if (dirpath is not None) and (sourcepath is not None):
        sourcepath = os.path.join(dirpath,sourcepath)

        if os.path.isfile(sourcepath):
            fmime = mimetypes.MimeTypes().guess_type(sourcepath)[0]
            
            if fmime in (filemimes['text'] + filemimes['image'] + filemimes['audio'] + filemimes['video']):
                with open(sourcepath,'rb') as f:
                    fcontent = f.read()
                    fstring = base64.encodestring(fcontent).replace('\n','')

                    if raw:
                        freturn = fstring
                    else:
                        freturn = ''.join(['data:',fmime,';base64,',fstring])
            else:
                freturn = sourcepath
        else:
            freturn = sourcepath

    return freturn


def _encodesourcesHTML (dirpath=None):
    if (dirpath is not None) and os.path.isdir(dirpath):
        html_content = None

        for htmlfile in os.listdir(dirpath):
            htmlfile_path = os.path.join(dirpath,htmlfile)

            if os.path.isfile(htmlfile_path) and htmlfile.endswith('.html'):
                with open(htmlfile_path,'rt') as read_html:
                    html_content = []
                    for line in read_html:
                        line = line.strip()
                        html_content.append(line)
                    html_content = '\n'.join(html_content)

                    if html_content:
                        htmlBS = BeautifulSoup(html_content,'html.parser')

                        for node in htmlBS.find_all('img'):
                            if node.name == 'img':
                                srcpath = node.get('src')
                                node['src'] = _filetoB64(dirpath,srcpath)

                        html_content = htmlBS.renderContents()

                with open(htmlfile_path,'w') as write_html:
                    write_html.write(html_content)


def _htmls(data=None,output=None):
    if len(data['post']) and (output is not None):

        # Make the output directory if not available
        if not os.path.exists(output):
            os.makedirs(output)

        # Remove all *.html files inside output directory
        for html in os.listdir(output):
            html_path = os.path.join(output,html)
            if os.path.isfile(html_path) and html.endswith('.html'):
                os.remove(html_path)

        # Make the website json
        with open(os.path.join(output,'allpost.json'),'w') as j:
            data_json = json.dumps(data,indent=2)
            j.write(data_json)

        # Output index.html
        with open(os.path.join(output,'index.html'),'w') as home:
            dat = {
                'site_title': data['settings']['title'],
                'categories': data['categories'],
                'rows': data['post']
            }
            tpl = tpls.get_template('home.tpl').render(dat)
            home.write(tpl)

        # Output all post html's
        for row in data['post']:
            with open(os.path.join(output,row['file']),'w') as page:
                row['image'] = row['image'] if ('image' in row.keys()) else None
                row['content'] = mistune.markdown(row['content']) if ('content' in row.keys()) else None
                dat = {
                    'site_title': data['settings']['title'],
                    'categories': data['categories'],
                    'post': row
                }
                tpl = tpls.get_template('post.tpl').render(dat)
                page.write(tpl)

        # Encode base64 html's resources
        _encodesourcesHTML(output)





