import urllib2
import simplejson
import random


def randomImage(searchTerm):
    """
    Returns the URL of a random image from google
    image search based on the search term
    """
    fetcher = urllib2.build_opener()
    searchTerm = searchTerm.replace(' ', '+').encode("utf-8")
    randomizer = random.randrange(1, 20)
    searchUrl = "https://www.googleapis.com/customsearch/v1?q="+searchTerm+"&cx=+011209494308152849851%3Az4ka7vstowm&imgSize=large&imgType=photo&num=1&safe=medium&searchType=image&start="+str(randomizer)+"&key=AIzaSyD9kcUCZztzrT3WyjyJpNT7vmNcXwqIeQ4"  # NOQA
    f = fetcher.open(searchUrl)
    output = simplejson.load(f)
    return output['items'][0]['link']
