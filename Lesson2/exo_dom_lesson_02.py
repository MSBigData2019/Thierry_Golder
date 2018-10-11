#!/usr/bin/env python3 -tt
# -*- coding: utf-8 -*

import unittest

from bs4 import BeautifulSoup
import requests


originalURL = "https://www.reuters.com/finance/stocks/financial-highlights/"
societes = ["AIR.PA", "DANO.PA", "LVMH.PA"]

def _handle_request_result_and_build_soup(url, type = "get",data = ""):
    if type == "post" :
        request_result = requests.post(url, data)
    else :
        request_result= requests.get(url)
    try :
        if request_result.status_code == 200:
            html_doc =  request_result.text
            soup = BeautifulSoup(html_doc,"html.parser")
    except FileNotFoundError:
        print("oups")
        return BeautifulSoup("erreur d'URL", "html.parser")
    return soup

def _getSoups(firms = societes) :
    ls = {}
    for el in firms :
        ls[el] = _handle_request_result_and_build_soup(originalURL+el)
    return ls

def _getQuarterEnding18(soup) :
    return soup.find("tr", class_="stripe").findChildren()[2].text 

def _getSharesOwned(soup):
     return soup.findAll("tbody", class_="dataSmall")[2].findChildren()[3].text

def _getStockPrice(soup):
     return _removeBadCaracter(soup.findAll("div", class_="sectionQuoteDetail")[0].findChildren()[3].text)

def _getPurcentageEvolutionStock(soup):
     return _removeBadCaracter(soup.findAll("div", class_="sectionQuoteDetail")[1].findChildren()[5].text)

def _getDividendYield(soup):
     gen = soup.findAll("td", string="Dividend Yield" )[0]
     ret = ""
     for i in range(0,3):
         gen = gen.findNextSibling("td")
         ret = ret + gen.text +" " 
     return ret

def _removeBadCaracter(s):
     s = s.replace("\n", "").replace(" ", "").replace("\t", "").replace("(", "").replace(")","")
     return s


class Lesson2Tests(unittest.TestCase):

    def testChargementPage(self) :
        self.assertEqual(str(type(_handle_request_result_and_build_soup(originalURL + "LVMH.PA"))), "<class 'bs4.BeautifulSoup'>")
        self.assertEqual(str(type(_handle_request_result_and_build_soup(originalURL + "AIR.PA"))), "<class 'bs4.BeautifulSoup'>")
        self.assertEqual(str(type(_handle_request_result_and_build_soup(originalURL + "DANO.PA"))), "<class 'bs4.BeautifulSoup'>")


    def testQuaterEnding(self) :
        self.assertEqual(_getQuarterEnding18(_handle_request_result_and_build_soup(originalURL + "LVMH.PA")), "13,667.70")
        self.assertEqual(_getQuarterEnding18(_handle_request_result_and_build_soup(originalURL + "AIR.PA")), "23,493.00")
        self.assertEqual(_getQuarterEnding18(_handle_request_result_and_build_soup(originalURL + "DANO.PA")), "6,072.60")

    def testSharesOwned(self) :
        self.assertEqual(_getSharesOwned(_handle_request_result_and_build_soup(originalURL + "LVMH.PA")), "20.57%")
        self.assertEqual(_getSharesOwned(_handle_request_result_and_build_soup(originalURL + "AIR.PA")), "43.53%")
        self.assertEqual(_getSharesOwned(_handle_request_result_and_build_soup(originalURL + "DANO.PA")), "50.60%")

    def testPurcentageEvolutionStock(self) :
        self.assertEqual(_getPurcentageEvolutionStock(_handle_request_result_and_build_soup(originalURL + "LVMH.PA")), "-7.14%")
        self.assertEqual(_getPurcentageEvolutionStock(_handle_request_result_and_build_soup(originalURL + "AIR.PA")), "-3.42%")
        self.assertEqual(_getPurcentageEvolutionStock(_handle_request_result_and_build_soup(originalURL + "DANO.PA")), "-0.47%")

    def testStockPrice(self):
        self.assertEqual(_getStockPrice(_handle_request_result_and_build_soup(originalURL + "LVMH.PA")), "265.30")
        self.assertEqual(_getStockPrice(_handle_request_result_and_build_soup(originalURL + "AIR.PA")), "98.99")
        self.assertEqual(_getStockPrice(_handle_request_result_and_build_soup(originalURL + "DANO.PA")), "65.33")

    def testDividendYield(self):
        self.assertEqual(_getDividendYield(_handle_request_result_and_build_soup(originalURL + "LVMH.PA")), "1.92 1.70 2.60 ")
        self.assertEqual(_getDividendYield(_handle_request_result_and_build_soup(originalURL + "AIR.PA")), "1.45 1.34 1.64 ")
        self.assertEqual(_getDividendYield(_handle_request_result_and_build_soup(originalURL + "DANO.PA")), "2.90 2.78 2.48 ")


def main():
    unittest.main()

if __name__ == '__main__':
    main()

