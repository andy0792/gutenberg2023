# -*- coding: utf-8 -*-
##Python文件名：gutenberg_analysis_engine.py
##分析引擎——df_pivot_statistic——提供接口和准备绘图/报告所需数据,数据落盘持久化##
# 提供接口——get_topx_words_pct()通过计算pct_topx_words, 返回占全文词汇量占比。
# 准备数据——prepare_data_dict()准备用于绘制折线图和输出statistic文字报告的数据
# 按词汇总——merge_sheet_by_word()在已合并多张WorkSheet并返回DataFrame格式数据的基础上, 
# 按词汇总——加总所有单词的词频, 单词按总词频倒序排
# 返回按词汇总后同样为DataFrame格式的df_pivot_sorted, 并写入Excel文件做数据持久化。##
import pandas as pd 
import numpy as np 
import math 
##导入module##
from gutenberg_persistent_data import save_to_excel_xlsxwriter

def merge_sheet_by_word(df, save_excel_filename):
    '''在已合并多张WorkSheet并返回DataFrame格式数据的基础上, 
    按词汇总——加总所有单词的词频, 单词按总词频倒序排列——
    返回按词汇总后同样为DataFrame格式的df_pivot_sorted, 并写入Excel文件做数据持久化。
    :param df: 用Pandas逐个读取单张WorkSheet的数据, 数据格式DataFrame
    :param df_pivot: 用pd.groupby()分组,用.agg({"Count":"sum"}加总已分组的Count列
    :param df_pivot_sorted: 用df.sort_values(), 以加总后的Count列倒序排列
    :param save_excel_filename: 合并后的DataFrame存放位置, 建议绝对路径
    :param df_pivot_sorted : 按词汇总合并后的DataFrame, 包含所有工作表的数据——
    ##加总所有单词的词频, 单词按总词频倒序排列。
    :return df_pivot_sorted 
    '''
    ##按词汇总——数据透视表功能——按词频倒序排列##
    ##用pd.groupby()分组。用.agg({"Count":"sum"} 加总已分组的Count列##
    ##用df.sort_values(), 以加总后的Count列倒序排列##
    df_pivot = df.groupby("Word", sort="Count").agg({"Count":"sum"})  
    df_pivot_sorted = df_pivot.sort_values( by = ["Count"], ascending = False )
    ##排序后的df_pivot_sorted格式为<class 'pandas.core.frame.DataFrame'> ##
    # print(type(df_pivot_sorted))   

    ##写Excel文件, 保存排序后的DataFrame##
    ##调用函数，合并多张WorkSheet的词频统计——原本是一张WorkSheet保存一部小说的统计##
    ##按词汇总——加总所有单词的词频, 单词按总词频倒序排列##
    save_to_excel_xlsxwriter(df_pivot_sorted, save_excel_filename )   
    return df_pivot_sorted  

def get_topx_words_pct(df_pivot_sorted, topx_words = 3500):
    '''通过计算pct_topx_words, 返回占全文词汇量占比, 可切换输出的格式——小数or分数。
    :param df_pivot_sorted: 源数据的变量名, 源数据格式DataFrame
    :param total_words_num: 全部单词个数, 不算重复单词
    :param vocabulary: 词汇量，重复单词也算
    :param topx_words: 最高频单词, 如top3500_words表示3500个最高频单词
    :param pct_topx_words: 全文词汇量的占比, 如pct_top3500_words表示3500个单词占比
    :param occurrence_topx_words: 3500个最高频单词, 出现总次数
    :param high_freq_top20: 前20%的最高频单词个数, 重复单词也算向上求整, 单词个数
    :param pct_high_freq_top20: 前20%的最高频单词个数, 占全文词汇量的占比
    return pct_topx_words
    '''
    # total_words_num = df_pivot_sorted.size              ##全部单词个数, 不算重复单词##
    vocabulary = sum(df_pivot_sorted["Count"])          ##词汇量，重复单词也算##
    ##计算掌握前5000个最高频单词, 占全文词汇量的多少##
    df_topx_words = df_pivot_sorted.head(topx_words)    ##切片, 前3500个最高频单词##
    occurrence_topx_words = sum(df_topx_words["Count"])       ##3500个最高频单词,出现总次数##
    pct_topx_words = occurrence_topx_words / vocabulary       ##计算占比,3500个最高频单词##

    ##可切换输出的格式——小数or分数, 影响到折线图的纵坐标plt.yticks标签刻度的密集程度##
    # return  pct_topx_words  ##返回小数, topx_words占全文词汇量占比##
    return f"{pct_topx_words:.0%}"  ##返回百分数不带小数，topx_words占全文词汇量占比##
    # return f"{pct_topx_words:.1%}"  ##太密集了，此处不推荐百分数带1位小数##

def get_stacking_occurrences(df_pivot_sorted, topx_words = 3500):
    '''通过计算occurrence_topx_words, 返回叠加出现次数,  
    ##如3500个最高频单词, 出现总次数。
    :param df_pivot_sorted: 源数据的变量名, 源数据格式DataFrame
    :param total_words_num: 全部单词个数, 不算重复单词
    :param vocabulary: 词汇量，重复单词也算
    :param topx_words: 最高频单词, 如top3500_words表示3500个最高频单词
    :param pct_topx_words: 全文词汇量的占比, 如pct_top3500_words表示3500个单词占比
    :param occurrence_topx_words: 3500个最高频单词, 出现总次数
    :param high_freq_top20: 前20%的最高频单词个数, 重复单词也算向上求整, 单词个数
    :param pct_high_freq_top20: 前20%的最高频单词个数, 占全文词汇量的占比
    :return occurrence_topx_words
    '''
    # total_words_num = df_pivot_sorted.size              ##全部单词个数, 不算重复单词##
    # vocabulary = sum(df_pivot_sorted["Count"])          ##词汇量，重复单词也算##
    ##计算掌握前5000个最高频单词, 占全文词汇量的多少##
    df_topx_words = df_pivot_sorted.head(topx_words)    ##切片, 前3500个最高频单词##
    ##3500个最高频单词, 出现总次数##
    occurrence_topx_words = sum(df_topx_words["Count"])       
    # pct_topx_words = occurrence_topx_words / vocabulary       ##计算占比,3500个最高频单词##
    return occurrence_topx_words  ##返回3500个最高频单词, 出现总次数##
   

def prepare_data_dict(df_pivot_sorted):
    '''准备用于绘制折线图DataFrame数据——用于输出statistic文字报告的dict数据。
    :param df_pivot_sorted: 源数据的变量名, 源数据格式DataFrame
    :param total_words_num: 全部单词个数, 不算重复单词
    :param vocabulary: 总词频，重复单词也算
    :param topx_words_list: 最高频单词, 如top3500_words表示3500个最高频单词
    :param pct_topx_words_list: 全文词汇量的占比, 如pct_top3500_words表示3500个单词占比
    :param high_freq_top20: 前20%的最高频单词个数, 重复单词也算向上求整, 单词个数
    :param pct_high_freq_top20: 前20%的最高频单词个数, 占全文词汇量的占比
    :param report_nested_dict: 嵌套字典dict-dict, 存报告头部和主体两个dict##
    :param inner_topx_words_dict: 内层dict, 数据结构——字典dict-列表list-字典dict
    :param middle_topx_words_list: 中间层list, 数据结构——字典dict-列表list-字典dict
    :param outer_topx_words_dict: 外层dict, 临时的容器, 追加到report_nested_dict
    :param df_draw_chart_metadata: 为画图准备的DataFrame格式数据
    :return df_draw_chart_metadata, report_nested_dict
    '''
    ##计算20%的最高频单词, 有多少个单词, 全文词汇占比多少##
    total_words_num = df_pivot_sorted.size          ##全部单词个数, 不算重复单词##
    vocabulary = sum(df_pivot_sorted["Count"])      ##词汇量，重复单词也算##
    ##计算掌握前20%的最高频单词, 共有多少个单词, 占全文词汇量的多少##
    high_freq_top20 = math.ceil(total_words_num * 0.2)      ##向上求整, 单词个数##
    ##计算掌握前20%的最高频单词, 占全文词汇量的多少##
    pct_high_freq_top20 = get_topx_words_pct(df_pivot_sorted, high_freq_top20 )
    ##前20%的最高频单词, 叠加出现次数##
    occurrences_high_freq_top20 = get_stacking_occurrences(df_pivot_sorted, high_freq_top20 )
    ##为输出statistic文字报告准备的dict格式数据, 报告头部##
    report_nested_dict = {"total_words_num": total_words_num,
                        "vocabulary": vocabulary,
                        "high_freq_top20": high_freq_top20,
                        "pct_high_freq_top20": pct_high_freq_top20,
                        "occurrences_high_freq_top20": occurrences_high_freq_top20
                       }
    ##计算20%的最高频单词, 有多少个单词, 全文词汇占比多少##
    ##准备数据, np.arange()左闭右开, 不包括20001值本身, 构造pd.DataFrame()##
    topx_words_list = np.arange(500, 20001, step = 500)
    pct_topx_words_list = []
    occurrences_topx_words_list = []
    # print(type(topx_words))     ##输出<class 'numpy.ndarray'>##
    ####
    for pct_item in topx_words_list:
        pct_topx_words_list.append(get_topx_words_pct(df_pivot_sorted, pct_item))
        occurrences_topx_words_list.append(get_stacking_occurrences(df_pivot_sorted, pct_item))
    # print(type(pct_topx_words)) ##输出<class 'list'>##
    ##构造pd.DataFrame()##
    df_draw_chart_metadata = pd.DataFrame({
        "topx_words":topx_words_list,
        "pct_topx_words":pct_topx_words_list,
    }) 
    # print(type(df_draw_chart_metadata))     
    ##输出<class 'pandas.core.frame.DataFrame'>##
    # print(type(df_draw_chart_metadata["topx_words"]))  
    ##输出<class 'pandas.core.series.Series'>
    # print(type(df_draw_chart_metadata["pct_topx_words"]))  
    ##输出<class 'pandas.core.series.Series'>
    # print(df_draw_chart_metadata.head)
    ##数据结构——字典dict-列表list-字典dict, 中间那层list##
    middle_topx_words_list = []
    ##df.items(): 按列遍历, 将DataFrame的每一列迭代为(列名, Series)对，
    ##通过row[index]对元素进行访问##
    for index, row in df_draw_chart_metadata["pct_topx_words"].items():
        ##在循环体内, 拼接字符串##
        topx_words = df_draw_chart_metadata["topx_words"].loc[index]
        pct_topx_words = df_draw_chart_metadata["pct_topx_words"].loc[index]
        ##遍历列表取值##
        occurrences_topx_words = occurrences_topx_words_list[index]
        ##打印前x个单词、前x个单词的总词频占比、前x个单词的叠加总次数##
        inner_topx_words_dict = {"前x个单词topx_words": topx_words,
                      "前x个单词的总词频占比pct_topx_words": pct_topx_words,
                      "前x个单词的叠加总次数occurrences_topx_words": occurrences_topx_words
                      }
        # print(inner_topx_words_dict)
        # {'topx_words': 500, 'pct_topx_words': '41%', 'occurrences_topx_words': 760849}
        # {'topx_words': 1000, 'pct_topx_words': '53%', 'occurrences_topx_words': 996698}
        # {'topx_words': 1500, 'pct_topx_words': '61%', 'occurrences_topx_words': 1138994}
        ##将遍历得来的多个字典dict逐个append到列表list中##
        middle_topx_words_list.append(inner_topx_words_dict)
        # print(report_body_list)
    ##循环体外, 将list封装为dict, 用于追加到最外层dict字典report_nested_dict##
    ##数据结构——字典dict-列表list-字典dict##
    outer_topx_words_dict = {"middle_topx_words_list": middle_topx_words_list}
    ##用合并两个字典的方式, 实现append的效果##
    ##数据结构——字典dict-列表list-字典dict##
    report_nested_dict.update(outer_topx_words_dict)
    ##在循环体外, return##
    return df_draw_chart_metadata, report_nested_dict   