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

    for _ in range(6):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(5)

    driver.close()



if __name__ == '__main__':
    print("Find Me A Job -- Command-Line Interface")
    print("---" * 10)
    job_query = getInput()

    scrapeLinkedIn()