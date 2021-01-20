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

    # SCRAPE!
    listings = driver.find_elements_by_class_name('result-card')

    # runs limit is 11-12 before LinkedIn asks us to sign in. We'll play it safe and stop it at 11.
    # will figure out a way to bypass in the future

    runs = 0
    for listing in listings:
        if runs >= 11:
            break

        div = listing.find_element_by_css_selector('div.result-card__contents')
        title = div.find_element_by_css_selector('h3')
        company = div.find_element_by_css_selector('h4').find_element_by_class_name('result-card__subtitle-link')

        applyNow = div.find_elements_by_class_name('job-result-card__easy-apply-label')

        # skipping Apply Now / Easy Apply jobs for now
        if len(applyNow) >= 1:
            continue

        listing.click()

        time.sleep(1)

        right = driver.find_element_by_class_name('topcard__content-right')

        link = 0
        try:
            link = right.find_element_by_class_name('apply-button')
            print(title.text, '-', company.text, '-', link.get_attribute("href"))
        except common.exceptions.StaleElementReferenceException as error:
            pass
        
        runs += 1

def scrapeIndeed():
    driver.get("https://www.indeed.com/jobs?q={}".format(job_query))
    time.sleep(3)
    emailPopUpExists = driver.find_elements_by_class_name("popover-x-button-close")

    if len(emailPopUpExists) > 0:
        # discard that popup box
        driver.find_element_by_class_name("popover-x-button-close").click()

    # list of all postings on Indeed
    postings = driver.find_elements_by_class_name("jobsearch-SerpJobCard")

    for posting in postings:
        # iterate thru postings
        title = posting.find_element_by_class_name("jobtitle").get_attribute("title")
        company = posting.find_element_by_class_name("company")
        
        children = company.find_elements_by_css_selector("*")

        company_text = ""
        if len(children) > 0:
            company_text = children[0].text
        else:
            company_text = company.text
            
        print(title, '-', company_text)


if __name__ == '__main__':
    print("Find Me A Job -- Command-Line Interface")
    print("---" * 13)
    job_query = getInput()

    scrapeLinkedIn()
    scrapeIndeed()

    driver.close()