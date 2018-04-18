#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 08:10:35 2018

@author: richard
"""

import os
import re


def load_dict(dirname):
    symbols = dict()
    for f in os.listdir(dirname):
        if f.split('.')[1] != 'tsv':
            continue
        sym = f.split('.')[0]
        doc = load_doc(os.path.abspath(dirname) + '/' + f)
        pairs = to_pairs(doc)
        symbols[sym] = pairs
    return symbols

# load doc into memory
def load_doc(filename):
    # open the file as read only
    print('[%s]' % filename)
    file = open(filename, mode='rt', encoding='utf-8')
    #file = open(filename, mode='rt')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text

# split a loaded document into sentences
def to_pairs(doc):
    lines = doc.strip().split('\n')
    pairs = [line.split('\t') for line in  lines]
    return pairs

def generate(sentences):
    sentence_list = list()
    for template in sentences:
        temp_eng = template[0]
        temp_tag = template[1]
        p = re.compile('\$[A-Za-z]+')
        tokens = p.findall(temp_eng)
        if len(tokens) > 0:
            p = re.compile('\\' + tokens[0])
            key = tokens[0][1:]
            for val in symbols[key]:
                eng = p.sub(val[0], temp_eng)
                tag = p.sub(val[1], temp_tag)
                #print('[%s] ==> [%s]' % (eng, tag))
                sentence_list.append([eng,tag])
        else:
            sentence_list.append(template)
    if len(sentences) < len(sentence_list):
        return generate(sentence_list)
    else:
        return sentence_list
    
def capitalize(sentences):
    sentence_list = list()
    for sentence_pair in sentences:
        english = sentence_pair[0].capitalize()
        tagalog = sentence_pair[1].capitalize()
        sentence_list.append([english,tagalog])
        
    return sentence_list
    

# save a list of clean sentences to file
def save_clean_data(sentences, filename):
    with open(filename,"w") as f:
        count = 0
        for sentence in sentences:
            count = count + 1
            line = "%s\t%s\n" % (sentence[0], sentence[1])
            f.write(line)
        print('Saved: %s' % filename)


# load dataset
symbols = load_dict('symbols')
sentences = to_pairs(load_doc('template.tsv'))
sentences = generate(sentences)
sentences = capitalize(sentences)

# save clean pairs to file
save_clean_data(sentences, 'english-tagalog-augmented.tsv')
