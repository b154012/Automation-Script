#!/usr/bin/env python
#title           :data_transformation.py
#description     :This script will clean data issues and create standardized csvs.
#author          : Zulmi Yahya
#date            :20/03/2022
#usage           :python data_transformation.py
#python_version  :3.7 above 

# import pandas, numpy
import pandas as pd
import numpy as np
import re
import os
from datetime import datetime
from prettytable import PrettyTable
pd.set_option('display.min_rows', None)
pd.set_option('display.max_rows', None)

def convert_specific_values(newdf):
    col = ['col1', 'col2']

    for x in range(len(col)):
        if col[x] in list(newdf.columns):
            col_ebv_dna = list(newdf[col[x]])
            tmp = col_ebv_dna.copy()

            for i, dna in enumerate(col_ebv_dna):
                if re.match(r"[>]+", str(dna)):
                    col_ebv_dna[i] = float(dna.replace('>', '')) + 0.0001
                elif re.match(r"[<]+", str(dna)):
                    col_ebv_dna[i] = float(dna.replace('<', '')) - 0.0001
                elif re.match("[0-9]+", str(dna)):
                    col_ebv_dna[i] = float(dna)
                else:
                    if str(dna) == "":
                        col_ebv_dna[i] = 0.0001
                    elif str(dna) == "" or str(dna) == "":
                        col_ebv_dna[i] = 0.0002

            # replace 
            old_data = tmp
            new_data = list(col_ebv_dna)
            newdf[col[x]] = newdf[col[x]].replace(old_data, new_data)

    return newdf

def sort_col(newdf, colname):

    no_exp = []
    exp = []

    for name in colname:
        exist = bool(re.search(r'exceptions', name, flags=re.I))
        if not exist:
            no_exp.append(name)
        else:
            exp.append(name)


    new_sorted_col = no_exp + exp

    return newdf[new_sorted_col]
        

def format_date(newdf, colname):
    col_date = [i for i in colname if re.search(r'Date|date', i)]
    no_exp_col = []
        
    for name in colname:
        exist = bool(re.search(r'exceptions', name, flags=re.I))
        if not exist:
            #print(name)
            no_exp_col.append(name)

    no_exp_col = [i for i in no_exp_col if re.search(r'Date|date', i)]

    for col in no_exp_col:
        date_format_1 = list(newdf[col])
        new_format = [convert(i) for i in date_format_1]
        old_data = list(newdf[col])
        new_data = list(new_format)
        newdf[col] = newdf[col].replace(old_data, new_data)

    return newdf

def remove_words(newdf, colname):
    remove_list = ["unknown", "ongoing", "Ongoing", "Unknown", "UNK"]

    for name in colname:
        exist = bool(re.search(r'exceptions', name, flags=re.I))
        if not exist:
            for i in range(len(remove_list)):
                newdf[name].replace(remove_list[i], np.nan, inplace=True)

    return newdf

def split_mul_records(r_df):
    cols = list(r_df.columns)[0:3]

    rdf = r_df.set_index(cols) \
          .stack() \
          .str.split('\n', expand=True) \
          .stack() \
          .unstack(-2) \
          .reset_index(-1, drop=True) \
          .reset_index()

    return rdf
        
def create_exception_col(r_df, copy_r_df):

    specific_values = ["unknown", "ongoing", "Ongoing", "Unknown", "UNK", "Detection of IgA antibody to Early Ag", "Detection of IgA antibody to Early Ag and Capsid Ag", "Detection of IgA antibody to Capsid Ag"]
    index = []
    value = []
    column = []

    for i in list(copy_r_df.columns):
        for x, v in copy_r_df[i].items():
            if v in specific_values:
                col_new = i + " exceptions"
                r_df[col_new] = ""
                index.append(x)
                value.append(v)
                column.append(col_new)
            elif re.match(r"[<]+", str(v)) or re.match(r"[>]+", str(v)):
                col_new = i + " exceptions"
                r_df[col_new] = ""
                index.append(x)
                value.append(v)
                column.append(col_new)

    dictionary = list(zip(index, value, column))
            
    for i in range(len(dictionary)):
        #print(dictionary[i][0], dictionary[i][1], dictionary[i][2])
        r_df.at[dictionary[i][0], dictionary[i][2]] = dictionary[i][1]

    return r_df

def convert(dtm):
    formats = ['%d/%m/%Y', '%d/%m/%Y %H:%M:%S %p', '%d/%m/%Y %H:%M:%S']
    regex = re.compile('[-]')

    if type(dtm) == float:
        return dtm
    elif (regex.search(dtm) != None):
        # eg. 2020-12-17
        return change_date_format(dtm)
    else:
        if len(dtm) >= 9:
            #eg. '22/07/2022'
            for fmt in formats:
                    d = datetime.strptime(dtm, fmt).strftime('%d/%m/%Y')
                    return d + ' 00:00:00'
        elif len(dtm) == 8:
            match = re.search(r'/', dtm[-4:])
            if match:
                    #eg. '10/12/17'
                d = datetime.strptime(dtm, '%d/%m/%y').strftime('%d/%m/%Y')
                return d + ' 00:00:00'
            else:
                #eg. '1/1/2018'
                d = datetime.strptime(dtm, '%d/%m/%Y').strftime('%d/%m/%Y')
                return d + ' 00:00:00'
        else:
            #eg. '1/1/12' or '11/8/20'
            match = re.search(r'/', dtm[-4:])
            if match:
                d = datetime.strptime(dtm, '%d/%m/%y').strftime('%d/%m/%Y')
                return d + ' 00:00:00'

# change wrong data from 2022-03-17
def change_date_format(dt):
        # change 2022-03-17 to 17/03/2022
        date_1 = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)
        date_1 = date_1.replace('-', '/')
        d = datetime.strptime(date_1, '%d/%m/%Y %H:%M:%S').strftime('%d/%m/%Y')
        return d + ' 00:00:00'

def run_task(files):

    for csv in files:

        # read csv
        r_df = pd.read_csv(csv)
        copy_r_df = r_df.copy()

        # create unique ID for each row
        r_df.insert(2, 'row_num', np.arange(len(r_df)), True)

        # Problem 6: Create exception column for specific values
        r_df = create_exception_col(r_df, copy_r_df)

        # Problem 3: split 2 records in one line
        rdf = split_mul_records(r_df)

        # create another df for rows that are removed after >>>>Problem 3
        exist_data = [i for i in rdf['row_num'] if i in r_df['row_num']]

        # remove existing rows in rdf 
        for i in range(len(exist_data)):
            r_df.drop(r_df.index[(r_df["row_num"] == exist_data[i])], axis=0, inplace=True)

        #print(r_df.tail(5))

        # combine empty/NaN (r_df) and filled dataframes (rdf)
        # sort by row_num in ascending order
        newdf = pd.concat([rdf, r_df], ignore_index=False, sort=False) \
        .sort_values(by='row_num', ascending=True)

        # drop row_num to clean columns
        newdf.drop(['row_num'], axis=1, inplace=True)

        # Problem 2 & 4: remove unccessary words and make it NaN/empty
        colname = (newdf.columns)
        newdf = remove_words(newdf, colname)

        # Problem 5: define methods to compute dataframe format to dd/mm/yyyy hh:mm:ss
        newdf = format_date(newdf, colname)

        # Problem 1: convert specific values such as >750/<750, detection options into float
        newdf = convert_specific_values(newdf)
                
        newdf.replace('nan', np.nan, inplace=True)

        newdf = sort_col(newdf, colname)
                
        #Finally save it into CSV
        new_csv = csv[:-4] + "_clean.csv"
        newdf.to_csv(new_csv, index=False)
    
if __name__ == '__main__':
    
    # assumming in the current directory that contains a list of required CSVs
    files = [i for i in os.listdir() if i.endswith("_data.csv")]  
    
    run_task(files)
