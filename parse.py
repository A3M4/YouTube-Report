#!/usr/bin/python3
import re
import os
import json
import datetime
import collections
import itertools

missing=[]
dir = os.path.join(os.getcwd(),"Takeout/YouTube/")
if not os.path.exists(dir):
	missing.append(dir)
found=False
for path in ('Verlauf/Wiedergabeverlauf.html','history/watch-history.html'):	#translations
	watch_history = os.path.join(dir,path)
	if os.path.exists(watch_history):
		found=True
		break
if not found:
	missing.append(watch_history)
found=False
for path in ('Verlauf/Suchverlauf.html','history/search-history.html'):	#translations
	search_history = os.path.join(dir,path)
	if os.path.exists(search_history):
		found=True
		break
if not found:
	missing.append(search_history)
found=False
for path in ('Meine Kommentare/Meine Kommentare.html','my-comments/my-comments.html'):	#translations
	comments_history = os.path.join(dir,path)
	if os.path.exists(comments_history):
		found=True
		break
if not found:
	missing.append(comments_history)
found=False
for path in ('Playlists/Positive Bewertungen.json','playlists/likes.json'):	#translations
	like_history = os.path.join(dir,path)
	if os.path.exists(like_history):
		found=True
		break
if not found:
	missing.append(like_history)
del found

if len(missing)>0:
	raise OSError("Required directories do not exist: %s"%(missing))
del missing


class HTML:
    with open(watch_history, "r", encoding="utf-8") as f:
        html_watch = f.read()
    with open(search_history, "r", encoding="utf-8") as f:
        html_search = f.read()
    try:
        with open(comment_history, "r", encoding="utf-8") as f:
            html_comment = f.read()
    except Exception:
       print("Could not parse comments.")

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
        matchList = pattern.findall(str(self.html_watch))

        # save links into list
        return [match for match in matchList if type(match)==str]	#just sorting out stuff that could f up the whole script


    def find_times(self):
        times = []
        for translation in (r"""\xa0watched<br><a href=\"[^\"]*\">[^<]*<\/a><br>(\d\d?)\.(\d\d?)\.(\d\d\d\d), (\d\d?):(\d\d?):(\d\d?) ([^<]*)<\/div>""",r"""\xa0angesehen<br><a href=\"[^\"]*\">[^<]*<\/a><br>(\d\d?)\.(\d\d?)\.(\d\d\d\d), (\d\d?):(\d\d?):(\d\d?) ([^<]*)<\/div>"""):
        	times+=self.raw_find_times(translation)
        return times
        
    def raw_find_times(self,translation):
        pattern = re.compile(translation)
        matchList = pattern.findall(str(self.html_watch))
        times=[]
        for time in matchList:
            times.append(datetime.datetime.strptime("%s.%s.%s %s:%s:%s %s"%(time),'%d.%m.%Y %H:%M:%S %Z'))
        return times

    def _find_times(self):
        """
        Find and format times within the HTML file.

        Returns
        -------
        times : List[str]
            e.g. "19 Feb 2013, 11:56:19 UTC Tue"
        """
        # Format all matched dates
        times = [
            datetime_obj.strftime("%d %b %Y, %H:%M:%S UTC %a")
            for datetime_obj in self._find_times_datetime()
        ]
        return times

    def search_history(self):
        search_raw = []
        search_clean = []
        pattern = re.compile(r"search_query=[^%].*?>")
        match_list = pattern.findall(str(HTML.html_search))

        # save links into list
        for match in match_list:
            match = match[13:][:-2]
            match = match.split("+")
            search_raw.append(match)
        for word in list(itertools.chain.from_iterable(search_raw)):
            if "%" not in word:
                search_clean.append(word)
        return search_raw, search_clean

    def comment_history(self):
        try:
            pattern = re.compile(r'<a href=".*?">')
            match_list = pattern.findall(str(HTML.html_comment))
            link = match_list[-1][9:][:-2]
            return link, match_list
        except Exception:
            pass

    def like_history(self):
        with open(like_history, "rb") as f:
            data = json.load(f)
            pattern = re.compile(r"videoId.{15}")
            match_list = pattern.findall(str(data))
            link = r"https://www.youtube.com/watch?v=" + match_list[-1][11:]
            return link, match_list



    def dataframe_heatmap(self, day):
        times = self.find_times()
        watchtimes=[0 for t in range(12)]
        
        for time in times:
        	if time.weekday()==day:
        		watchtimes[(time.hour//2)-time.hour%2]+=1

        return watchtimes



