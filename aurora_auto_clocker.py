import time
import logging
import random
from xpath_dict import xpath_dict
from xmlrpc.client import Boolean
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.action_chains import ActionChains

class AuroraAutoClocker:
    # logger = logging.getLogger("auto-clocker-static")
    def __init__(self, url='https://login.aoacloud.com.tw/Home/MobileAuthIndex') -> None:
        self.logger = logging.getLogger("aurora-auto-clocker")
        self._url = url
        self._driver = None
        # self._open_Chrome()
        self._open_Firefox()
        self._login_fields = [xpath_dict['公司'],xpath_dict['帳號'],xpath_dict['密碼']]
        self._credentials = []
        self._on_hour, self._off_hour, self._on_off_min = None, None, None
        self.logger.info("[Done] instantiated AutoClocker")
        
    def _open_Firefox(self):
        try:
            self._driver = webdriver.Firefox()
            self._driver.minimize_window()
            self._driver.set_window_size(1280,720) 
            #self._driver.set_window_position(-100000,0)
            self._driver.get(self._url)
            self.logger.info("[Done] opened Aurora webpage in Firefox")
        except Exception as e:
            self.logger.error(f"open the Aurora webpage in Firefox: {e}")

    def _open_Chrome(self):
        try:
            self.chrome_options = webdriver.ChromeOptions()
            self.chrome_options.add_argument('--no-sandbox')
            self.chrome_options.add_argument('--disable-dev-shm-usage')
            self._driver = webdriver.Chrome()
            self._driver.minimize_window()
            self._driver.set_window_size(1280,720) 
            #self._driver.set_window_position(-100000,0)
            self._driver.get(self._url)
            self.logger.info("[Done] opened Aurora webpage in Chrome")
        except Exception as e:
            self.logger.error(f"open the Aurora webpage in Chrome: {e}")

    @property
    def browser_id(self):
        self.logger.info(f"[Done] returnning the browser session id {self._driver.session_id}")
        return self._driver.session_id

    @property
    def browser_title(self):
        try: 
            title = self._driver.title
            self.logger.info(f"[Done] returnning the title of the browser: {title}")
            return title
        except Exception as e:
            self.logger.warning(f"accessing the browser {e}")
            return None

    def _sleep_for_a_second_after_calling(func):
        def take_a_pause(*args):
            func(*args)
            time.sleep(1)
            #self.logger.debug("[Done] sleeping 1 second")
        return take_a_pause

    def _sleep_for_two_seconds_after_calling(func):
        def take_a_pause(self, target):
            func(self, target)
            time.sleep(2)
            self.logger.debug("[Done] sleeping 2 seconds")
        return take_a_pause

    def login(self, credentials=['qd9323', '123456', 'A123456789']) -> Boolean:
        self._credentials = credentials
        try:
            # 輸入credentials 並登入
            for (field,cred) in zip(self._login_fields,self._credentials):
                self._driver.find_element_by_xpath(field).send_keys(cred)
            option = '登入' if (self._driver.current_url == self._url) else '登入web'
            self._driver.find_element_by_xpath(xpath_dict[option]).click()

            # 選到 to 補登頁面
            self._driver.find_element_by_xpath(xpath_dict['人資系統']).click()
            WebDriverWait(self._driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_dict['考勤補登申請單']))).click()
            self.logger.info("[Done] login to the Aurora")
            return True       
        except Exception as e:
            self.logger.error(f"login to the Aurora: {e}")
            return False
    
    @_sleep_for_two_seconds_after_calling
    def press_button(self, target):
        try:
            self._driver.find_element_by_xpath(xpath_dict[str(target)]).click()
            self.logger.info(f"[Done] press the button: {target}")
        except Exception as e:
            self.logger.error(f"press the button {target}: {e}")
        if target == '送出':
                time.sleep(3.5)

    # #todo: is it better to implement this method to static/class method?
    def gen_random_duty_time(self):
        on_off_min = f"{random.randint(30,60)}分\n"
        if on_off_min == "60分\n":
            on_off_min = "00分" 
        on_hour = "09時\n" if on_off_min == "60分\n" else "08時\n"
        off_hour = "18時\n" if on_off_min == "60分\n" else "17時\n"
        
        self._on_hour, self._off_hour, self._on_off_min = on_hour, off_hour, on_off_min
        self.logger.info(f"[Checked] the generated random on/off time: On-Hour: {on_hour},  Off-Hour: {off_hour}, Min: {on_off_min}")

    # Select the time: 'Hour' and check whether to toggle to Off work
    def select_time(self, clkin=True, y=2024, m=6, d=11):
        # 20220309選擇小時: 原本的寫法, 只有改變到HTML的外觀!! 
        # btnHour = self._driver.find_element_by_xpath('//*[@id="MainContent_drpHour_chosen"]/a/span')
        btnHour = self._driver.find_element_by_xpath(xpath_dict['小時'])
        btnMin = self._driver.find_element_by_xpath(xpath_dict['分鐘'])
        btnOffDuty = self._driver.find_element_by_xpath(xpath_dict['卡別'])

        if not clkin:
            # 20220309選擇小時: 原本的寫法, 只有改變到HTML的外觀!!  
            #self._driver.execute_script('arguments[0].innerHTML = "18時";', btnHour)
            self._driver.execute_script("arguments[0].setAttribute('class','chosen-container chosen-container-single chosen-container-active chosen-with-drop')", btnHour)
            self._driver.find_element_by_xpath(xpath_dict['小時按鈕']).send_keys(self._off_hour)

            # 20220309選擇下班卡別: 震旦JS code會去判斷是否有"checked" 這個attribute, 透過JS 將此attr設為false 使卡別判斷可進到下班條件產生 sS_type: 0002
            self._driver.execute_script("arguments[0].setAttribute('class', 'switch-off switch-animate')", btnOffDuty)
            btnOffDutyCheck = self._driver.find_element_by_xpath(xpath_dict['卡別按鈕'])
            self._driver.execute_script("arguments[0].checked = false;",btnOffDutyCheck)
            time.sleep(1)       
        else:
            # 20220309選擇小時: 原本的寫法, 只有改變到HTML的外觀!!  
            #self._driver.execute_script('arguments[0].innerHTML = "09時";', btnHour)
            self._driver.execute_script("arguments[0].setAttribute('class','chosen-container chosen-container-single chosen-container-active chosen-with-drop')", btnHour)
            self._driver.find_element_by_xpath(xpath_dict['小時按鈕']).send_keys(self._on_hour)

        # Select the 'Min'
        self._driver.execute_script("arguments[0].setAttribute('class','chosen-container chosen-container-single chosen-container-active chosen-with-drop')", btnMin)
        self._driver.find_element_by_xpath(xpath_dict['分鐘按鈕']).send_keys(self._on_off_min)

        # Select the 'Date'
        date = f'day_Click({y},{m},{d});'
        month_year = f'{m}\t{y}\t'
        self.logger.info("[Done] received date: " + date)

        try:
            self._driver.find_element_by_xpath(xpath_dict['月曆按鈕']).click()
            time.sleep(1)
            iFrame = self._driver.find_element_by_xpath(xpath_dict['月曆'])
            self._driver.switch_to.frame(iFrame)
            # xpath_target_date = "//td[.='{}']".format(target_date)
            self._driver.find_element_by_xpath(xpath_dict['月份按鈕']).click()
            self._driver.find_element_by_xpath(xpath_dict['月份按鈕']).send_keys(month_year)
            xpath_target_date = "//td[@onclick='{}']".format(date)
            self._driver.find_element_by_xpath(xpath_target_date).click()
            self._driver.switch_to.parent_frame()
            self.logger.info("[Done] selecting the date: " + xpath_target_date)
        except Exception as e:
            self.logger.error(f"selecting the date: {xpath_target_date}: {e}")

    def close(self):
        self._driver.close()
        self.logger.info("[Done] close the web browser driver")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
    handlers=[logging.FileHandler('aurora_auto_clock.log', 'w', 'utf-8')])

    atclk = AuroraAutoClocker()
    atclk.login()

    atclk.gen_random_duty_time()
    atclk.press_button('申請')
    atclk.select_time(clkin=True)
    atclk.press_button('存檔')
    atclk.press_button('關閉')

    atclk.press_button('申請')
    atclk.select_time(clkin=False)
    atclk.press_button('存檔')
    atclk.press_button('關閉')

    atclk.close()