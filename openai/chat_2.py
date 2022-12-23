import json
from pymongo import MongoClient
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import random
import requests
import os
import pydub
from speech_recognition import Recognizer, AudioFile
import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options



name = 'johngarrett1848@snapmail.cc'
password = 'ngarrett1848123'

client = MongoClient(host='34.72.119.207', port=30228,username='root',password='yV3UX5moXGzlnSxB')
db = client.openai
col_meta = db.openai_account1



def get_cookie(id,name,password):
    options = uc.ChromeOptions()
    options.add_argument("--incognito")#匿名
    options.add_argument('--headless')#无头
    print(1)
    driver = uc.Chrome(options=options)
    print(2)
    driver.get('https://chat.openai.com/chat')

    try:
        time.sleep(10)
        driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/button[1]').click()
        time.sleep(5)
        # time.sleep(5)
        name = driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(name)
        time.sleep(2)

        recaptcha_iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "//iframe[@title='reCAPTCHA']"
        )))
        driver.switch_to.frame(recaptcha_iframe)
        driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border").click()
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@title='recaptcha challenge expires in two minutes']"))
        time.sleep(random.random()*10)
        driver.find_element(By.ID, "recaptcha-audio-button").click()
        time.sleep(random.random()*10)
        # 点击播放按钮
        try:
            driver.find_element(By.XPATH, "//button[@aria-labelledby]").click()
        except NoSuchElementException:
            print("没有找到audio url")
        # 定位声源文件 url
        audio_url = driver.find_element(By.ID, "audio-source").get_attribute("src")

        path_audio_mp3 = "audio.mp3"
        path_audio_wav = "audio.wav"
        # 将声源文件下载到本地
        print(audio_url)
        res = requests.get(audio_url)
        try:
            os.remove("audio.mp3")
        except Exception:
            audio_file = open("audio.mp3", "wb")
            audio_file.write(res.content)
            audio_file.close()
        else:
            audio_file = open("audio.mp3", "wb")
            audio_file.write(res.content)
            audio_file.close()
        # 转换音频格式 mp3 --> wav
        pydub.AudioSegment.from_mp3(path_audio_mp3).export(path_audio_wav, format="wav")

        language = "en-US"
        language = "en-US" if language is None else language
        # 将音频读入并切割成帧矩阵
        recognizer = Recognizer()
        audio_file = AudioFile(path_audio_wav)
        with audio_file as stream:
            audio = recognizer.record(stream)
        # 流识别
        answer: str = recognizer.recognize_google(audio, language=language)
        # 返回短音频对应的文本(str)，en-US 情况下为不成句式的若干个单词

        try:
            # 定位回答框
            input_field = driver.find_element(By.ID, "audio-response")
            # 提交文本数据
            input_field.clear()
            input_field.send_keys(answer.lower())
            # 使用 clear + ENTER 消除控制特征
            input_field.send_keys(Keys.ENTER)
        except (NameError, NoSuchElementException):
            print("提交失败")

        time.sleep(3+3*random.random())
        driver.switch_to.parent_frame()
        qd = driver.find_element(By.XPATH, '/html/body/main/section/div/div/div/form/div[2]/button').click()
        password = driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
        time.sleep(5)
        qd1 = driver.find_element(By.XPATH, '/html/body/main/section/div/div/div/form/div[2]/button').click()
        time.sleep(5)
        cook = driver.get_cookies()
        cook1 = json.dumps(cook)
        cook2 =json.loads(cook1)
        cookie = [item["name"] + "=" + item["value"] for item in cook2]
        cookiestr = '; '.join(item for item in cookie)
        print('cookies',cookiestr)
        time.sleep(1)
        col_meta.update_one({"_id": id}, {"$set": {'cookies': cookiestr}})
        col_meta.update_one({"_id": id}, {"$set": {'status': '2'}})
        driver.quit()
    except Exception as e:
        print(e)
        driver.quit()




if __name__ == '__main__':
    while 1:
        print('开始运行')
        alls = col_meta.find({ '$and' : [{"status" : "1"}, {"server" : 1}] })
        for all in alls:
            print(all)
            print(3)
            try:
                name = all['name']
                password = all['password']
                id = all['_id']
                get_cookie(id, name, password)
            except Exception as e:
                print('出现验证码', e)
        time.sleep(300)