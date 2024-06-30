#!/usr/bin/python
# Author: Hearto Lazor
# Clean a list of urls using a Rom management Dat file.
# Tool page: https://github.com/HeartoLazor/autotile_generator
# Developed and tested in python 3.x
# Command examples:
#    python.exe .\dat_url_cleaner\dat_url_cleaner.py -i .\example\example_urls.txt -d .\example\example_dat.dat -o .\example\example_out.dat
# Dat Url Cleaner utility, cleans an url list based in a rom dat file. Useful to clean an url list that are expensive to download/store, 
# for example playstation 2 romset.
# An example is to copy the html table from myrient download lists, use a word processor tool like sublime to leave only the 
# links on each line and then pass that list in this tool using a dat file.
# Then use the generated list file in a mass downloader like jdownloader to download them all.
# Generates three files after finish:
#    out.txt: name can be defined by the -o command, it's the url list ready to copy to a mass downloader client like jdownloader.
#    missing_file_list.log: a list of the files from the dat that has not be found in the url_list. This means that you need to look for those remaining urls to complete the dat set.
#    removed_url_list.log: informative log with all of the rejected urls.
# Note 1: the links requires to have the same rom/iso name as the name found in the dat file. For example if in the dat the 
# filename is (Super Mario: Lost Levels) and in the url is (Super Mario Lost Levels), the url will be discarded because of the : character. 
# Note 2: the links urls can have html encoded characters, for example Super%20Mario%20World is transformed automatically to spaces, 
# also caps are ignores in comparisons.
# -i --input_url_list: rom input url list, where each url is one line.
# -d --input_dat: rom organization dat file.
# -o --out: optional parameter, cleaned generated list intended to use in jdownloader or another mass downloader client.
# -h --help: show help.

from os import listdir
from argparse import ArgumentParser
from urllib.parse import unquote
import sys
import xml.etree.ElementTree as ET

OUT_EXTENSION = ".txt"
ROM_EXTENSIONS = [".zip", ".7z", ".rar"]
REMOVED_LOG_NAME ="removed_url_list.log"
MISSING_LOG_NAME ="missing_file_list.log"
URL_PROCESS_PRINT_DISTANCE = 100

#Compare appending rom extension, fixes possible cases when try to find a subname, for example "http://nice_url/Awesome Game 2.zip" "http://nice_url/Awesome Game.zip" and the dat name is Awesome Game, 
#without the extension this test will do a false positive against Awesome Game 2
def compare_dat_name_with_url(name, url):
    formated_name = name.lower()
    formated_url = dat_format_url(url)
    for extension in ROM_EXTENSIONS:
        if((formated_name + extension) in formated_url):
            return True
    return False

#Transform an url with symbols like %20 to a dat friendly format to comparison
#Example Super%20Mario%20Bros is transformed to super mario bros
def dat_format_url(url):
    return unquote(url.lower())

def process(input_url_list, input_dat, out_name):
    print("Generating filtered file list using the urls found in: " + input_url_list)
    input_urls = []
    with open(input_url_list) as file:
        for line in file:
            stripped_line = line.rstrip()
            if(not stripped_line in input_urls):
                input_urls.append(stripped_line)
    print("Generating dat names list using the names found in: " + input_dat)
    tree = ET.parse(input_dat)
    root = tree.getroot()
    dat_names = []
    for child in root:
        if(child.tag == 'game'):
            name = child.attrib['name'].rstrip()
            if(not name in dat_names):
                dat_names.append(name)
    print("Found " + str(len(dat_names)) + " names in the dat file.")
    out_file_name = out_name + OUT_EXTENSION
    print("Generating the filtered list: " + out_file_name)
    count = 0
    count_total = 0
    total = len(input_urls)
    out_urls = []
    removed_urls = []
    print("processing [" + str(count_total) + "/" + str(total) + "] urls...")
    for url in input_urls:
        if(count > URL_PROCESS_PRINT_DISTANCE - 1):
            print("processing [" + str(count_total) + "/" + str(total) + "] urls. Found: " + str(len(out_urls)) + ". Rejected: " + str(len(removed_urls)) + " ...")
            count = 0
        count += 1
        count_total += 1
        found = False
        for name in dat_names:
            if(compare_dat_name_with_url(name, url)):
                out_urls.append(url)
                found = True
                dat_names.remove(name) #optimization
                break
        if(not found):
            removed_urls.append(url)
    print("finished! processed [" + str(count_total) + "/" + str(total) + "] urls. Found: " + str(len(out_urls)) + ". Rejected: " + str(len(removed_urls)) + " ...")
    print("Saving results to " + out_file_name)
    with open(out_file_name, "w") as txt_file:
        for line in out_urls:
            txt_file.write(line + "\n")
    print("Saving debug removed urls to: " + REMOVED_LOG_NAME)
    with open(REMOVED_LOG_NAME, "w") as txt_file:
        for line in removed_urls:
            txt_file.write(line + "\n")
    print("Saving debug missing dat filenames to: " + MISSING_LOG_NAME)
    with open(MISSING_LOG_NAME, "w") as txt_file:
        for line in dat_names:
            txt_file.write(line + "\n")
    print("Finished processing...")
    
def main():
    print("Dat Url Cleaner utility, cleans an url list based in a rom dat file. Useful to clean an url list that are expensive to download/store, for example playstation 2 romset.\n" +
          "An example is to copy the html table from myrient download lists, use a word processor tool like sublime to leave only the links on each line and then pass that list in this tool using a dat file.\n" + 
          "Then use the generated list file in a mass downloader like jdownloader to download them all.\n" +
          "Note 1: the links requires to have the same rom/iso name as the name found in the dat file. For example if in the dat the filename is (Super Mario: Lost Levels) and in the url is (Super Mario Lost Levels), the url will be discarded because of the : character.\n" + 
          "Note 2: the links urls can have html encoded characters, for example Super%20Mario%20World is transformed automatically to spaces, also caps are ignores in comparisons.\n") 
    parser = ArgumentParser()
    parser.add_argument("-i", "--input_url_list", type=str, dest="input_url_list", required=True, help="rom input url list, where each url is one line.")
    parser.add_argument("-d", "--input_dat", type=str, dest="input_dat", required=True, help=" rom organization dat file.")
    parser.add_argument("-o", "--out", type=str,  dest="out", default="out", help="cleaned generated list intended to use in jdownloader or another mass downloader client.")
    args = parser.parse_args()
    process(args.input_url_list, args.input_dat, args.out)

if __name__ == '__main__':
    main()