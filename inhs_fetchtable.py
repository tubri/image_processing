import json
import random
import re
import time
import urllib

from bs4 import BeautifulSoup
import xlwt
import requests

# save to excel
from fake_useragent import UserAgent

book = xlwt.Workbook()
sheet1 = book.add_sheet('sheet1', cell_overwrite_ok=True)

#create ip proxy pool
ua = UserAgent()
"http://greatlakesinvasives.org/portal/imagelib/search.php?nametype=2&taxtp=2&taxa=&common=&photographer=&tags=&keywords=&uploaddate1=1000&uploaddate2=2020&imagecount=all&imagedisplay=thumbnail&imagetype=all&taxastr=&countrystr=&statestr=&keywordstr=&phuidstr=&phjson=&submitaction=Load+Images&db%5B%5D=48"
"http://greatlakesinvasives.org/portal/imagelib/search.php?nametype=2&taxtp=2&taxa=&common=&photographer=&tags=&keywords=&uploaddate1=1000&uploaddate2=2020&imagecount=all&imagedisplay=thumbnail&imagetype=all&taxastr=&countrystr=&statestr=&keywordstr=&phuidstr=&phjson=&submitaction=Load+Images&db%5B%5D=48#"
ippool_req = requests.get("https://www.proxy-list.download/api/v1/get?type=http") # This ip pool is updated every 2 hours
#ippool_response = requests.urlopen(ippool_req)
ippool_content = ippool_req.content.decode()
ip_list = str.split(ippool_content,sep='\r\n')

def get_random_ip():
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

#start id and end id
startid = 1
endid = 215
currentid = startid

# get data
sheet_row = 1
data_list_title = ["id"]
while currentid <= endid:
    value0 = str(currentid)
    url = "http://greatlakesinvasives.org/portal/imagelib/rpc/changeimagepage.php"

    data = {
        "starr": json.dumps({"db": "48;", "taxa": "", "taxontype": "2", "usethes": 0, "country": "", "state": "", "phuid": "",
            "tags": "", "keywords": "", "uploaddate1": "1000", "uploaddate2": "2020", "imagecount": "all",
            "imagedisplay": "thumbnail", "imagetype": "all"}),
        "page": currentid,
        "view":"thumb",
        "taxon":""
    }

    #generate fake random user agent
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'referer': 'https://www.morphbank.net',
        "Content-Type": "application/x-www-form-urlencoded"
    }

    ### start web crawling
    html = "https://www.morphbank.net/Browse/ByImage/?tsn=161061&activeSubmit=2&keywords=&tsnId_Kw=id&tsnKeywords=161061&viewId_Kw=keywords&spId_Kw=keywords&localityId_Kw=keywords&offset=180&numPerPage=2000000&log=NO"
    # get one random ip from ip pool, if the ip is blocked by tennfish website, select another ip from the pool
    while True:
        #proxies = get_random_ip()
        try:
            #response = requests.post(url,data=formdata, headers = headers,proxies = proxies)
            response = requests.post(url,data=data, headers = headers)
            responsejson =response.json()
            html = response.json()
            break
        except requests.exceptions.RequestException as e:
            print(e)
            continue

    #html = html.decode("utf-8")
    bs = BeautifulSoup(html, 'lxml')


    tntiv_list = bs.find_all(name='div',attrs={"class":"tndiv"})
    for div in tntiv_list:
        first_div = div.contents[1]
        if len(first_div.contents)>1:
            id=first_div.contents[2].contents[0]
        else:
            id= first_div.contents[0].contents[0]
        data_list_title.append(id)
        print(id)
    # dealing with content
    currentid = currentid + 1
print(data_list_title)
# save file
#book.save('sum'+str(startid) + '-' + str(endid) +'.xls')


