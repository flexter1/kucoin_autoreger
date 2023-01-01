from random import randint, choice
from multiprocessing import Pool
import selenium.common.exceptions
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from loguru import logger
import os
import re
from bs4 import BeautifulSoup
from passwordgenerator import pwgenerator
import json



with open('ramblers.txt', 'r', encoding='utf-8') as file:
    rambler_acc_list = [x.rstrip() for x in file.readlines()]
with open('ua.txt', 'r', encoding='utf-8') as file:
    ua_list = [x.rstrip() for x in file.readlines()]
with open('config.json','r') as file:
    config_file = json.load(file)
    API_KEY = config_file['anti_captcha_apikey']
    trading_password = config_file['set_trading_password']
    processes_count = config_file['processes_count']

logger.info("THIS SOFTWARE WAS WRITTEN BY FLEXTER | https://t.me/flexterwork")
logger.info("CURRENT VERSION 1.0.0")

class KucoinReger:



    def create_browser(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument(f'user-agent={choice(ua_list)}')
            chrome_options.add_argument('--disable-blink-feature=AutomationControlled')
            chrome_options.add_extension((os.path.abspath('anticaptcha-plugin_v0.62.crx')))
            browser = webdriver.Chrome(service=Service(os.path.abspath('chromedriver')), options=chrome_options)
            browser.maximize_window()
            browser.get('chrome-extension://lncaoejhfdpcafpkkcddpjnhnodcajfg/options.html')
            browser.implicitly_wait(5)
            api_key = browser.find_element(By.CSS_SELECTOR,
                                           'body > div > div.options_form > input[type=text]:nth-child(7)')
            api_key.send_keys(API_KEY)

            log_in_button = browser.find_element(By.CSS_SELECTOR, 'body > div > input').click()

            return browser
        except Exception as ex:
            logger.error(ex)
            browser.quit()

    def rambler_login(self, log_pass:str):
        try:
            login, password = log_pass.split(':')
            browser = self.create_browser()
            browser.get('https://mail.rambler.ru/?utm_source=head&utm_campaign=self_promo&utm_medium=header&utm_content=mail')
            browser.implicitly_wait(15)
            browser.switch_to.frame(browser.find_element(By.CSS_SELECTOR,'#root > div > div.c021 > div.c0219 > iframe'))
            email_input = browser.find_element(By.CSS_SELECTOR,'#login').send_keys(login)
            password_input = browser.find_element(By.CSS_SELECTOR,'#password').send_keys(password)
            browser.find_element(By.CSS_SELECTOR,'#__next > div > div > div.styles_popup__hP12r > div > div > div > div.styles_leftColumn__k_O3r > form > button > span').click()
            sleep(5)
            if browser.page_source.find('Поиск по почте')!=-1:
                logger.info(f'Успешно вошел в почту | Аккаунт: {log_pass}')

                browser.get('https://id.rambler.ru/account/change-password')
                browser.implicitly_wait(15)
                sleep(3)
                current_password_input = browser.find_element(By.CSS_SELECTOR,'#password').send_keys(password)
                new_password = f"{pwgenerator.generate().replace('#', '').replace('=','').replace(':', '').replace(';','').replace('.','').replace(',','')[:10]}1@aA"
                input_new_password = browser.find_element(By.CSS_SELECTOR,'#newPassword').send_keys(new_password)
                sleep(60)
                save_button = browser.find_element(By.CSS_SELECTOR,'body > div:nth-child(9) > div > div > div > form > footer > button.rui-Button-button.rui-Button-type-primary.rui-Button-size-medium.rui-Button-iconPosition-left > span').click()
                browser.get('https://mail.rambler.ru/folder/INBOX')
                browser.implicitly_wait(15)
                sleep(10)
                if browser.page_source.find('Изменение пароля в Rambler')!=-1:
                    logger.info(f'Успешно изменил пароль в почте Rambler | {login}:{new_password}')
                    with open('new_rambler_passes.txt', 'a+') as file:
                        file.writelines(f'{login}:{new_password}\n')
                    return [True, browser, login, new_password]
            else:
                browser.quit()
                return [False]
        except:
            browser.quit()
            return [False]

    def kucoin_reger(self, log_pass:str):
        def get_code(last_code):
            browser.switch_to.window(browser.window_handles[0])
            sleep(10)
            browser.get('https://mail.rambler.ru/folder/INBOX')
            browser.implicitly_wait(15)
            sleep(5)
            if browser.page_source.find('KuCoin Verification Code') != -1:
                last_two_messages = browser.find_elements(By.CLASS_NAME, 'ListItem-snippet-1a')[:2]
                for message in last_two_messages:
                    try:
                        code = (re.search(r"\d+", message.text).group())
                        if int(code)!=int(last_code):
                            return code
                    except:
                        pass
            else:
                browser.find_element(By.CSS_SELECTOR,
                                     '#app > div.App-root-hg > div.AppContainer-root-3m.AppContainer-withRightAdMax-Bm.AutoAppContainer-root-2P > div.AutoAppContainer-inner-1B > div.AutoAppContainer-sidebar-LW > div.FoldersSidebar-root-1a > div:nth-child(1) > div > ul > li:nth-child(5) > div > a').click()
                sleep(3)
                browser.implicitly_wait(3)
                if browser.page_source.find('KuCoin Verification Code') != -1:
                    code = re.search(r"\d+", browser.find_element(By.CLASS_NAME, 'ListItem-snippet-1a').text).group()
                    if int(code) != int(last_code):
                        return code

        result = self.rambler_login(log_pass)
        try:        
            if result[0] is True:
                browser = result[1]
                email = result[2]
                password = result[3]
                browser.switch_to.new_window()
                browser.get('https://www.kucoin.com/ru/ucenter/signup?spm=kcWeb.B1homepage.register.1')
                browser.implicitly_wait(15)

                email_input = browser.find_element(By.CSS_SELECTOR,'#email').send_keys(email)
                password_input = browser.find_element(By.CSS_SELECTOR,'#password').send_keys(f'{password}{password}')
                register_button = browser.find_element(By.CSS_SELECTOR,'#root > div > div > div > div > div.box_container___33QNB.signup_page___1CtX6 > div > div > div > div.KuxCol-col.KuxCol-14-col.lrtcss-1ufd3pb > div > div.KuxBox-root.lrtcss-xl471x > form > button').click()
                sleep(15)
                success = 0
                for i in range(3):
                    try:
                        code_input = browser.find_element(By.CSS_SELECTOR, '#root > div > div > div > div > div.box_container___33QNB.signup_page___1CtX6 > div > div > div > div.KuxCol-col.KuxCol-14-col.lrtcss-1ufd3pb > div > div.lrtcss-12a29vk > div.KuxInput-container.KuxInput-largeContainer.lrtcss-1rn3ul7 > input')
                        success = 1
                        break

                    except Exception as exc:
                        logger.info(f'Решаю капчу... {email}')
                        sleep(10)
                        success = 0
                if success == 1:
                    code1 = get_code(last_code=0)
                    if code1!='':
                        browser.switch_to.window(browser.window_handles[1])
                        code_input.send_keys(code1)
                        activate_button = browser.find_element(By.CSS_SELECTOR,'#root > div > div > div > div > div.box_container___33QNB.signup_page___1CtX6 > div > div > div > div.KuxCol-col.KuxCol-14-col.lrtcss-1ufd3pb > div > div.lrtcss-12a29vk > button').click()
                        browser.implicitly_wait(10)
                        sleep(15)
                        if browser.page_source.find('Основной Аккаунт')!=-1:
                            logger.info(f'Успешно зарегистрировал Kucoin аккаунт | {email}:{password}{password}')
                            with open('kucoin_accs_without_data.txt','a+') as file:
                                file.writelines(f"{email}:{password}{password}")
                            #enable trade password
                            browser.get('https://www.kucoin.com/ru/account/security/protect')
                            browser.implicitly_wait(15)
                            browser.find_element(By.CSS_SELECTOR,'#__SEND_VCODE__EMAIL').click()
                            sleep(3)
                            code = get_code(last_code=code1)
                            browser.switch_to.window(browser.window_handles[1])
                            code_input = browser.find_element(By.CSS_SELECTOR,'#my_email > div > input').send_keys(code)
                            sleep(5)
                            browser.find_element(By.CSS_SELECTOR,'body > div.KuxDialog-root.KuxDialog-basic.lrtcss-1fknefy > div.KuxDialog-body.KuxDialog-basic.lrtcss-smus82 > div.KuxDialog-content.lrtcss-14ijqpp > div > button').click()
                            input_trade_pass = browser.find_element(By.CSS_SELECTOR,'#SetForm_password').send_keys('020204')
                            confirm_input_trade_pass = browser.find_element(By.CSS_SELECTOR,'#SetForm_passwordr').send_keys(trading_password)
                            confirm_button = browser.find_element(By.CSS_SELECTOR,'#SetForm > div > div.formBody___-reP3 > button').click()
                            sleep(10)
                            browser.implicitly_wait(10)
                            if browser.page_source.find('Пароль для Входа')!=-1:
                                logger.info(f"Успешно установил торговый пароль {trading_password} | {email}:{password}{password}")

                                #get_wallet
                                browser.get('https://www.kucoin.com/ru/assets/coin/USDT?spm=kcWeb.B1assetsMain.assetsList.deposti')
                                browser.implicitly_wait(15)
                                sleep(3)
                                browser.find_element(By.CSS_SELECTOR,'#root > div > div > div.body___1UbSf > div.box___3B-ao.thinBox___1y67J > div > div > section > div > div.content___314Eg > div > section.css-1usvh99 > div:nth-child(2) > div > div > span').click()
                                sleep(3)
                                browser.implicitly_wait(3)
                                browser.find_element(By.CSS_SELECTOR,'body > div.lrtcss-11ebto9 > div > div.lrtcss-1gx5y8y > div > div:nth-child(2)').click()
                                sleep(7)
                                address = browser.find_element(By.CSS_SELECTOR,'#root > div > div > div.body___1UbSf > div.box___3B-ao.thinBox___1y67J > div > div > section > div > div.content___314Eg > div > div > div > div > section > p').text
                                logger.info(f'Успешно получил адрес депозита | {email}:{password}{password}')
                                change = browser.find_element(By.CSS_SELECTOR,'#root > div > div > div.body___1UbSf > div.box___3B-ao.thinBox___1y67J > div > div > section > div > div.content___314Eg > div > div > section > div > div:nth-child(1) > section > div > p > span.css-ant644').click()
                                sleep(3)
                                browser.find_element(By.CSS_SELECTOR,'body > div.lrtcss-11ebto9 > div > div.lrtcss-1gx5y8y > section > p:nth-child(2) > span.css-1ceshgx > span').click()
                                sleep(3)
                                logger.info(f'Успешно изменил депозит с основного на торговый аккаунт | {email}:{password}{password}')

                                avatar = ActionChains(browser).move_to_element(browser.find_element(By.CSS_SELECTOR,'#hook_nav_user > div > div:nth-child(4) > div > div > div > div')).perform()
                                sleep(15)
                                browser.implicitly_wait(5)
                                try:                                
                                    uid = re.search(r"\d+",browser.find_element(By.CLASS_NAME, 'uid').text).group()
                                    with open('kucoin_accs_with_data.txt', 'a+') as file:
                                        file.writelines(f'{email}:{password}{password}:{address}:{uid}\n')
                                    logger.info(f'Успешно собрал UID | {email}:{password}{password}')
                                    logger.success(f'Завершаю работу с аккаунтом | {email}:{password}{password}')
                                    browser.quit()
                                except:
                                    with open('kucoin_accs_with_data.txt', 'a+') as file:
                                        file.writelines(f'{email}:{password}{password}:{address}\n')
                else:
                    browser.quit()
        except TypeError:
            pass

    def main(self):
        Pool(processes=processes_count).map(self.kucoin_reger, rambler_acc_list)

if __name__ == '__main__':
    KucoinReger().main()
