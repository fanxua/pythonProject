from selenium import webdriver
import time,base64,json
# #声明浏览器对象
from pymongo import MongoClient
from selenium.webdriver.common.by import By
import urllib.parse
import hashlib

client = MongoClient(host='34.72.119.207', port=30228,username='root',password='yV3UX5moXGzlnSxB')
db = client.openai
col_meta = db.openai_account1



def getcookies(id,name,password):
    # #访问页面
    path = r'C:\Users\Administrator\Desktop\Chrome\Application\chromedriver.exe'
    browser1 = webdriver.Chrome()
    browser1.get("https://chat.openai.com/chat")

    time.sleep(5)
    browser1.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[4]/button[1]').click()
    time.sleep(4)
    name = browser1.find_element(By.XPATH,'//*[@id="username"]').send_keys(name)
    # try:
    #     yzm = browser1.find_element_by_xpath('//form/div/div/div/div/img')
    #     yzm.screenshot('5.png')
    #     if len(str(yzm))>4:
    #
    #         yzm1 = getyzm(yzm)
    #         print(yzm1)
    #     time.sleep(3)
    #     #关闭当前窗口
    #     browser1.close()
    #     # nhvchp7660345
    # except:
    #     print('cw')

    qd = browser1.find_element(By.XPATH, '/html/body/main/section/div/div/div/form/div[2]/button').click()
    password =browser1.find_element(By.XPATH,'//*[@id="password"]').send_keys(password)
    time.sleep(5)
    qd1 = browser1.find_element(By.XPATH,'/html/body/main/section/div/div/div/form/div[2]/button').click()
    time.sleep(5)
    token =browser1.execute_script('return localStorage.getItem("AuthToken");')


    print('token',token)
    try:
        qr = browser1.find_element(By.XPATH,'//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/h4').text
        if  'This is a f' in str(qr):

            cook =browser1.get_cookies()
            cook1 = json.dumps(cook)
            cook2 =json.loads(cook1)
            cookie = [item["name"] + "=" + item["value"] for item in cook2]
            cookiestr = '; '.join(item for item in cookie)
            print('cookies',cookiestr)
            time.sleep(1)
            col_meta.update_one({ "_id": id}, { "$set": {'cookies':cookiestr } })
            col_meta.update_one({"_id": id}, {"$set": {'status': '2'}})
            browser1.quit()

    except Exception as e:
        print('cw22',e)

# getcookies()

zhs = [['semk6067@varnet.asia','Fooshm5065064'],['pnrjv6834@varnet.asia','Oppfaei298303'],['ujzbs9850@adshe.asia','gcbhuob4041838']]
while 1:

    print('开始运行')
    alls = col_meta.find({'status':'1'})
    for all in alls:
        print(all)
        try:
            name = all['name']
            password= all['password']
            id = all['_id']
            getcookies(id,name,password)
        except Exception as e:
            print('出现验证码',e)
    time.sleep(300)