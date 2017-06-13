# -*- coding: utf-8 -*-

import os, sys, hashlib, json, base64, mimetypes
from bs4 import BeautifulSoup
import mistune
import yaml
import jinja2
from filemimes import filemimes


# -------------------------------------
# Setup
# -------------------------------------

reload(sys)  
sys.setdefaultencoding('utf8')

templates_dir = '../templates'
tpls = jinja2.Environment(
    loader = jinja2.PackageLoader('modules', templates_dir)
)


# -------------------------------------
# Site maker
# -------------------------------------

class Bloggen(object):
    settings = None
    datasite = None

    def __init__(self):
        pass

    def make(self,**settings):
        postymls = []
        sortdates = []
        categories = []
        postdir = None

        settingsKeys = settings.keys()
        if 'postdir' not in settingsKeys:
            settings['postdir'] = './posts'
        if 'outputdir' not in settingsKeys:
            settings['outputdir'] = './output'
        if 'domain' not in settingsKeys:
            settings['domain'] = 'coolsite.me'
        if 'site_title' not in settingsKeys:
            settings['site_title'] = 'My cool website'
        if 'encodedResources' not in settingsKeys:
            settings['encodedResources'] = True
        self.settings = settings
        postdir = settings['postdir']

        if not os.path.exists(postdir):
            os.makedirs(postdir)

        for yml in os.listdir(postdir):
            yml_path = os.path.join(postdir,yml)
            
            if os.path.isfile(yml_path):
                yml_nam, yml_ext = os.path.splitext(yml)
                yml_ext = yml_ext[1:]
                
                if yml_ext in ('md','markdown','mdown','mkdn','mkd','mdwn','mdtxt','mdtext','text','txt','yml','yaml','yamel'):
                    html = yml_nam + '.html'
                    permalink = ''.join(['http://', settings['domain'], '/', html])
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
                            categories.append(config['category'])
                        
                        sortdates.append(config['date'])
                        postymls.append(config)

        if len(postymls):
            sortdates = sorted(sortdates,reverse=True)
            categories = sorted(list(set(categories)))

            postymls_sorted = []
            for d in sortdates:
                for r,row in enumerate(postymls):
                    if row['date'] == d:
                        postymls_sorted.append(row)

            self.datasite = dict(
                categories = categories,
                post = postymls_sorted,
                settings = dict(
                    domain = settings['domain'],
                    title = settings['site_title']
                )
            )

            self.makeSiteFiles()
            print 'BLOGGEN [OK]: Your website is ready.'
        else:
            print 'BLOGGEN [WARNING]: None post available. Write some and save it into the "' + os.path.abspath(postdir) + '" directory.'


    def makeSiteFiles(self):
        settings = self.settings
        datasite = self.datasite
        outputdir = self.settings['outputdir']
        datasite_json = None

        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        # Make the website json
        with open(os.path.join(outputdir,'allpost.json'),'w') as j:
            datjson = json.dumps(datasite,indent=2)
            j.write(datjson)

        # Remove all *.html files inside the output directory
        for html in os.listdir(outputdir):
            html_path = os.path.join(outputdir,html)
            if os.path.isfile(html_path) and html.endswith('.html'):
                os.remove(html_path)

        # Output index.html
        with open(os.path.join(outputdir,'index.html'),'w') as home:
            dat = {
                'site_title': datasite['settings']['title'],
                'categories': datasite['categories'],
                'rows': datasite['post']
            }
            tpl = tpls.get_template('home.tpl').render(dat)
            home.write(tpl)

        # Output all post html's
        for row in datasite['post']:
            with open(os.path.join(outputdir,row['file']),'w') as page:
                row['image'] = row['image'] if ('image' in row.keys()) else None
                row['content'] = mistune.markdown(row['content']) if ('content' in row.keys()) else None
                dat = {
                    'site_title': datasite['settings']['title'],
                    'categories': datasite['categories'],
                    'post': row
                }
                tpl = tpls.get_template(row['template']).render(dat)
                page.write(tpl)

        # Encode to base64 all images from html's
        if settings['encodedResources']:
            self.encodedResources()


    def encodedResources(self):
        outputdir = self.settings['outputdir']
        html_content = None

        for htmlfile in os.listdir(outputdir):
            htmlfile_path = os.path.join(outputdir,htmlfile)

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
                                node['src'] = self.filetoB64(srcpath)

                        html_content = htmlBS.renderContents()

                with open(htmlfile_path,'w') as write_html:
                    write_html.write(html_content)


    def filetoB64(self,sourcepath=None,raw=False):
        outputdir = self.settings['outputdir']
        fstring = None
        fmime = None
        b64 = None

        if sourcepath is not None:
            sourcepath = os.path.abspath(os.path.join(outputdir,sourcepath))

            if os.path.isfile(sourcepath):
                fmime = mimetypes.MimeTypes().guess_type(sourcepath)[0]
                
                if fmime in (filemimes['text'] + filemimes['image'] + filemimes['audio'] + filemimes['video']):
                    with open(sourcepath,'rb') as f:
                        fcontent = f.read()
                        fstring = base64.encodestring(fcontent).replace('\n','')

                        if raw:
                            b64 = fstring
                        else:
                            b64 = ''.join(['data:',fmime,';base64,',fstring])
                else:
                    b64 = sourcepath
            else:
                b64 = sourcepath

        return b64

