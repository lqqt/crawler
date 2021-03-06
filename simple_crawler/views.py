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
        cnt = FullWebsite(content=s.content)
        el = Element(title=s.title, address=s.url, describtion=s.desc, content=cnt)
        cnt.save()
        el.save()
        
        data.append(el)

    return render(request, "simple_crawler/result.html", {"element_list": data})


#
# Classes used to temporary keep sites, parse them and for designing crawling behaviour.
#


class Site():
    def __init__(self, url):
        try:
            self.parsed = False
            self.url = self.parse_url(url)    
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
            self.parsed = False
            print(e)

    def get_describtion(self):
        self.desc = ""
        for h in ["h1", "h2", "h3", "h4"]:
            try:
                self.desc += " " + self.soup.find(h).text.strip()
                if len(self.desc) > 300:
                    self.desc = self.desc[:300]
                    break
            except Exception:
                continue

    def parse_url(self, url):
        url = url.partition("#")[0]
        if url.startswith("www"):
            url = "http://" + url

        self.response = urlopen(url)
        self.ct = self.response.getheader('Content-Type').partition(";")[0]
        if self.ct == 'text/html':
            return url
        else:
            raise Exception()

class Crawler():
    def __init__(self, start_url, max_steps=8):
        self.starting_site = Site(start_url)
        self.links_to_visit = self.starting_site.links
        self.visited_links = set(start_url)
        self.max_steps = max_steps
        self.parsed_sites = []

    def crawl(self):
        for nr, link in enumerate(self.links_to_visit, 1):
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