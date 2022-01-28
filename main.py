from bs4 import BeautifulSoup
import urllib3
import json
from datetime import datetime
import PyRSS2Gen

url = "http://www.hankintailmoitukset.fi/fi/notice/search/?_s%5B_sent%5D=1&_s%5Bphrase%5D=&_s%5Bcpv%5D=72-5&_s%5Borganisation%5D=&_s%5Bnuts%5D=&_s%5Bpublished_start%5D=&_s%5Bpublished_end%5D=&_s%5Bform_number%5D%5B%5D=domestic_contract&_s%5Bform_number%5D%5B%5D=contract&_s%5Bform_number%5D%5B%5D=contract_utilities"

http = urllib3.PoolManager()
r = http.request('GET', url)
soup = BeautifulSoup(r.data)
data = soup.table.tbody.findAll("tr")
items=[]

items = []
for tr in data:
    adata = tr.findAll("td")

    ''' JSON type reservation '''
    # a = {"published": adata[1].text, "deadline": adata[2].text, "name": adata[3].a.text, "url": adata[3].a['href']}

    r = http.request('GET', adata[3].a['href'])
    asoup = BeautifulSoup(r.data)
    contact = asoup.find_all("table", class_="CONTACT")
    contactname = contact[0].tr.find_all("td")[1].text
    try:
        print(asoup.findAll("dd").p)
    except:
        pass
    item = PyRSS2Gen.RSSItem(
        title = contactname + " - " + adata[3].a.text,
        link = adata[3].a['href'],
        description = adata[3].a.text + " Deadline: " + adata[2].text,
        guid = PyRSS2Gen.Guid(adata[3].a['href']),
        pubDate = datetime.strptime(adata[1].text, '%d.%m.%Y %I.%M')
    )
    items.append(item)

rss = PyRSS2Gen.RSS2(
    title = "HILMA HANKKEET",
    link = url,
    description = "Hilma prospects",
    lastBuildDate = datetime.now(),
    items=items

)

rss.write_xml(open("pyrss2gen.xml", "w"), encoding="utf-8")
