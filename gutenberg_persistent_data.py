# -*- coding: utf-8 -*-
##Python文件名：gutenberg_persistent_data.py
##持久化数据, 将处理好的中间结果保存到磁盘文件或者数据库中##
##数据持久化——保存中间结果——提供写入和读取Excel/PG/MySQL接口##
##提供持久化接口——中间结果写入到Excel, 提供写入和读取Excel文件接口##
##提供持久化接口——中间结果写入到数据库PG, 提供写入和读取数据库接口##
##提供持久化接口——中间结果写入到数据库MySQL, 提供写入和读取数据库接口##

import pandas as pd  
import os
import xlsxwriter

def save_to_excel(df, save_excel_filename, sheet_name):
    '''统计英文小说的单词和词频, 一部小说存于一张WorkSheet, 保存到Excel文件##
    #engine="openpyxl"支持append模式, 写入多张WorkSheet
    #engine="xlsxwriter"不支持append模式, 会覆盖之前的Excel内容
    :param df: 包含单词和词频两个值的DataFrame,源数据是List-Dict
    :param save_excel_filename: Excel保存位置, 建议绝对路径
    :param sheet_name: 用英文小说名作为WorkSheet名称, 要求长度少于32个字符
    :return nothing but a Excel file
    '''
    # save_excel_filename = r"C:\Users\86151\Desktop\经典英文小说最高频单词和词频.xlsx"
    ##FileNotFoundError: [Errno 2] No such file or directory:  ##
    ##'C:\\Users\\86151\\Desktop\\经典英文小说最高频单词和词频.xlsx'  
    ##用程序生成Excel WorkSheet的名字##
    ##用程序生成txt的绝对路径##
    if os.path.exists(save_excel_filename):
        print(f"{save_excel_filename} 已经存在, 打开Excel写数据")
        print(f"……>>>数据已存入工作表 {sheet_name} ")
    else:  
        print(f"{save_excel_filename} 不存在, 现在就创建一个, 再打开Excel写数据")
        workbook = xlsxwriter.Workbook(save_excel_filename)
        ##添加一个工作表Sheet##
        worksheet = workbook.add_worksheet("总表")
        ##关闭Excel文件##
        workbook.close()
    ##写入Excel文件,engine="xlsxwriter"不支持append模式，替换为engine="openpyxl" ##
    # ##ValueError: Append mode is not supported with xlsxwriter!##
    # with pd.ExcelWriter(excel_filename, engine="xlsxwriter" ) as writer:
    with pd.ExcelWriter(save_excel_filename, engine="openpyxl", mode="a" ) as writer:
        df.to_excel(writer, sheet_name = sheet_name )

def save_to_excel_xlsxwriter(df, save_excel_filename, sheet_name = "总表"):
    '''合并多张WorkSheet的词频统计——写Excel文件, 保存排序后的DataFrame。
    #按词汇总——加总所有单词的词频, 单词按总词频倒序排列。
    #原本是一张WorkSheet保存一部小说的统计。
    #engine="openpyxl"支持append模式, 写入多张WorkSheet
    #engine="xlsxwriter"不支持append模式, 会覆盖之前的Excel内容
    :param df: 包含单词和词频两个值的DataFrame, 源数据是List-Dict
    :param save_excel_filename: Excel保存位置, 建议绝对路径
    :param sheet_name: Excel的工作簿名称, 此处设置默认值sheet_name = "总表"
    :return nothing but a Excel file
    '''
    # save_excel_filename = r"C:\Users\86151\Desktop\经典英文小说最高频单词和词频.xlsx"
    ##FileNotFoundError: [Errno 2] No such file or directory:  ##
    ##'C:\\Users\\86151\\Desktop\\经典英文小说最高频单词和词频.xlsx'  
    ##用程序生成Excel WorkSheet的名字##
    ##用程序生成txt的绝对路径##
    if os.path.exists(save_excel_filename):
        print(f"{save_excel_filename} 已经存在, 打开Excel写数据")
        print(f"……>>>数据已存入工作表 {sheet_name} ")
    else:  
        print(f"{save_excel_filename} 不存在, 现在就创建一个, 再打开Excel写数据")
        workbook = xlsxwriter.Workbook(save_excel_filename)
        ##添加一个工作表Sheet##
        worksheet = workbook.add_worksheet("总表")
        ##关闭Excel文件##
        workbook.close()
    ##写Excel文件, 保存排序后的DataFrame##
    with pd.ExcelWriter(save_excel_filename, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name)
    ##写入Excel文件, engine="xlsxwriter"不支持append模式，替换为engine="openpyxl" ##
    # ##ValueError: Append mode is not supported with xlsxwriter!##
    # with pd.ExcelWriter(save_excel_filename, engine="xlsxwriter" ) as writer:
    # with pd.ExcelWriter(save_excel_filename, engine="openpyxl", mode="a" ) as writer:
    #     df_merged.to_excel(writer, sheet_name = "Sheet1" )
