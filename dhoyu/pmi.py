#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
from collections import defaultdict

class PMI(object):
    def __init__(self):
        self.total = 0
        self.letter_freqs = {}
        self.pairs = {}
        self.total_pairs = 0

    def add_word(self, word):

        word = word.lower().strip()

        # add the frequencies
        for letter in word:
            self.total += 1
            if letter in self.letter_freqs:
                self.letter_freqs[letter] += 1
            else:
                self.letter_freqs[letter] = 1

        # no pairs
        if len(word) < 2:
            return

        # add the pairs
        for i in range(0, len(word)-1):
            pair = word[i:i+2]
            self.total_pairs += 1
            if pair in self.pairs:
                self.pairs[pair] += 1
            else:
                self.pairs[pair] = 1

    def pmi(self, x, y):
        '''
        get pmi(x;y)
        '''

        # normalize
        x = x.lower()
        y = y.lower()

        p_x = self.letter_freqs.get(x, 0) / self.total
        p_y = self.letter_freqs.get(y, 0) / self.total

        p_xy = self.pairs.get(x+y, 0) / self.total_pairs

        if p_x * p_y == 0 or p_xy == 0:
            return -5

        pmi = math.log(p_xy / (p_x * p_y))

        return pmi

    def get_all_pmis(self):
        pmis = {}

        for pair in self.pairs:
            pmi = self.pmi(pair[0], pair[1])
            pmis[pair] = '{:.3f}'.format(pmi)

        return pmis


PMIs = {
    # 'en': PMI(),
}

def init_pmi(language, word_file_obj):
    pmi_machine = PMI()

    for word in word_file_obj:
        pmi_machine.add_word(word)

    PMIs[language] = pmi_machine


def segment(word, language='en', threshold=0):
    pmi_machine = PMIs[language]

    probs = []
    for i in range(0, len(word)-1):
        p = pmi_machine.pmi(word[i], word[i+1])
        probs.append(p)

    pieces = []
    last = 0
    for i, p in enumerate(probs):
        if p < threshold:
            pieces.append(word[last:i+1])
            last = i+1
    pieces.append(word[last:])

    return pieces
