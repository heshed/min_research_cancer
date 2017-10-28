#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from fake_useragent import UserAgent
import csv
import logging
from random import randint
from time import sleep
import cPickle as pickle
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

__author__ = 'heshed'

def crawl_detail(input_path, out_directory):
    """
    경향신문/
       1-20171019-곽윤섭-01101001.20171019210903001.json
    :param input:
    :param out_directory:
    :return:
    """

    ua = UserAgent()

    headers = {
        'Pragma': 'no-cache',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'User-Agent': ua.chrome,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Cache-Control': 'no-cache',
        'Cookie': 'delquotationtxt=null; delquotationCnt=0; delNewsId=null; delCnt=0; newsDelCancelBtnCheck=news; recentKeyword=%EC%95%94; newsDelCancelBtnCheck=news; recentKeyword=%EC%95%94; _ga=GA1.3.832767489.1506507423; Bigkinds=26992848E9DE6642B753FABE577B9DE8',
        'Connection': 'Close',
    }

    url = 'https://www.bigkinds.or.kr/news/detailView.do'

    logging.info('open: %s', input_path)

    index_db = read_index()

    # 01100701.20160107233646233
    # 4987
    # 6508
    with open(input_path) as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader, start=1):
            if index <= index_db['index']:
                logging.info("skip {}".format(index))
                continue
            index_db['index'] = index
            docid = row[reader.fieldnames[0]]  # id
            media = row[reader.fieldnames[2]]  # 언론사
            directory_path = os.path.join(out_directory, media)

            r = requests.get(url, headers=headers, params={'docId': docid})
            logging.info('{}: {}'.format(index, r.url))
            if r.status_code == 200:
                media_index = get_index(media, index_db)
                logging.info('write: {}: {}/{}:'.format(index, media, media_index))
                write_detail(r.json(), directory_path, media_index, r.url)

                # write json response

                json_path = os.path.join('json_response', os.path.basename(input_path)+'.json')
                write_json(r.json(), json_path)
            else:
                logging.warn('{}: {}'.format(r.reason, r.url))

            r.close()

            '''
            import json
            result_json = json.load(open('details/sample.json'))
            write_detail(result_json, directory_path, index, '')
            '''

            write_index(index_db)

            sleep(randint(4, 6))
    return


def index_path():
    return 'index.pickle'


def read_index():
    if not os.path.exists(index_path()):
        return {'index': 1}

    with open(index_path(), 'rb') as f:
        e = pickle.load(f)
        return e


def write_index(index_db):
    with open(index_path(), 'wb') as f:
         f.write(pickle.dumps(index_db))


def get_index(key, db_name={}):
    index = db_name.get(key, 0)
    db_name[key] = index + 1
    return index + 1


def write_json(result, output_path):
    import io, json
    with io.open(output_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))
        f.write(unicode('\n'))


def write_detail(result, output_dir, index, link):
    """ json sample
    {
   "ctx":"https://www.bigkinds.or.kr:443",
   "detail":{
      "BYLINE":"곽윤섭",
      "CATEGORY_CODE":"004000000 004006000\n004000000 004007000\n004000000 004005000",
      "CATEGORY_INCIDENT":"",
      "TMS_NE_LOCATION":"서울\n르완다\n키상가니\n자이르\n류가헌\n제주",
      "CATEGORY_MAIN":"문화>미술_건축",
      "TMS_SIMILARITY":"",
      "DATE":"20171019",
      "NEWS_ID":"01101001.20171019210903001",
      "TMS_NE_ORGANIZATION":"보건복지부\n가톨릭관동대\n국제성모병원\n춘천기독병원\n류가헌\n유엔\n전주대",
      "IMAGES":"http://www.bigkinds.or.kr/resources/images/01101001/2017/10/19/01101001.20171019210903001.01.jpg",
      "CATEGORY_INCIDENT_MAIN":"",
      "TMS_NE_STREAM":"",
      "CATEGORY":"",
      "TMS_RAW_STREAM":"",
      "TMS_SENTIMENT_CLASS":"",
      "PROVIDER_LINK_PAGE":"http://www.hani.co.kr/arti/culture/culture_general/815283.html",
      "PROVIDER":"한겨레",
      "TITLE":"“‘호스피스 100일’ 촬영 하루만에 내 오만함 깨졌다”",
      "PROVIDER_CODE":"01101001",
      "CONTENT":"",
      "TMS_NE_PERSON":"성남훈"
   },
   "quotResult":[

   ]
}
    :param result:
    :param output_dir:
    :param index:
    :return:
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, str(index) + '.txt')

    detail = result['detail']
    template = '''제목: {title}
날짜: {date}
기자: {author}
링크: {link}
본문: {content}
'''.format(title=detail['TITLE'],
           date=detail['DATE'],
           author=detail['BYLINE'],
           link=link,
           content=detail['CONTENT'].encode('UTF-8'),
           )

    with open(file_path, 'w') as f:
        f.write(template)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                        filename='output.log',
                        level=logging.INFO)
    crawl_detail('source/NewsResult_20140101-20161231.csv', '결과-상세')
