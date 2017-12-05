#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date : 2016-12-28 21:03:21
# @Author : Donoy (172829352@qq.com)
# @Link : http://www.cnblogs.com/Donoy/
# @Version : $Id$
from tkinter import *
import tkinter.messagebox
import requests
import json
import urllib
import mp3play
import threading
import time
import urllib
import urllib.request
import http.cookiejar
import pygame

# head: dict of header
def makeMyOpener(head={
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    print(header)
    opener.addheaders = header
    return opener




def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)


def createWnd():
    global root
    global listBox
    global text

    root = Tk()
    root.title('-----DMPlayer------来自网易云音乐-----')
    center_window(root, 440, 250)
    root['background'] = '#C7EDCC'
    text = Entry(font='宋体', width=36)
    text.pack()
    button = Button(root, text='搜索', width=18, fg='red', background='#CDCDC1', command=searchM).pack()

    listBox = Listbox(root, height=12, width=72, background='#C7EDCC')
    listBox.bind('<Double-Button-1>', play)
    listBox.pack()

    root.mainloop()


def searchM():
    global m_List
    global m_List_id
    global mp3_name
    itemCount = 50

    if not text.get():
        tkinter.messagebox.showinfo('温馨提示', '您可以输入以下内容进行搜索\n1.歌曲名\n2.歌手名\n3.部分歌词')
        return

    # 获得输入的歌名
    url = 'http://s.music.163.com/search/get/?type=1&s=%s&limit=%s' % (text.get(), itemCount)

    # get请求
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
    html = requests.get(url, header)
    data = json.loads(html.text)
    m_List = []
    m_List_id=[]
    mp3_name=[]
    try:
        listBox.delete(0, listBox.size())
        for MusicData in data['result']['songs']:
            listBox.insert(END, MusicData['name'] + '------' + '(' + MusicData['artists'][0]['name'] + ')')
            m_List.append(MusicData['audio'])
            m_List_id.append(str(MusicData['id']))
            mp3_name.append(MusicData['name'] + '------' +'('+ MusicData['artists'][0]['name'] + ')')
            #print MusicData
    except Exception as e:
        print(e)
        tkinter.messagebox.showinfo('温馨提示', '查询过程出现错误，请重试')
        # print '查询过程出现错误，请重试'

def get_real_url(url,try_count = 1):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    dlink = response.geturl()
    print(dlink)
    return dlink
def play_music(url,music_file ="temp.mp3"):

    pass
    #print(dlink)
    #return dlink
def play(args):
    try:
        global mp3
        sy = listBox.curselection()[0]

        #print(get_real_url("http://music.163.com/song/media/outer/url?id="+m_List_id[int(sy)]+".mp3"))
        #http://m7.music.126.net/20171125230044/935c8886854dc2da413bc3ef013507be/ymusic/082c/5ff5/4ac8/995349705582f6c156807789794a11ac.mp3

        print("播放音乐1")
        musicurl = get_real_url("http://music.163.com/song/media/outer/url?id="+m_List_id[int(sy)]+".mp3")
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()


        music_file =mp3_name[int(sy)]+".mp3"

        req = urllib.request.Request(musicurl)
        response = urllib.request.urlopen(req)
        dlink = response.read()
        file = open(mp3_name[int(sy)]+".mp3", "wb")
        file.write(dlink)
        file.close()

        track = pygame.mixer.music.load((mp3_name[int(sy)]+".mp3").encode('utf-8'))
        pygame.mixer.music.play()

        #time.sleep(100)
        #pygame.mixer.music.stop()
        #mp3 = mp3play.load()
        #mp3.play()
        # time.sleep(1000)
    except Exception as e:
        print(e)
        pass


def main():
    pygame.mixer.init()
    createWnd()


if __name__ == '__main__':
    main()