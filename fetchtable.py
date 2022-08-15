import random
import time

from bs4 import BeautifulSoup
import xlwt
import requests

# save to excel
from fake_useragent import UserAgent

book = xlwt.Workbook()
sheet1 = book.add_sheet('sheet1', cell_overwrite_ok=True)

#create ip proxy pool
ua = UserAgent()
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
startid = 1501
endid = 5000
currentid = startid

# get data
sheet_row = 1
while currentid <= endid:
    value0 = str(currentid)
    url = "https://tennfish.utk.edu/record.php?ID=" + value0

    #generate fake random user agent
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'referer': 'https://tennfish.utk.edu/',
    }

    ### start web crawling
    html = ""
    # get one random ip from ip pool, if the ip is blocked by tennfish website, select another ip from the pool
    while True:
        proxies = get_random_ip()
        try:
            response = requests.get(url,headers = headers,proxies = proxies)
            html = response.content
            break
        except requests.exceptions.RequestException as e:
            print(e)
            continue

    html = html.decode("utf-8")
    bs = BeautifulSoup(html, 'lxml')


    # dealing with content
    data_list_title = ["id"]
    if currentid == startid:
        title = bs.find_all('td')[::2] #odd index->title/attributes
        for data in title:
            data_list_title.append(data.text.strip()[:-1])

    content = bs.find_all('td')[1::2] # even index->data
    data_list_content = [value0]
    for data in content:
        data_list_content.append(data.text.strip())



    #save td tiltle
    heads = data_list_title[:]
    ii = 0
    for head in heads:
        sheet1.write(0, ii, head)
        ii += 1

    # save content
    contents = data_list_content[:]
    j = 0
    for row in contents:
        sheet1.write(sheet_row, j, row)
        j += 1

    print(currentid);
    sheet_row += 1
    currentid += 1

    #time.sleep(1)


# save file
book.save('sum'+str(startid) + '-' + str(endid) +'.xls')


