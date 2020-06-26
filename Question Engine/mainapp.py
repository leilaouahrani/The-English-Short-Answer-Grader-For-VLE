# -*- coding: utf-8 -*-
"""
# Question Engine Short Answer Grader deployed on Pythonanywhere via Flask (main)
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

from flask import Flask,request
app = Flask(__name__)

def isri(x1):
    
    alpha = ['A','a','B','b','C','c','D','d','E','e','F','f','G','g','H','h','I','i','J','j','K','k',
             'L','l','M','m','N','n','O','o','P','p','Q','q','R','r','S','s','T','t','U','u','V','v',
             'W','w','X','x','Y','y','Z','z','.', ',', '¡','،', ':', '"', "'", '÷', '×', 'º', '>', '<', '|', '//','?','؟', '¿', '!', '@', '#', '$',
          '%', '^', '&', '*', ')', '(', '_', '-', '+', '=', ';', '~', 'ø', '/', '§', '£', '{', '[',
          '`', ']', '}', 'ّ', 'َ', 'ً', 'ُ', 'ٌ', 'ٍ', 'ْ', 'ِ','1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'ّ', 'َ', 'ً', 'ُ', 'ٌ', 'ٍ', 'ْ', 'ِ']
    '''
    alpha2 = ['.', ',', '¡','،', ':', '"', "'", '÷', '×', 'º', '>', '<', '|', '//','?','؟', '¿', '!', '@', '#', '$',
          '%', '^', '&', '*', ')', '(', '_', '-', '+', '=', ';', '~', 'ø', '/', '§', '£', '{', '[',
          '`', ']', '}', 'ّ', 'َ', 'ً', 'ُ', 'ٌ', 'ٍ', 'ْ', 'ِ']

    alpha3 = [ '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'ّ', 'َ', 'ً', 'ُ', 'ٌ', 'ٍ', 'ْ', 'ِ']
    '''

    with c.open("/home/shortanswerplugin/mysite/pythonanywhere/beta.txt", "r", "utf-8")as f:
     beta = f.read()
    beta=beta.split()
    with c.open("/home/shortanswerplugin/mysite/pythonanywhere/stopwords.txt", "r", "utf-8")as f:
        stop = f.read()
    stop=stop.split()

    # ***************************************************************************************************
    # Removal of non-Arabic characters  and Normalization  

    for x in range(len(alpha)):
        if alpha[x] in x1:
            x1 = x1.replace(alpha[x],"")
    # normalization

    for x in range(len(beta)):
        if beta[x] in x1:
            x1 = x1.replace(beta[x],"ا")

    x1 = x1.replace("ة","ه")
    x1 = x1.replace("ى","ي")
    x1 = x1.replace("يء","ئ")
    x1= x1.replace("ءى","ئ")

    x1 = x1.split();
    for x in stop:
        while x  in x1:
                del x1[x1.index(x)]
    x1 = ' '.join(x1)

    st = ISRIStemmer()
    with c.open("/home/shortanswerplugin/mysite/pythonanywhere/stopwords.txt", "r+", "utf-8") as file:
        stop = file.read()
    stop=stop.split("\n")


    myList = []
    for a in x1.split():

        myList.append(st.stem(a))

    for x in stop:
            while x in myList:
                del myList[myList.index(x)]
    phrase = ' '.join(myList)
    return phrase

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
    # Recovery of the context vectors of each word of the answers s1 and s2 in v1 and v2
    v1, v2 = [0.0 for i in range(len(p1))], [0.0 for i in range(len(p2))]
    for i in range(len(p1)):
        if p1[i] in NWORDS:
            #print("mot: ",p1[i])
            x = NWORDS.index(p1[i])
            # v1[i]=Norm[x]
            v1[i] = cc.getline("/home/shortanswerplugin/mysite/pythonanywhere/SemanticSpaceNew.txt",x+1)
            v1[i]=v1[i].split()
            #v1[i]=list(map(float,v1[i]))
           # print("Vecteur :",v1[i])
            if p1[i] in NWORDS:
                y= NWORDS.index(p1[i])
                id=float(cc.getline("/home/shortanswerplugin/mysite/pythonanywhere/TF_MinMax_cyber.txt",y+1))
            else:
                id=1
            v1[i] = [float(j) * id for j in v1[i]]
            #print("vecteur after :",v1[i])
        else:
            #print("mot: ",p1[i])
            v1[i] = [0.0 for ii in range(len(NWORDS))]
            #print("Vecteur :",v1[i])

    for i in range(len(p2)):
        if p2[i] in NWORDS:
            x = NWORDS.index(p2[i])
            v2[i] = cc.getline("/home/shortanswerplugin/mysite/pythonanywhere/SemanticSpaceNew.txt",x+1)
            v2[i]=v2[i].split()
            if p2[i]in NWORDS:
                y = NWORDS.index(p2[i])
                id = float(cc.getline("/home/shortanswerplugin/mysite/pythonanywhere/TF_MinMax_cyber.txt",y+1))
            else:
                id=1
            v2[i] = [float(j) * id for j in v2[i]]
        else:
            v2[i] = [0.0 for ii in range(len(NWORDS))]

    #***************************************************************************
    # Similarity calculation
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

    with c.open("/home/shortanswerplugin/mysite/pythonanywhere/WWords.txt","r","utf-8")as f:
            stocks = f.read()

    stocks = stocks.split()
    NWORDS = stocks
    x1=isri(x1)
    x2=isri(x2)

    sim=similarity(NWORDS,x1,x2)
    sim2=dice(x1,x2)
    sim3=(sim+sim2)/2
    sim3=round(sim3,2)
    return str(sim3)





if __name__ == '__main__':
    app.run(debug=True,threaded=True)
