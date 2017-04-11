from selenium import webdriver
# The keys library provides keys in the keyboard like enter, ALT and so on
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, ErrorInResponseException


operations = ['',' ','_','-']
primaries = ['log','Log','LOG','sign','Sign','SIGN']
secoundaries = ['in','In','IN','on','On','ON']

def check_exists_by_xpath(driver, inner_text):
    try:
        driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")
        # driver.find_element_by_xpath("//input[@value='"+inner_text+"']")
    except NoSuchElementException :
        return False
    return True



def word_op(first,second,op):
    return str(first)+str(op)+str(second)

def word_combinations():
    word_list = []
    for op in operations:
        for second in secoundaries:
            for first in primaries:
               word_list.append(word_op(first,second,op))

    return word_list

def click_element(driver,inner_text):
    try:
        button = driver.find_elements_by_xpath("//*[contains(text(), '"+inner_text+"')]")
        button.click()
    except:
        pass

def run(url):
    driver = webdriver.Firefox()
    driver.get(url)
    word_list = word_combinations()
    for word in word_list:
        if check_exists_by_xpath(driver,word):
            click_element(driver,word)

if __name__== "__main__":
    run('https://www.paypal.com')