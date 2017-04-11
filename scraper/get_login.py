from selenium import webdriver
# The keys library provides keys in the keyboard like enter, ALT and so on
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, ErrorInResponseException

def check_exists_by_xpath(driver, inner_text):
    try:
        driver.find_elements_by_xpath("//*[contains(text(), '"+inner_text+"')]")
    except NoSuchElementException :
        return False
    return True


operations = ['',' ','_','-']
primaries = ['log','Log','LOG','sign','Sign','SIGN']
secoundaries = ['in','In','IN','on','On','ON']

def word_op(first,second,op):
    return str(first)+str(op)+str(second)

def word_combinations():
    for op in operations:
        for second in secoundaries:
            for first in primaries:
                print(word_op(first,second,op))

if __name__== "__main__":
    word_combinations()