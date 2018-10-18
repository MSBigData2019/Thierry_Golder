#!/usr/bin/env python3 -tt
# -*- coding: utf-8 -*

import unittest
import pandas as pd
import requests
import numpy as np

originalURL = "https://gist.github.com/paulmillr/2657075"
token = ""
git_API_URL="https://api.github.com/"
headers={'Content-Type': 'application/json', 'Authorization': 'token {}'.format(token)}

def _handle_request_result_and_get_text(url, type = "get",data = "", header=""):
    html_doc = ""
    if type == "post" :
        request_result = requests.post(url, data)
    elif header != "" :
        request_result = requests.get(url, headers=header)
    else :
        request_result = requests.get(url)
    try :
        if request_result.status_code == 200:
             html_doc =  request_result.text
    except FileNotFoundError:
        print("oups")
    return request_result 

def _loadTopContributor():
    dfs = pd.read_html(originalURL)
    df = dfs[0]
    df["Mean Star"] = pd.Series(np.zeros(len(df))) 
# creation de la colonne permettant de stocker le nombre moyen d'etoile par repertoire
    return df

def _git_API_Request(param) :
    req = _handle_request_result_and_get_text(git_API_URL+param, header=headers)
    print(git_API_URL+param)
    return req


def _getGitUserData(user) :
    req = _git_API_Request("users/"+user+"/repos?page1&per_page=100")
    df0 = pd.read_json(req.text)
    df = df0.copy()
    i=2
    max=0
    dernierePage = True
    if (len(df) == 100) :
        dernierePage = False 
    while (dernierePage == False) :
        req = _git_API_Request("users/"+user+"/repos?page1&per_page=100&page="+str(i)) 
        i=i+1
        df = pd.read_json(req.text)
        df0 = pd.concat([df0,df]) 
        if ( len(df) != 100) :
            dernierePage = True
    return df0["stargazers_count"].mean() 
 

def _filDataFrameWithMeansAndOrder(df):
    i=0 
    for index, row in df["User"].items(): 
        df["Mean Star"][i] = _getGitUserData(row.split()[0])
        i=i+1
    df.sort_values(by=['Mean Star'])
    return df

class Lesson3Tests(unittest.TestCase):

    def testChargementPage(self) :
        df = _loadTopContributor() 
        self.assertEqual(len(df),256)
        df1 = _filDataFrameWithMeansAndOrder(df)
        self.assertEqual(df1['Mean Star'][0]>df1['Mean Star'][1], True)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

