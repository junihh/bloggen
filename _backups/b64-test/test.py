import os
from bs4 import BeautifulSoup
import base64 
import mimetypes
from filemimes import filemimes



# BeautifulSoup
# http://beautiful-soup-4.readthedocs.io/en/latest
# https://www.crummy.com/software/BeautifulSoup/bs4/doc



def filetoB64 (fpath=None,raw=False):
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



def replaceB64HTML (htmlstr=None):
    if htmlstr is not None:
        html = BeautifulSoup(htmlstr,'html.parser')

        for node in html.find_all(['link','script','img']):
            if node.name == 'link':
                href = node.get('href')
                node['href'] = filetoB64(href)

            if node.name in ('script','img'):
                src = node.get('src')
                node['src'] = filetoB64(src)
        
        return html.renderContents()



with open('test.html','rt') as htmlfile:
    print replaceB64HTML(htmlfile)

    



