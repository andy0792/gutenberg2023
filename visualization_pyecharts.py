# -*- coding: utf-8 -*-
##Python文件名：visualization_pyecharts.py
##数据收集-清洗-可视化展示，三部曲中的数据可视化展示##
##Python可视化输出： 生成各种可视化chart##
##一个调用pyecharts, 画图的类

import re
import os
import pandas as pd
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Grid
from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode





