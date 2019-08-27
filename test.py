import configparser as ConfigParser
import pandas as pd
import numpy as np
import string
import os
import sys
import xlrd



def excelRead():
	teacherExcel=pd.read_excel("C:/Users/sky/Desktop/课表/2019.9月人事安排表(2019.8.25).xlsx", encoding='UTF-8')
	# data=teacherExcel.loc[:,["班级"]]
	# print(teacherExcel.loc[[0,17]])
	# print(teacherExcel.loc[:,["班主任"]].values)
	print(len(teacherExcel.columns.values))
	print(np.delete(teacherExcel.columns.values,0))
	# print(teacherExcel.columns.values[16])
	print(teacherExcel.loc[:,teacherExcel.columns.values[0]].values)
def conf():
	conf_par = ConfigParser.RawConfigParser(allow_no_value=True)
	conf_par.read("config.conf", encoding='UTF-8')
	all_sections = conf_par.sections()
	try:
		# 所有模块
		print(all_sections)
		# 获取所有options
		print(conf_par.options("班主任"))
		# 获取对应的值
		print(conf_par.get("班主任","武广英"))
	except ConfigParser.NoOptionError:
		print(ConfigParser.NoOptionError)


if __name__ == '__main__':
	# excelRead()
	# a={"班主任":[{"qq":[1,2]},{"ww":[3,4]}]}
	# print(a["班主任"][0]["qq"])

