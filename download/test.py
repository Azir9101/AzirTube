import requests
import ast
import json
import os

from urllib import unquote
from collections import defaultdict

url = 'https://www.youtube.com/watch?v=6kz7bgqGvLY'

comp_url = 'https://r5---sn-n3cgv5qc5oq-bh2es.googlevideo.com/videoplayback?gir=yes&ipbits=0&pcm2=no&lmt=1464971610580746&clen=16544708&signature=DC8CEE7E78A7AB624951E323627280A94C4BED63.D59C23A222E33DB3E2AE986E70DC364AFBF7F265&source=youtube&upn=L6LGyS6Tq24&expire=1481498555&initcwndbps=3523750&key=yt6&keepalive=yes&ei=WotNWMHmPIXY4QKN97KgAg&sparams=clen%2Cdur%2Cei%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpcm2%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&mn=sn-n3cgv5qc5oq-bh2es&mm=31&ip=1.234.231.14&itag=137&dur=141.833&id=o-ACUMYnF6koD_FiUYxSOyeP8rMOASTOLAakGx5iFrQifK&mime=video%2Fmp4&ms=au&requiressl=yes&pl=22&mv=m&mt=1481476639'

resp = requests.get(url)

data = resp.content

def offset(d):
    offset = []
    off_count = 0
    count = 0
    result = []
    for k, i in enumerate(d):
        if i == '{':
            count += 1
            offset.append(k)
        elif count > 0 and i == '}':
            result.append(d[offset[off_count]:k+1])
            off_count += 1
            count -= 1
            if count == 0:
                break
    return result

def find_url(a):
    set_config = []
    length = len(a)
    start = 0
    test_string = 'ytplayer.config = '
    test_length = len(test_string)
    for i in range(test_length, length):
        string = a[start:i].lower()
        if string == test_string:
            break
        start += 1
    count = 1
    for k in range(i+1, len(a)):
        if a[k] == '{':
            count += 1
        if a[k] == '}':
            count -= 1
        if count == 0:
            break
    string_dic = a[i:k+1]
    js = json.loads(string_dic)
    return js

def stream_map(js):
    stream_map = js['args']['url_encoded_fmt_stream_map'].split('url=')
    for i in range(1, len(stream_map)):
        stream_map[i] = unquote(stream_map[i])
    stream_map[1:]

def parse_stream(string):
    dic = defaultdict(list)
    videos = string.split(',')
    videos = [video.split('&') for video in videos]
    for video in videos:
        for i in video:
            key, value = i.split('=')
            dic[key].append(unquote(value))
    return dic

def adaptive(js):
    result = js['args']['adaptive_fmts']
    urls = result.split('url=')
    for i in range(1, len(urls)):
        urls[i] = unquote(urls[i])
    for i in range(len(urls)):
        if urls[i] == comp_url:
            print urls[i]
    return urls

js = find_url(data)
stream_data = js['args']['url_encoded_fmt_stream_map'] 
a = parse_stream(js['args']['url_encoded_fmt_stream_map'])

print a

def url2dict(string):
    a = string.split('?')[1]
    b = a.split('&')
    print b
    dic = {}
    for i in b:
        s = i.split('=')
        if len(s) >= 2:
            dic[s[0]] = s[1]
    return dic


def ts():
    dic = {}
    dic['a']=url2dict(get_url2)
    dic['b']=url2dict(test_url)
    return dic

print os.path.dirname(os.path.abspath(__file__))
