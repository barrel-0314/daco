import pickle
import Levenshtein
from rdflib import Graph, Literal, RDF, URIRef,RDFS,Namespace
from class_candidate import Candidate
import random
from rdflib.namespace import FOAF,XSD,OWL
from index_tree import find_triple,read_tree
import os
from read_data import read_data_sample
from string_index_test import candidate_index
import difflib

def other_dir(label):
    
    if len(label)==0 or ord(label[0])>1000:        
        dire='other/1000'
    elif '1'<=label[0]<='9':
        if label[0]!='1'and label:
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
    elif label[0]=='0':
        
        dire='other/non'
    elif ord(label[0])<=100:
        dire='other/100'
    else:
        dire='other/500'
    
    return dire

def find_distance_inlist(L,label,n,c,lit):
    
    if lit==False:
        for l in L:
        
            firstsplit=l.split('/')
            entity1=firstsplit[-1]
            #entity2=(firstsplit[-1].split('>'))[0]
        
            if entity1 not in c.keys():
            
                if Levenshtein.distance(label,entity1)<n:
                
                    c[entity1]=Levenshtein.distance(label,entity1)
                    
    else:
        for l in L:
            
            if l not in c.keys():
                
                if Levenshtein.distance(label,l)<n:
                    c[l]=Levenshtein.distance(label,l)

    return c

def candidate_search(label,k,n):
    label2=label[0]
    result=[]
    candidate={}
    #n=len(label)
    s=label2[0].upper()
    if s>='A' and s<='Z':
        f=open('../../KG/KG_data/triple/'+s+'_RDF_triple.data','rb')
        KG_o=pickle.load(f)
        f.close()
        f=open('../../KG/KG_data/triple_reverse/'+s+'_triple_reverse.data','rb')
        KG_or=pickle.load(f)
        f.close()
        
    else:
        f=open('../../KG/KG_data/triple/'+'other'+'_RDF_triple.data','rb')
        KG_o=pickle.load(f)
        f.close()
        f=open('../../KG/KG_data/triple_reverse/'+'other'+'_triple_reverse.data','rb')
        KG_or=pickle.load(f)
        f.close()
        
    L=list(map(str,list(KG_o.subjects())))
    candidate=find_distance_inlist(L,label,n,candidate,False)
        
    L=list(map(str,list(KG_or.objects())))

    candidate=find_distance_inlist(L,label,n,candidate,False)
    
    #KG_o.close()
    #KG_or.close()    
    candidate=sorted(candidate.items(),key=lambda kv:(kv[1],kv[0]))
    result_whole=[c[0] for c in candidate]                   

    if len(candidate)>k:
        
        candidate=candidate[0:k]
        
    result=[c[0] for c in candidate]
    return result,result_whole

def candidate_search_in_literal(label,k,n,tree_dict,word_dict):
    #print(label)
    result=[]
    candidate={}
    C_rel={}
    if len(label)!=0:
        s=label[0].upper()
        if s<'A' or s>'Z':
            s=other_dir(label).replace('/','_')
            #f=open('../../KG/KG_data/literal_reverse/'+s+'_other_reverse.data','rb')
            s_index=candidate_index(label,True)
        else:
            s_index=candidate_index(label,True)
            #f=open('../../KG/KG_data/literal_reverse/'+s+'_literal_reverse.data','rb')
    '''
    else:
        s=other_dir(label)        
        f=open('../../KG/KG_data/literal_reverse/'+s+'_other_reverse.data','rb')
    
    g=pickle.load(f)
    f.close()
    L=list(map(str,list(g.objects())))
    '''
    flen=len(s_index)
    for ff in range(flen):
        
        st=s_index[ff][0]
        ed=s_index[ff][1]
        f=open('../../KG/list_data_char_index/'+s+'_ll/'+str(st)+'_to_'+str(ed)+'.data','rb')
        ll=pickle.load(f)
        f.close()
        candidate=find_distance_inlist(ll,label,n,candidate,True)
        
    #candidate=find_distance_inlist(L,label,n,candidate,True)
    candidate=sorted(candidate.items(),key=lambda kv:(kv[1],kv[0]))
    if len(candidate)>k:
        
        candidate=candidate[0:k]
        
    result=[c[0] for c in candidate]
    indexfile='../../KG/index KG/'
    for r in result:
        #C_rel[r]=[]
        if len(r)==0:
            cc='o'
        elif r[0]<='Z' and r[0]>='A':
            cc='az'
        else:
            cc='o'
        C_rel[r]=list(set(find_triple(r,True,tree_dict['lr_'+cc],word_dict['lr_'+cc],'lr','p',indexfile)))

        #rel=list(set((g.predicates(None,Literal(r)))))
        #C_rel[r]=rel
    
    return result,C_rel    


def candidate_search_in_literal2(label,k,n,tree_dict,word_dict):
    #print(label)
    result=[]
    candidate={}
    C_rel={}
    if len(label)!=0:
        s=label[0].upper()
        if s<'A' or s>'Z':
            s=other_dir(label)
            #s=other_dir(label).replace('/','_')
            f=open('../../KG/KG_data/literal_reverse/'+s+'_other_reverse.data','rb')
            #s_index=candidate_index(label,True)
        else:
            #s_index=candidate_index(label,True)
            f=open('../../KG/KG_data/literal_reverse/'+s+'_literal_reverse.data','rb')
    
    else:
        s=other_dir(label)        
        f=open('../../KG/KG_data/literal_reverse/'+s+'_other_reverse.data','rb')
    
    g=pickle.load(f)
    f.close()
    L=list(map(str,list(g.objects())))
    '''
    flen=len(s_index)
    for ff in range(flen):
        
        st=s_index[ff][0]
        ed=s_index[ff][1]
        f=open('../../KG/list_data_char_index/'+s+'_ll/'+str(st)+'_to_'+str(ed)+'.data','rb')
        ll=pickle.load(f)
        f.close()
        candidate=find_distance_inlist(ll,label,n,candidate,True)
        
    #candidate=find_distance_inlist(L,label,n,candidate,True)
    candidate=sorted(candidate.items(),key=lambda kv:(kv[1],kv[0]))
    '''
    can=difflib.get_close_matches(label, L)
    

    if len(can)>k:
        
        candidate=can[0:k]
    else:
        candidate=can
    result=candidate
    
    indexfile='../../KG/index KG/'
    for r in result:
        #C_rel[r]=[]
        if len(r)==0:
            cc='o'
        elif r[0]<='Z' and r[0]>='A':
            cc='az'
        else:
            cc='o'
        C_rel[r]=list(set(find_triple(r,True,tree_dict['lr_'+cc],word_dict['lr_'+cc],'lr','p',indexfile)))

        #rel=list(set((g.predicates(None,Literal(r)))))
        #C_rel[r]=rel
    
    return result,C_rel    
def identify_file(candidate):

    if len(candidate)==0:
        ch='other'
    else:
        if 'A'<=candidate[0].upper()<='Z':
            ch=candidate[0].upper()
        else:
            ch='other'
            
    return ch

def candidate_search_simplify(label,s_index,k,n):
    
    if len(label)==0:
        S='other'
    else:
        
        label2=label[0]
        s=label2[0].upper() 
        if s>='A' and s<='Z':
            S=s
        else:
            S='other'
    result=[]
    candidate={}
    #n=len(label)
    
    """  
    if s>='A' and s<='Z':
        f=open('../../KG/list_data_char/'+s+'_elist.data','rb')
        el=pickle.load(f)
        f.close()
        
    else:
        s='other'
        f=open('../../KG/list_data_char/'+s+'_elist.data','rb')
        el=pickle.load(f)
        f.close()        
    """
    flen=len(s_index)
    for ff in range(flen):
        
        st=s_index[ff][0]
        ed=s_index[ff][1]
        f=open('../../KG/list_data_char_index/'+S+'_el/'+str(st)+'_to_'+str(ed)+'.data','rb')
        el=pickle.load(f)
        f.close()
        candidate=find_distance_inlist(el,label,n,candidate,False)
        
    
    candidate=sorted(candidate.items(),key=lambda kv:(kv[1],kv[0]))
    result_whole=[c[0] for c in candidate]                   

    if len(candidate)>k:
        
        candidate=candidate[0:k]
        
    result=[c[0] for c in candidate]
    return result,result_whole

def candidate_search_simplify2(label,k,n):
    
    if len(label)==0:
        S='other'
    else:
        
        label2=label[0]
        s=label2[0].upper() 
        if s>='A' and s<='Z':
            S=s
        else:
            S='other'
    result=[]
    candidate={}
    #n=len(label)
    
      
    if s>='A' and s<='Z':
        f=open('../../KG/list_data_char/'+S+'_elist.data','rb')
        el=pickle.load(f)
        f.close()
        
    else:
        s='other'
        f=open('../../KG/list_data_char/'+s+'_elist.data','rb')
        el=pickle.load(f)
        f.close()        
    

    can=difflib.get_close_matches(label, el)
    

    if len(can)>k:
        
        candidate=can[0:k]
    else:
        candidate=can
    result=candidate
    return result,can
#def candidate_search_literal_simplify(label,k,n): 

          
def candidate_type(candidate,tree_dict,word_dict):
    #dbpedia_e=Namespace('http://dbpedia.org/resource/') 
    #dbpedia_t=Namespace('http://dbpedia.org/ontology/')
    C_type={}
    C_rin={}
    C_rout={}
    indexfile='../../KG/index KG/'
    for c in candidate:
        
        if len(c)==0:
            cc='o'
        elif c[0]<='Z' and c[0]>='A':
            cc='az'
        else:
            cc='o'
            
        #print(cc,c)
        C_type[c]=list(set(find_triple(c,True,tree_dict['ty_'+cc],word_dict['ty_'+cc],'ty','o',indexfile)))
        C_rin[c]=list(set(find_triple(c,True,tree_dict['tr_'+cc],word_dict['tr_'+cc],'tr','p',indexfile)))
        C_rout[c]=list(set(find_triple(c,True,tree_dict['ti_'+cc],word_dict['ti_'+cc],'ti','p',indexfile)))
        
        
    """
    filelist=['other']+[chr(y) for y in range(65, 91)]+['other']
    
    if len(candidate[0])==0:
        char='other'
    else:
        if 'A'<=candidate[0][0].upper()<='Z':
            char=candidate[0][0].upper()
        else:
            char='other'
    
    loc=0
    terminate=False
    #print(len(candidate))
    for ch in filelist:
        
        if identify_file(candidate[loc])==ch:
            f=open('../../KG/KG_data/type/'+ch+'_RDF_type.data','rb')
            KG_type=pickle.load(f)
            f.close()
            f=open('../../KG/KG_data/triple/'+ch+'_RDF_triple.data','rb')
            KG_tri=pickle.load(f)
            f.close()
            f=open('../../KG/KG_data/triple_reverse/'+ch+'_triple_reverse.data','rb')
            KG_tri_rev=pickle.load(f)
            f.close()
            
        while identify_file(candidate[loc])==ch:
            c=candidate[loc]
            c_t=list(KG_type.objects(dbpedia_e[c],None))
            C_type[c]=c_t
            c_ro=list(set((KG_tri.predicates(dbpedia_e[c],None))))
            C_rout[c]=c_ro

            c_ri=list(set((KG_tri_rev.predicates(None,dbpedia_e[c]))))
            C_rin[c]=c_ri
                 
            loc+=1
            #print(loc)
            if loc==len(candidate):
                terminate=True
                break
                
        if terminate==True:
            break
    """
    return C_type,C_rout,C_rin
            

def topk_candidate_search(candidate,k,label):
    
    C={}
    
    for c in candidate:
        C[c]=Levenshtein.distance(c,label)
        
    cc=sorted(C.items(),key=lambda kv:(kv[1],kv[0]))    
    if len(candidate)>k:
        
        cc=cc[0:k]
            
    result=[i[0] for i in cc]
    return result





"""    
def initial_candidate(WT,name):
    
    #sample_row=random.sample(range(BWT.row_num),N)
    f=open('candidate_set/'+name+'_can_set.data','rb')
    C=pickle.load(f)
    f.close()
    #C=candidate_main(WT)
    Can={}
    Can_w={}
    for r in range(WT.row_num):
        for c in range(WT.number_start):
            
            #Can[(s,c)]=[]
            l=WT.content[r][c]
            #print(l)
            if ' ' in l:
                l=l.replace(' ','_')
                #print(l)
                
            
            if len(l)<5:
                n=len(l)
            else:
                n=5
            can=candidate_search(l,5,n)
            
            #print(can)
            result=topk_candidate_search(C[l],5,l)
            Can[(r,c)]=result
    #Cank=list(Can.keys())
    Canv=list(Can.values())
    Canl=sorted(list(set(sum(Canv,[]))))
    C_type,C_rout,C_rin=candidate_type(Canl)
    #discover candidate info
    
    Can_set={}
    for pos in Can:
        Can_set[pos]=[]
        Can_w[pos]=[]
        if len(Can[pos])!=0:
            
            for can in Can[pos]:
                Can_w[pos].append(1)
                if can not in C_type:
                    C_type[can]=[]
                if can not in C_rin:
                    C_rin[can]=[]
                if can not in C_rout:
                    C_rout[can]=[]
                norm_c=Candidate(can,WT.content[pos[0]][pos[1]],-1,C_type[can],pos,False,C_rin[can],C_rout[can])
                Can_set[pos].append(norm_c)
        else:
            l=WT.content[pos[0]][pos[1]]
            if len(l)<5:
                n=len(l)
            else:
                n=5
            result,c_rel=candidate_search_in_literal(l,5,n)
            for r in result:
                
                norm_c=Candidate(r,WT.content[pos[0]][pos[1]],-1,[],pos,True,c_rel[r],[])
                Can_set[pos].append(norm_c)
                Can_w[pos].append(c)
     
    return Can_set,Can_w
    
"""
def read_index_info():
    word_dict={}
    tree_dict={}
    fl=['ti','tr','li','lr','ty']
    wl=['az','o']
    
    for ff in fl:
        
        for ww in wl:
            
            T,L=read_tree(ff+'_wl_'+ww)
            word_dict[ff+'_'+ww]=L
            tree_dict[ff+'_'+ww]=T
                     
    return tree_dict,word_dict
         
   
    
def initial_candidate2(WT,name,N,ifsample,db):
    
    
    if db=='iswc':
        
        can_f='candidate_set/'
        res='iswc_result/'
        
    elif db=='t2d':
        
        can_f='../../web_table/candidate_set/'
        res='t2d_result/'
        
    elif db=='git':
        
        can_f='../../web_table/git_candidate/'
        res='git_result/'
        
    elif db=='wiki':
        
        can_f='../../web_table/wiki_candidate/'
        res='wiki_result/'
    elif db=='t2dc':
        
        can_f='../../web_table/t2dc_candidate/'
        res='t2dc_result/' 
        
    elif db=='santos':
        
        can_f='../../web_table/santos_candidate/'
        res='santos_result/' 
        
    elif db=='multicc':
        
        can_f='../../web_table/multicc_candidate/'
        res='multicc_result/' 
        
    if ifsample==True:
        sample_row=random.sample(range(WT.row_num),N)
    else:
        f=open(res+name+'_cw.data','rb')
        cw=pickle.load(f)
        f.close()
        sample_row=[]
        
        for rr in cw:
            
            if rr[0] not in sample_row:
                
                sample_row.append(rr[0])
        
    f=open(can_f+name+'_can_set.data','rb')
    #f=open('../../web_table/wiki_candidate/'+name+'_can_set.data','rb')
    #f=open('candidate_set/'+name+'_can_set.data','rb')
    #f=open('example_t2d.data','rb')
    C=pickle.load(f)
    f.close()
    #C=candidate_main(WT)
    Can={}
    Can_w={}
    #print(sample_row)
    for r in range(N):
        for c in range(WT.number_start):
            
            #Can[(s,c)]=[]
            #print(WT.content[sample_row[r]][c],sample_row[r])
            l=WT.content[sample_row[r]][c].split('(')[0]
            
            #print(l)
            #if ' ' in l:
            #    l=l.replace(' ','_')
                #print(l)
                
            """
            if len(l)<5:
                n=len(l)
            else:
                n=5
            can=candidate_search(l,5,n)
            """
            #print(can)
            #print(C[l])
            if l not in C:
                result=[]
            else:
                result=topk_candidate_search(C[l],5,l)
            
            Can[(sample_row[r],c)]=result
            #print(l,result)
    #Cank=list(Can.keys())
    tree_dict,word_dict=read_index_info()
    #print(tree_dict['ty_o'].root.values)
    Canv=list(Can.values())
    Canl=sorted(list(set(sum(Canv,[]))))
    #print(Canl)
    C_type,C_rout,C_rin=candidate_type(Canl,tree_dict,word_dict)
    #discover candidate info
    
    Can_set={}
    for pos in Can:
        Can_set[pos]=[]
        Can_w[pos]=[]
        if len(Can[pos])!=0:
            
            for can in Can[pos]:
                Can_w[pos].append(1)
                if can not in C_type:
                    C_type[can]=[]
                if can not in C_rin:
                    C_rin[can]=[]
                if can not in C_rout:
                    C_rout[can]=[]
                norm_c=Candidate(can,WT.content[pos[0]][pos[1]].split('(')[0],-1,C_type[can],pos,False,C_rin[can],C_rout[can])
                Can_set[pos].append(norm_c)
        else:
            
            l=WT.content[pos[0]][pos[1]].split('(')[0]
            if len(l)<5:
                n=len(l)
            else:
                n=5
            if len(l)!=0:
                result,c_rel=candidate_search_in_literal(l,5,n,tree_dict,word_dict)
            else:
                result=[]
            for r in result:
                
                norm_c=Candidate(r,WT.content[pos[0]][pos[1]].split('(')[0],-1,[],pos,True,c_rel[r],[])
                Can_set[pos].append(norm_c)
                Can_w[pos].append(c)
     
    return Can_set,Can_w,tree_dict,word_dict

def initial_candidate3(WT,name,N,ifsample):
    
    if ifsample==True:
        sample_row=random.sample(range(WT.row_num),N)
    else:
        f=open('index_result/row'+name+'_cw.data','rb')
        cw=pickle.load(f)
        f.close()
        sample_row=[]
        
        for rr in cw:
            
            if rr[0] not in sample_row:
                
                sample_row.append(rr[0])
        
    f=open('index_result/row'+name+'_can_set.data','rb')
    #f=open('../../web_table/wiki_candidate/'+name+'_can_set.data','rb')
    #f=open('candidate_set/'+name+'_can_set.data','rb')
    #f=open('example_t2d.data','rb')
    C=pickle.load(f)
    f.close()
    #C=candidate_main(WT)
    Can={}
    Can_w={}
    #print(sample_row)
    for r in range(N):
        for c in range(WT.number_start):
            
            #Can[(s,c)]=[]
            #print(WT.content[sample_row[r]][c],sample_row[r])
            l=WT.content[sample_row[r]][c].split('(')[0]
            
            #print(l)
            #if ' ' in l:
            #    l=l.replace(' ','_')
                #print(l)
                
            """
            if len(l)<5:
                n=len(l)
            else:
                n=5
            can=candidate_search(l,5,n)
            """
            #print(can)
            #print(C[l])
            if l not in C:
                result=[]
            else:
                result=topk_candidate_search(C[l],5,l)
            
            Can[(sample_row[r],c)]=result
            #print(l,result)
    #Cank=list(Can.keys())
    tree_dict,word_dict=read_index_info()
    #print(tree_dict['ty_o'].root.values)
    Canv=list(Can.values())
    Canl=sorted(list(set(sum(Canv,[]))))
    #print(Canl)
    C_type,C_rout,C_rin=candidate_type(Canl,tree_dict,word_dict)
    #discover candidate info
    
    Can_set={}
    for pos in Can:
        Can_set[pos]=[]
        Can_w[pos]=[]
        if len(Can[pos])!=0:
            
            for can in Can[pos]:
                Can_w[pos].append(1)
                if can not in C_type:
                    C_type[can]=[]
                if can not in C_rin:
                    C_rin[can]=[]
                if can not in C_rout:
                    C_rout[can]=[]
                norm_c=Candidate(can,WT.content[pos[0]][pos[1]].split('(')[0],-1,C_type[can],pos,False,C_rin[can],C_rout[can])
                Can_set[pos].append(norm_c)
        else:
            
            l=WT.content[pos[0]][pos[1]].split('(')[0]
            if len(l)<5:
                n=len(l)
            else:
                n=5
            if len(l)!=0:
                result,c_rel=candidate_search_in_literal2(l,5,n,tree_dict,word_dict)
            else:
                result=[]
            for r in result:
                
                norm_c=Candidate(r,WT.content[pos[0]][pos[1]].split('(')[0],-1,[],pos,True,c_rel[r],[])
                Can_set[pos].append(norm_c)
                Can_w[pos].append(c)
     
    return Can_set,Can_w,tree_dict,word_dict



def candidate_main(WT):
    C={}
    for r in range(WT.row_num):
        
        for c in range(WT.column_num):
            
            mention=WT.content[r][c].split('(')[0]
            if mention not in C:
                
                if len(mention)<5:
                    n=len(mention)
                else:
                    n=5
                if len(mention)!=0:
                    s_index=candidate_index(mention, False)
                    re,rew=candidate_search_simplify(mention,s_index,5,n)
                else:
                    rew=[]
                C[mention]=rew
    
    return C

def candidate_main2(WT):
    C={}
    for r in range(WT.row_num):
        
        for c in range(WT.number_start):
            
            mention=WT.content[r][c].split('(')[0]
            if mention not in C:
                
                if len(mention)<5:
                    n=len(mention)
                else:
                    n=5
                if len(mention)!=0:
                    #s_index=candidate_index(mention, False)
                    re,rew=candidate_search_simplify2(mention,5,n)
                else:
                    rew=[]
                C[mention]=rew
    
    return C
def candidate_main_remend(WT,name):
    #C={}
    f=open('candidate_set/'+name+'_can_set.data','rb')
    #f=open('candidate_set/'+name+'_can_set.data','rb')
    #f=open('example_t2d.data','rb')
    C=pickle.load(f)
    f.close()
    for r in range(WT.row_num):
        
        for c in range(WT.number_start):
            
            mention=WT.content[r][c].split('(')[0]
            #print(mention)
            if mention not in C:
                
                if len(mention)<5:
                    n=len(mention)
                else:
                    n=5
                    
                s_index=candidate_index(mention, False)
                re,rew=candidate_search_simplify(mention,s_index,5,n)
                C[mention]=rew
    
    return C


mention='Machester'
#Canl=['Calgary']
s_index=candidate_index(mention, False)
re,rew=candidate_search_simplify(mention,s_index,5,5)
'''
td,wd=read_index_info()
C_type2,C_rout2,C_rin2=candidate_type(Canl,td,wd)

M,WL=read_data_sample('santos')
F=[]
N_total=0
N_rate=0
for i in range(len(M)):
    
    try:
        N_total+=WL[i].row_num*WL[i].column_num
        f=open('../../web_table/santos_candidate/'+M[i]+'_can_set.data','rb')
        C=pickle.load(f)
        f.close()
        for c in C:
            if len(C[c])==0:
                N_rate+=1
        #Cs,_,_,_=initial_candidate2(WL[i],M[i],N,ifsample,db)
    except:
        F.append(M[i])
'''    
'''
F=[]
M,WL=read_data_sample('multicc')

f=open('need_multi.data','rb')
nd=pickle.load(f)
f.close()
for i in range(94):
    
    t=M[i]
    #if t+'_can_set.data' not in lccl:
        
    try:
        if M[i] in nd:
            C=candidate_main(WL[i])
            f=open('../../web_table/multicc_candidate/'+t+'_can_set.data','wb')
            pickle.dump(C,f)
            f.close()
    except:
        F.append(i)
        

'''        


#td,wd=read_index_info()
#T=[]
"""
for i in range(5,56):
    
    loc=t.index(T[i])
    try:
        C=candidate_main(WT_list[loc])
        f=open('../../web_table/candidate_set/'+t[loc]+'_can_set.data','wb')
        pickle.dump(C,f)
        f.close()
        
    except:
        #T.append(t[i])
        print(t[loc])
""" 

#Cs,Cw,td,wd=initial_candidate2(WT_list[4],t[4],2)
 