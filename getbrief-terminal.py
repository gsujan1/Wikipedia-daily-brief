from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
from PIL import Image

#load in url
url = 'https://en.wikipedia.org/wiki/Main_Page'
source = requests.get(url)

# loads in necessary html blocks
only_featured_article = SoupStrainer(id='mp-tfa')
only_did_you_know = SoupStrainer(id='mp-dyk')
only_news = SoupStrainer(id='mp-itn')
# # uncomment line below to get special events on today's date
# only_on_this_day = SoupStrainer(id='mp-otd')
only_featured_pic = SoupStrainer(id='mp-lower')

# parse necessary information from Wikipedia's main page
soup_featured_article = BeautifulSoup(source.content, 'lxml', parse_only = only_featured_article)
soup_did_you_know = BeautifulSoup(source.content, 'lxml', parse_only = only_did_you_know)
soup_news = BeautifulSoup(source.content, 'lxml', parse_only = only_news)
# # uncomment line below to get special events on today's date
# soup_on_this_day = BeautifulSoup(source.content, 'lxml', parse_only = only_on_this_day)
soup_featured_pic = BeautifulSoup(source.content, 'lxml', parse_only = only_featured_pic)

######################### FEATURED ARTICLE ######################################
featured_article = ''

for string in soup_featured_article.stripped_strings:
    featured_article = featured_article + string + ' '

splitter_featured_article = '( Full'
featured_article = featured_article.split(splitter_featured_article, 1)[0]

featured_article = featured_article.replace(' . ', '. ')
featured_article = featured_article.replace(' , ', ', ')

print("TODAY'S FEATURED ARTICLE : ")
print(str(featured_article))
print(' ')

######################### DID YOU KNOW ##########################
did_you_know = ''

list_did_you_know = iter(soup_did_you_know.stripped_strings)
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

print('DID YOU KNOW ?')
print(str(did_you_know))
print(' ')

######################### IN THE NEWS #######################################
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

print('IN THE NEWS :')
print(str(in_the_news))
print(' ')

################################################################################
# I don't need this information, it's not useful/interesting for me
# but one can uncomment this section to get unformatted text from this section
# ######################### ON THIS DAY ########################################
# on_this_day = ''

# for string in soup_on_this_day.stripped_strings:
#     on_this_day = on_this_day + string + ' '

# splitter_today = 'More anniversaries'
# on_this_day = on_this_day.split(splitter_today, 1)[0]

# print('ON THIS DAY : ')
# print(str(on_this_day))
# print(' ')

########################## TODAY'S PICTURE ######################################
# prints text for featured text
featured_pic = ''
for string in soup_featured_pic.stripped_strings:
    featured_pic = featured_pic + string + ' '

splitter_pic = 'Photograph credit'
featured_pic = featured_pic.split(splitter_pic, 1)[0]

featured_pic = featured_pic.replace(' . ', '. ')
featured_pic = featured_pic.replace(' , ', ', ')

print("TODAY'S PICTURE:")
print(str(featured_pic))

# creating link from wikipedia source,
# downloading image and saving it in folder
image = soup_featured_pic.img
link = image['src']

link = link.replace('thumb/', '')

link = '/'.join(link.split('/')[:8])

link = 'https:' + link

img_url = str(link)
img_request = requests.get(img_url)
open('current_wiki_img', 'wb').write(img_request.content)

img = Image.open('current_wiki_img')
img = img.resize((550,450))
img.show()
