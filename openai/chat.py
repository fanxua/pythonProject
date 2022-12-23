import argparse
import json
import random
import re
import time
from tqdm import tqdm
import jsonlines
import requests
from pymongo import MongoClient

client = MongoClient(host='34.72.119.207', port=30228,username='root',password='yV3UX5moXGzlnSxB')
db = client.openai
col_meta = db.openai_account1

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

def get_content_info(text):
    global file_num,accessToken,lose_count,cookie
    url = 'https://chat.openai.com/backend-api/conversation'
    status = False
    try:
        response_text = get_content(url, text)
        # print(response_text)
        if re.findall('Your authentication token has expired. Please try signing in again',response_text):
            col_meta.update_one({"_id":int(file_num)},{"$set":{'status':'1'}})
            c_json = mg()
            cookie = c_json['cookies']
            accessToken = hq_lp()
            return status
        elif re.findall('Too many requests in 1 hour. Try again later',response_text):
            time.sleep(300)
        else:
            try:
                data = re.findall('data:(.*"error": null})', response_text)[-1]
                soup1 = json.loads(data)
                parts = soup1['message']['content']['parts']
                data_json = {
                    "src": text,
                    "target": parts,
                }
                file_name = 'jsonl_all/gx_{}.jsonl'.format(file_num)
                with jsonlines.open(file_name, mode='a') as e:
                    e.write(data_json)
            except:
                parts = ""
            return status
    except Exception as e:
        print(e)
        return status

def dq_txt():
    global file_num
    file_name = 'file_txt/gx_{}.txt'.format(file_num)
    with open(file_name,'r',encoding='utf-8') as f:
        r_line = f.read()
        r_list = re.split('\n',r_line)
    return r_list


def jx_run(r_list):
    global file_num
    complete_list = []
    file_name = 'jsonl_all/gx_{}.jsonl'.format(file_num)
    try:
        with jsonlines.open(file_name,'r') as r:
            for i in r:
                complete_list.append(i['src'])
        no_run_list = list(set(r_list) - set(complete_list))
        print(len(complete_list),len(no_run_list))
        return no_run_list
    except:
        return r_list

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
        print(a)
        if a:
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
    #file_num = '30'
    cookie_json = mg()
    cookie = cookie_json['cookies']
    # print(cookie)
    url = 'https://chat.openai.com/backend-api/conversation'
    lose_count = 0
    accessToken = hq_lp()
    while True:
        r_list = dq_txt()
        r_list = jx_run(r_list)
        if len(r_list) == 0:
            break
        for i in tqdm(r_list):
            try:
                status = get_content_info(i)
                if status:
                    break
            except:
                print('错误')
            time.sleep(2)


