'''
file: nopi.py
author: Michael Watson
github: M-Watson

NOPI is a main script for the unofficial New Orleans Programming Interface.
This will include many sources but is starting with the municode api.

'''
import requests


base_url = 'https://library.municode.com/la/new_orleans'

info_url = 'https://api.municode.com/Products/name?clientId=3524&productName=code of ordinances'

# The 10040 seems to show up in the info url under productid
latest_url = 'https://api.municode.com/Jobs/latest/10040'


# Table of contents side banner
# The Ids are the calls that can be made through CodesContent
toc_url = 'https://api.municode.com/codesToc?jobId=360878&productId=10040'

'''
https://api.municode.com/CodesContent?jobId=360878&nodeId=CD_NEW_ORLEANS_LOUISIANA&productId=10040
https://api.municode.com/CodesContent?jobId=360878&nodeId=SUHITA&productId=10040
https://api.municode.com/CodesChangedDocs?jobId=360878&productId=10040

'''


#Munidocs
munidocs_url = 'https://api.municode.com/Products/name?clientId=3524&productName=munidocs'

'''
https://api.municode.com/munidocsToc?productId=30001
https://api.municode.com/MunidocsContent?isAdvancedSearch=false&productId=30001&searchText=
'''

#minutes
minutes_url = 'https://api.municode.com/MunidocsContent?isAdvancedSearch=false&nodeId=minutes&productId=30001&searchText='

def all_urls():
    urls = {
                'code_changed':'https://api.municode.com/CodesChangedDocs?jobId=360878&productId=10040',
            }

def get_toc():
    toc_response = requests.get(toc_url)
    toc = toc_response.json()
    i = 0
    toc_list = []
    for i in range(len(toc['Children'])):
        toc_list.append(toc['Children'][i]['Id'])
    return(toc_list)

def get_chapter(chapter):
    url = "https://api.municode.com/CodesContent?jobId=360878&nodeId={}&productId=10040".format(chapter)
    chapter_request = requests.get(url)
    chapter_response = chapter_request.json()
    return(chapter_response)

def get_code_change():
    url = 'https://api.municode.com/CodesChangedDocs?jobId=360878&productId=10040'
    cc_request = requests.get(url)
    cc_response = cc_request.json()
