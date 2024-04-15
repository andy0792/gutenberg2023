# -*- coding: utf-8 -*-
##Python文件名：visualization_plotly.py
##数据收集-清洗-可视化展示，三部曲中的数据可视化展示##
##Python可视化输出： 生成各种可视化chart##
##一个调用plotly, 画图的类
##plotly  5.18.0##

import plotly.express as px 


class Drawchartplotly():
    '''一个调用plotly.express, 画图的类'''

    def draw_plotly_df(df):
        '''绘制条形图bar, 绘制高频单词和出现频率
        :param df: 源数据的变量名, 源数据格式DataFrame
        return: none but draw a chart
        '''
        x_axis_data = df["topx_words"]
        y_axis_data = df["pct_topx_words"]
        ##对结果进行可视化##
        # fig = px.bar(x=poss_results, y=frequencies )
        title = "条形图——高频单词和出现频率"
        labels = {"x": "单词", "y":"Frequency出现频率"}
        fig = px.bar(x = x_axis_data, y = y_axis_data, title = title, labels = labels)
        ##x轴的布局给所有的条形加上标签##
        fig.update_layout(xaxis_dtick=1,)

        ##展示和保存图表只能二选一##
        # fig.show()
        fig.write_image(r"C:\Users\86151\Desktop\plot-express.png")
        ##保存图表格式也只能二选一##
        fig.write_html(r"C:\Users\86151\Desktop\plotly-express.html")
        # fig.write_json()

if __name__=="__main__":
    Drawchartplotly()   
