#!/usr/bin/env python
# coding=utf-8
'''
Author: uniooo
Date: 2021-12-29 20:56:02
LastEditors: uniooo
LastEditTime: 2021-12-29 23:08:21
FilePath: /dblp-coauthors/get_coauthors.py
Description: 
'''

import argparse
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
# import mechanize
# from bs4 import BeautifulSoup, SoupStrainer
# import re

inspect_years = set()
coauthor_list = set()

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--years', default=2, help='coauthor in recent years')
    parser.add_argument('--author_list', default='author_list.txt', help='the authors\' dblp pages that we need to inspect')
    parser.add_argument('--output', default='coauthors.txt', help='resulting coauthors')
    
    return parser.parse_args()

def get_paper_info(paper):
    global coauthor_list
    temp_coauthor = []
    for child in paper:
        if child.tag == 'year':
            year = int(child.text)
            if year not in inspect_years:
                return
        if child.tag == 'author':
            temp_coauthor.append(child.text)

    for coauthor in temp_coauthor:
        coauthor_list.add(coauthor)

def crawl_page(author_page_xml):
    xml_response = requests.get(author_page_xml)
    root = ET.fromstring(xml_response.content)
    for child in root:
        if child.tag == 'r':
            for paper in child:
                get_paper_info(paper)

def crawl_data(args):
    # print('\n-----------------------')
    # print('Starting crawl')
    # print('-----------------------\n')
    with open(args.author_list) as author_pages:
        for author_page_url in author_pages:
            crawl_page(author_page_url[:-5] + "xml")

    
    # br = mechanize.Browser()
    # with open(args.author_list) as author_pages:
    #     for author_page_url in author_pages:
    #         print(author_page_url[:-4] + "xml")
    #         crawl_page(br, author_page_url)
    

def set_inspect_years(args):
    global inspect_years
    years = int(args.years)
    year = datetime.today().year
    for i in range(years + 1):
        inspect_years.add(year-i)
    inspect_years.add(year+1) # some journals may publish next year's issue
    # print(inspect_years)

def main(args):
    global coauthor_list
    set_inspect_years(args)
    crawl_data(args)

    coauthors = []
    for coauthor in coauthor_list:
        coauthors.append(tuple(coauthor.split(" ", 1)))

    coauthors = sorted(coauthors, key=lambda x: x[1])
    with open(args.output, "w") as fout:
        for coauthor in coauthors:
            fout.write(" ".join(coauthor) + "\n")
           
if __name__ == "__main__":
    args = parse_args()
    main(args)