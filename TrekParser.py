'''
Created on Sep 2, 2012

@author: mejones
'''
from HTMLParser import HTMLParser
import urllib

BASE_URL = "http://www.tiler.com/StarTrek/"
SHOW_NAMES = {'images/ENT_label.gif': 'Enterprise',
              'images/TAS_label.gif': 'The Animated Series',
              'images/TOS_label.gif': 'The Original Series',
              'images/MOV_label.gif': 'Movie',
              'images/TNG_label.gif': 'The Next Generation',
              'images/DS9_label.gif': 'Deep Space 9',
              'images/VOY_label.gif': 'Voyager'}

class MainParser(HTMLParser):
    
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.top = None
        self.list = None
        f = urllib.urlopen(BASE_URL + url)
        self.feed(f.read())
    
    def handle_starttag(self, tag, attrs):
        if tag == 'frame':
            name = ''
            for k, v in attrs:
                if k == 'name':
                    name = v
                elif k == 'src':
                    if name == 'top':
                        self.top = TopParser(v)
                    elif name == 'list':
                        self.list = ListParser(v)
    

class TopParser(HTMLParser):
    
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.next = None
        f = urllib.urlopen(BASE_URL + url)
        self.feed(f.read())
        
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for k, v in attrs:
                if k == 'href':
                    self.curLink = v
                    
    def handle_data(self, data):
        if data == 'Next Season':
            self.next = self.curLink
        

class ListParser(HTMLParser):
    
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.next = None
        self.curData = ''
        self.curEpisode = None
        self.episodes = []
        f = urllib.urlopen(BASE_URL + url)
        self.feed(f.read())
        for e in self.episodes:
            if e.title == '':
                self.episodes.remove(e)
        self.episodes.pop()
        
    def handle_starttag(self, tag, attrs):
        from TrekData import Episode
        self.curData = ''
        if tag == 'tr':
            self.curEpisode = Episode()
        elif tag == 'img':
            for k, v in attrs:
                if k == 'src':
                    self.curEpisode.show = SHOW_NAMES[v]
                    
    def handle_endtag(self, tag):
        if tag == 'a':
            self.curEpisode.star_date = self.curData
        elif tag == 'b':
            self.curEpisode.title = self.curData
        elif tag == 'tr':
            self.episodes.append(self.curEpisode)
        
    def handle_data(self, data):
        self.curData = self.curData + data
        self.curData = self.curData.strip()
