import json
import mimetypes
import time
import random
from time import sleep
from bs4 import BeautifulSoup

import requests
import pandas as pd

#
# image_df = pd.DataFrame(columns=('ImageID', 'ScientificName'))
#
# html = "https://www.morphbank.net/Browse/ByImage/?tsn=161061&activeSubmit=2&keywords=&tsnId_Kw=id&tsnKeywords=161061&viewId_Kw=keywords&spId_Kw=keywords&localityId_Kw=keywords&offset=180&numPerPage=2000000&log=NO"
#
# #response = requests.get(html)
#
# bs = BeautifulSoup(open("download.html"),'html.parser')
# image_list = bs.find_all(name='div',attrs={"class":"imagethumbnail"})
#
# for image_item in image_list:
#     image_id_span = image_item.span.contents[0]
#     image_taxon = image_item.a.contents[0]
#
#
#     image_df = image_df.append({'ImageID': image_id_span, 'ScientificName': image_taxon}, ignore_index=True)
#
# image_df.to_excel('morphobank_img_list.xlsx',index = False)
# print("hi")
#from fake_useragent import UserAgent
# #create ip proxy pool
#ua = UserAgent()
# #"http://greatlakesinvasives.org/portal/imagelib/search.php?nametype=2&taxtp=2&taxa=&common=&photographer=&tags=&keywords=&uploaddate1=1000&uploaddate2=2020&imagecount=all&imagedisplay=thumbnail&imagetype=all&taxastr=&countrystr=&statestr=&keywordstr=&phuidstr=&phjson=&submitaction=Load+Images&db%5B%5D=48"
# #"http://greatlakesinvasives.org/portal/lh00/search.php?nametype=2&taxtp=2&taxa=&common=&photographer=&tags=&keywords=&uploaddate1=1000&uploaddate2=2020&imagecount=all&imagedisplay=thumbnail&imagetype=all&taxastr=&countrystr=&statestr=&keywordstr=&phuidstr=&phjson=&submitaction=Load+Images&db%5B%5D=48#"
#ippool_req = requests.get("https://www.proxy-list.download/api/v1/get?type=http") # This ip pool is updated every 2 hours
# #ippool_response = requests.urlopen(ippool_req)
#ippool_content = ippool_req.content.decode()
#ip_list = str.split(ippool_content,sep='\r\n')

# def get_random_ip():
#     proxy_list = []
#     for ip in ip_list:
#         proxy_list.append(ip)
#     proxy_ip = random.choice(proxy_list)
#     proxies = {'http': proxy_ip}
#     return proxies

#path = "C:\\work\\hdr\\GBIF\\"
image_url_df = pd.read_excel("morphobank_img_metadata.xlsx", engine='openpyxl')
#image_url_df = pd.read_excel("test.xlsx", engine='openpyxl')

# headers = {
#         'User-Agent': ua.random()
#     }
data = [] #store all metadata
for index_p, row in enumerate(image_url_df.iterrows()):
    #proxies = get_random_ip()
    #r = requests.get(row[1]["identifier"], headers=headers, proxies=proxies,allow_redirects=True)
    #r = requests.get(row[1]["identifier"], headers=headers, allow_redirects=True,verify=False)
    url = row[1]["detail_path"]
    ### start web crawling
    html = ""
    # get one random ip from ip pool, if the ip is blocked by tennfish website, select another ip from the pool
        #proxies = get_random_ip()
    try:
        response = requests.get(url)
        html = response.content
    except requests.exceptions.RequestException as e:
        print(e)
        continue

    html = html.decode("utf-8")
    bs = BeautifulSoup(html, 'lxml')
    container = {
        'ImageRecordId':row[1]['ImageID'],
        'ScientificName':row[1]['ScientificName'],
        'metadata_path':row[1]["detail_path"]
    }

    #top and middle_part: Specimen, Locality, Determination, External links/identifiers, Other Annotations
    for index,tds in enumerate(bs.select('td.firstColumn')):
        if index == 3:
            break
        for table in tds.find_all('table'):
            for tr in table.find_all('tr', recursive=False):
                container[tr.find('th').text.strip().rstrip(':')] = tr.find('td').text.strip()
                if tr.find('th').text.strip().rstrip(':') == 'License':
                    a_ele = tr.find('a')
                    container[tr.find('th').text.strip().rstrip(':')] = a_ele.attrs['href'].strip()


    #Determination annotations
    determination_annotation = bs.select('td.imageAnnotation')[0]
    determination_annotation_table = determination_annotation.find_all('table')
    if len(determination_annotation_table) > 0:
        rows = determination_annotation_table[0].find_all('tr')
        strongs = rows[0].find_all('strong')
        for strong in strongs:
                container['Determination_Annotation_' + strong.text.strip().rstrip(':')] = strong.nextSibling.strip()

    #bottom related annotation
    relate_imageAnnotation = bs.select('td.imageAnnotation')[2]
    relate_imageAnnotation_table = relate_imageAnnotation.find_all('table')[1]
    rows = relate_imageAnnotation_table.find_all('tr')
    theader = rows[0].find_all('td')
    tcontents = rows[1].find_all('td')
    for index, th in enumerate(theader):
        container['Relate_Annotation_' + th.text.strip()] = tcontents[index].text.strip()
        if th.text.strip() is '' and len(th.attrs) > 0:
            container['Relate_Annotation_'+ th.attrs['title']] = tcontents[index].text.strip()
    data.append(container)
    print(container['ImageRecordId'])

with open('json_data_fin.json', 'w') as outfile:
    json.dump(data, outfile)


#result_df = pd.read_json(json.dumps(data))
#result_df.to_csv('metadata.csv', index = None)


#image_url_df.to_excel(path + 'new_gbif_imglist.xlsx',index = False)