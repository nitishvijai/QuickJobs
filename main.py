#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Nitish Vijai
# <nitishv@umich.edu>
# https://github.com/nitishvijai/QuickJobs
# main.py

# This file will scrape job postings from major job sites (LinkedIn, Glassdoor, and Indeed).
# Still working on the implementation.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

job_query = ""
driver = webdriver.Chrome()
job_array = []

def getInput(): 
    # Input a job title and URLify the query
    job_title = input("\nWhat kind of jobs are you looking for today?> ")
    print("Looking for", job_title, "jobs...")
    job_title = job_title.replace(" ", "%20")
    return job_title

def scrapeLinkedIn():
    # Initialize Selenium driver to LinkedIn site
    driver.get("https://www.linkedin.com/jobs/search?keywords={}".format(job_query))
    print("Searching on LinkedIn...")

    for _ in range(6):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    # scroll up
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(5)

    # SCRAPE!
    listings = driver.find_elements_by_class_name('result-card')

    for listing in listings:
        div = listing.find_element_by_css_selector('div.result-card__contents')
        title = div.find_element_by_css_selector('h3')
        print(title.text)

    driver.close()



if __name__ == '__main__':
    print("Find Me A Job -- Command-Line Interface")
    print("---" * 13)
    job_query = getInput()

    scrapeLinkedIn()