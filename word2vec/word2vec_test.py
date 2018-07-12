# coding: utf-8

import os
import sys
import logging
import word_cut
import model_train
from gensim.models import word2vec

reload(sys)
sys.setdefaultencoding('utf8')

file_name = './data/倚天屠龙记.txt'
train_file_name = file_name + '_cut'
model_file = file_name + '.model'
model_file_bin = file_name + '.model.bin'

def word2vec_test():
    print 'word2vec_test begin.'
    try:
        # 加载日志输出配置
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        # 加载文件切词
        print '加载文件:%s 切词后存放为:%s.' % (file_name, train_file_name)
        if not os.path.exists(file_name):    # 判断文件是否存在，参考：https://www.cnblogs.com/jhao/p/7243043.html
            print '加载文件切词失败。'
            exit(0)
        else:
            word_cut.cut_txt(file_name, train_file_name)  # 须注意文件必须先另存为utf-8编码格式

        # 训练模型
        print '从文件:%s 训练模型存放在: %s' % (train_file_name, model_file)
        if not os.path.exists(model_file):     # 判断文件是否存在
            model_train.model_train(train_file_name, model_file)
        else:
            print('此训练模型已经存在，不用再次训练')

        # 加载已训练好的模型
        print '从文件:%s 中加载模型' % model_file
        # model_1 = gensim.models.KeyedVectors.load_word2vec_format(model_file_bin, binary=True)
        model_1 = word2vec.Word2Vec.load(model_file)

        # 计算两个词的相似度/相关程度
        y1 = model_1.similarity(u"赵敏", u"韦一笑")
        print u"赵敏和韦一笑的相似度为: %g" % y1
        print "-------------------------------\n"

        # 计算某个词的相关词列表
        y2 = model_1.most_similar(u"张三丰", topn=20)  # 20个最相关的
        print(u"和张三丰最相关的词有:\n")
        for item in y2:
            print "%s: %g" % (item[0], item[1])
        print("-------------------------------\n")
    except Exception, e:
            print "Exception", e
    print 'word2vec_test end.'

if __name__ == "__main__":
    word2vec_test()
