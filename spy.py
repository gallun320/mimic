
import urllib2
import sqlite3 as sqlite
from BeautifulSoup import *
from urlparse import urljoin

ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


class crawler:
    def __init__(self,dbname):
        self.con=sqlite.connect(dbname)
    def __del__(self):
        self.con.close( )
    def dbcommit(self):
        self.con.commit( )

    def getentryid(self,table,field,value,createnew=True):
         return None
    def addtoindex(self,url,soup):
              print '%s' % url
    def gettextonly(self,soup):
        return None
    def separatewords(self,text):
        return None
    def isindexed(self,url):
        return False
    def addlinkref(self,urlFrom,urlTo,linkText):
        pass
    def crawl(self,pages,depth=2):
        for i in range(depth):
            newpages = set()

            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print "%s" % page
                    continue
                soup = BeautifulSoup(c.read())
                self.addtoindex(page, soup)

                links = soup('a')

                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1: continue
                        url = url.split('#')[0]

                        if url[0:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText=self.gettextonly(link)
                        self.addlinkref(page,url,linkText)

                    self.dbcommit()
                pages = newpages
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit( )

crawler('net').crawl(['https://ru.wikipedia.org/wiki/Python'])
