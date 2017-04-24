#!/usr/bin/env python3
import urllib
import os
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup

site = "http://midi.midicn.com"
spidered = []

def spider(url):
    if(url[-1] == '/'):
        url = url[0:-1] # get rid of trailing /
    if(url in spidered):
        return
    else:
        spidered.append(url)
    print('Processing webpage %s' % request.unquote(url))
    try:
        req = request.urlopen(url+'/')
    except urllib.error.HTTPError as e:
        print("HTTP Error: %s" % e.reason)
        return
    output = req.read().decode('utf-8')
    soup = BeautifulSoup(output, 'lxml')
    # find links
    links = soup.find_all('a')
    tospider = []
    for link in links:
        link = link.get('href')
        try:
            if(link[0] == '/'):
                link = site + link
            if(link[0] == '#'):
                continue
            if(link[-4:] == '.mid'):
                print('Downloading MIDI file %s' % request.unquote(link))
                path = link[28:]
                try:
                    os.makedirs(os.path.dirname(path))
                except:
                    pass
                request.urlretrieve(link, path)
            elif(link[-4:] == '.zip'):
                path = link[28:]
                print('Downloading ZIP file %s' % request.unquote(link))
                try:
                    os.makedirs(os.path.dirname(path))
                except:
                    pass
                request.urlretrieve(link, path)
            else:
                tospider.append(link)
        except:
            pass
    print("Webpage %s finished" % request.unquote(url))
    for link in tospider:
        try:
            spider(link)
        except:
            pass

spider(site)
