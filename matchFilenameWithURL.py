import os
from concurrent.futures.thread import ThreadPoolExecutor
from os.path import basename
from urllib.request import urlopen

import requests
import pandas as pd
import sys
#import grequests

# institution code: cumv,utep,uam
institutioncode = 'cumv'

#scExcel = pd.read_excel("D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "_Copy.xlsx")
scExcel = pd.read_table("D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "_ar - Copy.txt")
scExcel['filename'] = None
newExcel = pd.DataFrame(columns=['ac:accessURI', 'redirectURI', 'filename'])
newExcel['ac:accessURI'] = scExcel['ac:accessURI'].copy()
newExcel['redirectURI'] = scExcel['redirectURI'].copy()
length = len(newExcel)
# for index in range(length):
#     url = newExcel['ac:accessURI'][index]
#     url = url.split('/')[-1]
#     url = url.replace("-","")
#     newExcel['merge'][index] = url
#     print(index, "/", length)
# newExcel.to_csv("E:/"+ institutioncode +"_url_merge.csv",index=False)

# def get_filename_dict():
#     folder_path = "D:/HDR/multimedia_5/splitedworksheet/" + institutioncode
#     grayscale_path = "D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + '/grayscale'
#     labels_path = "D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + '/grayscale/labels'
#     filename_dict = list()
#     for root, dirs, files in os.walk(folder_path):
#
#         for file in files:
#             #print(file)
#             filename_dict.append(file)
#
#     for root, dirs, files in os.walk(grayscale_path):
#         #filename_dict = list()
#         for file in files:
#             #print(file)
#             filename_dict.append(file)
#     for root, dirs, files in os.walk(labels_path):
#         #filename_dict = list()
#         for file in files:
#             #print(file)
#             filename_dict.append(file)
#     return filename_dict
#
# filelist = get_filename_dict()
# filelistDf = pd.DataFrame(columns=['merge','filename'])
# filelistDf['filename'] = filelist
# for index in range(len(filelist)):
# #for index in range(10):
#     arkfile = filelistDf['filename'][index].strip("ark-_65665_")
#     arkfile = arkfile.strip(".jpg")
#     if "-" in arkfile:
#         arkfile = arkfile.replace("-","")
#     filelistDf['merge'][index] = arkfile
#     print(arkfile)
#
# # rs = pd.merge(newExcel,filelistDf, how='left', on=['merge'])
# filelistDf.to_csv("E:/"+ institutioncode +"_filename_merge.csv",index=False)
#
# filenameDFmerge = pd.read_csv("E:/" + institutioncode + "_filename_merge.csv")
# urlDFmerge = pd.read_csv("E:/" + institutioncode + "url_merge.csv")
#
# rs = pd.merge(urlDFmerge,filenameDFmerge, how='left', on=['merge'])
# print(rs)
# rs.to_csv("E:/"+ institutioncode +"_final_merge.csv",index=False)
import re

def main(index):
    print(index,"/",length)
    try:
        #if scExcel['source'][index] == 'www.morphbank.net':
        #    newExcel['filename'][index] = "Error"
        #else:
            url = newExcel['redirectURI'][index]
            r = requests.get(url)
            #d = r.headers['content-disposition']
            #filename = re.findall("filename\*=(.+)", d)[0]
            #filename = filename.replace("utf-8''","")
            #print(filename)
            # filetype = ''
            # if r.headers['Content-Type'] == 'text/html; charset=UTF-8':
            #     newExcel['filename'][index] = "html"
            #     return
            # if "image/jpeg" in r.headers['Content-Type']:
            #     filetype = ".jpg"
            # elif "image/tiff" in r.headers['Content-Type']:
            #     filetype = ".tif"
            # elif "image/png" in r.headers['Content-Type']:
            #     filetype= ".png"

            # if ".jpg" not in filename:
            filename = basename(urlopen(url).url)
                #if filename == "":
                #    filename_fromurl = url.split('/')[-1]
            filename = filename.replace(".JPG", ".jpg")
            filename = filename.replace(".PNG", ".png")
            filename = filename.replace(".TIF", ".tif")
            newExcel['filename'][index] = filename
            print(url, "/", filename)

    except KeyError as e :
        newExcel['filename'][index] = "Error"

#institutioncode = 'usnm'
#return a list of filename



if __name__ == '__main__':
    #time1=strftime("%Y-%m-%d %H:%M:%S", localtime())#当前时间


    Pool=ThreadPoolExecutor(20)  #创建5个线程
    for i in range(length):
       Pool.submit(main,i)#向线程提交任务
    Pool.shutdown(wait=True) #wait=True
    # for i in range(length):
    #    main(i)








#print(newExcel)
newExcel.to_excel("D:/HDR/multimedia_5/splitedworksheet/"+ institutioncode +"_filename.xlsx",index=False)

