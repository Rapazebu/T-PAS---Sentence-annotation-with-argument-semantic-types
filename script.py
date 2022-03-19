# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 10:09:44 2022

@author: marta

This script should be used to extract data from the TPAS database having a 




"""

import json
from codecs import * 
#%% 
f = open('C:/Users/marta/Dati/Task/INFORMATION type/CONCEPTS/annot_download_examples_.json')
r = json.load(f)

#data is a list containing [verb, patternNum, sentence]

data = r["data"]
#%%
#parsa un file [n, verbo, pattern] e ritorna una lista verb, pattern
def GetType(verb, patternID):
    for el in TPASdata:
        if el["query"] == verb: 
            
            Labels = el["labels"]   #è una lista
            for diz in Labels: 
                if diz["label"] == patternID:
                    Data = diz["data"]
                    Slots = Data["slots"]
                    
                    for el in Slots:
                        if el["slot"] == "object":
                            return el["semtype"]
                        
                        
                        
 #%%                       
#this parses the json GDEX file 
f = open('C:/Users/marta/Dati/Task/PHYSENT type/ARTIFACTS/examples.json', "r", "utf-8")
r = json.load(f)
Ls = []
for key in r: 
    verbo = key
    for subkey in r[key]:
        try:
            ID = subkey
            listasent = r[key][subkey]
            for x in listasent:     
                sent = (verbo, ID, x)
                Ls.append(sent)
        except: 
            pass



#%%


def ParsePattern(filename):
    fh = open(filename, "r", "latin-1")
    testo = fh.read().split("\n")
    Ls = []
    for x in testo:
        rigasplit = x.replace("\r", "").split("\t")
        if len(rigasplit) == 3:
            verbo = rigasplit[1]
            ID = rigasplit[2]
            couple = (verbo, ID)
            if couple not in Ls:
                Ls.append(couple) 
    return Ls

#returns the ST of a [verb, pattern] couple


#returns a list verb, st, pattern, sentence 

def crossed(data, patterns):
    Ls = []
    for x in data:
        for y in patterns: 
            if x[0] == y[0] and x[1] == y[1]:
                verb = x[0]
                pattern = x[1]
                st = GetType(verb, pattern)
                sentence = x[2]
                quadr = [verb, pattern, st, sentence]
                Ls.append(quadr)
    return Ls
    



#%%

Patterns = ParsePattern("C:/Users/marta/Dati/Task/PHYSENT type/ARTIFACTS/New Microsoft Excel Worksheet.txt")
sentences = crossed(Ls, Patterns)


#%%
def removeAlt(Ls):
    alt = []
    for x in Ls:
        if len
        for ST in x[2]:
            if ST != "Concept" and ST != "Information":
                alt.append(x)
    noalt = []
    for x in Ls:
        if x not in alt:
            noalt.append(x)
    return noalt

SentNoAlt = removeAlt(sentences)


#%%
 
fh = open("Artifacts.txt", "w", "utf-8")
for x in sentences:
    a = x[0]
    b = x[1]
    c = str(x[2]).replace("['", "").replace("']", "")
    d = x[3]
    
    fh.write(a + "\t" + b + "\t" + c + "\t" + d + "\n")
