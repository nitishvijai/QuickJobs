#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Nitish Vijai
# <nitishv@umich.edu>
# https://github.com/nitishvijai/QuickJobs
# main.py

# This file will scrape job postings from major job sites (LinkedIn, Glassdoor, and Indeed).
# Still working on the implementation.

from selenium import webdriver
from selenium import common
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
        company = div.find_element_by_css_selector('h4').find_element_by_class_name('result-card__subtitle-link')

        applyNow = div.find_elements_by_class_name('job-result-card__easy-apply-label')

        # skipping Apply Now / Easy Apply jobs for now
        if len(applyNow) >= 1:
            continue

        time.sleep(1)

        listing.click()

        time.sleep(1)

        right = driver.find_element_by_class_name('topcard__content-right')
        
        time.sleep(1)

        link = 0
        try:
            link = right.find_element_by_class_name('apply-button')
            time.sleep(1)
            print(title.text, '-', company.text, '-', link.get_attribute("href"))
        except common.exceptions.StaleElementReferenceException as error:
            pass
        

        

    driver.close()



if __name__ == '__main__':
    print("Find Me A Job -- Command-Line Interface")
    print("---" * 13)
    job_query = getInput()

    scrapeLinkedIn()