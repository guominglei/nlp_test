#!/usr/local/env python
# -*- coding: utf-8 -*-
"""
    Author: GuoMingLei
    Created: 2019/3/11

    双列表实现前缀树。
    wiki:
        https://www.cnblogs.com/zhangbo2008/p/9082012.html
        https://segmentfault.com/a/1190000008877595#articleHeader7

    字符编码层级遍历。 便于编码减少移动。

    base    记录上层数组编号     记录本字下一个字的基础偏移量。 未负数情况（1、已经是结尾了。2、当前位置没有存储）
    check   记录当前是否是尾部   上一字index

    最后遍历一次。如果当前字已经是最后的了。就把当前base值变为负数。

    查找的时候 人为设置一个初始量 1 加上 base + 编码

    压缩指的是后缀压缩。要是分支上是一条线既只有一个节点。那这些节点可以组合成一个。编码更改吗？
"""


class DART(object):

    def __init__(self, data):

        # 关键字
        self.key_words = sorted(data)

        # 编码
        self.code_dict = {}
        # 基础表
        self.base_list = []
        # 验证表
        self.check_list = []
        #

    def init_code_map(self):
        """
            1、初始化编码表 层级遍历 便于编码
            2、初始化
        """
        code = 1
        total = 0
        layer = 0
        while 1:
            layer_num = 0
            for words in self.key_words:
                try:
                    word = words[layer]
                    if word not in self.code_dict:
                        self.code_dict[word] = code
                        code += 1
                    total += 1
                    layer_num += 1
                except:
                    pass
            if layer_num > 0:
                layer += 1
        #
        self.code_dict[""] = 0
        # 初始化基础表
        self.base_list = [0] * total
        self.base_list[0] = 1
        # 初始化校验表
        self.check_list = [0] * total

    def get_layer_word(self, layer=0):
        """
            获取分层数据
        """
        has_next_num = 0
        layer_words = []

        for item in self.key_words:
            if item and len(item) > layer:
                has_next_num += 1
                word = item[layer]
                if word not in layer_words:
                    layer_words.append(word)
        if has_next_num:
            layer += 1
        else:
            layer = -1
        return layer, layer_words

    def create_layer(self, layer=0, lastest_index_list=[]):
        """
            按层来初始化数据。
            所谓层就是字段数的前缀
        """
        has_next, layer_words = self.get_layer_word(layer)

        for w_index, word in layer_words:
            if layer == 0:
                before_index = 0
            else:
                before_index =lastest_index_list[w_index]
            while 1:
                base_index = self.base_list[before_index] + self.code_dict[word]
                if self.base_list[base_index] == 0:
                    # ok
                    self.base_list[base_index] == 1



