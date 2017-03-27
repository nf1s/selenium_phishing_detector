# Importing libraries for web driver
# the selenium web driver module provides all the web driver implementations.
# current supported implementations are firefox, chrome and IE
# it case be used remotely as well
from selenium import webdriver
# The keys library provides keys in the keyboard like enter, ALT and so on
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from influxdb import InfluxDBClient
import checkDomain
# Instance of the web-driver is created and firefox will start
# driver.get method will navigate firefox to the page requested
from pymongo import MongoClient

global_url = 'http://resolution-help-centers.com/www.sign-secure-update/mpp/signin/1e68/websrc'

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#------ testing part -------------------------------------------------------------#

def test_with_invalid_email_type(driver, test_email):
    email = driver.find_element_by_xpath("//input[@type='email']")
    email.send_keys(test_email)  # Your email_id
    email.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(email))


def test_with_invalid_email_id(driver, test_email):
    email = driver.find_element_by_xpath("//input[@id='email']")
    email.send_keys(test_email)  # Your email_id
    email.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(email))


def test_with_invalid_email_name(driver, test_email):
    email = driver.find_element_by_xpath("//input[@name='email']")
    email.send_keys(test_email)  # Your email_id
    email.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(email))


def test_with_invalid_password(driver):
    passwd = driver.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys("12345678")  # Your password
    passwd.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(passwd))


def invalid_data_test_email_by_type(driver, test_email):
    email = driver.find_element_by_xpath("//input[@type='email']")
    email.clear()
    email.send_keys(test_email)  # Your email_id
    passwd = driver.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys("12345678")  # Your password
    passwd.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(passwd))

    # driver will press the enter key.


def invalid_data_test_email_by_id(driver, test_email):
    email = driver.find_element_by_xpath("//input[@id='email']")
    email.clear()
    email.send_keys(test_email)  # Your email_id
    passwd = driver.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys("12345678")  # Your password
    passwd.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(passwd))


def invalid_data_test_email_by_name(driver, test_email):
    email = driver.find_element_by_xpath("//input[@name='email']")
    email.clear()
    email.send_keys(test_email)  # Your email_id
    passwd = driver.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys("12345678")  # Your password
    passwd.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(passwd))


def invalid_data_test_user_by_id(driver, test_email):
    email = driver.find_element_by_xpath("//input[@id='user']")
    email.clear()
    email.send_keys(test_email)  # Your email_id
    passwd = driver.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys("12345678")  # Your password
    passwd.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(passwd))


def invalid_data_test_user_by_name(driver, test_email):
    email = driver.find_element_by_xpath("//input[@name='user']")
    email.clear()
    email.send_keys(test_email)  # Your email_id
    passwd = driver.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys("12345678")  # Your password
    passwd.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(passwd))

    # driver will press the enter key.


def invalid_data_test_username_by_name(driver, test_email):
    email = driver.find_element_by_xpath("//input[@name='username']")
    email.clear()
    email.send_keys(test_email)  # Your email_id
    passwd = driver.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys("12345678")  # Your password
    passwd.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(passwd))


def email_and_password_exits(driver):
    input_tag = check_exists_by_xpath (driver, "//input")
    email_type = check_exists_by_xpath(driver, "//input[@type='email']")
    email_id = check_exists_by_xpath(driver, "//input[@id='email']")
    email_name = check_exists_by_xpath(driver, "//input[@name='email']")
    user_id = check_exists_by_xpath(driver, "//input[@id='user']")
    user_name = check_exists_by_xpath(driver, "//input[@name='user']")
    username_name = check_exists_by_xpath(driver, "//input[@name='username']")
    passwd = check_exists_by_xpath(driver, "//input[@type='password']")

    return  input_tag, email_type, email_id, email_name, \
           user_id, user_name, username_name, passwd


def test_email_list():
    emails = ['first.last@name.com', 'bla@bla.com', 'python@great.com']
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


def full_test(driver, domain_name):

    input_tag,email_type, email_id, email_name, \
    user_id, user_name, username_name, \
    password = email_and_password_exits(driver)

    count = 0
    email_list = test_email_list()

    try:
        while password and count < 3:

            if input_tag:

                domain = checkDomain.get_domain_from_uri(driver.current_url)

                if email_type and password:
                    invalid_data_test_email_by_type(driver, email_list[count])

                elif email_id and password:
                    invalid_data_test_email_by_id(driver, email_list[count])

                elif email_name and password:
                    invalid_data_test_email_by_name(driver, email_list[count])

                elif user_id and password:
                    invalid_data_test_user_by_id(driver, email_list[count])

                elif user_name and password:
                    invalid_data_test_user_by_name(driver, email_list[count])

                elif username_name and password:
                    invalid_data_test_username_by_name(driver, email_list[count])

                elif email_type and not password:
                    test_with_invalid_email_type(driver, email_list[count])

                elif email_id and not password:
                    test_with_invalid_email_id(driver, email_list[count])

                elif email_name and not password:
                    test_with_invalid_email_name(driver, email_list[count])

                elif password and not (email_id or email_name or email_type):
                    test_with_invalid_password(driver)

                else:
                    break

                newDomain = checkDomain.get_domain_from_uri(driver.current_url)

                if newDomain != domain:
                    print('this is a phishing website')
                    break

                count += 1

                input_tag,email_type, email_id, email_name, \
                user_id, user_name, username_name, \
                password = email_and_password_exits(driver)

            else:
                return 2

        if count < 1 and (not email_type or not email_id or not email_name) and not password:
            print('this page has no login')
            return 2

        elif not password:
            if not email_type or not email_id or not email_name:
                print('this is a phishing website')
                return 1
        else:
            print('this is a legitimate page')
            to_mongodb(domain_name)
            return 0

    except TimeoutException:
        print('test incomplete')
        return -1


def run():
    driver = webdriver.Firefox()
    url = global_url
    driver.get(url)
    domain = checkDomain.get_domain_from_uri(url)
    domain_in_whiteList = check_domain_in_white_list(domain)
    if domain_in_whiteList != None:
        print('domain is legit and in whitelist')
    else:
        result = full_test(driver, domain)
        to_influx_database(url, result)
    driver.quit()


run()
