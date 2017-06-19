# -*- coding: utf-8 -*-

import os, sys, hashlib, json, base64, mimetypes, re, datetime, time
from bs4 import BeautifulSoup
import mistune
import yaml
import jinja2 as jinja
from filemimes import filemimes


# -------------------------------------
# Bloggen class 
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
        if 'embeddedResources' not in settingsKeys:
            settings['embeddedResources'] = True
        if 'onlyJSON' not in settingsKeys:
            settings['onlyJSON'] = False
        self.settings = settings
        postdir = settings['postdir']

        if not os.path.exists(postdir):
            os.makedirs(postdir)

        for yml in os.listdir(postdir):
            yml_path = os.path.join(postdir,yml)
            
            if os.path.isfile(yml_path):
                yml_nam, yml_ext = os.path.splitext(yml)
                
                if yml_ext in ('.md','.markdown','.mdown','.mkdn','.mkd','.mdwn','.mdtxt','.mdtext','.text','.txt','.yml','.yaml','.yamel'):
                    html = self.slugify(yml_nam) + '.html'

                    with open(yml_path,'rt') as ymlfile:
                        yml_content = ymlfile.read()
                        content = str(yml_content).split('======================================================')
                        config = yaml.load(content[0])

                        config['file'] = html
                        config['id'] = hashlib.sha1(html).hexdigest()
                        config['permalink'] = ''.join(['http://', settings['domain'], '/', html])
                        config['content'] = content[1].strip()

                        configKeys = config.keys()

                        if 'category' in configKeys:
                            categories.append(config['category'])

                        if 'date' in configKeys:
                            dte = config['date'].strftime('%Y-%m-%d').split('-')
                            dte = datetime.datetime(int(dte[0]),int(dte[1]),int(dte[2]))
                            config['date'] = str(dte)
                        else:
                            config['date'] = str(time.strftime('%Y-%m-%d %H:%M:%S'))
                        
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
            print 'BLOGGEN [OK]: "' + settings['site_title'] + '" is ready.'
        else:
            print 'BLOGGEN [WARNING]: None post available. Write some and save it into the "' + os.path.realpath(postdir) + '" directory.'


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

        # Make the website html
        if settings['onlyJSON'] != True:
            # Remove all *.html files inside the output directory
            for html in os.listdir(outputdir):
                html_path = os.path.join(outputdir,html)
                if os.path.isfile(html_path) and html.endswith('.html'):
                    os.remove(html_path)

            # Output index.html
            with open(os.path.join(outputdir,'index.html'),'w') as home:
                dat = dict(
                    site_title = datasite['settings']['title'],
                    categories = datasite['categories'],
                    rows = datasite['post']
                )
                tpl = tpls.get_template('home.tpl').render(dat)

                if settings['embeddedResources']:
                    tpl = self.embeddedResources(tpl)

                home.write(tpl)

            # Output all post html
            for row in datasite['post']:
                dat = dict(
                    site_title = datasite['settings']['title'],
                    categories = datasite['categories'],
                    post = row
                )
                tpl = tpls.get_template(row['template']).render(dat)

                if settings['embeddedResources']:
                    tpl = self.embeddedResources(tpl)

                with open(os.path.join(outputdir,row['file']),'w') as page:
                    page.write(tpl)


    def embeddedResources(self,html=None):
        outputdir = self.settings['outputdir']
        htmlret = None

        if html is not None:
            htmlBS = '<pre>' + html.strip() + '</pre>'
            htmlBS = BeautifulSoup(htmlBS,'html.parser')

            for node in htmlBS.find_all(['img','link','script']):
                path = None

                if node.name == 'img':
                    src = node.get('src').strip()
                    path = os.path.join(outputdir,src)

                    if os.path.isfile(path):
                        node['src'] = self.filetoB64(src)

                if node.name == 'link':
                    href = node.get('href').strip()
                    path = os.path.join(outputdir,href)
                    rel = ','.join(node.get('rel')).lower()

                    if 'stylesheet' in rel:
                        if os.path.isfile(path):
                            with open(path,'rt') as f:
                                styles = '\n' + str(f.read())
                                node.extract()

                                new_style = htmlBS.new_tag('style')
                                new_style.append(styles)
                                htmlBS.head.append(new_style)

                    if 'icon' in rel:
                        if os.path.isfile(path):
                            node['href'] = self.filetoB64(href)

                if node.name == 'script':
                    src = node.get('src')

                    if src:
                        src = src.strip()
                        path = os.path.join(outputdir,src)

                        if os.path.isfile(path):
                            with open(path,'rt') as f:
                                jscript = '\n' + str(f.read())
                                node.append(jscript)
                                del node['src']

            genmeta = htmlBS.new_tag('meta')
            genmeta['name'] = 'generator'
            genmeta['content'] = 'bloggen'
            htmlBS.head.append(genmeta)

            htmlret = str(htmlBS.renderContents())[5:][:-6]

        return htmlret


    def filetoB64(self,sourcepath=None,raw=False):
        outputdir = self.settings['outputdir']
        fstring = None
        fmime = None
        b64 = None

        if sourcepath is not None:
            sourcepath = os.path.realpath(os.path.join(outputdir,sourcepath))

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


    def parseMD(self,mdstr=None):
        html = mdstr

        if mdstr is not None:
            mdstr = mdstr.strip()
            html = mistune.markdown(mdstr)

        return html


    def slugify(self,name=None):
        s = name

        if name is not None:
            s = name.lower()
            
            s = re.sub('á|à|â|ã|ä|å|ā|æ', 'a', s);
            s = re.sub('é|è|ê|ë|ē|ę', 'e', s);
            s = re.sub('í|î|ï|ī', 'i', s);
            s = re.sub('ó|õ|ô|ö|ő|ō|ø|œ', 'o', s);
            s = re.sub('ú|ü|û|ů|ű|ŭ|ū', 'u', s);

            s = re.sub('ç|č|ĉ|ć', 'c', s);
            s = re.sub('š|ŝ|ś|ş', 's', s);
            s = re.sub('ÿ|ý|ŷ', 'y', s);
            s = re.sub('ž|ź|ż', 'z', s);
            s = re.sub('ţ|ț', 't', s);
            s = re.sub('ñ|ň', 'n', s);
            s = re.sub('ř', 'r', s);
            s = re.sub('ĵ', 'j', s);
            s = re.sub('ğ', 'g', s);
            s = re.sub('ŵ', 'w', s);
            s = re.sub('ß', 'b', s);

            s = re.sub('([^\s\w]|_)+', '', s);
            s = re.sub('(\r\n|\n|\r|\s+)', '-', s);

        return s


    def humanizedDate(self,date=None):
        months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        if date is not None:
            date = date.split(' ')[0].split('-')
            month = months[int(date[1])-1]

            return ''.join([month,' ',date[2],', ',date[0]])


# -------------------------------------
# Setup
# -------------------------------------

reload(sys)  
sys.setdefaultencoding('utf8')

templates_dir = '../templates'
tpls = jinja.Environment(
    loader = jinja.PackageLoader('bloggenmod',templates_dir)
)
tpls.filters = dict(
    parsemd = Bloggen().parseMD,
    slugify = Bloggen().slugify,
    humanizeddate = Bloggen().humanizedDate
)


