import argparse
import datetime
import json
import re
import time
import requests
from pymongo import MongoClient

client = MongoClient(host='34.72.119.207', port=30228,username='root',password='yV3UX5moXGzlnSxB')
db = client.openai
col_meta = db.openai_account1

client_2 = MongoClient(host='34.28.207.247', port=30000,username='root',password='yV3UX5moXGzlnSxB')
db_2 = client_2.openai
col_txt = db_2.corpus

ip = requests.get('https://myip.ipip.net', timeout=5).text
ip = re.findall(r'(\d+\.\d+\.\d+\.\d+)', ip)[0]

def get_content(url,text):
    global accessToken
    header = {
    "authorization": accessToken,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
}
    data = {"action":"next","messages":[{"id":"7158d32b-122f-4b92-a142-b47907a9ba6d","role":"user","content":{"content_type":"text","parts":[text]}}],"parent_message_id":"0f926278-00d8-4b83-8a81-ba440b0084ac","model":"text-davinci-002-render"}
    response = requests.post(url=url,headers=header,json=data)
    response_text = response.text
    # print(response_text)
    return response_text

def get_content_info(json_text):
    global file_num,accessToken,lose_count,cookie
    url = 'https://chat.openai.com/backend-api/conversation'
    status = False
    try:
        response_text = get_content(url, json_text['text'])
        # print(response_text)
        if re.findall('Your authentication token has expired. Please try signing in again',response_text):
            col_meta.update_one({"_id":int(file_num)},{"$set":{'status':'1'}})
            c_json = mg()
            cookie = c_json['cookies']
            accessToken = hq_lp()
            return status
        else:
            try:
                data = re.findall('data:(.*"error": null})', response_text)[-1]
                soup1 = json.loads(data)
                parts = soup1['message']['content']['parts']
                add_date = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
                col_txt.update_one({'_id':json_text['_id']},{'$set':{'result':parts,'status':2,'updateTime':add_date,'ip':ip}})
                print(json_text['_id'],'完成')
            except Exception as e:
                col_txt.update_one({'_id': json_text['_id']}, {'$set': {'status': -1}})
                print(e)
                time.sleep(30)
            return status
    except Exception as e:
        print(e)
        return status



def hq_lp():
    global cookie
    header = {
    "cookie": cookie,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
    url = 'https://chat.openai.com/api/auth/session'
    response = requests.get(url=url, headers=header)
    # print(response.status_code)
    response_text = response.json()['accessToken']
    return response_text


def mg():
    global file_num
    while True:
        a = col_meta.find_one({'$and': [{"_id": int(file_num)}, {"status": '2'}]})
        if a:
            print(file_num, 'cookies已拿到')
            break
        else:
            print('等待更新cookies')
            time.sleep(5)
            continue
    return a

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--nf', type=str, default=None)
    args = parser.parse_args()
    file_num = args.nf
    #file_num = '208'
    cookie_json = mg()
    cookie = cookie_json['cookies']
    url = 'https://chat.openai.com/backend-api/conversation'
    lose_count = 0
    accessToken = hq_lp()
    while True:
        json_txt = col_txt.find_one_and_update({'status':0},{'$set':{'status':1}})
        if json_txt == None:
            break
        status = get_content_info(json_txt)
