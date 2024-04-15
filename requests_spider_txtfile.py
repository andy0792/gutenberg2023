# -*- coding: utf-8 -*-
##Python文件名：requests_spider_txtfile.py
##从Excel文件批量读取下载链接URL,用爬虫下载古登堡计划(Gutenberg)英文小说,存为txt文件##
##文件名：Python读写Excel文件.xlsx
##完整路径：C:\Users\86151\Desktop\Python读写Excel文件.xlsx

import requests  
import pandas as pd
import time 

def save_to_txt(url, save_txt_filename):
    '''用爬虫下载古登堡计划(Gutenberg)英文小说, 存为txt文件
    #古登堡计划(Gutenberg)提供两种版本, txt版本和在线阅读版, 
    #函数save_to_txt()解析html提取内容的写法有差异##
    :param url: 书目对应古登堡计划(Gutenberg)中的网址URL
    :param save_txt_filename: 希望保存书目的文件名,建议用绝对路径
    '''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"}
    html_response = requests.get(url, headers=headers).text
   
    # ##写法一，在with控制块结束时，文件会自动关闭，就不需要再调用close()方法##
    # ##想保存时将原文清空，可将第二个参数改写为w ##
    # with open(save_txt_filename, "a", encoding = "utf-8") as file:
    with open(save_txt_filename, "w", encoding = "utf-8") as file:
        file.write('\n' + '=' * 50 + '\n')
        file.write('\n'.join([html_response]))     #用file对象的write()方法将提取的内容写入文件
        file.write('\n' + '=' * 50 + '\n')  


def read_from_excel(excel_filename, sheet_name):
    '''从Excel文件批量读取下载链接URL, 英文书名用于传参,最终用于Excel的Sheet命名##
    :param excel_filename: excel文件名称
    :param sheet_name: excel中表格sheet名称
    '''
    df =  pd.read_excel(excel_filename, sheet_name) 
    print(type(df))     
    print(df.columns)       ##数据集所有列的名字##
    ##输出 Index(['序号', '中文小说名', '英文小说名', '作者', '古登堡计划URL地址'], dtype='object')##  
    print(df)

    for i in df.index:
        # print(df["英文小说名"][i])
        # print(df["古登堡计划URL地址"][i])
        ##拼接网址加https:// 协议头 gutenberg.org/cache/epub/1342/pg1342.txt#
        https_url = rf"https://{df["古登堡计划URL地址"][i]}"
        save_txt_filename = rf"C:\Users\86151\Desktop\Gutenberg\{df["英文小说名"][i]}.txt"
        # print(https_url)
        # print(save_txt_filename)
  
        print(f"开始第{(i + 1)} 个任务,书名为{df["英文小说名"][i]}, 从{https_url}下载,将网页保存为txt文件,保存到{save_txt_filename}")

        ##调用函数，将网页保存为txt文件##
        save_to_txt(https_url, save_txt_filename)

        ##暂停60秒,防止IP被网站ban##
        time.sleep(60)
        print(f"暂停60秒,防止IP被网站ban")
        

if __name__=="__main__":
    excel_filename = r"C:\Users\86151\Desktop\Python读写Excel文件.xlsx"
    sheet_name = r"古登堡计划"
    ##调用函数，从Excel文件中读取古登堡计划(Gutenberg)指定书目, URL等信息##
    read_from_excel(excel_filename, sheet_name)

    # ##古登堡计划(Gutenberg)提供两种版本, txt版本和在线阅读版, 
    # # 函数save_to_txt()解析html提取内容的写法有差异##
    # url = r"https://www.gutenberg.org/cache/epub/72398/pg72398.txt"
    # save_txt_filename = r"C:\Users\86151\Desktop\Gutenberg\pg72398.txt"
    # ##调用函数，将网页保存为txt文件##
    # save_to_txt(url, save_txt_filename)