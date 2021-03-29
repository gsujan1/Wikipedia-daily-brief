from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
from tkinter import Tk, Label, Frame, Grid
from PIL import ImageTk,Image

###################### SCRAPING STUFF ############################
#load in url and parse necessary information from wikipedia
url = 'https://en.wikipedia.org/wiki/Main_Page'
source = requests.get(url)

only_featured_article = SoupStrainer(id='mp-tfa')
only_did_you_know = SoupStrainer(id='mp-dyk')
only_news = SoupStrainer(id='mp-itn')
only_featured_pic = SoupStrainer(id='mp-lower')

soup_featured_article = BeautifulSoup(source.content, 'lxml', parse_only = only_featured_article)
soup_did_you_know = BeautifulSoup(source.content, 'lxml', parse_only = only_did_you_know)
soup_news = BeautifulSoup(source.content, 'lxml', parse_only = only_news)
soup_featured_pic = BeautifulSoup(source.content, 'lxml', parse_only = only_featured_pic)

######################### FEATURED ARTICLE ################################
featured_article = ''   

list_featured_article = iter(soup_featured_article.stripped_strings)
next(list_featured_article)

for string in list_featured_article:
    featured_article = featured_article + string + ' '

splitter_featured_article = '( Full'
featured_article = featured_article.split(splitter_featured_article, 1)[0]

featured_article = featured_article.replace(' . ', '. ')
featured_article = featured_article.replace(' , ', ', ')

######################### DID YOU KNOW ##########################
did_you_know = ''

list_did_you_know = iter(soup_did_you_know.stripped_strings)
next(list_did_you_know)
next(list_did_you_know)

for string in list_did_you_know:
    did_you_know = did_you_know + string + ' '

splitter_did_you_know = 'Archive Start'
did_you_know = did_you_know.split(splitter_did_you_know, 1)[0]

# probably some very inefficient cleaning to make text more readable
did_you_know = did_you_know.replace(' ? ... ', '?\n')
did_you_know = did_you_know.replace('... ', '')
did_you_know = did_you_know.replace(' ... ', '\n')
did_you_know = did_you_know.replace(' , ', ', ')
did_you_know = did_you_know.replace('? ', '?\n')
did_you_know = did_you_know.replace('that', 'THAT')

######################### IN THE NEWS ################################
in_the_news = ''

list_in_the_news = iter(soup_news.stripped_strings)
next(list_in_the_news)
for string in list_in_the_news:
    in_the_news = in_the_news + string + ' '

splitter_news = 'Recent deaths'
in_the_news = in_the_news.split(splitter_news, 1)[0]

# also probably very inefficient
in_the_news = in_the_news.replace(' . ', '.')
in_the_news = in_the_news.replace(' , ', ', ')
in_the_news = in_the_news.replace('.', '\n')

########################## TODAY'S PICTURE ###############################
# prints text for featured text
featured_pic = ''
for string in soup_featured_pic.stripped_strings:
    featured_pic = featured_pic + string + ' '

splitter_pic = 'Recently featured'
featured_pic = featured_pic.split(splitter_pic, 1)[0]

featured_pic = featured_pic.replace(' . ', '. ')
featured_pic = featured_pic.replace(' , ', ', ')

####################### IMAGE STUFF ##############################
# creating link from wikipedia source,
# downloading image and saving it in folder
image = soup_featured_pic.img
link = image['src']

link = link.replace('thumb/', '')

link = '/'.join(link.split('/')[:8])

link = 'https:' + link

img_url = str(link)
img_request = requests.get(img_url)
open('current_wiki_img.png', 'wb').write(img_request.content)

####################### GUI STUFF ################################
img = Image.open("current_wiki_img.png")
img_resize = img.resize((600, 450), Image.ANTIALIAS)

root = Tk()
root.title("Wikipedia's Daily Brief")
root.configure(background='black')
root.minsize(width=1400, height=800)

root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(2, weight=1)

top1 = Label(root, text = "TODAY'S FEATURED ARTICLE / PICTURE:", bg="black", font=('Courier 18 bold'))
top2 = Label(root, text = featured_article, wraplength=500, bg="black", font=('Helvetica', 10))

left1 = Label(root, text = "DID YOU KNOW...", wraplength=400, bg="black", font=('Courier 18 bold'))
left2 = Label(root, text = did_you_know, wraplength=400, justify='left', bg="black", font=('Helvetica', 10))

right1 = Label(root, text = "IN THE NEWS:", wraplength=400, bg="black", font=('Courier 18 bold'))
right2 = Label(root, text = in_the_news, wraplength=400, justify='right', bg="black", font=('Helvetica', 10))

import_img = ImageTk.PhotoImage(img_resize)
bot1 = Label(root, image=import_img)
bot2 = Label(root, text = featured_pic, wraplength=500, bg="black", font=('Helvetica', 10))

top1.grid(row=0, column=1)
top2.grid(row=1, column=1)

left1.grid(row=0, column=0)
left2.grid(row=1, rowspan=2, column=0)

right1.grid(row=0, column=2)
right2.grid(row=0, rowspan=2, column=2)

bot1.grid(row=3, column=1)
bot2.grid(row=2, column=1)

root.mainloop()  
