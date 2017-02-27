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

global_url = 'http://www.paypal.com/signin'


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def test_with_invalid_email_type(driver,test_email):
    email = driver.find_element_by_xpath("//input[@type='email']")
    email.send_keys(test_email)  # Your email_id
    email.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(email))

def test_with_invalid_email_id(driver,test_email):
    email = driver.find_element_by_xpath("//input[@id='email']")
    email.send_keys(test_email)  # Your email_id
    email.send_keys(Keys.RETURN)
    WebDriverWait(driver, 5).until(EC.staleness_of(email))

def test_with_invalid_email_name(driver,test_email):
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
    email = driver.find_element_by_xpath("//input[@name='Email']")
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


def email_and_password_exits(driver):
    email_type = check_exists_by_xpath(driver, "//input[@type='email']")
    email_id = check_exists_by_xpath(driver, "//input[@id='email']")
    email_name = check_exists_by_xpath(driver, "//input[@name='email']")
    user_id = check_exists_by_xpath(driver, "//input[@id='user']")
    user_name = check_exists_by_xpath(driver, "//input[@name='user']")
    passwd = check_exists_by_xpath(driver, "//input[@type='password']")

    return email_type, email_id, email_name, user_id, user_name, passwd


def test_email_list():
    emails = ['first.last@name.com', 'bla@bla.com', 'python@great.com']
    return emails


def full_test(driver):
    email_type, email_id, email_name, user_id, user_name, password = email_and_password_exits(driver)
    count = 0
    email_list = test_email_list()

    try:
        while password and count < 3:

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

            elif email_type and not password:
                test_with_invalid_email_type(driver, email_list[count])

            elif email_id and not password:
                test_with_invalid_email_id(driver, email_list[count])

            elif email_name and not password:
                test_with_invalid_email_name(driver, email_list[count])

            elif password and not ( email_id or email_name or email_type):
                test_with_invalid_password(driver)

            else:
                break

            newDomain = checkDomain.get_domain_from_uri(driver.current_url)

            if newDomain != domain:
                print('this is a phishing website')
                break

            count += 1
            email_type, email_id, email_name, user_id, user_name, password = email_and_password_exits(driver)

        if count == 0 and (not email_type or not email_id or not email_name) and not password:
            print('this page has no login')
            return 2

        elif not password:
            if not email_type or not email_id or not email_name:
                print('this is a phishing website')
                return 1
        else:
            print('this is a legitimate page')
            return 0

    except TimeoutException:
        print('test incomplete')
        return -1


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
        db_client = InfluxDBClient('localhost', '8086', 'root', 'root', 'phishing_db')
        db_client.create_database('phishing_db')
        db_client.write_points(points)

    except IOError as error:
        print(str(error))


def run():
    driver = webdriver.Firefox()

    url = global_url
    driver.get(url)

    result = full_test(driver)

    to_influx_database(url, result)

    driver.quit()


run()
