import os, base64, mimetypes
from bs4 import BeautifulSoup
from filemimes import filemimes



# BeautifulSoup
# http://beautiful-soup-4.readthedocs.io/en/latest
# https://www.crummy.com/software/BeautifulSoup/bs4/doc



def _filetoB64 (fpath=None,raw=False):
    fstring = None
    fmime = None
    freturn = None

    if fpath is not None:
        if os.path.isfile(fpath):
            fmime = mimetypes.MimeTypes().guess_type(fpath)[0]
            
            if fmime in (filemimes['text'] + filemimes['image'] + filemimes['audio'] + filemimes['video']):
                with open(fpath,'rb') as f:
                    fcontent = f.read()
                    fstring = base64.encodestring(fcontent).replace('\n','')

                    if raw:
                        freturn = fstring
                    else:
                        freturn = ''.join(['data:',fmime,';base64,',fstring])
            else:
                freturn = fpath
        else:
            freturn = fpath

    return freturn


def _encodesourcesHTML (path=None):
    html_content = None

    if (path is not None) and os.path.isfile(path):
        with open(path,'rt') as read_html:
            html_content = []
            for line in read_html:
                line = line.strip()
                html_content.append(line)
            html_content = '\n'.join(html_content)

            if html_content:
                htmlBS = BeautifulSoup(html_content,'html.parser')

                for node in htmlBS.find_all(['link','script','img']):
                    if node.name == 'link':
                        href = node.get('href')
                        node['href'] = _filetoB64(href)

                    if node.name in ('script','img'):
                        src = node.get('src')
                        node['src'] = _filetoB64(src)

                html_content = htmlBS.renderContents()

        with open(path,'w') as write_html:
            write_html.write(html_content)

_encodesourcesHTML('test.html')

    


