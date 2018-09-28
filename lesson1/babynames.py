#!/usr/bin/env python3 -tt
# -*- coding: utf-8 -*-

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
from os import listdir

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""


def extract_names(filename):
    """Given a file name flor baby.html, returns a list starting with the year string
  
       followed by the name-rank strings in alphabetical order.
       ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]

        :param filename: file path
        :type filename: string
        :return: dictionary of ranked names of boys an ranked names of girls
        :rtype: dictionary of (strings, int)
  
    """
    myFile = extract_from_file(filename)
#  print(myFile)
    year = extract_year(myFile)
#  print(year)
    durtyList = extract_all_names(myFile)
    cleanList = create_dictionary(durtyList)
#  print(cleanList)
    finalList = {year: ""}
    finalList.update(cleanList[0])
    finalList.update(cleanList[1])
    finalSortedList = sorted(finalList.items())
#  print (finalList)
    return finalSortedList


def list_to_text(myList):
    """Utility : Given a dictionary, return a string with the concatation of key + value 

        :param myList: the original dictionary
        :type myList: dict
        :return: the resulting text
        :rtype: string
  
    """
    textList = ""
    for k, v in myList:
        textList = textList + k + "\t" + v + "\n"
    return textList


def extract_from_file(filename):
    """Utility : return the string from a file

        :param filename: path of the file
        :type filename: string
        :return: the resulting text
        :rtype: string
  
    """
    myFile = open(filename, mode="r")
    text = myFile.read()
    myFile.close()
    return text


def extract_year(textFile):
    """Utility : extract the year of the record

        :param textFile: text of the record
        :type textFile: string
        :return: the resulting year
        :rtype: string
  
    """  
    pat = re.compile(r"Popularity in \d+")
    yearExpression = pat.findall(textFile)
    return yearExpression[0][14:]


def extract_all_names(textFile):
    """Utility : extract the boys and girls names of the record

        :param textFile: text of the record
        :type textFile: string
        :return: the resulting list
        :rtype: sequence
  
    """   
    pat = re.compile(r"<td>\d+</td><td>[A-Z][a-z]+</td><td>[A-Z][a-z]+</td>")
    durtyListNames = pat.findall(textFile)
    return durtyListNames


def create_dictionary(durtyList):
    """Utility : from a list of records, return a dictionaries where keys are names and values are ranked
     first list for boys and second for girls

        :param durtyList: list of the records
        :type durtyList: list
        :return: the resulting lists
        :rtype: sequence of dict
  
    """       
    cleanList = list(map(lambda x: x.replace("</td><td>", " ")
                         .replace("</td>", "")
                         .replace("<td>", ""), durtyList))
    cleanBoysDict = dict()
    cleanGirlsDict = dict()
    sorted(cleanBoysDict, reverse=True)
    sorted(cleanGirlsDict, reverse=True)
    for item in cleanList:
        details = item.split()
        cleanBoysDict[details[1]] = details[0]
        cleanGirlsDict[details[2]] = details[0]
    return [cleanBoysDict, cleanGirlsDict]


def store_summary(fileDir, fileName):
    """Utility : store datas of fileName in a new file "fileName.summary" in a new format

        :param fileDir: directory path of fileName
        :type fileDir: string
        :param fileName: fileName
        :type fileDir: string
        :return: no return  
    """      
    summaryFile = extract_names(fileDir + "/" + fileName)
    newFile = open(fileDir + "/" + fileName + ".summary", "w")
    newFile.write(list_to_text(summaryFile))
    newFile.close()


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]
    # For each filename, get the names, then either print the text output
    # or write it to a summary file
        if len(args) == 0:
            print("Sorry ----- No file")
        else:
            for fileName in args:
                store_summary(".",  fileName)
    else:
        myList = extract_names(args[0])
        print(list_to_text(myList))


if __name__ == '__main__':
    main()
