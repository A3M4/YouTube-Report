#!/usr/bin/python3
import math
import os
import re
import subprocess
import sys
from io import BytesIO
from shutil import which

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import pylab as pl
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph
from wordcloud import WordCloud

from parse import HTML

image_dir = os.path.join(os.getcwd(),"Images/")
logo = os.path.join(image_dir,"LOGO.png")
urls = HTML().find_links()
if(len(urls)==0):
    raise ValueError("Could not find any links. Please send the developer your takeout data, so the issue can be addressed")
search_raw, search_clean = HTML().search_history()

try:
    link, all_links = HTML().comment_history()
except TypeError:
    link = all_links = ""

try:
    like, all_likes = HTML().like_history()
except FileNotFoundError:
    like = all_likes = ""


class Visualization:
    def heat_map(self):
        print("Generating Heat Map.....")
        html = HTML()
        Mon = html.dataframe_heatmap(0)
        Tue = html.dataframe_heatmap(1)
        Wed = html.dataframe_heatmap(2)
        Thu = html.dataframe_heatmap(3)
        Fri = html.dataframe_heatmap(4)
        Sat = html.dataframe_heatmap(5)
        Sun = html.dataframe_heatmap(6)
        df = np.vstack((Mon, Tue, Wed, Thu, Fri, Sat, Sun))

        print(df)
        Index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        Cols = [
            "0AM to 2AM",
            "2AM to 4AM",
            "4AM to 6AM",
            "6AM to 8AM",
            "8AM to 10AM",
            "10AM to 12PM",
            "12PM to 2PM",
            "2PM to 4PM",
            "4PM to 6PM",
            "6PM to 8PM",
            "8PM to 10PM",
            "10PM to 12AM",
        ]
        plt.figure(figsize=(20, 5))
        sns.heatmap(df,
                    cmap="Blues",
                    linewidths=2,
                    xticklabels=Cols,
                    yticklabels=Index)

        plt.title("What Time Do You Usually Watch Youtube Videos? (Eastern Standard Time)",
                  fontsize=27,
                  color="steelblue",
                  fontweight="bold",
                  fontname="Arial")

        plt.annotate("             The plot above is based on a total of %s videos you have watched"%(len(HTML().find_links())),
                     (0, 0), (0, -20),
                     fontsize=20,
                     color="steelblue",
                     fontweight="bold",
                     fontname="Arial",
                     xycoords="axes fraction",
                     textcoords="offset points",
                     va="top")

        plt.savefig(os.path.join(image_dir,"week_heatmap.png"), dpi=400)
        plt.clf()

    def table(self):
        plt.figure(figsize=(6, 6))
        plt.title(
            "Do You Still Remember?",
            fontsize=27,
            color="steelblue",
            fontweight="bold",
            fontname="Arial",
        )

        plt.annotate(
            "First Watched Video: \n\nMost Watched Video:\n\nFirst Like"
            "d Video:\n\nFirst Commented Video:\n\nFirst Searched Words:",
            (0, 0),
            (-35, 298),
            fontsize=34,
            color="k",
            fontweight="bold",
            fontname="Arial",
            xycoords="axes fraction",
            textcoords="offset points",
            va="top",
        )
        plt.axis("off")
        plt.savefig(os.path.join(image_dir, "memory.png"), dpi=400)
        plt.clf()

    def wordCloud(self):
        print("Generating Word Cloud.....")
        unique_string = (" ").join(search_clean)
        bg = np.array(Image.open(logo))
        # import nltk.stopwords
        # stopwords.words("english")
        english_stopwords = [
            "i",
            "me",
            "my",
            "myself",
            "we",
            "our",
            "ours",
            "ourselves",
            "you",
            "you're",
            "you've",
            "you'll",
            "you'd",
            "your",
            "yours",
            "yourself",
            "yourselves",
            "he",
            "him",
            "his",
            "himself",
            "she",
            "she's",
            "her",
            "hers",
            "herself",
            "it",
            "it's",
            "its",
            "itself",
            "they",
            "them",
            "their",
            "theirs",
            "themselves",
            "what",
            "which",
            "who",
            "whom",
            "this",
            "that",
            "that'll",
            "these",
            "those",
            "am",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "having",
            "do",
            "does",
            "did",
            "doing",
            "a",
            "an",
            "the",
            "and",
            "but",
            "if",
            "or",
            "because",
            "as",
            "until",
            "while",
            "of",
            "at",
            "by",
            "for",
            "with",
            "about",
            "against",
            "between",
            "into",
            "through",
            "during",
            "before",
            "after",
            "above",
            "below",
            "to",
            "from",
            "up",
            "down",
            "in",
            "out",
            "on",
            "off",
            "over",
            "under",
            "again",
            "further",
            "then",
            "once",
            "here",
            "there",
            "when",
            "where",
            "why",
            "how",
            "all",
            "any",
            "both",
            "each",
            "few",
            "more",
            "most",
            "other",
            "some",
            "such",
            "no",
            "nor",
            "not",
            "only",
            "own",
            "same",
            "so",
            "than",
            "too",
            "very",
            "s",
            "t",
            "can",
            "will",
            "just",
            "don",
            "don't",
            "should",
            "should've",
            "now",
            "d",
            "ll",
            "m",
            "o",
            "re",
            "ve",
            "y",
            "ain",
            "aren",
            "aren't",
            "couldn",
            "couldn't",
            "didn",
            "didn't",
            "doesn",
            "doesn't",
            "hadn",
            "hadn't",
            "hasn",
            "hasn't",
            "haven",
            "haven't",
            "isn",
            "isn't",
            "ma",
            "mightn",
            "mightn't",
            "mustn",
            "mustn't",
            "needn",
            "needn't",
            "shan",
            "shan't",
            "shouldn",
            "shouldn't",
            "wasn",
            "wasn't",
            "weren",
            "weren't",
            "won",
            "won't",
            "wouldn",
            "wouldn't",
        ]

        stop_words = ["porn", "nigga", "pussy"] + english_stopwords
        found=False
        FONTS=("LinBiolinum_R","Arial","arial","DejaVuSansMono")
        for font in FONTS:	#this should fix an error where the font couldn't be found
            try:
                wordcloud = WordCloud(
                    stopwords=stop_words,
                    mask=bg,
                    background_color="white",
                    colormap="Set2",
                    font_path=font,
                    max_words=380,
                    contour_width=2,
                    prefer_horizontal=1,
                ).generate(unique_string)
            except OSError:
                continue
            else:
                found=True
                break
        if not found:
            raise OSError("Could not find any of these fonts: %s"%(FONTS))
        del FONTS
        del found
        
        plt.figure()
        plt.imshow(wordcloud)
        plt.axis("off")
        # plt.savefig("your_file_name"+".png", bbox_inches="tight")
        plt.title("What Do You Usually Search on YouTube?",
                  fontsize=18,
                  color="steelblue",
                  fontweight="bold",
                  fontname="Comic Sans MS")

        plt.annotate("   WordCloud is based on a total of %s search queries"%(str(len(search_clean))),
                     (0, 0), (-10, 10),
                     fontsize=13,
                     color="steelblue",
                     fontweight="bold",
                     fontname="Comic Sans MS",
                     xycoords="axes fraction",
                     textcoords="offset points",
                     va="top")

        plt.savefig(os.path.join(image_dir,"word_cloud.png"), dpi=400)
        plt.clf()

    def bar(self):
        print("Generating Bar Plot.....")
        plt.figure(figsize=(10, 5))
        sns.set(style="white", font_scale=1.5)
        splot = sns.barplot(
            x=[
                len(HTML().find_links()),
                len(search_clean),
                len(all_likes),
                len(all_links),
            ],
            y=["Watch", "Search", "Like", "Comment"],
            palette="Blues",
        )
        for p in splot.patches:
            width = p.get_width()
            splot.text(
                width,
                p.get_y() + p.get_height() / 2 + 0.1,
                "{:1.0f}".format(width),
                ha="left",
            )
        splot.grid(False)
        plt.title("Breakdown of Your Activity on Youtube",
                  fontsize=24,
                  color="steelblue",
                  fontweight="bold",
                  fontname="Comic Sans MS")
        plt.savefig(os.path.join(image_dir,"bar.png"), dpi=400)
        plt.clf()

    def score(self):
        print("Calculating Your Activity Score.....")
        colors = ["#ff3300", "#33cc33"]
        score_value = round(
            math.log(
                (
                    len(urls)
                    + len(search_clean * 2)
                    + len(all_likes * 3)
                    + len(all_links * 4)
                )
                / 9,
                1.12,
            ),
            1,
        )
        x_0 = [1, 0, 0, 0]
        pl.pie([100 - score_value, score_value], autopct="%1.1f%%", startangle=90, colors=colors, pctdistance=10)
        plt.pie(x_0, radius=0.7, colors="w")
        plt.axis("equal")

        plt.title("Your YouTube Activity Score",
                  fontsize=21,
                  color="steelblue",
                  fontweight="bold",
                  fontname="Arial")

        plt.annotate(score_value,
                     (0, 0), (123, 154),
                     fontsize=54,
                     color="teal",
                     fontweight="bold",
                     fontname="Arial",
                     xycoords="axes fraction",
                     textcoords="offset points",
                     va="top")
        plt.savefig(os.path.join(image_dir,"score.png"), dpi=400)
        plt.clf()

    def gen_pdf(self):
        print("Combining Images into PDF.....")
        path1 = os.path.join(image_dir, "week_heatmap.png")
        path2 = os.path.join(image_dir, "memory.png")
        path3 = os.path.join(image_dir, "word_cloud.png")
        path4 = os.path.join(image_dir, "bar.png")
        path5 = os.path.join(image_dir, "score.png")
        path6 = os.path.join(image_dir, "red.png")
        pdf = PdfFileWriter()

        # Using ReportLab Canvas to insert image into PDF
        img_temp = BytesIO()
        img_doc = canvas.Canvas(img_temp, pagesize=(2000, 2300))

        # heat map x, y - start position
        img_doc.drawImage(path1, -150, 1400, width=2600, height=650)
        # memory
        img_doc.drawImage(path2, 1070, 681, width=697, height=667)
        # word_cloud
        img_doc.drawImage(path3, -28, 585, width=1100, height=778)
        # score
        img_doc.drawImage(path5, 1128, -59, width=894, height=672)
        # bar
        img_doc.drawImage(path4, 0, -11, width=1286, height=620)
        # logo
        img_doc.drawImage(logo, 99, 2068, width=105, height=80)
        # red square
        img_doc.drawImage(path6, inch * 24.3, inch * 16.25, width=91, height=45)
        img_doc.drawImage(path6, inch * 24.3, inch * 14.69, width=91, height=45)
        img_doc.drawImage(path6, inch * 24.3, inch * 13.14, width=91, height=45)
        img_doc.drawImage(path6, inch * 24.3, inch * 11.60, width=91, height=45)

        # draw three lines, x,y,width,height
        img_doc.rect(0.83 * inch, 28.5 * inch, 26.0 * inch, 0.04 * inch, fill=1)
        img_doc.rect(0.83 * inch, 18.9 * inch, 26.0 * inch, 0.04 * inch, fill=1)
        img_doc.rect(0.83 * inch, 8.5 * inch, 26.0 * inch, 0.04 * inch, fill=1)
        # title
        img_doc.setFont("Helvetica-Bold", 82)
        img_doc.drawString(
            212, 2078, "Personal YouTube Usage Report",
        )

        # first watch
        print("First watched video: " + urls[-1])
        body_style = ParagraphStyle("Body", fontSize=31)
        items1 = []
        link1 = "<link href=%s>PLAY</link>"%(urls[-1])
        items1.append(Paragraph(link1, body_style))
        f1 = Frame(inch*24.1, inch*14.89, inch*12, inch*2)
        f1.addFromList(items1, img_doc)

        # most watch
        most_watched_url = max(set(urls), key=urls.count)
        print(
            "Most Watched Video ({}x watched): {}".format(
                urls.count(most_watched_url), most_watched_url
            )
        )
        items2 = []
        link2 = "<link href=%s>PLAY</link>"%(max(set(urls), key=urls.count))
        items2.append(Paragraph(link2, body_style))
        f2 = Frame(inch * 24.1, inch * 13.37, inch * 12, inch * 2)
        f2.addFromList(items2, img_doc)

        # first like
        print("First like: " + like)
        items3 = []
        link3 = "<link href=%s>PLAY</link>"%(like)
        items3.append(Paragraph(link3, body_style))
        f3 = Frame(inch * 24.1, inch * 11.85, inch * 12, inch * 2)
        f3.addFromList(items3, img_doc)

        # first comment
        print("First Commented Video: " + link)
        items4 = []
        link4 = "<link href=%s>PLAY</link>"%(link)
        items4.append(Paragraph(link4, body_style))
        f4 = Frame(inch * 24.3, inch * 10.25, inch * 12, inch * 2)
        f4.addFromList(items4, img_doc)

        # first search
        items5 = []
        link5 = "<link href=''>%s</link>"%(re.sub("[^\w\s]", "", str(search_raw[-1])))
        items5.append(Paragraph(link5, body_style))
        f5 = Frame(inch * 23.7, inch * 8.73, inch * 12, inch * 2)
        f5.addFromList(items5, img_doc)

        img_doc.save()
        pdf.addPage(PdfFileReader(BytesIO(img_temp.getvalue())).getPage(0))
        with open("YouTube_Report.pdf","wb") as f:
        	pdf.write(f)
        print("Congratulations! You have successfully created your personal YouTube report!")
        if sys.platform == "win32":
            os.startfile("YouTube_Report.pdf")
        elif sys.platform == "win64":
            os.startfile("YouTube_Report.pdf")
        elif sys.platform == "darwin":
            subprocess.call(["open", "YouTube_Report.pdf"])
        elif which("xdg-open") is not None:
            subprocess.call(["xdg-open", "YouTube_Report.pdf"])
        else:
            print("No opener found for your platform. Just open YouTube_Report.pdf.")

if __name__ == "__main__":
    visual = Visualization()
    visual.heat_map()
    visual.table()
    visual.wordCloud()
    visual.score()
    visual.bar()
    visual.gen_pdf()
