# -*- coding: utf-8 -*-
"""
Created on Fri May 21 12:38:40 2021

cross-validation for AA snps at: https://gnomad.broadinstitute.org/


@author:  Hugh Lu

"""

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from random import seed
import numpy as np
import time


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


#path="C:/Users/danny/Desktop/snp_match_python"
#os.chdir(path)



### Get the combined url address for double check process  
def slash_join(*args):
    '''
    Joins a set of strings with a slash (/) between them. Useful for creating URLs.
    If the strings already have a trailing or leading slash, it is ignored.
    Note that the python's urllib.parse.urljoin() does not offer this functionality. 
    '''
    stripped_strings = []
    # strip any leading or trailing slashes
    for a in args:
        if a[0] == '/': start = 1
        else:           start = 0
        if a[-1] =='/':
            stripped_strings.append(a[start:-1])
        else:
            stripped_strings.append(a[start:])

    return '/'.join(stripped_strings)


## Get Selenium working first 
browser = webdriver.Chrome(ChromeDriverManager().install())
imput_url = "https://gnomad.broadinstitute.org/variant/"

## Read SNPs name and into list
aasn = pd.read_excel("AA_447_short.xlsx")

input_snp_names = aasn.AA_snps

temp = "rs1447295"

tail = "/?dataset=gnomad_r3"

#### Define crapping parameters 
## SNP Name
SNPN= []
SNPN_extra = []
## AA allele frequency 
AAAF = []
## White allele frequency
WAF = []
## Gene name 
GN = []
## Variation difference
VD = []



temp1=[]
temp2=[]

classes = []


## Start looping 
for i in range (0,len(input_snp_names)):
    test_url = slash_join(imput_url, input_snp_names[i],tail)
    browser.get(imput_url + input_snp_names[i] + tail)
    ## set a buffering time for server to resopnse the searching results
    time.sleep(4)
## if the url did not change, then we need run selenium one more time with the information extracted by
##  beautifsoup, so, let's working on this now. 
    current_url = browser.current_url
    if (len(test_url) == len(current_url)):
        SNPN_extra.append(input_snp_names[i]) ## take care of this multip-variants data later 
    else:
        r = requests.get(current_url)
        soup= BeautifulSoup(r.content, "html.parser")
        print(soup.prettify())
browser.close()
        




 


# # data = {'snp_name': SNPN,'AA_allele_frequency ':AAAF,
# #         'White_allele_frequency':WAF,'Gene_name':GN, 'Variation_difference':VD}
 
# # df = pd.DataFrame(data)
# # df.to_csv('snap_comparison_AA.csv', index=False, encoding='utf-8')    




 