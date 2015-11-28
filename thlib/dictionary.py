import requests
from pyquery import PyQuery
import os

DEST_PATH = os.environ.get("DEST_PATH","./TibDict")

if not os.path.exists(DEST_PATH):
    os.mkdir(DEST_PATH)

def getLetterPATH(letter_id):
    letterPATH = os.path.join(DEST_PATH,str(letter_id))
    if not os.path.exists(letterPATH):
        os.mkdir(letterPATH)
    return letterPATH


def getLetterPageURL(letter_id):
    return "http://dictionary.thlib.org/browse?letter={letter_id}".format(letter_id=letter_id)


def listlettersUrls():
    return map(getLetterPageURL,range(1,31))


def getLetterPageMaxOffset(letter_id):
    print "[in getLetterPageMaxOffset] letter_id = ", letter_id
    res = requests.get(getLetterPageURL(letter_id))
    S = PyQuery(res.text)
    lastURL = S("a[id]").map(lambda i,e: "http://dictionary.thlib.org" + PyQuery(e).attr("onclick").split("url:'")[-1].split("'")[0])[-1]
    return int(lastURL.split("offset=")[-1])

def getLetterOffsetPageURL(letter_id, offset):
    return "http://dictionary.thlib.org/internal_definitions/alphabet_sub_list?letter={letter_id}&offset={offset}".format(letter_id=letter_id,offset=offset)


def listAllOffsetURLs(letter_id):
    offsets = range(0,getLetterPageMaxOffset(letter_id),100)
    return [getLetterOffsetPageURL(letter_id,offset) for offset in offsets]
    
    
def getTermIDs(offsetPageURL):
    res = requests.get(offsetPageURL)
    S = PyQuery(res.text)
    termIDs = S(".tib1 a").map(lambda i,e:PyQuery(e).attr("href").split("public_term/")[-1].split("?")[0])
    return termIDs


def listLetterTermIDs(letter_id, limit=10):
    allTermIDs = []
    offsetURLs = listAllOffsetURLs(letter_id)
    if limit>0:
        for url in offsetURLs[:limit]:
            allTermIDs.extend(getTermIDs(url))
    else:
        for url in offsetURLs:
            allTermIDs.extend(getTermIDs(url))
    return allTermIDs



import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def saveTermSourceHTML(term_id, letter_id):
    LPATH = getLetterPATH(letter_id)
    
    url = "http://dictionary.thlib.org/internal_definitions/public_term/{term_id}".format(term_id=term_id) 
    res = requests.get(url)
    S = PyQuery(res.text)
    
    with open(os.path.join(LPATH,term_id),"w") as wf:
        wf.write(S("body").outerHtml())
    
    return os.path.join(LPATH,term_id)


def saveLetterTermsHTML(letter_id, limit=-1, update=True):
#     print "[in saveLetterTermsHTML] letter_id = ", letter_id
    LPATH = getLetterPATH(letter_id)
    termIDs = listLetterTermIDs(letter_id=letter_id,limit=limit)
#     print "[in saveLetterTermsHTML] letter_id = ", letter_id, " / termIDs = ", termIDs
    
    for tid in termIDs:
        print "[in saveLetterTermsHTML] tid = ", tid
        if update:
            if not tid in os.listdir(LPATH):
                print saveTermSourceHTML(tid, letter_id)
                
        else:
            print saveTermSourceHTML(tid, letter_id)
        
