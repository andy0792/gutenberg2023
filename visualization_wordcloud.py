# -*- coding: utf-8 -*-
##Python文件名：visualization_wordcloud.py
##数据收集-清洗-可视化展示，三部曲中的数据可视化展示##
##Python可视化输出： 生成各种可视化chart##
##一个调用wordcloud, 画图Word Cloud（词云）的类
import wordcloud
import numpy as np 
from PIL import Image 
import matplotlib.pyplot as plt  
##导入module##
##从存放英文小说的文件夹, 获取所有的英文小说txt文本文件名, 传给后续函数做变量##
from gutenberg_collect_data import recursive_listdir
##导入module, 读取txt小说，返回文本novel_txt##
from gutenberg_collect_data import read_from_txt_for_wordcloud

def draw_wordcloud(novel_txt, novel_title):
    '''绘制词云图, 单词出现越多次数, 字体越大
    :param novel_txt: 小说文本, str格式, 不支持DataFrame数据格式
    :param novel_title: 小说名字, 用于词云图的标题和文件名
    :param img: 图片的绝对地址, 支持jpg, png, webp格式
    :param mask: 将图片转换为数组
    :param stopwords_list: 存不需要显示的词, 字符串列表
    :param wc: 方法wordcloud.WordCloud()的对象
    
    return: none but draw a chart
    '''
    ##打开遮罩图片##
    img = Image.open(r"C:\Users\86151\Desktop\python.webp")
    # img = Image.open(r"C:\Users\86151\Desktop\python.jpg")
    ##将图片转换为数组##
    mask = np.array(img)
    ##去掉不需要显示的词##
    stopwords_list = ["the", "and", "to", "of", "i", "a", "in", "that", "was", "he", 
                "it", "you", "his", "her", "with", "as", "had", "for", "she", 
                "my", "not", "s", "at", "but", "on", "is", "me", "be", "said", 
                "him", "have", "all", "this", "so", "by", "which", "from", 
                "they", "were", "what", "there", "if", "no", "or", "when", 
                "one", "we", "would", "up", "an", "out", "been", "are", "do", 
                "who", "them", "could", "very", "now", "little", "will", 
                "into", "more", "your", "their", "about", "some", "then", 
                "like", "any", "did", "know", "man", "how", "upon", "well", 
                "time", "see", "than", "down", "can", "good", "old", "never", 
                "before", "should", "come", "much", "over", "only", "other", 
                "has", "such", "am", "made", "after", "must", "say", "go", 
                "here", "mr", "t", "mrs", "don", "miss", "again", "us", "great",
                "our", "think", "thought", "two", "where", "came", "way", "too",
                "might", "day", "went", "own", "may", "such", "these" ]

    wc = wordcloud.WordCloud(width = 1000,
                            height = 1000,
                            mask = mask, 
                            background_color = "white",
                            max_words = 500, stopwords = stopwords_list)

    wc.generate(novel_txt)
    # print(f"novel_txt的类型是 {type(novel_txt)}")
    # # novel_txt的类型是 <class 'str'>
    # TypeError: expected string or bytes-like object, got 'DataFrame'
    ##更wordcloud的保存图表, 缺点没有标题##
    # wc.to_file(rf"C:\Users\86151\Desktop\词云{novel_title}.png")

    ##用plt显示图片##
    plt.imshow(wc, interpolation="bilinear")
    # plt.title("词云")
    plt.axis("off")     ##不显示坐标轴##

    ##设置横纵坐标标签，加上图标题##
    plt.suptitle(f"词云图-{novel_title}", fontsize = 18)

    ##图表显示中文##
    # plt.rcParams['font.sans-serif'] = ['YouYuan']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    ##Matplotlib绘制的坐标轴无法显示负号，只出现了框框##
    # plt.rcParams["axes.unicode_minus"] = False 

    ##展示和保存图表只能二选一##
    # plt.show()
    plt.savefig(rf"C:\Users\86151\Desktop\词云图-{novel_title}.png", bbox_inches = "tight")

    ##更wordcloud的保存图表, 缺点没有标题##
    # wc.to_file(rf"C:\Users\86151\Desktop\词云{novel_title}.png")


def draw_batch_wordcloud(txt_file_directory):
    '''批量绘制词云图, 调用函数recursive_listdir()和read_from_txt_for_wordcloud()
    # 从存放小说文件夹下, 读取所有的小说名字, 返回嵌套列表txt_file_list,  
    # 存小说的绝对路径和小说名(不含文件名后缀)
    :param txt_file_directory: txt文件存放目录, 存放经典英文小说txt文件, 为ANSI编码
    :param txt_file_list: 嵌套列表list-list, 存小说的绝对路径和小说名(不含文件名后缀)
    :param txt_filename: 小说的绝对路径
    :param sheet_name: 小说名(不含文件名后缀), 同novel_title
    :param novel_title: 小说名(不含文件名后缀)
    :param novel_txt: 调用函数read_from_txt_for_wordcloud()返回的小说str字符串
    :return none
    '''
    ##调用函数，递进遍历指定目录下的所有文件##
    txt_file_list = recursive_listdir(txt_file_directory)
    ##路径末尾不能带\,提示语法错误SyntaxError: unterminated string literal##
    for txt_file in txt_file_list:
        txt_filename = txt_file["txt_filename"]
        novel_title = txt_file["sheet_name"]
        novel_txt = read_from_txt_for_wordcloud(txt_filename)
        ##调用函数，绘制每部小说的词云图##
        draw_wordcloud(novel_txt, novel_title)
