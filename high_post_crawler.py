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


#institution_list = institution_string.split(",");
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
string_json={}
for i in [1]:
    url = "https://www.douban.com/group/topic/232069820/"
    #generate fake random user agent
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    ### start web crawling
    html = ""
    # get one random ip from ip pool, if the ip is blocked by tennfish website, select another ip from the pool
    while True:
       proxies = get_random_ip()
       try:
            #response = requests.post(url,data=data, headers = headers,proxies = proxies)
            response = requests.get(url, headers = headers)

            html = response.text
            break
       except requests.exceptions.RequestException as e:
            print(e)
            continue

    #html = html.decode("utf-8")
    #html = '<table width="100%" border="0" cellspacing="0" cellpadding="20" class="bodytext"><tr><td><b>[ 1 ]</b> record where abbreviation = <b>MAMU</b><hr noshade size="1"><table cellspacing="5"><tr><td valign="top" class="dispdata"><b>MAMU&nbsp;&nbsp;&nbsp;</b></td><td class="dispdata"><b>University of Sydney, Macleay Museum, Sydney, New South Wales, Australia.  Types are at AMS.</b></td></tr><tr><td>&nbsp;</td><td class="dispdata"><b>Other Abbrev.:</b> MU,MMUS. <b>Country:</b> Australia</td></tr><tr><td>&nbsp;</td><td class="dispdata"><b>WWW sites:</b> <b>Main site:</b> <a href="http://sydney.edu.au/museums/collections/macleay.shtml" target=_>http://sydney.edu.au/museums/collections/macleay.shtml</a>&nbsp;&nbsp;&nbsp;</td></tr><tr><td>&nbsp;</td><td class="dispdata"><b>Publications:</b> <a href="getref.asp?id=19518">19518</a></td></tr></table><hr size="1" noshade></td></tr></table>'
    bs = BeautifulSoup(html, 'lxml')
    institution_table_list = bs.find_all(name='table', attrs={"cellspacing": 5})
    for table in institution_table_list:
        tr_lists = table.find_all(name="tr")

        for index, tr in enumerate(tr_lists):
            if index==0:
                institution_abbrev_tr = tr.contents[0].text
                string_json[institution_abbrev_tr] = {}
                full_name_tr = tr.contents[1].text
                string_json[institution_abbrev_tr]["Full_Name"] =full_name_tr
            else:
                b_lists = tr.find_all(name="b")
                for b_index, b in enumerate(b_lists):
                    b_next = b.find_next_sibling()
                    if b_next is not None:
                        if b_next.name == 'b' and b.nextSibling.strip() == '':
                            string_json[institution_abbrev_tr][b.text] = 'None'
                        elif b_next.name == 'b' and b.nextSibling.strip() != '':
                            string_json[institution_abbrev_tr][b.text] = b.nextSibling
                        else:
                            string_json[institution_abbrev_tr][b.text] = b_next.text
                    else:
                        string_json[institution_abbrev_tr][b.text] = b.nextSibling
    print(string_json)


with open('data_country.txt', 'w') as outfile:
    json.dump(string_json, outfile)




