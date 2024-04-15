# -*- coding: utf-8 -*-
##Python文件名：visualization_matplotlib.py
##Python可视化——绘制折线图——掌握单词个数与理解全文的曲线关系##
##一个调用matplotlib, 画图的类##

import matplotlib.pyplot as plt
##从pyplot导入MultipleLocator类，用于设置刻度间隔##
from matplotlib.pyplot import MultipleLocator 

class Drawchart():
    '''一个调用matplotlib.pyplot, 画图的类'''
    def line_chart_df(df):
        '''绘制折线图, 绘制掌握最高频单词个数与理解全文的曲线关系
        :param df: 源数据的变量名, 源数据格式DataFrame
        return: none but draw a chart
        '''
        x_axis_data = df["topx_words"]
        y_axis_data = df["pct_topx_words"]
        
        plt.style.use("seaborn-v0_8")
        ##define the size of the figure in(width, height) inch##
        fig, ax = plt.subplots(figsize = (22, 10), dpi = 128)    ##指定画布大小，英寸##
        ax.plot(x_axis_data, y_axis_data, linewidth=3)  

        ##红点突出高中词汇量3500和四级词汇量4200, 考研和六级词汇量5500+##
        ##index值是手工计算或者尝试出来的2n-1##
        # 设置注释文本的样式和箭头的样式
        bbox = dict(boxstyle="round", fc="0.8")
        bbox_green = dict(boxstyle="round", fc=(0.8,0.9,0.9), ec="b", alpha=0.8)
        ax.scatter(x_axis_data[6], y_axis_data[6], c = "red", edgecolors = "none", s = 100)
        ax.annotate(f"高中词汇量3500,理解全文的{y_axis_data[6]}", 
                    xy = (x_axis_data[6], y_axis_data[6]), 
                    xytext = (+30,-30), textcoords = 'offset points', 
                    fontsize = 16, bbox = bbox_green, 
                    arrowprops = dict(arrowstyle='->',connectionstyle="arc3,rad=.2"))

        ##红点突出四级词汇量4200##
        ax.scatter(x_axis_data[8],  y_axis_data[8], c = "red", edgecolors = "none", s = 100)
        ax.annotate(f"四级词汇量4200+,理解全文的{y_axis_data[8]}", 
                    xy = (x_axis_data[8], y_axis_data[8]), 
                    xytext = (-240,+30), textcoords = 'offset points', 
                    fontsize = 16, bbox = bbox_green, 
                    arrowprops = dict(arrowstyle='->',connectionstyle="arc3,rad=-0.2"))
        ##红点突出四级词汇量5000##
        ax.scatter(x_axis_data[9],  y_axis_data[9], c = "red", edgecolors = "none", s = 200)

        ##红点突出考研和六级词汇量5500+##
        ax.scatter(x_axis_data[10],  y_axis_data[10], c = "red", edgecolors = "none", s = 200)
        ax.annotate(f"考研和六级词汇量5500+,理解全文的{y_axis_data[10]}", 
                    xy = (x_axis_data[10], y_axis_data[10]), 
                    xytext = (+30,-30), textcoords = 'offset points', 
                    fontsize = 16, bbox = bbox_green, 
                    arrowprops = dict(arrowstyle='->',connectionstyle="arc3,rad=.2"))

        ##红点突出看美剧和专八级熟练掌握词汇量8000##
        ax.scatter(x_axis_data[15],  y_axis_data[15], c = "red", edgecolors = "none", s = 300)
        ax.annotate(f"看美剧和专八熟练掌握词汇量8000,理解全文的{y_axis_data[15]}", 
                    xy = (x_axis_data[15], y_axis_data[15]), 
                    xytext = (-240,+30), textcoords = 'offset points', 
                    fontsize = 16, bbox = bbox_green, 
                    arrowprops = dict(arrowstyle='->',connectionstyle="arc3,rad=-0.2"))

        ##红点突出阅读英文原著小说词汇量12500, 专八词汇量13000##
        ax.scatter(x_axis_data[24],  y_axis_data[24], c = "red", edgecolors = "none", s = 400)
        ax.annotate(f"阅读英文原著小说词汇量12500,理解全文的{y_axis_data[24]}", 
                    xy = (x_axis_data[24], y_axis_data[24]), 
                    xytext = (-240,+30), textcoords = 'offset points', 
                    fontsize = 16, bbox = bbox_green, 
                    arrowprops = dict(arrowstyle='->',connectionstyle="arc3,rad=-0.2"))

        ##红点突出专八词汇量13000##
        ax.scatter(x_axis_data[25],  y_axis_data[25], c = "red", edgecolors = "none", s = 400)
        ax.annotate(f"专八词汇量13000,理解全文的{y_axis_data[25]}", 
                    xy = (x_axis_data[25], y_axis_data[25]), 
                    xytext = (+30,-30), textcoords = 'offset points', 
                    fontsize = 16, bbox = bbox_green, 
                    arrowprops = dict(arrowstyle='->',connectionstyle="arc3,rad=.2"))

        x_major_locator = MultipleLocator(500)        ##x轴的刻度间隔##
        ##传入为百分数时,加上此注释; 若y_axis_data传入为小数,去掉此注释; ##
        # y_marjor_locator = MultipleLocator(0.02)       ##y轴的刻度间隔##
        ax = plt.gca()      ##ax为两条坐标轴的实例##
        ax.xaxis.set_major_locator(x_major_locator)     ###设置x和y轴的主刻度#
        ##传入为百分数时,加上此注释; 若y_axis_data传入为小数,去掉此注释; ##
        # ax.yaxis.set_major_locator(y_marjor_locator)    ###设置x和y轴的主刻度#

        ##设置横纵坐标标签，加上图标题##
        ax.set_xlabel("掌握最高频单词个数", fontsize = 20)
        ax.set_ylabel("理解全文的程度(总词频占比)", fontsize = 18)
        ax.set_title("掌握单词个数与理解全文的曲线关系", fontsize = 28)
        ax.tick_params(labelsize = 14)  ##设置刻度标记的样式##

        plt.xlim(500, 20000)          ##指定x轴刻度范围##
        ##把x轴的刻度范围设置为500到20000##
        ##传入为百分数时,加上此注释; 若y_axis_data传入为小数,去掉此注释; ##
        # plt.ylim(0.4, 1)       ##指定y轴刻度范围##
        # plt.ylim(0, 1)         ##指定y轴刻度范围##
        ##把y轴的刻度范围设置为0到1##
        plt.xticks(rotation = 30)        ##设置x轴标签刻度倾斜,数字为倾斜的角度##
        plt.yticks(rotation = 30)        ##设置y轴标签刻度倾斜,数字为倾斜的角度##

        ##图表显示中文##
        # plt.rcParams['font.sans-serif'] = ['YouYuan']
        plt.rcParams['font.sans-serif'] = ['SimHei']
        ##Matplotlib绘制的坐标轴无法显示负号，只出现了框框##
        # plt.rcParams["axes.unicode_minus"] = False 

        ##展示和保存图表只能二选一##
        # plt.show()
        plt.savefig(r"C:\Users\86151\Desktop\掌握单词个数与理解全文的曲线关系.png", bbox_inches = "tight")

if __name__=="__main__":
    Drawchart()   
