from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path="wedriver/chromedriver.exe")
driver.get('localhost:8080/postfactor')
driver.implicitly_wait(3)
driver.maximize_window()

driver.find_element_by_name("ext-comp-1011-inputEl").send_keys("oj/ab")
driver.find_element_by_name("ext-comp-1011-inputEl").send_keys(Keys.RETURN)