'''
Created on Sep 2, 2012

@author: mejones
'''
from TrekParser import MainParser

class Episode(object):
    
    def __init__(self):
        self.show = ''
        self.star_date = ''
        self.title = ''
        self.seen = False
    
    
class EpisodeList(object):
    
    def __init__(self):
        self.episodes = []
        
    def fetch_list(self):
        try:
            self.episodes = []
            parser = MainParser("dynamic_frames.php?sid=21")
            self.episodes.extend(parser.list.episodes)
            page = 1
            while not parser.top.next == None:
                page += 1
                parser = MainParser(parser.top.next)
                self.episodes.extend(parser.list.episodes)
            movieX = Episode()
            movieX.show = 'Movie'
            movieX.star_date = '56844.9'
            movieX.title = 'Star Trek X: Nemesis'
            self.episodes.append(movieX)
            return True
        except IOError:
            return False
        
    def save_list(self):
        f = open('episode_list', 'w')
        for e in self.episodes:
            if not e.seen:
                f.write(e.show + '|')
                f.write(e.star_date + '|')
                f.write(e.title + '\n')
        f.close()
        
    def load_list(self):
        try:
            self.episodes = []
            f = open('episode_list', 'r')
            for line in f:
                info = line.strip().split('|')
                e = Episode()
                e.show = info[0]
                e.star_date = info[1]
                e.title = info[2]
                self.episodes.append(e)
            return True
        except IOError:
            return False
        