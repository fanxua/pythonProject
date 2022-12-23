import time
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

name = 'dbxq3647@adshe.asia'
password = 'atgj5192'
chrome_options = ChromeOptions()
chrome_options.add_argument("--load-extension=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default/Extensions/mpbjkejclgfgadiemmefgebjfooflfhl/1.3.2_0")
driver = Chrome(options=chrome_options)
# driver.implicitly_wait(30)
driver.get('https://chat.openai.com/chat')
time.sleep(10)
driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[4]/button[1]').click()
time.sleep(5)
# import pyautogui,time
#
# time.sleep(1)
# x,y = pyautogui.position()
# print('鼠标位置：x=%d,y=%d'%(x,y))
#
# # pyautogui.moveTo(x=121, y=425)
# time.sleep(4)


ActionChains(driver).move_by_offset(530, 419).click().perform()
# driver.find_element(By.XPATH,'//*[@id="rc-anchor-container"]/div[3]/div[2]').click()
# time.sleep(50)
# driver.switchTo().frame()
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='c-'][src^='https://www.recaptcha.net/recaptcha/enterprise/bframe?']")))
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
time.sleep(5)
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="solver-button"]'))).click()

# h = driver.window_handles
# print(h)
# but = driver.find_element_by_css('button.solver-button')
# print(but)
# but.click()
show = driver.find_element(By.XPATH,'//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[4]')
show = driver.execute_script("return arguments[0].shadowRoot.querySelector('button[@id=\"solver-button\"]')",show)
print(show)
# show.find_element_by_id_name('solver-button').click()
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="uc-center-container"]/div[2]/div/div/div/div[1]/button'))).click()
import pyautogui,time

time.sleep(2)
x,y = pyautogui.position()
print('鼠标位置：x=%d,y=%d'%(x,y))

pyautogui.moveTo(x=615, y=936)
time.sleep(4)
ActionChains(driver).move_by_offset(x=615, y=936).click().perform()
time.sleep(5)
# iframe = driver.find_element_by_name('c-mquw7zhsunyj')
# print(iframe)
# driver.switch_to.frame(iframe)
# driver.find_element(By.XPATH,'//*[@id="solver-button"]').click()
# time.sleep(5)

# driver.find_element(By.XPATH,'//*[@id="solver-button"]').click()
time.sleep(5)
driver.switch_to.parent_frame()
name = driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(name)
qd = driver.find_element(By.XPATH, '/html/body/main/section/div/div/div/form/div[2]/button').click()
password =driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(password)
time.sleep(5)
qd1 = driver.find_element(By.XPATH,'/html/body/main/section/div/div/div/form/div[2]/button').click()
time.sleep(5)