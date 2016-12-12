import requests
import json
import os

from collections import defaultdict
from urllib import unquote

class Azirtube(object):
    def __init__(self, url):
        self.url = url
        self.file_name = None
        self.dic = None
        self.urls = None

    def youtube(self):
        pass

    def get_html2dict(self):
        url = self.url
        resp = requests.get(url)
        if resp.ok:
            html = resp.content
            config_string = 'ytplayer.config = ' 
            conf_length = len(config_string)
            html_length = len(html)
            start = 0
            for ch in range(conf_length, html_length):
                st = html[start:ch].lower()
                if st == config_string:
                    break
                start += 1
            count = 1
            for i in range(ch+1, html_length):
                if html[i] == '{':
                    count += 1
                elif html[i] == '}':
                    count -= 1
                if count == 0:
                    break
            res = html[ch:i+1]
            dic = json.loads(res)
            stream_map = dic['args']['url_encoded_fmt_stream_map']
            dic['stream_map'] = self.parse_stream(stream_map)
            self.dic = dic
            return dic
        else:
            return -1

    def parse_stream(self, string):
        dic = defaultdict(list)
        videos = string.split(',')
        videos = [video.split('&') for video in videos]
        for video in videos:
            for kv in video:
                key, value = kv.split('=')
                dic[key].append(unquote(value))
        return dic
        
    def downlaod(self): 
        path = os.path.dirname(os.path.abspath(__file__))
        pass

    def get_file_name(self):
        if self.dic is None:
            self.dic = self.get_html2dict()
        return self.dic['args']['title']

url = 'https://www.youtube.com/watch?v=6kz7bgqGvLY'            
test = Azirtube(url)
print test.get_file_name()       
