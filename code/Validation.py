import pickle
import random
import read_data
import numpy as np
import candidate_generate
from class_candidate import Candidate
import candidate_iter
import Relation_Discover

def valid_sample(WT,Cs,vld_num):
    
    iter_row=list(set([i[0] for i in list(Cs.keys())]))
    sam_rag=list(set(range(WT.row_num)).difference(iter_row))
    vld_row=random.sample(sam_rag, vld_num)
    '''
    vld_con=[]
    for i in range(WT.row_num):
        
        if i in vld_row:
            vld_con.appemd(WT.content[i])
    '''        
    return vld_row

def valid_candidate_initial(ns,vld_row,who_con,wt_name,db,tree_dict,word_dict):
    
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
        
        
    f=open(can_f+wt_name+'_can_set.data','rb')
    C=pickle.load(f)
    f.close()
    Can={}
    Can_w={}
    for r in range(len(vld_row)):
        for c in range(ns):
            
            #Can[(s,c)]=[]
            #print(WT.content[sample_row[r]][c],sample_row[r])
            l=who_con[vld_row[r]][c].split('(')[0]
            
            if l not in C:
                result=[]
            else:
                result=candidate_generate.topk_candidate_search(C[l],5,l)
            
            Can[(vld_row[r],c)]=result
    #print(tree_dict['ty_o'].root.values)
    Canv=list(Can.values())
    Canl=sorted(list(set(sum(Canv,[]))))
    #print(Canl)
    C_type,C_rout,C_rin=candidate_generate.candidate_type(Canl,tree_dict,word_dict)
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
                norm_c=Candidate(can,who_con[pos[0]][pos[1]].split('(')[0],-1,C_type[can],pos,False,C_rin[can],C_rout[can])
                Can_set[pos].append(norm_c)
        else:
            
            l=who_con[pos[0]][pos[1]].split('(')[0]
            if len(l)<5:
                n=len(l)
            else:
                n=5
            if len(l)!=0:
                result,c_rel=candidate_generate.candidate_search_in_literal(l,5,n,tree_dict,word_dict)
            else:
                result=[]
            for r in result:
                
                norm_c=Candidate(r,who_con[pos[0]][pos[1]].split('(')[0],-1,[],pos,True,c_rel[r],[])
                Can_set[pos].append(norm_c)
                Can_w[pos].append(c)
     
    return Can_set,Can_w
    
def valid_type_score(Cs,Cw,WT,ctf):

    cs=candidate_iter.candidate_score(Cs,Cw,WT.number_start)
    Cot=candidate_iter.column_type(Cs,cs) 
    Tw=candidate_iter.initial_type_weight(Cot)
    cot=candidate_iter.weight_column_type_score(Cot,Tw)
    v_ctf=candidate_iter.column_type_filter(cot)
    
    type_score={}
    for j in range(WT.number_start):
        
       upp=len(set(ctf[j]).intersection(v_ctf[j]))
       low=min(len(ctf[j]),len(v_ctf[j]))
       #low=len(set(ctf[j]).union(v_ctf[j]))
       if low==0:
           type_score[j]=1
       else:
           type_score[j]=upp/(low)
        
    return v_ctf,type_score

def valid_filter_candidate(ctf,v_ctf,wt_name,Vs,ns):
    
    for pos in Vs:
        ct=v_ctf[pos[1]]
        if len(ct)!=0:
            canl_new=[]
            for can in Vs[pos]:
            
                can_ct=list(set(can.c_type+can.rin))
                
                for i in range(len(can_ct)):
                    can_ct[i]=str(can_ct[i]).split('/')[-1]
                    
                #print(can_ct)
                s=len(set(can_ct).intersection(ct))/len(ct)
                #print(s)
                if s>0.7:
                
                    canl_new.append(can)
                
            Vs[pos]=canl_new
        
    return Vs


def valid_relation_score(Vs,tree_dict,word_dict,ns):
    
    Rel={}
    RR={}
    CR={}
    CRs={}
    for j in range(ns):
        
        NS=np.zeros(ns)
        NS=NS.reshape(-1,1)
        NS[j]=1
        Rel,RR,S,O,R=Relation_Discover.relation_discovery(Vs,NS,Rel,RR,tree_dict,word_dict)
        
        for cp in Rel:
            if cp[1] in S:
                canl=Vs[cp]
                for can in canl:
                    if can.name in Rel[cp]:
                        for r in Rel[cp][can.name]:
                            #r=Rel[cp][can.name]['node'][i]
                            
                            #print(r)
                            if r[0] in O:
                                
                                if (cp[1],r[0]) not in CR:
                                    
                                    CR[(cp[1],r[0])]=[cp[0]]
                                    
                                else:
                                    
                                    if cp[0] not in CR[(cp[1],r[0])]:
                                        
                                        CR[cp[1],r[0]].append(cp[0])
                                        
        CRs[j]=0
        
    for p in CR:
        
        CRs[p[0]]+=len(CR[p])
    
    return CR,CRs

def valid_main(wt_name,WT,Cs,ctf,vld_num,td,wd,db,cc):
    
    vld_flag=1
    
    vld_row=valid_sample(WT,Cs,vld_num)  
    Vs,Vw=valid_candidate_initial(WT.number_start,vld_row,WT.content,wt_name,db,td,wd)
    v_ctf,ts=valid_type_score(Vs,Vw,WT,ctf)
    #print(v_ctf)
    if np.mean(np.array(list(ts.values())))<0.5:
        
        vld_flag=0
        
    else:    
        
        Vs=valid_filter_candidate(ctf,v_ctf,wt_name,Vs,WT.number_start)
        CR,crs=valid_relation_score(Vs,td,wd,WT.number_start)
        
        mc=max(list(crs.values()))
        if crs[cc]!=mc:
            vld_flag=0
    
    return vld_flag,vld_row,Vs

'''    
db='iswc'
M,WL=read_data.read_data_sample(db)  

i=35
f=open(db+'_result/'+M[i]+'_cw.data','rb')
Cw=pickle.load(f)
f.close()
f=open(db+'_result/'+M[i]+'_ctf.data','rb')
ctf=pickle.load(f)
f.close()
td,wd=candidate_generate.read_index_info()

vf,vr,vc,cr=valid_main(M[i],WL[i],Cw,ctf,3,td,wd,db,0)

vld_row=valid_sample(WL[i],Cw,3)  
td,wd=candidate_generate.read_index_info()
Vs,Vw=valid_candidate_initial(WL[i].number_start,vld_row,WL[i].content,M[i],db,td,wd)
v_ctf,ts=valid_type_score(Vs,Vw,WL[i],ctf)
Vs=valid_filter_candidate(ctf,v_ctf,M[i],Vs,WL[i].number_start)
CR,crs=valid_relation_score(Vs,td,wd,WL[i].number_start)
'''