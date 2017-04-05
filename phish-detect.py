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
text_type_xpath = "//input[@type='text']"
email_type_xpath = "//input[@type='email']"
email_id_xpath = "//input[@id='email']"
email_name_xpath = "//input[@name='email']"
userId_xpath = "//input[@id='user']"
user_name_xpath = "//input[@name='user']"
username_name_xpath = "//input[@name='username']"


# this function will check the existance of all of the elements specified
# and will return the ones that exists for testing
#
def email_and_password_exits(driver):
    input_tag = check_exists_by_xpath (driver, "//input")
    text_type = check_exists_by_xpath(driver, "//input[@type='text']")
    email_type = check_exists_by_xpath(driver, "//input[@type='email']")
    email_id = check_exists_by_xpath(driver, "//input[@id='email']")
    email_name = check_exists_by_xpath(driver, "//input[@name='email']")
    user_id = check_exists_by_xpath(driver, "//input[@id='user']")
    user_name = check_exists_by_xpath(driver, "//input[@name='user']")
    username_name = check_exists_by_xpath(driver, "//input[@name='username']")
    passwd = check_exists_by_xpath(driver, "//input[@type='password']")

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
    passwd = driver.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys("Hello12345")  # Your password
    passwd.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(passwd))



def test_email_list():
    emails = ['first.last@name.com', 'bla@bla.com', 'python@great.com','happy@best.com']
    return emails

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

def check_domain_in_white_list(domain):
    db_client = MongoClient()
    db = db_client.phishing
    cursor = db.whitelist.find_one({'legitimate.domain_name': domain})
    return cursor

def to_mongodb(domain):
    db_client = MongoClient()
    db = db_client.phishing
    db.whitelist.insert_one(
        {
            "legitimate": {
                "domain_name": domain
            }
        }
    )


def get_domain_from_uri(uri):
    domain_name = urlparse(uri).hostname.split('.')
    domain = domain_name[-2] +'.'+ domain_name[-1]
    return domain

def full_test(driver, domain_name):

    input_tag, text_type, email_type, email_id, email_name, \
    user_id, user_name, username_name, \
    password = email_and_password_exits(driver)

    count = 0
    email_list = test_email_list()


    while input_tag and count < 4:

        if password:

                domain = get_domain_from_uri(driver.current_url)

                if email_type:
                    test_fake_credentials(driver, email_list[count],email_type_xpath)

                if email_id:
                    test_fake_credentials(driver, email_list[count],email_id_xpath)

                if email_name:
                    test_fake_credentials(driver, email_list[count],email_name_xpath)

                if user_id:
                    test_fake_credentials(driver, email_list[count],userId_xpath)

                if user_name:
                    test_fake_credentials(driver, email_list[count],user_name_xpath)

                if username_name:
                    test_fake_credentials(driver, email_list[count],username_name_xpath)

                if text_type :
                    test_fake_credentials(driver, email_list[count],text_type_xpath)

                test_fake_password(driver)


                newDomain = get_domain_from_uri(driver.current_url)

                if newDomain != domain:
                    print('this is a phishing website because of redirect')
                    return 1
                else:
                    count += 1

                    input_tag,text_type, email_type, email_id, email_name, \
                    user_id, user_name, username_name, \
                    password = email_and_password_exits(driver)

        else:
            break

    if count < 1 and (not email_type or not email_id or not email_name) and not password:
        print('this page has no login')
        return 2

    elif not password and count < 3:
        if not email_type or not email_id or not email_name:
            print('this is a phishing website due to test')
            return 1
    else:
        print('this is a legitimate page')
        to_mongodb(domain_name)
        return 0

def get_legitimate_pages():
    text_file = open("scraper/alexa.txt", "r")
    lines = text_file.read().split('\n')
    links = []
    for line in lines:
        links.append('https://www.'+line)

    return links

def get_phishing_pages():
    jsonFile = open('scraper/links-old.json', 'r')
    data = json.load(jsonFile)
    jsonFile.close()

    link_array = []

    for index in data:
        link_array.append(index['url'])

    print(len(link_array))

    return link_array

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
                        result = full_test(driver, domain)
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
