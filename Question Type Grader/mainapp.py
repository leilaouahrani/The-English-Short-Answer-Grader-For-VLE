# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 19:28:48 2020

@author: Salah Abdellaoui For the C00L07UN100120180002 Project
"""

import io
import numpy as np
import codecs as c
import math as m
import sys
import linecache as cc
import nltk
import csv
import argparse
from nltk import word_tokenize,sent_tokenize
from nltk.stem.isri import ISRIStemmer

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
import glob
import time
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from flask import Flask,request
app = Flask(__name__)

def Norm(s1 , s2):
    cachedStopWords = stopwords.words("english")

    new_str = re.sub("[^a-zA-Z\n]", " ", s1)
    new_str2 = re.sub("[^a-zA-Z\n]", " ", s2)

    new_str = re.sub(' +', ' ', new_str).strip()
    new_str2 = re.sub(' +', ' ', new_str2).strip()

    new_str = new_str.lower()
    new_str2 = new_str2.lower()

    words = new_str.split()
    new_str = ' '.join([word for word in words if word not in cachedStopWords])

    words = new_str2.split()
    new_str2 = ' '.join([word for word in words if word not in cachedStopWords])

    str = ""
    words = new_str.split()
    for w in words:
        str = str + stemmer.stem(w) + ' '

    str2 = ""
    words = new_str2.split()
    for w in words:
        str2 = str2 + stemmer.stem(w) + ' '

    return str,str2

def SpellChecker(String):
    from spellchecker import SpellChecker
    spell = SpellChecker()
    String = String.split()
    line = ""

    for w in String:
        line = line + spell.correction(w) + ' '
    return line

def dice(x1, x2):

    if not len(x1) or not len(x2): return 0.0
    if len(x1) == 1:  x1=x2+u'.'
    if len(x2) == 1:  x2=x2+u'.'

    a_bigram_list=[]
    for i in range(len(x1)-1):
      a_bigram_list.append(x1[i:i+2])
      b_bigram_list=[]
    for i in range(len(x2)-1):
      b_bigram_list.append(x2[i:i+2])

    a_bigrams = set(a_bigram_list)
    b_bigrams = set(b_bigram_list)
    overlap = len(a_bigrams & b_bigrams)

    dice_coeff = overlap * 2.0/(len(a_bigrams) + len(b_bigrams))

    return dice_coeff

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = m.sqrt(sum([val**2 for val in vector1])) * m.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude

def similarity(NWORDS,s1, s2):
    p1 = s1.split()
    p2 = s2.split()
    #*******************************************************************************************
    #  Vector Contexts for each word in model answer and student answer  s1 et s2 In  v1 et v2
    v1, v2 = [0.0 for i in range(len(p1))], [0.0 for i in range(len(p2))]
    for i in range(len(p1)):
        if p1[i] in NWORDS:
            #print("word: ",p1[i])
            x = NWORDS.index(p1[i])
            # v1[i]=Norm[x]
            v1[i] = cc.getline("/home/englishanswer1/mysite/pythonanywhere/SemanticSpace.txt",x+1)
            v1[i]=v1[i].split()
            # v1[i]=list(map(float,v1[i]))
            # print("Vector :",v1[i])
            if p1[i] in NWORDS:
                y= NWORDS.index(p1[i])
                id=float(cc.getline("/home/englishanswer1/mysite/pythonanywhere/TF_MinMax.txt",y+1))
            else:
                id=1
            v1[i] = [float(j) * id for j in v1[i]]
            #print("vecteur after :",v1[i])
        else:
            print("mot: ",p1[i])
            v1[i] = [0.0 for ii in range(len(NWORDS))]
            #print("Vector :",v1[i])

    for i in range(len(p2)):
        if p2[i] in NWORDS:
            x = NWORDS.index(p2[i])
            v2[i] = cc.getline("/home/englishanswer1/mysite/pythonanywhere/SemanticSpace.txt",x+1)
            v2[i]=v2[i].split()
            if p2[i]in NWORDS:
                y = NWORDS.index(p2[i])
                id = float(cc.getline("/home/englishanswer1/mysite/pythonanywhere/TF_MinMax.txt",y+1))
            else:
                id=1
            v2[i] = [float(j) * id for j in v2[i]]
        else:
            print("mot non trouve: ",p2[i])
            v2[i] = [0.0 for ii in range(len(NWORDS))]
            #print("Vector :",v2[i])

    #***************************************************************************
    #  Similarity Calculation
    W1 = [0 for i in range(len(NWORDS))]
    for i in range(len(NWORDS)):
        for j in range(len(v1)):
            W1[i] += v1[j][i]

    W2 = [0 for i in range(len(NWORDS))]
    for i in range(len(NWORDS)):
        for j in range(len(v2)):
            W2[i] += v2[j][i]
    return cosine_similarity(W1,W2)


@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
            x1 = request.args.get('donnee')
            x2= request.args.get('data')


    with c.open("/home/englishanswer1/mysite/pythonanywhere/Words.txt","r","utf-8")as f:
            stocks = f.read()

    stocks = stocks.split()
    NWORDS = stocks
    x1 = SpellChecker(x1)
    x2 = SpellChecker(x2)
    x1,x2 = Norm(x1,x2)

    sim1=similarity(NWORDS,x1,x2)
    sim2=dice(x1,x2)
    sim3=(sim1*0.8+sim2*0.2)
    sim3=round(sim3,2)
    return str(sim3)





if __name__ == '__main__':
    app.run(debug=True,threaded=True)
