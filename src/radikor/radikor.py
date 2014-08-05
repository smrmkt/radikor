#!/usr/bin/env python
#-*-coding:utf-8-*-

from base64 import b64encode
from bs4 import BeautifulSoup
import datetime
import os
from prettyprint import pp_str
import re
import time
from urllib import urlretrieve
from urllib2 import Request, urlopen

class RadikoPlayer:
    # Radiko urls
    player_url = 'http://radiko.jp/player/swf/player_3.0.0.01.swf'
    auth1_fms_url = 'https://radiko.jp/v2/api/auth1_fms'
    auth2_fms_url = 'https://radiko.jp/v2/api/auth2_fms'
    stream_xml_url = 'http://radiko.jp/v2/station/stream/'
    list_xml_url = 'http://radiko.jp/v2/station/list/'

    # local files
    tmp_dir = '/tmp/radiko_player'
    player_file = tmp_dir + '/player.swf'
    key_file = tmp_dir + '/authkey.png'
    partial_key_file = tmp_dir + '/partial_key'

    # local commands
    swfextract_path = '/usr/local/bin/swfextract'
    rtmpdump_path = '/usr/local/bin/rtmpdump'
    ffmpeg_path = '/usr/local/bin/ffmpeg'

    # stream parameters
    stream_url_parts = []
    auth_token = ''
    region = ''

    def __init__(self, ch='FMT'):
        self.__get_authkey()
        auth1_fms = self.__get_auth_fms(self.auth1_fms_url)
        self.auth_token, length, offset = self.__get_auth_params(auth1_fms)
        partial_key = self.__get_partial_key(offset, length)
        auth2_fms = self.__get_auth_fms(self.auth2_fms_url, self.auth_token, partial_key)
        self.region = self.__get_region(auth2_fms)
        self.stream_url_parts = self.__get_stream_url(ch)

    def play(self):
        os.system(self.rtmpdump_path + ' -v' +
                  ' -r ' +  self.stream_url_parts[0] +
                  ' --app ' + self.stream_url_parts[1] +
                  ' --playpath ' + self.stream_url_parts[2] +
                  ' -W ' + self.player_url +
                  ' -C S:"" -C S:"" -C S:"" -C S:' + self.auth_token +
                  ' --live | mplayer -')

    def record(self, duration, out_dir):
        file_name = str(time.mktime(datetime.datetime.now().utctimetuple()))
        os.system(self.rtmpdump_path + ' -v' +
                  ' -r ' +  self.stream_url_parts[0] +
                  ' --app ' + self.stream_url_parts[1] +
                  ' --playpath ' + self.stream_url_parts[2] +
                  ' -W ' + self.player_url +
                  ' -C S:"" -C S:"" -C S:"" -C S:' + self.auth_token +
                  ' --live' +
                  ' --stop ' + str(duration * 60) +
                  ' --flv ' + self.tmp_dir + '/' + file_name)
        os.system(self.ffmpeg_path +
                  ' -loglevel quiet'
                  ' -y'
                  ' -i ' + self.tmp_dir + '/' + file_name +
                  ' -acodec libmp3lame'
                  ' -ab 128k'
                  ' "' + out_dir + '/' + file_name + '.mp3"')

    def list(self):
        list_xml = urlopen(self.list_xml_url + self.region + '.xml')
        soup = BeautifulSoup(list_xml)
        names = soup.find_all('name')
        ids = soup.find_all('id')
        stations = {name.string: id.string for name, id in zip(names, ids)}
        print 'Your region code is "' + self.region + '", and stations in your region are:'
        print pp_str(stations)

    def __get_authkey(self):
        # download player.swf
        if os.path.isdir(self.tmp_dir) is False:
            os.mkdir(self.tmp_dir)
        urlretrieve(self.player_url, self.player_file)
        # extract authkey.jpg
        os.system(self.swfextract_path +
                  ' -b 14 ' + self.player_file +
                  ' -o ' + self.key_file)

    def __get_auth_fms(self, url, token=None, key=None):
        req = Request(url)
        req.add_header('pragma', 'no-cache')
        req.add_header('X-Radiko-App', 'pc_1')
        req.add_header('X-Radiko-App-Version', '2.0.1')
        req.add_header('X-Radiko-User', 'test-stream')
        req.add_header('X-Radiko-Device', 'pc')
        if token is not None:
            req.add_header('X-Radiko-Authtoken', token)
        if key is not None:
            req.add_header('X-Radiko-Partialkey', key)
        req.add_data('\r\n')
        return urlopen(req).read()

    def __get_auth_params(self, fms_data):
        token = re.compile(r'X-Radiko-AuthToken=([\w-]+)')\
            .search(fms_data)\
            .group(1)
        length = re.compile(r'X-Radiko-KeyLength=(\d+)')\
            .search(fms_data)\
            .group(1)
        offset = re.compile(r'X-Radiko-KeyOffset=(\d+)')\
            .search(fms_data)\
            .group(1)
        return token, length, offset

    def __get_partial_key(self, offset, length):
        os.system('dd if=' + self.key_file +
                  ' bs=1' +
                  ' skip=' + offset +
                  ' count=' + length +
                  ' 2> /dev/null' +
                  '> ' + self.partial_key_file)
        return b64encode(open(self.partial_key_file).read())

    def __get_region(self, fms_data):
        return re.compile(r'.*(JP\d+),.*')\
            .search(fms_data)\
            .group(1)

    def __get_stream_url(self, ch):
        stream_xml = urlopen(self.stream_xml_url + ch + '.xml')
        stream_url = BeautifulSoup(stream_xml).find('item').string
        parts = re.compile(r'^(rtmpe://.*?)/(.*)/(.*)').search(stream_url)
        return [parts.group(1), parts.group(2), parts.group(3)]
