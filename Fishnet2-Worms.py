import glob
import json
import os
import pandas as pd
import numpy as np
from fake_useragent import UserAgent


def split(filehandler, delimiter='\t', row_limit=1499,
          output_name_template='D://Fishnet2//New folder//output_%s.csv', output_path='.', keep_headers=True):
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w', newline=''), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = next(reader)
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w', newline=''), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)


#split(open('D://Fishnet2//ScientificNames.csv', 'r', errors='ignore'));

def classfication():
    current_file_index = 1
    while current_file_index <= 61:
        data = pd.read_excel("D://Fishnet2//output_matched//output_"+ str(current_file_index) +"_matched.xlsx")

        #exact
        data_unnone = data.dropna(subset=["Match type"]) #filter none type
        data_unnone_unabgious = data_unnone.loc[data_unnone['Match type'] != 'ambiguous'] # filter ambiguous type
        data_unnone_unabgious_str = data_unnone_unabgious[data_unnone_unabgious['AphiaID'].notnull()].copy()
        data_unnone_unabgious['AphiaID'] = data_unnone_unabgious['AphiaID'].astype(int)
        data_unnone_unabgious['AphiaID'] = data_unnone_unabgious['AphiaID'].astype(str)
        data_output = data_unnone_unabgious[['ScientificName','AphiaID','Match type','LSID','ScientificName.1']]

        data_output.to_csv('D://Fishnet2//output_matched//exact//matched_'+ str(current_file_index) +'_exact.csv',index=False)

        #none
        data_none = data[data['Match type'].isna()]
        #data_none['AphiaID'] = data_none['AphiaID'].astype(int).astype(str)
        data_none_output = data_none[['ScientificName', 'AphiaID', 'Match type', 'LSID', 'ScientificName.1']]

        data_none_output.to_csv('D://Fishnet2//output_matched//none//matched_' + str(current_file_index) + '_none.csv',
                           index=False)

        #ambiguous
        data_ambiguous = data_unnone.loc[data_unnone['Match type'] == 'ambiguous']
        #data_ambiguous['AphiaID'] = data_ambiguous['AphiaID'].astype(int).astype(str)
        data_ambiguous_output = data_ambiguous[['ScientificName', 'AphiaID', 'Match type', 'LSID', 'ScientificName.1']]
        data_ambiguous_output.to_csv('D://Fishnet2//output_matched//amb//matched_' + str(current_file_index) + '_amb.csv',
                                index=False)

        current_file_index = current_file_index + 1

#classfication()

def merge_file(inputfile_dir, outputfile):

    csv_list = glob.glob(inputfile_dir+ '\\*')

    filepath = csv_list[0]
    df = pd.read_csv(filepath)
    df = df.to_csv(outputfile, index=False)

    for i in range(1, len(csv_list)):
        filepath = csv_list[i]
        df = pd.read_csv(filepath)
        df = df.to_csv(outputfile, index=False, header=False, mode='a+')

#merge_file("D://Fishnet2//output_matched//none","D://Fishnet2//output_matched_none_list.csv")
#merge_file("D://Fishnet2//output_matched//exact","D://Fishnet2//output_matched_exact_list.csv")
#merge_file("D://Fishnet2//output_matched//amb","D://Fishnet2//output_matched_amb_list.csv")

import requests

def get_amb():
    url="http://www.marinespecies.org/rest/AphiaRecordsByMatchNames"
    df = pd.read_csv("D://Fishnet2//output_matched_amb_list.csv")
    scientificNames = df["ScientificName"].values.tolist()
    scientificNames = scientificNames[:300]
    parameters = "?"
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'referer': 'http://www.marinespecies.org/rest/',
    }
    for name in scientificNames:
        parameters = parameters + "scientificnames[]=" + name + "&"
    parameters  = parameters + "&like=true&marine_only=false"

    #parameters ="?scientificnames[]=Pikea%20sp.&scientificnames[]=Gobius%20niger&like=true&marine_only=true"
    r = requests.get(url + parameters, headers=headers)

    if r.status_code == 200:

        json_data = r.json()

        with open('D://Fishnet2//data.json', 'w') as json_file:
            json_file.write(r.text)

#get_amb()

#pd.read_json("D://Fishnet2//data.json").to_excel("D://Fishnet2//datajson.xlsx")

import random

def random_pick(some_list, probabilities):
    x = random.uniform(0,1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item

some_list = [1,2,3,4]
probabilities = [0.2,0.1,0.6,0.1]



def random_pick_weight(data):
    total = sum(data.values())
    rad = random.randint(1, total)

    cur_total = 0
    res = ""
    for k, v in data.items():
        cur_total += v
        if rad <= cur_total:
            res = k
            break
    return res


def random_pick_next_imageid():
    overlap_p = random_pick([5, 10], [0.05, 0.95])
    selected_score = 0
    if overlap_p == 5:
        selected_score = 3
        #select from user record
    else:
        data={"5":5, "20":20, "50":50, "25":25}
        selected_score = int(random_pick_weight(data))
        #select from image pool based on score
    return selected_score

i=0
while i < 100:
    print(random_pick_next_imageid())
    i = i+1