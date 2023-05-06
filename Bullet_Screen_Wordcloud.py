import requests
import re
import json
from lxml import etree
import jieba
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt

def get_bvid():
    url = input("Please input the url:")
    bvid = re.search('BV(\w+)',url).group()
    #print(bvid)
    return bvid

def get_cid(bvid):
    url = "https://api.bilibili.com/x/player/pagelist?bvid="+bvid+"&jsonp=jsonp"
    #print(url)
    try:
        res = requests.get(url, timeout=None)
        if res is not None:
            #print(res.text)
            return res.text
        else:
            print("Response is none.")
            return 0
    except Exception as e:
        print(e.args)

def stop_word():
    with open("cn_stopwords.txt","r",encoding="utf-8") as f: 
        stopword_list = [w.strip("\n") for w in f.readlines()]
    #print(stopword_list)
    return stopword_list

def word_cloud():
    word = open("bullet_screen.txt","r",encoding="utf-8").read()
    word = word.replace("\n","")
    word = word.replace("\u3000","") #\u3000為空白字符
    c_word = jieba.lcut(word)
    c_word = " ".join(c_word)
    
    word_cloud = WordCloud(font_path="Hiragino Sans GB.ttc", background_color="white", stopwords = sw_list)
    word_cloud.generate(c_word)
    plt.subplots(figsize=(256,256)) #圖片長寬
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()
    word_cloud.to_file(im_file_name)
    
if __name__ == '__main__':
    bvid = get_bvid()
    data = get_cid(bvid)
    json_data = json.loads(data)
    bs_url = "http://api.bilibili.com/x/v1/dm/list.so?oid="
    all_bs_api = []
    for cid_data in json_data["data"]:
        cid = cid_data.get("cid")
        bs_api = bs_url + str(cid)
        #print(bs_api)
        all_bs_api.append(bs_api)
        
    for bs in all_bs_api :
        api_content = requests.get(bs)
        s = api_content.text
        selector = etree.HTML(s.encode("utf-8"))
        for item in selector.xpath("."):
            ss = item.xpath(".//d/text()")
        with open("bullet_screen.txt",'a',encoding="utf-8") as file:
            file.truncate(0)
            for i in ss:
                #print(i.encode("raw_unicode_escape").decode()) #str轉bytes轉str
                file.write(i.encode("raw_unicode_escape").decode()+"\n")
    sw_list = stop_word()
    im_title = input("Please input the file name of the wordcloud:")
    im_file_name = im_title + ".png"
    word_cloud()