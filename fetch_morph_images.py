import json
import mimetypes
import time
import random
from time import sleep
from bs4 import BeautifulSoup
import xlwt
import requests
import pandas as pd
import numpy as np
import re
import sys
import ssl
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
from fake_useragent import UserAgent
# #create ip proxy pool
ua = UserAgent()
# #"http://greatlakesinvasives.org/portal/imagelib/search.php?nametype=2&taxtp=2&taxa=&common=&photographer=&tags=&keywords=&uploaddate1=1000&uploaddate2=2020&imagecount=all&imagedisplay=thumbnail&imagetype=all&taxastr=&countrystr=&statestr=&keywordstr=&phuidstr=&phjson=&submitaction=Load+Images&db%5B%5D=48"
# #"http://greatlakesinvasives.org/portal/lh00/search.php?nametype=2&taxtp=2&taxa=&common=&photographer=&tags=&keywords=&uploaddate1=1000&uploaddate2=2020&imagecount=all&imagedisplay=thumbnail&imagetype=all&taxastr=&countrystr=&statestr=&keywordstr=&phuidstr=&phjson=&submitaction=Load+Images&db%5B%5D=48#"
#ippool_req = requests.get("https://www.proxy-list.download/api/v1/get?type=http") # This ip pool is updated every 2 hours
# #ippool_response = requests.urlopen(ippool_req)
#ippool_content = ippool_req.content.decode()
#ip_list = str.split(ippool_content,sep='\r\n')
def get_random_ip():
    if sys.version_info[0] == 2:
        import six
        from six.moves.urllib import request
        ctx = ssl.create_default_context()
        ctx.verify_flags = ssl.VERIFY_DEFAULT
        opener = request.build_opener(
            request.ProxyHandler({'http': 'http://127.0.0.1:24000'}),
            request.HTTPSHandler(context=ctx))
        r = opener.open('http://lumtest.com/myip.json').read()
    if sys.version_info[0] == 3:
        import urllib.request
        ctx = ssl.create_default_context()
        ctx.verify_flags = ssl.VERIFY_DEFAULT
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({'http': 'http://127.0.0.1:24000'}),
            urllib.request.HTTPSHandler(context=ctx)
            )
        r = opener.open('http://lumtest.com/myip.json').read()
    proxy_dictionary = json.loads(r)
    return {'http': proxy_dictionary["ip"] + ":" + str(proxy_dictionary["asn"]["asnum"])}
    # return {'https': proxy_dictionary["ip"]}
# def get_random_ip():
#     proxy_list = []
#     for ip in ip_list:
#         proxy_list.append(ip)
#     proxy_ip = random.choice(proxy_list)
#     proxies = {'http': proxy_ip}
#     return proxies

path = "C:\\work\\hdr\\missing\\"
image_url_df = pd.read_excel("C:\\work\\hdr\\gbif_dataset\\missing_images.xlsx", engine='openpyxl')

headers = {
        'User-Agent': ua.random,
        'authority': 'data.nhm.ac.uk',
        'Connection':'close'
    }
# s=requests.session()
# jar = requests.cookies.RequestsCookieJar()
# jar.set('ckan','45135db2e61f4991b1f0612835da603c6d9fbac8e0ecec2159e94e679eb0e14e95ca755a')
# s.cookies.update(jar)
proxies = get_random_ip()
loop_counter = 1
for row in image_url_df.iterrows():
    if loop_counter == 100:
        loop_counter = 1
        proxies = get_random_ip()
    #r = requests.get(row[1]["identifier"], headers=headers, proxies=proxies,allow_redirects=True)
    #r = requests.get(row[1]["identifier"], headers=headers, allow_redirects=True,verify=False)
    #r = s.get(row[1]["identifier"], headers=headers, allow_redirects=True)
    try:
        sleep(1)
        r = requests.get(row[1]["identifier"], headers=headers,proxies=proxies,verify=False)
        content_type = r.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        if extension == None:
            extension = ''
        if extension == '.jpe':
            extension = '.jpg'
        print(row[1]["imageName"], r.status_code,time.time())
        image_url_df.at[row[0], 'imageFullName'] = str(row[1]["imageName"]) + extension

        with open(path + str(row[1]["imageName"]) + extension, 'wb') as f:
            f.write(r.content)
        f.close()
        r.close()
        loop_counter = loop_counter + 1
    except Exception as e:
        cur_try = 0
        total_try = 50
        while cur_try < total_try:
            print("cut_try" + str(cur_try))
            proxies = get_random_ip()
            try:
                sleep(15)
                r = requests.get(row[1]["identifier"], headers=headers, proxies=proxies, verify=False)
                content_type = r.headers['content-type']
                extension = mimetypes.guess_extension(content_type)
                if extension == None:
                    extension = ''
                if extension == '.jpe':
                    extension = '.jpg'
                print(row[1]["imageName"], r.status_code, time.time())
                image_url_df.at[row[0], 'imageFullName'] = str(row[1]["imageName"]) + extension

                with open(path + str(row[1]["imageName"]) + extension, 'wb') as f:
                    f.write(r.content)
                f.close()
                r.close()
                loop_counter = loop_counter + 1
                break
            except Exception as e:
                cur_try += 1
                loop_counter = 1


image_url_df.to_excel(path + 'new_gbif_imglist.xlsx',index = False)