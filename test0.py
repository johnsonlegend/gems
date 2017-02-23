# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 22:43:09 2017

@author: johnson
"""

import urllib  
import urllib2
import re

def extract_paper(content):
    pattern = re.compile('gsc_title">.*?data-clk.*?">(.*?)</a>.*?gsc_field">Authors.*?gsc_value">(.*?)</div>.*?gsc_field">Publication date.*?gsc_value">(.*?)</div>.*?gsc_field">Total citations.*?>Cited by (.*?)</a>', re.S)
    items = re.findall(pattern, content)
    for item in items:
        print("Title: " + item[0])
        print("Authors: " + item[1])
        print("Publication date: " + item[2])
        print("Citations: " + item[3])
    return items
        

def extract_person(content):
    pattern = re.compile('publications.\'>Citations</a>.*?std">(.*?)</td>.*?\'>h-index</a>.*?std">(.*?)</td>.*?\'>i10-index</a>.*?std">(.*?)</td>', re.S)
    items = re.findall(pattern, content)
#    print(items.group())
    for item in items:
        print("Aggregate Citations: " + item[0])
        print("h-index: " + item[1])
        print("i10-index: " + item[2])
#        print("Number of publications: " + item[3])
    return items    
        

def get_papers(content):
    pattern = re.compile('gsc_a_tr\">.*?href="/(.*?)" ', re.S)
    items = re.findall(pattern, content)
#    for item in items:
#        print(item)
    return items


def get_response(url):
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'  
#    values = {'username' : 'xxxx',  'password' : 'XXXX' }  
    headers = { 'User-Agent' : user_agent }  
    data = urllib.urlencode(headers)
    try:
        request = urllib2.Request(url, data)  
        response = urllib2.urlopen(request)  
        page = response.read().decode('utf-8','ignore')
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    return page
        
        
def main(start):     
    url = 'https://scholar.google.com/'
    person_page = get_response(url + start)
    
    
    """===== Extract Person ====="""
    extract_person(person_page)
    
    """===== Get Papers ====="""
    papers = get_papers(person_page)    
    
    """===== Extract Paper ====="""
    for paper_url in papers:
#        print((url + paper_url).replace('amp;',''))
        paper_page = get_response((url + paper_url).replace('amp;',''))
        extract_paper(paper_page)
        print('\n')
    
    

    f = open('result.txt', 'w')
    f.write(person_page)
    f.close()    
#    
#    print (person_page)
    
if __name__ == '__main__':
  main('citations?user=fmSHtE8AAAAJ&hl=en')