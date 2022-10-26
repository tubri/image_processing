"""
    fetch size, height and width of images(deprecated)
"""
from urllib import request as ulreq
from concurrent.futures.thread import ThreadPoolExecutor
from os.path import basename
from urllib.request import urlopen
from PIL import ImageFile
from io import BytesIO

# import requests
import pandas as pd
import sys

# import grequests

# institution code: cumv,utep,uam
# institutioncode = 'cumv'

# scExcel = pd.read_excel("D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "_Copy.xlsx")


# scExcel = pd.read_csv("C:/Users/Administrator/img_metadata.csv")
# scExcel = pd.read_csv("D:/HDR/iDigBio_List_CompleteFish_20210420.csv")
# scExcel = pd.read_csv("E:/D/HDR/GLIN_missing_imageslist_Nov2021_dimention.csv")
scExcel = pd.read_csv("C:/work/hdr/dataset/morphbank_metadata.csv")
scExcel['width'] = None
scExcel['height'] = None
scExcel['size'] = None
scExcel['dimension_status'] = None
length = len(scExcel)


def getSizes(uri):
    # get file size *and* image size (None if not known)
    file = ulreq.urlopen(uri)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while True:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.width, p.image.height
            break
    file.close()
    return size, None, None


def main(index):
    try:
        # if scExcel['source'][index] == 'www.morphbank.net':
        #    newExcel['filename'][index] = "Error"
        # else:
        # through internet
        url = scExcel['Path'][index]
        # r = requests.get(url)
        # imageFile = Image.open(BytesIO(r.content))
        #
        # scExcel['width'], scExcel['height'] = imageFile.size
        # scExcel['filename'][index] = filename
        if url is not "No Path":
            imgInfo = getSizes(url)
            scExcel['size'][index], scExcel['width'][index], scExcel['height'][index] = imgInfo

            # through local
            # path = "D:/HDR/idigbio_missing_dim/" + scExcel['OriginalFileName'][index]
            # scExcel['size'][index] = os.path.getsize(path)
            print(scExcel['filename'][index], scExcel['size'][index])
    except KeyError as e:
        scExcel['dimension_status'][index] = "Error"


# institutioncode = 'usnm'
# return a list of filename


if __name__ == '__main__':
    # time1=strftime("%Y-%m-%d %H:%M:%S", localtime())# currTime

    Pool = ThreadPoolExecutor(20)  # create 5 threads
    for i in range(length):
        Pool.submit(main, i)  # submit tasks to threads pool
    Pool.shutdown(wait=True)  # wait=True
# for i in range(length):
#   main(i)


# print(newExcel)
# newExcel.to_excel("D:/HDR/multimedia_5/splitedworksheet/"+ institutioncode +"_filename.xlsx",index=False)
# scExcel.to_csv("C:/Users/Administrator/idigbio_metadata_final.csv", index=False)
scExcel.to_csv("C:/work/hdr/dataset/morphbank_metadata_with_dimention.csv", index=False)
