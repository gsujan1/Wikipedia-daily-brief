# Wikipedia-daily-brief
Pulls news and other daily-updated information from Wikipedia's main page

Built using Python 3.7.4

Packages needed:
1. BeautifulSoup4 and Requests for url handling and text extraction
2. Pillow library for image storage, manipulation, and display
  1. run ```sudo apt install python3-pil python3-pil.imagetk```
3. tkinter (standard library in Python)

'getbrief-terminal.py' scrapes data and outputs information to the terminal, as well as opening the image using an image viewer

'getbrief-gui.py' performs same scraping, but ouputs information in a new tkinter window
