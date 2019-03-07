import jieba
import sys
import re
def load_stopwords(path):
	f = open(path,'r')
	result = []
	for line in f:
		result.append(line[:-1])	
	return result

def remove_punctuation(line):
	rule = re.compile(u"[^\u4e00-\u9fa5]")
	line = rule.sub('',line)
	return line

if __name__ == '__main__':
 
	inp, outp1 = sys.argv[1:3]
	
	in_file = open(inp, 'r')
	
	out_file = open(outp1, 'w')
	
#	stopwords = load_stopwords("./stopwords.txt")
	
	i = 0

	for line in in_file:
		
		
		line = remove_punctuation(line[:-1])
		
		seg_list = jieba.cut(line, cut_all=False)
#		words = []
#		for word in seg_list:
#			if len(word) < 2 or word in stopwords:
#				continue
#			else:
#				words.append(word)
		out_file.write(" ".join(seg_list) + '\n')
		
		i = i + 1
		if (i % 10000 == 0):
			print("processed " + str(i) + " lines")
 
