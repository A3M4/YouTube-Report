import sys
import math
import subprocess
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from parse import *
from PIL import Image
from io import BytesIO
from wordcloud import WordCloud
from matplotlib import pylab as pl
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.styles import ParagraphStyle



image_dir = os.getcwd() + "/Images/"
logo = image_dir + "LOGO.png"
urls = HTML().find_links()
searchRaw, searchClean = HTML().searchHistory()

try:
    link, allLinks = HTML().commentHistory()
except TypeError:
    link = allLinks = ''

try:
    like, allLikes = HTML().likeHistory()
except FileNotFoundError:
    like = allLikes = ''


class Visualization:


    def heat_map(self):
        print('Generating Heat Map.....')
        html = HTML()
        Mon = html.dataframe_heatmap('Mon')
        Tue = html.dataframe_heatmap('Tue')
        Wed = html.dataframe_heatmap('Wed')
        Thu = html.dataframe_heatmap('Wed')
        Fri = html.dataframe_heatmap('Fri')
        Sat = html.dataframe_heatmap('Fri')
        Sun = html.dataframe_heatmap('Sun')
        df = np.vstack((Mon, Tue, Wed, Thu, Fri, Sat, Sun))

        print(df)
        Index = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        Cols = ['0AM to 2AM', '2AM to 4AM', '4AM to 6AM', '6AM to 8AM', '8AM to 10AM',  '10AM to 12PM',
                '12PM to 2PM', '2PM to 4PM', '4PM to 6PM', '6PM to 8PM', '8PM to 10PM', '10PM to 12AM', ]
        plt.figure(figsize=(20, 5))
        sns.heatmap(df, cmap='Blues', linewidths=2, xticklabels=Cols,yticklabels=Index)

        plt.title("What Time Do You Usually Watch Youtube Videos? (Eastern Standard Time)",
                  fontsize=26, color='steelblue',fontweight="bold", fontname="Comic Sans MS")

        plt.annotate("             The plot above is based on a total of " +
                     str(len(HTML().find_links())) +" videos you have watched",
                     (0, 0), (0, -20), fontsize=20, color='steelblue', fontweight="bold",
                     fontname="Comic Sans MS", xycoords='axes fraction', textcoords='offset points', va='top')

        plt.savefig(image_dir + 'week_heatmap.png', dpi=400)
        plt.clf()



    def table(self):
        plt.figure(figsize=(6, 6))
        plt.title("Do You Still Remember?",
                  fontsize=27, color='steelblue', fontweight="bold", fontname="Comic Sans MS")

        plt.annotate("First Watched Video:\n\nMost Watched Video:\n\nFirst Like"
                     "d Video:\n\nFirst Commented Video:\n\nFirst Searched Words:",
                     (0, 0), (-35, 298), fontsize=29, color='k', fontweight="bold",
                     fontname="Comic Sans MS", xycoords='axes fraction', textcoords='offset points', va='top')

        plt.axis('off')
        plt.savefig(image_dir + 'memory.png', dpi=400)
        plt.clf()



    def wordCloud(self):
        print('Generating Word Cloud.....')
        unique_string = (" ").join(searchClean)
        bg = np.array(Image.open(logo))

        font = "arial" if sys.platform == "win32" else "DejaVuSansMono" if sys.platform == "linux" else  "Arial"
        wordcloud = WordCloud(mask=bg, background_color="white", colormap='Set2', font_path=font,
                              max_words=380,contour_width=2, prefer_horizontal=1).generate(unique_string)

        plt.figure()
        plt.imshow(wordcloud)
        plt.axis("off")
        # plt.savefig("your_file_name"+".png", bbox_inches='tight')
        plt.title("What Do You Usually Search on YouTube?",
                  fontsize=18, color='steelblue', fontweight="bold", fontname="Comic Sans MS")

        plt.annotate("   WordCloud is based on a total of " +
                      str(len(searchClean)) + " search queries",
                     (0, 0), (-10, 10), fontsize=13, color='steelblue', fontweight="bold",
                     fontname="Comic Sans MS", xycoords='axes fraction', textcoords='offset points', va='top')

        plt.savefig(image_dir + 'word_cloud.png', dpi=400)
        plt.clf()



    def bar(self):
        print('Generating Bar Plot.....')
        plt.figure(figsize=(10, 5))
        sns.set(style='white', font_scale=1.5)
        splot = sns.barplot(
            x=[len(HTML().find_links()), len(searchClean), len(allLikes), len(allLinks)],
            y=['Watch', 'Search', 'Like', 'Comment'], palette="Blues")
        for p in splot.patches:
            width = p.get_width()
            splot.text(width,
                p.get_y() + p.get_height() / 2 + 0.1,
                '{:1.0f}'.format(width),
                ha="left")
        splot.grid(False)
        plt.title("Breakdown of Your Activity on Youtube",
                  fontsize=24, color='steelblue', fontweight="bold", fontname="Comic Sans MS")
        plt.savefig(image_dir + 'bar.png', dpi=400)
        plt.clf()



    def score(self):
        print('Caculating Your Activity Score.....')
        colors = ['#ff3300', '#33cc33']
        scoreValue = round(math.log((len(urls)+len(searchClean*2)+len(allLikes*3)+len(allLinks*4))/9, 1.12), 1)
        x_0 = [1, 0, 0, 0]
        pl.pie([100 - scoreValue, scoreValue], autopct='%1.1f%%', startangle=90, colors=colors, pctdistance=10)
        plt.pie(x_0, radius=0.7, colors='w')
        plt.axis('equal')

        plt.title("Your YouTube Activity Score",
                  fontsize=21, color='steelblue', fontweight="bold", fontname="Comic Sans MS")

        plt.annotate(scoreValue,
                     (0, 0), (115, 154), fontsize=54, color='teal', fontweight="bold",
                     fontname="Comic Sans MS", xycoords='axes fraction', textcoords='offset points', va='top')
        plt.savefig(image_dir + 'score.png', dpi=400)
        plt.clf()



    def gen_pdf(self):
        print('Combining Images into PDF.....')
        path1 = image_dir + 'week_heatmap.png'
        path2 = image_dir + 'memory.png'
        path3 = image_dir + 'word_cloud.png'
        path4 = image_dir + 'bar.png'
        path5 = image_dir + 'score.png'
        path6 = image_dir + 'red.png'
        pdf = PdfFileWriter()

        # Using ReportLab Canvas to insert image into PDF
        imgTemp = BytesIO()
        imgDoc = canvas.Canvas(imgTemp, pagesize=(2000, 2300))


        # heat map x, y - start position
        imgDoc.drawImage(path1, -150, 1400, width=2600,height=650)
        # memory
        imgDoc.drawImage(path2, 1070, 678, width=697, height=667)
        # word_cloud
        imgDoc.drawImage(path3, -28, 592, width=1100, height=767)
        # score
        imgDoc.drawImage(path5, 1128, -57, width=894, height=672)
        # bar
        imgDoc.drawImage(path4, 0, -11, width=1286, height=620)
        # logo
        imgDoc.drawImage(logo, 99, 2068, width=105, height=80)
        # red square
        imgDoc.drawImage(path6, inch * 24.1, inch * 16.25, width=91, height=45)
        imgDoc.drawImage(path6, inch * 24.1, inch * 14.73, width=91, height=45)
        imgDoc.drawImage(path6, inch * 24.1, inch * 13.21, width=91, height=45)
        imgDoc.drawImage(path6, inch * 24.1, inch * 11.69, width=91, height=45)


        # draw three lines, x,y,width,height
        imgDoc.rect(0.83 * inch, 28.5 * inch, 26.0 * inch, 0.04 * inch, fill=1)
        imgDoc.rect(0.83 * inch, 18.9 * inch, 26.0 * inch, 0.04 * inch, fill=1)
        imgDoc.rect(0.83 * inch, 8.5 * inch, 26.0 * inch, 0.04 * inch, fill=1)
        # title
        imgDoc.setFont('Helvetica-Bold', 82)
        imgDoc.drawString(212, 2078, "Personal YouTube Usage Report", )


        # first watch
        bodyStyle = ParagraphStyle('Body', fontSize=31)
        items1 = []
        link1 = '<link href='+urls[-1]+'>PLAY</link>'
        items1.append(Paragraph(link1, bodyStyle))
        f1 = Frame(inch*24.1, inch*14.89, inch*12, inch*2)
        f1.addFromList(items1, imgDoc)

        # most watch
        items2 = []
        link2 = '<link href=' + max(set(urls), key=urls.count) + '>PLAY</link>'
        items2.append(Paragraph(link2, bodyStyle))
        f2 = Frame(inch * 24.1, inch * 13.37, inch * 12, inch * 2)
        f2.addFromList(items2, imgDoc)

        # first like
        items3 = []
        link3 = '<link href=' + like + '>PLAY</link>'
        items3.append(Paragraph(link3, bodyStyle))
        f3 = Frame(inch * 24.1, inch * 11.85, inch * 12, inch * 2)
        f3.addFromList(items3, imgDoc)

        # first comment
        items4 = []
        link4 = '<link href=' + link + '>PLAY</link>'
        items4.append(Paragraph(link4, bodyStyle))
        f4 = Frame(inch * 24.1, inch * 10.32, inch * 12, inch * 2)
        f4.addFromList(items4, imgDoc)

        # first search
        items4 = []
        link4 = '<link href=''>' + str(re.sub('[^\w\s]', '', str(searchRaw[-1]))) + '</link>'
        items4.append(Paragraph(link4, bodyStyle))
        f4 = Frame(inch * 22.7, inch * 8.77, inch * 12, inch * 2)
        f4.addFromList(items4, imgDoc)

        imgDoc.save()
        pdf.addPage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))
        pdf.write(open("YouTube_Report.pdf","wb"))
        print('Congratulations! You have successfully created your personal YouTube report!')
        if sys.platform == "win32":
            os.startfile("YouTube_Report.pdf")
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, "YouTube_Report.pdf"])




if __name__ == "__main__":
    visual = Visualization()
    visual.heat_map()
    visual.table()
    visual.wordCloud()
    visual.score()
    visual.bar()
    visual.gen_pdf()
