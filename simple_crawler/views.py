from django.shortcuts import render
from django.http import Http404

from bs4 import BeautifulSoup
from urllib.request import urlopen 
from functools import reduce
from urllib import parse

from .models import Element, FullWebsite


def index(request):
    return render(request, "simple_crawler/index.html")

def result(request, link):

    if not link.startswith("http://"):
        link = "http://" + link
    
    cwl = Crawler(link)
    links = cwl.crawl()
    tmp_cnt = FullWebsite(content="TMP")
    data = []
    for i in links:
        data.append(Element(title="TITLE", address=i, describtion="DESC", content=tmp_cnt))

    # data = Element.objects.order_by('content')[:5]
    return render(request, "simple_crawler/result.html", {"element_list": data})



    # title = models.CharField(max_length=100)
    # address = models.URLField()
    # describtion = models.CharField(max_length=300)
    # content = models.ForeignKey(FullWebsite, on_delete=models.CASCADE)




class Site():
    def __init__(self, url):
        self.url = url
        self.response = urlopen(url)

        self.ct = self.response.getheader('Content-Type').partition(";")[0]
        if self.ct == 'text/html':
            self.parse_site()
            self.parsed = True
        else:
            self.parsed = False
        

    def parse_site(self):
        self.soup = BeautifulSoup(self.response, "html.parser")
        try:
            self.title = self.soup.title.string
            self.links = {parse.urljoin(self.url, link.get("href")) for link in self.soup.find_all('a')}
            self.content = str(self.soup)
            self.get_describtion()
        except Exception as e:
            self.parsed = False
            print(e)

    def get_describtion(self):
        
        for h in ["h1", "h2", "h3", "h4"]:
            try:
                self.desc = self.soup.find(h).text.strip()
                if self.desc:
                    break
            except:
                continue

        print("DESC:  ", self.desc)


class Crawler():
    def __init__(self, start_url, max_depth=2):
        self.links = {start_url}
        self.current_depth = 1
        self.visited_links = set()

    def crawl(self, max_depth=4):
        tmp_links = []
        counter = 0
        for link in self.links:
            if link not in self.visited_links:
                site = Site(link)
                if site.parsed:
                    tmp_links.append(site.links)
                self.visited_links.add(link)
            if counter == max_depth:
                break
            else:
                counter += 1
        
        if tmp_links:
            tmp = reduce(lambda x, y: x.update(y), tmp_links)
            self.links.update(tmp)
        return self.links
