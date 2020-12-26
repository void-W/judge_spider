from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time


INDEX_URL = "https://wenshu.court.gov.cn/"
PHONE_NUM = "17621626837"
PWD = "Qwe1994422."


class firefoxdriver(object):
    """
    docstring
    """

    def __init__(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        self.__driver = webdriver.Firefox(options=options)
        self.__wait = WebDriverWait(self.__driver, 20)
        account, pwd = get_account_info()
        self.__account = account
        self.__pwd = pwd
        self.__driver.get("https://www.baidu.com")
        self.__login()

    def get_data(self, key_word):
        self.__login()
        self.__wait_by_class("advenced-search").click()
        self.__wait_by_id("s17").send_keys(key_word)
        self.__wait_by_id("searchBtn").click()
        items = self.__wait_by_class_batch("LM_list")
        data = []
        for i in items:
            result = parse(i)
            data.append(result)
        self.__driver.get(INDEX_URL)  # 返回首页，重置搜索条件
        return data

    def __get_judge(self):
        if self.__is_in_judge():
            return
        self.__driver.execute_script(
            'window.open("https://wenshu.court.gov.cn/")')
        window_list = self.__driver.window_handles
        self.__driver.switch_to.window(window_list[-1])
        time.sleep(0.5)

    def __is_in_judge(self):
        return INDEX_URL in self.__driver.current_url

    def __is_logined(self):
        login = self.__wait_by_id_batch("loginLi")
        if len(login) == 0:
            return False
        return not login[0].text == "登录"

    def __login(self):
        self.__get_judge()
        if self.__is_logined():
            return
        login_url = INDEX_URL + self.__wait_by_id("loginLi").find_element_by_tag_name(
            "a").get_attribute("onclick")[8:-2]
        self.__driver.get(login_url)

        frame = self.__wait_by_id("contentIframe")
        self.__driver.switch_to.frame(frame)
        self.__wait_by_class("phone-number-input").send_keys(self.__account)
        self.__wait_by_class("password").send_keys(self.__pwd)
        self.__wait_by_class("login-button-container").click()
        time.sleep(1)
        self.__driver.switch_to.default_content()

    def __wait_by_class(self, class_name):
        return self.__wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

    def __wait_by_class_batch(self, class_name):
        return self.__wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))

    def __wait_by_id(self, id):
        return self.__wait.until(EC.presence_of_element_located((By.ID, id)))

    def __wait_by_id_batch(self, id):
        return self.__wait.until(EC.presence_of_all_elements_located((By.ID, id)))


def get_account_info():
    return PHONE_NUM, PWD


def parse(item):
    return {
        "doc_type": item.find_element_by_class_name("labelTwo").text,
        "title": item.find_element_by_class_name("caseName").text,
        "court": item.find_element_by_class_name("slfyName").text,
        "doc_id": item.find_element_by_class_name("ah").text,
        "date": item.find_element_by_class_name("cprq").text,
        "reason": item.find_element_by_tag_name("p").text
    }
