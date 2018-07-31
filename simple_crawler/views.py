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
    sites = cwl.crawl()
    tmp_cnt = FullWebsite(content="TMP")
    data = []
    for s in sites:
        data.append(Element(title=s.title, address=s.url, describtion=s.desc, content=tmp_cnt))

    # data = Element.objects.order_by('content')[:5]
    return render(request, "simple_crawler/result.html", {"element_list": data})



    # title = models.CharField(max_length=100)
    # address = models.URLField()
    # describtion = models.CharField(max_length=300)
    # content = models.ForeignKey(FullWebsite, on_delete=models.CASCADE)




class Site():
    def __init__(self, url):
        try:
            self.parsed = False
            self.url = url
            self.response = urlopen(url)

            self.ct = self.response.getheader('Content-Type').partition(";")[0]
            if self.ct == 'text/html':
                self.parse_site()
        except Exception:
            self.parsed = False


    def parse_site(self):
        self.soup = BeautifulSoup(self.response, "html.parser")
        try:
            self.title = self.soup.title.string
            self.links = {parse.urljoin(self.url, link.get("href")) for link in self.soup.find_all('a')}
            self.content = str(self.soup)
            self.get_describtion()
            self.parsed=True
        except Exception as e:
            self.title=""
            self.links = {}
            self.content = ""
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
    def __init__(self, start_url, max_steps=5):
        self.starting_site = Site(start_url)
        self.links_to_visit = self.starting_site.links
        self.visited_links = set(start_url)
        self.max_steps = max_steps
        self.parsed_sites = []

    def crawl(self):
        for nr, link in enumerate(self.links_to_visit):
            if link not in self.visited_links:
                site = Site(link)
                if site.parsed:
                    self.parsed_sites.append(site)
                self.visited_links.add(link)
            if nr >= self.max_steps:
                break

        if self.parsed_sites:
            for s_site in filter(lambda x: x is not None, self.parsed_sites):
                self.links_to_visit.update(s_site.links)

        return self.parsed_sites
