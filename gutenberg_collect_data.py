# -*- coding: utf-8 -*-
##Python文件名：gutenberg_collect_data.py
##数据收集-清洗-可视化展示, 三部曲中的数据收集——从文件夹下的小说txt读取数据##
##数据收集-清洗-可视化展示, 三部曲中的数据收集——从Excel读取数据##
##数据收集, 用Pandas库读取Excel文件, 返回DataFrame数据格式

import pandas as pd 
import os
import copy

# class Collectdata():
#     '''数据收集,用Pandas或xlrd库读取Excel文件,返回DataFrame或自定义的数据格式
#     读取Excel下单张WorkSheet, 返回的DataFrame数据——df_excel_sheet
#     读取Excel下所有WorkSheet, 返回的DataFrame数据——df_excel_dict
#     读取Excel下单张WorkSheet, 返回自定义数据格式的数据——data_list
#     '''

def recursive_listdir(path):
    '''从存放英文小说的文件夹, 获取所有的英文小说txt文本文件名, 传给后续函数做变量
    ##递进遍历指定目录下的所有文件
    :param path: 指明文件夹路径, 路径末尾不能带反斜杠, 会提示语法错误SyntaxError
    :param txt_filename_list: 返回英文小说的文件名, 传给后续函数做变量
    :param txt_file_directory: txt文件存放目录, 存放经典英文小说txt文件, 为ANSI编码
    :param txt_file_list: 嵌套列表list-list, 存小说的绝对路径和小说名(不含文件名后缀)
    :param txt_file_dict: list-dict结构, 内层的dict##
    :param files_list: os.listdir()返回的文件夹下文件列表
    :param txt_filename: 小说的绝对路径
    :param sheet_name: 小说名(不含文件名后缀), 同novel_title
    :param novel_title: 小说名(不含文件名后缀)
    :param txt_file_dict_deepcopy: list-dict结构append用深复制, 另造一个值复制, 不用指针引用
    :return txt_filename_list
    '''
    ##需要一个存放文件绝对路径和文件名(不带后缀)的容器——没错，就是字典+列表。
    ##list-dict结构, 外层的list, 保存dict, 对应每一个遍历出的txt文件##
    txt_file_list = []
    ##list-dict结构, 内层的dict, 保存txt文件绝对路径和保存txt文件名(不带后缀)##
    txt_file_dict = {}
    ##files_list, os.listdir()返回的文件夹下文件列表
    files_list = os.listdir(path)
    for file in files_list:
        file_path = os.path.join(path, file) 
        ##如果是文件,保存文件绝对路径和文件名(不带后缀),作为其他函数的参数##
        if os.path.isfile(file_path):
            # print(file)
            # print(file_path)
            # print(file.rsplit(".", 1)[0])
            txt_filename = file_path
            sheet_name = file.rsplit(".", 1)[0]
            ##在循环体内, 每个文件有两条记录，保存为dict##
            ##txt_filename_dict["txt_filename"]保存txt文件绝对路径
            ##txt_filename_dict["sheet_name"]保存txt文件名(不带后缀)##
            txt_file_dict["txt_filename"] = txt_filename
            txt_file_dict["sheet_name"] = sheet_name
            # print(txt_filename_dict)
        elif os.path.isdir(file_path):
            print(f"这里是一个目录, 递进遍历下一层目录")
            ##递进遍历, 封装为Class之后, 要带上Class名字##
            # Collectdata.recursive_listdir(file_path)
            ##递进遍历, 如果只封装为函数, 不需要带上Class名字##
            recursive_listdir(file_path)
        ##在循环体内, list-dict结构##
        ##list已保存的内容会全部被最新的dict内容覆盖, 为什么呢? 对象引用(指针)造成的##
        ##解决办法, Python的copy.deepcopy(), 另造一个值复制, 不用指针引用##
        txt_file_dict_deepcopy = copy.deepcopy(txt_file_dict)
        txt_file_list.append(txt_file_dict_deepcopy)
    return  txt_file_list

def read_from_txt(txt_filename):
    '''从txt文件中读取小说文本, 做文本预处理——排除中英文标点符号(置空), 
    ##排除一些冠词、连接词、介词, 排除he's类似的所有格中的逗号(置空)
    :param txt_filename: txt文件名
    :param novel_txt: 用open()读取txt小说, novel_txt的数据类型是str
    :param words_list: 分词后的单词列表, 数据类型是list
    :param vocabulary_counts_dict: 字典dict, Key存单词, Value存词频
    :param excludes_set: 排除100个高频特简单词名单, excludes_set的数据类型是set
    :param items_list: 存储所有的单词, 单词做词频倒序排列, 数据类型是list
    :return df
    '''
    #   novel_txt = open(txt_filename, "r", encoding = "gb18030", errors="ignore").read()  
    # （1）在打开文本时候，可以指明打开方式：
    # （2）如果上一步还不能解决，是文本中出现的一些特殊符号超出了gbk的编码范围，
    ##   可以选择编码范围更广的‘gb18030’，如：
    # （3）如果（2）还不能解决，说明文中出现了连‘gb18030'也无法编码的字符，
    ##    可以用‘ignore’属性忽略非法字符
    ##打开txt文件，r读取权限##
    ##字符编码不对——鈥(”),鈥淚(“i),it鈥檚(it’s),don鈥檛(don’t),(that’s)##
    ##字符编码有乱码的解决办法——将英文小说TXT文本，另存为，更改编码为ANSI##
    novel_txt = open(txt_filename, "r", errors = "ignore" ).read()  
    # print(f"novel_txt的数据类型是 {type(novel_txt)}")
    # # novel_txt的数据类型是 <class 'str'>
    # print(f"novel_txt的长度是 {len(novel_txt)}")
    # # novel_txt的长度是 177865

    ##文本预处理,标点符号等特殊符号置空##
    ##字符编码不对——鈥(”),鈥淚(“i),it鈥檚(it’s),don鈥檛(don’t),(that’s),(I’ll)##
    for ch in "# $ % & () * + , - _ — \“ \” \‘ \’ \" \' ! . : ; < = > ? @ [\\] ^ { }":
        novel_txt = novel_txt.replace(ch,  " " )    ##特殊字符用英文空格代替##

    novel_txt = novel_txt.lower()   ##将所有单词字母转为为小写##
    words_list = novel_txt.split()       ##什么都不填表示用空格来分隔##
    # print(f"words_list的数据类型是 {type(words)}")
    # # words_list的数据类型是 <class 'list'>
    # print(f"words_list的长度是 {len(words)}")
    # # words_list的长度是 32419
    #英文文本，单词之间本身就存在空格符，不需要分词的。文本预处理。
    #中文文本，词与词之间没有空格符，所以需要中文分词工具
    #中文分词工具如：jieba、pkuseg、pynlpir、thulac 等。

    ##用一个空字典dict, 存放词频, 字典中Key与Value, 分别存放单词+单词出现的次数##
    vocabulary_counts_dict = {}  
    for word in words_list:
        vocabulary_counts_dict[word] = vocabulary_counts_dict.get(word, 0) + 1
        ##vocabulary_counts_dict[word]是把遍历到的词作为key，
        ##后面的表达式，get()去查询 key出现的次数，出现一次，就+1，如果没有，返回0##

    ##排除一些冠词、连接词、介词##
    ##用for循环去遍历文件中的词，用del()删去它们##
    ###排除123个高频特简单词 don't变成don和t两个word##
    excludes_set = {"the", "and", "to", "of", "i", "a", "in", "that", "was", "he", 
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
                "might", "day", "went", "own", "may", "such", "these" }
    # print(f"excludes_set的数据类型是 {type(excludes_set)}")
    # # excludes_set的数据类型是 <class 'set'>
    ##遇到单词mr和mrs和t和don, 就会报错KeyError: 'mr',只好移出excludes列表##
    ##报错KeyError: 'don'和报错KeyError: 't'##
    ##报错KeyError: 'old'原因, 有的小说中没有这些词, del dict[key]报错KeyError##
    ##解决办法, 主动忽略这种情况，保持程序不被中断##
    for word in excludes_set:
        try:
            del(vocabulary_counts_dict[word]) 
        except KeyError:
            print("小说中不包含某个单词key, 已跳过del dict[key]这个单词")
            ##except代码打印一条友好消息, 程序不被中断继续运行, 用户看不到traceback##
        
    ##列表中包含的是字典中所有键值对形成的元组##
    items_list = list(vocabulary_counts_dict.items())
    # print(f"items_list的数据类型是 {type(items_list)}")
    # # items_list的数据类型是 <class 'list'>
    # print(f"items_list的长度是 {len(items_list)}")
    # # items_list的长度是 4561
    ##对结果排序，把字典中的键值形成的元组，保存到列表里面去，
    ##字典是无序的，数据量一大, 我们无法统计哪个词频率最高，哪个最低##
    items_list.sort(key = lambda x: x[1], reverse = True)
    ##实现了以词出现的次数为条件的降序排序。
    ##sort()方法便是以第一列为基准升序排序的。
    ##用lambda匿名函数让它以第二列为基准降序排序##

    ##排名前10最高频的单词##
    # for i  in range(10):
    #     word, count = items[i]
    #     print(f"{word}  {count}  \n")

    ##List-Dict转DataFrame##
    df = pd.DataFrame(data = items_list,  columns=["Word", "Count" ])
    # print(f"List-Dict转DataFrame\n {df} \n" )
    return df  


def read_from_txt_for_wordcloud(txt_filename):
    '''从txt文件中读取小说文本, 做文本预处理——排除中英文标点符号(置空), 
    ##排除一些冠词、连接词、介词, 排除he's类似的所有格中的逗号(置空)
    :param txt_filename: txt文件名
    :param novel_txt: 用open()读取txt小说, novel_txt的数据类型是str  
    :param novel_txt: 调用函数read_from_txt_for_wordcloud()返回的小说str字符串
    :return novel_txt
    '''
    novel_txt = open(txt_filename, "r", errors = "ignore" ).read()  
    # print(f"novel_txt的数据类型是 {type(novel_txt)}")
    # # novel_txt的数据类型是 <class 'str'>
    # print(f"novel_txt的长度是 {len(novel_txt)}")
    # # novel_txt的长度是 177865

    ##文本预处理,标点符号等特殊符号置空##
    ##字符编码不对——鈥(”),鈥淚(“i),it鈥檚(it’s),don鈥檛(don’t),(that’s),(I’ll)##
    for ch in "# $ % & () * + , - _ — \“ \” \‘ \’ \" \' ! . : ; < = > ? @ [\\] ^ { }":
        novel_txt = novel_txt.replace(ch,  " " )    ##特殊字符用英文空格代替##

    novel_txt = novel_txt.lower()   ##将所有单词字母转为为小写##
    # words_list = novel_txt.split()       ##什么都不填表示用空格来分隔##
    # print(f"words_list的数据类型是 {type(words)}")
    # # words_list的数据类型是 <class 'list'>
    # print(f"words_list的长度是 {len(words)}")
    # # words_list的长度是 32419
    #英文文本，单词之间本身就存在空格符，不需要分词的。文本预处理。
    #中文文本，词与词之间没有空格符，所以需要中文分词工具
    #中文分词工具如：jieba、pkuseg、pynlpir、thulac 等。
    return novel_txt

def merge_excel_sheet(excel_filename):
    '''用Pandas同时读取Excel的多张WorkSheet, 合并为一个DataFrame, 
    #要求多张WorkSheet的表头一致, 此处均为Word列和Count列。
    :param excel_filename: Excel保存位置, 建议绝对路径。
    :param df_excel_dict: 返回字典dict, Key是工作表名, Value是工作表对应的DataFrame
    :param df_merged: 创建一个空的DataFrame用于存储合并
    :return df_merged 
    '''
    ##用pd.read_excel()函数读取Excel文件，指定参数sheet_name=None表明读取所有sheet。
    ##返回字典dict, Key是工作表名, Value是工作表对应的DataFrame##
    df_excel_dict = pd.read_excel(excel_filename, sheet_name = None, header = 0)
    # df_excel_dict = pd.read_excel(excel_filename, sheet_name = None)

    ##易于理解的写法，创建一个空的DataFrame用于存储合并的数据##
    df_merged = pd.DataFrame()
    ##用for循环遍历字典中的每个工作表数据，用pd.concat()函数合并到df_merged中。
    ##设置ignore_index=True表示重置索引，忽略原索引，确保合并的DataFrame从0开始递增##
    for sheet_name, sheet_data in df_excel_dict.items():
        df_merged = pd.concat([df_merged, sheet_data], ignore_index = True)
        # print(sheet_name)
        # print(type(sheet_data))
    ##节省代码行数的写法##
    # df_merged = pd.concat(df_excel_dict.values(), ignore_index = True)
    ##df_excel_dict.values()返回DataFrame对象，<class 'pandas.core.frame.DataFrame'>
    ##设置ignore_index=True表示重置索引，忽略原索引，确保合并的DataFrame从0开始递增##
    # print(type(df_merged))
    # print(df_merged.head())
    ##合并后的DataFrame, 包含所有工作表的数据, 原工作表的数据也是DataFrame格式##
    ##返回合并后的DataFrame##
    return df_merged

def pandas_read_excel(read_excel_filename, sheetname):
    '''用Pandas库读取Excel文件, 指定WorkSheet名字
    读取Excel下单张WorkSheet, 返回的DataFrame数据——df_excel_sheet
    :param read_excel_filename: Excel文件名称,建议绝对路径
    :param sheetname: Excel中表格WorkSheet名称
    :return: df_excel_sheet
    '''
    ##读Excel文件##
    df_excel_sheet = pd.read_excel(read_excel_filename, sheetname)
    # print(f"\n只读取一张WorkSheet\n {type(df_excel_sheet)} \n" )
    ## <class 'pandas.core.frame.DataFrame'>##
    # print(df_excel_sheet.columns)       ##数据集所有列的名字##
    ##Index(['分数', '人数', '累计人数'], dtype='object')##
    # print(df_excel_sheet.head)          ##数据集前几行##
    return df_excel_sheet

def pandas_read_excel_dict(read_excel_filename):
    '''用Pandas库读取Excel文件, 返回DataFrame数据格式
    读取Excel下所有WorkSheet, 返回的DataFrame数据——df_excel_dict
    返回一个字典dict,键key是工作表名,值value是工作表对应的DataFrame
    :param read_excel_filename: Excel文件名称,建议绝对路径
    :return: df_excel_dict
    '''
    ##读Excel文件,用pd.read_excel()函数读取Excel文件,
    ##指定参数sheet_name=None表明读取所有Sheet。
    ##返回一个字典dict,键key是工作表名,值value是工作表对应的DataFrame##
    # df_excel_dict = pd.read_excel(read_excel_filename, sheet_name = None, header = 0)
    df_excel_dict = pd.read_excel(read_excel_filename, sheet_name = None)
    print(f"\n读取Excel下所有WorkSheet\n{type(df_excel_dict)} \n" )
    # print(f"{df_excel_dict} \n" )
    return df_excel_dict

# if __name__=="__main__":
    ##调用Class, 数据收集——从Excel读取数据##
    # Collectdata()

    ##调试用##
    # read_excel_filename = r"C:\Users\86151\Desktop\2023-2020年江西高考一分一段表.xlsx"
    # sheetname = r"2023年江西高考理工类"

    # ##调用函数, 读取Excel下所有WorkSheet, 返回的DataFrame数据——df_excel_dict
    # ##调用函数, 返回一个字典dict,键key是工作表名,值value是工作表对应的DataFrame##
    # Collectdata.pandas_read_excel_dict(read_excel_filename)

    # ##调用函数, 读取Excel下单张WorkSheet, 返回的DataFrame数据——df_excel_sheet##
    # ##调用函数, 指定WorkSheet名字##
    # Collectdata.pandas_read_excel(read_excel_filename, sheetname)  
