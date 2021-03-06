#-*-coding:utf-8
'''
检查图片路径下的图片少了哪一张, 拿到缺少的图片id去数据库取相应的书名
然后去起点那里获取图片的链接.
用法: python qidian.py > nonpict_book.txt
接着运行Ruby下载脚本
'''
import os
import MySQLdb
import urllib
import urllib2
import json


# TODO:只能下载到最后有图片的书
def get_nopict_bid(path="/var/www/img/covers"):
    picts = os.listdir(path)
    temppicts = [int(v[:-4]) for v in picts if v != "default.jpg"]
    temppicts.sort()
    fixed = 1
    nonpict_books = []
    for curindex, v in enumerate(temppicts):
        if curindex + 1 == len(temppicts):
            break
        curfix = temppicts[curindex + 1] - temppicts[curindex]
        if curfix > fixed:
            cur_val = v
            for num in range(1, curfix):
                nonpict_books.append(cur_val + 1)
                cur_val += 1
    return nonpict_books


def mysqlconn():
    try:
        conn = MySQLdb.connect(
            host='localhost', user='root', passwd='xiaoshuoroot', db='xiaoshuo',
            port=3306, charset="utf8")
        cur = conn.cursor()
        return cur
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def getqidianID(bname):
    referer = r"http://sosu.qidian.com/searchresult.aspx?keyword=%s" % urllib.quote(
        bname)
    url = r" http://sosu.qidian.com/ajax/search.ashx?method=Search&keyword=%s" % urllib.quote(
        bname)
    req = urllib2.Request(url)
    req.add_header('Referer', referer)
    r = urllib2.urlopen(req)
    response = json.loads(r.read())
    if response['Flag']:
        return response['Data']['search_response']['books'][0]['coverurl']


def main():
    cur = mysqlconn()
    nonpb = get_nopict_bid()
    for bid in nonpb:
        cur.execute('select title from book where id=%d' % bid)
        result = cur.fetchone()
        title = result[0].encode("utf-8")
        print bid, "\t", title, "\t", getqidianID(title)
    print "#count:%d" % len(nonpb)

if __name__ == "__main__":
    try:
        main()
    except:
        pass
    #getqidianID("武动乾坤")
