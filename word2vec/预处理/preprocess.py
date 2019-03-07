import os
import jieba
import sys
import re


def remove_punctuation(line):
	rule = re.compile(u"[^\u4e00-\u9fa5]")
	line = rule.sub('',line)
	return line

if __name__ == '__main__':
	out_file = open("./processed.out",'w')
	txt_files = []
	for root, dirs, files in os.walk("./"):
		for file in files:
			if file.endswith(".txt"):
				 txt_files.append(os.path.join(root, file))
				
				
	for txt_file in txt_files:
		in_file = open(txt_file, 'r')
		for line in in_file:
			line = remove_punctuation(line[:-1])
			if line == '':
				continue
			seg_list = jieba.cut(line, cut_all=False)
			out_file.write(" ".join(seg_list) + '\n')
			