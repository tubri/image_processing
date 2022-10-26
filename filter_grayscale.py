"""
    remove grayscale, blackwhite images from a repository
"""
import glob
import os
import shutil
import pandas as pd

import cv2
from PIL import Image, ImageStat,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
def detect_color_image(filepath, thumb_size=40, MSE_cutoff=22, adjust_color_bias=True):
    for img_path in sorted(glob.glob(filepath + "/*.jpg")):
        gray_flag = False
        unknown = False
        with Image.open(img_path) as pil_img:
            bands = pil_img.getbands()
            if bands == ('R','G','B') or bands== ('R','G','B','A'):
                thumb = pil_img.resize((thumb_size,thumb_size))
                SSE, bias = 0, [0,0,0]
                if adjust_color_bias:
                    bias = ImageStat.Stat(thumb).mean[:3]
                    bias = [b - sum(bias)/3 for b in bias ]
                for pixel in thumb.getdata():
                    mu = sum(pixel)/3
                    SSE += sum((pixel[i] - mu - bias[i])*(pixel[i] - mu - bias[i]) for i in [0,1,2])
                MSE = float(SSE)/(thumb_size*thumb_size)
                if MSE <= MSE_cutoff:
                    print(img_path + "grayscale\t")
                    gray_flag = True

                else:
                    print(img_path + "Color\t\t\t")
                #print("( MSE=",MSE,")")
            elif len(bands)==1:
                print(img_path + "Black and white", bands)
                gray_flag = True
            else:
                unknown = True
                print(img_path + "Don't know...", bands)
        if gray_flag:
            shutil.move(img_path, filepath + "/grayscale")
        #elif unknown:
            #shutil.move(img_path, filepath + "/unknown")

def handle_img(file_path):
    for img_path in sorted(glob.glob(file_path + "/*.jpg")):
        print("processing:", img_path)
        img = Image.open(img_path)
        pix = img.convert('RGB')
        width = img.size[0]
        height = img.size[1]
        ir = 0
        hd = 0
        for x in range(width):
            for y in range(height):
                r,g,b = pix.getpixel((x,y))
                r = int(r)
                g = int(g)
                b = int(b)
                if r != g != b:
                     print(img_path + " is not grayscale")
                else:
                    print(img_path + " is grayscale")
                #if r==g==b:
                #    ir += 1
                #else:
                #    hd += 1
        #if ir > hd:
            #print(img_path + " is grayscale")

img_path = "E:/nhmuk/noextion - Copy"
#detect_color_image(img_path)

img_path = "E:/uf"
#detect_color_image(img_path)

img_path = "E:/mnhn"
#detect_color_image(img_path)

institutioncode = 'cas'
#return a list of filename

def get_filename_dict(folder_path):

    for root, dirs, files in os.walk(folder_path):
        filename_dict = list()
        for file in files:
            #print(file)
            filename_dict.append(file)
        return filename_dict
def rename_noextention(folder_path):
    for root, dirs, files in os.walk(folder_path):
        filename_dict = list()
        for file in files:
            orginalFilename = folder_path + "/" + file
            renameFilename = orginalFilename + ".jpg"
            os.rename(orginalFilename,renameFilename)
            print(renameFilename)
        return filename_dict
#rename_noextention("E:/nhmuk/noextion - Copy")

def merge_grayscale_url():
    folder_path = "D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "/grayscale"
    #folder_path = "E:/" + institutioncode + "/grayscale"
    filenamelist = get_filename_dict(folder_path)
    filenameDf = pd.DataFrame(columns=['filename','G/C'])
    filenameDf['filename'] = filenamelist
    filenameDf['G/C'] = 'grayscale'
    scExcel = pd.read_excel("D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "_filename.xlsx")
    rs = pd.merge(scExcel,filenameDf, how='left', on=['filename'])
    rs.to_excel("D:/HDR/multimedia_5/splitedworksheet/"+ institutioncode +"_filename_matched.xlsx",index=False)

mode_to_bpp = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32, "YCbCr": 24, "LAB": 24, "HSV": 24, "I": 32, "F": 32,"I;16": 16, "I;16B": 16, "I;16L": 16, "I;16S": 16, "I;16BS": 16, "I;16LS": 16, "I;32": 32, "I;32B": 32, "I;32L": 32, "I;32S": 32, "I;32BS": 32, "I;32LS": 32}
def merge_bitdepth_url():
    grayscale_folder_path= "D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "/grayscale"
    #grayscale_folder_path= "E:/" + institutioncode + "/grayscale"
    filenamelist = get_filename_dict(grayscale_folder_path)
    file_gray_Df = pd.DataFrame(columns=['filename', 'mode', 'bitDepth'])
    file_gray_Df['filename'] = filenamelist
    for index in range(len(file_gray_Df)):
        data = Image.open(grayscale_folder_path + "/" + file_gray_Df["filename"][index])
        file_gray_Df["mode"][index] = data.mode
        file_gray_Df["bitDepth"][index] = mode_to_bpp[data.mode]
        print(data.mode)

    color_folder_path = "D:/HDR/multimedia_5/splitedworksheet/" + institutioncode
    #color_folder_path = "E:/" + institutioncode
    filenamelist = get_filename_dict(color_folder_path)
    file_color_Df = pd.DataFrame(columns=['filename', 'mode', 'bitDepth'])
    file_color_Df['filename'] = filenamelist
    for index in range(len(file_color_Df)):
        data = Image.open(color_folder_path + "/" + file_color_Df["filename"][index])
        file_color_Df["mode"][index] = data.mode
        file_color_Df["bitDepth"][index] = mode_to_bpp[data.mode]
        print(data.mode)
    file_bit_df = pd.concat([file_gray_Df,file_color_Df])
    filename_matced_DF = pd.read_excel("D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "_filename_matched.xlsx")
    rs = pd.merge(filename_matced_DF, file_bit_df, how='left', on=['filename'])
    print(rs)
    rs.to_excel("D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "_filename_bit_cb.xlsx", index=False)

institutioncode = 'cas'
#merge_grayscale_url()
#merge_bitdepth_url()

def merge_grayscale_nograyscale_url():
    folder_path = "D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "/grayscale"
    #folder_path = "E:/" + institutioncode + "/grayscale"
    filenamelist = get_filename_dict(folder_path)
    filenameDf = pd.DataFrame(columns=['filename','G/C'])
    filenameDf['filename'] = filenamelist
    filenameDf['G/C'] = 'colorful'
    scExcel = pd.read_excel("D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "_filename.xlsx")
    rs = pd.merge(scExcel,filenameDf, how='left', on=['filename'])
    rs.to_excel("D:/HDR/multimedia_5/splitedworksheet/"+ institutioncode +"_filename_matched.xlsx",index=False)

def merge_bitdepth_nograyscale_url():
    color_image_folder = "D:/HDR/multimedia_5/splitedworksheet/" + institutioncode
    #color_image_folder = "E:/" + institutioncode
    filenamelist = get_filename_dict(color_image_folder)
    file_color_Df = pd.DataFrame(columns=['filename', 'mode', 'bitDepth'])
    file_color_Df['filename'] = filenamelist
    for index in range(len(file_color_Df)):
        data = Image.open(color_image_folder + "/" + file_color_Df["filename"][index])
        file_color_Df["mode"][index] = data.mode
        file_color_Df["bitDepth"][index] = mode_to_bpp[data.mode]
        print(data.mode)
    filename_matced_DF = pd.read_excel(
        "D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "_filename_matched.xlsx")
    rs = pd.merge(filename_matced_DF, file_color_Df, how='left', on=['filename'])
    print(rs)
    rs.to_excel("D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "_filename_bit_cb.xlsx", index=False)


institutioncode = "fh"
merge_grayscale_nograyscale_url()
merge_bitdepth_nograyscale_url()

institutioncode = "nhmuk"
#merge_bitdepth_nograyscale_url()

institutioncode = "uf"
#merge_bitdepth_nograyscale_url()


institutioncode = "usnm"
def merge_grayscale_usnm_url():

    folder_path = "D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "/grayscale"
    filenamelist = get_filename_dict(folder_path)
    filenameDf = pd.DataFrame(columns=['filename','G/C'])
    filenameDf['filename'] = filenamelist
    filenameDf['G/C'] = 'grayscale'
    scExcel = pd.read_csv("D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "_filename.csv")
    rs = pd.merge(scExcel,filenameDf, how='left', on=['filename'])
    rs.to_csv("D:/HDR/multimedia_5/splitedworksheet/"+ institutioncode +"_filename_matched.csv",index=False)

#mode_to_bpp = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32, "YCbCr": 24, "LAB": 24, "HSV": 24, "I": 32, "F": 32,"I;16": 16, "I;16B": 16, "I;16L": 16, "I;16S": 16, "I;16BS": 16, "I;16LS": 16, "I;32": 32, "I;32B": 32, "I;32L": 32, "I;32S": 32, "I;32BS": 32, "I;32LS": 32}
def merge_bitdepth_usnm_url():
    grayscale_folder_path= "D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "/grayscale"
    filenamelist = get_filename_dict(grayscale_folder_path)
    file_gray_Df = pd.DataFrame(columns=['filename', 'mode', 'bitDepth'])
    file_gray_Df['filename'] = filenamelist
    for index in range(len(file_gray_Df)):
        data = Image.open(grayscale_folder_path + "/" + file_gray_Df["filename"][index])
        file_gray_Df["mode"][index] = data.mode
        file_gray_Df["bitDepth"][index] = mode_to_bpp[data.mode]
        print(data.mode)

    color_folder_path = "D:/HDR/multimedia_5/splitedworksheet/" + institutioncode
    filenamelist = get_filename_dict(color_folder_path)
    file_color_Df = pd.DataFrame(columns=['filename', 'mode', 'bitDepth'])
    file_color_Df['filename'] = filenamelist
    for index in range(len(file_color_Df)):
        data = Image.open(color_folder_path + "/" + file_color_Df["filename"][index])
        file_color_Df["mode"][index] = data.mode
        file_color_Df["bitDepth"][index] = mode_to_bpp[data.mode]
        print(data.mode)
    file_bit_df = pd.concat([file_gray_Df,file_color_Df])
    filename_matced_DF = pd.read_csv("D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "_filename_matched.csv")
    rs = pd.merge(filename_matced_DF, file_bit_df, how='left', on=['filename'])
    print(rs)
    rs.to_csv("D:/HDR/multimedia_5/splitedworksheet/" + institutioncode + "_filename_bit_cb.csv", index=False)
