# -*- coding: utf-8 -*-
##Python文件名：gutenberg_wash_data.py
##数据收集-清洗-可视化展示, 三部曲中的数据清洗——清除无效数据##
##导入module##
from gutenberg_collect_data import recursive_listdir
from gutenberg_collect_data import read_from_txt
from gutenberg_persistent_data import save_to_excel

class Washdata():
    '''数据收集-清洗-可视化展示,三部曲中的数据清洗
    清洗从txt读入的英文小说, 会预先调用函数read_from_txt()和recursive_listdir()
    # 读取小说文件夹下的所有英文小说, 将[Word]和[Count]两列, 表示单词和词频, 
    # 存入Excel做持久化, 一张WorkSheet存一部小说的词频统计##
    清除无效数据——字符串'100及以下'和'691及以上'会导致绘图时出错。
    清洗Excel下单张WorkSheet返回的DataFrame数据——df_excel_sheet
    清洗Excel下所有WorkSheet返回的DataFrame数据——df_excel_dict
    '''
    def wash_data_txt(txt_file_directory, save_excel_filename):
        '''清洗从txt读入的英文小说, 会预先调用函数read_from_txt()和recursive_listdir()
        # 读取小说文件夹下的所有英文小说, 将[Word]和[Count]两列, 表示单词和词频, 
        # 存入Excel做持久化, 一张WorkSheet存一部小说的词频统计##
        :param txt_file_directory: txt文件存放目录,存放经典英文小说txt文件,为ANSI编码
        :param save_excel_filename: Excel文件绝对路径,一张WorkSheet存一部小说的词频统计
        :param txt_filename: txt英文小说文件名
        :param sheet_name: Excel下的workSheet名字
        :param vocabulary_df: 每部英文小说的词汇量, DataFrame格式
        :return none
        '''
        ##调用函数，递进遍历指定目录下的所有文件##
        txt_file_list = recursive_listdir(txt_file_directory)
        ##路径末尾不能带\,提示语法错误SyntaxError: unterminated string literal##
        for txt_file in txt_file_list:
            txt_filename = txt_file["txt_filename"]
            sheet_name = txt_file["sheet_name"]
            ##xlsxwriter.exceptions.InvalidWorksheetName: 
            ##Excel worksheet name 'Alice's Adventures in Wonderland' must be <= 31 chars.##
            if len(sheet_name) >= 30:
                print(f"{sheet_name} 书名太长了, Excel的WorkSheet名字不支持, 裁短它")
                sheet_name = sheet_name[:25]  
                print(f"新书名 {sheet_name} 用于Excel的WorkSheet名字")

                ##调用函数，从txt文件中读取小说文本, 做文本预处理和词频统计##
                vocabulary_df = read_from_txt(txt_filename)   

                ##调用函数，统计英文小说的单词和词频, 一部小说存于一张WorkSheet##
                save_to_excel(vocabulary_df, save_excel_filename, sheet_name) 

            else:
                ##调用函数，从txt文件中读取小说文本, 做文本预处理和词频统计##
                vocabulary_df = read_from_txt(txt_filename)   

                ##调用函数，统计英文小说的单词和词频, 一部小说存于一张WorkSheet##
                save_to_excel(vocabulary_df, save_excel_filename, sheet_name)  
        
    def wash_data_excel(df_excel_sheet):
        '''清洗Excel下单张WorkSheet返回的DataFrame数据——df_excel_sheet
        清除无效数据——字符串'100及以下'和'691及以上'会导致绘图时出错。
        ##处理办法:将包含'及以上'直接替换为【下一档分数+1分】(int类型)##
        ##特殊情况,三校生的的最高分,不包含'及以上',不作处理##
        ##处理办法:将'100及以下'直接替换为100分(int类型)##
        :param df_excel_sheet: 待清洗的源数据, 数据格式DataFrame##
        :return: df_excel_sheet
        '''
        # print(df_excel_sheet.columns)       ##数据集所有列的名字##
        # ##Index(['分数', '人数', '累计人数'], dtype='object')##
        ##打印'分数'列的第一个和第二个元素的值##
        # print(f"\n打印'分数'列的第一个和第二个元素的值")
        # print(df_excel_sheet.loc[0, "分数"])
        # print(df_excel_sheet.loc[1, "分数"])
        # print(df_excel_sheet["分数"][0])  ##不推荐, 做赋值时会报错##
        # print(df_excel_sheet["分数"][1])  ##不推荐, 做赋值时会报错##

        ##返回对象的个数,如果不指定列,返回n列的n倍值##
        print(f"返回'分数'列的数据行数: {df_excel_sheet["分数"].size}")
        df_column_size = df_excel_sheet["分数"].size

        ##打印'分数'列的倒数第一个和倒数第二个元素的值##
        # print(f"\n打印'分数'列的倒数第一个和倒数第二个元素的值")
        # print(df_excel_sheet.loc[(df_column_size - 1), "分数"])
        # print(df_excel_sheet.loc[(df_column_size - 2), "分数"])
        # print(df_excel_sheet.iloc[-1]["分数"])  ##不推荐, 做赋值时会报错##
        # print(df_excel_sheet.iloc[-2]["分数"])  ##不推荐, 做赋值时会报错##

        ##处理办法:将包含'及以上'直接替换为【下一档分数+1分】(int类型)##
        ##三校生的的最高分,不包含'及以上',不作处理##
        ##第一列df_excel_sheet.loc[0, "分数"]有种格式：有int，也有string。
        ##含字符串"691及以上"和"100及以下"，才做数据清洗##
        ##解决办法,做类型判断TypeError: argument of type 'int' is not iterable##
        ##保证检查到两个条件,小心else陷阱,导致数据未矫正,或数据不全##
        if isinstance(df_excel_sheet.loc[0, "分数"], str):
            ##"分数"列第一个元素是string类型,直接替换为【下一档分数+1分】(int类型)##
            if  "及以上"  in  df_excel_sheet.loc[0, "分数"] :
                df_excel_sheet.loc[0, "分数"] = (df_excel_sheet.loc[1, "分数"] + 1)          
        elif isinstance(df_excel_sheet.loc[0, "分数"], int):
            ##"分数"列第一个元素是int类型,不做数据清洗,原值返回##
            df_excel_sheet.loc[0, "分数"] = df_excel_sheet.loc[0, "分数"]
        else:
            print(f"{df_excel_sheet.loc[0, "分数"]} 不是string类型,也不是int类型")

        ##处理办法:将'100及以下'直接替换为100分(int类型好于float类型)##
        df_excel_sheet.loc[(df_column_size - 1), "分数"] = 100 
        # 采用df_excel_sheet.loc[0, "分数"]写法,正常可用##
        ##采用df_excel_sheet["分数"][0]写法,会报错A value is trying to be 
        # set on a copy of a slice from a DataFrame##
        ##采用df_excel_sheet.iloc[-1]["分数"]写法,报同样的错##
        return df_excel_sheet
 

    def wash_data_excel_dict(df_excel_dict):
        '''清洗Excel下所有WorkSheet返回的DataFrame数据——df_excel_dict
        清除无效数据——字符串'100及以下'和'691及以上'会导致绘图时出错。
        ##处理办法:将包含'及以上'直接替换为【下一档分数+1分】(int类型)##
        ##特殊情况,三校生的的最高分,不包含'及以上',不作处理##
        ##处理办法:将'100及以下'直接替换为100分(int类型)##
        :param df_excel_dict: 待清洗的源数据, 数据格式DataFrame##
        :return: df_excel_dict
        '''
        # # print(df_excel_dict.keys())       ##数据集dict所有key的名字##
        # ##用keys()方法遍历所有键，keys()方法返回一个包含字典所有键的迭代器，
        # ##可以用于遍历所有键##
        # for df_key in df_excel_dict.keys():
        #     print(type(df_key))
        #     print(df_key)

        ##用values()方法遍历所有值，values()方法返回一个包含字典所有值的迭代器，
        ##可以用于遍历所有值##
        for df_value in df_excel_dict.values():
            # print(type(df_value))
            # # print(df_value.head)
            # print(df_value.columns)       ##数据集所有列的名字##
            # ##Index(['分数', '人数', '累计人数'], dtype='object')##
            ##打印'分数'列的第一个和第二个元素的值##
            # print(f"\n打印'分数'列的第一个和第二个元素的值")
            # print(df_value.loc[0, "分数"])
            # print(df_value.loc[1, "分数"])
            # print(df_value["分数"][0])  ##不推荐, 做赋值时会报错##
            # print(df_value["分数"][1])  ##不推荐, 做赋值时会报错##

            ##返回对象的个数,如果不指定列,返回n列的n倍值##
            print(f"返回'分数'列的数据行数: {df_value["分数"].size}")
            df_column_size = df_value["分数"].size
            ##打印'分数'列的倒数第一个和倒数第二个元素的值##
            # print(f"\n打印'分数'列的倒数第一个和倒数第二个元素的值")
            # print(df_value.loc[(df_column_size - 1), "分数"])
            # print(df_value.loc[(df_column_size - 2), "分数"])
            # print(df_value.iloc[-1]["分数"])  ##不推荐, 做赋值时会报错##
            # print(df_value.iloc[-2]["分数"])  ##不推荐, 做赋值时会报错##

            ##处理办法:将包含'及以上'直接替换为【下一档分数+1分】(int类型)##
            ##三校生的的最高分,不包含'及以上',不作处理##
            ##第一列df_value.loc[0, "分数"]有种格式：有int，也有string。
            ##含字符串"691及以上"和"100及以下"，才做数据清洗##
            ##解决办法,做类型判断TypeError: argument of type 'int' is not iterable##
            ##保证检查到两个条件,小心else陷阱,导致数据未矫正,或数据不全##
            if isinstance(df_value.loc[0, "分数"], str):
                ##"分数"列第一个元素是string类型,直接替换为【下一档分数+1分】(int类型)##
                if  "及以上"  in  df_value.loc[0, "分数"] :
                    df_value.loc[0, "分数"] = (df_value.loc[1, "分数"] + 1)          
            elif isinstance(df_value.loc[0, "分数"], int):
                ##"分数"列第一个元素是int类型,不做数据清洗,原值返回##
                df_value.loc[0, "分数"] = df_value.loc[0, "分数"]
            else:
                print(f"{df_value.loc[0, "分数"]} 不是string类型,也不是int类型")

            ##处理办法:将'100及以下'直接替换为100分(int类型好于float类型)##
            df_value.loc[(df_column_size - 1), "分数"] = 100 
            # 采用df_excel_dict.loc[0, "分数"]写法,正常可用##
            ##采用df_excel_dict["分数"][0]写法,会报错A value is trying to be 
            # set on a copy of a slice from a DataFrame##
            ##采用df_excel_dict.iloc[-1]["分数"]写法,报同样的错##
        return df_excel_dict
 
if __name__=="__main__":
    ##调用Class, 数据清洗——清除无效数据 
    Washdata()   

    # ##调用函数, 清洗Excel下单张WorkSheet返回的DataFrame数据——df_excel_sheet##
    # Washdata.wash_data_excel(df_excel_sheet)

    # ##调用函数, 清洗Excel下所有WorkSheet返回的DataFrame数据——df_excel_dict##
    # Washdata.wash_data_excel_dict(df_excel_dict)