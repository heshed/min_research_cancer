#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import argparse

__author__ = 'heshed'


def merge(input_dir, output_path):
    print '--- [뉴스 통짜 파일 제작 시작]'
    of = file(output_path, 'w')

    for item in os.listdir(input_dir):
        sub_dir = os.path.join(input_dir, item)
        if os.path.isdir(sub_dir):
            print '    ', sub_dir
            for news in os.listdir(sub_dir):
                file_path = os.path.join(sub_dir, news)
                if os.path.isfile(file_path):
                    title = '언론사: ' + file_path
                    content = read_file(file_path)
                    add_to_file(of, title, content)
    of.close()

    print '--- [뉴스 통짜 파일 제작 끝]'
    print '---', output_path

    return


def add_to_file(fp, title, content):
    fp.write('{}\n{}\n\n'.format(title, content))


def read_file(path):
    rf = file(path)
    data = rf.read()
    rf.close()
    return data


if __name__ == '__main__':
    default_input_path = '결과-상세'
    default_output_path = '결과-통짜/all-in-one.txt'

    parser = argparse.ArgumentParser(description="상세 뉴스 데이터를 머지합니다")
    parser.add_argument("-i", default=default_input_path, help="input directory: ex) " + default_input_path)
    parser.add_argument("-o", default=default_output_path, help="output path: ex) " + default_output_path)
    args = parser.parse_args()

    merge(args.i, args.o)
