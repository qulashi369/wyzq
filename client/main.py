# coding: utf8

import re
import time
import json
from urlparse import urljoin

from lxml import etree
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError

from config import limit, crawler_name, yiwanshu, interval, timeout


def get_tasks():
    url = '%s/api/update/tasks?limit=%d' % (yiwanshu, limit)
    resp = requests.get(url)
    return resp.json().get('tasks')


def is_same_chapter(chapter, latest_chapter):
    # FIXME 这里有问题
    chars = ur'[!,.()!?，。『』「」[]【】‘’“”"\'T]'
    chapter = re.sub(chars, '', chapter)
    latest_chapter = re.sub(chars, '', latest_chapter)
    try:
        c_num, chapter = chapter.split(' ', 1)
        l_num, latest_chapter = latest_chapter.split(' ', 1)
        if (c_num == l_num) or (chapter[-7:] == latest_chapter[-7:]):
            return True
    except (IndexError, ValueError):
        pass
    if chapter[-7:] == latest_chapter[-7:]:
        return True
    return False


def get_new_chapters(url, bid, chapters, latest_chapter, crawler):
    new_chapters = []
    for title, url in chapters:
        if is_same_chapter(title, latest_chapter):
            break
        else:
            new_chapters.insert(0, (title, url))
    if (len(new_chapters) == len(chapters)) and len(new_chapters) != 0:
        print ('Error: URL %s seems can not match book %s chapter %s' %
              (url, bid, latest_chapter))
        send_error(bid, crawler, latest_chapter)
        return []
    return new_chapters


def update(bid, content, title, crawler, type):
    url = '%s/api/update/%s' % (yiwanshu, bid)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = dict(
        crawler=crawler,
        chapter={
            'type': type,
            'title': title,
            'content': content
        }
    )
    data = json.dumps(data)
    resp = requests.post(url, data, headers=headers, timeout=timeout)
    assert resp.status_code == 200, 'HTTP ERROR!!'


def send_error(bid, crawler, latest_chapter):
    url = '%s/api/update/error/%s' % (yiwanshu, bid)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = dict(
        crawler=crawler,
        latest_chapter=latest_chapter,
    )
    data = json.dumps(data)
    resp = requests.post(url, data, headers=headers)
    assert resp.status_code == 200, 'HTTP ERROR!!'


def get_all_chapters(url, source_site):
    chapters = []
    resp = requests.get(url, timeout=timeout)
    content = resp.content
    tree = etree.HTML(content)
    if source_site == 'fftxt.net':
        elements = tree.xpath("//ul[@id='chapterlist']/li/a")
    elif source_site == 'hao123.se':
        elements = tree.xpath("//dl[@id='chapterlist']/dd/a")

    for ele in elements:
        if source_site == 'fftxt.net':
            chapter_url = urljoin(url, ele.attrib.get('href'))
        elif source_site == 'hao123.se':
            chapter_url = ele.attrib.get('href')
        title = ele.text
        if title:
            chapters.insert(0, (title, chapter_url))
    return chapters


def get_content(url, source_site):
    resp = requests.get(url, timeout=timeout)
    html = resp.content
    tree = etree.HTML(html)
    if source_site == 'fftxt.net':
        elements = tree.xpath("//div[@class='novel_content']/text()")
        content = '<br><br>'.join(elements[1:])
    elif source_site == 'hao123.se':
        elements = tree.xpath("//div[@id='content']/text()")
        content = '<br><br>'.join(elements)
    return content


def crawl_chapters():
    print 'get update tasks from %s...' % yiwanshu
    for book in get_tasks():
        bid = book.get('bid')
        source_site = book.get('source_site')
        latest_chapter = book.get('latest_chapter')
        url = book.get('source_url')
        print 'update book %s, try to get new chapters from %s' % (bid, url)
        try:
            chapters = get_all_chapters(url, source_site)
        except requests(Timeout, ConnectionError, HTTPError):
            print 'get chapters timeout. %s' % url
            continue
        new_chapters = get_new_chapters(url, bid, chapters, latest_chapter,
                                        crawler_name)
        if len(new_chapters) == 0:
            print 'no new chapters\n'
            continue
        print '%d new chapters.' % len(new_chapters)
        for title, url in new_chapters:
            try:
                content = get_content(url, source_site)
                update(bid, content, title, crawler_name, 'text')
                print 'update book %s, chapter %s' % (bid, title)
            except (Timeout, ConnectionError, HTTPError):
                print 'get content timeout. %s' % url
                continue
        print 'book %s update finish.\n\n' % bid


if __name__ == '__main__':
    while 1:
        try:
            crawl_chapters()
        except Exception as e:
            print 'Error!!!'
            print e
        print 'I\'m sleeping...\n'
        time.sleep(interval)
