from django.shortcuts import render
from django.shortcuts import HttpResponse
import jieba
import math
import difflib
import xlrd
from .models import Comment
import os
import sys
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.metrics import BigramAssocMeasures

name_list = []
res1 = {}
res2 = {}
res3 = {}
res4 = {}
res = {}
fazhi = 0.78

def get_words(filename):
    stop = [line.strip() for line in open('./stop2.txt', 'r', encoding='gbk').readlines()]  # 停用词
    f = open(filename, 'r', encoding='gbk')
    line = f.readline()
    global x
    x = 0
    words = {}
    while line:
        s = line.split()
        fenci = jieba.cut(s[0], cut_all=False)  # 精准模式
        word_list = list(set(fenci) - set(stop))
        for word in word_list:
            x += 1
        for word in word_list:
            if word not in words:
                words[word] = 1
            else:
                words[word] += 1
        line = f.readline()
    for word in words:
        words[word] = round(words[word] / x * 100, 4)
    return words


def qingganfenxi(file_name):
    stop = [line.strip() for line in open('./stop2.txt', 'r', encoding='gbk').readlines()]  # 停用词
    name_list = []
    posWords = {}
    negWords = {}
    pos = {}
    neg = {}
    pos_words = []
    neg_words = []
    pos_words = [line.strip() for line in open('./zhengmian.txt', 'r', encoding='gbk').readlines()]
    neg_words = [line.strip() for line in open('./fumian.txt', 'r', encoding='gbk').readlines()]
    posWords = get_words('./good.txt')  # 可统计积极文本中的词频和消极文本中的词频
    negWords = get_words('./bad.txt')
    for word in negWords:
        negWords[word] = -negWords[word]  # 将消极词的词频变为负号
    for k in list(posWords.keys()):  # 区分消极词与积极词中同时存在的词
        if k not in pos_words:
            del (posWords[k])
    for k in list(negWords.keys()):  # 区分消极词与积极词中同时存在的词
        if k not in neg_words:
            del (negWords[k])
    for i in range(1, 51):  # 取出情感强度最强的前50个积极词，并赋权值
        for key, value in posWords.items():
            if value == max(posWords.values()):
                max_key = key
        pos[max_key] = 4
        del (posWords[max_key])
    for i in range(1, 51):  # 取出情感强度最强的前50个消极词，并赋权值
        for key, value in negWords.items():
            if value == min(negWords.values()):
                min_key = key
        neg[min_key] = -4
        del (negWords[min_key])
    name_pl = {}  # 建立用户-评论字典
    print('情感分析打开文件: ' + file_name)
    data = xlrd.open_workbook(file_name)  # 打开xls文件
    table = data.sheets()[0]  # 打开第一张表
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):  # 循环逐行打印
        if i == 0:  # 跳过第一行
            continue
        name = str(table.row_values(i)[:1])  # 取出第一列的名字
        pl = str(table.row_values(i)[3:4])  # 取出第二列的评论
        s = pl.split('\t')
        fenci1 = jieba.cut(s[0], cut_all=True)  # 给评论分词
        word_list = set(fenci1) - set(stop)
        name_pl.setdefault(name, []).append(word_list)  # 将每个用户的评论分词集合在一起
    n1 = 0
    y1 = 0
    for key, value in name_pl.items():
        for items in value:
            n1 = n1 + 1
            qg = 0
            j = 1
            for item in items:
                if item in list(pos.keys()):
                    qg += pos[item]
                    j = j + 1
                if item in list(neg.keys()):
                    qg += neg[item]
                    j = j + 1
            if qg >= 0:  # 将情感极性强度缩小到[0，1]范围
                qg = 1 - (1 / math.exp(qg / j))
            else:
                qg = 1 - 1 / (math.exp(((-1) * qg) / j))
            if (key not in res4):
                res4[key] = qg
            else:
                if res4[key] < qg:
                    res4[key] = qg

    # print(res4)
    # print("----------------------------------------------------------------")


def name_date(file_name):
    stop = [line.strip() for line in open('./stop2.txt', 'r', encoding='gbk').readlines()]  # 停用词
    name_date = {}  # 建立用户-评论日期字典
    data = xlrd.open_workbook(file_name)  # 打开xls文件
    table = data.sheets()[0]  # 打开第一张表
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):  # 循环逐行打印
        if i == 0:  # 跳过第一行
            continue
        name = str(table.row_values(i)[:1])  # 取出第一列的名字
        if name not in name_list:
            name_list.append(name)
        date = str(table.row_values(i)[1:2])  # 取出第二列的评论日期
        date = date[10:]
        name_date.setdefault(name, []).append(date)  # 将每个用户的评论日期集合在一起
    for key, value in name_date.items():  # 循环用户
        r = {}
        m = 0
        l = 0
        for date in value:  # 循环评论日期
            m = m + 1
            if date not in r:
                r[date] = 1
            else:
                r[date] += 1
        n = 0
        for date in r:
            if r[date] > n:
                n = r[date]
        for date in r:
            r[date] = r[date] / m
            if r[date] >= l:
                l = r[date]
            if m == 1:
                l = 0
        if key not in res1:
            res1[key] = l
    # print(res1)
    # print("-------------------------------------------------------------------")


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


def name_pl(file_name):
    stop = [line.strip() for line in open('./stop2.txt', 'r', encoding='gbk').readlines()]  # 停用词
    name_list = []
    name_pl = {}  # 建立用户-评论字典
    data = xlrd.open_workbook(file_name)  # 打开xls文件
    table = data.sheets()[0]  # 打开第一张表
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):  # 循环逐行打印
        if i == 0:  # 跳过第一行
            continue
        name = str(table.row_values(i)[:1])  # 取出第一列的名字
        pl = str(table.row_values(i)[3:4])  # 取出第四列的评论文本
        name_pl.setdefault(name, []).append(pl)  # 将每个用户的评论集合在一起
    for key, value in name_pl.items():  # 循环用户
        i = 0
        for pl1 in value:  # 循环评论
            i = i + 1
            j = 0
            for pl2 in value:
                j = j + 1
                if (i <= j):
                    continue
                if (key not in res2) or (string_similar(pl1, pl2) > res2[key]):
                    res2[key] = string_similar(pl1, pl2)
        if i == 1:
           res2[key] = fazhi
    # print(res2)
    # print("-------------------------------------------------------------------")


def name_star(file_name):
    name_star = {}  # 建立用户-星级字典
    data = xlrd.open_workbook(file_name)  # 打开xls文件
    table = data.sheets()[0]  # 打开第一张表
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):  # 循环逐行打印
        if i == 0:  # 跳过第一行
            continue
        name = str(table.row_values(i)[:1])  # 取出第一列的名字
        star = str(table.row_values(i)[2:3])  # 取出第三列的评论星级
        star = star[2:3]
        name_star.setdefault(name, []).append(star)  # 将每个用户的评论星级集合在一起
    for key, value in name_star.items():  # 循环用户
        n = 0
        m = 0
        for star in value:  # 循环评论星级
            n = n + 1
            if (star == '4') or (star == '5'):
                m = m + 1
        if key not in res3:
            if n == 1:
                res3[key] = 0
            else:
                res3[key] = m / n
    # print(res3)  # 虚假评论者列表3
    # print("-------------------------------------------------------------------")



def false_comment_filter(file):
    qingganfenxi(file)
    name_date(file)
    name_pl(file)
    name_star(file)
    for name in name_list:
        res[name] = 0.4 * res4[name] + 0.1 * res1[name] + 0.3 * res2[name] + 0.2 * res3[name]
    # print(res)
    # for key, value in res.items():
    #    print(value)
    real = 0
    wrong = 0
    for key, value in res.items():
        if value >= fazhi:
            wrong = wrong + 1
        else:
            real = real + 1
    ans = 0
    if file == 'false.xlsx':
        # print("The number of false reviews:" + str(wrong))
        ans = wrong
    else:
        # print("The number of true reviews" + str(real))
        ans = real


# Create your views here.
def comment_analysis(request):
    file = 'true.xlsx'
    false_comment_filter(file)
    return render(request, 'pages/comment_analysis.html', {'comments': res})


def comment_show(request):
    true_comment = []
    false_comment = []
    # true
    data = xlrd.open_workbook('true.xlsx') # all sheet
    table = data.sheets()[0]  # 0th sheet
    nrows = table.nrows
    for i in range(nrows):
        temp = Comment()
        temp.username = str(table.row_values(i)[0])
        temp.date = str(table.row_values(i)[1])
        temp.score = str(table.row_values(i)[2])
        temp.comment_text = str(table.row_values(i)[3])
        temp.type = True
        true_comment.append(temp)
    # false
    data = xlrd.open_workbook('false.xlsx') # all sheet
    table = data.sheets()[0]  # 0th sheet
    nrows = table.nrows
    for i in range(nrows):
        temp = Comment()
        temp.username = str(table.row_values(i)[0])
        temp.date = str(table.row_values(i)[1])
        temp.score = str(table.row_values(i)[2])
        temp.comment_text = str(table.row_values(i)[3])
        temp.type = False
        false_comment.append(temp)
    return render(request, 'pages/comment_show.html', {'true_comments': true_comment, 'false_comments': false_comment})


def index(request) :
    return render(request, 'pages/index.html')


def new_false_comment_filter(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return render(request, 'pages/file_upload.html', {'info': 'failed'})
        destination = open(os.path.join("D:\\upload", myFile.name), 'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        # print("start")
        file = myFile.name
        qingganfenxi(file)
        name_date(file)
        name_pl(file)
        name_star(file)
        for name in name_list:
            res[name] = 0.4 * res4[name] + 0.1 * res1[name] + 0.3 * res2[name] + 0.2 * res3[name]
        # print(res)  # 最终的虚假评论者集合
        # for key, value in res.items():
        #    print(value)
        real = 0
        wrong = 0
        true_list = {}
        false_list = {}
        for key, value in res.items():
            if value >= fazhi:
                wrong = wrong + 1
                false_list[key] = value
            else:
                real = real + 1
                true_list[key] = value
        return render(request, 'pages/new_comment_analysis.html', {'file_name': file, 'true_list': true_list,
                                                                   'false_list': false_list})
