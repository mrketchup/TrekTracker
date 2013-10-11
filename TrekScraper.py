'''
Created on Oct 10, 2013

@author: mejones
'''

from urllib2 import urlopen, Request
import re
import json

class Episode:
    def __init__(self, show):
        self.show = show
        self.showEpisode = '0'
        self.season = '0'
        self.episode = '0'
        self.title = '[TITLE]'
        self.starDate = 'Unknown'
        self.estimatedStarDate = '0000.0'
        self.airDate = '0000-00-00'
        
    def __str__(self):
        return "%s (%s): %s (s%se%s): %s, %s" % (self.show, self.showEpisode,
                                                self.title, self.season,
                                                self.episode, self.starDate,
                                                self.airDate)

reSeasons = re.compile('<h3><span class=.*?</table>')
reEpisodes = re.compile('<tr class="vevent".*?</tr>')
reNumbers = re.compile('<th scope="row" id=".*?" style="text-align: center;.*?">(\d+)</th><td>(\d+)</td>')
reTitleStarDate = re.compile('"<a href=".*?" title=".*?">(.*?)</a>"</td><td>(.*?)</td>')
reAirDate = re.compile('\(<span class=".*?">(.*?)</span>\)')

if __name__ == '__main__':
    request = Request('http://en.wikipedia.org/wiki/List_of_Star_Trek:_The_Original_Series_episodes',
                  headers={'User-Agent': "Magic Browser"})
    response = urlopen(request);
    
    rawHtml = response.read()
    rawHtml = rawHtml.replace('\n', '')
    
    episodes = []
    rawSeasons = re.findall(reSeasons, rawHtml)
    season = 0
    for rawSeason in rawSeasons:
        rawEpisodes = re.findall(reEpisodes, rawSeason)
        for rawEpisode in rawEpisodes:
            episode = Episode('Original Series')
            numbers = re.findall(reNumbers, rawEpisode)
            episode.season = str(season)
            
            if len(numbers) > 0:
                sNum, eNum = numbers[0]
                episode.showEpisode = sNum
                episode.episode = eNum
            
            title, starDate = re.findall(reTitleStarDate, rawEpisode)[0]
            episode.title = title
            episode.starDate = starDate
            
            airDate = re.findall(reAirDate, rawEpisode)
            if len(airDate) > 0:
                episode.airDate = airDate[0]
            
            episodes.append(episode)
        season += 1
    
    with open('original_series.json', 'w') as outfile:
        json.dump(episodes, outfile, indent=4, separators=(',', ': '), default=lambda o: o.__dict__)
    
