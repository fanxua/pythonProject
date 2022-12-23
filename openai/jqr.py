import datetime
import json
import os
import re
import time
import requests

# 机器人地址
url_deepl = "https://oapi.dingtalk.com/robot/send?access_token=361dd149170133dfe10688a427d765457582d1758b487bda17f3d9ca7cd272d0"


def post(url, data=None):
    data = json.dumps(data, ensure_ascii=False)
    data = data.encode(encoding="utf-8")
    req = requests.post(url=url, data=data, headers={
        "content-type": "application/json; charset=utf-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/100.0.4896.60 "
                      "Safari/537.36",
    })
    req = json.loads(req.text)
    return req


def massage_text(content):
    data = {
        "text": {
            "content": content
        },
        "msgtype": "text"
    }
    return post(url_deepl, data)


def get_count():
    path = "jsonl_all"
    count = 0
    f_list = os.listdir(path)
    for i in f_list:
        if os.path.splitext(i)[1] == '.jsonl':
            "对于文件内容比较多，采用enumerate获取文件行数"
            file_name = path + '/' + i
            with open(file_name, "r", encoding="utf-8") as f:
                for index, line in enumerate(f):
                    count += 1
    return count


def get_content():
    count = get_count()
    content = ">>>chatgpt进度——{}\n目前数据量合计：{}条".format(ip, count)
    return content


# 获取当天时间0点的时间戳
def get_zero_time():
    date = datetime.datetime.now().date()
    if not date:
        return 0
    date_zero = datetime.datetime.now().replace(year=date.year, month=date.month,
                                                day=date.day, hour=0, minute=0, second=0)
    date_zero_time = int(time.mktime(date_zero.timetuple()))
    return date_zero_time


# 时间格式转换
def time_change(time_object):
    timeTemp = float(time_object)
    tupTime = time.localtime(timeTemp)
    return time.strftime("%Y/%m/%d %H:%M:%S", tupTime)


ip = requests.get('https://myip.ipip.net', timeout=5).text
ip = re.findall(r'(\d+\.\d+\.\d+\.\d+)', ip)[0]

if __name__ == "__main__":
    print(massage_text(get_content()))
    while True:
        now = time.strftime("%M", time.localtime())
        if now == "00":
            print(massage_text(get_content()))
            time.sleep(60)
        else:
            time.sleep(1)

