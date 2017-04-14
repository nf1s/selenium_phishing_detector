#!/usr/bin/python3
# Importing libraries for web driver
# the selenium web driver module provides all the web driver implementations.
# current supported implementations are firefox, chrome and IE
# it case be used remotely as well
from selenium import webdriver
# The keys library provides keys in the keyboard like enter, ALT and so on
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, ErrorInResponseException
from influxdb import InfluxDBClient
from pymongo import MongoClient
import json
from urllib.parse import urlparse

#selenium webdriver has no builtin function to check whether an element exists or not
# this is why this function was implemented
# it tries to find an element by xpath
# if the element does not exist
# NoSuchElementException will be raised and the function will catch that exception and
# and return false
def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException :
        return False
    return True


#The elemnts that we need to interact with will be defined here
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

# this function will check the existance of all of the elements specified
# and will return the ones that exists for testing
def email_and_password_exits(driver):
    input_tag = check_exists_by_xpath (driver, input_tag_xpath)
    text_type = check_exists_by_xpath(driver, text_type_xpath)
    email_type = check_exists_by_xpath(driver, email_type_xpath)
    email_id = check_exists_by_xpath(driver, email_id_xpath)
    email_name = check_exists_by_xpath(driver, email_name_xpath)
    user_id = check_exists_by_xpath(driver, userId_xpath)
    user_name = check_exists_by_xpath(driver, user_name_xpath)
    username_name = check_exists_by_xpath(driver, username_name_xpath)
    passwd = check_exists_by_xpath(driver, passwd_xpath)

    return  input_tag, text_type, email_type, email_id, email_name, \
           user_id, user_name, username_name, passwd
#------ testing part -------------------------------------------------------------#

# this function will take fake credentials (email, username .. etc)
# and will first clear the text input field then add
# the fake email
def test_fake_credentials(driver,test_email,xpath):
    try:
        user = driver.find_element_by_xpath(xpath)
        user.clear()
        user.send_keys(test_email)  # Your email_id
    except ElementNotVisibleException:
        pass

# this function will get the password type field and will input a fake password
def test_fake_password(driver):
    passwd = driver.find_element_by_xpath(passwd_xpath)
    passwd.send_keys("Hello12345")  # Your password
    passwd.send_keys(Keys.RETURN)
    WebDriverWait(driver, 2)
    WebDriverWait(driver, 5).until(EC.staleness_of(passwd))

# this function returns a list of fake emails for testing
def test_email_list():
    emails = ['some_email@nicedomain.com', 'happy.forever@best.com', 'python@great.com', 'first.last@name.com']
    return emails

# Influx_db is a time series no sql databases which has the first field always as the current time the log
# in our case it is used because of the ease of use
#we have mainly 4 measurements
# phishing for websites that are detected as phishing
# legitimate for the websites that are detected as legitimate
# if the website has no login or considered as neutral
# if the website contains login yet for some reason the test could not complete
# it is considered as incomplete_test
# this function takes the url and sends it to the influxdb under its corresponding measurement
def to_influx_database(url, res):
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

# this function is called whenever a legitimate website
# needs to be added to our whitelist which is hosted in this mongodb
# the domain will be added under the collection *legitimate* in phishing database name
def to_mongodb(domain,url):
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

# this function fetchs the mongodb white list for domains
# to check if it already resides in the whitelist
def check_domain_in_white_list(domain):
    db_client = MongoClient()
    db = db_client.phishing
    cursor = db.whitelist.find_one({'legitimate.domain_name': domain})
    return cursor

# function mainly strips domain from protocol header and path
# to be saved in the white list later
def get_domain_from_uri(uri):
    domain_name = urlparse(uri).hostname
    return domain_name

# here is our main testing function
def full_test(driver, domain_name, url):

    # returns all elements that we are interested in
    input_tag, text_type, email_type, email_id, email_name, \
    user_id, user_name, username_name, \
    password = email_and_password_exits(driver)

    # getting the fake email list
    count = 0
    email_list = test_email_list()

    # the loop will continue to test the website as long as
    # there is an input field and password
    while input_tag and count < 3:

        if password:

                domain = get_domain_from_uri(driver.current_url)

                if email_type:
                    test_fake_credentials(driver, email_list[count],email_type_xpath)

                elif email_id:
                    test_fake_credentials(driver, email_list[count],email_id_xpath)

                elif email_name:
                    test_fake_credentials(driver, email_list[count],email_name_xpath)

                elif user_id:
                    test_fake_credentials(driver, email_list[count],userId_xpath)

                elif user_name:
                    test_fake_credentials(driver, email_list[count],user_name_xpath)

                elif username_name:
                    test_fake_credentials(driver, email_list[count],username_name_xpath)

                elif text_type :
                    test_fake_credentials(driver, email_list[count],text_type_xpath)

                test_fake_password(driver)

                # if selenium injects the website with an email and password
                # and a redirect occurs this is for sure a phishing website
                newDomain = get_domain_from_uri(driver.current_url)

                if newDomain != domain:
                    print('this is a phishing website because of redirect')
                    return 1
                else:
                    count += 1
                    #rechecking again what are the elements exist in the page before the next iteration
                    input_tag,text_type, email_type, email_id, email_name, \
                    user_id, user_name, username_name, \
                    password = email_and_password_exits(driver)

        else:
            break
    #if this was the first iteration and there is not login fields
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
    elif password and count >=2 :
        print('this is a legitimate page')
        to_mongodb(domain_name,url)
        return 0

    else:
        print('random error')

# our scraper for alexsa 500 saves the legit websites in a text file
# this function opens the txt file, extracts the domains and append it to an array
def get_legitimate_pages():
    text_file = open("scraper/alexa_login.txt", "r")
    lines = text_file.read().split('\n')

    return lines

# our ruby scraper will scrape phishtank and will return all phishing links
# in JSON form mait in 'links-old.json' file
# this function will open the josn file and parse
# the url links to an array
def get_phishing_pages():
    jsonFile = open('scraper/links-old.json', 'r')
    data = json.load(jsonFile)
    jsonFile.close()

    link_array = []

    for index in data:
        link_array.append(index['url'])

    print(len(link_array))

    return link_array

# this is our main function
# user will be prompt to input whether he wants to test legitimate or phishing page
# the function will extract domain from url and check if it is in white list
# if domains exits the webdriver will close the firefox window session
# if domain does not exit then it will be tested by 'full_test' function
# then it will be logged
def run():
    user_input = input("choose (l) for legitimate or (p) for phishing: ")
    if user_input == 'p':
        link_array = get_phishing_pages()
    elif user_input == 'l':
        link_array = get_legitimate_pages()
    else:
        link_array = get_phishing_pages()
    old_link = ''
    for link in link_array:
        print(link)
        if link != old_link:
            if link is not None and link != '':
                driver = webdriver.Firefox()
                try:
                    url = link
                    driver.get(url)
                    domain = get_domain_from_uri(url)
                    print(domain)
                    domain_in_whiteList = check_domain_in_white_list(domain)
                    if domain_in_whiteList != None:
                        print('domain is legit and in whitelist')
                    else:
                        WebDriverWait(driver,2)
                        result = full_test(driver, domain, url)
                        to_influx_database(url, result)

                except TimeoutException as error:
                    print(error)
                    to_influx_database(link, -1)
                    pass
                except WebDriverException as error:
                    print(error)
                    pass
                except ValueError or TypeError or UnicodeDecodeError as error:
                    print (error)
                    continue
                except Exception as error:
                    print(error)
                    continue

                driver.quit()
                old_link = link

run()
