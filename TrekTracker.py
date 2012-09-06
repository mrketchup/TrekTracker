'''
Created on Sep 2, 2012

@author: mejones
'''
from TrekData import EpisodeList, Episode
    
if __name__ == '__main__':
    elist = EpisodeList()
    cur = Episode()
    print "Welcome to Trek Tracker!"
    
    kill = False
    
    if not elist.load_list():
        print "Downloading episode list..."
        if not elist.fetch_list():
            print "Unable to download list."
            kill = True
        else:
            cur = elist.episodes[0]
    else:
        cur = elist.episodes[0]
            
    print "(Type 'help' for list of commands)"
    
    while not kill:
        cmd = raw_input('--> ')
        
        if cmd == 'exit' or cmd == 'e':
            kill = True
            
        elif cmd == 'mark' or cmd == 'm':
            cur.seen = True
            elist.episodes.remove(cur)
            cur = elist.episodes[0]
            
        elif cmd == 'next' or cmd == 'n':
            showMax = len('Show')
            titleMax = len('Title')
            starMax = len('Star Date')
            for i in range(1, min(11, len(elist.episodes))):
                if len(elist.episodes[i].show) > showMax:
                    showMax = len(elist.episodes[i].show)
                if len(elist.episodes[i].title) > titleMax:
                    titleMax = len(elist.episodes[i].title)
                if len(elist.episodes[i].star_date) > starMax:
                    starMax = len(elist.episodes[i].star_date)
            print 'Show'.center(showMax), '|',
            print 'Title'.center(titleMax), '|',
            print 'Star Date'.center(starMax)
            print '-'*(showMax+1) + '+' + '-'*(titleMax+2) + '+' + '-'*(starMax+1)
            for i in range(1, min(11, len(elist.episodes))):
                print elist.episodes[i].show.rjust(showMax), '|',
                print elist.episodes[i].title.rjust(titleMax), '|',
                print elist.episodes[i].star_date.rjust(starMax)
            
        elif cmd == 'remaining' or cmd == 'rem' or cmd == 'r':
            print "Remaining:", len(elist.episodes)
            
        elif cmd == 'current' or cmd == 'cur' or cmd == 'c':
            print 'Show:     ', cur.show
            print 'Title:    ', cur.title
            print 'Star Date:', cur.star_date
            
        elif cmd == 'fetch' or cmd == 'f':
            if raw_input("Are you sure? (y/n): ") == 'y':
                print "Downloading episode list..."
                if not elist.fetch_list():
                    print "Unable to download list."
                    kill = True
                else:
                    print "Done!"
                    cur = elist.episodes[0]
                    
        elif cmd == 'load' or cmd == 'l':
            if raw_input("Are you sure? (y/n): ") == 'y':
                if not elist.load_list():
                    print "Unable to load list."
                else:
                    cur = elist.episodes[0]
                    
        elif cmd == 'save' or cmd == 's':
            elist.save_list()
            
        elif cmd == 'help' or cmd == 'h':
            print "List of commands:"
            print "help, h - print this list of commands"
            print "mark, m - mark the current episode as seen"
            print "next, n - list the next 10 episodes"
            print "remaining, rem, r - print the number of episodes remaining"
            print "fetch, f - download and restart the list"
            print "load, l - load the last saved list"
            print "save, s - save the list"
            print "current, cur, c - print the current episode info"
            print "exit, e - exit the program"
            
        else:
            print "Unrecognized command. Type 'help' for list of commands."
