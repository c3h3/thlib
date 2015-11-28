'''
Created on Nov 28, 2015

@author: c3h3
'''

import os
from thlib.dictionary import *
LETTER_IDS = os.environ.get("LETTER_IDS", ",".join(map(str,range(1,31)))).split(",")
LIMIT = int(os.environ.get("LIMIT", 3))


for lid in LETTER_IDS:
    saveLetterTermsHTML(letter_id=lid, limit=LIMIT, update=True)
    
