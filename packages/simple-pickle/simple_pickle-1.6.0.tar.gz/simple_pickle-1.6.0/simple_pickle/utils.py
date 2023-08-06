# -*- coding: utf-8 -*-
# @Time    : 18-9-28 下午1:07
# @Author  : duyongan
# @FileName: utils.py
# @Software: PyCharm
import pickle
from smart_open import open
import traceback


def read_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def write_pickle(data, filename):
    with open(filename, 'wb') as f:
        return pickle.dump(data, f, protocol=5)


def read_data(filename):
    with open(filename, encoding='utf-8') as f:
        return f.readlines()


def write_data(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data)
        return True
    except:
        traceback.print_exc()


def append_data(data, filename):
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(data)
        return True
    except:
        traceback.print_exc()


def write_datalist(datalist, filename):
    try:
        assert type(datalist) == list
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines([line + '\n' for line in datalist])
        return True
    except:
        return traceback.print_exc()


def append_datalist(datalist, filename):
    try:
        assert type(datalist) == list
        with open(filename, 'a', encoding='utf-8') as f:
            f.writelines([line + '\n' for line in datalist])
        return True
    except:
        return traceback.print_exc()
