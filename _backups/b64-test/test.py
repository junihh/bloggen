import os
import base64 
import mimetypes
from filemimes import filemimes

# https://code.tutsplus.com/tutorials/base64-encoding-and-decoding-using-python--cms-25588
# http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python

def filetoB64 (fpath=None,raw=False):
    fstring = None
    fmime = None
    freturn = None
    mimeok = False

    if fpath is not None:
        if os.path.isfile(fpath):
            fmime = mimetypes.MimeTypes().guess_type(fpath)[0]
            with open(fpath,'rb') as f:
                fcontent = f.read()
                fstring = base64.encodestring(fcontent)

                if fmime in filemimes['text']:
                    mimeok = True
                elif fmime in filemimes['image']:
                    mimeok = True
                elif fmime in filemimes['audio']:
                    mimeok = True
                elif fmime in filemimes['video']:
                    mimeok = True
                else:
                    mimeok = False

                if raw:
                    freturn = fstring
                else: 
                    if mimeok:
                        freturn = ''.join(['data:',fmime,';base64,',fstring])
                    else:
                        freturn = fstring

    return freturn


print filetoB64('./files/file.gif')

