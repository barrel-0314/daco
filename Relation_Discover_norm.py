import pickle
import numpy as np
from rdflib import Graph, Literal, RDF, URIRef,RDFS,Namespace
from class_candidate import Candidate
from index_tree import find_triple

def other_dir(label):
    
    if len(label)==0 or ord(label[0])>1000:        
        dire='other/1000'
    elif '0'<=label[0]<='9':
        if label[0]!='1':
            dire='other/'+label[0]
        else:
            if len(label)==1:
                dire='other/non'
            elif '0'<=label[1]<='8':
                dire='other/08'
            elif label[1]=='9':
                dire='other/91'
            else:
                dire='other/non'
    elif ord(label[0])<=100:
        dire='other/100'
    else:
        dire='other/500'
    
    return dire

def obtain_column_pair(NS,Cs):
    
    ns=NS.reshape(1,-1)
    scol=np.argwhere(ns==1)[:,1].tolist()
    ocol=np.argwhere(ns==0)[:,1].tolist()
    pos=list(Cs.keys())
    R=list(set([i[0] for i in pos]))
    return scol,ocol,R
        
def obtain_relation(cl,tree_dict,word_dict):
    #dbpedia_e=Namespace('http://dbpedia.org/resource/') 
    #print(cl)
    if len(cl)!=0:
        clv={}
        #ff=0
        indexfile='index KG/'
        #print(char)
        for can in cl:
            if can.name not in clv:
                if len(can.name)==0:
                    cc='o'
                elif can.name[0]<='Z' and can.name[0]>='A':
                    cc='az'
                else:
                    cc='o'
                clv[can.name]=[]
            else:
                continue
            if can.literal==False:
                #print(cc)
                #print(can.name,list(kg_tr.objects(dbpedia_e[can.name],None)))
                clv[can.name]+=list(map(str,find_triple(can.name,True,tree_dict['ti_'+cc],word_dict['ti_'+cc],'ti','o',indexfile)))
                clv[can.name]+=list(map(str,find_triple(can.name,True,tree_dict['li_'+cc],word_dict['li_'+cc],'li','o',indexfile)))
                                
    else:
        clv={}
    return clv
def extract_object_column_candidate(r,Cs,O):

    OC={}
    for o in O:
        OC[o]=[]
        for pos in Cs:
            if pos[0]==r and pos[1]==o:
                for can in Cs[pos]:
                    OC[o].append(can.name)
                    
    return OC

                    
def identify_relation(clv,Cs,OC,O,Rel):
        
    for can in clv:
          #print(clv[can])
          V=list(set(clv[can]))
          #R=list(sum(clv[can]['rel'],[]))
          #print(V)
          for i in range(len(V)):
              v=V[i]
              vv=v.split('/')[-1]
              #rr=R[i].split('/')[-1]
              for o in O:
                  if vv in OC[o]:
                      loc=OC[o].index(vv)
                      if can not in Rel:
                          Rel[can]=[(o,loc,vv)]
                      else:
                          Rel[can].append((o,loc,vv))
    return Rel
                  
        
def relation_discovery(Cs,NS,Rel,RR,tree_dict,word_dict):
    
    S,O,R=obtain_column_pair(NS,Cs)
    Rel={}
    #print(S,O,R)
    #RR={}
    for s in S:
        
        for r in R:
            if (r,s) not in Rel:
                if (r,s) not in RR:
                    cl=Cs[(r,s)]
                    #print((r,s))
                    clv=obtain_relation(cl,tree_dict,word_dict)
                    RR[(r,s)]=clv
                #print(O)
                OC=extract_object_column_candidate(r,Cs,O)
                #print(OC)
                Rel[(r,s)]=identify_relation(RR[(r,s)],Cs,OC,O,{})
            else:
                #print(O)
                OC=extract_object_column_candidate(r,Cs,O)
                #print(OC)
                Rel[(r,s)]=identify_relation(RR[(r,s)],Cs,OC,O,Rel[(r,s)])
                
    return Rel,RR,S,O,R