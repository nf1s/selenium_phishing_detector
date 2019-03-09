# -*- coding: utf-8 -*-
"""get_login Module.

This module is created to find elements in a web-page which is responsible
from authentication (login link or a signup button). This is required for
selenium to process if a the current website requires user credentials.


"""
from selenium import webdriver
# The keys library provides keys in the keyboard like enter, ALT and so on
from selenium.common.exceptions import NoSuchElementException

operations = ['', ' ', '_', '-']
primaries = ['log', 'Log', 'LOG', 'sign', 'Sign', 'SIGN']
secondaries = ['in', 'In', 'IN', 'on', 'On', 'ON']


def check_exists_by_xpath(driver, inner_text):
    """Function checks if there are elements (buttons are links) used for login
    Args:
        driver: Instance of Selenium Web Driver

    Returns:
        bool: True if a login element is found, False Otherwise

    """
    try:
        driver.find_elements_by_xpath("//*[contains(text(), '" + inner_text + "')]")
    except NoSuchElementException:
        return False
    return True


def word_op(first, second, op):
    """Function creates the full name out of two parts and a separator

    Args:
        first: (str) first part of the name
        second: (str) second part of the name
        op: (str) separator between the two name

    Returns:
        str: full name of element

    """
    return str(first) + str(op) + str(second)


def word_combinations():
    """ Function gets the three lists (operations,primaries and secondaries)
    and creates all of the possible combinations from all of these lists
    to be used later for finding if an element for login exists on some page

    Returns:
        list: list of all possible combinations of names

    """
    word_list = []
    for op in operations:
        for second in secondaries:
            for first in primaries:
                word_list.append(word_op(first, second, op))

    return word_list


def click_element(driver, inner_text):
    """Function tries to click the login/signin element if found
        to check of selenium webdriver is able to click this element.
        if not then the test cannot be continued

    Args:
        driver: instance of selenium webdriver
        inner_text: element name


    """
    try:
        button = driver.find_elements_by_xpath("//*[contains(text(), '" + inner_text + "')]")
        button.click()
    except:
        pass


def run(url):
    driver = webdriver.Firefox()
    driver.get(url)
    word_list = word_combinations()
    for word in word_list:
        if check_exists_by_xpath(driver, word):
            click_element(driver, word)


if __name__ == "__main__":
    run('https://www.paypal.com')
