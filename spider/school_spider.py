#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/05/26
# @Author  : kingsley kwong
# @Site    :
# @File    : school_spider.py
# @Software:
# @Function:

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

r = requests.get('https://www.schooland.hk/kg/')
soup = BeautifulSoup(r.text)
soup = soup.find_all(class_='category-link')
soup = soup[0].find_all('a')
pat = re.compile(r'^/')
for link in soup:
    if not re.match(pat, link['href']):
        print(link['href'], link.text)
        links = requests.get('https://www.schooland.hk/kg/'+link['href'])
        a = BeautifulSoup(links.text)
        tbs = a.find_all(class_='school-table')
        for tb in tbs:
            for lk in tb.find_all('a'):
                print(lk['href'], lk.text)
                schl_detl = requests.get('https://www.schooland.hk/kg/' + lk['href'])
                schl_detl_soup = BeautifulSoup(schl_detl.text)
                contact = schl_detl_soup.find_all(class_='contact')
                print(contact)
                break
            break
        break


class crawl_school(object):
    school_level = {'kindomgarden': 'https://www.schooland.hk/kg/',
                    'primary_school': 'https://www.schooland.hk/ps/',
                    'senior_school': 'https://www.schooland.hk/ss/'}
    international_school = 'https://www.schooland.hk/is/list-kg'
    university = 'https://www.schooland.hk/hi/'
    def __init__(self):
        self.area = {}

    def crawl_area(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        soup = soup.find_all(class_='category-link')
        soup = soup[0].find_all('a')
        pat = re.compile(r'^/')
        for link in soup:
            if not re.match(pat, link['href']):
                self.area.update({link.text: link['href']})

    def crawl_school_table_link(self, sch_lev, area):
        for level in sch_lev:
            for area_name, area_href in area.items():
                r = requests.get(''.join([level, area_href]))
                soup = BeautifulSoup(r.text)
                sch_tb = soup.find_all(class_='school-table')
                for tb in sch_tb:
                    for school_link in tb.find_all('a'):
                        yield area_name, school_link, level

    def crawl_school_contract(self, area_name, school_link, level):
        schl_detl = requests.get(''.join([level, school_link]))
        schl_detl_soup = BeautifulSoup(schl_detl.text)
        contact = schl_detl_soup.find_all(class_='contact')


