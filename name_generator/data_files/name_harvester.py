import requests
from html.parser import HTMLParser
import wikipedia



class WikipediaListParser(HTMLParser):

    def handle_endtag(self, tag):
        pass

    def handle_starttag(self, tag, attrs):
        pass

    def handle_data(self, data):
        pass



class WikipediaHarvester:

    def __init__(self):
        self.parser = WikipediaListParser()

    def request_page(self, url):
        data = requests.get(url)
        self.parser.feed(data)


# harvester = WikipediaHarvester()
# harvester.request_page('https://en.wikipedia.org/wiki/List_of_lakes')

page = wikipedia.page(title='List_of_lakes')

print(page.links)