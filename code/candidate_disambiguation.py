from rdflib import Graph, Literal, RDF, URIRef,RDFS,Namespace
import pickle
from candidate_generate import initial_candidate
import numpy as np
from rdflib import Graph, Literal, RDF, URIRef,RDFS,Namespace
import pickle

def discover_relation(s,o,f1,f2):
    ff=False
    dbpedia_e=Namespace('http://dbpedia.org/resource/') 
    s0=s[0].upper()
    if s0>'Z' or s0<'A':
        char='other'
    else:
        char=s0
        
    if f1==False and f2==False:
        f=open('../../KG/KG_data/triple/'+char+'_RDF_triple.data','rb')
        kg_tr=pickle.load(f)
        f.close()
    elif f1==False and f2==True:
        f=open('../../KG/KG_data/literal/'+char+'_RDF_literal.data','rb')
        kg_tr=pickle.load(f)
        f.close()
        
    O=list(map(str,list(kg_tr.objects(dbpedia_e[s],None))))
    if str(dbpedia_e[o]) in O:
        
        ff=True
        
    return ff
        
    
def candidate_disambiguation(WT,name,cc):
    
    N=WT.row_num
    C,w=initial_candidate(WT,N,name)
    F={}
    #pren=0
    for loc in C:
        #pren+=len(C[loc])
        print(type(C[loc]))
        F[loc]=np.zeros(len(C[loc]))
        
    for loc in C:
        
        if loc[1]!=cc:
            
            ucl=C[loc]
            cl=C[(loc[0],cc)]
            for i in range(len(ucl)):
                u=ucl[i]
                for j in range(len(cl)):
                    c=cl[j]
                    if list(set(u.rin).intersection(c.rout))!=[] and F[loc][i]==0:
                        ff=discover_relation(c.name,u.name,c.literal,u.literal)
                        if ff==True:
                            F[loc][i]=1
                            F[(loc[0],cc)][j]=1
                    elif list(set(u.rout).intersection(c.rin)) and F[loc][i]==0:
                        ff=discover_relation(u.name,c.name,u.literal,c.literal)
                        if ff==True:
                            F[loc][i]=1
                            F[(loc[0],cc)][j]=1
                              
    return F
"""
for i in range(1,9):
    try:
        F=candidate_disambiguation(WT_list[i],CD[i],ccc[CD[i]])
        f=open('CD_result/'+CD[i]+'_F.data','wb')
        pickle.dump(F,f)
        f.close()
        
    except:
        print(i)    
"""

