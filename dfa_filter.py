#!/usr/local/env python
# -*- coding: utf-8 -*-

"""
    Author: GuoMingLei
    Created: 2019/3/11

    DFA（有限状态自动机） 敏感词过滤
    https://blog.csdn.net/chenssy/article/details/26961957

    实现方式：
        1、就是前缀树。 以空间换时间。

        2、双数组实现方式：https://segmentfault.com/a/1190000008877595#articleHeader7

"""
import os
import cPickle


class Node(object):
    """
        数据节点
    """
    def __init__(self):
        #  多茬树
        self.children = None
        # 叶子节点 内容
        self.word = None
        # 是否是敏感词。 默认过滤。
        # 主要是用于过滤 逼， 牛逼， 这类的。 牛逼不属于敏感词。但是逼就属于敏感词。
        self.is_valid = True

    def add_word(self, word, is_valid=True):
        """
            更新字段树
        """
        node = self
        for i in range(len(word)):
            if not node.children:
                node.children = {}
                node.children[word[i]] = Node()
            elif word[i] not in node.children:
                node.children[word[i]] = Node()

            node = node.children[word[i]]

        node.word = word
        node.is_valid = is_valid


class DFAFilter(object):
    """
        DFA 算法 敏感词过滤
    """
    def __init__(self, dict_path=None):

        if dict_path:
            self.data_path = dict_path
        else:
            self.data_path = "dfa.data"
        self.root = None
        self.load_dict_data()

    def load_dict_data(self):
        """
            加载前缀数字典
        """
        if os.path.exists(self.data_path):
            self.root = cPickle.load(open(self.data_path, "r"))

    def save_dict_data(self):
        """
            保存前缀数
        """
        cPickle.dump(self.root, open(self.data_path, "w"))

    def add_word(self, word, valid):
        """
            添加敏感词
        """
        if not self.root:
            self.root = Node()

        self.root.add_word(word, is_valid=valid)

    def is_sensitive(self, content):
        """
            检测是否为敏感词
        """
        is_valid = False
        valid_words = []

        content_length = len(content)
        next_index = 0
        for index, word in enumerate(content):
            parent = self.root
            if index < next_index:
                continue

            next_index = index
            while next_index < content_length and parent.children != None and content[next_index] in parent.children:
                parent = parent.children[content[next_index]]
                next_index += 1
            if parent.word == content[index:next_index] and parent.is_valid:
                valid_words.append(parent.word)

        if valid_words:
            is_valid = True

        return is_valid, valid_words


def test():

    words = [
        #[u"牛逼", False],
        [u"逼", True],
        [u"牛逼", True],
        [u"习大大", True],
        [u"习近平", True]
    ]

    dfa = DFAFilter()

    for w, valid in words:
        dfa.add_word(w, valid)

    content = u"习近平通知很牛逼啊女人习大大！"

    is_ok, valid_words = dfa.is_sensitive(content)
    print is_ok, valid_words
    for vw in valid_words:
        print vw

    #dfa.save_dict_data()


if __name__ == "__main__":

    test()