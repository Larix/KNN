#!/usr/bin/python
# -*- coding: utf-8 -*-
import jieba
import jieba.analyse

import math
import json
import sys

def load_news_training_data():
	"""
	載入ETTODAY NEWS新聞資料作為測試資料，產生訓練集向量與訓練集分類。 
	:return: 訓練集的向量及訓練集分類
	"""
	training_set_tf = dict()
	training_set_class = dict()
	keywords = list()

	with open('data/ettoday.news.json', 'r', encoding='utf-8') as file:
		news_data = json.load(file)
	for news in news_data:
		training_set_class[news['title']] = news['category']
		#保存每篇文章詞彙出現次數
		#seg_list = jieba.cut(news['content'])
		seg_list = jieba.analyse.extract_tags(news['content'], topK = 100)
		seg_content = {}
		for seg in seg_list:
			if seg in seg_content:
				seg_content[seg] += 1
			else:
				seg_content[seg] = 1
		#保存文章詞彙頻率
		training_set_tf[news['title']] = seg_content	
		#獲取關鍵詞
		keywords.extend(jieba.analyse.extract_tags(news['content'], topK = 100))
	#文章斷詞轉成向量表示
	seg_corpus = list(set(keywords))
	for title in training_set_tf:
		tf_list = list()
		for word in seg_corpus:
			if word in training_set_tf[title]:
				tf_list.append(training_set_tf[title][word])
			else:
				tf_list.append(0)
		training_set_tf[title] = tf_list

	return (training_set_tf, training_set_class, seg_corpus)

def get_article_vector(content, seg_corpus):
    """
    計算要測試的文章向量。
    :param content: 文章內容
    :param seg_corpus: 新聞關鍵詞彙語料庫
    :return: 文章的詞頻向量
    """

	#seg_list = jieba.cut(content)
    seg_content = {}
    seg_list = jieba.analyse.extract_tags(content, topK = 100)
    for seg in seg_list:
        if seg in seg_content:
            seg_content[seg] += 1
        else:
            seg_content[seg] = 1
	#產生vector		
    tf_list = list()
    for word in seg_corpus:
        if word in seg_content:
            tf_list.append(seg_content[word])
        else:
            tf_list.append(0)
    return tf_list

def cosine_similarity(v1, v2):
    """
    計算兩個向量的cosine similarity。數值越高表示距離越近，也代表越相似，範圍為0.0~1.0。
    :param v1: 輸入向量1
    :param v2: 輸入向量2
    :return: 2個向量的正弦相似度
    """
    #compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)
    sum_xx, sum_xy, sum_yy = 0.0, 0.0, 0.0
    for i in range(0, len(v1)):
    	x, y = v1[i], v2[i]
    	sum_xx += math.pow(x, 2)
    	sum_yy += math.pow(y, 2)
    	sum_xy += x * y
    try:
        return sum_xy / math.sqrt(sum_xx * sum_yy)	
    except ZeroDivisionError:
        return 0	

def knn_classify(input_tf, trainset_tf, trainset_class, k):
    """
    kNN分類演算法
    :param input_tf: 輸入向量
    :param trainset_tf: 訓練集的向量
    :param trainset_class: 訓練集的分類
    :param k: 決定最近鄰居取k個
    :return:
    """
    tf_distance = dict()
    # 計算每個訓練集合特徵關鍵字頻率向量和輸入向量的距離
    print ('(1) 計算向量距離')
    for position in trainset_tf.keys():
        tf_distance[position] = cosine_similarity(trainset_tf.get(position), input_tf)
        print ('\tDistance(%s) = %f' % (position.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding), tf_distance.get(position)))

    # 取出k個最近距離的分類
    class_count = dict()
    print ('(2) K個最近鄰居的分類, k = %d' % k)
    for i, position in enumerate(sorted(tf_distance, key=tf_distance.get, reverse=True)):
        current_class = trainset_class.get(position)
        print ('\t(%s) = %f, class = %s' % (position.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding), tf_distance.get(position), current_class))
        #將最接近的鄰居之分類做加權
        if i == 0:
        	class_count[current_class] = class_count.get(current_class, 0) + 2
       	else:
        	class_count[current_class] = class_count.get(current_class, 0) + 1
        if (i + 1) >= k:
            break

    print ('(3) 依K個最近鄰居中出現最高頻率的作分類')
    input_class = ''
    for i, c in enumerate(sorted(class_count, key=class_count.get, reverse=True)):
        if i == 0:
            input_class = c
        print ('\t%s, %d' % (c, class_count.get(c)))
    print ('(4) 分類結果 = %s' % input_class)

if __name__ == '__main__':
	trainset_tf, trainset_class, seg_corpus = load_news_training_data()
	content = "（中央社記者潘智義台北2日電）台北股市今天以平高盤開出，上半場維持漲勢，但清明節長假前賣壓出籠，指數收盤小跌以10888.27點作收，雖失守10900點關卡，但仍站在5日均線10885點之上。終場加權指數收在10888.27點，下跌31.22點，跌幅0.29%，成交值新台幣1019.43億元。8大類股當中，營建、紡織、食品類股漲勢較明顯，但電子、金融類股走弱。晶圓代工龍頭台積電收246.5元，小跌0.4%；系統組裝服務大廠鴻海收88.1元，小跌0.45%；股王大立光收3185元，下跌4.92%，再創波段新低。元大投顧分析師薛舜日表示，進入4月上市公司法人說明會密集期，第1季財報將成焦點，因新台幣第1季升值2.4%，高於去年第4季的1.5%，需留意外銷產業匯損的風險。薛舜日表示，美國政府鷹派當道，美國總統川普將貿易保護的重拳直接擊向中國，使3月全球金融市場再次出現劇烈震盪，雖然美國可望針對削減貿易赤字、對等開放市場兩大目標，與中方進行談判，有助於緩和全面性貿易戰的緊張情緒，但美國期中選舉將在第4季舉行，川普掀起的貿易戰恐不易快速平息。他說，4月中旬仍是融券回補高峰期，需提防回補近尾聲，帶來股市轉弱效應。"
	input_tf = get_article_vector(content, seg_corpus)
	knn_classify(input_tf, trainset_tf, trainset_class, k=3)