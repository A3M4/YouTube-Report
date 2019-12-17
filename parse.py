import re
import os
import json
import datetime
import itertools
import collections


Dir = os.getcwd() + "/Takeout/YouTube/"
watchHistory = Dir + 'history/watch-history.html'
searchHistory = Dir + 'history/search-history.html'
commentHistory = Dir + 'my-comments/my-comments.html'
likeHistory = Dir + 'playlists/likes.json'



class HTML:

    htmlWatch = open(watchHistory, 'r', encoding='utf-8').read()
    htmlSearch = open(searchHistory, 'r', encoding='utf-8').read()
    try:
        htmlComment = open(commentHistory, 'r', encoding='utf-8').read()
    except: pass

    def find_links(self):
        # search all links based on your personal html file
        links = []
        pattern = re.compile(r'Watched.<.*?>')
        matchList = pattern.findall(str(HTML.htmlWatch))

        # save links into list
        for match in matchList:
            match = match.split('"')[1]
            links.append(match)
        return links



    def find_times(self):
        times = []
        pattern = re.compile(r'(?:[A-Za-z]{3}\s\d{1,2}\,\s[0-9]{4}\,|\d{1,2}\s.{9})\s\d?\d:\d\d:\d\d\s(?:PM\s|AM\s)?[A-Z]{3,4}')
        matchList = pattern.findall(str(HTML.htmlWatch))
 
        # add '0' to the beginning of the string to make all string same length
        for time in matchList:
            if time[0].isalpha():
                if time[6] != ",":
                    time = time[:4] + "0" + time[4:]               
                dayOfWeek = datetime.datetime.strptime(time[0:12], '%b %d, %Y').strftime('%a')
                time = time[:6] + time[7:]
                dt = datetime.datetime.strptime(time[12:24].strip(), "%I:%M:%S %p")
                times.append(time[:13] + dt.strftime("%H:%M:%S") + ' ' + time[-3:] + ' ' + dayOfWeek)
            else:
                if len(time) == 24:
                    time = str(0) + time
                    # add the day of week to the end of strings
                    dayOfWeek = datetime.datetime.strptime(time[0:11], '%d %b %Y').strftime('%a')
                    times.append(time + ' ' + dayOfWeek)
                else:
                    # add the day of week to the end of strings
                    dayOfWeek = datetime.datetime.strptime(time[0:11], '%d %b %Y').strftime('%a')
                    times.append(time + ' ' + dayOfWeek)
        return times



    def searchHistory(self):
        searchRaw = []
        searchClean = []
        pattern = re.compile(r'search_query=[^%].*?>')
        matchList = pattern.findall(str(HTML.htmlSearch))

        # save links into list
        for match in matchList:
            match = match[13:][:-2]
            match = match.split('+')
            searchRaw.append(match)
        for word in list(itertools.chain.from_iterable(searchRaw)):
            if '%' not in word:
                searchClean.append(word)
        return searchRaw, searchClean



    def commentHistory(self):
        try:
            pattern = re.compile(r'<a href=".*?">')
            matchList = pattern.findall(str(HTML.htmlComment))
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
        timeWeeks = []
        daytime = []
        times = self.find_times()
        for time in times:
            timeWeek = time[-3:]+time[13:15]
            timeWeeks.append(timeWeek)
        freq = collections.Counter(timeWeeks)
        for k, v in freq.items():
            if k[0:3] == day:
                daytime.append(str(k)+' '+str(v))
        daytime.sort(key=lambda x: int(str(x)[3:5]))
        print(daytime)

        zero_one = 0
        two_three = 0
        four_five = 0
        six_seven= 0
        eight_nine = 0
        ten_eleven = 0
        twelve_thirteen = 0
        fourteen_fifteen = 0
        sixteen_seventeen = 0
        eighteen_nineteen = 0
        twenty_twentyone = 0
        twentytwo_twentythree = 0

        for i in daytime:
            if int(i[3:5]) in range(0, 2):
                zero_one = zero_one + int(i.split(' ')[1])
            elif int(i[3:5]) in range(2, 4):
                two_three = two_three + int(i.split(' ')[1])
            elif int(i[3:5]) in range(4, 6):
                four_five = four_five + int(i.split(' ')[1])
            elif int(i[3:5]) in range(6, 8):
                six_seven = six_seven + int(i.split(' ')[1])
            elif int(i[3:5]) in range(8, 10):
                eight_nine = eight_nine + int(i.split(' ')[1])
            elif int(i[3:5]) in range(10, 12):
                ten_eleven = ten_eleven + int(i.split(' ')[1])
            elif int(i[3:5]) in range(12, 14):
                twelve_thirteen = twelve_thirteen + int(i.split(' ')[1])
            elif int(i[3:5]) in range(14, 16):
                fourteen_fifteen = fourteen_fifteen + int(i.split(' ')[1])
            elif int(i[3:5]) in range(16, 18):
                sixteen_seventeen = sixteen_seventeen + int(i.split(' ')[1])
            elif int(i[3:5]) in range(18, 20):
                eighteen_nineteen = eighteen_nineteen + int(i.split(' ')[1])
            elif int(i[3:5]) in range(20, 22):
                twenty_twentyone = twenty_twentyone + int(i.split(' ')[1])
            else:
                twentytwo_twentythree = twentytwo_twentythree + int(i.split(' ')[1])

        return ([zero_one, two_three, four_five, six_seven, eight_nine, ten_eleven, twelve_thirteen, fourteen_fifteen,
                 sixteen_seventeen, eighteen_nineteen, twenty_twentyone, twentytwo_twentythree])














