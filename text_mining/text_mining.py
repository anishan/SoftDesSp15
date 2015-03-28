# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21

@author: Anisha Nakagawa

Text Mining Mini-Project:
Compare objectivity of news articles from different sources
about the same topic.

"""

# Import Packages
# To get html from websites:
from pattern.web import URL, plaintext, strip_between, Google
# For language analysis:
from pattern.en import sentiment
# For graphing
import numpy as np
import matplotlib.pyplot as plt

def get_HTML(website):
    """ Reads in the HTML from a website and removes the HTML formatting

        website: url of website to read
        returns: string of text in document
    """
    # Get html source code
    # These are stored as separate variables for ease of testing
    html = URL(website).download()
    text = html

    # Strings to strip
    # (Each news source has a different format for their HTML)
    general = [('<footer', '</footer>'), ('<nav', '</nav>'), ('<header', '</header>'), ('<a', '</a>'), ('<span', '</span>')]
    bbc = [('<meta', '/>'), ('<div id="most-popular"', '</div>'), ('<li', '</li>'), ('<span', '</span>'), ('<button', '</button>')]
    fox = [('<div id="user-options"', '</span'), ('<div id="subscribe', '</div>'), ('<div class="subscribe', '</div>'), ('<p class="advert-txt">', '</p>')]
    cnn = [('<span', '</span>'), ('<div class="cd__description"', '</div>'), ('<div class="js-el__gallery', '</div>'), ('<div class="el__gallery','</div>')]
    eco = [('<strong','/strong>'), ('<li', '</li>'), ('<div class="title">', '</div>'), ('<div class="about">', '</div>'), ('<div class="product', '</div>')]
    glb = [('<li', '</li>'), ('<span', '</span>'), ('class="bg', '</'), ('<button', '</button>'), ('<div class="fineprint', '</'), ('="email', '</'), ('<div class="tease-text">', '</div>'), ('<div class="paywall', '</div>')]
    npr = [('<div id="commentBlock">', '</div>'), ('<div class="adwrap">', '</div>')]
    usa = [('<li', '</li>'), ('<span', '</span>'), ('class="share','</'), ('class="util','</')]
    yho = [('<li', '</li>'), ('<span', '</span>')]
    
    # Strip specific formatting
    for i in range(len(general)):
        text = strip_between(general[i][0], general[i][1], text)
    if 'bbc' in website:
        for i in range(len(bbc)):
            text = strip_between(bbc[i][0], bbc[i][1], text)
    elif 'fox' in website:
        for i in range(len(fox)):
            text = strip_between(fox[i][0], fox[i][1], text)
    elif 'cnn' in website:
        for i in range(len(cnn)):
            text = strip_between(cnn[i][0], cnn[i][1], text)
    elif 'economist' in website:
        for i in range(len(eco)):
            text = strip_between(eco[i][0], eco[i][1], text)
    elif 'bostonglobe' in website:
        for i in range(len(glb)):
            text = strip_between(glb[i][0], glb[i][1], text)
    elif 'npr' in website:
        for i in range(len(npr)):
            text = strip_between(npr[i][0], npr[i][1], text)
    elif 'usa' in website:
        for i in range(len(usa)):
            text = strip_between(usa[i][0], usa[i][1], text)
    elif 'yahoo' in website:
        for i in range(len(usa)):
            text = strip_between(yho[i][0], yho[i][1], text)

    # Strip general HTML and convert text form
    text = plaintext(text)
    text = text.encode('utf8')
    return text

def save_file(string, filename):
    """ Saves a string to a file

        string: the string to save
        filename: name of the file
        returns: none
    """
    file = open(filename, "w")
    file.write(string)
    file.close()

def save_HTML(websites):
    """ Takes a dictionary of websites and filenames and saves the html
        text from each website to the corresponding filename

        websites: list of website urls
        returns: none
    """
    for title in websites:
        url = websites[title]
        html = get_HTML(url)
        save_file(html, title)

def read_files(filenames):
    """ Takes a list of filenames and returns the contents of the files

        filenames: names of files in the same directory
        returns: dictionary of filenames and strings from files
    """
    contents = dict()
    for f in filenames:
        file = open(f, 'r')
        contents[f] = file.read()
        file.close()
    return contents

def analyze(event, files, color):
    """ Analyzes the text in websites for sentiment and
        plots the articles on a scale of polarity and objectivity

        event: string containing event name
        text: list of filenames to analyze
        color: color of dot to plot, in format 'bo', 'ro', etc,
        following the formatting of matplotlib
        returns: dictionary with filenames as keys, sentiment anaysis tuples
        as values
    """
    analyzed = dict()
    for f in files:
        analyzed[f] = sentiment(files[f])
        plt.plot(analyzed[f][0], analyzed[f][1], color)
        a = plt.annotate(f[3:-4], analyzed[f], textcoords = 'offset points', ha = 'right', va = 'bottom')
        a.draggable()
    plt.title(event)
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    #plt.show()
    return analyzed

####################### MAIN ############################

""" Primary articles, sorted by event, from news sources
    Keys are the filename (containing the website name), values are the urls).

    (I know it is possible to automate this process by using the results
    from a google search instead of hard-coding in the urls. However, I wanted
    to compare the primary article from each news source, not opinion or blog
    posts. Therefore, I wanted to make sure that I am comparing good articles,
    which are not necessarily the first search result.)
"""
# People's Climate March, September 2014
cm_websites = {'cm_Fox.txt': 'http://www.foxnews.com/science/2014/09/19/new-york-set-for-massive-climate-march/',
               'cm_BBC.txt': 'http://www.bbc.com/news/science-environment-29302277',
               'cm_NPR.txt': 'http://www.npr.org/blogs/thetwo-way/2014/09/21/350320021/large-protests-in-hundreds-of-cities-vents-ire-at-climate-change',
               'cm_CNN.txt': 'http://www.cnn.com/2014/09/21/us/new-york-climate-change-march/',
               'cm_The_Economist.txt': 'http://www.economist.com/blogs/economist-explains/2014/09/economist-explains-16',
               'cm_Boston_Globe.txt': 'http://www.bostonglobe.com/news/nation/2014/09/21/thousands-march-new-york-other-cities-about-climate/qCu8tXtcfExa4Fod3hOB7N/story.html',
               'cm_Yahoo.txt': 'http://news.yahoo.com/york-gears-historic-climate-march-155128809.html',
               'cm_USA_Today.txt': 'http://www.usatoday.com/story/news/nation/2014/09/21/nyc-climate-change-march/16008009/',
               }

# State of the Union, January 2015
su_websites = {'su_Fox.txt': 'http://www.foxnews.com/opinion/2015/01/20/state-union-2015-obama-misses-opportunity-with-republican-congress/',
               'su_BBC.txt': 'http://www.bbc.com/news/world-us-canada-30908095',
               'su_NPR.txt': 'http://www.npr.org/blogs/thetwo-way/2015/01/20/378669064/live-blog-president-obama-delivers-2015-state-of-the-union',
               'su_CNN.txt': 'http://www.cnn.com/2015/01/20/politics/state-of-the-union-address-2015-preview/',
               'su_The_Economist.txt': 'http://www.economist.com/news/united-states/21640351-barack-obama-tries-set-tone-2016-middle-class-economics',
               'su_Boston_Globe.txt': 'http://www.bostonglobe.com/news/nation/2015/01/21/state-union-focuses-community-college-tax-relief-family-leave/jKiBxFgooguNyLzzYIJ3SI/story.html',
               'su_Yahoo.txt': 'http://news.yahoo.com/us-state-union-2015-live-report-011035949.html',
               'su_USA_Today.txt': 'http://www.usatoday.com/story/news/2015/01/20/obama-state-of-the-union-republican-senate-mitch-mcconnell/22040331/',
               }

# Keystone Pipeline Veto, February 2015
kp_websites = {'kp_Fox.txt': 'http://www.foxnews.com/politics/2015/02/24/obama-to-usher-in-new-phase-presidency-with-keystone-veto/',
               'kp_BBC.txt': 'http://www.bbc.com/news/world-us-canada-31596580',
               'kp_NPR.txt': 'http://www.npr.org/blogs/thetwo-way/2015/02/24/388738159/obama-to-veto-keystone-xl-pipeline-today-without-drama-or-fanfare-or-delay',
               'kp_CNN.txt': 'http://www.cnn.com/2015/02/24/politics/obama-keystone-veto/',
               'kp_The_Economist.txt': 'http://www.economist.com/blogs/democracyinamerica/2015/02/keystone-xl-and-presidents-veto',
               'kp_Boston_Globe.txt': 'https://www.bostonglobe.com/news/nation/2015/02/25/obama-vetoes-keystone-pipeline-bill/sFYI02m7OsmKyZZfKoB2BK/story.html',
               'kp_Yahoo.txt': 'http://news.yahoo.com/obama-vetoes-canada-us-keystone-oil-pipeline-bill-205404558.html',
               'kp_USA_Today.txt': 'http://www.usatoday.com/story/news/politics/2015/02/24/obama-keystone-veto/23879735/',
               }

""" Use this code to save the website text
    (Only has to be done once)
"""
#save_HTML(cm_websites)
#save_HTML(su_websites)
#save_HTML(kp_websites)


""" Use this code to analyze the websites for sentiment
    Works best if you only run the code for one event at a time
"""
# Climate March:
#cm_text = read_files(cm_websites.keys())
#print analyze("People's Climate March", cm_text, 'go')

# State of the Union
#su_text = read_files(su_websites.keys())
#print analyze('State of the Union', su_text, 'bo')

# Keystone Pipeline Veto
#kp_text = read_files(kp_websites.keys())
#print analyze('Keystone Pipeline Veto', kp_text, 'ro')

#plt.show()

g = Google()
for result in g.search('Olin College'):
    print result.url
    print result.text



