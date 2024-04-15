# -*- coding: utf-8 -*-
##Python文件名：gutenberg_main.py
##古登堡计划(Gutenberg) ——主函数入口——批处理30部小说可视化（2023）##
##提供输入, 小说存放文件夹路径, 用于遍历读取所有英文小说TXT文本##
##提供输入, 存放每部小说按词频倒排结果, Excel的保存路径, 用于输出词云图##
##提供输入, 按词合并所有小说的词频统计结果, Excel的存储路径, 用于输出折线图和文字报告##
##调用函数, 绘制数据可视化图折线图和词云图##
##调用函数, 得到statistic文字报告##

##导入Class##
##绘制折线图, 绘制掌握最高频单词个数与理解全文的曲线关系##  
from visualization_matplotlib import Drawchart
from gutenberg_wash_data import Washdata
from visualization_plotly import Drawchartplotly

##导入module##
##准备词云图所需文本和小说名字##
from visualization_wordcloud import draw_batch_wordcloud

##导入module##
from gutenberg_collect_data import merge_excel_sheet
from gutenberg_analysis_engine import merge_sheet_by_word
from gutenberg_analysis_engine import prepare_data_dict
from gutenberg_txt_report import save_gutenberg_txt_report

##第一段——生成每部小说的词频统计结果##
# 主函数,古登堡计划(Gutenberg)项目--经典英文小说最高频单词和词频统计
# :param txt_file_directory: txt文件存放目录,存放经典英文小说txt文件,为ANSI编码
# :param save_excel_filename: Excel文件绝对路径,一张WorkSheet存一部小说的词频统计
##调用函数，递进遍历指定目录txt_file_directory下的所有文件##
##路径末尾不能带\,提示语法错误SyntaxError: unterminated string literal##
txt_file_directory = r"C:\Users\86151\Desktop\Gutenberg"  
save_excel_filename = r"C:\Users\86151\Desktop\经典英文小说最高频单词和词频.xlsx"


##第一段——耗时很长——将小说转为词频存入Excel, 绘制每部小说的词云图##
##调用Class类, 清洗从txt读入的小说, 将中间结果存入Excel##
##一张WorkSheet存一部小说的词频统计##
# Washdata.wash_data_txt(txt_file_directory, save_excel_filename)

##绘制每部小说的词云图##
# draw_batch_wordcloud(txt_file_directory)


##第二段——合并所有小说的词频统计结果,输出古登堡计划(Gutenberg)文字结论和可视化##
read_excel_filename = r"C:\Users\86151\Desktop\经典英文小说最高频单词和词频.xlsx"
save_excel_filename = r"C:\Users\86151\Desktop\经典英文小说词频总表.xlsx"
save_txt_filename = r"C:\Users\86151\Desktop\经典英文小说词频statistics统计.txt"  

##调用函数, 用Pandas同时读取Excel的多张WorkSheet, 合并为一个DataFrame##
df_merged = merge_excel_sheet(read_excel_filename)

##调用函数, 按词汇总,按总词频倒序排列——写Excel文件持久化,并返回排序排列后的DataFrame##
##在已合并多张WorkSheet并返回DataFrame格式数据的基础上, 
##按词汇总——加总所有单词的词频, 单词按总词频倒序排列——
##返回按词汇总后同样为DataFrame格式的df_pivot_sorted, 并写入Excel文件做数据持久化。
df_pivot_sorted = merge_sheet_by_word(df_merged, save_excel_filename)

##调用函数, 准备用于绘制折线图DataFrame数据——用于输出statistic文字报告的dict数据##
df_draw_chart_metadata, gutenberg_report_nested_dict = prepare_data_dict(df_pivot_sorted)

##调用函数, 输出statistic文字报告##
save_gutenberg_txt_report(gutenberg_report_nested_dict, save_txt_filename)

##调用Class类, 绘制折线图, 绘制掌握最高频单词个数与理解全文的曲线关系##
Drawchart.line_chart_df(df_draw_chart_metadata)

##调用Class类, 绘制条形图bar, 绘制高频单词和出现频率##
Drawchartplotly.draw_plotly_df(df_draw_chart_metadata)
