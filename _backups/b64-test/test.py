import os
import re
from bs4 import BeautifulSoup
import json
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



# with open('test.html','rt') as file:
#     for line in file:
#         line = line.replace('\n','')
#         print line


# thehtmlstr = '<img src="files/file.png" alt="">'
# thehtmlstr = 'Hello, DoctoR.'

# if re.compile(r"\bd\w*r\b", re.IGNORECASE).search(thehtmlstr) != None:
#     print 'src'



# myHtmlLine = '<img src="files/file.png" alt="">'
# strJunk = '<img src="files/file.png" alt="">'
# match = re.search(r'<img src="?([^">]+)', strJunk)
# matchResult = match.group(1).strip()
# print matchResult

# def replaceSRC (original=None,replace=None):
#     match = re.search(r'<img src="?([^">]+)', original)
#     result = match.group(1).strip()
#     print result

# replaceSRC('<img src="files/file.png" alt="">','data:image/png;base64,PD94bWwgdmVyc2lvbj0i')


# match = re.findall('(\w+)="(.*?)"', myHtmlLine)




myhtml = None

with open('test.html') as htmfile:
    html = BeautifulSoup(htmfile,'html.parser')

    for node in html.find_all(['link','script','img']):
        # print node
        # print node.name
        # print node.get('href')

        if node.name == 'link':
            print node.name, node.get('href')

        if node.name in ('script','img'):
            print node.name, node.get('src')

















