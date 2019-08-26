import configparser as ConfigParser
import string
import os
import sys





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
	conf()