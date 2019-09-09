#!/usr/local/env python
# -*- coding: utf-8 -*-

"""
    Author: GuoMingLei
    Created: 2019/3/11

    AC(多模匹配算法) filter

    算法的核心在于找到=失败指针。
    假设当前节点为parent 其孩子节点为child 。求child的Fail指针。
    1、首先找到parent的 fail指针指向的节点T 。
    2、如果T的子节点中有和child节点相同字符 则这个子节点就是child的Fail 节点。
    3、如果T的子节点中没有和child相同的字符。则找T节点的Fail节点。直至找的root。还没有则最后child节点的Fail 为root

"""


class Node(object):

    def __init__(self):
        self.link = {}
        self.fail = None
        self.isWord = False
        self.word = ""


class AC(object):

    def __init__(self):
        self.root = Node()

    def addWord(self, word):
        """
            添加新字
        """
        parent = self.root
        for char in word:
            if char not in parent.link:
                parent.link[char] = Node()
            parent = parent.link[char]
        parent.isWord = True
        parent.word = word

    def make_fail(self):
        """
            组织fail 指针
        """
        queue = []

        queue.append(self.root)
        while len(queue) != 0:
            parent = queue.pop(0)
            parent_fail = None
            for key, value in parent.link.items():
                if parent == self.root:
                    parent.link[key].fail = self.root
                else:
                    parent_fail = parent.fail
                    while parent_fail is not None:
                        if key in parent_fail.link:
                            parent.link[key].fail = parent_fail.fail
                            break
                        parent_fail = parent_fail.fail
                    if parent_fail is None:
                        parent.link[key].fail = self.root
                queue.append(parent.link[key])

    def search(self, content):

        parent = self.root

        result = []

        position = 0

        while position < len(content):

            word = content[position]

            while word in parent.link == False and parent != self.root:
                parent = parent.fail

            if word in parent.link:
                parent = parent.link[word]
            else:
                parent = self.root

            if parent.isWord:
                next_position = position + 1
                if next_position < len(content):
                    next_word = content[next_position]
                    if next_word not in parent.link:
                        #  最大匹配 解决 法律， 法律人 同时出现的情况
                        result.append(parent.word)
                        parent = self.root
                else:
                    result.append(parent.word)
                    parent = self.root

            position += 1

        return result


def test():
    filter = AC()
    filter.addWord(u"法律人")
    filter.addWord(u"法律")
    text1 = u"现在的法律是保护老百姓法律人吗!习大大"
    word_list = filter.search(text1)
    for word in word_list:
        print word


if __name__ == "__main__":
    test()
