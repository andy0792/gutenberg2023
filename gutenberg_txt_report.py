# -*- coding: utf-8 -*-
##Python文件名：gutenberg_txt_report.py
##写入txt文件log文件——报告样式和组织语言——输出statistic文字报告

import time 

def save_gutenberg_txt_report(gutenberg_report_nested_dict, save_txt_filename):
    '''输出statistic文字报告
    写入txt文件log文件——报告样式和组织语言——输出statistic文字报告
    :param df_pivot_sorted: 已按词汇总——pivot——sorted排序后的数据, DataFrame格式
    :param save_txt_filename: 保存txt文件路径, 建议绝对路径
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
    :return nothing
    '''
    ##从嵌套字典dict-dict报告头部的Key-Value键值对, 还原为变量, 方便调用##
    vocabulary = gutenberg_report_nested_dict["vocabulary"]
    total_words_num = gutenberg_report_nested_dict["total_words_num"]
    high_freq_top20 = gutenberg_report_nested_dict["high_freq_top20"]
    pct_high_freq_top20 = gutenberg_report_nested_dict["pct_high_freq_top20"]
    occurrences_high_freq_top20 = gutenberg_report_nested_dict["occurrences_high_freq_top20"]
    ##在with控制块结束时，文件会自动关闭，就不需要再调用close()方法##
    ##想保存时将原文清空，可将第二个参数改写为w ##
    with open(save_txt_filename, "a", encoding = "utf-8") as file:
    ##用items()方法遍历所有键值对，items()方法返回一个包含字典所有键值对的迭代器，
    ##可以用于遍历所有键值对key, value。
    # with open(save_txt_filename, "w", encoding = "utf-8") as file:
        file.write('\n' + '=' * 50 + '\n')  #用file.write()方法写50个=号作为分隔符
        file.write(f"{time.asctime()}   \n")
        file.write(f"经典英文小说词频statistics统计—— \n") 
        file.write(f"共有 {vocabulary:,} 个词频, 单词共 {total_words_num:,} 个。\n\n") 
        file.write(f"Q: 前20%的最高频单词, 占全文词汇量（总词频）的多少, 是80%吗? \n") 
        file.write(f"A: 需要掌握 {high_freq_top20:,}个单词。\n") 
        file.write(f"前20%的最高频单词, 出现了 {occurrences_high_freq_top20:,} 次, \n") 
        file.write(f"共有{vocabulary:,}词频, 全文词汇量占比 {pct_high_freq_top20} \n")   
        file.write('\n' + '=' * 50 + '\n')  #用file.write()方法写50个=号作为分隔符
        ##从上述gutenberg_report_nested_dict["report_body_dict"]取值##
        # print(type(gutenberg_report_nested_dict))
        # # 输出<class 'dict'>
        # print(type(gutenberg_report_nested_dict["middle_topx_words_list"]))
        # # 输出<class 'list'>
        # print(gutenberg_report_nested_dict)
        for item in gutenberg_report_nested_dict.get("middle_topx_words_list"):
            file.write(f" {item}。\n")  
        file.write('\n' + '=' * 50 + '\n')  #用file.write()方法写50个=号作为分隔符
        file.write(f"\n")
     

##文件名：高考报告_2023年.txt
##完整路径：C:\Users\86151\Desktop\高考报告_2023年.txt
##文件名：高考statistic文字报告.txt
##完整路径：C:\Users\86151\Desktop\高考statistic文字报告
def save_statistical_text_report(gaokao_nested_dict, save_txt_filename):
    '''输出statistic文字报告
    写入txt文件log文件——报告样式和组织语言——输出statistic文字报告
    :param df_pivot_sorted: 已按词汇总——pivot——sorted排序后的数据, DataFrame格式
    :param save_txt_filename: 保存txt文件路径,建议绝对路径
    :param df_washed_dict: 源数据的变量名, 源数据格式DataFrame
    :param nested_dict: 数据格式dict, 和df_excel_dict键一样, 存储高考分数线
    :param df_column_size: 高考分数档位, df["分数"]的size
    :param gaokao_competitors: 全省高考总人数(分科 理工,文史,三校文理)
    :param gaokao_1st_score: 高考一本分数线dot1_x
    :param gaokao_2nd_score: 高考二本分数线/三校生的本科线dot2_x
    :param gaokao_3rd_score: 高考专科分数线dot3_x
    :param competitors_1st_score: 高考一本分数线——同分人数dot1_y
    :param competitors_2nd_score: 高考二本分数线/三校生的本科线——同分人数dot2_y
    :param competitors_3rd_score: 高考专科分数线——同分人数dot3_y
    :param rank_1st_score: 高考一本分数线全省排名dot1_rank
    :param rank_2nd_score: 高考二本分数线全省排名/三校生的本科线dot2_rank
    :param rank_3rd_score: 高考专科分数线全省排名dot3_rank
    :param top_pct_1st_score: 高考一本分数线领先全省多少考生(百分比%)dot1_pct
    :param top_pct_2nd_score: 高考二本分数线领先全省多少考生(百分比%)dot2_pct
    :param top_pct_3rd_score: 高考专科分数线领先全省多少考生(百分比%)dot3_pct
    :param gte_1000_competitors: 同分人数超过1000人(含)的高考分数、同分人数……等
    :param gte_1000_competitors_list: 装字典的list, 数据结构list-dict
    :return nothing
    '''
    ##在with控制块结束时，文件会自动关闭，就不需要再调用close()方法##
    ##想保存时将原文清空，可将第二个参数改写为w ##
    with open(save_txt_filename, "a", encoding = "utf-8") as file:
    ##用items()方法遍历所有键值对，items()方法返回一个包含字典所有键值对的迭代器，
    ##可以用于遍历所有键值对key, value。
        ##gaokao_year_subject, inner_dict就是dict的Key和Value##
        for gaokao_year_subject, inner_dict in gaokao_nested_dict.items():
            # print(df_excel_sheetname)
            ##两个dict字典的Key同名##
            # with open(save_txt_filename, "w", encoding = "utf-8") as file:
            file.write('\n' + '=' * 50 + '\n')  #用file.write()方法写50个=号作为分隔符
            file.write(f"{time.asctime()}   \n")
            file.write(f"\n当前科目:【{gaokao_year_subject}】 ")   
            file.write(f"\n全省高考人数有 {inner_dict.get("gaokao_competitors")} 人")   
            file.write(f"\n一共有{inner_dict.get("df_column_size")}个分数档位, 提及的数据均已保存。\n")

            file.write(f"\n一本分数线{inner_dict.get("gaokao_1st_score")}分，")  
            file.write(f"全省排 {inner_dict.get("rank_1st_score")}名，")   
            file.write(f"全省前 {inner_dict.get("top_pct_1st_score")}考生，")  
            file.write(f"一本分数线——同分人数{inner_dict.get("competitors_1st_score")}人。\n")  

            file.write(f"\n二本分数线{inner_dict.get("gaokao_2nd_score")}分，") 
            file.write(f"全省排 {inner_dict.get("rank_2nd_score")}名，")  
            file.write(f"全省前 {inner_dict.get("top_pct_2nd_score")}考生，")    
            file.write(f"二本分数线——同分人数{inner_dict.get("competitors_2nd_score")}人。\n")  

            file.write(f"\n专科分数线{inner_dict.get("gaokao_3rd_score")}分，") 
            file.write(f"全省排 {inner_dict.get("rank_3rd_score")}名，")  
            file.write(f"全省前 {inner_dict.get("top_pct_3rd_score")}考生，")    
            file.write(f"专科分数线——同分人数{inner_dict.get("competitors_3rd_score")}人。\n")   
            file.write(f"\n")  
            file.write(f"\n同分人数超过1000人(含)的高考分数、同分人数、全省排名:\n")
            ##打印同分人数超过1000人(含)的高考分数、同分人数、全省排名##
            # file.write(f" {inner_dict.get("gte_1000_competitors")}。 \n")
            ##装字典的list, 数据结构list-dict##  
            for item in inner_dict.get("gte_1000_competitors"):
                file.write(f" {item}。\n")  
            file.write(f"\n\n")
