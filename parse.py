#!/usr/bin/python3
import re
import os
import json
import datetime
import itertools
import collections

missing=[]
Dir = os.path.join(os.getcwd(),"Takeout/YouTube/")
if not os.path.exists(Dir):
	missing.append(Dir)
found=False
for path in ('Verlauf/Wiedergabeverlauf.html','history/watch-history.html'):	#translations
	watchHistory = os.path.join(Dir,path)
	if os.path.exists(watchHistory):
		found=True
		break
if not found:
	missing.append(watchHistory)
found=False
for path in ('Verlauf/Suchverlauf.html','history/search-history.html'):	#translations
	searchHistory = os.path.join(Dir,path)
	if os.path.exists(searchHistory):
		found=True
		break
if not found:
	missing.append(searchHistory)
found=False
for path in ('Meine Kommentare/Meine Kommentare.html','my-comments/my-comments.html'):	#translations
	commentsHistory = os.path.join(Dir,path)
	if os.path.exists(commentsHistory):
		found=True
		break
if not found:
	missing.append(commentsHistory)
found=False
for path in ('Playlists/Positive Bewertungen.json','playlists/likes.json'):	#translations
	likeHistory = os.path.join(Dir,path)
	if os.path.exists(likeHistory):
		found=True
		break
if not found:
	missing.append(likeHistory)
del found

if len(missing)>0:
	raise OSError("Required directories do not exist: %s"%(missing))


class HTML:
    with open(watchHistory, 'r', encoding='utf-8') as f:
        htmlWatch = f.read()
    with open(searchHistory, 'r', encoding='utf-8') as f:
        htmlSearch = f.read()
    try:
        with open(commentHistory, 'r', encoding='utf-8') as f:
            htmlComment = f.read()
    except: pass

    def find_links(self):
        # search all links based on your personal html file
        links = []
        #if you want to understand ↓these↓, go to regex101.com.
        #also, I just assumed that the previously written english regex was faulty too, but replace that one if needed. I've only got the german one on hand.
        for translation in (r"""<a href=\"([^\"]*)\">[^<]*<\/a>\xa0watched""",r"""<a href=\"([^\"]*)\">[^<]*<\/a>\xa0angesehen"""):
            links+=self.raw_find_links(translation)
        return links
    def raw_find_links(self,translation):
        pattern = re.compile(translation)
        matchList = pattern.findall(str(self.htmlWatch))

        # save links into list
        return [match for match in matchList if type(match)==str]	#just sorting out stuff that could f up the whole script


    def find_times(self):
        times = []
        for translation in (r"""\xa0watched<br><a href=\"[^\"]*\">[^<]*<\/a><br>(\d\d?)\.(\d\d?)\.(\d\d\d\d), (\d\d?):(\d\d?):(\d\d?) ([^<]*)<\/div>""",r"""\xa0angesehen<br><a href=\"[^\"]*\">[^<]*<\/a><br>(\d\d?)\.(\d\d?)\.(\d\d\d\d), (\d\d?):(\d\d?):(\d\d?) ([^<]*)<\/div>"""):
        	times+=self.raw_find_times(translation)
        return times
        
    def raw_find_times(self,translation):
        pattern = re.compile(translation)
        matchList = pattern.findall(str(self.htmlWatch))
        times=[]
        # add '0' to the beginning of the string to make all string same length
        for time in matchList:
            times.append(datetime.datetime.strptime("%s.%s.%s %s:%s:%s %s"%(time),'%d.%m.%Y %H:%M:%S %Z'))
        return times


    def searchHistory(self):
        searchRaw = []
        searchClean = []
        pattern = re.compile(r'search_query=[^%].*?>')
        matchList = pattern.findall(str(self.htmlSearch))

        # save links into list
        for match in matchList:
            match = match[13:][:-3]
            match = match.split('+')
            searchRaw.append(match)
        for word in list(itertools.chain.from_iterable(searchRaw)):
            if '%' not in word:
                searchClean.append(word)
        return searchRaw, searchClean



    def commentHistory(self):
        try:
            pattern = re.compile(r'<a href=".*?">')
            matchList = pattern.findall(str(self.htmlComment))
            link = matchList[-1][9:][:-2]
            return link, matchList
        except:
            pass



    def likeHistory(self):
        with open(likeHistory, 'rb') as f:
            data = json.load(f)
            pattern = re.compile(r'videoId.{15}')
            matchList = pattern.findall(str(data))
            link = r"https://www.youtube.com/watch?v=" + matchList[-1][11:]
            return link, matchList



    def dataframe_heatmap(self,day):
        times = self.find_times()
        watchtimes=[0 for t in range(12)]
        
        for time in times:
        	if time.weekday()==day:
        		watchtimes[(time.hour//2)-time.hour%2]+=1

        return watchtimes



