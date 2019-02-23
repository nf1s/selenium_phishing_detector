# Alexa Top 500 Scraper

## What does it do?
- Scrapes Pages from Alexa 500 Top without API.
- You can scrape top 500 global.
- You can scrape top 500 countrywise.
- You can scrape top 500 category and subcategory wise.

## Why are there two scripts?
- Two different Implementations.
- script.py - More generic approach, extracts data based on ```<li>``` tag (a little slower).
- scripy2.py - More specific approach, extracts data based on ```<a>``` in combination with regex over links.

## How it works
- The idea is simple, we open the link.
- Fetch the data
- Capture the data, read and convert it to string.
- Using the Python HTML Parser, we check whether if the current class holds a link out those 500 mentioned
- If it is a useful link, set the flag and capture data and unset it after data capture.

## How is it implemented?
- Pure Python, no libraries, no extra dependencies
- Checkout output.txt

## How does it run?
- It is tested on Python 2.7.12 and 3.5.2
- generic command: ```python script-name.py number-of-links country/category country-code/sub-categories```
- Here is list of combinations
- ```python script.py```
- ```python script.py (N)```
- ```python script.py countries (two letter country code (eg: IN for India))```
- ```python script.py category subcategory1/subcategory2/```

## Thank You