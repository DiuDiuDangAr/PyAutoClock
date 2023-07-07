from web_controller import WebController
from selenium import webdriver
import logging
import requests
from bs4 import BeautifulSoup

class EssSyncer(WebController):
    def __init__(self):
        self.logger = logging.getLogger("ess-syncer")
        self._driver = None
        self._url = "https://cn-sha-hrm1.ni.corp.natinst.com/PlatinumHRM-ESS/logon.aspx"

    def _open_Chrome(self):
        try:
            self._driver = webdriver.Chrome()
            self._driver.get(self._url)
            self.logger.info("[Done] opened a webpage in Chrome")
        except Exception as e:
            self.logger.error(f"open a webpage in Chrome: {e}")

    def login(self, id, pwd):
        self._driver.find_element_by_xpath('//*[@id="ctl00_mainContent_txtUsername"]').send_keys(id)
        self._driver.find_element_by_xpath('//*[@id="txtPasswordFront"]').send_keys(pwd)
        self._driver.find_element_by_xpath('//*[@id="ctl00_mainContent_btnLogon"]').click()

    def press_btn(self, target):
        self._driver.find_element_by_xpath(target).click()

    def browse_webpage(self, tgt_url):
        self._driver.get(tgt_url)

    def crawl_web(self):
        response = requests.get('https://cn-sha-hrm1.ni.corp.natinst.com/PlatinumHRM-ESS/WebPages/MyTime/MyLeaveDetails.aspx?tab=ESS_11')
        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.find_all("tr", id="ctl00_mainContent_gridLeaveDetailsView_row_0")
        print(result)
        # date = soup.find_all()

    def wait_element_appear(self):
        pass


if __name__ == "__main__":
    print("ok")
    ess_syncer = EssSyncer()
    ess_syncer._open_Chrome()
    ess_syncer.login(422631, "Aa791024!")
    ess_syncer.browse_webpage('https://cn-sha-hrm1.ni.corp.natinst.com/PlatinumHRM-ESS/WebPages/MyTime/MyLeaveDetails.aspx?tab=ESS_11')
    ess_syncer.crawl_web()