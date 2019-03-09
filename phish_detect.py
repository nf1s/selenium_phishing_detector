# -*- coding: utf-8 -*-
"""Phish_detect Module.

The selenium web driver module provides all the web driver implementations.
Current supported implementations are firefox, chrome and IE
it can be used remotely as well

"""
import json
from urllib.parse import urlparse

from influxdb import InfluxDBClient
from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.common.exceptions import TimeoutException, WebDriverException
# The keys library provides keys in the keyboard like enter, ALT and so on
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import url_analysis

# The elemnts that we need to interact with will be defined here
# according to their Xpath
input_tag_xpath = "//input"
text_type_xpath = "//input[@type='text']"
email_type_xpath = "//input[@type='email']"
email_id_xpath = "//input[@id='email']"
email_name_xpath = "//input[@name='email']"
userId_xpath = "//input[@id='user']"
user_name_xpath = "//input[@name='user']"
username_name_xpath = "//input[@name='username']"
passwd_xpath = "//input[@type='password']"


def check_exists_by_xpath(driver, xpath):
    """selenium webdriver has no builtin function to check whether an element exists or not
    this is why this function was implemented
    it tries to find an element by xpath
    Args:
        driver: (object) Instance of Selenium Webdriver
        xpath: (str) Xpath for a certain HTML element

    Returns:
        bool: True when element is found, False otherwise

    Raises:
        NoSuchElementException: if Element does not exit.

    """
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


# this function will check the existance of all of the elements specified
# and will return the ones that exists for testing
def email_and_password_exits(driver):
    """This function will check the existance of all of the elements specified
    and will return the ones that exists for testing

    Args:
        driver: (object) Instance of Selenium Webdriver
      
    Returns:
        tuple: input_tag, text_type, email_type, email_id, email_name, \
           user_id, user_name, username_name, passwd

    """
    input_tag = check_exists_by_xpath(driver, input_tag_xpath)
    text_type = check_exists_by_xpath(driver, text_type_xpath)
    email_type = check_exists_by_xpath(driver, email_type_xpath)
    email_id = check_exists_by_xpath(driver, email_id_xpath)
    email_name = check_exists_by_xpath(driver, email_name_xpath)
    user_id = check_exists_by_xpath(driver, userId_xpath)
    user_name = check_exists_by_xpath(driver, user_name_xpath)
    username_name = check_exists_by_xpath(driver, username_name_xpath)
    passwd = check_exists_by_xpath(driver, passwd_xpath)

    return input_tag, text_type, email_type, email_id, email_name, \
           user_id, user_name, username_name, passwd


def test_fake_credentials(driver, test_email, xpath, count):
    """This function will take fake credentials (email, username .. etc)
    and will first clear the text input field then add
    the fake email
    Args:
        driver: (object) Instance of Selenium Webdriver
        test_email: (str) invalid email for testing purposes e.g.
        xpath: (str) Xpath for a certain HTML element
        count: (int) the number of iterations

    Returns:

    """
    try:
        user = driver.find_element_by_xpath(xpath)
        if count > 0:
            try:
                # user.clear()
                user.send_keys(Keys.CONTROL + "a")
                user.send_keys(Keys.DELETE)
            except:
                pass
        user.send_keys(test_email)  # Your email_id
    except ElementNotVisibleException:
        pass
    except NoSuchElementException:
        pass


def test_fake_password(driver, count):
    """This function tests the password field type with fake password
       the fake password
       Args:
           driver: (object) Instance of Selenium Webdriver
           count: (int) the number of iterations
       Returns:

       """
    passwd = driver.find_element_by_xpath(passwd_xpath)
    if count > 0:
        try:
            passwd.clear()
            passwd.send_keys(Keys.CONTROL + "a")
            passwd.send_keys(Keys.DELETE)
        except:
            pass
    passwd.send_keys("Hello12345")  # Your password
    passwd.send_keys(Keys.RETURN)
    WebDriverWait(driver, 2)
    WebDriverWait(driver, 5).until(EC.staleness_of(passwd))


def test_email_list():
    """Functions contains the list of emails used for testing

    Returns:
        list: list of invalid/ fake emails

    """
    emails = ['some_email@nicedomain.com', 'happy.forever@best.com', 'python@great.com', 'first.last@name.com']
    return emails


# Influx_db is a time series no sql databases which has the first field always as the current time the log
# in our case it is used because of the ease of use
# we have mainly 4 measurements
# phishing for websites that are detected as phishing
# legitimate for the websites that are detected as legitimate
# if the website has no login or considered as neutral
# if the website contains login yet for some reason the test could not complete
# it is considered as incomplete_test
# this function takes the url and sends it to the influxdb under its corresponding measurement
def to_influx_database(url, res):
    """Influx_db is a time series no sql databases which has the first field always as the current time the log
    in our case it is used because of the ease of use
    we have mainly 4 measurements
    phishing for websites that are detected as phishing
    legitimate for the websites that are detected as legitimate
    if the website has no login or considered as neutral
    if the website contains login yet for some reason the test could not complete
    it is considered as incomplete_test
    this function takes the url and sends it to the influxdb under its corresponding measurement

    Args:
        url: (str) url of the tested website
        res: (int) result value

    Raises:
        IOError: when database server is unreachable


    """
    if res == 1:
        result = "phishing"
    elif res == 0:
        result = "legitimate"
    elif res == -1:
        result = "incomplete_test"
    else:
        result = "neutral"

    points = [

        {
            "measurement": result,
            "tags": {
                "browser": "firefox"
            },
            "fields": {
                "url": url
            }
        }

    ]

    try:
        db_client = InfluxDBClient('localhost', '8086',
                                   'root', 'root', 'phishing_db')
        db_client.create_database('phishing_db')
        db_client.write_points(points)

    except IOError as error:
        print(str(error))


def to_mongodb(domain, url):
    """this function is called whenever a legitimate website
    needs to be added to our whitelist which is hosted in this mongodb
    the domain will be added under the collection *legitimate* in phishing database name


    Args:
        domain: (str) domain of tested website
        url: (str) url of tested website

    """
    db_client = MongoClient()
    db = db_client.phishing
    db.whitelist.insert_one(
        {
            "legitimate": {
                "domain_name": domain,
                "url": url
            }
        }
    )


def check_domain_in_white_list(domain):
    """this function fetchs the mongodb white list for domains
      to check if it already resides in the whitelist

    Args:
        domain: (str) domain name of web-page being tested

    Returns:
        object: database response

    """
    db_client = MongoClient()
    db = db_client.phishing
    cursor = db.whitelist.find_one({'legitimate.domain_name': domain})
    return cursor


def get_domain_from_uri(uri):
    """function mainly strips domain from protocol header and path
    to be saved in the white list later
    Args:
        uri: (str) Uri being tested

    Returns:
        str: domain name

    """
    domain_name = urlparse(uri).hostname
    return domain_name


def full_test(driver, domain_name, url):
    """ Main function for executing test steps

    Args:
        driver:  (Object )Instance of selenium Driver
        domain_name: (str) domain name
        url: (str) url

    Returns:
        int: result (1=Positive, 0=neutral, -1=Negative

    """
    # returns all elements that we are interested in
    input_tag, text_type, email_type, email_id, email_name, \
    user_id, user_name, username_name, \
    password = email_and_password_exits(driver)

    # getting the fake email list
    count = 0
    email_list = test_email_list()

    # the loop will continue to test the website as long as
    # there is an input field and password
    try:

        while input_tag and count < 3:

            if password:

                domain = get_domain_from_uri(driver.current_url)

                if email_type:
                    test_fake_credentials(driver, email_list[count], email_type_xpath, count)

                elif email_id:
                    test_fake_credentials(driver, email_list[count], email_id_xpath, count)

                elif email_name:
                    test_fake_credentials(driver, email_list[count], email_name_xpath, count)

                elif user_id:
                    test_fake_credentials(driver, email_list[count], userId_xpath, count)

                elif user_name:
                    test_fake_credentials(driver, email_list[count], user_name_xpath, count)

                elif username_name:
                    test_fake_credentials(driver, email_list[count], username_name_xpath, count)

                elif text_type:
                    test_fake_credentials(driver, email_list[count], text_type_xpath, count)

                test_fake_password(driver, count)

                # if selenium injects the website with an email and password
                # and a redirect occurs this is for sure a phishing website
                newDomain = get_domain_from_uri(driver.current_url)

                if newDomain != domain:
                    print('this is a phishing website because of redirect')
                    return 1
                else:
                    count += 1
                    # rechecking again what are the elements exist in the page before the next iteration
                    input_tag, text_type, email_type, email_id, email_name, \
                    user_id, user_name, username_name, \
                    password = email_and_password_exits(driver)

            else:
                break

    except TimeoutException as error:
        if password and count > 0:
            print('this is a legitimate page')
            to_mongodb(domain_name, url)
            return 0
        # if this was the first iteration and there is not login fields
    # then this page has no login
    if count < 1 and (not email_type or not email_id or not email_name) and not password:
        print('this page has no login')
        return 2

    # if after a couple of emails there are no more password field exists?
    # then the website is a phishing one
    elif not password and count < 2:
        if not email_type or not email_id or not email_name:
            print('this is a phishing website due to test')
            return 1
    # if the loop continued till the end and password still exits
    # this website passes the test and is considered as legit
    elif password and count >= 2:
        print('this is a legitimate page')
        to_mongodb(domain_name, url)
        return 0

    else:

        print('random error')


# our scraper for alexsa 500 saves the legit websites in a text file
# this function opens the txt file, extracts the domains and append it to an array

def get_legitimate_pages():
    """our scraper for alexsa 500 saves the legit websites in a text file
    this function opens the txt file, extracts the domains and append it to an array


    Returns:
        list: legit urls

    """
    text_file = open("scraper/legit_links.txt", "r")
    lines = text_file.read().split('\n')
    return lines


def get_phishing_pages():
    """our ruby scraper will scrape phishtank and will return all phishing links
    in JSON form mait in 'links-old.json' file
    this function will open the json file and parse
    the url links to an array
    Returns:

    """
    jsonFile = open('scraper/links.json', 'r')
    data = json.load(jsonFile)
    jsonFile.close()

    link_array = []

    for index in data:
        link_array.append(index['url'])

    return link_array


def run():
    """This is our main function
    user will be prompt to input whether he wants to test legitimate or phishing page
    the function will extract domain from url and check if it is in white list
    if domains exits the webdriver will close the firefox window session
    if domain does not exit then it will be tested by 'full_test' function
    then it will be logged
    Returns:

    """
    user_input = input("choose (l) for legitimate or (p) for phishing: ")
    if user_input == 'p':
        link_array = get_phishing_pages()
    elif user_input == 'l':
        link_array = get_legitimate_pages()
    else:
        link_array = get_phishing_pages()
    print('test started with ' + str(len(link_array)) + ' pages')
    old_link = ''
    for link in link_array:
        print(link)
        analysis = url_analysis.check(link)
        if analysis >= 7:
            print('this is a phishing website domain analysis')
            to_influx_database(link, 1)
            continue
        if link != old_link:
            if link is not None and link != '':
                driver = webdriver.Firefox()
                url = link
                domain = get_domain_from_uri(url)
                try:
                    driver.get(url)
                    print('testing .... ' + domain)
                    domain_in_whiteList = check_domain_in_white_list(domain)
                    if domain_in_whiteList != None:
                        print('domain is legit and in whitelist')
                        to_influx_database(link, 0)
                    else:
                        WebDriverWait(driver, 2)
                        result = full_test(driver, domain, url)
                        to_influx_database(url, result)

                except TimeoutException as error:
                    print('there is a timeout exception here' + str(error))
                    to_influx_database(link, -1)
                    pass
                except WebDriverException as error:
                    print('webdriver exception here' + str(error))
                    pass
                except ValueError or TypeError or UnicodeDecodeError as error:
                    print('value error or type error: ' + str(error))
                    continue
                except Exception as error:
                    print('total random exception: ' + str(error))
                    continue

                driver.quit()
                old_link = link
    print('test sucessfully finished')


run()
