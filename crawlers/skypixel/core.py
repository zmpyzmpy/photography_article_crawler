#!/usr/bin/env python2
# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import sys
import os
import time
import random

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def start_browser():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "whatever you want")
    br = webdriver.Firefox(firefox_profile = profile)
#    br.implicitly_wait(10)
    return br
            
def get_links(link,br):
    page = 0
    links = []
    while True:
        new_links = []
        if page == 0:
            br.get(link)
        elif page == 1:
            link = link[:38] + ';1'+link[38:]
            br.get(link)
        else:
            link = link[:39] + str(page)+link[40:]
            br.get(link)
            
        html = br.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for lin in soup.findAll("div", { "class" : "td DescriptionCell" }):
            new_links.append(lin.findAll('a')[0].getText())
        if new_links == []:
            break
        links.extend(new_links)
        page = page + 1
        time.sleep(1)
    return links
