#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import string, os, sys
import re
from collections import defaultdict
import random

# 过滤文件
def filter_files(files):
	newfiles = []
	for f in files:
		if f.endswith('.hrl'):
			newfiles.append(f)
	return newfiles

# 从错误码定义文件获取错误码段号 用于排序
# 错误码文件必须符合格式的行: # @doc NNN 模块名
def get_err_sect(filename):
	text_file = open(filename, "r")
	lines = text_file.readlines()
	sect = random.uniform(10000, 20000)
	for line in lines:
		m = re.match(r"%+\s*@doc\s*(\d+)\s*(.*)", line)
		if m:
			sect = int(eval(m.group(1)))
			break
		m = re.match(r"-define\((\w+),\s*(-{0,1}\d+)\)\.\s*%%\s*(.*)", line)
		if m:
			sect = int(eval(m.group(2))) / 1000
	
	text_file.close()
	return sect

# 文件排序
def sort_files(files):
	d = {}
	for f in files:
		sect = get_err_sect(f)
		d[f] = sect
		
	sort_kv = sorted(d.items(), lambda x, y: cmp(x[1], y[1]))
	
	sort_list = []
	for i in range(0, len(sort_kv)):
		sort_list.append(sort_kv[i][0])
	
	return sort_list	

# 解析一个错误码定义文件
cmd = 0
def gen_one_file(filename, outxml):
	text_file = open(filename, "r")
	lines = text_file.readlines()
	global cmd
	for line in lines:
		#print line
		m = re.match(r"%+\s*@doc\s*{(.*)}\s*{(.*)}", line)
		#print m
		if m:
			outxml.write("   <!-- " + m.group(1) + "\t" + m.group(2) + "-->\n")
		m = re.match(r"-define\((\w+),\s*(-{0,1}\d+)\)\.\s*%%\s*(.*)", line)
		if m:
			id = int(eval(m.group(2)))
			outxml.write("	<err>\n")
			outxml.write("		<code>" + str(id) + "</code>\n")
			outxml.write("		<desc>" + m.group(3) + "</desc>\n")
			outxml.write("	</err>\n")
			outerl.write("info(_ErrCode = " + str(id) + ") -> <<\"" + m.group(3) + "\">>;\n")
	text_file.close()
	outxml.write("\n")

# 解析目录下所有错误码定义文件
def gen_dir_files(dirname, outxml):
	files = os.listdir(dirname)
	for i in range(0, len(files)):
		files[i] = dirname + os.sep + files[i]
	
	files = filter_files(files)
	
	files = sort_files(files)
	
	for f in files:
		#print filename
		gen_one_file(f, outxml)

#print sys.argv

#准备文件
outxml = open('ErrorCode.xml','w')
outerl = open('src/errcode.erl', 'w')

#文件头
#xml
outxml.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
outxml.write("<xml>\n")
outxml.write("\n")
#erl
outerl.write("-module(erlcode).")
outerl.write("-export[info/1].\n\n")

#生成
gen_dir_files("include/errcode", outxml)

#文件尾
outxml.write("</xml>")
outerl.write("info(_) -> <<>>.\n")

#关闭文件
outxml.close()
outerl.close()

