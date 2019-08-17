import os
import time
from datetime import datetime as dt

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ResultPage(object):

    def __init__(self, driver):
        self.driver = driver

    def verif_autorization(self):
        return self.driver.find_element_by_xpath(
            '//div[@class="x-toolbar-text  ps-user-label x-box-item x-toolbar-item x-toolbar-text-default"]').text

    def check(self, source):
        self.driver.find_element_by_xpath("//span[contains(.,'%s')]" % (source + " (")).click()
        print("Зарегистрировано " + source + ": " + self.driver.find_element_by_xpath(
            '//div[text()="%s"]/../../div[1]/div[1]' % Out).text)
        return self.driver.find_element_by_xpath('//div[text()="%s"]' % Out).text

class HomePage(object):

    def __init__(self, driver):
        self.driver = driver

    def authorization(self, login):
        self.driver.find_element_by_name("ext-comp-1011-inputEl").send_keys(login)
        self.driver.find_element_by_name("ext-comp-1011-inputEl").send_keys(Keys.RETURN)
        return ResultPage(self.driver)

    def getControl(self, label):
        return self.driver.find_element_by_xpath('//div//span[text()="' + label + ':"]/../..')

    def getSubcontrol(self, control, xpath):
        return control.find_element_by_xpath('.//' + xpath)

    def fillInfo(self, source, surname, name, patronymic, mail):

        if source != "mil":
            family_name = self.getControl("Фамилия")
            self.getSubcontrol(family_name, 'div[@role="textbox"]').click()
            self.getSubcontrol(family_name, 'input').send_keys(surname)

            family_name = self.getControl("Имя")
            self.getSubcontrol(family_name, 'div[@role="textbox"]').click()
            self.getSubcontrol(family_name, 'input').send_keys(name)

            family_name = self.getControl("Отчество")
            self.getSubcontrol(family_name, 'div[@role="textbox"]').click()
            self.getSubcontrol(family_name, 'input').send_keys(patronymic)

            family_name = self.getControl("e-mail")
            self.getSubcontrol(family_name, 'div[@role="textbox"]').click()
            self.getSubcontrol(family_name, 'input').send_keys(mail)

            if source == "Лично" or source == "Письменно":
                family_name = self.getControl("Канал")
                self.getSubcontrol(family_name, 'div[@role="textbox"]').click()
                self.getSubcontrol(family_name, 'input').clear()
                self.getSubcontrol(family_name, 'input').send_keys(source)
                self.getSubcontrol(family_name, 'input').send_keys(Keys.RETURN)
            else:
                pass
        else:
            pass

        family_name = self.getControl("Исходящий №")
        self.getSubcontrol(family_name, 'div//div[@role="textbox"]').click()
        self.getSubcontrol(family_name, 'input').send_keys(numb)
        self.getSubcontrol(family_name, 'input').send_keys(Keys.RETURN)
        time.sleep(2)

    def regNewDoc(self, source):

        # mil и e-mail документы
        if source == "mil":
            self.driver.find_element_by_xpath(
                '//*[@id="z8-tree-view-1034-record-30"]/tbody/tr/td[1]/div/span').click()
            time.sleep(1)
            self.fillInfo(source, "", "", "", "")
            time.sleep(1)
        else:
            pass

        if source == "e-mail":
            self.driver.find_element_by_xpath('//*[@id="z8-tree-view-1034-record-30"]/tbody/tr/td[1]/div/span').click()
            time.sleep(1)
            self.fillInfo(source, "Иванов", "Иван", "Иванович", "ivk@ya.ru")
            time.sleep(1)
        else:
            pass

        # личный и письменный документы
        if source == "Лично" or source == "Письменно":
            self.driver.find_element_by_xpath('//span[text()="НОВОЕ"]').click()
            time.sleep(2)
            self.fillInfo(source, "Иванов", "Иван", "Иванович", "ivk@ya.ru")
            if source == "Лично":
                self.driver.find_element_by_xpath(
                    '//*[@id="ext-379"]').send_keys(
                    os.chdir(os.getcwd() + "/pytest") + "/Письмо МЧС РФ от 7 апреля 2010 г.txt")
            else:
                self.driver.find_element_by_xpath(
                    '//*[@id="ext-379"]').send_keys(
                    os.chdir(os.getcwd() + "/pytest") + "/Письмо МЧС РФ от 7 апреля 2010 г.txt")
                pass
        time.sleep(3)

        # Регистрация
        self.driver.find_element_by_xpath('//span[text()="ЗАРЕГИСТРИРОВАТЬ"]').click()
        time.sleep(3)

        global data
        data = self.driver.find_element_by_xpath(
            '//span[text()="Исходящий №:"]/../../../div[2]//div[@role="textbox"]/div').text
        global Out
        Out = str(numb) + ' от ' + str(data)
        time.sleep(2)
        return ResultPage(self.driver)


class   Test:

    def setup(self):
        self.driver = webdriver.Chrome('C:/pf_testing/wedriver/chromedriver.exe')
        self.driver.get("localhost:8080/postfactor/")
        self.driver.implicitly_wait(2)
        self.driver.maximize_window()
        global numb
        numb = dt.now().strftime('%d%m%Y%H%M%S')


    def test_Test(self):
        self.driver.implicitly_wait(10)
        self.driver.maximize_window

    def test_RegPerson(self):
        home = HomePage(self.driver)
        result = home.authorization("oj/ab")
        assert "А. В. Антонов" in result.verif_autorization()
        home.regNewDoc("Лично")
#        assert Out in result.check("Лично")

    def teardown(self):
        self.driver.quit()