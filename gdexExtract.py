# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 17:19:33 2021

@author: marta
"""
    
from codecs import *  
import spacy-udpipe


def ParsePattern(filename):
    """questa funzione legge un file in excel come il file Patterns.csv 
    e ritorna una lista di tuple (verbo, n° pattern)"""
    
    fh = open(filename, "r", "utf-8")
    testo = fh.read().split("\n")
    testo = testo[1:]
    Ls = []               #contains list of tuples [()] for each raw 
    for riga in testo:
        rigasplit = riga.replace("\r", "").split("|")
        if len(rigasplit) == 3:
            t1 = rigasplit[1]
            t2 = rigasplit[2]
            tupla = (t1, t2)
            if tupla != ('',''):
                Ls.append(tupla)
    return Ls







#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%555

""""incrocia il file dei pattern e ritorna una lista di frasi per i pattern in ds"""
def ReturnPositive(Ls, Ds):
    
    Positive = []    
    
    for x in Ls:
        for y in Ds:
            if x[0] == y[0] and x[1] == y[1]:
                Positive.append(x[2])
                
    return Positive


#%%

""""qui alcune varianti: rispettivamente
    come ritornare una lista di coppie  (verbo, frase) solo per i verbi di Ds
    o una lista di triple (verbo, pattern, frase) solo per i verbi di Ds
    o un dizionario verbo:frase
    """

def ReturnPositiveCoup(Ls, Ds):
    D = {}
    
    Lista = []
    
    for x in Ls:        #per ogni tupla del file gdex
        
        for y in Ds:
            
            if x[0] == y[0] and x[1] == y[1]:
                
                verb = x[0]
                sentence = x[2]
                ST = y[2]
                coup = (verb, ST, sentence)
                Lista.append(coup)
    return Lista


def ReturnPositiveTrip(Ls, Ds):    
    D = {}
    Lista = []
    for x in Ls:        #per ogni tupla del file gdex
        for y in Ds:
            if x[0] == y[0] and x[1] == y[1]:
                verb = x[0]
                patternID = x[1]
                sentence = x[2]
                
                coup = (verb, patternID, sentence)
                Lista.append(coup)
    return Lista


def ReturnPositiveDict(Lista):
    D = {}
    for coup in Lista:
        if coup[0] not in D:
            
            D[coup[0]] = coup[1]
            
        else: 
            D[coup[0]] = D[coup[0]] + "/" + "|" + coup[1]
    
    for key in D: 
        D[key] = D[key].split("/")
        
    return D
           



#%% 

def FiltraDoppi(As):
    Ls = []
    for x in As:
        if x not in Ls: 
            Ls.append(x)
    return Ls

def FiltraAlternanze(As):              
    Ls = []
    for x in As:
        a = GetObjSlot(x[0], x[1])
        try:
            if len(a) == 1:
                Ls.append(x)
        except:
            pass
    return Ls





#%%

def ReturnQuad(A):
    As = []
    for trip in A:
    
        SemType = GetObjSlot(trip[0], trip[1])
        verb = trip[0]
        patternID = trip[1]
        sent = trip[2]
        
        quad = (SemType, verb, patternID, sent)
        As.append(quad)
    return As

def ReturnTypesPatt(Ds):
    Ls = []
    for patt in Ds:
        SemType = GetObjSlot(patt[0], patt[1])
        tup = (patt, SemType)
        Ls.append(tup)
    return Ls
        

def writefileA(As, filename): #As in formato tokvb, [tokobj], [ST], sentence
 
    fh = open(filename, "w", "latin-1")
    for x in As:
        a = str(x[1]).replace("['", "").replace("']", "").replace("'", "").replace('["l"]', "l'")
        b = str(x[2]).replace("['", "").replace("']", "").replace("'", "")
        try:
            fh.write(str(x[0]) + "|" + a + "|" + b + "|" + str(x[3]) + "\n")
        except: 
            pass
  
def writefileB(D, filename):
    fh = open(filename, "w", "latin-1")
    for key in D:
        fh.write(str(key))
        fh.write("|")
        
        clean = str(D[key]).replace("[", "").replace("]", "")
        fh.write(clean)
        fh.write("\n")
    fh.close()


import random
def ReturnRandom(Ls):
    randomlist = random.sample(range(0, 35566), 5000)
    Random = []
    for j in randomlist:
        Random.append(Ls[j])
    return Random




""""PARSING"""

import spacy
def HasObject(sentence):
    nlp = spacy.load('it_core_news_sm')
    doc = nlp(sentence)
    Ls = []
    for token in doc:
        Ls.append(token.dep_)
    if "obj" in Ls:
        return True 
    else:
        return False


def ReturnNegativeTransitive(Ls):
    Fs = []
    
    for sentence in Ls:
        if HasObject(sentence):
            Fs.append(sentence)
    return Fs

def getObject(sentence):
    nlp = spacy.load('it_core_news_sm')
    doc = nlp(sentence)
    Ls = []
    for token in doc:

        if token.dep_ == "obj":
             return token
         
            
         
""""parse with UDPIPE""" 
import spacy_udpipe           




""""returns the list of tokens tagged as "obj" in filename"""
     
def getObjectList(filename):
    fh = open(filename)
    testo = fh.read().split("\n")

    Ls = []
    for line in testo:
        obj = getObject(line)
        if obj != None:
            Ls.append(obj)
            
    return Ls



""" check if the token tagged as "obj" has the pattern verb as head """


def Check(filename):
    fh = open(filename)
    testo = fh.read().split("\n")
    
    for line in testo: 
        r = line.split("|")
    
        nlp = spacy.load("it_core_news_sm")
        doc = nlp(r[1])
        
        for token in doc:
            if token.dep_ == "obj":
        
                if token.dep_ == "obj" and token.head.lemma_ == r[0]:
                    print(token, " <=== ", token.head.lemma_)
                    
                    
                 
                    

#%%     

" FILTERING ALTERNATIONS "

import json
 
f = open('annot_download.json')

r = json.load(f)

TPASdata = []
for diz in r['data']:
    if diz["status"] == "WIP":
        TPASdata.append(diz)
        
"""" ritorna la lista dei st di un pattern"""

def GetObjSlot(verb, patternID):
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

""""UDPIPE PARSE"""

import spacy_udpipe

def GetObjectSUD(verb, sentence):
    nlp = spacy_udpipe.load("it")
    Ls = []
    doc = nlp(sentence)
    for token in doc:
        if token.head.lemma_ == verb and token.dep_ == "obj":
            Ls.append(token.text)
    return Ls
        
def getVerbSUD(verb, sentence):
    verb.replace("_1", "") 
    nlp = spacy_udpipe.load("it")
    doc = nlp(sentence)
    for token in doc:
        if token.lemma_==verb:
            return token.text
    
#prova = getVerb("accettare_1", "Come lo Sciri , ha accettato di entrare a far parte del Consiglio provvisorio .")

#%%
""""Stanza Parse"""

import stanza
#stanza.download('it')

def GetObjectS(verb, sentence):
    nlp = stanza.Pipeline(lang='it', processors='tokenize, pos, lemma')
    doc = nlp(sentence)
    print(doc)
    for token in doc:
        print(token.lemma)

    





"""il blocco che segue filtra le alternanze.
    FiltraAlternanzePos ritorna True se non ci sono alternanze o se sono tutte alternanze di tipi di PhysEnt,
    FiltraAlternanzeNeg ritorna True se non ci sono alternanze o se sono tutte alternanze di tipi di non-PhysEnt"""

def HaAlternanzePos(verb, patternID):
    PositiveTypes = ["Anything", "Entity", "Physical Entity", "Inanimate", "Artifact", "Weapon", "Projectile", "Firearm","Bomb","Beverage", "Alcoholic Drink", "Wine", "Garment", "Device", "Computer", "Food", "Dough", "Wall", "Floor", "Machine", "Vehicle", "Road Vehicle", "Water Vehicle", "Flying Vehicle", "Picture", "Sculpture", "Document", "Container", "Engine", "Furniture", "Flag", "Image", "Sound Maker", "Musical Instrument", "String", "Ball", "Drug", "Fuel", "Animate", "Human", "Human Group", "Business Enterprise", "Animal", "Cow", "Horse", "Dog", "Sheep", "Goat", "Snake", "Spider", "Bird", "Insect", "Fish", "Cat", "Animal Group", "Body", "Part of Body", "Bone", "Finger", "Hair", "Nail", "Head", "Plant", "Flower", "Fruit", "Location", "Route", "Natural Landscape Feature", "Body of Water", "Watercourse", "Hill", "Aperture", "Human1", "Human2", "Inanimate1", "Inanimate2"]
    a = GetObjSlot(verb, patternID)    

    for ST in a: 
        if ST not in PositiveTypes:
            return False
    return True 

def FiltraAlternanzePos(As): #As = (verb, pattern)
    Ls = []
    
    for x in As:
        try: 
            if HaAlternanzePos(x[0], x[1]) == True:
                ST = GetObjSlot(x[0], x[1])
                tup = (x[0], x[1], ST)
                Ls.append(tup)
        except: 
            pass
    return Ls
    
def HaAlternanzeNeg(verb, patternID):
    NegativeTypes = ["Abstract Entity", "Deity", "Fantasy Character", "Business Enterprise", "Resource", "Asset", "Deficit", "Money", "Psych", "Goal", "Attitude", "Emotion", "Number", "Numerical Value", "Money Value", "Quantity", "Time Period", "Time Point", "Concept", "Rule", "Permission", "Proposition", "Video", "Musical Composition", "Picture", "Sculpture", "Information", "Language", "Part of Language", "Name", "Software", "Field of Interest", "Narrative", "Obligation", "Responsibility", "Opportunity", "Power", "Uncertainty", "Privilege", "Limit", "Energy", "Wavelength", "Light", "Sound", "Signal", "Heat", "Particle", "Eventuality", "Event", "Process", "Weather Event", "Wind", "Fire", "Disease", "Activity", "Investigation", "Plan", "Performance",  "Speech Act", "Offer", "Agreement", "Command", "Request", "Question", "Claim", "Punctual Event", "Explosion", "Action", "Decision", "State", "Relationship", "Temperature", "System", "Illness", "Cognitive State", "Property", "Skill", "Colour", "Smell", "Role", "Injury", "Weight", "Reputation", "Event1", "Event2", "Eventuality1", "Eventuality2"]
    a = GetObjSlot(verb, patternID)
    for ST in a: 
        if ST not in NegativeTypes:
            return False
    return True 

def FiltraAlternanzeNeg(As): #As = (verb, pattern)
    Ls = []                     #Ls = (verb, pattern, st)
    for x in As:
        try:
            if HaAlternanzeNeg(x[0], x[1]) == True:
                ST = GetObjSlot(x[0], x[1])
                tup = (x[0], x[1], ST)
                Ls.append(tup) 
        except:
            pass
    return Ls


"""" appends the object and the verb token """

def AppendiObjAndVerb(Positive):
    Ls = []
    for trip in Positive: 
        token_verbo = getVerbSUD(trip[0], trip[2])
        token_obj = GetObjectSUD(trip[0], trip[2])
        ST = (trip[1])
        sentence = trip[2]
        tup = (token_verbo, token_obj, ST, sentence)
        Ls.append(tup)
    return Ls

""""appende st al file dei pattern"""

def AppendST(As):
    Ls = []
    for coup in As:
        ST = GetObjSlot(coup[0], coup[1])
        trip = (coup[0], coup[1], ST)
        Ls.append(trip)
    return Ls

















