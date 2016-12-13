import requests
import json
import os

from collections import defaultdict
from urllib import unquote
from bs4 import BeautifulSoup as beauti


class AzirTubeException(Exception):
    pass

class AzirTube(object):
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
            if self.dic is not None:
                self.dic = dic
            return dic
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
        # current_path file download on self.url
        path = os.path.dirname(os.path.abspath(__file__))
        file_name = get_file_name()
        download_urls = self.dic['stream_map']['url']
        start = 0
        length = len(donwlaod_urls)
        for url in download_urls:
            resp = requests.get(url)
            if resp.ok:
                break
        if resp.ok:
            pass
        

    def get_file_name(self):
        if self.dic is None:
            self.dic = self.get_html2dict()
        return self.dic['args']['title']

    def get_audio_urls(self):
        # adaptive_fmts is contained video or audio url
        if self.dic is None:
            self.dic = self.get_html2dict()
        audio_dic = self.parse_stream(self.dic['args']['adaptive_fmts'])
        types = audio_dic['type']
        audioes = []
        idxs = []
        for idx, type_ in enumerate(types):
            type_ = type_.split(';')[0].split('/')[0]
            if type_ == 'audio':
                idxs.append(idx)
        for i in idxs:
            audioes.append(audio_dic['url'][i])
        return audioes


    def get_search_result(self, search_url):
        resp = requests.get(search_url)
        soup = beauti(resp.content, 'html.parser')
        search_result = []
        result_div = soup.find('div', id='results')
        img_tags = result_div.find_all('img')
        print len(img_tags)
        h3_tags = result_div.find_all('h3')
        result = defaultdict(list)
        for i in range(2, len(img_tags)):
            title = h3_tags[i].text.split(' - ')
            title = ' '.join(title[:-1])
            img_src = img_tags[i].get('src')
            result['titles'].append(title)
            result['images'].append(img_src)
        return result
        
    def search(self, search_query):
        search_query = search_query.split(' ')
        query = None
        for i in search_query:
            if query is None:
                query = i
            else:
                query+'+'+i
        search_url = 'https://www.youtube.com/results?search_query={0}'.format(query)
        result = self.get_search_result(search_url) 
        return result
