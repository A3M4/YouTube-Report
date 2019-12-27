import collections
import itertools
import json
import os
import re

from dateutil import parser

dir = os.getcwd() + "/Takeout/YouTube/"
watch_history = dir + "history/watch-history.html"
search_history = dir + "history/search-history.html"
comment_history = dir + "my-comments/my-comments.html"
like_history = dir + "playlists/likes.json"


class HTML:
    html_watch = open(watch_history, "r", encoding="utf-8").read()
    html_search = open(search_history, "r", encoding="utf-8").read()
    try:
        html_comment = open(comment_history, "r", encoding="utf-8").read()
    except Exception:
        print("Could not parse comments.")

    def find_links(self):
        # search all links based on your personal html file
        links = []
        pattern = re.compile(r"Watched.<.*?>")
        match_list = pattern.findall(str(HTML.html_watch))

        # save links into list
        for match in match_list:
            match = match.split('"')[1]
            links.append(match)
        return links

    def _find_times_datetime(self):
        # Match any kind of date format
        pattern = re.compile(r"(?<=<br>)([^>]*)(?=</div><div )")
        match_list = pattern.findall(str(HTML.html_watch))

        # parser recognize any kind of date format
        times = [parser.parse(time) for time in match_list]
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
        """
        For the given day, count how many events happened in the time buckets.

        Parameters
        ----------
        day : {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}

        Returns
        -------
        bucketed_event_counts : List[int]
        """
        # Get the correct day
        times = self._find_times_datetime()
        times = [
            datetime_obj for datetime_obj in times if datetime_obj.strftime("%a") == day
        ]

        # Get the bucket counts
        bucketed_event_counts = [0 for _ in range(12)]
        for datetime_obj in times:
            bucketed_event_counts[datetime_obj.hour // 2] += 1
        return bucketed_event_counts
